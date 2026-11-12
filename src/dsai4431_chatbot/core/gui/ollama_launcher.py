"""Ollama 的探测、「接管」与「按需拉起」。

用户的决定（2026-11-12）：**这个程序要掌管 Ollama**。
启动时先看端口：已经有别的 Ollama 在跑，就关掉它，然后按设置里的路径
（可执行文件 + 模型目录）重新起一个。这样"实际用的是哪份模型"永远等于
设置页显示的那份，不会悄悄复用外面的服务。

三条规矩：
1. 先探测 `GET /api/tags`；通着就**接管**（见 `stop_foreign`）
2. 只在后台线程里调（`rag_service` 的同步任务），别卡启动
3. **只关进程名叫 ollama 的**：端口被别的东西占着就报错放手，绝不乱杀
4. 退出时只关自己 Popen 出来的那份（记在模块级 `_owned`）

`ensure_running()` 的 `command` 参数是给测试用的钩子：
真实路径是 `[ollama.exe, "serve"]`，测试里换成 `[python, stub.py, "serve"]`。
传了它就不做接管（测试里的"服务"是 python 假进程，不能被 taskkill）。
"""

from __future__ import annotations

import os
import subprocess
import sys
import time
import urllib.error
import urllib.request
from dataclasses import dataclass
from pathlib import Path
from urllib.parse import urlsplit

DEFAULT_BASE_URL = "http://127.0.0.1:11434"
DEFAULT_PORT = 11434
# 探测超时：短一点，探测失败是正常路径（没装/没启动）
PROBE_TIMEOUT_S = 0.6
# 拉起后最长等多久才算「起来了」
WAIT_READY_S = 20.0
# Windows 下别弹黑窗口
_CREATE_NO_WINDOW = 0x08000000

_owned: subprocess.Popen | None = None


@dataclass
class LaunchResult:
    """`detail` 是给界面用的短语，i18n 里按它挑文案。"""

    ok: bool = False
    started: bool = False
    # already_running / started / took_over / disabled / no_exe /
    # timeout / failed / port_busy
    detail: str = ""
    exe: str = ""

    @property
    def message_key(self) -> str:
        return f"settings.rag.ollama_{self.detail or 'failed'}"


# ---------------------------------------------------------------------------
# 探测
# ---------------------------------------------------------------------------
def base_url(cfg=None) -> str:
    raw = ""
    if cfg is not None:
        raw = str(getattr(cfg, "rag_ollama", "") or "")
    return (raw or DEFAULT_BASE_URL).strip().rstrip("/")


def tags_url(url: str) -> str:
    return f"{url}/api/tags"


def is_alive(url: str = DEFAULT_BASE_URL, timeout: float = PROBE_TIMEOUT_S) -> bool:
    """`GET /api/tags` 有响应就算活着（Ollama 会回一段 JSON）。"""
    try:
        with urllib.request.urlopen(tags_url(url), timeout=timeout) as response:
            return 200 <= int(getattr(response, "status", 200)) < 300
    except (urllib.error.URLError, OSError, ValueError, TimeoutError):
        return False


# ---------------------------------------------------------------------------
# 接管：把端口上**别人**的 Ollama 关掉
# ---------------------------------------------------------------------------
def url_port(url: str = DEFAULT_BASE_URL) -> int:
    """从 base_url 里取端口；解析不出来就按 11434。"""
    try:
        parts = urlsplit(url)
        return int(parts.port or DEFAULT_PORT)
    except (ValueError, TypeError):
        return DEFAULT_PORT


def listener_pids(port: int) -> list[int]:
    """监听该端口的 PID 列表。

    用 netstat 而不是 psutil：项目刻意保持零第三方依赖。
    """
    if sys.platform != "win32":
        return []
    try:
        output = subprocess.run(  # noqa: S603,S607 - 固定命令，无用户输入
            ["netstat", "-ano", "-p", "TCP"],
            capture_output=True,
            text=True,
            timeout=8,
            creationflags=_CREATE_NO_WINDOW,
        ).stdout
    except (OSError, subprocess.SubprocessError):
        return []

    pids: list[int] = []
    for line in output.splitlines():
        parts = line.split()
        if len(parts) < 5 or parts[3].upper() != "LISTENING":
            continue
        if not parts[1].endswith(f":{port}"):
            continue
        try:
            pids.append(int(parts[4]))
        except ValueError:
            continue
    return pids


def process_name(pid: int) -> str:
    """PID 对应的进程名（小写，带 .exe）；查不到返回空串。"""
    try:
        output = subprocess.run(  # noqa: S603,S607
            ["tasklist", "/FI", f"PID eq {pid}", "/FO", "CSV", "/NH"],
            capture_output=True,
            text=True,
            timeout=8,
            creationflags=_CREATE_NO_WINDOW,
        ).stdout.strip()
    except (OSError, subprocess.SubprocessError):
        return ""
    if not output or output.startswith("INFO:"):
        return ""
    # 形如 "ollama.exe","8496","Console","1","60,236 K"
    return output.split('","')[0].strip('"').lower()


def stop_foreign(url: str = DEFAULT_BASE_URL, *, wait_s: float = 8.0) -> str:
    """关掉端口上那个**不是本程序拉起**的 Ollama。

    返回：
    - `stopped`      关掉了，端口已释放
    - `no_listener`  端口上没有人
    - `not_ollama`   端口被别的程序占着（不动它）
    - `failed`       关了但端口没释放

    ⚠ 只 taskkill 进程名是 ollama 的。用户机器上 `P:\\.Ollama` 那份是
    自己用 start-ollama.ps1 启的常驻服务，别的工具可能也在用 —— 但既然
    用户要求"按设置里的路径掌管 Ollama"，这里就是会关掉它。
    """
    if _owned is not None and _owned.poll() is None:
        return "no_listener"                  # 端口上是我们自己起的，别动

    port = url_port(url)
    pids = listener_pids(port)
    if not pids:
        return "no_listener"

    killed = False
    for pid in pids:
        name = process_name(pid)
        if name not in ("ollama.exe", "ollama"):
            print(
                f"[rag] 端口 {port} 被 {name or f'PID {pid}'} 占着，不是 ollama，不动它",
                flush=True,
            )
            continue
        try:
            subprocess.run(  # noqa: S603,S607
                ["taskkill", "/PID", str(pid), "/F"],
                capture_output=True,
                text=True,
                timeout=15,
                creationflags=_CREATE_NO_WINDOW,
            )
        except (OSError, subprocess.SubprocessError) as exc:
            print(f"[rag] 关闭 Ollama（PID {pid}）失败：{exc}", flush=True)
            continue
        killed = True
        print(f"[rag] 已关掉占用 {port} 的外部 Ollama（PID {pid}）", flush=True)

    if not killed:
        return "not_ollama"

    # taskkill 是异步的：等端口真的放开，否则我们自己的服务会抢不到
    deadline = time.monotonic() + max(1.0, float(wait_s))
    while time.monotonic() < deadline:
        if not listener_pids(port):
            return "stopped"
        time.sleep(0.15)
    return "failed"


# ---------------------------------------------------------------------------
# 找可执行文件
# ---------------------------------------------------------------------------
def _project_root() -> Path:
    """单独抽出来，测试里可以替换（不要在测试里往真实 asset/ 写东西）。"""
    from dsai4431_chatbot.core.gui import settings_store

    return settings_store.project_root()


def models_dir(cfg=None) -> Path:
    """模型目录：设置页填的 > `asset/embedding`。

    **不看环境变量 `OLLAMA_MODELS`**（用户 2026-11-12 的决定：设置页说了算）。
    照环境变量走的坑实测过：机器上那份 Ollama 的模型目录是只读的，
    新下载的 Ollama 一启动就想在那里建 `manifests-v2`，直接 Permission denied。
    """
    explicit = str(getattr(cfg, "rag_models_dir", "") or "").strip() if cfg is not None else ""
    if explicit:
        return Path(explicit)
    return _project_root() / "asset" / "embedding"


def find_executable(cfg=None) -> Path | None:
    """按顺序找 ollama：设置页填的目录 → 项目便携版 → PATH → 系统安装的典型位置。"""
    explicit = str(getattr(cfg, "rag_ollama_dir", "") or "").strip() if cfg is not None else ""
    if explicit:
        base = Path(explicit)
        # 用户可能选了目录，也可能直接选了 exe
        for candidate in (base, base / "ollama.exe", base / "ollama"):
            if candidate.is_file():
                return candidate
        return None                       # 填了但不对，就别偷偷换别的，让状态行报出来

    portable = _project_root() / "asset" / "ollama" / "ollama.exe"
    if portable.is_file():
        return portable

    from shutil import which

    found = which("ollama")
    if found:
        return Path(found)

    local = os.environ.get("LOCALAPPDATA", "")
    candidates = []
    if local:
        candidates.append(Path(local) / "Programs" / "Ollama" / "ollama.exe")
    candidates.append(Path("C:/Program Files/Ollama/ollama.exe"))
    for path in candidates:
        if path.is_file():
            return path
    return None


# ---------------------------------------------------------------------------
# 拉起 / 收掉
# ---------------------------------------------------------------------------
def ensure_running(
    cfg,
    *,
    command: list[str] | None = None,
    wait_s: float = WAIT_READY_S,
    take_over: bool | None = None,
) -> LaunchResult:
    """探测 → 接管 → 拉起 → 等就绪。任何一步失败都只是返回 detail。

    `take_over`：端口上已经有别的 Ollama 时，要不要先关掉它、再按我们的
    可执行文件和模型目录重起。默认开（用户要求）；传了 `command`（测试钩子）
    就自动关掉 —— 测试里的"服务"是 python 假进程，绝不能去 taskkill。
    """
    url = base_url(cfg)
    if take_over is None:
        take_over = command is None
    took_over = False

    if is_alive(url):
        if not take_over:
            return LaunchResult(ok=True, started=False, detail="already_running")

        code = stop_foreign(url)
        if code == "not_ollama":
            # 端口被别的东西占了：不杀、也不硬起（会抢端口失败）
            return LaunchResult(ok=False, started=False, detail="port_busy")
        if code == "failed":
            return LaunchResult(ok=False, started=False, detail="failed")
        if code == "no_listener":
            # is_alive 说活、netstat 却看不到监听（多半是代理/别的地址族），
            # 也可能是我们自己起的那份：没法接管，当成已可用，别硬起第二份
            return LaunchResult(ok=True, started=False, detail="already_running")
        took_over = True                     # stopped：端口已释放，往下按自己的起

    if not bool(getattr(cfg, "rag_autostart", True)):
        return LaunchResult(ok=False, started=False, detail="disabled")

    exe = find_executable(cfg) if command is None else Path(command[0])
    if command is None and exe is None:
        return LaunchResult(ok=False, started=False, detail="no_exe")

    argv = command or [str(exe), "serve"]
    env = os.environ.copy()
    # 设置页填了模型目录就以它为准；没填才沿用环境变量，再退回 asset/embedding
    env["OLLAMA_MODELS"] = str(models_dir(cfg))

    creation = _CREATE_NO_WINDOW if sys.platform == "win32" else 0
    try:
        process = subprocess.Popen(  # noqa: S603 - 路径来自上面固定候选，非用户输入
            argv,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            stdin=subprocess.DEVNULL,
            env=env,
            creationflags=creation,
        )
    except OSError:
        return LaunchResult(ok=False, started=False, detail="failed", exe=str(argv[0]))

    global _owned
    _owned = process

    deadline = time.monotonic() + max(1.0, float(wait_s))
    while time.monotonic() < deadline:
        if is_alive(url, timeout=0.4):
            return LaunchResult(
                ok=True,
                started=True,
                detail="took_over" if took_over else "started",
                exe=str(argv[0]),
            )
        if process.poll() is not None:
            break
        time.sleep(0.2)

    # 没起来：别留一个半死的进程占着
    stop_owned()
    detail = "timeout" if process.poll() is None else "failed"
    return LaunchResult(ok=False, started=False, detail=detail, exe=str(argv[0]))


def owned_pid() -> int | None:
    return None if _owned is None else _owned.pid


def stop_owned() -> None:
    """只关「我们自己起的」那份。别人开着的、或者本来就是系统装的，不碰。"""
    global _owned
    process, _owned = _owned, None
    if process is None:
        return
    try:
        if process.poll() is None:
            process.terminate()
            try:
                process.wait(timeout=3)
            except subprocess.TimeoutExpired:
                process.kill()
    except OSError:
        pass

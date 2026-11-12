"""Ollama 的探测与「按需拉起」。

用户的决定（2026-11-12）：**探测不到就自己起，退出时把我们起的那份关掉**（方案 B）。
别人手动开着的那份永远不碰。

三条规矩：
1. 先探测 `GET /api/tags`；**通了就什么都不做**（否则两个 Ollama 抢 11434）
2. 只在后台线程里调（`rag_service` 的同步任务），别卡启动
3. 只 kill 自己 Popen 出来的进程（记在模块级 `_owned`）

`ensure_running()` 的 `command` 参数是给测试用的钩子：
真实路径是 `[ollama.exe, "serve"]`，测试里换成 `[python, stub.py, "serve"]`。
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

DEFAULT_BASE_URL = "http://127.0.0.1:11434"
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
    detail: str = ""          # already_running / started / disabled / no_exe / timeout / failed
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
# 找可执行文件
# ---------------------------------------------------------------------------
def _project_root() -> Path:
    """单独抽出来，测试里可以替换（不要在测试里往真实 asset/ 写东西）。"""
    from dsai4431_chatbot.core.gui import settings_store

    return settings_store.project_root()


def models_dir() -> Path:
    """模型应该放的地方：`<repo>/asset/embedding`（README 里就是这么定的）。"""
    return _project_root() / "asset" / "embedding"


def find_executable() -> Path | None:
    """按顺序找 ollama：项目便携版 → PATH → 系统安装的典型位置。"""
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
) -> LaunchResult:
    """探测 → (没通且允许自动启动) 拉起 → 等就绪。任何一步失败都只是返回 detail。"""
    url = base_url(cfg)
    if is_alive(url):
        return LaunchResult(ok=True, started=False, detail="already_running")

    if not bool(getattr(cfg, "rag_autostart", True)):
        return LaunchResult(ok=False, started=False, detail="disabled")

    exe = find_executable() if command is None else Path(command[0])
    if command is None and exe is None:
        return LaunchResult(ok=False, started=False, detail="no_exe")

    argv = command or [str(exe), "serve"]
    env = os.environ.copy()
    # 只在用户没自己设过时兜底，别覆盖他显式配置的路径
    if not env.get("OLLAMA_MODELS"):
        env["OLLAMA_MODELS"] = str(models_dir())

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
            return LaunchResult(ok=True, started=True, detail="started", exe=str(argv[0]))
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

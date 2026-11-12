"""首次运行「全自动装好」：下载 Ollama 便携版 + 拉 embedding 模型到项目里。

用户的要求（2026-11-12）：
- 设置页那两个路径**留空**时，第一次运行就自动下载配置好
- Ollama 解压到 `asset/ollama/`，模型进 `asset/embedding/`（都在项目里，不进 git）

⚠ 体积很大（Windows 版 zip 约 1.6 GB，模型另算），所以：
- 只在「设置页没填路径 **且** 探测不到任何 Ollama」时才跑
- 全程在后台线程，进度写进 RAG 页状态行
- 任何一步失败都只返回错误串，绝不让聊天崩

测试钩子：
- `DSAI_OLLAMA_ZIP_URL` 换下载地址（单元测试用本地假 zip）
- `extract_zip()` / `pull_model()` 都是独立函数，可以单独测
"""

from __future__ import annotations

import os
import shutil
import subprocess
import sys
import urllib.request
import zipfile
from dataclasses import dataclass
from pathlib import Path

ZIP_URL = os.environ.get(
    "DSAI_OLLAMA_ZIP_URL", "https://ollama.com/download/ollama-windows-amd64.zip"
)
# 下载超时：大文件用大超时；urllib 的 timeout 是「单次读」的超时，不是总时长
DOWNLOAD_TIMEOUT_S = 60
CHUNK = 1 << 20


@dataclass
class BootstrapResult:
    ok: bool = False
    detail: str = ""        # already_ok / downloaded / pulled / no_zip / failed
    exe: str = ""
    models_dir: str = ""
    error: str = ""

    @property
    def message_key(self) -> str:
        return f"settings.rag.boot_{self.detail or 'failed'}"


# ---------------------------------------------------------------------------
# 路径（和 settings 里留空时的默认位置一致）
# ---------------------------------------------------------------------------
def _project_root() -> Path:
    from dsai4431_chatbot.core.gui import settings_store

    return settings_store.project_root()


def ollama_dir() -> Path:
    return _project_root() / "asset" / "ollama"


def models_dir() -> Path:
    return _project_root() / "asset" / "embedding"


def ollama_exe(directory: Path | None = None) -> Path:
    base = Path(directory) if directory else ollama_dir()
    return base / ("ollama.exe" if sys.platform == "win32" else "ollama")


# ---------------------------------------------------------------------------
# 下载 / 解压
# ---------------------------------------------------------------------------
def download(url: str, dest: Path, progress=None) -> Path:
    """流式下载到 `dest`；`progress(done_bytes, total_bytes)` 可空。"""
    dest.parent.mkdir(parents=True, exist_ok=True)
    tmp = dest.with_suffix(dest.suffix + ".part")
    request = urllib.request.Request(url, headers={"User-Agent": "dsai4431-chatbot"})
    with urllib.request.urlopen(request, timeout=DOWNLOAD_TIMEOUT_S) as response:
        total = int(response.headers.get("Content-Length") or 0)
        done = 0
        with open(tmp, "wb") as handle:
            while True:
                block = response.read(CHUNK)
                if not block:
                    break
                handle.write(block)
                done += len(block)
                if progress is not None:
                    progress(done, total)
    os.replace(tmp, dest)
    return dest


def extract_zip(zip_path: Path, dest: Path) -> None:
    """解压到 `dest`（跳过路径穿越条目）。"""
    dest.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(zip_path) as archive:
        for member in archive.namelist():
            target = (dest / member).resolve()
            if not str(target).startswith(str(dest.resolve())):
                continue                      # 别让 zip 里的 ../ 跑到项目外面
            archive.extract(member, dest)


# ---------------------------------------------------------------------------
# 拉模型
# ---------------------------------------------------------------------------
def pull_model(
    exe: Path,
    model: str,
    model_dir: Path,
    progress=None,
    *,
    command: list[str] | None = None,
) -> bool:
    """用 `ollama pull` 把模型拉到 `model_dir`（通过 OLLAMA_MODELS 指过去）。

    `command` 是测试钩子：真实路径是 `[ollama.exe, "pull", model]`，
    测试里换成 `[python, 假脚本]`（假脚本把拿到的环境变量写进文件）。
    """
    if not model:
        return False
    model_dir.mkdir(parents=True, exist_ok=True)
    env = os.environ.copy()
    env["OLLAMA_MODELS"] = str(model_dir)
    env.setdefault("OLLAMA_HOST", "127.0.0.1:11434")
    creation = 0x08000000 if sys.platform == "win32" else 0
    argv = command or [str(exe), "pull", model]
    try:
        process = subprocess.Popen(  # noqa: S603 - exe 来自固定候选，非用户输入
            argv,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            stdin=subprocess.DEVNULL,
            env=env,
            text=True,
            encoding="utf-8",
            errors="replace",
            creationflags=creation,
        )
    except OSError as exc:
        if progress is not None:
            progress(f"启动失败：{exc}")
        return False
    try:
        assert process.stdout is not None
        for line in process.stdout:
            text = line.strip()
            if text and progress is not None:
                progress(text)
    finally:
        process.wait()
    return process.returncode == 0


# ---------------------------------------------------------------------------
# 总流程
# ---------------------------------------------------------------------------
def needs_bootstrap(cfg, *, service_alive: bool) -> bool:
    """要不要走「自动下载」这套。

    只要满足任意一条就不下：
    1. 设置页里填了 Ollama 目录（用户明确指定）
    2. 服务已经在跑（说明机器上有能用的 Ollama）
    3. `find_executable()` 能在默认位置找到 exe（`asset/ollama` 已经有了）
    """
    if bool(getattr(cfg, "rag_ollama_dir", "")):
        return False
    if service_alive:
        return False
    from dsai4431_chatbot.core.gui import ollama_launcher

    if ollama_launcher.find_executable(cfg) is not None:
        return False
    return True


def ensure_stack(
    cfg,
    *,
    progress=None,
    service_alive: bool = False,
    starter=None,
) -> BootstrapResult:
    """需要就把 Ollama 和模型装到项目里。

    `starter()` 由调用方给（一般是 `ollama_launcher.ensure_running`）：
    **`ollama pull` 必须先有一个在跑的 serve**（CLI 自己找不到 app 会报
    「could not locate ollama app」，实测），所以顺序是
    「解压 → 起服务 → pull」。只下载不拉模型时可以不传。
    """
    target_dir = Path(getattr(cfg, "rag_ollama_dir", "") or ollama_dir())
    target_models = Path(getattr(cfg, "rag_models_dir", "") or models_dir())
    model = str(getattr(cfg, "rag_embedding", "") or "").strip()

    exe = ollama_exe(target_dir)
    if not exe.is_file():
        zip_path = target_dir / "ollama-windows-amd64.zip"
        try:
            if progress is not None:
                progress("downloading", 0, 0)
            download(ZIP_URL, zip_path, lambda d, t: progress and progress("downloading", d, t))
            if progress is not None:
                progress("extracting", 0, 0)
            extract_zip(zip_path, target_dir)
            # 官方 zip 解压出来可能多一层目录，找一次真正的 ollama.exe
            if not exe.is_file():
                found = next(iter(target_dir.rglob("ollama.exe")), None)
                if found is not None:
                    exe = found
                    for item in found.parent.iterdir():
                        shutil.move(str(item), str(target_dir / item.name))
        except Exception as exc:              # noqa: BLE001 - 网络错误种类太多
            return BootstrapResult(ok=False, detail="failed", error=f"下载/解压失败：{exc}")
        finally:
            try:
                zip_path.unlink(missing_ok=True)
            except OSError:
                pass
        if not exe.is_file():
            return BootstrapResult(ok=False, detail="no_zip", error="解压后没找到 ollama.exe")

    if not model:
        return BootstrapResult(ok=True, detail="pulled", exe=str(exe), models_dir=str(target_models))

    # pull 需要一个在跑的服务（CLI 自己起不来 app）
    if starter is not None and not service_alive:
        if progress is not None:
            progress("pulling", 0, 0)
        try:
            starter()
        except Exception as exc:              # noqa: BLE001 - 起服务失败不该炸
            print(f"[rag] 启动 Ollama 失败：{exc}", flush=True)

    if progress is not None:
        progress("pulling", 0, 0)
    ok = pull_model(exe, model, target_models, lambda line: progress and progress("pulling", 0, 0))
    if not ok:
        return BootstrapResult(
            ok=False,
            detail="failed",
            exe=str(exe),
            models_dir=str(target_models),
            error=f"`ollama pull {model}` 失败（服务没起来或模型名不对）",
        )
    return BootstrapResult(ok=True, detail="pulled", exe=str(exe), models_dir=str(target_models))

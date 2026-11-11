"""重启主程序（换语言后用）。

为什么要绕一圈：换了语言必须重启才能重新取文案，但在**自己进程里**直接
`startDetached` 拉起新进程有个坑 —— 旧进程还没退干净，两份 QtWebEngine
会去抢同一个 profile 目录。所以先起一个「中间人」进程，它等旧进程真的退出
（按 PID 轮询）后再拉起主程序：

    python -m dsai4431_chatbot.core.gui.relaunch --delay 1.5 --pid 1234

中间人进程独立、无控制台（Windows 用 DETACHED_PROCESS），不会跟着旧窗口
一起消失。主程序用**同一个解释器**拉起，所以从 .bat 启动的照样有控制台、
从 pythonw 启动的照样没有。

命令行用法（排查问题时可以手动跑）：
    python -m dsai4431_chatbot.core.gui.relaunch --pid <PID> --delay 2
"""

from __future__ import annotations

import argparse
import os
import subprocess
import sys
import time

# 等旧进程退出的上限；超过就不再等（宁可新进程稍早起来，也不能永远不起）
WAIT_TIMEOUT = 12.0
# 旧进程退掉后再缓一会儿，让 WebEngine 的缓存/锁文件收尾
SLACK = 0.6
# 默认延迟：--pid 没给（手动跑）时用
DELAY = 1.5

_STILL_ACTIVE = 259


def app_command(exe: str | None = None) -> list[str]:
    """拉起主程序的命令行。打包版直接跑自己，源码版走 `-m`。"""
    exe = exe or sys.executable
    if getattr(sys, "frozen", False):
        return [exe]
    return [exe, "-m", "dsai4431_chatbot.core.gui"]


def _pid_alive(pid: int) -> bool:
    """PID 还在跑吗（Windows 用 OpenProcess，其他平台用 os.kill 探活）。"""
    if pid <= 0:
        return False
    if os.name != "nt":
        try:
            os.kill(pid, 0)
        except OSError:
            return False
        return True

    import ctypes

    PROCESS_QUERY_LIMITED_INFORMATION = 0x1000
    kernel32 = ctypes.windll.kernel32
    handle = kernel32.OpenProcess(PROCESS_QUERY_LIMITED_INFORMATION, 0, int(pid))
    if not handle:
        return False
    try:
        code = ctypes.c_ulong()
        if not kernel32.GetExitCodeProcess(handle, ctypes.byref(code)):
            return False
        return code.value == _STILL_ACTIVE
    finally:
        kernel32.CloseHandle(handle)


def wait_for_exit(pid: int, timeout: float = WAIT_TIMEOUT, slack: float = SLACK) -> bool:
    """等 PID 退出；返回是否确认它已经没了（超时是 False）。"""
    if not pid:
        return False
    end = time.monotonic() + max(0.0, timeout)
    while time.monotonic() < end:
        if not _pid_alive(pid):
            time.sleep(max(0.0, slack))
            return True
        time.sleep(0.12)
    return False


def spawn_helper(delay: float = DELAY, exe: str | None = None, pid: int | None = None) -> bool:
    """起一个延迟重启的助手进程；只是拉起，不等它，返回是否成功。"""
    args = [
        "-m",
        f"{__package__}.relaunch",
        "--delay",
        str(float(delay)),
    ]
    if pid:
        args += ["--pid", str(int(pid))]
    if exe:
        args += ["--exe", str(exe)]

    kwargs: dict = {
        "stdin": subprocess.DEVNULL,
        "stdout": subprocess.DEVNULL,
        "stderr": subprocess.DEVNULL,
        "close_fds": True,
    }
    if os.name == "nt":
        # DETACHED_PROCESS：不分配控制台，也不会因为父进程退出被带走
        kwargs["creationflags"] = 0x00000008

    try:
        subprocess.Popen([sys.executable, *args], **kwargs)
    except OSError as exc:
        print(f"[relaunch] 无法启动重启助手：{exc}", file=sys.stderr)
        return False
    return True


def restart(delay: float = DELAY, exe: str | None = None) -> bool:
    """拉起新进程并退出当前应用。失败时返回 False（调用方负责回滚 UI）。"""
    from PySide6.QtWidgets import QApplication

    if not spawn_helper(delay=delay, exe=exe or sys.executable, pid=os.getpid()):
        return False

    app = QApplication.instance()
    if app is not None:
        app.quit()
    return True


def main(argv: list[str] | None = None) -> int:
    """助手进程入口：等旧进程退出 → 拉起主程序。"""
    parser = argparse.ArgumentParser(
        prog="dsai4431_chatbot.core.gui.relaunch",
        description="等待旧进程退出后重新启动主界面。",
    )
    parser.add_argument("--delay", type=float, default=DELAY, help="最短等待秒数")
    parser.add_argument("--pid", type=int, default=0, help="要等待退出的旧进程 PID")
    parser.add_argument("--exe", default=None, help="用哪个解释器拉起主程序")
    ns = parser.parse_args(argv)

    # 先至少睡 --delay，再确认旧 PID 真的没了（两者取长）
    time.sleep(max(0.0, ns.delay))
    wait_for_exit(ns.pid)

    try:
        subprocess.Popen(app_command(ns.exe), close_fds=True)
    except OSError as exc:
        print(f"[relaunch] 拉起主程序失败：{exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

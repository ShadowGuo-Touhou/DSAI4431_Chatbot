"""方案 A：Python 起本地 HTTP 服务 + QtWebEngine 内嵌浏览器渲染 Live2D。

和 jingyu-live2d-agent 完全同一条技术栈（PixiJS + pixi-live2d-display + Cubism Core for Web），
区别只是把外部浏览器换成 Python 进程里的一个窗口，所以模型物理、表情、口型、
motion3.json 全部原样支持，不需要重写渲染。

依赖：
    pip install PySide6            # 含 QtWebEngine（PySide6-Addons）
    # vendor/live2dcubismcore.min.js 需自行从 Live2D 官网下载（见 README）

运行：
    python option_web_qt.py --model "D:/models/大肥鱼/大肥鱼.model3.json"
    python option_web_qt.py --model "..." --size 480x700 --bg "#00000000"

从 Python 控制角色（窗口加载完成后）：
    win.eval("l2d.motion('Idle')")
    win.eval("l2d.expression('f01')")
    win.eval("l2d.set('ParamMouthOpenY', 0.6)")
"""

from __future__ import annotations

import argparse
import os
import sys
import threading
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

HERE = Path(__file__).resolve().parent
DEMO_ROOT = HERE
MODEL_PREFIX = "/model/"


class Handler(SimpleHTTPRequestHandler):
    """静态服务：/ 指向 demo 目录，/model/ 指向模型目录（允许跨盘、跨目录）。"""

    model_dir: str = ""

    def __init__(self, *args, model_dir: str, **kwargs):
        self.model_dir = model_dir
        super().__init__(*args, directory=str(DEMO_ROOT), **kwargs)

    def log_message(self, *args):  # 静音访问日志
        pass

    def do_GET(self):
        if not self.path.startswith(MODEL_PREFIX):
            return super().do_GET()

        # 把 /model/xxx 重写为模型目录下的 /xxx，交给父类做 mime / range 处理
        original_path, original_dir = self.path, self.directory
        self.path = self.path[len(MODEL_PREFIX) - 1 :]  # 保留开头的 "/"
        self.directory = self.model_dir
        try:
            return super().do_GET()
        finally:
            self.path, self.directory = original_path, original_dir


def start_server(model_dir: Path) -> tuple[ThreadingHTTPServer, int]:
    handler = partial(Handler, model_dir=str(model_dir))
    server = ThreadingHTTPServer(("127.0.0.1", 0), handler)  # 0 = 让系统分配空闲端口
    threading.Thread(target=server.serve_forever, daemon=True).start()
    return server, server.server_port


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--model", required=True, help="xxx.model3.json 的完整路径")
    ap.add_argument("--size", default="560x760", help="窗口尺寸，默认 560x760")
    ap.add_argument("--bg", default="#1b1f24", help="背景色，#00000000 为透明（需配合无边框窗口）")
    args = ap.parse_args()

    model_json = Path(args.model).expanduser().resolve()
    if not model_json.is_file():
        print(f"[error] 找不到模型文件: {model_json}", file=sys.stderr)
        return 2
    if not (DEMO_ROOT / "vendor" / "live2dcubismcore.min.js").is_file():
        print(
            "[error] 缺少 vendor/live2dcubismcore.min.js\n"
            "        从 https://www.live2d.com/en/sdk/download/web/ 下载 Cubism SDK for Web，\n"
            "        取其中的 Core 文件放到 vendor/ 目录。",
            file=sys.stderr,
        )
        return 2

    # QtWebEngine 必须在创建 QApplication 之前 import（且不能晚于 QApplication 构造）
    from PySide6.QtWebEngineWidgets import QWebEngineView
    from PySide6.QtCore import QTimer, QUrl
    from PySide6.QtWidgets import QApplication

    server, port = start_server(model_json.parent)
    w, h = (int(x) for x in args.size.lower().split("x"))

    app = QApplication(sys.argv)
    view = QWebEngineView()
    view.setWindowTitle("Live2D · Python + QtWebEngine")
    view.resize(w, h)
    view.setStyleSheet(f"background: {args.bg};")

    url = QUrl(f"http://127.0.0.1:{port}/index.html?m={model_json.name}")
    view.load(url)
    view.show()

    # 等页面里的模型加载完成后再放行，避免调用 l2d 时报 undefined
    ready = {"ok": False}

    def poll():
        def cb(res):
            if res is True:
                ready["ok"] = True
                print("[ok] 模型已加载，可调用 view.eval(...)")
                timer.stop()
            elif res:
                print(f"[error] 渲染失败: {res}", file=sys.stderr)
                timer.stop()

        view.page().runJavaScript(
            "window.l2dReady === true ? true : (window.l2dError || false)", cb
        )

    timer = QTimer()
    timer.timeout.connect(poll)
    timer.start(300)

    # 供外部脚本/调试用
    view.eval = lambda js: view.page().runJavaScript(js)  # type: ignore[attr-defined]
    if os.environ.get("L2D_DEMO_MOTION"):
        QTimer.singleShot(3000, lambda: view.eval(f"l2d.motion({os.environ['L2D_DEMO_MOTION']!r})"))

    code = app.exec()
    server.shutdown()
    return code


if __name__ == "__main__":
    raise SystemExit(main())

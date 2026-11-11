"""在已有的 PyQt5 GUI 里嵌入 Live2D —— 方案 A：QWebEngineView + PixiJS / Cubism Web。

这条路和 jingyu-live2d-agent 完全同栈：渲染在 Chromium 的 WebGL 里做，
Python 只负责（1）起一个只监听 127.0.0.1 的静态服务把模型文件喂给页面，
（2）调用 runJavaScript 控制角色。物理、表情、口型、motion3 全部原样支持。

依赖：
    pip install PyQt5 PyQtWebEngine
    # vendor/live2dcubismcore.min.js 需自行从 Live2D 官网获取（见同目录 README）

在你自己窗口里的用法：

    from pyqt5_web import Live2DWidget          # 必须早于 QApplication 创建！

    class MainWindow(QMainWindow):
        def __init__(self):
            super().__init__()
            self.live2d = Live2DWidget("D:/models/大肥鱼/大肥鱼.model3.json", parent=self)
            self.live2d.setMinimumSize(360, 480)
            self.setCentralWidget(self.live2d)
            self.live2d.motion("Idle")
            self.live2d.set_param("ParamMouthOpenY", 0.6)

    app = QApplication(sys.argv)
    ...
"""

from __future__ import annotations

import json
import threading
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import quote

from PyQt5.QtCore import Qt, QTimer, QUrl, pyqtSignal
from PyQt5.QtWidgets import QApplication, QVBoxLayout, QWidget

HERE = Path(__file__).resolve().parent
MODEL_PREFIX = "/model/"

# ---------------------------------------------------------------------------
# 关键：QtWebEngine 有两个"必须在 QApplication 之前"的硬性要求
#   1) setAttribute(Qt.AA_ShareOpenGLContexts, True)
#   2) import PyQt5.QtWebEngineWidgets（若晚于 QApplication 会直接崩或黑屏）
# 所以这里在模块被 import 的时候就做完。只要你的 import 写在文件顶部就没问题。
# ---------------------------------------------------------------------------
if QApplication.instance() is None:
    QApplication.setAttribute(Qt.AA_ShareOpenGLContexts, True)

from PyQt5.QtWebEngineWidgets import QWebEngineView  # noqa: E402  （必须在上面的属性之后）


class _Handler(SimpleHTTPRequestHandler):
    """静态服务：'/' -> 本目录（html + vendor），'/model/' -> 模型目录（任意盘符）。"""

    def __init__(self, *args, model_dir: str, **kwargs):
        self.model_dir = model_dir
        super().__init__(*args, directory=str(HERE), **kwargs)

    def log_message(self, *args):  # 静音访问日志
        pass

    def do_GET(self):
        if not self.path.startswith(MODEL_PREFIX):
            return super().do_GET()
        original_path, original_dir = self.path, self.directory
        self.path = self.path[len(MODEL_PREFIX) - 1 :]  # "/model/x" -> "/x"
        self.directory = self.model_dir
        try:
            return super().do_GET()
        finally:
            self.path, self.directory = original_path, original_dir


def _start_server(model_dir: Path) -> tuple[ThreadingHTTPServer, int]:
    server = ThreadingHTTPServer(("127.0.0.1", 0), partial(_Handler, model_dir=str(model_dir)))
    threading.Thread(target=server.serve_forever, daemon=True).start()
    return server, server.server_port


class Live2DWidget(QWidget):
    """可直接 addWidget 进任何布局的 Live2D 视图。

    信号：
        ready()          模型加载完成，可以安全调用 motion()/expression()
        loadFailed(str)  加载失败（通常是缺 Cubism Core 或模型路径不对）
    """

    ready = pyqtSignal()
    loadFailed = pyqtSignal(str)

    def __init__(self, model_json: str | Path, parent: QWidget | None = None, *, transparent: bool = False):
        super().__init__(parent)
        model = Path(model_json).expanduser().resolve()
        if not model.is_file():
            raise FileNotFoundError(f"找不到模型文件: {model}")
        if not (HERE / "vendor" / "live2dcubismcore.min.js").is_file():
            raise FileNotFoundError(
                "缺少 vendor/live2dcubismcore.min.js —— 从 Live2D 官网下载 Cubism SDK for Web 的 Core 放到 vendor/"
            )

        self._server, port = _start_server(model.parent)
        self._model_name = model.name

        self._view = QWebEngineView(self)
        if transparent:
            # 让网页背景透出到 Qt 窗口（窗口本身还要 WA_TranslucentBackground，见 make_pet_window）
            self.setAttribute(Qt.WA_TranslucentBackground, True)
            self._view.setAttribute(Qt.WA_TranslucentBackground, True)
            self._view.page().setBackgroundColor(Qt.transparent)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self._view)

        self._view.load(QUrl(f"http://127.0.0.1:{port}/index.html?m={quote(self._model_name)}"))

        self._poll = QTimer(self)
        self._poll.setInterval(200)
        self._poll.timeout.connect(self._check_ready)
        self._poll.start()

    # --- 就绪探测 ---------------------------------------------------------
    def _check_ready(self):
        def cb(result):
            if result is True:
                self._poll.stop()
                self.ready.emit()
            elif result:
                self._poll.stop()
                self.loadFailed.emit(str(result))

        self._view.page().runJavaScript(
            "window.l2dReady === true ? true : (window.l2dError || '')", cb
        )

    # --- 控制接口 ---------------------------------------------------------
    def run_js(self, js: str):
        """逃生舱：直接执行任意 JS。"""
        self._view.page().runJavaScript(js)

    def motion(self, group: str, index: int = 0):
        """播放 motion3.json 里的动作组，例如 motion('Idle')、motion('tap_body', 1)。"""
        self.run_js(f"window.l2d && l2d.motion({json.dumps(group)}, {int(index)})")

    def expression(self, name: str):
        """切换表情（对应 expressions/*.exp3.json 的 Name）。"""
        self.run_js(f"window.l2d && l2d.expression({json.dumps(name)})")

    def set_param(self, param_id: str, value: float):
        """直接写参数，口型同步就用这个（ParamMouthOpenY / ParamAngleX ...）。"""
        self.run_js(f"window.l2d && l2d.set({json.dumps(param_id)}, {float(value)})")

    def get_param(self, param_id: str, callback):
        self._view.page().runJavaScript(
            f"window.l2d ? l2d.get({json.dumps(param_id)}) : null", callback
        )

    def focus_at(self, x: float, y: float):
        """视线跟随到控件坐标 (x, y)，一般不用手动调 —— 页面已绑定 mousemove。"""
        self.run_js(f"window.l2d && l2d.model.focus({x}, {y})")

    # --- 生命周期 ---------------------------------------------------------
    def closeEvent(self, event):
        self._poll.stop()
        self._server.shutdown()
        super().closeEvent(event)


def make_pet_window(widget: QWidget, *, click_through: bool = False):
    """把一个普通窗口变成透明无边框置顶桌宠（Windows 上 QWebEngineView 透明总体可用）。

    click_through=True 时鼠标事件穿透到桌面（托盘菜单里再切回来）。
    """
    widget.setAttribute(Qt.WA_TranslucentBackground, True)
    widget.setWindowFlags(
        Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.Tool
        | (Qt.WindowTransparentForInput if click_through else Qt.Widget)
    )
    widget.setStyleSheet("background: transparent;")
    return widget


def main() -> int:
    import argparse
    import sys

    ap = argparse.ArgumentParser()
    ap.add_argument("--model", required=True, help="xxx.model3.json 的完整路径")
    ap.add_argument("--size", default="560x760")
    ap.add_argument("--pet", action="store_true", help="透明无边框置顶桌宠")
    ap.add_argument("--click-through", action="store_true", help="配合 --pet：鼠标穿透")
    args = ap.parse_args()

    app = QApplication(sys.argv)
    w, h = (int(x) for x in args.size.lower().split("x"))

    win = QWidget()
    win.resize(w, h)
    lay = QVBoxLayout(win)
    lay.setContentsMargins(0, 0, 0, 0)
    stage = Live2DWidget(args.model, parent=win, transparent=args.pet)
    lay.addWidget(stage)
    stage.ready.connect(lambda: print("[ok] 模型已加载"))
    stage.loadFailed.connect(lambda m: print(f"[error] {m}"))

    if args.pet:
        make_pet_window(win, click_through=args.click_through)
        win.setWindowTitle("Live2D pet")

    win.show()
    return app.exec()


if __name__ == "__main__":
    raise SystemExit(main())

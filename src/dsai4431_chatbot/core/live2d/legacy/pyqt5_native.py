"""在已有的 PyQt5 GUI 里播放 Live2D —— 方案 B：live2d-py + QOpenGLWidget 原生渲染。

不走浏览器：live2d-py 把 Live2D Cubism Native SDK (C++) 包成 C 扩展，
只要有一个 OpenGL 上下文就能画，QOpenGLWidget 正好提供。

依赖：
    pip install PyQt5 live2d-py        # live2d-py 要求 Python >= 3.11
    # Cubism Core 与许可按 live2d-py wiki 安装页说明处理

在你自己窗口里的用法：

    from pyqt5_native import Live2DGLWidget   # 内部会做 live2d.init()，尽量早 import

    self.stage = Live2DGLWidget("D:/models/大肥鱼/大肥鱼.model3.json", parent=self)
    layout.addWidget(self.stage)

    self.stage.motion("Idle")        # 播动作组
    self.stage.expression("f01")     # 换表情
    self.stage.set_param("ParamMouthOpenY", 0.6)

注意：
  * 这是 Native SDK 路线，物理 / 表情 / motion3 都支持，但像素细节与 Web 版不完全一致。
  * 一个进程里多个 QOpenGLWidget 会共享上下文；若与别的 GL 控件互相干扰，
    给本控件设 setUpdateBehavior(QOpenGLWidget.NoPartialUpdate)。
"""

from __future__ import annotations

from pathlib import Path

from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QSurfaceFormat
from PyQt5.QtWidgets import QApplication, QOpenGLWidget, QVBoxLayout, QWidget

_INITED = False


def _ensure_live2d_init():
    """live2d.init() 只需一次，且应在创建模型之前。"""
    global _INITED
    if not _INITED:
        import live2d

        live2d.init()
        _INITED = True


class Live2DGLWidget(QOpenGLWidget):
    """可直接 addWidget 的原生 Live2D 画布。"""

    def __init__(self, model_json: str | Path, parent: QWidget | None = None, *, fps: int = 60):
        super().__init__(parent)
        self._model_path = Path(model_json).expanduser().resolve()
        if not self._model_path.is_file():
            raise FileNotFoundError(f"找不到模型文件: {self._model_path}")
        _ensure_live2d_init()

        self._model = None
        self._error: str | None = None
        self.setMouseTracking(True)

        self._timer = QTimer(self)
        self._timer.setInterval(max(1, int(1000 / max(1, fps))))
        self._timer.timeout.connect(self.update)
        self._timer.start()

    # --- GL 生命周期 ------------------------------------------------------
    def initializeGL(self):
        import live2d

        try:
            live2d.glInit()  # 必须等 GL 上下文就绪
            model = live2d.Model()
            model.LoadModelJson(str(self._model_path))
            self._resize_model()
            model.SetAutoBlink(True)   # 自带眨眼
            model.SetAutoBreath(True)  # 自带呼吸
            self._model = model
            print("[ok] live2d 模型已加载")
        except Exception as exc:  # 缺贴图 / Core 版本不符 / moc3 损坏
            self._error = str(exc)
            print(f"[error] live2d 加载失败: {exc}")

    def paintGL(self):
        if self._model is None:
            return
        import live2d

        self._model.Update()   # 推进动作、物理、表情、眨眼
        live2d.clearBuffer()   # 清屏（rgba，默认全透明）
        self._model.Draw()

    def resizeGL(self, w, h):
        self._resize_model()

    def _resize_model(self):
        if self._model is None:
            return
        dpr = self.devicePixelRatioF()
        self._model.Resize(max(1, int(self.width() * dpr)), max(1, int(self.height() * dpr)))

    # --- 鼠标交互 ---------------------------------------------------------
    def mouseMoveEvent(self, event):
        if self._model is None:
            return
        # Drag 接收模型画布像素坐标；与 _resize_model 用同一个 dpr 才对齐
        dpr = self.devicePixelRatioF()
        self._model.Drag(event.position().x() * dpr, event.position().y() * dpr)

    def mousePressEvent(self, event):
        if self._model is None or event.button() != Qt.MouseButton.LeftButton:
            return
        dpr = self.devicePixelRatioF()
        x, y = event.position().x() * dpr, event.position().y() * dpr
        hits = self._model.HitPart(x, y, False)  # 精确到部件的点击检测
        print(f"[hit] {hits}")
        if hits:
            self._model.StartRandomMotion(priority=3)  # 3 = FORCE
        else:
            print(f"[expression] {self._model.SetRandomExpression()}")

    # --- 控制接口 ---------------------------------------------------------
    def motion(self, group: str, index: int = 0):
        if self._model is not None:
            import live2d

            self._model.StartMotion(group, int(index), live2d.MotionPriority.FORCE)

    def expression(self, name: str):
        if self._model is not None:
            self._model.SetExpression(name)

    def set_param(self, param_id: str, value: float):
        if self._model is not None:
            self._model.SetParamById(param_id, float(value))

    def lip_sync(self, rms: float, gain: float = 3.0):
        """把音频 RMS 塞进嘴型参数，自己接播放器时每帧调一次。"""
        self.set_param("ParamMouthOpenY", min(1.0, rms * gain))

    def params(self) -> list[str]:
        if self._model is None:
            return []
        return list(self._model.GetParamIds())

    # --- 生命周期 ---------------------------------------------------------
    def closeEvent(self, event):
        self._timer.stop()
        if self._model is not None:
            try:
                self._model.DestroyRenderer()
            except Exception:
                pass
            self._model = None
        super().closeEvent(event)


def prepare_transparent_gl():
    """想要"模型下面透出桌面/父窗口"时，在 QApplication 之前调用。

    Windows 上 QOpenGLWidget 逐像素透明还要求控件自身：
        w.setAttribute(Qt.WA_TranslucentBackground, True)
        w.setAttribute(Qt.WA_AlwaysStackOnTop, True)
    这两个标志在部分驱动上仍会失效，纯透明需求建议直接用 pyqt5_web.py 那条路。
    """
    fmt = QSurfaceFormat.defaultFormat()
    fmt.setAlphaBufferSize(8)
    QSurfaceFormat.setDefaultFormat(fmt)


def main() -> int:
    import argparse
    import sys

    ap = argparse.ArgumentParser()
    ap.add_argument("--model", required=True, help="xxx.model3.json 的完整路径")
    ap.add_argument("--size", default="560x760")
    ap.add_argument("--transparent", action="store_true", help="请求逐像素透明 GL 表面")
    args = ap.parse_args()

    if args.transparent:
        prepare_transparent_gl()
    app = QApplication(sys.argv)

    w, h = (int(x) for x in args.size.lower().split("x"))
    win = QWidget()
    win.resize(w, h)
    lay = QVBoxLayout(win)
    lay.setContentsMargins(0, 0, 0, 0)
    stage = Live2DGLWidget(args.model, parent=win)
    if args.transparent:
        win.setAttribute(Qt.WA_TranslucentBackground, True)
        stage.setAttribute(Qt.WA_AlwaysStackOnTop, True)
    lay.addWidget(stage)
    win.show()
    return app.exec()


if __name__ == "__main__":
    raise SystemExit(main())

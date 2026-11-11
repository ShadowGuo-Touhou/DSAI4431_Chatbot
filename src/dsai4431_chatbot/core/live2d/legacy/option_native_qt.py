"""方案 B：纯 Python 原生渲染 Live2D，不经过浏览器。

live2d-py 用 C 扩展把 Live2D Cubism Native SDK (C++) 包成 Python 模块，
只要有一个 OpenGL 上下文就能画：PySide6 / PyQt / pygame / GLFW 都行。
本文件用 PySide6 的 QOpenGLWidget，鼠标直接驱动视线。

依赖：
    pip install PySide6 live2d-py        # Python >= 3.11（本机 3.12 可用）
    # live2d-py 自身不带 Cubism Core，按官方 wiki 安装页的说明处理 Core 文件与许可

运行：
    python option_native_qt.py --model "D:/models/大肥鱼/大肥鱼.model3.json"

注意：
    * 这是 Cubism Native SDK 路线，模型物理/表情/motion3 都支持，
      但渲染细节、shader 与 Web 版不是逐像素一致。
    * 模型用的如果是 Cubism 5 新特性，先确认 live2d-py 打包的 SDK 版本（当前 5-r.5）。
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--model", required=True, help="xxx.model3.json 的完整路径")
    ap.add_argument("--size", default="560x760")
    ap.add_argument("--fps", type=int, default=60)
    args = ap.parse_args()

    model_json = Path(args.model).expanduser().resolve()
    if not model_json.is_file():
        print(f"[error] 找不到模型文件: {model_json}", file=sys.stderr)
        return 2

    try:
        import live2d
    except ImportError:
        print("[error] 缺少 live2d-py，先执行: pip install live2d-py", file=sys.stderr)
        return 2

    from PySide6.QtCore import Qt
    from PySide6.QtOpenGLWidgets import QOpenGLWidget
    from PySide6.QtWidgets import QApplication

    class Live2DStage(QOpenGLWidget):
        def __init__(self):
            super().__init__()
            self.model = None
            self.msg = ""
            self.setWindowTitle("Live2D · Python + live2d-py (native)")
            self.setMouseTracking(True)

        def initializeGL(self):
            # GL 上下文就绪之后才能初始化 SDK 与创建模型
            live2d.glInit()
            try:
                model = live2d.Model()
                model.LoadModelJson(str(model_json))
                model.Resize(self.width(), self.height())
                model.SetAutoBlink(True)   # 自带眨眼
                model.SetAutoBreath(True)  # 自带呼吸
                self.model = model
            except Exception as exc:  # 模型缺贴图 / Core 版本不符等
                self.msg = f"加载失败: {exc}"
                print(f"[error] {self.msg}", file=sys.stderr)
                return
            self.startTimer(max(1, int(1000 / max(1, args.fps))))
            print("[ok] 模型已加载")

        def paintGL(self):
            if self.model is None:
                return
            self.model.Update()          # 推进动作、物理、表情
            live2d.clearBuffer()         # 清屏（rgba）
            self.model.Draw()

        def resizeGL(self, w, h):
            if self.model is not None:
                self.model.Resize(w, h)

        def timerEvent(self, _event):
            self.update()

        def mouseMoveEvent(self, event):
            if self.model is None:
                return
            # Drag 接收的是模型画布像素坐标，需要按设备像素比换算
            dpr = self.devicePixelRatioF()
            self.model.Drag(event.position().x() * dpr, event.position().y() * dpr)

        def mousePressEvent(self, event):
            if self.model is None or event.button() != Qt.MouseButton.LeftButton:
                return
            dpr = self.devicePixelRatioF()
            x, y = event.position().x() * dpr, event.position().y() * dpr
            hits = self.model.HitPart(x, y, False)
            print(f"[hit] {hits}")
            if hits:
                self.model.StartRandomMotion(priority=3)  # 点到身体就随机播一个动作
            else:
                print(f"[expression] {self.model.SetRandomExpression()}")

    live2d.init()  # 在 QApplication 之前
    app = QApplication(sys.argv)
    stage = Live2DStage()
    w, h = (int(x) for x in args.size.lower().split("x"))
    stage.resize(w, h)
    stage.show()
    code = app.exec()
    live2d.dispose()
    return code


if __name__ == "__main__":
    raise SystemExit(main())

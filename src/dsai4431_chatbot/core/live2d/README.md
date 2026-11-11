# 在 PyQt5 应用里播放 Live2D

两条路，都是可 `addWidget` 进现有布局的控件，不是独立小工具。

> `option_web_qt.py` / `option_native_qt.py` 是同一套东西的 PySide6 版本，留作参考；
> 你用的是 PyQt5，就只用下面两个 `pyqt5_*.py`（两者 API 基本一一对应）。

| | 方案 A：内嵌 Web 渲染 | 方案 B：原生渲染 |
|---|---|---|
| 文件 | `pyqt5_web.py` → `Live2DWidget` | `pyqt5_native.py` → `Live2DGLWidget` |
| 实现 | `QWebEngineView` 里跑 PixiJS + pixi-live2d-display + Cubism **Web** Core | `QOpenGLWidget` + `live2d-py`（Cubism **Native** SDK 的 C 扩展） |
| 与 [jingyu-live2d-agent](https://github.com/InariNGT-Ofiicial/jingyu-live2d-agent) | 同一套栈，`web/engine.mjs` 的思路可直接搬 | 完全不同的实现 |
| 依赖 | `pip install PyQt5 PyQtWebEngine` + 3 个 js 文件 | `pip install PyQt5 live2d-py`（Python ≥ 3.11） |
| 保真度 | 官方 Web 示例级：物理 / 表情 / 口型 / motion3 全支持，Cubism 5 模型也能跑 | SDK 5-r.5，特性齐全；像素细节与 Web 版不完全一致 |
| 逐像素透明 | 支持（`page().setBackgroundColor(Qt.transparent)`） | 支持但挑驱动（`QSurfaceFormat` alpha + `WA_AlwaysStackOnTop`） |
| 适合 | 要物理、复杂交互、录屏导出 | 要"别背一个 Chromium"，启动快、包体小 |

## 一、方案 A：QWebEngineView

```powershell
pip install PyQt5 PyQtWebEngine      # QtWebEngine 自 PyQt5 5.12 起是独立包
```

```python
from pyqt5_web import Live2DWidget        # 必须写在文件顶部，早于 QApplication 创建

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.live2d = Live2DWidget("D:/models/大肥鱼/大肥鱼.model3.json", parent=self)
        self.setCentralWidget(self.live2d)
        self.live2d.ready.connect(lambda: self.live2d.motion("Idle"))

    # 任意位置控制
    # self.live2d.expression("f01")
    # self.live2d.set_param("ParamMouthOpenY", 0.6)   # 口型
```

三个必须知道的点：

1. **两个硬性顺序**
   `QApplication.setAttribute(Qt.AA_ShareOpenGLContexts, True)` 和
   `from PyQt5.QtWebEngineWidgets import QWebEngineView` 都必须在 `QApplication` 创建**之前**完成，
   否则会崩或黑屏。`pyqt5_web.py` 在模块 import 时就把这两件事做完了，所以你的 `import` 要放文件顶部。
2. **必须走 http://，不能 file://**
   pixi-live2d-display 用 `fetch` 读 `model3.json`，再按 json 里的相对路径取 moc3 与贴图；
   `file://` 会被 CORS 拦死。`pyqt5_web.py` 里用 `ThreadingHTTPServer` 在 `127.0.0.1:随机端口`
   起个只服务本机的静态服务，并把 `/model/` 重写到模型目录（模型放哪个盘都行）。
3. **控制走 `runJavaScript`**
   `motion() / expression() / set_param()` 都是拼一句 JS 丢进页面执行；
   页面在 `window.l2d` 上暴露了模型对象。要 JS 反向调 Python 用 `QWebChannel`。

## 二、方案 B：live2d-py + QOpenGLWidget

```powershell
pip install PyQt5 live2d-py
```

```python
from pyqt5_native import Live2DGLWidget

self.stage = Live2DGLWidget("D:/models/大肥鱼/大肥鱼.model3.json", parent=self)
layout.addWidget(self.stage)
self.stage.motion("Idle")
self.stage.lip_sync(rms, gain=3.0)      # 把音频 RMS 塞进 ParamMouthOpenY
```

实现就是四个回调：`initializeGL` 里 `live2d.glInit()` + `LoadModelJson`；
`paintGL` 里 `Update()` → `clearBuffer()` → `Draw()`；`resizeGL` 里 `Resize()`；
鼠标 `mouseMoveEvent` 里 `Drag()`、`mousePressEvent` 里 `HitPart()`。

## 三、两个方案都要

把 `vendor/live2dcubismcore.min.js` 放到 `vendor/`（**本目录不含**，Live2D 许可要求使用者自己获取）：

1. <https://www.live2d.com/en/sdk/download/web/> 下载 Cubism SDK for Web
2. 取出 Core 文件，改名 `live2dcubismcore.min.js` 放进 `vendor/`
3. `vendor/` 里已有 `pixi.min.js`(6.5.10) 与 `cubism4.min.js`(pixi-live2d-display 0.4.0)，来自鲸语仓库

## 四、本机验证到哪一步

| 项目 | 结果 |
|---|---|
| 两个 .py 语法编译 | 通过 |
| `index.html` 的 module 脚本 `node --check` | 通过 |
| 静态服务 + `/model/` 路由（html/vendor/json/moc3/png/404） | 实测 200/404 全部正确 |
| PyQt5 5.15.11 各枚举（`AA_ShareOpenGLContexts`、`WindowTransparentForInput`、`WA_AlwaysStackOnTop` …） | 实测存在 |
| **方案 B：真窗口 + `glInit()` + `clearBuffer()` + 5 帧 paintGL** | **实测通过，干净退出 0** |
| **方案 B：`LoadModelJson` 传入非法 model3.json** | **进程直接 0xC0000409 崩溃**（C++ 层异常，Python `try/except` 兜不住） |
| 方案 A：`QWebEngineView` 实机 | 未验证 —— 本机没装 `PyQtWebEngine`，沙箱挡了 pip 写入 |

由第 6 项得到一条实用结论：**别指望用 `try/except` 兜模型加载失败**。
在调用 `LoadModelJson` 之前先做存在性/可解析性检查，或者把加载放进独立子进程，
否则用户选错文件时整个 GUI 会无声消失。

## 五、嵌进已有 GUI 的注意点

- **线程**：Qt 控件、GL 上下文、`runJavaScript` 全部只能在 GUI 线程；HTTP 服务是 daemon 线程，安全。
- **尺寸**：两个控件都跟随布局；`QOpenGLWidget` 里按 `devicePixelRatioF()` 统一缩放 `Resize` 与 `Drag`，否则 125% 缩放下点击会错位。
- **透明桌宠**：`Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.Tool` + `WA_TranslucentBackground`；
  鼠标穿透用 `Qt.WindowTransparentForInput`，留一个托盘菜单切回来，否则窗口会变得点不到。
- **多 GL 控件**：一个进程里多个 `QOpenGLWidget` 共享上下文，若互相干扰给本控件 `setUpdateBehavior(NoPartialUpdate)`。
- **打包**：PyInstaller 有 PyQt5/QtWebEngine 的 hook，通常会带上 `QtWebEngineProcess.exe` 与 `resources/`；
  若打出来白屏，用 `--collect-data PyQt5` 并检查 `QtWebEngineProcess.exe` 是否在包里。
  个别虚拟机上 WebGL 不可用，可设 `QTWEBENGINE_CHROMIUM_FLAGS=--disable-gpu` 兜底（会掉帧）。

## 六、许可

- Cubism Core（Web / Native）是 Live2D 专有运行库，不能再分发，按官方协议使用。
- `pixi.min.js` MIT、`cubism4.min.js`（pixi-live2d-display）MIT、`live2d-py` MIT（但其依赖的 Cubism Native SDK 另有条款）。
- 角色模型、贴图、PSD 的权利属于原画师/建模师，与代码许可无关。

"""demo_interactive.py —— 路线 A（QWebEngineView + Cubism Web）的可上手试验台。

和 pyqt5_web.py 的区别：那个是"给你往自己 GUI 里塞的控件"，
这个是"你自己玩的控制台"：按钮、滑块、开关、截图、桌宠，全部现场可操作。

两种模式
--------
probe 模式（`--probe`，或本机找不到模型时自动进入）
    不需要 Cubism Core、不需要模型文件。用一个 Canvas 占位角色把
    「Qt 窗口 ↔ 本地 HTTP 服务 ↔ QWebEngineView ↔ Python↔JS 双向控制 ↔ 截图导出」
    整条链路跑通。用来确认环境和交互逻辑，现在就能测。

live 模式（`--model x/xxx.model3.json`）
    真实 Live2D 模型。需要 vendor/live2dcubismcore.min.js。
    动作组 / 表情名从运行时的 model3.json 里读，不用手写。

用法
----
    python demo_interactive.py --probe
    python demo_interactive.py --model "D:/models/hiyori/hiyori.model3.json"
    python demo_interactive.py --probe --pet          # 透明桌宠模式演示

依赖
----
    pip install PyQt5 PyQtWebEngine
"""

from __future__ import annotations

import argparse
import base64
import json
import math
import os
import sys
import threading
import traceback
from datetime import datetime
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import quote

HERE = Path(__file__).resolve().parent


def _resolve_asset_root() -> Path:
    """资源根目录 asset/live2d。

    代码在 src/dsai4431_chatbot/core/live2d/，而依赖库和模型在项目根的
    asset/live2d/ 下，所以从本文件所在目录逐级向上找 <repo>/asset/live2d。
    目录结构换了就用环境变量 L2D_ASSET_DIR 直接指过去。
    """
    env = os.environ.get("L2D_ASSET_DIR")
    if env:
        return Path(env).expanduser().resolve()
    for base in (HERE, *HERE.parents):
        cand = base / "asset" / "live2d"
        if cand.is_dir():
            return cand
    return HERE / "asset" / "live2d"


ASSET_ROOT = _resolve_asset_root()
VENDOR_DIR = ASSET_ROOT / "vendor"
MODELS_DIR = ASSET_ROOT / "models"
MODEL_PREFIX = "/model/"
VENDOR_PREFIX = "/vendor/"
CORE_FILE = VENDOR_DIR / "live2dcubismcore.min.js"
PAGE_LIVE = "demo_live2d.html"
PAGE_PROBE = "demo_probe.html"

BANNER = "=" * 70


def die(msg: str, hint: str = "") -> None:
    print(f"\n{BANNER}\n{msg}")
    if hint:
        print(f"\n{hint}")
    print(f"{BANNER}\n", flush=True)
    raise SystemExit(2)


# ---------------------------------------------------------------------------
# 依赖检查（PyQtWebEngine 必须在 QApplication 之前 import）
# ---------------------------------------------------------------------------
try:
    from PyQt5.QtCore import Qt, QTimer, QUrl, pyqtSignal
    from PyQt5.QtGui import QCursor
    from PyQt5.QtWidgets import (
        QApplication,
        QCheckBox,
        QComboBox,
        QFileDialog,
        QFrame,
        QGroupBox,
        QHBoxLayout,
        QLabel,
        QMainWindow,
        QPushButton,
        QScrollArea,
        QSlider,
        QTabWidget,
        QVBoxLayout,
        QWidget,
    )
except ImportError as exc:
    die(f"缺少 PyQt5：{exc}", "pip install PyQt5")

# ---------------------------------------------------------------------------
# 必须在 import QtWebEngineWidgets 之前设的两个环境变量
#
# PyQtWebEngine 5.15 内置的 Chromium 是 83 版。在本机实测：它自带的渲染进程沙箱
# 会让 QtWebEngineProcess 起不来 —— 表现是 loadProgress 一路到 100%，但
# loadFinished 永不触发、网页 JS 一行都不执行、窗口一片白。
# 实测结论：不加 flag、只加 --disable-gpu 都白屏；加 --no-sandbox 才正常。
#
# 这是对 Chromium 渲染沙箱的降级（不影响主进程和本地静态服务）。
# 介意的话设 L2D_KEEP_SANDBOX=1 跳过，自己处理环境。
# ---------------------------------------------------------------------------
if not os.environ.get("L2D_KEEP_SANDBOX"):
    os.environ.setdefault("QTWEBENGINE_DISABLE_SANDBOX", "1")
    _chromium_flags = os.environ.get("QTWEBENGINE_CHROMIUM_FLAGS", "")
    if "--no-sandbox" not in _chromium_flags:
        os.environ["QTWEBENGINE_CHROMIUM_FLAGS"] = (_chromium_flags + " --no-sandbox").strip()

if QApplication.instance() is None:
    QApplication.setAttribute(Qt.AA_ShareOpenGLContexts, True)
    # 高分屏（4K / 系统 150%~200% 缩放）必须开这两个，否则整个界面会小到看不清：
    # PyQt5 默认按逻辑像素绘制，不跟随 Windows 的缩放比例。
    # 开了之后 15px 的字体在你屏幕上才是真正"15px 该有的样子"。
    try:
        QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)
        QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps, True)
    except AttributeError:
        pass

try:
    from PyQt5.QtWebEngineWidgets import QWebEngineView  # noqa: E402
except ImportError as exc:
    die(
        f"缺少 PyQtWebEngine：{exc}",
        "pip install PyQtWebEngine\n"
        "（QtWebEngine 自 PyQt5 5.12 起是独立包，光装 PyQt5 不够）",
    )


# ---------------------------------------------------------------------------
# 静态服务：代码目录作站点根，/model/ 与 /vendor/ 分别映射到 asset/live2d 下。
# HTML 里的 <script src="vendor/xxx.js"> 因此不用改：浏览器请求 /vendor/xxx.js，
# 这里改写到 ASSET_ROOT/vendor/xxx.js 再交给父类去读。
# ---------------------------------------------------------------------------
class _Handler(SimpleHTTPRequestHandler):
    def __init__(self, *args, model_dir: str = str(MODELS_DIR), **kwargs):
        self._model_dir = model_dir
        super().__init__(*args, directory=str(HERE), **kwargs)

    def log_message(self, *args):  # 静音
        pass

    def do_GET(self):
        for prefix, target in (
            (MODEL_PREFIX, self._model_dir),
            (VENDOR_PREFIX, str(VENDOR_DIR)),
        ):
            if self.path.startswith(prefix):
                saved_path, saved_dir = self.path, self.directory
                self.path = self.path[len(prefix) - 1 :]
                self.directory = target
                try:
                    return super().do_GET()
                finally:
                    self.path, self.directory = saved_path, saved_dir
        return super().do_GET()


def _serve(model_dir: Path) -> tuple[ThreadingHTTPServer, int]:
    srv = ThreadingHTTPServer(
        ("127.0.0.1", 0), partial(_Handler, model_dir=str(model_dir))
    )
    srv.daemon_threads = True
    threading.Thread(target=srv.serve_forever, daemon=True).start()
    return srv, srv.server_port


# ---------------------------------------------------------------------------
# 模型体检（在交给浏览器之前拦掉明显错误，报错比白屏好查）
# ---------------------------------------------------------------------------
def validate_model(model_json: Path) -> dict:
    if not model_json.is_file():
        raise ValueError(f"模型文件不存在：{model_json}")

    try:
        doc = json.loads(model_json.read_text(encoding="utf-8-sig"))
    except Exception as exc:
        raise ValueError(f"model3.json 解析失败：{exc}") from exc
    if not isinstance(doc, dict):
        raise ValueError("model3.json 顶层不是对象")

    refs = doc.get("FileReferences") or {}
    if not isinstance(refs, dict):
        raise ValueError("model3.json 的 FileReferences 不是对象")

    moc_rel = refs.get("Moc")
    if not moc_rel:
        raise ValueError("model3.json 里没有 FileReferences.Moc")
    moc_path = model_json.parent / moc_rel
    if not moc_path.is_file():
        raise ValueError(f"缺 moc3 文件：{moc_path}")
    with moc_path.open("rb") as fh:
        head = fh.read(4)
    if head != b"MOC3":
        raise ValueError(f"moc3 文件头不是 MOC3（读到 {head!r}）：{moc_path}")

    textures = refs.get("Textures") or []
    if not textures:
        raise ValueError("model3.json 里没有 FileReferences.Textures")
    missing = [t for t in textures if not (model_json.parent / t).is_file()]
    if missing:
        more = " ..." if len(missing) > 3 else ""
        raise ValueError("缺贴图：" + ", ".join(map(str, missing[:3])) + more)

    motions = {}
    for group, items in (refs.get("Motions") or {}).items():
        motions[group] = len(items) if isinstance(items, list) else 0
    expressions = [
        e.get("Name") or Path(e.get("File", "")).stem
        for e in (refs.get("Expressions") or [])
        if isinstance(e, dict)
    ]

    return {
        "motions": motions,
        "expressions": [e for e in expressions if e],
        "textures": len(textures),
        "moc": str(moc_path),
    }


def find_models(roots: list[Path], limit: int = 20) -> list[Path]:
    """递归找 model3.json，跳过 .venv，并让 *.demo.model3.json 排在最前。

    demo 版是 make_demo_model.py 生成的（带动作/表情引用），比原版更适合本程序。
    """
    found: list[Path] = []
    for root in roots:
        if not root.is_dir():
            continue
        try:
            for p in root.rglob("*.model3.json"):
                if ".venv" in p.parts or "__pycache__" in p.parts:
                    continue
                found.append(p)
        except OSError:
            continue
    # demo 版优先，其次路径短的
    found.sort(key=lambda p: (0 if p.name.endswith(".demo.model3.json") else 1, len(str(p))))
    return found[:limit]


# ---------------------------------------------------------------------------
# JS 参数序列化
# ---------------------------------------------------------------------------
def jsv(value) -> str:
    if value is None:
        return "null"
    if isinstance(value, bool):
        return "true" if value else "false"
    if isinstance(value, int):
        return str(value)
    if isinstance(value, float):
        return repr(value)
    return json.dumps(str(value), ensure_ascii=False)


# ---------------------------------------------------------------------------
# 舞台控件
# ---------------------------------------------------------------------------
class Stage(QWidget):
    ready = pyqtSignal()
    failed = pyqtSignal(str)

    def __init__(self, *, page: str, model_json: Path | None, parent=None):
        super().__init__(parent)
        self._page = page
        self._model_json = model_json
        model_dir = model_json.parent if model_json else MODELS_DIR

        self._server, port = _serve(model_dir)
        self._view = QWebEngineView(self)
        lay = QVBoxLayout(self)
        lay.setContentsMargins(0, 0, 0, 0)
        lay.addWidget(self._view)

        if model_json:
            url = f"http://127.0.0.1:{port}/{page}?m={quote(model_json.name)}"
        else:
            url = f"http://127.0.0.1:{port}/{page}"
        self._view.load(QUrl(url))

        self._polls = 0
        self._done = False
        self._timer = QTimer(self)
        self._timer.setInterval(120)
        self._timer.timeout.connect(self._check)
        self._timer.start()

        # 鼠标位置轮询：QWebEngineView 不保证把 mousemove 转发给页面，
        # 所以由 Qt 这边读全局光标位置，直接推给渲染端做头部跟随。
        self._aim = (0.0, 0.0)
        self._aim_timer = QTimer(self)
        self._aim_timer.setInterval(60)
        self._aim_timer.timeout.connect(self._poll_mouse)
        self._aim_timer.start()

    # --- 鼠标位置 → 渲染端 ------------------------------------------------
    def _poll_mouse(self):
        if not self._done:
            return
        try:
            p = self._view.mapFromGlobal(QCursor.pos())
            r = self._view.rect()
            w, h = r.width(), r.height()
            if w <= 0 or h <= 0:
                return
            nx = max(-1.0, min(1.0, (p.x() / w) * 2 - 1))
            ny = max(-1.0, min(1.0, (p.y() / h) * 2 - 1))
            ox, oy = self._aim
            # 变化太小就不发，省一次跨进程 JS 调用
            if abs(nx - ox) < 0.008 and abs(ny - oy) < 0.008:
                return
            self._aim = (nx, ny)
            self.call("setAim", round(nx, 3), round(ny, 3))
        except Exception:
            pass

    # --- 就绪探测 ---------------------------------------------------------
    def _check(self):
        self._polls += 1

        def cb(result):
            # 大模型加载慢时 runJavaScript 的回调会积压，停止定时器后仍有一批
            # pending 回调会陆续回来 —— 用标志位保证 ready/failed 只发一次。
            if self._done:
                return
            if result is True:
                self._done = True
                self._timer.stop()
                self.ready.emit()
            elif result:
                self._done = True
                self._timer.stop()
                self.failed.emit(str(result))
            elif self._polls > 620:  # ~75 秒
                self._done = True
                self._timer.stop()
                self.failed.emit("等待页面就绪超时（75s）")

        self._view.page().runJavaScript(
            "window.l2dReady === true ? true : (window.l2dError || '')", cb
        )

    # --- 调用 -------------------------------------------------------------
    def js(self, code: str, cb=None):
        if cb is None:
            self._view.page().runJavaScript(code)
        else:
            self._view.page().runJavaScript(code, cb)

    def call(self, method: str, *args, cb=None):
        payload = ", ".join(jsv(a) for a in args)
        self.js(f"window.l2d ? l2d.{method}({payload}) : null", cb)

    # --- 生命周期 ---------------------------------------------------------
    def shutdown(self):
        try:
            self._timer.stop()
        except Exception:
            pass
        try:
            self._server.shutdown()
            self._server.server_close()
        except Exception:
            pass
        try:
            self._view.deleteLater()
        except Exception:
            pass

    def closeEvent(self, event):  # noqa: N802
        self.shutdown()
        super().closeEvent(event)


# ---------------------------------------------------------------------------
# 参数滑块表（StandardParamsV3 常用项；模型没有的参数会被 Cubism 忽略）
# ---------------------------------------------------------------------------
PARAM_TABS: list[tuple[str, list[tuple[str, str, float, float]]]] = [
    (
        "头部",
        [
            ("ParamAngleX", "转头（左右）", -30.0, 30.0),
            ("ParamAngleY", "抬头（上下）", -30.0, 30.0),
            ("ParamAngleZ", "歪头", -30.0, 30.0),
            ("ParamBodyAngleX", "身体倾斜", -10.0, 10.0),
            ("ParamBodyAngleY", "身体前后", -10.0, 10.0),
        ],
    ),
    (
        "眼睛",
        [
            ("ParamEyeLOpen", "左眼睁开", 0.0, 1.0),
            ("ParamEyeROpen", "右眼睁开", 0.0, 1.0),
            ("ParamEyeBallX", "瞳孔左右", -1.0, 1.0),
            ("ParamEyeBallY", "瞳孔上下", -1.0, 1.0),
        ],
    ),
    (
        "嘴、眉",
        [
            ("ParamMouthOpenY", "张嘴", 0.0, 1.0),
            ("ParamMouthForm", "嘴角（笑/哭）", -1.0, 1.0),
            ("ParamBrowLY", "左眉", -1.0, 1.0),
            ("ParamBrowRY", "右眉", -1.0, 1.0),
        ],
    ),
    (
        "其它",
        [
            ("ParamBreath", "呼吸量", 0.0, 1.0),
            ("ParamArmLA", "左臂", 0.0, 1.0),
            ("ParamArmRA", "右臂", 0.0, 1.0),
            ("ParamHairFront", "前发摆动", -1.0, 1.0),
        ],
    ),
]

DARK_QSS = """
QWidget { background:#1b1f24; color:#c8d4e0;
          font-family:'Segoe UI','Microsoft YaHei UI'; font-size:15px; }
QMainWindow { background:#12161b; }
QTabWidget::pane { border:1px solid #2a333d; background:#1b1f24; }
QTabBar::tab { background:#232b34; padding:9px 18px; margin-right:2px;
               border:1px solid #2a333d; border-bottom:none; color:#93a4b5; }
QTabBar::tab:selected { background:#2e3a46; color:#8fc7ff; }
QPushButton { background:#28323d; border:1px solid #37485a; padding:8px 14px;
              border-radius:4px; color:#c8d4e0; }
QPushButton:hover { background:#31404f; }
QPushButton:pressed { background:#1e2833; }
QPushButton:disabled { color:#5a6572; border-color:#2a333d; }
QComboBox { background:#232b34; border:1px solid #37485a; padding:6px 9px;
            min-height:22px; }
QComboBox QAbstractItemView { background:#232b34; selection-background-color:#31404f;
                              font-size:15px; }
QSlider::groove:horizontal { height:7px; background:#2a333d; border-radius:3px; }
QSlider::handle:horizontal { width:18px; height:18px; margin:-6px 0; background:#5c88b8;
                             border-radius:9px; }
QSlider::handle:horizontal:hover { background:#7aa8d8; }
QGroupBox { border:1px solid #2a333d; margin-top:18px; padding-top:12px;
            border-radius:4px; font-size:15px; }
QGroupBox::title { subcontrol-origin: margin; left:12px; padding:0 6px;
                   color:#8fb4d8; }
QCheckBox { spacing:10px; font-size:15px; }
QCheckBox::indicator { width:18px; height:18px; border:1px solid #37485a;
                       background:#232b34; border-radius:3px; }
QCheckBox::indicator:checked { background:#5c88b8; border-color:#7aa8d8; }
QScrollArea { border:none; }
QLabel { font-size:15px; }
QLabel#status { color:#8b9aa9; font-size:14px; }
"""


class DemoWindow(QMainWindow):
    def __init__(self, *, probe: bool, model_json: Path | None, size: tuple[int, int]):
        super().__init__()
        self._probe = probe
        self._model_json = model_json
        self._sliders: dict[str, tuple[QSlider, QLabel, float, float]] = {}
        self._stage: Stage | None = None
        self._talk_phase = 0.0
        self._stage_ready = False
        self._meta: dict = {}

        self.resize(*size)
        self._build_chrome()
        self._talk_timer = QTimer(self)
        self._talk_timer.setInterval(40)
        self._talk_timer.timeout.connect(self._talk_tick)

        self._mount_stage(probe=probe, model_json=model_json)

    # --- 界面骨架 ---------------------------------------------------------
    def _build_chrome(self):
        root = QWidget()
        outer = QHBoxLayout(root)
        outer.setContentsMargins(0, 0, 0, 0)
        outer.setSpacing(0)

        self._stage_host = QWidget()
        self._stage_host_lay = QVBoxLayout(self._stage_host)
        self._stage_host_lay.setContentsMargins(0, 0, 0, 0)
        outer.addWidget(self._stage_host, 1)

        panel = QWidget()
        panel.setFixedWidth(460)
        pv = QVBoxLayout(panel)
        pv.setContentsMargins(12, 12, 12, 12)
        pv.setSpacing(9)

        self._tabs = QTabWidget()
        self._tabs.addTab(self._tab_motion(), "动作")
        self._tabs.addTab(self._tab_expression(), "表情")
        self._tabs.addTab(self._tab_params(), "参数")
        self._tabs.addTab(self._tab_settings(), "设置")
        pv.addWidget(self._tabs, 1)

        self._status = QLabel("初始化中…")
        self._status.setObjectName("status")
        self._status.setWordWrap(True)
        pv.addWidget(self._status)

        outer.addWidget(panel, 0)
        self.setCentralWidget(root)

    # --- 动作页 -----------------------------------------------------------
    def _tab_motion(self) -> QWidget:
        w = QWidget()
        v = QVBoxLayout(w)
        v.setContentsMargins(10, 10, 10, 10)
        v.setSpacing(8)

        # ---- 互动反应（程序化编排，不依赖模型自带的 motion3）----
        v.addWidget(QLabel("互动反应"))
        row_rx = QHBoxLayout()
        b_tap = QPushButton("戳一下")
        b_tap.setToolTip("紧闭眼睛 + 歪头（参数时间轴，约 1 秒）")
        b_tap.clicked.connect(lambda: self.react("tap"))
        b_pat = QPushButton("摸摸头")
        b_pat.setToolTip("眯眼 + 微笑 + 脸红 + 头微低（约 2 秒）")
        b_pat.clicked.connect(lambda: self.react("headpat"))
        row_rx.addWidget(b_tap)
        row_rx.addWidget(b_pat)
        v.addLayout(row_rx)

        row_rx2 = QHBoxLayout()
        b_loop = QPushButton("摸头（循环）")
        b_loop.setToolTip("像 GIF 一样一直循环：眯眼微笑脸红 + 头轻轻晃。再点一次停止")
        b_loop.setCheckable(True)
        b_loop.toggled.connect(self._toggle_headpat_loop)
        self._loop_btn = b_loop
        b_stop = QPushButton("停止")
        b_stop.setToolTip("停掉当前正在播的反应")
        b_stop.clicked.connect(self.stop_reaction)
        row_rx2.addWidget(b_loop)
        row_rx2.addWidget(b_stop)
        v.addLayout(row_rx2)

        line = QFrame()
        line.setFrameShape(QFrame.HLine)
        line.setStyleSheet("color:#2a333d;")
        v.addWidget(line)

        v.addWidget(QLabel("动作组（来自 model3.json 的 Motions）"))
        self._motion_group = QComboBox()
        self._motion_group.currentIndexChanged.connect(self._on_motion_group_changed)
        v.addWidget(self._motion_group)

        row = QHBoxLayout()
        self._motion_index = QComboBox()
        row.addWidget(self._motion_index, 1)
        v.addLayout(row)

        row2 = QHBoxLayout()
        b_play = QPushButton("播放")
        b_play.clicked.connect(self._play_motion)
        b_rand = QPushButton("随机动作")
        b_rand.clicked.connect(lambda: self._stage and self._stage.call("randomMotion"))
        row2.addWidget(b_play)
        row2.addWidget(b_rand)
        v.addLayout(row2)

        self._motion_hint = QLabel("")
        self._motion_hint.setWordWrap(True)
        self._motion_hint.setStyleSheet("color:#6f7f8f;")
        v.addWidget(self._motion_hint)
        v.addStretch(1)
        return w

    def _tab_expression(self) -> QWidget:
        w = QWidget()
        v = QVBoxLayout(w)
        v.setContentsMargins(10, 10, 10, 10)
        v.setSpacing(8)

        v.addWidget(QLabel("表情（expressions/*.exp3.json 的 Name）"))
        self._expr_combo = QComboBox()
        v.addWidget(self._expr_combo)

        row = QHBoxLayout()
        b_apply = QPushButton("应用")
        b_apply.clicked.connect(
            lambda: self._stage
            and self._stage.call("expression", self._expr_combo.currentText())
        )
        b_rand = QPushButton("随机表情")
        b_rand.clicked.connect(lambda: self._stage and self._stage.call("randomExpression"))
        row.addWidget(b_apply)
        row.addWidget(b_rand)
        v.addLayout(row)

        b_reset = QPushButton("复位表情")
        b_reset.clicked.connect(lambda: self._stage and self._stage.call("resetExpression"))
        v.addWidget(b_reset)

        self._expr_hint = QLabel("")
        self._expr_hint.setWordWrap(True)
        self._expr_hint.setStyleSheet("color:#6f7f8f;")
        v.addWidget(self._expr_hint)
        v.addStretch(1)
        return w

    # --- 参数页 -----------------------------------------------------------
    def _tab_params(self) -> QWidget:
        holder = QWidget()
        outer = QVBoxLayout(holder)
        outer.setContentsMargins(0, 0, 0, 0)

        inner = QWidget()
        v = QVBoxLayout(inner)
        v.setContentsMargins(10, 10, 10, 10)
        v.setSpacing(4)

        for title, items in PARAM_TABS:
            box = QGroupBox(title)
            bv = QVBoxLayout(box)
            bv.setContentsMargins(8, 6, 8, 6)
            bv.setSpacing(3)
            for pid, label, lo, hi in items:
                bv.addWidget(self._param_row(pid, label, lo, hi))
            v.addWidget(box)

        row = QHBoxLayout()
        b_zero = QPushButton("全部归零")
        b_zero.clicked.connect(self._zero_all)
        row.addWidget(b_zero)
        v.addLayout(row)

        v.addSpacing(6)
        v.addWidget(QLabel("口型：按住下面的按钮时嘴巴跟着动"))
        self._talk_btn = QPushButton("按住说话（模拟口型）")
        self._talk_btn.pressed.connect(self._talk_start)
        self._talk_btn.released.connect(self._talk_stop)
        v.addWidget(self._talk_btn)

        v.addStretch(1)
        sc = QScrollArea()
        sc.setWidgetResizable(True)
        sc.setWidget(inner)
        outer.addWidget(sc)
        return holder

    def _param_row(self, pid: str, label: str, lo: float, hi: float) -> QWidget:
        row = QWidget()
        h = QHBoxLayout(row)
        h.setContentsMargins(0, 0, 0, 0)
        h.setSpacing(6)

        lb = QLabel(label)
        lb.setFixedWidth(116)

        slider = QSlider(Qt.Horizontal)
        slider.setRange(0, 1000)
        neutral = int(round((0 - lo) / (hi - lo) * 1000)) if lo < 0 < hi else 0
        slider.setValue(max(0, min(1000, neutral)))

        val = QLabel("0.00")
        val.setFixedWidth(64)
        val.setAlignment(Qt.AlignRight | Qt.AlignVCenter)

        def on_change(raw: int, pid=pid, lo=lo, hi=hi, val=val):
            v = lo + (hi - lo) * raw / 1000.0
            val.setText(f"{v:+.2f}" if lo < 0 else f"{v:.2f}")
            if self._stage:
                self._stage.call("set", pid, v)

        slider.valueChanged.connect(on_change)
        h.addWidget(lb)
        h.addWidget(slider, 1)
        h.addWidget(val)
        self._sliders[pid] = (slider, val, lo, hi)
        return row

    def _zero_all(self):
        for pid, (slider, _val, lo, hi) in self._sliders.items():
            slider.blockSignals(True)
            slider.setValue(int(round((0 - lo) / (hi - lo) * 1000)) if lo < 0 < hi else 0)
            slider.blockSignals(False)
            if self._stage:
                self._stage.call("set", pid, 0.0)

    def _talk_start(self):
        self._talk_phase = 0.0
        self._talk_timer.start()

    def _talk_stop(self):
        self._talk_timer.stop()
        if self._stage:
            self._stage.call("set", "ParamMouthOpenY", 0.0)

    def _talk_tick(self):
        self._talk_phase += 0.28
        # 双正弦叠加，比单正弦更像说话
        v = 0.5 + 0.5 * (
            math.sin(self._talk_phase) * 0.7 + math.sin(self._talk_phase * 2.7) * 0.3
        )
        if self._stage:
            self._stage.call("set", "ParamMouthOpenY", max(0.0, min(1.0, v)))

    # --- 设置页 -----------------------------------------------------------
    def _tab_settings(self) -> QWidget:
        w = QWidget()
        v = QVBoxLayout(w)
        v.setContentsMargins(10, 10, 10, 10)
        v.setSpacing(8)

        box = QGroupBox("自动行为")
        bv = QVBoxLayout(box)
        bv.setContentsMargins(8, 6, 8, 6)
        bv.setSpacing(5)

        self._cb_blink = QCheckBox("自动眨眼")
        self._cb_blink.setChecked(True)
        self._cb_blink.toggled.connect(
            lambda on: self._stage and self._stage.call("autoBlink", on)
        )
        self._cb_breath = QCheckBox("自动呼吸")
        self._cb_breath.setChecked(True)
        self._cb_breath.toggled.connect(
            lambda on: self._stage and self._stage.call("autoBreath", on)
        )
        self._cb_physics = QCheckBox("物理演算")
        self._cb_physics.setChecked(True)
        self._cb_physics.toggled.connect(
            lambda on: self._stage and self._stage.call("physics", on)
        )
        self._cb_follow = QCheckBox("鼠标视线跟随")
        self._cb_follow.setChecked(True)
        self._cb_follow.toggled.connect(
            lambda on: self._stage and self._stage.call("follow", on)
        )
        for cb in (self._cb_blink, self._cb_breath, self._cb_physics, self._cb_follow):
            bv.addWidget(cb)
        v.addWidget(box)

        box2 = QGroupBox("缩放")
        b2 = QVBoxLayout(box2)
        b2.setContentsMargins(8, 6, 8, 6)
        row = QHBoxLayout()
        self._zoom = QSlider(Qt.Horizontal)
        self._zoom.setRange(50, 250)
        self._zoom.setValue(100)
        self._zoom_label = QLabel("1.00x")
        self._zoom_label.setFixedWidth(64)
        self._zoom_label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)

        def on_zoom(raw: int):
            k = raw / 100.0
            self._zoom_label.setText(f"{k:.2f}x")
            if self._stage:
                self._stage.call("scale", k)

        self._zoom.valueChanged.connect(on_zoom)
        row.addWidget(self._zoom, 1)
        row.addWidget(self._zoom_label)
        b2.addLayout(row)
        v.addWidget(box2)

        box3 = QGroupBox("导出 / 窗口")
        b3 = QVBoxLayout(box3)
        b3.setContentsMargins(8, 6, 8, 6)
        b3.setSpacing(6)

        b_snap = QPushButton("截图保存 PNG")
        b_snap.clicked.connect(self._snapshot)
        b3.addWidget(b_snap)

        self._cb_pet = QCheckBox("透明桌宠模式（隐藏控制面板）")
        self._cb_pet.toggled.connect(self._toggle_pet)
        b3.addWidget(self._cb_pet)

        b3.addWidget(QLabel("（桌宠模式下面板隐藏，按 Esc 恢复）"))
        v.addWidget(box3)

        box4 = QGroupBox("模型")
        b4 = QVBoxLayout(box4)
        b4.setContentsMargins(8, 6, 8, 6)
        b_open = QPushButton("打开其他模型…")
        b_open.clicked.connect(self._pick_model)
        b4.addWidget(b_open)
        self._model_label = QLabel("—")
        self._model_label.setWordWrap(True)
        self._model_label.setStyleSheet("color:#6f7f8f;")
        b4.addWidget(self._model_label)
        v.addWidget(box4)

        v.addStretch(1)
        return w

    # --- 舞台装载 ---------------------------------------------------------
    def _mount_stage(self, *, probe: bool, model_json: Path | None):
        if self._stage is not None:
            self._stage_host_lay.removeWidget(self._stage)
            self._stage.shutdown()
            self._stage.deleteLater()
            self._stage = None
        self._stage_ready = False

        # 真实模型：Python 侧再解析一遍 model3.json，作为 JS 取不到时的兜底
        self._meta = {}
        if not probe and model_json is not None:
            try:
                self._meta = validate_model(model_json)
            except ValueError as exc:
                print(f"[warn] 复查模型失败：{exc}", flush=True)

        page = PAGE_PROBE if probe else PAGE_LIVE
        stage = Stage(page=page, model_json=None if probe else model_json)
        stage.ready.connect(self._on_ready)
        stage.failed.connect(self._on_failed)
        self._stage_host_lay.addWidget(stage)
        self._stage = stage

    def _on_ready(self):
        self._stage_ready = True
        tag = "PROBE（占位角色，无需素材）" if self._probe else "LIVE 2D"
        self.setWindowTitle(f"Live2D 试验台 · {tag}")
        self._status.setText(f"[{tag}] 已就绪，开始动手吧")
        print(f"[ready] {tag}", flush=True)

        def got(result):
            info = {}
            if isinstance(result, str):
                try:
                    info = json.loads(result)
                except Exception:
                    info = {}
            self._fill_from_info(info)

        if self._stage:
            self._stage.js("JSON.stringify(window.l2d ? l2d.info() : {})", got)

    def _on_failed(self, msg: str):
        self._status.setText(f"加载失败：{msg}")
        print(f"[failed] {msg}", flush=True)

    def _fill_from_info(self, info: dict):
        # 动作组：优先用页面运行时读到的，读不到就退回 Python 解析 model3.json 的结果
        groups = info.get("groups") or []
        if not groups and self._meta.get("motions"):
            groups = [{"name": k, "count": v} for k, v in self._meta["motions"].items()]

        self._motion_group.blockSignals(True)
        self._motion_group.clear()
        if groups:
            for g in groups:
                name = g.get("name") if isinstance(g, dict) else str(g)
                count = g.get("count") if isinstance(g, dict) else 1
                self._motion_group.addItem(f"{name}  ({count})", (name, int(count or 1)))
        else:
            self._motion_group.addItem("（无动作组）", ("", 0))
        self._motion_group.blockSignals(False)
        self._on_motion_group_changed()

        # 表情：同样双来源。pixi-live2d-display 不同版本里 expressionManager 挂的位置不一样，
        # 所以 Python 侧解析的 Expressions 是必须的兜底。
        expressions = info.get("expressions") or self._meta.get("expressions") or []
        expressions = [str(e) for e in expressions if e]
        self._expr_combo.clear()
        self._expr_combo.setEnabled(True)
        if expressions:
            self._expr_combo.addItems(expressions)
            self._expr_hint.setText(f"共 {len(expressions)} 个表情")
        else:
            self._expr_combo.addItem("（无表情）")
            self._expr_combo.setEnabled(False)
            self._expr_hint.setText(
                "这个模型没带 expression3 文件。"
                "表情是模型作者在 Cubism Editor 里做的，不是代码能凭空生成的。"
            )

        size = info.get("size") or []
        bits = []
        if size and len(size) == 2:
            try:
                bits.append(f"模型尺寸 {float(size[0]):.0f}×{float(size[1]):.0f}")
            except Exception:
                pass
        if info.get("mode") == "probe":
            bits.append("probe 占位角色")
            self._cb_physics.setEnabled(False)
        else:
            bits.append("物理 " + ("有" if info.get("hasPhysics") else "无"))
            bits.append("眨眼 " + ("有" if info.get("hasEyeBlink") else "无"))
        if self._model_json:
            bits.append(self._model_json.parent.name)
            self._model_label.setText(str(self._model_json))
        else:
            self._model_label.setText("（probe 模式，未载入真实模型）")
        self._status.setText("  ·  ".join(bits) if bits else "已就绪")

        if self._probe:
            self._motion_hint.setText(
                "probe 模式的动作用的是假数据，只验证通道是否通。"
            )

    def _on_motion_group_changed(self, *_):
        data = self._motion_group.currentData() or ("", 0)
        _name, count = data
        self._motion_index.clear()
        for i in range(max(1, int(count))):
            self._motion_index.addItem(f"#{i}", i)
        self._motion_index.setEnabled(int(count) > 1)

    def _play_motion(self):
        data = self._motion_group.currentData() or ("", 0)
        name, _count = data
        if not name or not self._stage:
            return
        self._stage.call("motion", name, self._motion_index.currentIndex())

    # --- 截图 -------------------------------------------------------------
    def _snapshot(self):
        if not self._stage:
            return

        def got(data):
            if not isinstance(data, str) or not data.startswith("data:"):
                self._status.setText("截图失败：页面没有返回图像")
                return
            try:
                raw = base64.b64decode(data.split(",", 1)[1])
            except Exception as exc:
                self._status.setText(f"截图解码失败：{exc}")
                return
            out = HERE / f"live2d_{datetime.now():%Y%m%d_%H%M%S}.png"
            try:
                out.write_bytes(raw)
            except OSError as exc:
                self._status.setText(f"写文件失败：{exc}")
                return
            self._status.setText(f"已保存 {out.name}（{len(raw) // 1024} KB）")
            print(f"[snapshot] {out}", flush=True)

        self._stage.call("snapshot", cb=got)

    # --- 互动反应 ---------------------------------------------------------
    def react(self, name: str) -> bool:
        """触发一个互动反应，给外部软件调用。

        name = 'tap'          被戳一下：瞬间闭紧眼睛 + 歪头 + 皱眉（约 1 秒）
        name = 'headpat'      被摸头：眯眼 + 微笑 + 脸红 + 头微低（约 2 秒）
        name = 'headpatLoop'  摸头循环：像 GIF 一样一直播，直到 stop_reaction()

        反应在渲染端用参数时间轴播放，不占模型自带的 motion 队列，
        所以随时触发都会立刻生效，也不会和换装动作互相打断。

        用法（拿到窗口实例后）：
            win.react('tap')
            win.react('headpat')
            win.react('headpatLoop')
            win.stop_reaction()
        """
        if not self._stage:
            return False
        self._stage.call("react", name)
        return True

    def stop_reaction(self) -> bool:
        """停掉当前正在播的反应（循环版必须靠它停）。"""
        if not self._stage:
            return False
        self._stage.call("stopReaction")
        btn = getattr(self, "_loop_btn", None)
        if btn is not None and btn.isChecked():
            btn.blockSignals(True)
            btn.setChecked(False)
            btn.blockSignals(False)
        return True

    def _toggle_headpat_loop(self, on: bool) -> None:
        if not self._stage:
            return
        if on:
            self._stage.call("react", "headpatLoop")
        else:
            self._stage.call("stopReaction")

    # --- 桌宠 -------------------------------------------------------------
    def _toggle_pet(self, on: bool):
        if on:
            self.setAttribute(Qt.WA_TranslucentBackground, True)
            self._tabs.parentWidget().setVisible(False)
            self._status.setVisible(False)
            self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.Tool)
            self.setStyleSheet("background: transparent;")
        else:
            self.setWindowFlags(Qt.Widget)
            self.setStyleSheet("")
            self._tabs.parentWidget().setVisible(True)
            self._status.setVisible(True)
        self.show()

    def keyPressEvent(self, event):  # noqa: N802
        if event.key() == Qt.Key_Escape and self._cb_pet.isChecked():
            self._cb_pet.setChecked(False)
            return
        super().keyPressEvent(event)

    # --- 换模型 -----------------------------------------------------------
    def _pick_model(self):
        path, _ = QFileDialog.getOpenFileName(
            self, "选择 model3.json", str(ASSET_ROOT), "Live2D 模型 (*.model3.json);;所有文件 (*)"
        )
        if not path:
            return
        target = Path(path)
        try:
            validate_model(target)
        except ValueError as exc:
            self._status.setText(f"模型体检不通过：{exc}")
            print(f"[invalid] {exc}", flush=True)
            return
        if not CORE_FILE.is_file():
            self._status.setText("缺少 vendor/live2dcubismcore.min.js，无法切到真实模型")
            return
        self._probe = False
        self._model_json = target
        self._cb_physics.setEnabled(True)
        self._mount_stage(probe=False, model_json=target)
        self._status.setText(f"正在载入 {target.name} …")

    def closeEvent(self, event):  # noqa: N802
        self._talk_timer.stop()
        if self._stage:
            self._stage.shutdown()
        super().closeEvent(event)


# ---------------------------------------------------------------------------
# 入口
# ---------------------------------------------------------------------------
def main() -> int:
    ap = argparse.ArgumentParser(
        description="路线 A（QWebEngineView + Cubism Web）交互式试验台"
    )
    ap.add_argument("--model", help="xxx.model3.json 的完整路径")
    ap.add_argument("--probe", action="store_true", help="不需要 Core / 模型的自检模式")
    ap.add_argument("--size", default="1120x860", help="窗口尺寸，如 1120x860")
    ap.add_argument("--pet", action="store_true", help="启动即进入透明桌宠模式")
    args = ap.parse_args()

    try:
        w, h = (int(x) for x in args.size.lower().split("x"))
    except ValueError:
        die(f"--size 格式应为 宽x高，收到的是：{args.size!r}")

    probe = bool(args.probe)
    model_json: Path | None = None

    if args.model:
        model_json = Path(args.model).expanduser().resolve()
        try:
            meta = validate_model(model_json)
        except ValueError as exc:
            die(f"模型体检不通过：{exc}", "换一个完整的模型目录再试，或者先跑 --probe")
        print(f"[model] {model_json}")
        print(f"[model] 动作组 {meta['motions'] or '（无）'}")
        print(f"[model] 表情    {meta['expressions'] or '（无）'}")
        print(f"[model] 贴图    {meta['textures']} 张")
        if not CORE_FILE.is_file():
            die(
                f"缺少 Cubism Web Core：{CORE_FILE}",
                "下载：https://www.live2d.com/en/sdk/download/web/\n"
                "取 Cubism SDK for Web 里的 Core，改名 live2dcubismcore.min.js "
                "放进 asset/live2d/vendor/",
            )
    else:
        found = find_models([ASSET_ROOT])
        if found and not probe:
            model_json = found[0]
            print(f"[auto] 发现模型：{model_json}")
            try:
                m = validate_model(model_json)
                print(
                    f"[auto] 动作组 {m['motions'] or '（无）'}  ·  "
                    f"表情 {len(m['expressions'])} 个  ·  贴图 {m['textures']} 张"
                )
            except ValueError as exc:
                print(f"[auto] 模型体检警告：{exc}")
            print("[auto] 想强制用占位角色请加 --probe")
        else:
            probe = True
            if not found:
                print("[auto] 没找到 *.model3.json，进入 probe 模式（不需要素材）")

    app = QApplication(sys.argv)
    app.setStyleSheet(DARK_QSS)

    win = DemoWindow(probe=probe, model_json=model_json, size=(w, h))
    win.show()
    if args.pet:
        win._cb_pet.setChecked(True)
    return app.exec()


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except SystemExit:
        raise
    except Exception:
        traceback.print_exc()
        input("\n按回车退出…")
        raise SystemExit(1)

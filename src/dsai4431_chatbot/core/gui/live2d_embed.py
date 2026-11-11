"""把 core/live2d 的渲染页嵌进 PySide6（Qt6）窗口。

这里只做三件事：

1. **本地静态服务**：`ThreadingHTTPServer` 起在 `127.0.0.1:0`，站点根是
   `core/live2d/`（渲染页所在目录），`/vendor/` 与 `/model/` 分别映射到
   `asset/live2d/vendor` 和模型目录。渲染页里的相对引用因此不用改。
   这段逻辑与 `core/live2d/demo_interactive.py` 里的 `_Handler` / `_serve`
   等价，但那支文件是 PyQt5 的（而且禁止改动），所以这里独立实现一份。

2. **Live2DView**：`QWebEngineView` + 就绪探测。渲染页在 `window.l2dReady`
   / `window.l2dError` 上给结论（见 demo_live2d.html 末尾），这里按
   `Stage._check()` 的做法轮询，成功发 `ready`，失败或超时发 `failed`。

3. **画布导出**：取证不依赖窗口截图 —— 走 JS：`l2d.snapshot()` →
   `renderer.extract.base64(stage)` 的 dataURL，Python 侧解码落盘。
   `snapshot(cb)` 就是这个入口。（实测 Qt 6.12 的 `QWidget.grab()` 已经能截到
   WebEngine 内容，但这是实现细节，不能依赖；JS 导出才是稳定的取证方式。）

⚠ QtWebEngine 的环境变量必须在**创建 QApplication 之前**生效，所以模块被
import 时就会调用 `apply_webengine_env()`；`main()` 里再显式调一次（幂等）。
本机实测 Qt6 **仍然需要** `--no-sandbox`（见下），所以默认打开；想自己接管
用 `L2D_KEEP_SANDBOX=1` 关掉。
"""

from __future__ import annotations

import json
import os
import sys
import time
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from threading import Thread
from urllib.parse import quote

# ---------------------------------------------------------------------------
# 环境变量（务必在 QtWebEngine 初始化 / QApplication 之前）
#
# 实测（本机，Qt 6.12 / QtWebEngine 6.140 = Chromium 140）：
#   不加 --no-sandbox → 渲染进程当场 AbnormalTerminationStatus，code=18，
#                       loadFinished 不触发、页面一行 JS 都不执行（与 Qt5 同症状）；
#   加 --no-sandbox   → 正常，load ~0.45s，模型就绪 ~2.3s。
# 所以 Qt6 在这里**仍然需要** --no-sandbox，默认打开。
# 想自己接管就用 L2D_KEEP_SANDBOX=1 关掉，或用 L2D_CHROMIUM_FLAGS 追加别的 flag。
# ---------------------------------------------------------------------------
_KEEP_SANDBOX = os.environ.get("L2D_KEEP_SANDBOX", "").strip().lower() in ("1", "true", "yes", "on")
_NO_SANDBOX = not _KEEP_SANDBOX


def apply_webengine_env() -> None:
    """补齐 QtWebEngine 需要的进程级环境变量。幂等，可重复调用。"""
    if os.environ.get("QTWEBENGINE_CHROMIUM_FLAGS") is None:
        flags: list[str] = []
        if _NO_SANDBOX:
            flags.append("--no-sandbox")
        extra = os.environ.get("L2D_CHROMIUM_FLAGS", "").strip()
        if extra:
            flags.extend(extra.split())
        if flags:
            os.environ["QTWEBENGINE_CHROMIUM_FLAGS"] = " ".join(flags)
    if _NO_SANDBOX:
        os.environ.setdefault("QTWEBENGINE_DISABLE_SANDBOX", "1")


apply_webengine_env()

# 上面这些必须先生效，import QtWebEngine 才有意义
from PySide6.QtCore import QTimer, QUrl, Signal  # noqa: E402
from PySide6.QtGui import QColor, QCursor  # noqa: E402
from PySide6.QtWebEngineCore import (  # noqa: E402
    QWebEnginePage,
    QWebEngineProfile,
    QWebEngineScript,
)
from PySide6.QtWebEngineWidgets import QWebEngineView  # noqa: E402
from PySide6.QtWidgets import (  # noqa: E402
    QApplication,
    QSizePolicy,
    QVBoxLayout,
    QWidget,
)

from dsai4431_chatbot.core.gui import settings_store  # noqa: E402

# ---------------------------------------------------------------------------
# 路径
# ---------------------------------------------------------------------------
_HERE = Path(__file__).resolve().parent
CORE_DIR = _HERE.parent                     # .../core
PAGE_DIR = CORE_DIR / "live2d"              # 渲染页所在目录 = HTTP 站点根
PAGE_LIVE = "demo_live2d.html"

# 取景方式（传给渲染页的 URL 参数）：
#   bust —— 上半身特写：宽度铺满、头顶留白，身高超出部分从下方裁掉
#   full —— 全身适应（旧 demo 的行为）
# 想临时试别的取景不用改代码，设环境变量即可：
#   $env:L2D_FRAMING = "full"     # 退回全身
#   $env:L2D_ZOOM = "1.2"         # 在上半身取景上再放大
FRAMING = os.environ.get("L2D_FRAMING", "bust")
# 1.9 是照着用户给的裁剪参考图定的：头到围裙下沿，两侧手臂自然裁掉。
# 面板越窄，同一个 zoom 看起来越"特写"；想更近就调大。
FRAMING_ZOOM = float(os.environ.get("L2D_ZOOM", "1.9"))
MODEL_PREFIX = "/model/"
VENDOR_PREFIX = "/vendor/"


def _resolve_asset_root() -> Path:
    """资源根目录 `<repo>/asset/live2d`（可被 L2D_ASSET_DIR 覆盖）。

    与 core/live2d/demo_interactive.py 的 `_resolve_asset_root()` 同一套规则，
    保持两边一致：从本文件所在目录逐级向上找。
    """
    env = os.environ.get("L2D_ASSET_DIR")
    if env:
        return Path(env).expanduser().resolve()
    for base in (_HERE, *_HERE.parents):
        cand = base / "asset" / "live2d"
        if cand.is_dir():
            return cand
    return _HERE / "asset" / "live2d"


ASSET_ROOT = _resolve_asset_root()
VENDOR_DIR = ASSET_ROOT / "vendor"
MODELS_DIR = ASSET_ROOT / "models"
CORE_FILE = VENDOR_DIR / "live2dcubismcore.min.js"

_profile_ready = False


def _prepare_profile() -> None:
    """把 QtWebEngine 的 disk cache / local storage 指到 `<repo>/data/webengine`。

    实测（Qt 6.12 这台机器）：`QWebEngineProfile.defaultProfile()` 是
    **off-the-record** 的 —— `httpCacheType` 是 `MemoryHttpCache`，正常运行时
    什么都不落盘（所以 data/webengine 会一直是空的）。这里的路径设置属于
    "双保险"：万一哪天 Qt 改成持久化，也只会写进项目目录，不会跑到用户目录。

    早先的版本确实在 `%LOCALAPPDATA%Low\\python\\cache\\QtWebEngine` 留过 30 多个
    缓存文件（那时缓存路径是默认值），2026-11-11 已清理。

    必须在**创建 QWebEngineView 之前**调用。
    """
    global _profile_ready
    if _profile_ready:
        return
    _profile_ready = True
    try:
        base = settings_store.webengine_dir()
        cache = base / "cache"
        storage = base / "storage"
        cache.mkdir(parents=True, exist_ok=True)
        storage.mkdir(parents=True, exist_ok=True)
        profile = QWebEngineProfile.defaultProfile()
        profile.setCachePath(str(cache))
        profile.setPersistentStoragePath(str(storage))
        profile.setHttpCacheType(QWebEngineProfile.HttpCacheType.DiskHttpCache)
    except Exception as exc:  # noqa: BLE001 - 指不到项目里也不该让角色区起不来
        print(f"[live2d] WebEngine 缓存目录设置失败（用默认位置）：{exc}", flush=True)

# 默认模型：必须是 make_demo_model.py 生成的 .demo. 版本（带动作/表情引用）
DEFAULT_MODEL = MODELS_DIR / "DeepSeek免费公皮" / "DeepSeek" / "大肥鱼.demo.model3.json"


def default_model() -> Path | None:
    """找一个能用的模型文件；找不到返回 None（调用方退回占位文字）。"""
    if DEFAULT_MODEL.is_file():
        return DEFAULT_MODEL
    if MODELS_DIR.is_dir():
        try:
            demos = sorted(MODELS_DIR.rglob("*.demo.model3.json"))
        except OSError:
            demos = []
        if demos:
            return demos[0]
    return None


def list_models() -> list[Path]:
    """models 目录下所有 *.model3.json（给设置页做可选模型列表）。"""
    if not MODELS_DIR.is_dir():
        return []
    try:
        return [p for p in sorted(MODELS_DIR.rglob("*.model3.json")) if p.is_file()]
    except OSError:
        return []


def model_key(path: Path) -> str:
    """模型在 models 目录下的相对路径，用作配置里的稳定标识。"""
    try:
        return path.relative_to(MODELS_DIR).as_posix()
    except ValueError:
        return path.name


def model_label(path: Path) -> str:
    """给人看的名字：保留文件名里的 .demo 后缀（同一模型的两份文件要能区分）。"""
    return path.name.replace(".model3.json", "")


# ---------------------------------------------------------------------------
# 本地静态服务
# ---------------------------------------------------------------------------
class _StaticHandler(SimpleHTTPRequestHandler):
    """站点根 = 渲染页目录；/vendor/、/model/ 改写到 asset 下再交给父类。"""

    def __init__(self, *args, model_dir: str = str(MODELS_DIR), **kwargs):
        self._model_dir = model_dir
        super().__init__(*args, directory=str(PAGE_DIR), **kwargs)

    def log_message(self, *args):  # 静音，别刷屏
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


class LocalPreviewServer:
    """`127.0.0.1:<随机端口>` 的静态服务，后台线程跑，可 shutdown。"""

    def __init__(self, model_json: Path | None = None):
        model_dir = model_json.parent if model_json else MODELS_DIR
        self._server = ThreadingHTTPServer(
            ("127.0.0.1", 0), partial(_StaticHandler, model_dir=str(model_dir))
        )
        self._server.daemon_threads = True
        self._thread = Thread(target=self._server.serve_forever, daemon=True)
        self._thread.start()
        self.port = int(self._server.server_port)

    def url(
        self,
        page: str,
        model_json: Path | None = None,
        *,
        framing: str | None = None,
        zoom: float | None = None,
    ) -> str:
        base = f"http://127.0.0.1:{self.port}/{page}"
        params: list[str] = []
        if model_json is not None:
            params.append(f"m={quote(model_json.name)}")
        if framing:
            params.append(f"framing={quote(str(framing))}")
        if zoom:
            params.append(f"zoom={quote(str(zoom))}")
        return base + ("?" + "&".join(params) if params else "")

    def stop(self) -> None:
        try:
            self._server.shutdown()
            self._server.server_close()
        except Exception:
            pass


# ---------------------------------------------------------------------------
# 页面（收集 console / 崩溃信息，方便出问题时定位）
# ---------------------------------------------------------------------------
# 渲染页自带的调试 HUD（左上角 aim/角度读数）在独立演示里有用，嵌进主界面时
# 不该露出来。渲染页是手工调过的、禁止修改，所以从宿主侧用 CSS 盖掉。
_INJECTED_CSS = """
html, body { background: transparent !important; }
/* 渲染页动态插在 body 末尾的调试 HUD（内联样式里有 Consolas） */
div[style*="Consolas"] { display: none !important; }
"""


class _Page(QWebEnginePage):
    console_message = Signal(int, str, int, str)
    crashed = Signal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.renderProcessTerminated.connect(self._on_terminated)

    def javaScriptConsoleMessage(self, level, message, line, source):  # noqa: N802
        # level 在 Qt6 里是 QWebEnginePage.JavaScriptConsoleMessageLevel 枚举，
        # 直接 int() 会抛 TypeError（踩过），要取 .value。
        try:
            lv = int(level.value) if hasattr(level, "value") else int(level)
        except Exception:
            lv = -1
        self.console_message.emit(lv, str(message), int(line), str(source))

    def _on_terminated(self, status, code):
        self.crashed.emit(f"渲染进程退出：status={status} code={code}")


# ---------------------------------------------------------------------------
# 视图
# ---------------------------------------------------------------------------
JS_SNAPSHOT = """
(function () {
  try {
    if (!window.l2d) return null;
    return window.l2d.snapshot();
  } catch (e) { return 'ERR:' + (e && e.message ? e.message : e); }
})()
"""


class Live2DView(QWidget):
    """一块能渲染 Live2D 的 WebView，带就绪探测和画布导出。

    生命周期：构造 → `start()` 装载 → `ready` / `failed` 二选一。
    失败后调用方应当 `shutdown()` 并把这块控件从布局里摘掉。
    """

    ready = Signal()
    failed = Signal(str)

    def __init__(
        self,
        parent=None,
        *,
        model_json: Path | None = None,
        page: str = PAGE_LIVE,
        poll_ms: int = 120,
        timeout_ms: int = 20_000,
    ):
        super().__init__(parent)
        self._model_json = model_json
        self._page_name = page
        self._timeout_ms = int(timeout_ms)
        self._polls = 0
        self._settled = False
        self._closed = False
        self._load_ok: bool | None = None
        self._load_ms: float | None = None
        self._ready_ms: float | None = None
        self._js_error = ""
        self.console_messages: list[tuple[int, str, int, str]] = []
        self.last_error = ""

        self._lay = QVBoxLayout(self)
        self._lay.setContentsMargins(0, 0, 0, 0)
        self._lay.setSpacing(0)

        # 先把缓存目录指到项目里，再建 view（顺序不能反）
        _prepare_profile()
        self._web = QWebEngineView(self)
        self._page = _Page(self._web)
        self._web.setPage(self._page)
        # 角色区是白色圆角卡片，页面侧 html/body 已注入透明背景，
        # 这里把 Qt 这层的底色也设成透明，模型才浮在卡片上。
        self._page.setBackgroundColor(QColor(0, 0, 0, 0))
        self._page.loadFinished.connect(self._on_load_finished)
        self._page.console_message.connect(self._on_console)
        self._page.crashed.connect(self._on_crashed)

        script = QWebEngineScript()
        script.setName("live2d-host-css")
        script.setInjectionPoint(QWebEngineScript.InjectionPoint.DocumentReady)
        script.setWorldId(QWebEngineScript.ScriptWorldId.MainWorld)
        script.setRunsOnSubFrames(False)
        script.setSourceCode(
            "(function(){var s=document.createElement('style');"
            f"s.textContent={_INJECTED_CSS!r};"
            "document.head.appendChild(s);})();"
        )
        self._page.scripts().insert(script)

        self._web.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self._lay.addWidget(self._web)

        self._poll = QTimer(self)
        self._poll.setInterval(max(50, int(poll_ms)))
        self._poll.timeout.connect(self._check)

        self._deadline = QTimer(self)
        self._deadline.setSingleShot(True)
        self._deadline.timeout.connect(self._on_timeout)

        # 头部跟随鼠标：页面自己只听 mousemove，那**只有鼠标落在角色区里**才动。
        # 页里 setAim() 那段注释写明了正确做法 ——「Qt 那边用轮询喂进来」，
        # 所以这里按和 demo_interactive.py 一样的方式轮询全局光标，跨整个窗口都跟。
        self._aim = (0.0, 0.0)
        self._aim_timer = QTimer(self)
        self._aim_timer.setInterval(60)
        self._aim_timer.timeout.connect(self._poll_aim)
        # 换装表情只套一次（页面重载后重置）
        self._expressions_done = False

    # --- 启动 -------------------------------------------------------------
    def start(self) -> None:
        """起本地服务并装载页面。"""
        app = QApplication.instance()
        if app is not None:
            # 进程退出时一定要关掉后台 HTTP 线程，否则 Qt 可能在析构时卡住
            app.aboutToQuit.connect(self.shutdown)
        if not CORE_FILE.is_file():
            self._fail(f"缺少 Cubism Core：{CORE_FILE}")
            return
        if self._model_json is None:
            self._fail("没有可用的 model3.json")
            return
        self._load()

    def switch_model(self, model_json: Path) -> None:
        """换模型：停掉旧服务、重置就绪探测，重新装载页面（约 2-3 秒）。

        ready 会再发一次，调用方在这里之后补上显示配置即可。
        """
        self._model_json = Path(model_json)
        self._stop_timers()
        if self._server is not None:
            self._server.stop()
            self._server = None
        self._settled = False
        self._polls = 0
        self._js_error = ""
        self._load_ok = None
        self.console_messages.clear()
        self._load()

    def _load(self) -> None:
        try:
            self._server = LocalPreviewServer(self._model_json)
        except OSError as exc:
            self._fail(f"本地静态服务启动失败：{exc}")
            return

        self._t0 = _now_ms()
        url = self._server.url(
            self._page_name,
            self._model_json,
            framing=FRAMING,
            zoom=FRAMING_ZOOM,
        )
        print(f"[live2d] load {url}", file=sys.stderr, flush=True)
        self._expressions_done = False          # 新页面，换装要重新套
        self._web.load(QUrl(url))
        self._poll.start()
        self._deadline.start(self._timeout_ms)
        self._aim_timer.start()

    # --- 计时（性能计数，够用且不依赖 Qt 的时钟） -------------------------
    _t0 = 0.0

    def timing(self) -> dict:
        return {
            "load_finished": self._load_ok,
            "load_ms": self._load_ms,
            "ready_ms": self._ready_ms,
        }

    # --- 页面事件 ---------------------------------------------------------
    def _on_load_finished(self, ok: bool) -> None:
        self._load_ok = bool(ok)
        self._load_ms = _now_ms() - self._t0
        print(
            f"[live2d] loadFinished={ok} 耗时 {self._load_ms:.0f} ms",
            file=sys.stderr,
            flush=True,
        )

    def _on_console(self, level: int, message: str, line: int, source: str) -> None:
        self.console_messages.append((level, message, line, source))
        # 0=INFO 1=WARNING 2=ERROR
        if level >= 1:
            print(f"[live2d][console:{level}] {message}  ({source}:{line})", file=sys.stderr, flush=True)

    def _on_crashed(self, msg: str) -> None:
        self._fail(msg)

    # --- 就绪探测 ---------------------------------------------------------
    def _check(self) -> None:
        if self._settled:
            return
        self._polls += 1

        def cb(result) -> None:
            if self._settled:
                return
            if result is True:
                self._settled = True
                self._stop_timers()
                self._ready_ms = _now_ms() - self._t0
                print(f"[live2d] ready 耗时 {self._ready_ms:.0f} ms", file=sys.stderr, flush=True)
                self.ready.emit()
            elif result:
                self._js_error = str(result)
                self._fail(f"渲染页报错：{result}")

        self._page.runJavaScript(
            "window.l2dReady === true ? true : (window.l2dError || '')", cb
        )

    def _on_timeout(self) -> None:
        if self._settled:
            return
        bits = [f"等待就绪超时（{self._timeout_ms / 1000:.0f}s）"]
        if self._load_ok is False:
            bits.append("loadFinished=false")
        if self._js_error:
            bits.append(self._js_error)
        errs = [m for lvl, m, _l, _s in self.console_messages if lvl >= 2]
        if errs:
            bits.append("console: " + " | ".join(errs[-3:])[:400])
        self._fail("；".join(bits))

    def _fail(self, msg: str) -> None:
        if self._settled:
            return
        self._settled = True
        self.last_error = msg
        self._stop_timers()
        print(f"[live2d] failed: {msg}", file=sys.stderr, flush=True)
        self.failed.emit(msg)

    def _stop_timers(self) -> None:
        """停就绪探测用的计时器。

        ⚠ 这里**不能**停 `_aim_timer`：就绪成功时也会调本方法，一停鼠标跟随就死了
        （2026-11-11 踩过：ready 之后 aim 一直是 0，查了半天是这里被顺手停掉）。
        视线跟随由 shutdown() 单独负责。
        """
        for t in (self._poll, self._deadline):
            try:
                t.stop()
            except Exception:
                pass

    # --- JS 通道 ----------------------------------------------------------
    def js(self, code: str, cb=None) -> None:
        if cb is None:
            self._page.runJavaScript(code)
        else:
            self._page.runJavaScript(code, cb)

    def call(self, method: str, *args, cb=None) -> None:
        payload = ", ".join(_jsv(a) for a in args)
        self.js(f"window.l2d ? l2d.{method}({payload}) : null", cb)

    def snapshot(self, cb) -> None:
        """从页面导出 canvas（Pixi extract → dataURL）。回调收到 str 或 None。"""
        self.js(JS_SNAPSHOT, cb)

    # --- 显示调整（设置页驱动） -------------------------------------------
    def set_scale(self, factor: float) -> None:
        self.call("scale", float(factor))

    def set_offset(self, dx: float, dy: float) -> None:
        self.call("offset", int(dx), int(dy))

    def set_framing(self, mode: str, zoom: float | None = None) -> None:
        self.call("framing", str(mode), zoom)

    def set_physics(self, on: bool) -> None:
        self.call("physics", bool(on))

    def set_blink(self, on: bool) -> None:
        self.call("autoBlink", bool(on))

    def set_breath(self, on: bool) -> None:
        self.call("autoBreath", bool(on))

    def set_follow(self, on: bool) -> None:
        self.call("follow", bool(on))

    def set_expressions(self, names) -> None:
        """套上「换装」表情（如「胸口衣服」「裙子切换」）。

        页面重载后**只套一次**：这套模型有几个表情其实是开关（裙子切换 =
        短裙/长裙来回切），设置页动一下别的项就会再调一次本函数，
        不加这个闸门裙子会一会长一会短。

        ⚠ 必须一次性传进去，不能循环调 expression()：cubism4 的表情管理器
        只有一个 currentExpression 槽位，后一个会把前一个顶掉 —— 之前
        「胸口衣服 + 裙子切换」里只有长裙生效，胸口一直是敞的。
        页面侧 setExpressions() 把这些表情的参数合并后每帧自己写。
        """
        if self._expressions_done:
            return
        self._expressions_done = True
        texts = [str(n).strip() for n in (names or ()) if str(n).strip()]
        self.call("setExpressions", *texts)

    def _poll_aim(self) -> None:
        """把全局光标位置换算成「相对角色区」的归一化坐标，推给页面。

        这样鼠标在聊天区、输入框上移动时头也会转（页面自己只听 mousemove，
        那只有光标落在角色区里才生效）。窗口不在前台时让它看回正中。
        """
        if not self._settled or self._closed:
            return
        cursor = QCursor.pos()
        win = self.window()
        if win is not None and not win.rect().contains(win.mapFromGlobal(cursor)):
            # 光标不在程序窗口里 → 看回正中（别让头一直歪着）
            nx, ny = 0.0, 0.0
        else:
            # 相对**角色区**归一化（和 demo_interactive 一致），再缩到 ±0.75：
            # 鼠标停在角色区边上头转约 ±19°，跑到右边聊天区打字时封顶 22.5°。
            # 不压的话聊天区远在 4 倍宽度外，头会死死钉在 30° 上限上。
            local = self.mapFromGlobal(cursor)
            w = max(1, self.width())
            h = max(1, self.height())
            nx = max(-0.75, min(0.75, ((local.x() / w) * 2 - 1) * 0.75))
            ny = max(-0.75, min(0.75, ((local.y() / h) * 2 - 1) * 0.75))
        ox, oy = self._aim
        # 变化太小就不发，省一次跨进程 JS 调用（和 demo_interactive 一致）
        if abs(nx - ox) < 0.008 and abs(ny - oy) < 0.008:
            return
        self._aim = (nx, ny)
        self.call("setAim", round(nx, 3), round(ny, 3))

    def parts(self, cb) -> None:
        """取部件清单（JSON 字符串回调）。部件 id 来自 moc3，很多模型就是 PartNN。"""
        self.js("window.l2d ? JSON.stringify(l2d.parts()) : '[]'", cb)

    def set_part_hidden(self, index: int, hidden: bool) -> None:
        self.call("setPart", int(index), bool(hidden))

    # --- 收尾 -------------------------------------------------------------
    def shutdown(self) -> None:
        if self._closed:
            return
        self._closed = True
        self._stop_timers()
        try:
            self._aim_timer.stop()        # 视线跟随的轮询，收尾时单独停
        except Exception:
            pass
        srv = getattr(self, "_server", None)
        if srv is not None:
            srv.stop()
            self._server = None
        try:
            self._web.deleteLater()
        except Exception:
            pass


# ---------------------------------------------------------------------------
# 工具
# ---------------------------------------------------------------------------
def _now_ms() -> float:
    return time.perf_counter() * 1000.0


def _jsv(value) -> str:
    if value is None:
        return "null"
    if isinstance(value, bool):
        return "true" if value else "false"
    if isinstance(value, (int, float)):
        return repr(value)
    return json.dumps(str(value), ensure_ascii=False)

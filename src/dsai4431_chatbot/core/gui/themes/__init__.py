"""主题（换肤）系统。

结构：

    gui/themes/
    ├── __init__.py          # ThemeManager + 图标重上色
    ├── light.toml           # 默认浅色
    └── deepseek-blue.toml   # DeepSeek 蓝（深色底）

一套主题 = 一个 toml：`label` / `note` 两个展示字段 + 一张 `[palette]` 表，
键名就是 `theme.py` 模板里的 token。加新皮只要丢一个 toml 进来，不用改代码
（启动时扫描目录）。

两个已知坑，这里都处理了：

1. **图标不会跟着主题变色**。QSS 里 url() 引用的 svg 颜色是写死的，深色皮下
   深色描边等于看不见。所以图标不走 QSS：读 SVG 文本 → 替换颜色 →
   QSvgRenderer 直接渲染成 pixmap（不落临时文件）。用到的按钮要 `bind()` 一下，
   换主题时才会被重新上色。
2. **动态属性变了必须重新 polish**。`setProperty("selected", ...)` 之后要
   `unpolish/polish`，否则 QSS 不重算。见 `restyle()`。
"""

from __future__ import annotations

import tomllib
import weakref
from dataclasses import dataclass
from pathlib import Path

from PySide6.QtCore import QByteArray, QObject, Qt, Signal
from PySide6.QtGui import QColor, QIcon, QPainter, QPalette, QPixmap
from PySide6.QtWidgets import QApplication, QWidget

from dsai4431_chatbot.core.gui import theme as _theme

# 配置的存放位置统一由 settings_store 管（语言模块也要用，放这里会成环）。
# 这三个名字仍然从这里导出，旧代码 `themes.app_settings()` 不用改。
from dsai4431_chatbot.core.gui.settings_store import (  # noqa: F401
    APP,
    ORG,
    app_settings,
    settings_path,
)

try:  # QtSvg 单独一个模块；缺了也不至于整个界面起不来
    from PySide6.QtSvg import QSvgRenderer

    _HAS_SVG = True
except Exception:  # pragma: no cover - 只在 QtSvg 缺失时走到
    QSvgRenderer = None  # type: ignore[assignment]
    _HAS_SVG = False

THEME_DIR = Path(__file__).resolve().parent

SETTINGS_KEY = "theme/id"


# ---------------------------------------------------------------------------
# 数据结构
# ---------------------------------------------------------------------------
@dataclass(frozen=True)
class Theme:
    id: str
    label: str
    note: str
    palette: dict[str, str]
    dark: bool = False

    @property
    def swatches(self) -> list[str]:
        """主题卡上的预览色块：底 / 卡片 / 强调 / 正文。"""
        return [
            self.palette.get("bg", "#000000"),
            self.palette.get("surface", "#000000"),
            self.palette.get("accent", "#000000"),
            self.palette.get("text", "#000000"),
        ]


def load_themes(directory: Path | None = None) -> list[Theme]:
    """扫描目录下所有 *.toml；按 id 排序，light 排最前。"""
    directory = directory or THEME_DIR
    themes: list[Theme] = []
    for path in sorted(directory.glob("*.toml")):
        with path.open("rb") as fh:
            data = tomllib.load(fh)
        tid = str(data.get("id") or path.stem)
        palette = {str(k): str(v) for k, v in dict(data.get("palette", {})).items()}
        themes.append(
            Theme(
                id=tid,
                label=str(data.get("label") or tid),
                note=str(data.get("note") or ""),
                palette=palette,
                dark=bool(data.get("dark", False)),
            )
        )
    if not themes:
        raise RuntimeError(f"没有找到任何主题文件：{directory}")
    themes.sort(key=lambda t: (t.id != "light", t.id))
    return themes


def restyle(widget: QWidget) -> None:
    """动态属性改完必须重刷一次，否则 QSS 不认新值。"""
    style = widget.style()
    style.unpolish(widget)
    style.polish(widget)
    widget.update()


# ---------------------------------------------------------------------------
# 管理器
# ---------------------------------------------------------------------------
class ThemeManager(QObject):
    """读主题、套 QSS、重上色图标、记住选择。"""

    changed = Signal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self._all = load_themes()
        self._by_id = {t.id: t for t in self._all}
        self._current = self._by_id.get("light", self._all[0])
        self._app: QApplication | None = None
        self._bindings: list[tuple[weakref.ref, str, str]] = []
        self._pixmaps: dict[tuple[str, str, str], QPixmap] = {}

    # --- 只读信息 -------------------------------------------------------
    @property
    def available(self) -> list[Theme]:
        return list(self._all)

    @property
    def current(self) -> Theme:
        return self._current

    @property
    def palette(self) -> dict[str, str]:
        return self._current.palette

    def get(self, theme_id: str) -> Theme | None:
        return self._by_id.get(theme_id)

    # --- 应用主题 -------------------------------------------------------
    def apply(
        self,
        app: QApplication | None = None,
        theme_id: str | None = None,
        *,
        persist: bool = True,
    ) -> Theme:
        target = self._by_id.get(theme_id or "") or self._current
        if app is not None:
            self._app = app
        self._current = target
        # 注意：setStyleSheet 是热替换的，Qt 会自己给所有控件重新 polish，
        # 不需要重启，也不用挨个 update()。
        if self._app is not None:
            self._apply_palette()
            self._app.setStyleSheet(_theme.stylesheet(self.palette))
        self._refresh_icons()
        if persist:
            settings = app_settings()
            settings.setValue(SETTINGS_KEY, target.id)
            settings.sync()  # 立刻落盘：进程被直接杀掉时不 sync 会丢
        self.changed.emit(target.id)
        return target

    def apply_saved(self, app: QApplication) -> Theme:
        """启动时按上次的选择应用；没有记录就用 light。"""
        saved = str(app_settings().value(SETTINGS_KEY, "") or "")
        return self.apply(app, saved or None, persist=False)

    def _apply_palette(self) -> None:
        """QSS 管不到的部分（tooltip、原生输入框、选区）也跟着走。"""
        assert self._app is not None
        p = self.palette
        pal = QPalette()
        pairs = (
            (QPalette.ColorRole.Window, "bg"),
            (QPalette.ColorRole.WindowText, "text"),
            (QPalette.ColorRole.Base, "surface_alt"),
            (QPalette.ColorRole.AlternateBase, "surface"),
            (QPalette.ColorRole.Text, "text"),
            (QPalette.ColorRole.Button, "surface"),
            (QPalette.ColorRole.ButtonText, "text"),
            (QPalette.ColorRole.ToolTipBase, "surface"),
            (QPalette.ColorRole.ToolTipText, "text"),
            (QPalette.ColorRole.Highlight, "accent"),
            (QPalette.ColorRole.HighlightedText, "text_on_accent"),
            (QPalette.ColorRole.PlaceholderText, "text_weak"),
            (QPalette.ColorRole.Mid, "border"),
        )
        for role, key in pairs:
            value = p.get(key)
            if value:
                pal.setColor(role, QColor(value))
        self._app.setPalette(pal)

    # --- 图标 -----------------------------------------------------------
    def icon(self, name: str, role: str = "icon") -> QIcon:
        """按当前主题给图标上色。

        role="icon"       —— 正文色描边（深色皮下自动变浅）
        role="on_accent"  —— 强调色底上用的白色图标
        """
        if not _HAS_SVG:
            return QIcon(str(_theme.ICON_DIR / f"{name}.svg"))
        pix = self._render(name, role)
        return QIcon(pix) if not pix.isNull() else QIcon()

    def bind(self, button, name: str, role: str = "icon") -> None:
        """设置图标并记住这个按钮，换主题时一起重上色。"""
        button.setIcon(self.icon(name, role))
        self._bindings.append((weakref.ref(button), name, role))

    def _refresh_icons(self) -> None:
        alive: list[tuple[weakref.ref, str, str]] = []
        for ref, name, role in self._bindings:
            button = ref()
            if button is None:  # 控件已经销毁
                continue
            button.setIcon(self.icon(name, role))
            alive.append((ref, name, role))
        self._bindings = alive

    def _render(self, name: str, role: str) -> QPixmap:
        key = (self._current.id, name, role)
        cached = self._pixmaps.get(key)
        if cached is not None:
            return cached

        path = _theme.ICON_DIR / f"{name}.svg"
        try:
            text = path.read_text(encoding="utf-8")
        except OSError:
            return QPixmap()

        color = self.palette.get(
            "icon" if role == "icon" else "icon_on_accent",
            self.palette.get("text", "#000000"),
        )
        # 图标文件里深色描边随主题走；send/check 那类是画在强调色上的白描边，
        # 只有 on_accent 时才替换。
        text = text.replace("#1f2329", color)
        if role == "on_accent":
            text = text.replace("#ffffff", color)

        renderer = QSvgRenderer(QByteArray(text.encode("utf-8")))
        if not renderer.isValid():
            return QPixmap()

        side = _theme.ICON_SIZE
        dpr = 2.0  # 高分屏下别糊
        pm = QPixmap(int(side * dpr), int(side * dpr))
        pm.fill(Qt.GlobalColor.transparent)
        painter = QPainter(pm)
        try:
            renderer.render(painter)
        finally:
            painter.end()
        pm.setDevicePixelRatio(dpr)

        self._pixmaps[key] = pm
        return pm


# ---------------------------------------------------------------------------
# 单例 + 方便函数
# ---------------------------------------------------------------------------
_manager: ThemeManager | None = None


def manager() -> ThemeManager:
    """全局单例。第一次调用时才建，避免在 QApplication 之前实例化 QObject。"""
    global _manager
    if _manager is None:
        _manager = ThemeManager()
    return _manager


def icon(name: str, role: str = "icon") -> QIcon:
    return manager().icon(name, role)


def bind(button, name: str, role: str = "icon") -> None:
    manager().bind(button, name, role)


def apply(app: QApplication | None = None, theme_id: str | None = None, *, persist: bool = True) -> Theme:
    return manager().apply(app, theme_id, persist=persist)


def apply_saved(app: QApplication) -> Theme:
    return manager().apply_saved(app)

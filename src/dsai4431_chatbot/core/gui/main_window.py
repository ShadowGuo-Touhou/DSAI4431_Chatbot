"""主窗口框架。

布局对照 asset/plan/main interface.png（手绘线框，顺时针旋转 90° 后阅读）：

    ┌──────────────┬─────────────────────────────────────────┐
    │              │  [菜单]                             [设置] │
    │              │  ┌───────────────────────────────────┐  │
    │   Live2D     │  │         消息区（滚动）             │  │
    │   角色区      │  └───────────────────────────────────┘  │
    │  （待接入）    │  ┌───────────────────────────────────┐  │
    │              │  │ 说点什么…                          │  │
    │              │  │ [+]                   [麦克风] [↑] │  │
    │              │  └───────────────────────────────────┘  │
    └──────────────┴─────────────────────────────────────────┘

输入卡这一块模仿 DSH 的做法：输入区和操作行**包在同一张圆角卡片里**，
附件在左、语音和发送在右。

图标说明：DSH 的界面图标是内联 SVG 组件、不是图片素材（它 asar 的 renderer/
里只有欢迎页和更新弹窗两个 SVG，主 bundle 取不到），所以 icons/*.svg 是按同一
视觉语言手绘的等价图标，随时可以换成正式素材。
"""

from __future__ import annotations

import sys
from typing import Literal

from PySide6.QtCore import QSize, Qt, Signal
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import (
    QApplication,
    QFrame,
    QHBoxLayout,
    QLabel,
    QMainWindow,
    QPlainTextEdit,
    QPushButton,
    QScrollArea,
    QSizePolicy,
    QSplitter,
    QVBoxLayout,
    QWidget,
)

from dsai4431_chatbot.core.gui import live2d_embed, theme, themes

ICON_DIR = theme.ICON_DIR


def load_icon(name: str, role: str = "icon") -> QIcon:
    """从 icons/ 读 SVG 并按当前主题上色。

    注意：这样拿到的图标不会自动跟着换肤 —— 要跟主题走的按钮请用
    `round_button()`（内部会 `themes.bind`）。
    """
    return themes.icon(name, role)


def round_button(
    icon: str,
    tooltip: str,
    *,
    primary: bool = False,
    action: bool = False,
) -> QPushButton:
    """统一规格的圆形图标按钮。"""
    btn = QPushButton()
    btn.setProperty("shape", "round")
    if primary:
        btn.setProperty("variant", "primary")
    if action:
        # 注意：动态属性不能叫 "size" —— QWidget 已经有一个 QSize 类型的 size
        # 属性，setProperty("size", "action") 会转换失败并静默丢弃，
        # 导致 QSS 的 [size="action"] 规则永远不生效（踩过）。
        btn.setProperty("kind", "action")

    # 图标走 themes.bind：换肤时会被重新上色（send 是白图标，画在强调色上）
    themes.bind(btn, icon, "on_accent" if primary else "icon")
    btn.setIconSize(QSize(theme.ICON_SIZE, theme.ICON_SIZE))

    side = theme.ACTION_BUTTON if action else theme.ROUND_BUTTON
    btn.setFixedSize(side, side)
    btn.setCursor(Qt.CursorShape.PointingHandCursor)
    btn.setToolTip(tooltip)
    return btn


class CharacterPanel(QWidget):
    """左侧 Live2D 角色区。

    内嵌 core/live2d 的渲染页：QWebEngineView + 本地静态服务（HTTP 与就绪
    探测的实现都在 gui/live2d_embed.py，接口与 core/live2d/demo_interactive.py
    的 Stage 一致）。渲染页就绪后显示模型；页面加载失败或超时要**优雅降级**
    回原来的占位文字，不白屏、不崩溃。
    """

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("characterPanel")
        # 普通 QWidget 子类默认不画 QSS 的 background/border，必须显式打开
        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)
        self.setMinimumWidth(280)

        self._lay = QVBoxLayout(self)
        self._lay.setContentsMargins(16, 16, 16, 16)

        self._hint = QLabel("Live2D 角色区\n（框架占位，待接入渲染页）")
        self._hint.setObjectName("characterHint")
        self._hint.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self._lay.addWidget(self._hint, 1)

        # 只在失败时出现的一行诊断；正常情况隐藏，不改变原有外观
        self._status = QLabel("")
        self._status.setObjectName("characterHint")
        self._status.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self._status.setWordWrap(True)
        self._status.hide()
        self._lay.addWidget(self._status, 0)

        self._view: live2d_embed.Live2DView | None = None
        self._start_embed()

    def _start_embed(self) -> None:
        """有模型就嵌进来；没有模型/素材就安静地保持占位，不报错。"""
        model = live2d_embed.default_model()
        if model is None:
            print("[character] 没有找到 *.demo.model3.json，保持占位", file=sys.stderr, flush=True)
            return

        view = live2d_embed.Live2DView(self, model_json=model)
        view.ready.connect(self._on_live2d_ready)
        view.failed.connect(self._on_live2d_failed)
        self._lay.insertWidget(0, view, 1)
        self._view = view
        view.start()

    def _set_state(self, value: str) -> None:
        """切换 QSS 状态。

        改完动态属性必须 unpolish/polish，否则样式不会重算 —— 这个坑在
        TODO.md 第六节记着。
        """
        self.setProperty("state", value)
        style = self.style()
        style.unpolish(self)
        style.polish(self)

    def _on_live2d_ready(self) -> None:
        self._hint.hide()
        self._status.hide()
        # 模型出来了，去掉占位用的虚线框
        self._set_state("model")

    def _on_live2d_failed(self, msg: str) -> None:
        view, self._view = self._view, None
        if view is not None:
            self._lay.removeWidget(view)
            view.hide()
            view.shutdown()
            view.deleteLater()
        self._hint.show()
        self._status.setText(f"Live2D 未加载：{msg}")
        self._status.show()
        # 退回占位态，虚线框回来
        self._set_state("")

    # --- 对外：给未来的业务调用（对话/情绪驱动角色） ---------------------
    def react(self, name: str) -> bool:
        """透传到渲染页的 window.l2d.react(name)；页面没起来就返回 False。"""
        if self._view is None:
            return False
        self._view.call("react", name)
        return True

    def stop_reaction(self) -> bool:
        if self._view is None:
            return False
        self._view.call("stopReaction")
        return True

    def snapshot(self, callback) -> bool:
        """从页面导出 canvas（dataURL）；没起来返回 False。"""
        if self._view is None:
            return False
        self._view.snapshot(callback)
        return True

    def shutdown(self) -> None:
        if self._view is not None:
            self._view.shutdown()


class MessageArea(QScrollArea):
    """消息区：可滚动的竖向气泡列表。"""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWidgetResizable(True)
        self.setFrameShape(QFrame.Shape.NoFrame)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

        self._body = QWidget()
        self._body.setObjectName("messageViewport")
        self._lay = QVBoxLayout(self._body)
        self._lay.setContentsMargins(4, 4, 4, 4)
        self._lay.setSpacing(10)
        self._lay.addStretch(1)

        self._empty = QLabel("还没有消息")
        self._empty.setObjectName("messageEmpty")
        self._empty.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self._lay.insertWidget(0, self._empty)

        self._has_messages = False
        self.setWidget(self._body)

    def add_message(self, role: Literal["user", "bot"], text: str) -> None:
        """追加一条消息。

        TODO(业务)：接入真实对话后由后端调用；现在只做展示骨架。
        """
        if not self._has_messages:
            self._empty.hide()
            self._has_messages = True

        bubble = QLabel(text)
        bubble.setObjectName("bubbleUser" if role == "user" else "bubbleBot")
        bubble.setWordWrap(True)
        bubble.setTextInteractionFlags(Qt.TextInteractionFlag.TextSelectableByMouse)
        bubble.setSizePolicy(QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Preferred)
        # 气泡最宽占视口的 2/3，长文本自动换行，短文本保持自身宽度
        bubble.setMaximumWidth(max(240, int(self.viewport().width() * 0.66)))

        row = QHBoxLayout()
        row.setContentsMargins(0, 0, 0, 0)
        if role == "user":
            row.addStretch(1)
            row.addWidget(bubble)
        else:
            row.addWidget(bubble)
            row.addStretch(1)

        box = QWidget()
        box.setLayout(row)
        self._lay.insertWidget(self._lay.count() - 1, box)

        bar = self.verticalScrollBar()
        bar.setValue(bar.maximum())

    def clear_messages(self) -> None:
        while self._lay.count() > 2:  # 保留 empty 标签与底部 stretch
            item = self._lay.takeAt(1)
            if item.widget():
                item.widget().deleteLater()
        self._has_messages = False
        self._empty.show()


class _InputEdit(QPlainTextEdit):
    """输入框本体：Enter 发送、Shift+Enter 换行。

    注意：键盘事件必须挂在这个 QPlainTextEdit 子类上 —— 焦点在它身上，
    写在外层 QFrame 的 keyPressEvent 里永远不会被触发。
    """

    submitted = Signal(str)

    def keyPressEvent(self, event):  # noqa: N802 (Qt 命名)
        if event.key() in (Qt.Key.Key_Return, Qt.Key.Key_Enter):
            if event.modifiers() & Qt.KeyboardModifier.ShiftModifier:
                return super().keyPressEvent(event)
            self.submit()
            return None
        return super().keyPressEvent(event)

    def submit(self) -> None:
        text = self.toPlainText().strip()
        if not text:
            return
        self.clear()
        self.submitted.emit(text)


class InputCard(QFrame):
    """输入卡：一张圆角卡片，上输入、下操作行（附件在左，语音/发送在右）。"""

    submitted = Signal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("inputCard")
        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)
        # 竖向只占内容高度，不要把消息区让出的空间全吃掉
        self.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Maximum)

        outer = QVBoxLayout(self)
        outer.setContentsMargins(14, 12, 12, 10)
        outer.setSpacing(6)

        self.edit = _InputEdit()
        self.edit.setObjectName("inputEdit")
        self.edit.setPlaceholderText("说点什么…（Enter 发送，Shift+Enter 换行）")
        self.edit.setFrameShape(QFrame.Shape.NoFrame)
        self.edit.setMinimumHeight(44)
        self.edit.setMaximumHeight(84)  # 最多约三行，再多就内部滚动
        outer.addWidget(self.edit)

        actions = QHBoxLayout()
        actions.setContentsMargins(0, 0, 0, 0)
        actions.setSpacing(8)

        self.btn_attach = round_button("plus", "添加附件（占位）", action=True)
        actions.addWidget(self.btn_attach)

        actions.addStretch(1)

        self.btn_voice = round_button("mic", "语音输入（占位）", action=True)
        actions.addWidget(self.btn_voice)

        self.btn_send = round_button("send", "发送", primary=True, action=True)
        actions.addWidget(self.btn_send)

        outer.addLayout(actions)

        self.edit.submitted.connect(self.submitted)
        self.btn_send.clicked.connect(self.edit.submit)


class ChatColumn(QWidget):
    """右侧聊天列：顶栏 + 消息区 + 输入卡。"""

    settings_requested = Signal()
    menu_requested = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)

        lay = QVBoxLayout(self)
        lay.setContentsMargins(0, 0, 0, 0)
        lay.setSpacing(12)

        # --- 顶栏 -------------------------------------------------------
        header = QHBoxLayout()
        header.setContentsMargins(0, 0, 0, 0)
        header.setSpacing(8)

        self.btn_menu = round_button("menu", "会话列表")
        self.btn_menu.clicked.connect(self.menu_requested.emit)
        header.addWidget(self.btn_menu)

        header.addStretch(1)

        self.btn_settings = round_button("gear", "设置")
        self.btn_settings.clicked.connect(self.settings_requested.emit)
        header.addWidget(self.btn_settings)

        lay.addLayout(header)

        # --- 消息区 -----------------------------------------------------
        self.messages = MessageArea()
        lay.addWidget(self.messages, 1)

        # --- 输入卡 -----------------------------------------------------
        self.input = InputCard()
        lay.addWidget(self.input)

        # 业务接线：输入框回车 → 先回显一条用户消息（真实后端接入后替换）
        self.input.submitted.connect(self._on_submit)

    def _on_submit(self, text: str) -> None:
        self.messages.add_message("user", text)
        # TODO(业务)：把 text 交给对话后端，再把回复 add_message("bot", ...)


class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("DSAI4431 Chatbot")
        self.resize(1440, 900)
        self.setMinimumSize(1100, 700)

        body = QWidget()
        body.setObjectName("windowBody")
        body.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)
        self.setCentralWidget(body)

        root = QHBoxLayout(body)
        root.setContentsMargins(16, 16, 16, 16)
        root.setSpacing(0)

        # 左右两栏用 QSplitter：允许用户拖动比例，也方便调试布局
        splitter = QSplitter(Qt.Orientation.Horizontal)
        splitter.setChildrenCollapsible(False)
        # 两栏之间的留白。注意别指望 QSS 的 QSplitter::handle{width}：
        # 实测不生效（handle 宽度会是 0，两栏贴死），只能在这里设。
        splitter.setHandleWidth(theme.SPLITTER_GAP)

        self.character = CharacterPanel()
        self.chat = ChatColumn()
        splitter.addWidget(self.character)
        splitter.addWidget(self.chat)
        splitter.setStretchFactor(0, 3)
        splitter.setStretchFactor(1, 7)
        splitter.setSizes([420, 1020])

        root.addWidget(splitter)

        self.chat.settings_requested.connect(self.open_settings)

    # --- 设置 -----------------------------------------------------------
    def open_settings(self) -> None:
        """打开设置窗口。

        目前只渲染布局，没有业务逻辑。分页与字段见 settings_dialog.py。
        """
        # 延迟导入：settings_dialog 反过来要用本模块的 ICON_DIR / load_icon
        from dsai4431_chatbot.core.gui.settings_dialog import SettingsDialog

        dlg = SettingsDialog(self)
        dlg.exec()


def main(argv: list[str] | None = None) -> int:
    """启动主界面。"""
    # Qt6 默认开启 HiDPI 缩放，AA_EnableHighDpiScaling / AA_UseHighDpiPixmaps
    # 已废弃（setAttribute 会告警甚至无效），这里不再设置。
    # AA_ShareOpenGLContexts 保留：嵌了 QWebEngineView，必须在 QApplication
    # 之前打开，否则 WebEngine 起不来（见 core/live2d 的踩坑记录）。
    QApplication.setAttribute(
        Qt.ApplicationAttribute.AA_ShareOpenGLContexts, True
    )

    # QtWebEngine 的环境变量也必须在 QApplication 之前落地。
    # live2d_embed 被 import 时已经设过一次，这里再显式调一次（幂等），
    # 让"必须在 QApplication 之前"这件事在入口处也看得见。
    live2d_embed.apply_webengine_env()

    app = QApplication(sys.argv if argv is None else argv)
    app.setApplicationName("DSAI4431 Chatbot")
    # 换肤：启动时按上次的选择套 QSS（没有记录就是 light）
    themes.apply_saved(app)

    win = MainWindow()
    win.show()
    return app.exec()


if __name__ == "__main__":
    raise SystemExit(main())

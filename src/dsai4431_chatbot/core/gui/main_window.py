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
from pathlib import Path
from typing import Literal

from PySide6.QtCore import QPoint, QSize, Qt, Signal
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import (
    QApplication,
    QComboBox,
    QFrame,
    QHBoxLayout,
    QLabel,
    QMainWindow,
    QPlainTextEdit,
    QPushButton,
    QScrollArea,
    QSizePolicy,
    QSplitter,
    QStackedWidget,
    QVBoxLayout,
    QWidget,
)

from dsai4431_chatbot.core.gui import (
    chat_client,
    chat_config,
    i18n,
    live2d_config,
    live2d_embed,
    personas,
    session_store,
    theme,
    themes,
)
from dsai4431_chatbot.core.gui.i18n import t
from dsai4431_chatbot.core.gui.session_drawer import DRAWER_W, SessionDrawer

ICON_DIR = theme.ICON_DIR
# 发给模型的历史上限（条）。太多会拖 token、太短又记不住上下文。
MAX_HISTORY_MESSAGES = 20

# 新对话页两颗下拉的「文字之外的宽度」：QSS 的左右内边距 + 箭头区 + 描边，
# 人格那颗还要加上前面的 16px 图标和图标间距。
# ⚠ 改 theme.py 里 #homePersona / #homeModel 的 padding / drop-down 宽度时要一起改。
PERSONA_CHROME = 12 + 4 + 20 + 2 + 16 + 6
MODEL_CHROME = 8 + 4 + 20 + 2


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

    # 每次（重新）就绪时发一次：换模型后设置页要重新拉部件清单
    live2d_ready = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("characterPanel")        # 普通 QWidget 子类默认不画 QSS 的 background/border，必须显式打开
        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)
        self.setMinimumWidth(280)

        self._lay = QVBoxLayout(self)
        self._lay.setContentsMargins(16, 16, 16, 16)

        self._hint = QLabel(t("main.character.placeholder"))
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
        # 显示配置（换模型/缩放/偏移/取景/行为开关/隐藏部件），存在 settings.ini
        self._cfg = live2d_config.load()
        self._start_embed(self._cfg.model_path())

    def _start_embed(self, model: "Path | None" = None) -> None:
        """有模型就嵌进来；没有模型/素材就安静地保持占位，不报错。"""
        model = model or live2d_embed.default_model()
        if model is None:
            print("[character] 没有找到 *.model3.json，保持占位", file=sys.stderr, flush=True)
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
        self._apply_display_config()
        self.live2d_ready.emit()

    def _apply_display_config(self) -> None:
        """把配置套到刚就绪的页面上（顺序有讲究：先取景，再偏移，最后缩放）。"""
        view = self._view
        if view is None:
            return
        cfg = self._cfg
        view.set_framing(cfg.framing)
        view.set_offset(cfg.offset_x, cfg.offset_y)
        view.set_scale(cfg.scale)
        view.set_physics(cfg.physics)
        view.set_blink(cfg.blink)
        view.set_breath(cfg.breath)
        view.set_follow(cfg.follow)
        # 换装（这套模型把换装做成表情名，默认「胸口衣服 + 裙子切换」）
        view.set_expressions(cfg.expressions)
        if cfg.hidden_parts:
            view.parts(self._apply_hidden_parts)

    def _apply_hidden_parts(self, payload) -> None:
        """页面回传部件清单后，把配置里勾了隐藏的部件藏回去。"""
        import json

        if self._view is None or not payload:
            return
        try:
            parts = json.loads(payload)
        except (TypeError, ValueError):
            return
        wanted = set(self._cfg.hidden_parts)
        for part in parts:
            if part.get("id") in wanted and not part.get("hidden"):
                self._view.set_part_hidden(part["index"], True)

    # --- 设置页（Live2D model）驱动的接口 --------------------------------
    @property
    def config(self):
        return self._cfg

    def current_model(self) -> Path | None:
        return self._cfg.model_path()

    def set_model(self, path: Path) -> None:
        """换模型。部件 id 是每个 moc3 自己的，所以隐藏记录一起清掉。"""
        self._cfg.model = live2d_embed.model_key(Path(path))
        self._cfg.hidden_parts = []
        live2d_config.save(self._cfg)
        if self._view is None:
            self._start_embed(Path(path))
        else:
            self._view.switch_model(Path(path))

    def set_framing(self, mode: str) -> None:
        self._cfg.framing = "full" if mode == "full" else "bust"
        live2d_config.save(self._cfg)
        if self._view is not None:
            self._view.set_framing(self._cfg.framing)

    def set_scale(self, factor: float) -> None:
        self._cfg.scale = float(factor)
        live2d_config.save(self._cfg)
        if self._view is not None:
            self._view.set_scale(self._cfg.scale)

    def set_offset(self, dx: int, dy: int) -> None:
        self._cfg.offset_x = int(dx)
        self._cfg.offset_y = int(dy)
        live2d_config.save(self._cfg)
        if self._view is not None:
            self._view.set_offset(self._cfg.offset_x, self._cfg.offset_y)

    def set_behavior(self, name: str, on: bool) -> None:
        setattr(self._cfg, name, bool(on))
        live2d_config.save(self._cfg)
        if self._view is None:
            return
        {
            "physics": self._view.set_physics,
            "blink": self._view.set_blink,
            "breath": self._view.set_breath,
            "follow": self._view.set_follow,
        }[name](bool(on))

    def request_parts(self, callback) -> bool:
        if self._view is None:
            return False
        self._view.parts(callback)
        return True

    def set_part_hidden(self, index: int, part_id: str, hidden: bool) -> None:
        ids = set(self._cfg.hidden_parts)
        if hidden:
            ids.add(part_id)
        else:
            ids.discard(part_id)
        self._cfg.hidden_parts = sorted(ids)
        live2d_config.save(self._cfg)
        if self._view is not None:
            self._view.set_part_hidden(index, hidden)

    def _on_live2d_failed(self, msg: str) -> None:
        view, self._view = self._view, None
        if view is not None:
            self._lay.removeWidget(view)
            view.hide()
            view.shutdown()
            view.deleteLater()
        self._hint.show()
        self._status.setText(t("main.character.error", msg=msg))
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

        self._empty = QLabel(t("main.messages.empty"))
        self._empty.setObjectName("messageEmpty")
        self._empty.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self._lay.insertWidget(0, self._empty)

        self._has_messages = False
        self.setWidget(self._body)

    def add_message(self, role: Literal["user", "bot"], text: str) -> QLabel:
        """追加一条完整消息，返回气泡（流式回复也可以先用它占位）。"""
        bubble = self.begin_message(role)
        bubble.setText(text)
        self.scroll_to_end()
        return bubble

    # 角色 → QSS 里用的 objectName
    ROLE_NAMES = {"user": "bubbleUser", "bot": "bubbleBot", "reasoning": "bubbleReasoning"}

    def begin_message(
        self, role: Literal["user", "bot", "reasoning"], before: QWidget | None = None
    ) -> QLabel:
        """先建一个空气泡，等流式内容一点点填进来。

        `before` 给「思考链气泡要插在回答气泡上面」用。
        """
        if not self._has_messages:
            self._empty.hide()
            self._has_messages = True

        bubble = QLabel("")
        bubble.setObjectName(self.ROLE_NAMES.get(role, "bubbleBot"))
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
        index = self._lay.count() - 1
        if before is not None:
            found = self._lay.indexOf(before)
            if found >= 0:
                index = found
        self._lay.insertWidget(index, box)
        self.scroll_to_end()
        return bubble

    def scroll_to_end(self) -> None:
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
    # 由外层注入：返回 False 时 Enter 不发也不清空（等回复时用）
    can_submit = None

    # 占位符文案 / 是否因为正在组字而临时藏起来了
    _ph_text = ""
    _ph_hidden = False

    def setPlaceholderText(self, text: str) -> None:  # noqa: N802 (Qt 命名)
        self._ph_text = text
        super().setPlaceholderText("" if self._ph_hidden else text)

    def inputMethodEvent(self, event) -> None:  # noqa: N802 (Qt 命名)
        """中文输入法组字时把占位符藏起来。

        IME 的预编辑串（拼音 "da"）**不进 document**，Qt 只按 document 是否
        为空决定画不画 placeholder，于是占位符会和拼音叠在同一行
        （截图里那个「da点什么…」）。这里按 preeditString 是否为空来切。
        """
        super().inputMethodEvent(event)
        composing = bool(event.preeditString())
        if composing == self._ph_hidden:
            return
        self._ph_hidden = composing
        super().setPlaceholderText("" if composing else self._ph_text)

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
        # 外层（ChatColumn）会在等回复时把 can_submit 设成 False：
        # 这时候不发、也**不清空**输入框，用户敲的字不会丢
        if self.can_submit is not None and not self.can_submit():
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
        self.edit.setPlaceholderText(t("main.input.placeholder"))
        self.edit.setFrameShape(QFrame.Shape.NoFrame)
        self.edit.setMinimumHeight(44)
        self.edit.setMaximumHeight(84)  # 最多约三行，再多就内部滚动
        outer.addWidget(self.edit)

        actions = QHBoxLayout()
        actions.setContentsMargins(0, 0, 0, 0)
        actions.setSpacing(8)

        self.btn_attach = round_button("plus", t("main.button.attach"), action=True)
        actions.addWidget(self.btn_attach)

        actions.addStretch(1)

        self.btn_voice = round_button("mic", t("main.button.voice"), action=True)
        actions.addWidget(self.btn_voice)

        self.btn_send = round_button(
            "send", t("main.button.send"), primary=True, action=True
        )
        actions.addWidget(self.btn_send)

        outer.addLayout(actions)

        self.edit.submitted.connect(self.submitted)
        self.btn_send.clicked.connect(self.edit.submit)


class _HomeCombo(QComboBox):
    """新对话页的选择器：**盒子**宽度贴着当前项，**弹窗**宽度贴着最长项。

    为什么不能直接用 QComboBox：
    - 它默认按最长的一项算盒子宽度 —— 选中短名字时右边留一截空白，箭头离文字老远
    - 而弹窗宽度又跟着盒子走 —— 盒子收窄之后，长选项被省略成「deeps...soner」

    所以盒子这边自己算宽度（见 HomePage._fit_combo），弹窗那边在 showPopup()
    里先把列表的最小宽度撑到最长项。
    """

    def showPopup(self) -> None:  # noqa: N802 - Qt 命名
        view = self.view()
        # sizeHintForColumn 已经把「列表项内边距 + 图标」算进去了；再加 14 给
        # 列表框自己的 padding/border 和取整余量 —— 少 1px 就会省略成「deeps…soner」
        view.setMinimumWidth(view.sizeHintForColumn(0) + 14)
        super().showPopup()


class HomePage(QWidget):
    """新对话页：「新建对话」后右侧聊天列里整块换成的空白首页。

    布局（对照 DSH 的首页）：

        ┌──────────────────────────────────────┐
        │                                      │
        │             开始新的对话              │  ← 大标题
        │  [赤蛮奇 ▾]                          │  ← 人格
        │  ┌────────────────────────────────┐  │
        │  │ 说点什么开始…                   │  │  ← 大输入框
        │  │ [+]      [deepseek-chat ▾] [↑] │  │
        │  └────────────────────────────────┘  │
        └──────────────────────────────────────┘

    为什么这个类写在 main_window.py 里而不是单独一个模块：它要用上面的
    `_InputEdit`（Enter 发送）和 `round_button`，单独成模块会与本模块循环
    导入（本模块必须先拿到 HomePage 才能装进 ChatColumn）。
    """

    # 输入框宽度上限：和 DSH 一样收窄居中的一列，太宽了输入框会失去焦点感
    COLUMN_W = 760
    submitted = Signal(dict)      # {"persona": dict, "model": str, "text": str}

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("homePage")

        outer = QVBoxLayout(self)
        outer.setContentsMargins(0, 0, 0, 0)
        outer.setSpacing(0)
        # 上下留白按 3:5 分：整块内容略高于正中，看起来不像飘在中间
        outer.addStretch(3)

        column = QWidget()
        column.setMaximumWidth(self.COLUMN_W)
        col = QVBoxLayout(column)
        col.setContentsMargins(0, 0, 0, 0)
        col.setSpacing(12)

        self.lb_title = QLabel(t("main.home.title"))
        self.lb_title.setObjectName("homeTitle")
        self.lb_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        col.addWidget(self.lb_title)
        col.addSpacing(14)

        # --- 人格（首页上方，左对齐的一颗胶囊）----------------------------
        self.cbo_persona = _HomeCombo()
        self.cbo_persona.setObjectName("homePersona")
        self.cbo_persona.setToolTip(t("session.persona"))
        # 图标用设置页 Personality 那颗（icons/user.svg），跟着换肤重新上色
        self.cbo_persona.setIconSize(QSize(16, 16))
        self.cbo_persona.setFixedHeight(36)
        # 宽度在 refresh()/切项时自己算（见 _fit_combo）：默认按最长项算会把
        # 右边撑开，箭头离文字很远
        self.cbo_persona.setSizePolicy(
            QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed
        )
        col.addWidget(self.cbo_persona, 0, Qt.AlignmentFlag.AlignLeft)

        # --- 大输入卡（模型选择器 + 发送放在卡片右下角）--------------------
        card = QFrame()
        card.setObjectName("homeCard")
        card.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)
        card.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Maximum)
        self.card = card
        inner = QVBoxLayout(card)
        inner.setContentsMargins(16, 14, 14, 12)
        inner.setSpacing(8)

        self.edit = _InputEdit()
        self.edit.setObjectName("homeEdit")
        self.edit.setPlaceholderText(t("main.home.placeholder"))
        self.edit.setFrameShape(QFrame.Shape.NoFrame)
        self.edit.setMinimumHeight(92)
        self.edit.setMaximumHeight(200)
        inner.addWidget(self.edit)

        actions = QHBoxLayout()
        actions.setContentsMargins(0, 0, 0, 0)
        actions.setSpacing(8)

        self.btn_attach = round_button("plus", t("main.button.attach"), action=True)
        actions.addWidget(self.btn_attach)
        actions.addStretch(1)

        # 模型：输入卡右下角的一行小字（无边框，悬停才浮出底色）
        self.cbo_model = _HomeCombo()
        self.cbo_model.setObjectName("homeModel")
        self.cbo_model.setToolTip(t("session.model"))
        self.cbo_model.setFixedHeight(28)
        # 同上：宽度自己算，箭头紧贴模型名
        self.cbo_model.setSizePolicy(
            QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed
        )
        actions.addWidget(self.cbo_model)

        self.btn_send = round_button(
            "send", t("main.button.send"), primary=True, action=True
        )
        actions.addWidget(self.btn_send)

        inner.addLayout(actions)
        col.addWidget(card)

        row = QHBoxLayout()
        row.setContentsMargins(0, 0, 0, 0)
        row.addStretch(1)
        row.addWidget(column, 20)      # 撑到 COLUMN_W 为止，剩下的给两侧的 stretch
        row.addStretch(1)
        outer.addLayout(row)
        outer.addStretch(5)

        self.edit.submitted.connect(self._emit)
        self.btn_send.clicked.connect(self.edit.submit)
        # 换一项就重新收一次宽度（不然换了长/短名字，箭头位置会飘）
        self.cbo_persona.currentIndexChanged.connect(self._fit_combos)
        self.cbo_model.currentIndexChanged.connect(self._fit_combos)

    # --- 数据 -----------------------------------------------------------
    def refresh(self) -> None:
        """每次显示时重读人格/模型清单（设置里刚改过 personas.json 也能反映）。

        尽量保住上次选的项：找不到就退回第一项 / 设置里的默认模型。
        """
        cfg = chat_config.load()

        keep_persona = self.cbo_persona.currentData()
        self.cbo_persona.clear()
        # 图标和设置页 Personality 用同一颗（icons/user.svg）。
        # 这里每次刷新都重新取：换主题后图标的颜色要跟着换。
        persona_icon = themes.icon("user")
        for persona in personas.list_personas():
            self.cbo_persona.addItem(persona_icon, persona.display, persona.id)
        if keep_persona:
            index = self.cbo_persona.findData(keep_persona)
            if index >= 0:
                self.cbo_persona.setCurrentIndex(index)

        keep_model = self.cbo_model.currentData() or cfg.model
        self.cbo_model.clear()
        for model in personas.model_options(cfg.model):
            self.cbo_model.addItem(model, model)
        index = self.cbo_model.findData(keep_model)
        if index >= 0:
            self.cbo_model.setCurrentIndex(index)
        self._fit_combos()

    @staticmethod
    def _fit_combo(combo: QComboBox, chrome: int) -> None:
        """把宽度收到「当前这一项」的宽度（而不是最长的那一项）。

        QComboBox 默认按最长项算宽度，选中短名字时右边会留一截空白，
        箭头离文字老远 —— DSH 里箭头是紧贴文字/图标的，所以自己算。

        `chrome` = 左右内边距 + 箭头区 + 描边（各控件的 QSS 里定），
        人格那颗还要加上前面 16px 的图标和图标间距。
        """
        text_w = combo.fontMetrics().horizontalAdvance(combo.currentText())
        combo.setFixedWidth(max(96, min(280, text_w + chrome)))

    def _fit_combos(self) -> None:
        self._fit_combo(self.cbo_persona, PERSONA_CHROME)
        self._fit_combo(self.cbo_model, MODEL_CHROME)

    def focus_input(self) -> None:
        self.edit.setFocus()

    def selection(self) -> dict:
        """当前选中的人格与模型（给测试和 _emit 共用）。"""
        persona_id = self.cbo_persona.currentData()
        persona = personas.by_id(persona_id) if persona_id else None
        model = self.cbo_model.currentData() or self.cbo_model.currentText()
        return {
            "persona": persona.as_dict() if persona else {},
            "model": str(model),
        }

    def _emit(self, text: str) -> None:
        payload = self.selection()
        payload["text"] = text
        self.submitted.emit(payload)


class ChatColumn(QWidget):
    """右侧聊天列：顶栏 + （对话页 | 新对话页）+ 会话后端。"""

    settings_requested = Signal()
    menu_requested = Signal()
    # 会话内容变了（新建 / 首条消息自动建 / 追加消息）→ 让外层刷新会话列表
    session_updated = Signal(str)

    def __init__(self, parent=None):
        super().__init__(parent)

        lay = QVBoxLayout(self)
        lay.setContentsMargins(0, 0, 0, 0)
        lay.setSpacing(12)

        # --- 顶栏 -------------------------------------------------------
        header = QHBoxLayout()
        header.setContentsMargins(0, 0, 0, 0)
        header.setSpacing(8)

        self.btn_menu = round_button("menu", t("main.button.menu"))
        self.btn_menu.clicked.connect(self.menu_requested.emit)
        header.addWidget(self.btn_menu)

        header.addStretch(1)

        self.btn_settings = round_button("gear", t("main.button.settings"))
        self.btn_settings.clicked.connect(self.settings_requested.emit)
        header.addWidget(self.btn_settings)

        lay.addLayout(header)

        # --- 两种页面：对话页 / 新对话页 ---------------------------------
        self.stack = QStackedWidget()
        self.stack.setObjectName("chatStack")
        lay.addWidget(self.stack, 1)

        page_chat = QWidget()
        page_lay = QVBoxLayout(page_chat)
        page_lay.setContentsMargins(0, 0, 0, 0)
        page_lay.setSpacing(12)

        self.messages = MessageArea()
        page_lay.addWidget(self.messages, 1)

        self.input = InputCard()
        page_lay.addWidget(self.input)

        self.page_chat = page_chat
        self.home = HomePage()
        self.stack.addWidget(page_chat)      # 0：看历史 / 继续对话
        self.stack.addWidget(self.home)      # 1：新对话页
        self.home.submitted.connect(self._on_home_submit)

        # --- 对话后端 ---------------------------------------------------
        self.client = chat_client.ChatClient(self)
        self.client.delta.connect(self._on_delta)
        self.client.reasoning_delta.connect(self._on_reasoning_delta)
        self.client.finished_ok.connect(self._on_reply_done)
        self.client.failed.connect(self._on_reply_failed)

        self._history: list[dict] = []   # OpenAI 格式：{"role": ..., "content": ...}
        self._bubble: QLabel | None = None   # 正在流式写入的那个气泡
        self._bubble_fresh = True            # 还没写过内容（要替换占位文字）
        self._reasoning_text = ""            # 本轮思考链全文（reasoner 才有）
        self._reasoning_bubble: QLabel | None = None
        # 当前会话（data/session 里的一条）；没建会话就直接发消息时自动建一条
        self._session_id = ""
        self._session: session_store.SessionMeta | None = None
        # 新对话页上选好的人格 / 模型：等第一句话发出去、真要建会话时才用
        self._pending_persona: dict | None = None
        self._pending_model = ""

        # 等回复时按 Enter 不发也不清空输入框
        self.input.edit.can_submit = lambda: not self.client.busy()
        self.input.submitted.connect(self._on_submit)

    # --- 发消息 ---------------------------------------------------------
    def _on_submit(self, text: str) -> None:
        # 每次都现读配置：设置页里刚填的 Key / 刚改的模型立刻生效
        cfg = chat_config.load()
        self.messages.add_message("user", text)

        ok, _reason = cfg.ready()
        if not ok:
            self.messages.add_message("bot", t("main.messages.no_key"))
            return

        # 没建会话就直接发消息：自动建一条（用第一个人格 + 当前模型）
        session = self._ensure_session(cfg)
        session_store.append_user_message(session.id, text)
        self.session_updated.emit(session.id)

        self._history.append({"role": "user", "content": text})
        self._bubble = self.messages.begin_message("bot")
        self._bubble.setText(t("main.messages.thinking"))
        self._bubble_fresh = True
        self._reasoning_text = ""
        self._reasoning_bubble = None

        model = session.model or cfg.model
        if not self.client.send(cfg, self._payload(cfg), model=model):
            self._finish_bubble(t("main.messages.failed", msg="请求没能发出去"))

    def _payload(self, cfg) -> list[dict]:
        """人格文件 → system 消息；再加最近若干轮对话。"""
        messages: list[dict] = []
        system = self._system_prompt(cfg)
        if system:
            messages.append({"role": "system", "content": system})
        messages.extend(self._history[-MAX_HISTORY_MESSAGES:])
        return messages

    def _system_prompt(self, cfg) -> str:
        """会话里记着用哪个人格；没有就退回设置页那份。"""
        session = self._session
        if session is not None and session.persona:
            prompt = personas.build_system_prompt(
                str(session.persona.get("dir") or ""),
                [str(name) for name in (session.persona.get("files") or [])],
            )
            if prompt:
                return prompt
        return cfg.system_prompt()

    # --- 会话 -----------------------------------------------------------
    @property
    def current_session_id(self) -> str:
        return self._session_id

    def _ensure_session(self, cfg) -> session_store.SessionMeta:
        if self._session is not None:
            return self._session
        # 新对话页上选过就按选的来；没选（比如直接在对话页敲字）就退回第一个人格
        persona_dict = self._pending_persona
        if not persona_dict:
            choices = personas.list_personas()
            persona_dict = choices[0].as_dict() if choices else {}
        meta = session_store.create_session(
            persona=persona_dict,
            model=self._pending_model or cfg.model or personas.MODELS[0],
        )
        self._pending_persona = None
        self._pending_model = ""
        self._session = meta
        self._session_id = meta.id
        self.session_updated.emit(meta.id)
        return meta

    # --- 两种页面 -------------------------------------------------------
    def show_home(self) -> None:
        """切到新对话页（首页）。"""
        self.home.refresh()
        self.stack.setCurrentWidget(self.home)
        self.home.focus_input()

    def show_conversation(self) -> None:
        """切到对话页（消息 + 输入卡）。"""
        self.stack.setCurrentWidget(self.page_chat)

    def start_new_conversation(self) -> None:
        """「新建对话」：把当前状态清干净，回到空白首页。

        注意这里**不建会话**：空会话文件没有意义，等第一句话发出去时
        `_ensure_session()` 才真正落盘（和以前「直接敲字自动建」是同一条路径）。
        """
        self.client.abort()
        self._bubble = None
        self._reasoning_bubble = None
        self._reasoning_text = ""
        self._history.clear()
        self._session = None
        self._session_id = ""
        self._pending_persona = None
        self._pending_model = ""
        self.messages.clear_messages()
        self.input.edit.clear()
        self.show_home()

    def _on_home_submit(self, payload: dict) -> None:
        """首页里敲下第一句话：带上选好的人格/模型，切到对话页按常规发出去。"""
        self._pending_persona = payload.get("persona") or None
        self._pending_model = str(payload.get("model") or "")
        self.show_conversation()
        self._on_submit(str(payload.get("text") or ""))
        self.input.edit.setFocus()

    def open_session(self, session_id: str) -> None:
        """切到某个会话：读回历史消息，重建上下文。"""
        self.client.abort()
        self._bubble = None
        self._session_id = session_id
        self._session = session_store.get_meta(session_id)
        self._pending_persona = None
        self._pending_model = ""
        self.messages.clear_messages()
        self._history.clear()
        self._reasoning_bubble = None
        self._reasoning_text = ""
        show_reasoning = chat_config.load().show_reasoning
        for row in session_store.load_messages(session_id):
            if row["role"] == "bot" and row["reasoning"] and show_reasoning:
                thought = self.messages.begin_message("reasoning")
                thought.setText(row["reasoning"])
            bubble = self.messages.begin_message(row["role"])
            bubble.setText(row["text"] or t("main.messages.empty_reply"))
            self._history.append(
                {
                    "role": "user" if row["role"] == "user" else "assistant",
                    "content": row["text"],
                }
            )
        self.messages.scroll_to_end()
        self.show_conversation()

    # --- 流式回填 -------------------------------------------------------
    def _on_reasoning_delta(self, piece: str) -> None:
        """思考链：**总是收**（要存进会话），只有开关打开才往界面上画。"""
        self._reasoning_text += piece
        if not chat_config.load().show_reasoning:
            return
        if self._reasoning_bubble is None:
            before = self._bubble.parentWidget() if self._bubble is not None else None
            self._reasoning_bubble = self.messages.begin_message("reasoning", before=before)
            self._reasoning_bubble.setText(piece)
        else:
            self._reasoning_bubble.setText(self._reasoning_bubble.text() + piece)
        self.messages.scroll_to_end()

    def _on_delta(self, piece: str) -> None:
        if self._bubble is None:
            return
        if self._bubble_fresh:
            self._bubble.setText(piece)
            self._bubble_fresh = False
        else:
            self._bubble.setText(self._bubble.text() + piece)
        self.messages.scroll_to_end()

    def _on_reply_done(self, full: str) -> None:
        self._finish_bubble(full or t("main.messages.empty_reply"))
        self._history.append({"role": "assistant", "content": full})
        if self._session is not None:
            session_store.append_assistant_message(
                self._session.id,
                full,
                reasoning=self._reasoning_text or self.client.last_reasoning(),
                usage=self.client.last_usage(),
            )
            self.session_updated.emit(self._session.id)
        self._reasoning_bubble = None

    def _on_reply_failed(self, reason: str) -> None:
        # 已经收到的部分保留（chat_client 会把它当成功发出来），这里只处理空回复
        self._finish_bubble(t("main.messages.failed", msg=reason))

    def _finish_bubble(self, text: str) -> None:
        if self._bubble is not None:
            self._bubble.setText(text)
            self._bubble = None
        self.messages.scroll_to_end()

    # --- 新对话 ---------------------------------------------------------
    def reset_conversation(self) -> None:
        """旧名字，保留给「删掉的正好是当前会话」那一处：清空并回到首页。"""
        self.start_new_conversation()


class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle(t("app.title"))
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
        self._settings = None

        # 会话抽屉（≡ 打开）：叠在窗口左侧，不占 splitter
        self._drawer = SessionDrawer(self)
        self._drawer.hide()
        self._drawer.new_session_requested.connect(self._on_new_session_requested)
        self._drawer.session_opened.connect(self._on_session_switch)
        self._drawer.session_deleted.connect(self._on_session_deleted)
        self._drawer.close_requested.connect(self.hide_drawer)
        self.chat.menu_requested.connect(self.toggle_drawer)
        self.chat.session_updated.connect(self._on_session_updated)

        # 退出前把 WebEngine 收掉（嵌入式 HTTP 服务 + 渲染进程）。
        # aboutToQuit 管"换语言自动重启"（app.quit() 不触发 closeEvent），
        # closeEvent 管用户直接关窗口，两个入口都收一遍；shutdown 是幂等的。
        app = QApplication.instance()
        if app is not None:
            app.aboutToQuit.connect(self._on_about_to_quit)

        # 一打开就把上一次的对话接上（没有对话 → 停在空白首页）
        self._restore_last_session()

    def _on_about_to_quit(self) -> None:
        self.character.shutdown()

    # --- 会话抽屉 -------------------------------------------------------
    def _place_drawer(self) -> None:
        """抽屉是独立窗口（见 SessionDrawer 里的说明），按主窗口左上角算全局坐标。"""
        margin = 12
        top_left = self.mapToGlobal(QPoint(margin, margin))
        self._drawer.move(top_left)
        self._drawer.resize(DRAWER_W, max(260, self.height() - margin * 2))

    def show_drawer(self) -> None:
        self._drawer.reload()
        self._place_drawer()
        self._drawer.show()
        self._drawer.raise_()

    def hide_drawer(self) -> None:
        self._drawer.hide()

    def toggle_drawer(self) -> None:
        if self._drawer.isVisible():
            self.hide_drawer()
        else:
            self.show_drawer()

    def _on_session_switch(self, session_id: str) -> None:
        """新建或选中会话：把它读进右边聊天区，然后收起抽屉。"""
        self.chat.open_session(session_id)
        self._drawer.set_current(session_id)
        self.hide_drawer()

    def _on_new_session_requested(self) -> None:
        """抽屉里点「新建对话」：收起抽屉，右侧换成空白首页（此时还不建会话）。"""
        self.hide_drawer()
        self._drawer.set_current("")
        self.chat.start_new_conversation()

    def _restore_last_session(self) -> None:
        """启动时自动接上最近更新过的那条对话；一条都没有就停在空白首页。"""
        sessions = session_store.list_sessions()      # 已按 updated_at 倒序
        if not sessions:
            self.chat.start_new_conversation()
            return
        newest = sessions[0]
        self.chat.open_session(newest.id)
        self._drawer.set_current(newest.id)

    def _on_session_updated(self, session_id: str) -> None:
        if self._drawer.isVisible():
            self._drawer.reload()
            self._drawer.set_current(session_id)

    def _on_session_deleted(self, session_id: str) -> None:
        """删掉的正好是当前打开的会话 → 聊天区清空（文件已没了）。"""
        if self.chat.current_session_id == session_id:
            self.chat.reset_conversation()

    def resizeEvent(self, event):  # noqa: N802 - Qt 命名
        super().resizeEvent(event)
        if self._drawer.isVisible():
            self._place_drawer()

    def moveEvent(self, event):  # noqa: N802
        super().moveEvent(event)
        if self._drawer.isVisible():
            self._place_drawer()

    def closeEvent(self, event):  # noqa: N802
        self._drawer.close()
        self.character.shutdown()
        super().closeEvent(event)

    def keyPressEvent(self, event):  # noqa: N802
        if event.key() == Qt.Key.Key_Escape and self._drawer.isVisible():
            self.hide_drawer()
            return
        super().keyPressEvent(event)

    # --- 设置 -----------------------------------------------------------
    def open_settings(self) -> None:
        """打开设置窗口（无边框圆角，点框外自动关）。

        注意是 modeless：只有非模态，窗口外的点击才会作为事件送到别处，
        「点框外关闭」才做得到（模态会把这些点击吃掉）。
        """
        # 延迟导入：settings_dialog 反过来要用本模块的 ICON_DIR / load_icon
        from dsai4431_chatbot.core.gui.settings_dialog import (
            DIALOG_H,
            DIALOG_W,
            SettingsDialog,
        )

        dlg = self._settings
        if dlg is not None and dlg.isVisible():
            dlg.raise_()
            dlg.activateWindow()
            return

        dlg = SettingsDialog(self, character=self.character)
        dlg.move(
            self.frameGeometry().center() - QPoint(DIALOG_W // 2, DIALOG_H // 2)
        )
        dlg.destroyed.connect(lambda: setattr(self, "_settings", None))
        self._settings = dlg
        dlg.show()


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
    # 语言：启动时定下来（没有记录就是中文）。换语言只能重启，所以这里读一次就够。
    i18n.apply_saved()
    # 换肤：启动时按上次的选择套 QSS（没有记录就是 light）
    themes.apply_saved(app)

    win = MainWindow()
    win.show()
    return app.exec()


if __name__ == "__main__":
    raise SystemExit(main())

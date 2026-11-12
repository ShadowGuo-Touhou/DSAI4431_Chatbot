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
import threading
from pathlib import Path
from typing import Literal

from PySide6.QtCore import (
    QEasingCurve,
    QLockFile,
    QPoint,
    QPropertyAnimation,
    QRectF,
    QRunnable,
    QSize,
    Qt,
    QThreadPool,
    QTimer,
    Signal,
)
from PySide6.QtGui import QColor, QIcon, QPainter, QPen
from PySide6.QtWidgets import (
    QApplication,
    QComboBox,
    QFrame,
    QHBoxLayout,
    QLabel,
    QMainWindow,
    QMessageBox,
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
    loading_page,
    personas,
    rag_service,
    session_store,
    theme,
    themes,
    tool_router,
    markdown_lite,
    voice_input,
)
from dsai4431_chatbot.core.gui.loading_page import LoadingPage
from dsai4431_chatbot.core.gui.rag_service import RagService
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
    # 首次装载「有结论」时发一次：成功 / 失败 / 没有模型。启动加载页要等它
    # 才能把「加载 Live2D」这一行收掉（ok, 失败原因；没有模型时原因是 "no_model"）
    settled = Signal(bool, str)

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
        """有模型就嵌进来；没有模型/素材就**留空**，不提示也不报错。"""
        model = model or live2d_embed.default_model()
        if model is None:
            print("[character] 没有 Live2D 模型文件，界面留空", file=sys.stderr, flush=True)
            self._hint.hide()
            self._status.hide()
            # 延到事件循环里再发：调用方通常在构造完才接这个信号
            QTimer.singleShot(0, lambda: self.settled.emit(False, "no_model"))
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
        self.settled.emit(True, "")

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
        # 按用户要求：素材缺失就**留空**，不在界面上报错（诊断只进控制台）
        print(f"[character] Live2D 加载失败，界面留空：{msg}", file=sys.stderr, flush=True)
        self._hint.hide()
        self._status.hide()
        self._set_state("")
        self.settled.emit(False, msg)

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


class _Bubble(QLabel):
    """聊天气泡。

    `role == "bot"` 的气泡把 Markdown 渲染成富文本（表格/代码块/列表…），
    用户消息与思考链保持纯文本；原文留在 `raw_text` 里，方便回放与测试。

    宽度：**按内容实测**决定（微信那种——短句窄框、长句撑到上限），
    只靠 sizeHint 的话 QLabel 会一直保持很窄，长句过早折行。
    """

    MAX_WIDTH = 10**6

    def __init__(self, role: str, parent=None) -> None:
        super().__init__(parent)
        self.role = role
        self.raw_text = ""
        self.max_width = self.MAX_WIDTH

    def set_raw(self, text: str) -> None:
        self.raw_text = "" if text is None else str(text)
        if self.role == "bot":
            self.setText(markdown_lite.to_html(self.raw_text))
        else:
            self.setText(self.raw_text)
        self._fit_width()

    def set_max_width(self, width: int) -> None:
        self.max_width = max(160, int(width))
        self.setMaximumWidth(self.max_width)
        self._fit_width()

    def _fit_width(self) -> None:
        """把最小宽度调到「内容自然宽度」，再用最大值收住。"""
        self.ensurePolished()        # 先让 QSS 生效，否则量到的字体是默认字体
        metrics = self.fontMetrics()
        natural = 0
        for line in (self.raw_text or "").splitlines() or [""]:
            natural = max(natural, metrics.horizontalAdvance(line))
        padding = 34 if self.role != "reasoning" else 26
        self.setMinimumWidth(max(60, min(self.max_width, natural + padding)))


class MessageArea(QScrollArea):
    """消息区：可滚动的竖向气泡列表。

    滚动规矩：
    - 用户发消息 / 追加消息 → 一定贴到底部（`_pin_bottom`）
    - 用户自己往上翻 → 松开吸附，流式回复不再把他拽回去
    - 不在底部时，视图底部中间浮出一个「↓」圆钮，点一下回到底部
    """

    JUMP_SIDE = 40          # 回到底部按钮直径

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWidgetResizable(True)
        self.setFrameShape(QFrame.Shape.NoFrame)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

        self._body = QWidget()
        self._body.setObjectName("messageViewport")
        self._lay = QVBoxLayout(self._body)
        self._lay.setContentsMargins(4, 4, 4, 4)
        # 行距收紧一点，交错排列时更像聊天软件（太松会显得散）
        self._lay.setSpacing(8)
        self._lay.addStretch(1)

        self._empty = QLabel(t("main.messages.empty"))
        self._empty.setObjectName("messageEmpty")
        self._empty.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self._lay.insertWidget(0, self._empty)

        self._has_messages = False
        self.setWidget(self._body)

        # 是否自动贴底：用户自己往上滚就松开，发消息时重新吸附
        self._pin_bottom = True
        self._jump = round_button("chevron", t("main.button.jump_bottom"))
        self._jump.setParent(self.viewport())
        self._jump.setFixedSize(self.JUMP_SIDE, self.JUMP_SIDE)
        self._jump.clicked.connect(self.jump_to_end)
        self._jump.hide()
        self._jump_anim = QPropertyAnimation(self.verticalScrollBar(), b"value", self)
        self._jump_anim.setDuration(160)
        self._jump_anim.setEasingCurve(QEasingCurve.Type.OutCubic)

        bar = self.verticalScrollBar()
        bar.rangeChanged.connect(self._on_range_changed)
        bar.valueChanged.connect(self._on_scrolled)

    def add_message(self, role: Literal["user", "bot"], text: str) -> QLabel:
        """追加一条完整消息，返回气泡（流式回复也可以先用它占位）。"""
        bubble = self.begin_message(role)
        bubble.set_raw(text)
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

        bubble = _Bubble(role)
        bubble.setObjectName(self.ROLE_NAMES.get(role, "bubbleBot"))
        bubble.setWordWrap(True)
        bubble.setTextInteractionFlags(Qt.TextInteractionFlag.TextSelectableByMouse)
        if role == "bot":
            # 回答里的链接可以点（Markdown 渲染之后才有 <a>）
            bubble.setOpenExternalLinks(True)
        bubble.setSizePolicy(QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Preferred)
        # 微信式：宽度跟着内容走，最多占视口 80%（以前 66% 太窄，长句很早就折行）
        bubble.set_max_width(self._bubble_max_width())

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
        # 布局里放的是 box（外层容器），外面拿到的是 bubble（QLabel）——
        # 记下来，`before=bubble` 才能插到正确位置（否则会一路追加到末尾，踩过）
        bubble._box = box
        index = self._lay.count() - 1
        if before is not None:
            target = getattr(before, "_box", before)
            found = self._lay.indexOf(target)
            if found >= 0:
                index = found
        self._lay.insertWidget(index, box)
        self.scroll_to_end()
        return bubble

    def scroll_to_end(self) -> None:
        """贴到底部。布局还没算完时（刚插入气泡）排一次队再滚。"""
        self._pin_bottom = True
        QTimer.singleShot(0, self._apply_pin)

    def _apply_pin(self) -> None:
        if not self._pin_bottom:
            return
        bar = self.verticalScrollBar()
        bar.setValue(bar.maximum())
        self._update_jump()

    def _on_range_changed(self, _low: int, _high: int) -> None:
        # 内容变长（流式回复、图片加载）时，贴着底部的人不能被甩开
        if self._pin_bottom:
            bar = self.verticalScrollBar()
            bar.setValue(bar.maximum())
        self._update_jump()

    def _on_scrolled(self, _value: int) -> None:
        bar = self.verticalScrollBar()
        # 到底就重新吸附，离开底部就松开（用户自己翻 / 动画过程中都走这条）
        self._pin_bottom = bar.value() >= bar.maximum() - 4
        self._update_jump()

    def _update_jump(self) -> None:
        bar = self.verticalScrollBar()
        away = bar.maximum() > 0 and bar.value() < bar.maximum() - 4
        if away:
            self._place_jump()
        self._jump.setVisible(away)

    def _place_jump(self) -> None:
        view = self.viewport()
        x = max(0, (view.width() - self._jump.width()) // 2)
        y = max(0, view.height() - self._jump.height() - 14)
        self._jump.move(x, y)

    def jump_to_end(self) -> None:
        """圆钮：平滑回到底部（并重新吸附）。"""
        self._pin_bottom = True
        bar = self.verticalScrollBar()
        self._jump_anim.stop()
        self._jump_anim.setStartValue(bar.value())
        self._jump_anim.setEndValue(bar.maximum())
        self._jump_anim.start()
        self._update_jump()

    def resizeEvent(self, event) -> None:      # noqa: N802 - Qt 命名
        super().resizeEvent(event)
        self._place_jump()
        # 窗口变宽变窄时，已有气泡的上限也要跟着变（否则一直卡在旧宽度）
        width = self._bubble_max_width()
        for bubble in self._body.findChildren(QLabel):
            if bubble.objectName().startswith("bubble"):
                if hasattr(bubble, "set_max_width"):
                    bubble.set_max_width(width)
                else:
                    bubble.setMaximumWidth(width)

    def _bubble_max_width(self) -> int:
        """气泡最大宽度：跟内容走，最多占视口 80%（微信那种观感）。"""
        return max(240, int(self.viewport().width() * 0.8))

    def clear_messages(self) -> None:
        while self._lay.count() > 2:  # 保留 empty 标签与底部 stretch
            item = self._lay.takeAt(1)
            if item.widget():
                item.widget().deleteLater()
        self._has_messages = False
        self._empty.show()
        self._pin_bottom = True
        self._jump.hide()


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


class _Waveform(QWidget):
    """录音时的声纹起伏：一排竖条，以中线为轴上下起伏。

    数据来自 `Recorder.level`（每块音频一个峰值，约 20 ms 一次）。这里不逐块
    推进，而是每 50 ms 推进一格取这段时间的最大值 —— 既够顺滑，又不会因为
    主线程被高频刷新拖住。
    """

    BARS = 32
    STEP_MS = 50
    # 麦克风原始电平很小（实测静音 0.004、正常说话才 0.05~0.3），
    # 放大几倍柱子才看得出来在"跳"
    GAIN = 3.0
    # 静音时也留 6px：3px 的柱子配 2px 间隙看着像断掉的虚线，像坏了
    MIN_BAR = 6.0

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("voiceWave")
        self.setFixedHeight(30)
        self._levels = [0.0] * self.BARS
        self._pending = 0.0
        self._timer = QTimer(self)
        self._timer.setInterval(self.STEP_MS)
        self._timer.timeout.connect(self._advance)
        self.hide()

    # --- 生命周期 -------------------------------------------------------
    def start(self) -> None:
        self._levels = [0.0] * self.BARS
        self._pending = 0.0
        self.show()
        self._timer.start()

    def stop(self) -> None:
        self._timer.stop()
        self.hide()

    def push(self, level: float) -> None:
        """记录这段时间里的最大峰值（尖峰不会被后续小声盖掉）。"""
        self._pending = max(self._pending, float(level))

    def _advance(self) -> None:
        self._levels.pop(0)
        self._levels.append(min(1.0, self._pending))
        self._pending *= 0.35            # 衰减，看起来才有"跳"的感觉
        self.update()

    # --- 绘制 -----------------------------------------------------------
    def _accent(self) -> QColor:
        try:
            return QColor(themes.manager().palette.get("accent", "#4D6BFE"))
        except Exception:                # noqa: BLE001 - 取不到就用兜底色
            return QColor("#4D6BFE")

    def paintEvent(self, event) -> None:  # noqa: N802 - Qt 命名
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        color = self._accent()
        width = self.width()
        height = self.height()
        count = self.BARS
        gap = 2.0
        bar_w = max(2.0, (width - gap * (count - 1)) / count)
        mid = height / 2.0

        # 基线：静音时也看得见"这里有一排东西"，不然整行像断掉的虚线
        baseline = QColor(color)
        baseline.setAlpha(55)
        painter.setPen(QPen(baseline, 1.0))
        painter.drawLine(0, int(mid), width, int(mid))

        painter.setPen(Qt.PenStyle.NoPen)
        for index, level in enumerate(self._levels):
            # 中间高、两边低：越靠中间系数越大，像真声纹
            center_bias = 1.0 - abs(index - (count - 1) / 2.0) / ((count - 1) / 2.0)
            shape = 0.45 + 0.55 * center_bias
            boosted = min(1.0, level * self.GAIN * shape)
            bar_h = max(self.MIN_BAR, boosted * (height - 4))
            x = index * (bar_w + gap)
            y = mid - bar_h / 2.0

            alpha = 110 + int(120 * min(1.0, boosted * 2))
            color.setAlpha(min(255, alpha))
            painter.setBrush(color)
            # 圆角最多 3px：取 bar_w/2 的话矮柱子会被吃成圆点，像一串珠子
            radius = min(bar_w / 2.0, bar_h / 2.0, 3.0)
            painter.drawRoundedRect(
                QRectF(x, y, bar_w, bar_h), radius, radius
            )
        painter.end()


class InputCard(QFrame):
    """输入卡：一张圆角卡片，上输入、下操作行（附件在左，语音/发送在右）。"""

    submitted = Signal(str)
    # 点了麦克风（开始/结束录音由 ChatColumn 判断，这里只是转发）
    voice_clicked = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("inputCard")
        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)
        # 竖向只占内容高度，不要把消息区让出的空间全吃掉
        self.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Maximum)

        outer = QVBoxLayout(self)
        outer.setContentsMargins(14, 12, 12, 10)
        outer.setSpacing(6)

        # 录音/识别的状态提示（平时隐藏，不占视线）
        self._note = QLabel("")
        self._note.setObjectName("voiceNote")
        self._note.setWordWrap(True)
        self._note.hide()
        outer.addWidget(self._note)

        # 录音时的声纹起伏（同样平时隐藏）
        self._wave = _Waveform()
        outer.addWidget(self._wave)

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
        self.btn_voice.clicked.connect(self.voice_clicked.emit)
        actions.addWidget(self.btn_voice)

        self.btn_send = round_button(
            "send", t("main.button.send"), primary=True, action=True
        )
        actions.addWidget(self.btn_send)

        outer.addLayout(actions)

        self.edit.submitted.connect(self.submitted)
        self.btn_send.clicked.connect(self.edit.submit)

    # --- 语音输入的状态显示 ---------------------------------------------
    def set_note(self, text: str) -> None:
        """显示/清掉一行状态（"正在听…"、"识别中…"、"没听清"）。"""
        if text:
            self._note.setText(text)
            self._note.show()
        else:
            self._note.clear()
            self._note.hide()

    def set_recording(self, on: bool) -> None:
        """录音中：麦克风按钮换状态（QSS 里 [recording="true"]）+ 声纹动画。"""
        self.btn_voice.setProperty("recording", bool(on))
        style = self.btn_voice.style()
        style.unpolish(self.btn_voice)
        style.polish(self.btn_voice)
        if on:
            self._wave.start()
        else:
            self._wave.stop()

    def push_level(self, level: float) -> None:
        """把录音电平喂给声纹动画（Recorder.level 直接连过来）。"""
        self._wave.push(level)


class _HomeCombo(QComboBox):
    """新对话页的选择器：**盒子**宽度贴着当前项，**弹窗**宽度贴着最长项。

    为什么不能直接用 QComboBox：
    - 它默认按最长的一项算盒子宽度 —— 选中短名字时右边留一截空白，箭头离文字老远
    - 而弹窗宽度又跟着盒子走 —— 盒子收窄之后，长选项被省略成「deeps...soner」

    所以盒子这边自己算宽度（见 HomePage._fit_combo），弹窗那边在 showPopup()
    里先把列表的最小宽度撑到最长项。
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # 弹窗圆角必须在第一次 showPopup 之前设好，见 themes.round_popup
        themes.round_popup(self)

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
        │  │ [+]     [deepseek-flash ▾] [↑] │  │
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


class _ToolJob(QRunnable):
    """后台跑一次工具调用（检索会发 HTTP 给 Ollama，最慢十几秒，绝不能卡界面）。

    worker 里**不碰任何 Qt 对象**：结果写进带锁的字段，主线程用 QTimer 轮询。
    """

    def __init__(
        self,
        router,
        calls: list,
        *,
        min_score: float | None = None,
        max_chars: int | None = None,
    ) -> None:
        super().__init__()
        self.router = router
        self.calls = [dict(call) for call in calls]
        # 门槛/字数上限都在**主线程**读好再带进来：worker 里不碰 QSettings
        self.min_score = min_score
        self.max_chars = max_chars
        self.lock = threading.Lock()
        self.outcomes: list | None = None
        self.error: BaseException | None = None
        self.setAutoDelete(True)

    def run(self) -> None:                      # noqa: D401 - QRunnable 约定
        outcomes = []
        try:
            for call in self.calls:
                outcomes.append(
                    self.router.run(
                        call, min_score=self.min_score, max_chars=self.max_chars
                    )
                )
        except BaseException as exc:            # noqa: BLE001 - 后台不能把异常丢给 Qt
            with self.lock:
                self.error = exc
        with self.lock:
            self.outcomes = outcomes

    def snapshot(self):
        with self.lock:
            return self.outcomes, self.error


class _VoiceJob(QRunnable):
    """后台做一次语音识别（模型加载 + 解码，几百毫秒到几秒）。

    和 `_ToolJob` 一个套路：worker 里不碰 Qt，结果写进带锁字段，
    主线程用 QTimer 轮询。
    """

    def __init__(self, samples, *, language: str = "auto", model_dir=None) -> None:
        super().__init__()
        self.samples = samples
        self.language = language
        self.model_dir = model_dir
        self.lock = threading.Lock()
        self.text = ""
        self.error: BaseException | None = None
        self.done = False
        self.setAutoDelete(True)

    def run(self) -> None:                      # noqa: D401 - QRunnable 约定
        try:
            from dsai4431_chatbot.core.gui import voice_input

            text = voice_input.transcribe(
                self.samples, self.language, self.model_dir
            )
            with self.lock:
                self.text = text
        except BaseException as exc:            # noqa: BLE001 - 交给主线程显示
            with self.lock:
                self.error = exc
        finally:
            with self.lock:
                self.done = True

    def snapshot(self):
        with self.lock:
            return self.text, self.error, self.done


class _SpeechJob(QRunnable):
    """后台确保语音模型在（缺哪个下哪个，带 sha256 校验）。

    下载 228 MB 会花几分钟，绝不能放主线程；进度靠主线程轮询。
    """

    def __init__(self, model_dir) -> None:
        super().__init__()
        self.model_dir = model_dir
        self.lock = threading.Lock()
        self.stage = ""
        self.done_bytes = 0
        self.total_bytes = 0
        self.result = ""
        self.error: BaseException | None = None
        self.done = False
        self.setAutoDelete(True)

    def run(self) -> None:                      # noqa: D401 - QRunnable 约定
        try:
            from dsai4431_chatbot.core.gui import voice_input

            result = voice_input.ensure_models(self.model_dir, progress=self._report)
            with self.lock:
                self.result = result
        except BaseException as exc:            # noqa: BLE001 - 交给主线程显示
            with self.lock:
                self.error = exc
        finally:
            with self.lock:
                self.done = True

    def _report(self, stage: str, done: int, total: int) -> None:
        with self.lock:
            self.stage = stage
            self.done_bytes = done
            self.total_bytes = total

    def snapshot(self):
        with self.lock:
            return (
                self.stage,
                self.done_bytes,
                self.total_bytes,
                self.result,
                self.error,
                self.done,
            )


class ChatColumn(QWidget):
    """右侧聊天列：顶栏 + （对话页 | 新对话页）+ 会话后端。"""

    settings_requested = Signal()
    menu_requested = Signal()
    # 会话内容变了（新建 / 首条消息自动建 / 追加消息）→ 让外层刷新会话列表
    session_updated = Signal(str)

    def __init__(self, parent=None, *, rag=None):
        super().__init__(parent)

        # 知识库检索：由 MainWindow 传进来（同一个实例也给设置页用，状态才一致）
        self.rag = rag if rag is not None else RagService(self)

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
        self.client.tool_calls.connect(self._on_tool_calls)

        # 工具调用（tool calling）：模型自己要检索时，这里负责真去查
        self._tool_router = tool_router.ToolRouter(self.rag)
        self._tool_rounds = 0          # 本轮已经查了几次（防无限循环）
        self._req_messages: list[dict] = []   # 正在发的这份 messages（工具轮要往后追加）
        self._req_model = ""
        self._tool_notes: list[QLabel] = []   # 本轮已画的「🔍 检索…」小字
        # 检索放到后台线程跑：主线程只轮询，界面不卡
        self._tool_job: _ToolJob | None = None
        self._tool_busy = False
        self._pending_note: QLabel | None = None
        self._tool_timer = QTimer(self)
        self._tool_timer.setInterval(80)
        self._tool_timer.timeout.connect(self._poll_tool_job)

        self._history: list[dict] = []   # OpenAI 格式：{"role": ..., "content": ...}
        self._bubble: QLabel | None = None   # 正在流式写入的那个气泡
        self._stream_raw = ""               # 本轮回答的原始 Markdown（渲染用）
        self._bubble_fresh = True            # 还没写过内容（要替换占位文字）
        self._reasoning_text = ""            # 本轮思考链全文（reasoner 才有）
        self._reasoning_bubble: QLabel | None = None
        # 当前会话（data/session 里的一条）；没建会话就直接发消息时自动建一条
        self._session_id = ""
        self._session: session_store.SessionMeta | None = None
        # 新对话页上选好的人格 / 模型：等第一句话发出去、真要建会话时才用
        self._pending_persona: dict | None = None
        self._pending_model = ""
        # 最近一次检索的结果（超时/失败时给上层看原因）
        self._rag_last = None

        # 等回复时（或正在后台检索时）按 Enter 不发也不清空输入框
        self.input.edit.can_submit = (
            lambda: not self.client.busy() and not self._tool_busy
        )
        self.input.submitted.connect(self._on_submit)

        # --- 语音输入 ---------------------------------------------------
        # 录音在主线程（QtMultimedia 的消息），识别放后台线程（模型加载
        # 2.5 s、解码几百毫秒，绝不能卡界面）
        self._recorder = voice_input.Recorder(self)
        self._recorder.auto_stopped.connect(self._finish_voice)
        # 电平直接喂给声纹动画（InputCard 自己决定要不要画）
        self._recorder.level.connect(self.input.push_level)
        self._voice_job: _VoiceJob | None = None
        self._voice_busy = False
        self._voice_timer = QTimer(self)
        self._voice_timer.setInterval(80)
        self._voice_timer.timeout.connect(self._poll_voice_job)
        self.input.voice_clicked.connect(self._on_voice_click)

    # --- 语音输入 -------------------------------------------------------
    def _voice_model_dir(self):
        cfg = chat_config.load()
        return voice_input.resolve_model_dir(getattr(cfg, "voice_model_dir", ""))

    def _on_voice_click(self) -> None:
        """麦克风按钮：没在录就开始，正在录就结束并识别。"""
        if self._voice_busy:
            return                       # 后台还在识别，别叠加
        if self._recorder.is_recording():
            self._finish_voice()
        else:
            self._begin_voice()

    def _begin_voice(self) -> None:
        if not self._recorder.supported():
            self.input.set_note(t("main.voice.no_device"))
            return
        model_dir = self._voice_model_dir()
        if not voice_input.models_ready(model_dir):
            self.input.set_note(t("main.voice.no_model"))
            return
        if not self._recorder.start():
            self.input.set_note(t("main.voice.start_failed"))
            return
        self.input.set_recording(True)
        self.input.set_note(t("main.voice.listening"))
        # 用户说话的这几秒正好用来把 228 MB 的模型读进来
        voice_input.warm_up_background("auto", model_dir)

    def _finish_voice(self) -> None:
        self.input.set_recording(False)
        samples = self._recorder.stop()
        if samples is None:
            self.input.set_note(t("main.voice.too_short"))
            return
        self._voice_busy = True
        self.input.set_note(t("main.voice.recognizing"))
        job = _VoiceJob(samples, model_dir=self._voice_model_dir())
        self._voice_job = job
        QThreadPool.globalInstance().start(job)
        self._voice_timer.start()

    def _poll_voice_job(self) -> None:
        job = self._voice_job
        if job is None:
            self._voice_timer.stop()
            return
        text, error, done = job.snapshot()
        if not done:
            return

        self._voice_timer.stop()
        self._voice_job = None
        self._voice_busy = False

        if error is not None:
            self.input.set_note(t("main.voice.failed", reason=str(error)[:60]))
            return
        if not text:
            self.input.set_note(t("main.voice.empty"))
            return

        self.input.set_note("")
        # 插到光标处（用户可能已经敲了半句），不覆盖
        self.input.edit.insertPlainText(text)
        self.input.edit.setFocus()

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
        self._bubble.set_raw(t("main.messages.thinking"))
        self._bubble_fresh = True
        self._stream_raw = ""
        self._reasoning_text = ""
        self._reasoning_bubble = None

        model = session.model or cfg.model
        self._tool_rounds = 0
        self._tool_notes = []
        self._tool_busy = False
        self._pending_note = None
        self._start_request(cfg, self._payload(cfg), model)

    # --- 发请求 / 工具轮 -------------------------------------------------
    def _rag_on(self, cfg) -> bool:
        """知识库是否参与本轮（只有开/关两种状态，检索方式固定为工具调用）。"""
        return bool(getattr(cfg, "rag_enabled", True))

    def _tools_for(self, cfg) -> list[dict] | None:
        """开着知识库、且有索引时，把工具声明发给模型（唯一检索方式）。"""
        if not self._rag_on(cfg):
            return None
        if self.rag is None or self.rag.index() is None:
            return None
        return [tool_router.TOOL_SPEC]

    def _start_request(self, cfg, messages: list[dict], model: str) -> None:
        self._req_messages = messages
        self._req_model = model
        if not self.client.send(cfg, messages, model=model, tools=self._tools_for(cfg)):
            self._finish_bubble(t("main.messages.failed", msg="请求没能发出去"))

    def _payload(self, cfg) -> list[dict]:
        """人格文件 → system 消息；RAG 提示词 → 另一条 system；再加最近对话。

        片段一律**不注入**：模型自己调 search_knowledge，结果作为 tool 消息回来。
        """
        messages: list[dict] = []
        system = self._system_prompt(cfg)
        if system:
            messages.append({"role": "system", "content": system})
        rag_hint = self._rag_hint(cfg)
        if rag_hint:
            # 这一轮确实会把工具声明发出去时，顺手加一句「走工具通道，别在正文写标记」
            if self._tools_for(cfg):
                rag_hint = f"{rag_hint.rstrip()}\n\n{tool_router.PROTOCOL_HINT}"
            messages.append({"role": "system", "content": rag_hint})
        messages.extend(self._history[-MAX_HISTORY_MESSAGES:])
        return messages

    def _rag_hint(self, cfg) -> str:
        """用户在设置页写的 RAG 提示词（默认只说「你有知识库、它在哪」）。

        `{dir}` 会替换成当前知识库目录，换了目录文案也不会说错。
        """
        if not self._rag_on(cfg):
            return ""
        text = str(getattr(cfg, "rag_prompt", "") or "").strip()
        if not text:
            return ""
        folder = str(getattr(cfg, "rag_dir", "") or "asset/RAG").strip()
        return text.replace("{dir}", folder)

    # --- 知识库检索 -----------------------------------------------------
    # --- 工具调用（tool calling）----------------------------------------
    def _on_tool_calls(self, calls: list) -> None:
        """模型说「我要查知识库」：真去查，把结果作为 tool 消息追加后重新发请求。"""
        cfg = chat_config.load()
        if not calls:
            self._finish_bubble(t("main.messages.failed", msg="模型返回了空的工具调用"))
            return
        if self._tool_rounds >= tool_router.MAX_ROUNDS:
            # 已经用完轮次、也明确告诉过它「不许再查」，它还要求工具 → 收尾，别死循环
            self._finish_bubble(
                t("main.messages.failed", msg="模型反复要求检索，已停止本轮")
            )
            return

        messages = self._req_messages
        # 思考模式下必须把这一轮的思考链带回去，否则下一次请求会被 400 拒掉
        messages.append(
            tool_router.assistant_message(calls, self.client.last_reasoning())
        )
        self._req_messages = messages

        # 先画一行「正在检索」，让用户知道在干什么（此时还没结果）
        self._pending_note = None
        try:
            self._pending_note = self.messages.begin_message(
                "reasoning", before=self._bubble
            )
            self._pending_note.setText("🔍 正在检索知识库…")
            self.messages.scroll_to_end()
        except Exception as exc:              # noqa: BLE001
            print(f"[rag] 检索提示行没画出来：{exc}", flush=True)

        # 检索丢到后台线程：这一步可能耗时十几秒，绝不能占着主线程
        self._tool_busy = True
        self._tool_job = _ToolJob(
            self._tool_router,
            calls,
            min_score=float(getattr(cfg, "rag_tool_min_score", 0.5)),
            max_chars=int(getattr(cfg, "rag_inject_chars", 3000) or 3000),
        )
        QThreadPool.globalInstance().start(self._tool_job)
        self._tool_timer.start()

    def _poll_tool_job(self) -> None:
        """轮询后台检索：好了就把 tool 消息接上、继续发请求。"""
        job = self._tool_job
        if job is None:
            self._tool_timer.stop()
            return
        outcomes, error = job.snapshot()
        if outcomes is None and error is None:
            return                            # 还在跑

        self._tool_timer.stop()
        self._tool_job = None
        self._tool_busy = False

        if error is not None:
            self._finish_bubble(
                t("main.messages.failed", msg=f"检索出错：{error}")
            )
            return

        messages = self._req_messages
        for index, outcome in enumerate(outcomes or []):
            call_id = outcome.call_id or ""
            messages.append(
                {
                    "role": "tool",
                    # 必须回填模型给的 call id，否则服务端会拒绝
                    "tool_call_id": call_id,
                    "content": outcome.content,
                }
            )
            self._show_tool_note(outcome, reuse=self._pending_note if index == 0 else None)
            print(f"[rag] 工具调用：{outcome.summary()}", flush=True)
            if self._session is not None:
                session_store.append_rag_event(
                    self._session.id,
                    query=outcome.query,
                    hits=[] if not outcome.hits else [f"{outcome.hits} 段"],
                    scores=[round(outcome.top_score, 4)] if outcome.hits else [],
                    elapsed_ms=outcome.elapsed_ms,
                )
        self._pending_note = None

        self._tool_rounds += 1
        # 到轮次上限就不给工具了，逼它拿现有资料直接回答
        exhausted = self._tool_rounds >= tool_router.MAX_ROUNDS
        if exhausted:
            messages.append(
                {
                    "role": "system",
                    "content": "检索次数已用完，请立刻基于已有资料回答；资料不足就直说。",
                }
            )
        cfg = chat_config.load()
        if not self.client.send(
            cfg,
            messages,
            model=self._req_model,
            tools=None if exhausted else self._tools_for(cfg),
        ):
            self._finish_bubble(t("main.messages.failed", msg="工具结果没能发回模型"))

    def _show_tool_note(self, outcome, reuse: QLabel | None = None) -> None:
        """在回答气泡上方写「🔍 检索…」。`reuse` 用来把「正在检索…」那行改写掉。"""
        try:
            note = reuse or self.messages.begin_message("reasoning", before=self._bubble)
            note.setText(f"🔍 {outcome.summary()}")
            if note not in self._tool_notes:
                self._tool_notes.append(note)
            self.messages.scroll_to_end()
        except Exception as exc:              # noqa: BLE001 - 提示行画不出来不影响主流程
            print(f"[rag] 检索提示行没画出来：{exc}", flush=True)

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
            # 旧会话/旧配置里可能是 deepseek-chat 这种下线的名字，建会话时就归一
            model=personas.normalize_model(self._pending_model or cfg.model)
            or personas.MODELS[0],
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
                thought.set_raw(row["reasoning"])
            bubble = self.messages.begin_message(row["role"])
            bubble.set_raw(row["text"] or t("main.messages.empty_reply"))
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
        # 用 set_raw：它会顺带按内容量宽度（直接用 setText 会一直保持很窄）
        self._reasoning_bubble.set_raw(self._reasoning_text)
        self.messages.scroll_to_end()

    def _on_delta(self, piece: str) -> None:
        if self._bubble is None:
            return
        self._stream_raw += piece
        self._bubble_fresh = False
        self._bubble.set_raw(self._stream_raw)
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
            self._bubble.set_raw(text)
            self._bubble = None
        # 收尾时把后台检索状态也清干净，免得输入框一直卡在「不能发」
        self._tool_timer.stop()
        self._tool_job = None
        self._tool_busy = False
        self._pending_note = None
        self.messages.scroll_to_end()

    # --- 新对话 ---------------------------------------------------------
    def reset_conversation(self) -> None:
        """旧名字，保留给「删掉的正好是当前会话」那一处：清空并回到首页。"""
        self.start_new_conversation()


class MainWindow(QMainWindow):
    # 启动加载清单：(key, i18n 标题键, 总进度权重)。
    # 以后接语音模型（SenseVoice）就再追加一行，别的都不用动。
    LOAD_STEPS = (
        ("ui", "loading.step_ui", 0.4),
        ("live2d", "loading.step_live2d", 1.6),
        ("session", "loading.step_session", 0.4),
        ("ollama", "loading.step_ollama", 3.0),
        ("bge", "loading.step_bge", 3.0),
        ("speech", "loading.step_speech", 3.0),
        ("index", "loading.step_index", 2.0),
    )

    # 角色区最多占窗口宽度的这个比例（用户要求：2/5 左右）。
    # QSplitter 没有「最大比例」这种东西，只能靠子控件的 maximumWidth 卡住 ——
    # splitter 会尊重它，拖到上限就停。
    CHARACTER_MAX_RATIO = 0.4

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle(t("app.title"))
        self.resize(1440, 900)
        self.setMinimumSize(1100, 700)

        body = QWidget()
        body.setObjectName("windowBody")
        body.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)
        self.setCentralWidget(body)
        self._body = body

        root = QHBoxLayout(body)
        root.setContentsMargins(16, 16, 16, 16)
        root.setSpacing(0)

        # 左右两栏用 QSplitter：允许用户拖动比例，也方便调试布局
        splitter = QSplitter(Qt.Orientation.Horizontal)
        splitter.setChildrenCollapsible(False)
        # 两栏之间的留白。注意别指望 QSS 的 QSplitter::handle{width}：
        # 实测不生效（handle 宽度会是 0，两栏贴死），只能在这里设。
        splitter.setHandleWidth(theme.SPLITTER_GAP)
        splitter.setStretchFactor(0, 3)
        splitter.setStretchFactor(1, 7)
        splitter.setSizes([420, 1020])
        self._splitter = splitter
        root.addWidget(splitter)
        # 加载期间整块主内容禁用：覆盖层挡住鼠标，disable 兜住键盘焦点
        splitter.setEnabled(False)

        # 下面这些部件由启动阶段一个个填进来；加载页还在的时候是 None，
        # 所以任何用到它们的地方都要先判断（见 resizeEvent / open_settings 等）
        self.character: CharacterPanel | None = None
        self.chat: ChatColumn | None = None
        self._drawer: SessionDrawer | None = None
        self._settings = None

        # 知识库服务构造很轻（只建对象 + 一个没启动的定时器），先建好
        self.rag = RagService(self)

        # 退出前把 WebEngine 收掉（嵌入式 HTTP 服务 + 渲染进程）。
        # aboutToQuit 管"换语言自动重启"（app.quit() 不触发 closeEvent），
        # closeEvent 管用户直接关窗口，两个入口都收一遍；shutdown 是幂等的。
        app = QApplication.instance()
        if app is not None:
            app.aboutToQuit.connect(self._on_about_to_quit)

        self._live2d_deadline: QTimer | None = None
        self._boot_seen: set[str] = set()
        self._rag_wired = False
        self._speech_job: _SpeechJob | None = None
        self._speech_timer = QTimer(self)
        self._speech_timer.setInterval(120)
        self._speech_timer.timeout.connect(self._poll_speech_job)

        # --- 启动加载页（覆盖层，见 gui/loading_page.py）-----------------
        self.loading = LoadingPage(body)
        self.loading.setGeometry(body.rect())
        self.loading.raise_()
        for key, title_key, weight in self.LOAD_STEPS:
            self.loading.add_step(key, t(title_key), weight)
        self.loading.skip_requested.connect(self._on_skip_downloads)
        self.loading.closed.connect(self._on_loading_closed)

        # 先把窗口和加载页画出来，再一步步干重活。之前是构造里一口气干完，
        # 界面出来的时候活已经做完了 —— 加载页根本没机会显示。
        QTimer.singleShot(0, self._startup_ui)

    # --- 启动阶段 -------------------------------------------------------
    # 每一步之间用 singleShot(0) 让事件循环刷一次，加载页才有动画。
    def _startup_ui(self) -> None:
        self.loading.step("ui").done(t("loading.state.ready"))
        self.loading.refresh_progress()
        QTimer.singleShot(0, self._startup_live2d)

    def _startup_live2d(self) -> None:
        row = self.loading.step("live2d")
        row.start()
        self.loading.refresh_progress()

        self.character = CharacterPanel()
        self.character.settled.connect(self._on_live2d_settled)
        self._splitter.insertWidget(0, self.character)
        self._fit_character_width()

        # CharacterPanel 自己有 20 s 探活超时，这里再兜一层：万一信号没发
        # 出来，加载页也不能一直卡在这一行
        self._live2d_deadline = QTimer(self)
        self._live2d_deadline.setSingleShot(True)
        self._live2d_deadline.timeout.connect(self._on_live2d_timeout)
        self._live2d_deadline.start(25_000)

    def _stop_live2d_deadline(self) -> bool:
        """收掉兜底定时器；返回 True 表示这次调用是"第一次"收（没被超时抢先）。"""
        timer, self._live2d_deadline = self._live2d_deadline, None
        if timer is None:
            return False
        timer.stop()
        return True

    def _fit_character_width(self) -> None:
        """按窗口宽度卡住角色区的最大宽度。

        分割条没有「最大比例」这种东西，只能设子控件的 maximumWidth：
        QSplitter 会尊重它，拖动到上限就停住，窗口变大时上限自动放宽。
        """
        character = getattr(self, "character", None)
        body = getattr(self, "_body", None)
        if character is None or body is None:
            return
        body_w = body.width()
        if body_w <= 0:
            return
        limit = max(
            character.minimumWidth(), int(body_w * self.CHARACTER_MAX_RATIO)
        )
        if character.maximumWidth() != limit:
            character.setMaximumWidth(limit)

    def _on_live2d_settled(self, ok: bool, reason: str) -> None:
        if not self._stop_live2d_deadline():
            return                      # 已经按超时算过了
        row = self.loading.step("live2d")
        if ok:
            row.done(t("loading.state.ready"))
        elif reason == "no_model":
            row.skipped(t("loading.state.no_model"))
        else:
            # 加载失败按用户要求是"留空不报错"，但加载页上要如实说一声
            row.failed(t("loading.state.blank"))
        self.loading.refresh_progress()
        QTimer.singleShot(0, self._startup_session)

    def _on_live2d_timeout(self) -> None:
        if not self._stop_live2d_deadline():
            return
        self.loading.step("live2d").skipped(t("loading.state.timeout"))
        self.loading.refresh_progress()
        QTimer.singleShot(0, self._startup_session)

    def _startup_session(self) -> None:
        self.loading.step("session").start()
        self.loading.refresh_progress()
        QTimer.singleShot(0, self._build_chat)

    def _build_chat(self) -> None:
        row = self.loading.step("session")
        self.chat = ChatColumn(rag=self.rag)
        self.chat.settings_requested.connect(self.open_settings)
        self._splitter.addWidget(self.chat)

        # 会话抽屉（≡ 打开）：叠在窗口左侧，不占 splitter
        self._drawer = SessionDrawer(self)
        self._drawer.hide()
        self._drawer.new_session_requested.connect(self._on_new_session_requested)
        self._drawer.session_opened.connect(self._on_session_switch)
        self._drawer.session_deleted.connect(self._on_session_deleted)
        self._drawer.close_requested.connect(self.hide_drawer)
        self.chat.menu_requested.connect(self.toggle_drawer)
        self.chat.session_updated.connect(self._on_session_updated)

        count = self._restore_last_session()
        if count:
            row.done(t("loading.detail.messages", count=count))
        else:
            row.done(t("loading.state.ready"))
        self.loading.refresh_progress()
        QTimer.singleShot(0, self._startup_rag)

    def _startup_rag(self) -> None:
        """启动的知识库同步：信号驱动加载页的 ollama / bge / index 三行。

        语音那一行和 RAG 无关，并行检查（`_startup_speech`），谁先完谁先绿。
        """
        cfg = chat_config.load()
        if not cfg.rag_enabled:
            for key in ("ollama", "bge", "index"):
                self.loading.step(key).skipped(t("loading.state.off"))
            self.loading.refresh_progress()
            QTimer.singleShot(0, self._startup_speech)
            return

        self.loading.step("ollama").start(t("loading.detail.checking"))
        self.loading.step("index").start(t("loading.detail.checking"))
        self.loading.refresh_progress()

        if not self._rag_wired:
            self._rag_wired = True
            self.rag.bootstrap_progress.connect(self._on_boot_progress)
            self.rag.bootstrap_ready.connect(self._on_boot_ready)
            self.rag.ollama_ready.connect(self._on_ollama_ready)
            self.rag.progress.connect(self._on_sync_progress)
            self.rag.synced.connect(self._on_sync_done)

        self.rag.refresh(cfg)
        QTimer.singleShot(0, self._startup_speech)

    # --- 加载页：语音模型 ------------------------------------------------
    def _startup_speech(self) -> None:
        page = self.loading
        if page is None:
            return
        try:
            cfg = chat_config.load()
            model_dir = voice_input.resolve_model_dir(
                getattr(cfg, "voice_model_dir", "")
            )
        except Exception:                        # noqa: BLE001 - 配置坏了不该卡启动
            model_dir = voice_input.default_model_dir()

        if voice_input.models_ready(model_dir):
            page.step("speech").skipped(t("loading.state.installed"))
            page.refresh_progress()
            self._maybe_complete()
            return

        page.step("speech").start(t("loading.detail.checking"))
        page.show_skip(True)                     # 228 MB，允许用户跳过
        page.refresh_progress()

        job = _SpeechJob(model_dir)
        self._speech_job = job
        QThreadPool.globalInstance().start(job)
        self._speech_timer.start()

    def _poll_speech_job(self) -> None:
        job = self._speech_job
        page = self.loading
        if job is None or page is None:
            self._speech_timer.stop()
            return

        stage, done, total, result, error, finished = job.snapshot()
        row = page.step("speech")

        if not finished:
            if stage:
                name = stage.split("/")[-1]
                if total:
                    row.start()
                    row.set_progress(
                        done / total,
                        t("loading.detail.model",
                          name=name, done=self._mb(done), total=self._mb(total)),
                    )
                else:
                    row.start(t("loading.detail.model_unknown", name=name))
                page.refresh_progress()
            return

        self._speech_timer.stop()
        self._speech_job = None
        page.show_skip(False)
        if error is not None:
            row.failed(t("loading.detail.speech_failed", reason=str(error)[:60]))
        elif result == "downloaded":
            row.done(t("loading.state.ready"))
        else:
            row.skipped(t("loading.state.installed"))
        page.refresh_progress()
        self._maybe_complete()

    def _maybe_complete(self) -> None:
        """所有阶段都收尾了才收起加载页。"""
        page = self.loading
        if page is None:
            return
        for key in ("ollama", "bge", "index", "speech"):
            if page.step(key).status in (loading_page.PENDING, loading_page.RUNNING):
                return
        page.complete()

    # --- 加载页：自动安装（Ollama / bge）的进度 --------------------------
    @staticmethod
    def _mb(value: int) -> str:
        return f"{value / (1024 * 1024):.1f}"

    def _on_ollama_ready(self, launch) -> None:
        """Ollama 那一步的结论：复用 / 已启动 / 已接管 / 失败。

        下载进度**不在这里**：`_on_boot_progress` 负责「正在下载 x / y MB」。
        两者不会打架 —— `bootstrap`（下载）一定跑在 `ensure_running`（起服务）
        前面，所以等这个信号来的时候，下载早就结束了。

        （之前漏连这个信号，于是不需要下载时那一行永远停在「检查中…」。）
        """
        page = self.loading
        if page is None or launch is None:
            return

        detail = str(getattr(launch, "detail", "") or "")
        row = page.step("ollama")
        if bool(getattr(launch, "ok", False)):
            row.done(
                t(f"loading.detail.ollama_{detail}", default=t("loading.state.ready"))
            )
        else:
            row.failed(
                t(f"settings.rag.ollama_{detail}", default=t("loading.state.failed"))
            )

        # 模型不需要下载时（本来就在该在的目录里），bge 那行没人更新，
        # 顺手在这里收掉，不然它会一直停在灰色的「等待」
        bge = page.step("bge")
        if bge.status == loading_page.PENDING:
            bge.skipped(t("loading.state.installed"))

        page.refresh_progress()

    def _on_boot_progress(self, stage: str, done: int, total: int) -> None:
        page = self.loading
        if page is None:
            return
        if stage in ("downloading", "extracting"):
            self._boot_seen.add(stage)
            page.show_skip(True)
            row = page.step("ollama")
            if stage == "extracting":
                row.start(t("loading.detail.extracting"))
            elif total:
                row.start()
                row.set_progress(done / total, t("loading.detail.downloading",
                                                 done=self._mb(done), total=self._mb(total)))
            else:
                row.start(t("loading.detail.downloading_unknown"))
        elif stage == "pulling":
            self._boot_seen.add(stage)
            page.show_skip(True)
            row = page.step("bge")
            if total:
                row.start()
                row.set_progress(done / total, t("loading.detail.pulling",
                                                 percent=int(done / total * 100),
                                                 done=self._mb(done), total=self._mb(total)))
            else:
                row.start(t("loading.detail.pulling_unknown"))
        page.refresh_progress()

    def _on_boot_ready(self, result) -> None:
        page = self.loading
        if page is None:
            return
        page.show_skip(False)
        ok = bool(getattr(result, "ok", False))
        detail = getattr(result, "detail", "") or ""
        error = getattr(result, "error", "") or ""

        if detail == "cancelled":
            return                      # 用户点的跳过，两行已经标好了
        if ok:
            if "downloading" in self._boot_seen or "extracting" in self._boot_seen:
                page.step("ollama").done(t("loading.state.ready"))
            else:
                page.step("ollama").skipped(t("loading.state.installed"))
            if "pulling" in self._boot_seen:
                page.step("bge").done(t("loading.state.ready"))
            else:
                page.step("bge").skipped(t("loading.state.installed"))
        else:
            # 报错归属：下载阶段失败的算 Ollama，pull 阶段失败的算 bge
            bad = "ollama" if self._boot_seen & {"downloading", "extracting"} else "bge"
            good = "bge" if bad == "ollama" else "ollama"
            page.step(bad).failed(error or t("loading.state.failed"))
            page.step(good).skipped(t("loading.state.ready"))
        page.refresh_progress()

    def _on_sync_progress(self, done: int, total: int, rel: str) -> None:
        page = self.loading
        if page is None:
            return
        row = page.step("index")
        if total:
            row.start()
            row.set_progress(done / total, t("loading.detail.chunks", done=done, total=total))
        elif rel:
            row.start(rel)
        page.refresh_progress()

    def _on_sync_done(self, result) -> None:
        page = self.loading
        if page is None:
            return
        status = getattr(result, "status", "") if result is not None else ""
        row = page.step("index")
        if status == "ok":
            row.done(t("loading.state.ready"))
        else:
            row.skipped(t("loading.state.off"))

        # 兜底：同步都跑完了就说明 Ollama 是能用的，但这两行可能一直挂在
        # 「检查中…」（例如注入了别的 runner，`ollama_ready` 根本不会发）。
        # 收到了真结论就不动它。
        for key in ("ollama", "bge"):
            fallback = page.step(key)
            if fallback.status in (loading_page.PENDING, loading_page.RUNNING):
                fallback.skipped(t("loading.state.ready"))

        page.show_skip(False)
        page.refresh_progress()
        # 语音那一行可能还在下模型，交给 _maybe_complete 判断
        self._maybe_complete()

    # --- 加载页：跳过下载 -----------------------------------------------
    def _on_skip_downloads(self) -> None:
        """用户不想等下载：让后台收手，先把主界面放出来。"""
        page = self.loading
        if page is None:
            return
        from dsai4431_chatbot.core.rag import bootstrap

        bootstrap.cancel()               # 语音模型的下载也走这个取消开关
        page.show_skip(False)
        for key in ("ollama", "bge", "speech"):
            row = page.step(key)
            if row.status in (loading_page.PENDING, loading_page.RUNNING):
                row.skipped(t("loading.state.skipped"))
        page.refresh_progress()
        page.complete()
        # complete() 会把提示换成"即将进入主界面"，所以这句必须放它后面：
        # 用户点了跳过，得看得见"跳过之后去哪儿配"
        page.set_hint(t("loading.skip_done"))

    def _on_loading_closed(self) -> None:
        """加载页收起：解禁主界面。"""
        self._splitter.setEnabled(True)
        page, self.loading = self.loading, None
        if page is not None:
            page.deleteLater()
        if self.chat is not None:
            # 人格/模型清单是加载期间读的，收尾再刷一次更稳
            self.chat.home.refresh()
        self.raise_()
        self.activateWindow()

    def start_rag_sync(self) -> None:
        """后台跑一次差量同步（设置页按钮会调；启动那次走 _startup_rag）。"""
        cfg = chat_config.load()
        if not cfg.rag_enabled:
            return
        self.rag.refresh(cfg)

    def _on_about_to_quit(self) -> None:
        if self.character is not None:
            self.character.shutdown()
        # 只关「本程序自己拉起的」Ollama；用户开着的、系统装的都不碰
        try:
            from dsai4431_chatbot.core.gui import ollama_launcher

            ollama_launcher.stop_owned()
        except Exception as exc:                 # noqa: BLE001 - 收尾逻辑不能挡退出
            print(f"[rag] 关闭自动启动的 Ollama 失败：{exc}", flush=True)

    # --- 会话抽屉 -------------------------------------------------------
    def _place_drawer(self) -> None:
        """抽屉是独立窗口（见 SessionDrawer 里的说明），按主窗口左上角算全局坐标。"""
        if self._drawer is None:
            return
        margin = 12
        top_left = self.mapToGlobal(QPoint(margin, margin))
        self._drawer.move(top_left)
        self._drawer.resize(DRAWER_W, max(260, self.height() - margin * 2))

    def show_drawer(self) -> None:
        if self._drawer is None:
            return
        self._drawer.reload()
        self._place_drawer()
        self._drawer.show()
        self._drawer.raise_()

    def hide_drawer(self) -> None:
        if self._drawer is not None:
            self._drawer.hide()

    def toggle_drawer(self) -> None:
        if self._drawer is None:
            return
        if self._drawer.isVisible():
            self.hide_drawer()
        else:
            self.show_drawer()

    def _on_session_switch(self, session_id: str) -> None:
        """新建或选中会话：把它读进右边聊天区，然后收起抽屉。"""
        if self.chat is None:
            return
        self.chat.open_session(session_id)
        if self._drawer is not None:
            self._drawer.set_current(session_id)
        self.hide_drawer()

    def _on_new_session_requested(self) -> None:
        """抽屉里点「新建对话」：收起抽屉，右侧换成空白首页（此时还不建会话）。"""
        self.hide_drawer()
        if self._drawer is not None:
            self._drawer.set_current("")
        if self.chat is not None:
            self.chat.start_new_conversation()

    def _restore_last_session(self) -> int:
        """启动时自动接上最近更新过的那条对话；返回渲染出的消息条数。

        返回条数是给加载页用的（"已恢复 N 条消息"比一个"完成"更有信息量）。
        """
        if self.chat is None:
            return 0
        sessions = session_store.list_sessions()      # 已按 updated_at 倒序
        if not sessions:
            self.chat.start_new_conversation()
            return 0
        newest = sessions[0]
        self.chat.open_session(newest.id)
        if self._drawer is not None:
            self._drawer.set_current(newest.id)
        return len(self.chat._history)

    def _on_session_updated(self, session_id: str) -> None:
        if self._drawer is not None and self._drawer.isVisible():
            self._drawer.reload()
            self._drawer.set_current(session_id)

    def _on_session_deleted(self, session_id: str) -> None:
        """删掉的正好是当前打开的会话 → 聊天区清空（文件已没了）。"""
        if self.chat is not None and self.chat.current_session_id == session_id:
            self.chat.reset_conversation()

    def resizeEvent(self, event):  # noqa: N802 - Qt 命名
        super().resizeEvent(event)
        # 加载页是覆盖层，不会跟着布局走，得手动同步尺寸
        page = getattr(self, "loading", None)
        body = getattr(self, "_body", None)
        if page is not None and body is not None:
            page.setGeometry(body.rect())
            page.raise_()
        self._fit_character_width()
        if self._drawer is not None and self._drawer.isVisible():
            self._place_drawer()

    def moveEvent(self, event):  # noqa: N802
        super().moveEvent(event)
        if self._drawer is not None and self._drawer.isVisible():
            self._place_drawer()

    def closeEvent(self, event):  # noqa: N802
        if self._drawer is not None:
            self._drawer.close()
        if self.character is not None:
            self.character.shutdown()
        super().closeEvent(event)

    def keyPressEvent(self, event):  # noqa: N802
        if (
            event.key() == Qt.Key.Key_Escape
            and self._drawer is not None
            and self._drawer.isVisible()
        ):
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

        # 加载页还在的时候不该能点到这里（覆盖层已经挡住了，这是第二道保险）
        if self.chat is None or self.character is None:
            return

        dlg = self._settings
        if dlg is not None and dlg.isVisible():
            dlg.raise_()
            dlg.activateWindow()
            return

        dlg = SettingsDialog(self, character=self.character, rag=self.rag)
        dlg.move(
            self.frameGeometry().center() - QPoint(DIALOG_W // 2, DIALOG_H // 2)
        )
        # 人格清单随时可能被改（新建/改名/换目录）：一保存就重读首页的下拉，
        # 不然刚建的人格要等下次切回首页才出现（用户就是这么被卡住的）
        # 注意：首页在 ChatColumn 下面（MainWindow 自己没有 home 属性）
        dlg.personas_changed.connect(self.chat.home.refresh)
        dlg.destroyed.connect(lambda: setattr(self, "_settings", None))
        self._settings = dlg
        dlg.show()


# 单实例锁：拿着不放，进程退出才释放（模块级变量，别让它被回收）
_INSTANCE_LOCK: QLockFile | None = None


def _single_instance_path():
    from dsai4431_chatbot.core.gui import settings_store

    return settings_store.settings_path().parent / "app.lock"


def acquire_single_instance(*, notify: bool = True) -> bool:
    """抢单实例锁；抢不到就弹窗告诉用户并返回 False。

    为什么必须在**所有检测之前**做：两个实例各自都要「接管」Ollama，
    后开的那个会把前一个刚拉起来的 ollama 杀掉，然后前一个的检索就全废。
    与其让它们互相拆台，不如第二个直接不开。

    QLockFile 自带崩溃兜底：锁文件里记着 PID + 主机名，进程没了会被当成
    过期锁清掉，所以上次异常退出不会导致永远打不开。

    `notify=False` 只给测试用（模态框会把无人值守的测试卡死）。
    """
    global _INSTANCE_LOCK
    lock = QLockFile(str(_single_instance_path()))
    if lock.tryLock(200):
        _INSTANCE_LOCK = lock
        return True

    if notify:
        QMessageBox.information(
            None,
            t("app.already_running.title"),
            t("app.already_running.body"),
        )
    return False


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

    # 一切检测之前：已经有窗口开着就直接拒绝（见 acquire_single_instance）
    if not acquire_single_instance():
        return 0

    win = MainWindow()
    win.show()
    return app.exec()


if __name__ == "__main__":
    raise SystemExit(main())

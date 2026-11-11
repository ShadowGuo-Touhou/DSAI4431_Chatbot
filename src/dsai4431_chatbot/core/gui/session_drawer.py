"""会话抽屉：左上角 ≡ 打开的那块面板。

现在只做第 13 条（新建对话 + 列表 + 进入）。改名 / 删除 / 批量删除是第 14、15 条，
后面在这上面接着加。

布局：

    ┌──────────────────────┐
    │ 会话            ×    │
    │ [+ 新建对话]          │
    │ ┌ 新建表单（默认收起）┐│
    │ │ 人格：[✓ 大肥鲸   ] ││
    │ │ 模型：[✓ deepseek…] ││
    │ │      [取消] [创建]  ││
    │ └────────────────────┘│
    │ ── 会话列表 ──        │
    │ 你好，帮我看看… 18:20  │
    │ 赤蛮奇的设定     17:02 │
    └──────────────────────┘
"""

from __future__ import annotations

import time

from PySide6.QtCore import QSize, Qt, Signal
from PySide6.QtWidgets import (
    QComboBox,
    QFrame,
    QHBoxLayout,
    QLabel,
    QListWidget,
    QListWidgetItem,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from dsai4431_chatbot.core.gui import personas, session_store, themes
from dsai4431_chatbot.core.gui.i18n import t

DRAWER_W = 300
ICON = 14


def _when(ms: int) -> str:
    """时间戳 → 「今天 18:20」/「11-10 09:31」这种人话。"""
    if not ms:
        return ""
    local = time.localtime(ms / 1000)
    today = time.localtime()
    if (local.tm_year, local.tm_yday) == (today.tm_year, today.tm_yday):
        return time.strftime("%H:%M", local)
    if local.tm_year == today.tm_year:
        return time.strftime("%m-%d %H:%M", local)
    return time.strftime("%Y-%m-%d", local)


class NewSessionForm(QFrame):
    """新建对话表单：选人格 + 选模型。"""

    submitted = Signal(dict)          # {"persona": dict, "model": str}
    cancelled = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("newSessionForm")
        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)

        lay = QVBoxLayout(self)
        lay.setContentsMargins(12, 12, 12, 12)
        lay.setSpacing(8)

        lay.addWidget(self._label(t("session.persona")))
        self.cbo_persona = QComboBox()
        for persona in personas.list_personas():
            self.cbo_persona.addItem(persona.display, persona.id)
        lay.addWidget(self.cbo_persona)

        lay.addWidget(self._label(t("session.model")))
        self.cbo_model = QComboBox()
        for model in personas.model_options():
            self.cbo_model.addItem(model, model)
        lay.addWidget(self.cbo_model)

        buttons = QHBoxLayout()
        buttons.setSpacing(8)
        buttons.addStretch(1)
        btn_cancel = QPushButton(t("session.cancel"))
        btn_cancel.setObjectName("smallButton")
        btn_cancel.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_cancel.clicked.connect(self.cancelled.emit)
        btn_create = QPushButton(t("session.create"))
        btn_create.setObjectName("smallButton")
        btn_create.setProperty("variant", "primary")
        btn_create.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_create.clicked.connect(self._emit)
        buttons.addWidget(btn_cancel)
        buttons.addWidget(btn_create)
        lay.addLayout(buttons)

    @staticmethod
    def _label(text: str) -> QLabel:
        lab = QLabel(text)
        lab.setObjectName("fieldLabel")
        return lab

    def reset(self) -> None:
        """重开表单时刷新人格清单（用户可能刚在设置里改了 personas.json）。"""
        self.cbo_persona.clear()
        for persona in personas.list_personas():
            self.cbo_persona.addItem(persona.display, persona.id)
        if self.cbo_persona.count():
            self.cbo_persona.setCurrentIndex(0)

    def _emit(self) -> None:
        persona_id = self.cbo_persona.currentData()
        persona = personas.by_id(persona_id) if persona_id else None
        model = self.cbo_model.currentData() or self.cbo_model.currentText()
        self.submitted.emit(
            {
                "persona": persona.as_dict() if persona else {},
                "model": str(model),
            }
        )


class SessionDrawer(QFrame):
    """会话面板（覆盖在窗口左侧，不是 splitter 里的一栏）。"""

    session_created = Signal(str)     # session id
    session_opened = Signal(str)
    close_requested = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("sessionDrawer")
        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)
        self.setFixedWidth(DRAWER_W)
        self._current_id = ""

        lay = QVBoxLayout(self)
        lay.setContentsMargins(12, 14, 12, 14)
        lay.setSpacing(10)

        # --- 标题行 -------------------------------------------------------
        header = QHBoxLayout()
        header.setSpacing(6)
        title = QLabel(t("session.title"))
        title.setObjectName("sectionTitle")
        header.addWidget(title)
        header.addStretch(1)
        self.btn_close = QPushButton()
        self.btn_close.setObjectName("iconButton")
        themes.bind(self.btn_close, "close")
        self.btn_close.setIconSize(QSize(ICON, ICON))
        self.btn_close.setFixedSize(26, 26)
        self.btn_close.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_close.setToolTip(t("session.close"))
        self.btn_close.clicked.connect(self.close_requested.emit)
        header.addWidget(self.btn_close)
        lay.addLayout(header)

        # --- 新建 ---------------------------------------------------------
        self.btn_new = QPushButton(t("session.new"))
        self.btn_new.setObjectName("smallButton")
        self.btn_new.setProperty("variant", "primary")
        self.btn_new.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_new.clicked.connect(self.toggle_form)
        lay.addWidget(self.btn_new)

        self.form = NewSessionForm()
        self.form.hide()
        self.form.submitted.connect(self._on_create)
        self.form.cancelled.connect(self.toggle_form)
        lay.addWidget(self.form)

        # --- 列表 ---------------------------------------------------------
        self.list = QListWidget()
        self.list.setObjectName("sessionList")
        self.list.setFrameShape(QFrame.Shape.NoFrame)
        self.list.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.list.itemDoubleClicked.connect(self._on_double_click)
        self.list.itemActivated.connect(self._on_double_click)
        lay.addWidget(self.list, 1)

        self.lb_empty = QLabel(t("session.empty"))
        self.lb_empty.setObjectName("hintText")
        self.lb_empty.setAlignment(Qt.AlignmentFlag.AlignCenter)
        lay.addWidget(self.lb_empty)

        self.reload()

    # --- 数据 -----------------------------------------------------------
    def reload(self) -> None:
        """重新读列表（新建/改名/删除之后都要调）。"""
        self.list.clear()
        sessions = session_store.list_sessions()
        for meta in sessions:
            item = QListWidgetItem()
            item.setData(Qt.ItemDataRole.UserRole, meta.id)
            item.setText(f"{meta.display_title}")
            bits = [_when(meta.updated_at or meta.created_at)]
            if meta.persona_label:
                bits.append(meta.persona_label)
            if meta.model:
                bits.append(meta.model)
            item.setToolTip(" · ".join(b for b in bits if b))
            item.setSizeHint(QSize(0, 26))
            self.list.addItem(item)
            if meta.id == self._current_id:
                self.list.setCurrentItem(item)

        self.lb_empty.setVisible(not sessions)
        self.list.setVisible(bool(sessions))

    def set_current(self, session_id: str) -> None:
        self._current_id = session_id or ""
        for row in range(self.list.count()):
            item = self.list.item(row)
            if item.data(Qt.ItemDataRole.UserRole) == self._current_id:
                self.list.setCurrentItem(item)
                break

    # --- 新建 -----------------------------------------------------------
    def toggle_form(self) -> None:
        visible = not self.form.isVisible()
        if visible:
            self.form.reset()
        self.form.setVisible(visible)
        self.btn_new.setText(t("session.cancel_new") if visible else t("session.new"))

    def _on_create(self, payload: dict) -> None:
        meta = session_store.create_session(
            persona=payload.get("persona") or {},
            model=str(payload.get("model") or ""),
        )
        self.toggle_form() if self.form.isVisible() else None
        self._current_id = meta.id
        self.reload()
        self.session_created.emit(meta.id)

    # --- 打开 -----------------------------------------------------------
    def _on_double_click(self, item: QListWidgetItem) -> None:
        session_id = item.data(Qt.ItemDataRole.UserRole)
        if session_id:
            self._open(str(session_id))

    def _open(self, session_id: str) -> None:
        self._current_id = session_id
        self.reload()
        self.session_opened.emit(session_id)

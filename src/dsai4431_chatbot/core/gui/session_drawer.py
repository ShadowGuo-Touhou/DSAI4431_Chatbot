"""会话抽屉：左上角 ≡ 打开的那块面板。

只负责「列出会话 + 打开 / 改名 / 删除 / 批量删除」。「新建对话」不再在这里
展开小表单（选人格、选模型、取消/创建），而是把右侧聊天列整块换成新对话页
（见 main_window.HomePage）—— 人格、模型、输入框都在那一页上，全程序只有
一条创建路径，不会出现两套行为。

布局：

    ┌──────────────────────┐
    │ 会话         [选择] × │
    │ [＋ 新建对话]          │
    │ ── 会话列表 ──        │
    │ 你好，帮我看看… 18:20  │
    │ 赤蛮奇的设定     17:02 │
    └──────────────────────┘
"""

from __future__ import annotations

import time

from PySide6.QtCore import QSize, Qt, Signal
from PySide6.QtWidgets import (
    QFrame,
    QHBoxLayout,
    QInputDialog,
    QLabel,
    QListWidget,
    QListWidgetItem,
    QMenu,
    QMessageBox,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from dsai4431_chatbot.core.gui import session_store, themes
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


class SessionDrawer(QFrame):
    """会话面板（覆盖在窗口左侧，不是 splitter 里的一栏）。"""

    new_session_requested = Signal()  # 点「＋ 新建对话」：由 MainWindow 切到新对话页
    session_opened = Signal(str)
    session_deleted = Signal(str)
    close_requested = Signal()

    def __init__(self, parent=None):
        # 独立窗口（Qt.Tool + 无边框）：QWebEngineView 是原生子窗口，
        # 会把同级的 Qt 控件盖住，raise_() 也没用 —— 只能让它当独立窗口浮在上面
        super().__init__(parent)
        self.setObjectName("sessionDrawer")
        self.setWindowFlags(
            Qt.WindowType.Tool | Qt.WindowType.FramelessWindowHint
        )
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
        self.btn_select = QPushButton(t("session.select"))
        self.btn_select.setObjectName("smallButton")
        self.btn_select.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_select.clicked.connect(lambda: self.toggle_select_mode())
        header.addWidget(self.btn_select)
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
        # 这里只发信号：真正的新对话页在右侧聊天列里，由 MainWindow 切过去。
        # 好处是「唯一创建路径」—— 人格/模型/输入框都在那一页，不会有两套行为。
        self.btn_new = QPushButton(t("session.new"))
        self.btn_new.setObjectName("smallButton")
        self.btn_new.setProperty("variant", "primary")
        self.btn_new.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_new.clicked.connect(self.new_session_requested.emit)
        lay.addWidget(self.btn_new)

        # --- 列表 ---------------------------------------------------------
        self.list = QListWidget()
        self.list.setObjectName("sessionList")
        self.list.setFrameShape(QFrame.Shape.NoFrame)
        self.list.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.list.itemDoubleClicked.connect(self._on_double_click)
        self.list.itemActivated.connect(self._on_double_click)
        self.list.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.list.customContextMenuRequested.connect(self._on_context_menu)
        self.list.itemChanged.connect(self._on_item_changed)
        lay.addWidget(self.list, 1)

        self.lb_empty = QLabel(t("session.empty"))
        self.lb_empty.setObjectName("hintText")
        self.lb_empty.setAlignment(Qt.AlignmentFlag.AlignCenter)
        lay.addWidget(self.lb_empty)

        # --- 批量选择（第 15 条）------------------------------------------
        self.select_bar = QWidget()
        sel_lay = QVBoxLayout(self.select_bar)
        sel_lay.setContentsMargins(0, 0, 0, 0)
        sel_lay.setSpacing(6)

        row = QHBoxLayout()
        row.setSpacing(6)
        self.btn_select_all = QPushButton(t("session.select_all"))
        self.btn_select_all.setObjectName("smallButton")
        self.btn_select_all.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_select_all.clicked.connect(self._on_select_all_clicked)
        self.lb_count = QLabel("")
        self.lb_count.setObjectName("hintText")
        row.addWidget(self.btn_select_all)
        row.addWidget(self.lb_count)
        row.addStretch(1)
        sel_lay.addLayout(row)

        self.btn_delete_sel = QPushButton(t("session.delete_selected", n=0))
        self.btn_delete_sel.setObjectName("smallButton")
        self.btn_delete_sel.setProperty("variant", "primary")
        self.btn_delete_sel.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_delete_sel.setEnabled(False)
        self.btn_delete_sel.clicked.connect(self.ask_delete_selected)
        sel_lay.addWidget(self.btn_delete_sel)

        self.select_bar.hide()
        lay.addWidget(self.select_bar)

        self._selecting = False
        self._loading = False
        self.reload()

    # --- 数据 -----------------------------------------------------------
    def reload(self) -> None:
        """重新读列表（新建/改名/删除之后都要调）。"""
        self._loading = True              # 建列表时 itemChanged 的噪声不要当真
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
            if self._selecting:
                item.setFlags(item.flags() | Qt.ItemFlag.ItemIsUserCheckable)
                item.setCheckState(Qt.CheckState.Unchecked)
            self.list.addItem(item)
            if meta.id == self._current_id:
                self.list.setCurrentItem(item)

        self.lb_empty.setVisible(not sessions)
        self.list.setVisible(bool(sessions))
        self._loading = False
        self._update_select_ui()

    def set_current(self, session_id: str) -> None:
        self._current_id = session_id or ""
        hit = False
        for row in range(self.list.count()):
            item = self.list.item(row)
            if item.data(Qt.ItemDataRole.UserRole) == self._current_id:
                self.list.setCurrentItem(item)
                hit = True
                break
        if not hit:
            # 「新建对话」之后列表不该还高亮着上一条
            self.list.clearSelection()

    # --- 打开 -----------------------------------------------------------
    def _on_double_click(self, item: QListWidgetItem | None) -> None:
        """双击列表项 = 打开这条会话。

        `itemActivated` 也会走到这里，而它**没有选中项时会传 None**
        （双击空白处、或焦点在列表上按回车），不判空就是
        `AttributeError: 'NoneType' object has no attribute 'data'` —— 实测崩过。
        """
        if item is None:
            return
        session_id = item.data(Qt.ItemDataRole.UserRole)
        if session_id:
            self._open(str(session_id))

    def _open(self, session_id: str) -> None:
        self._current_id = session_id
        self.reload()
        self.session_opened.emit(session_id)

    # --- 右键：重命名 / 删除（第 14 条）---------------------------------
    def _on_context_menu(self, pos) -> None:
        item = self.list.itemAt(pos)
        if item is None:
            return
        session_id = item.data(Qt.ItemDataRole.UserRole)
        if not session_id:
            return
        menu = QMenu(self)
        act_rename = menu.addAction(t("session.rename"))
        act_delete = menu.addAction(t("session.delete"))
        chosen = menu.exec(self.list.viewport().mapToGlobal(pos))
        if chosen is act_rename:
            self.ask_rename(str(session_id))
        elif chosen is act_delete:
            self.ask_delete(str(session_id))

    def ask_rename(self, session_id: str) -> None:
        meta = session_store.get_meta(session_id)
        if meta is None:
            return
        text, accepted = QInputDialog.getText(
            self, t("session.rename_title"), t("session.rename_title"), text=meta.title
        )
        if accepted:
            self.do_rename(session_id, text)

    def do_rename(self, session_id: str, title: str) -> None:
        if session_store.rename_session(session_id, title) is not None:
            self.reload()

    def ask_delete(self, session_id: str) -> None:
        meta = session_store.get_meta(session_id)
        name = meta.display_title if meta is not None else session_id
        if self._confirm(t("session.delete_ask", name=name)):
            self.do_delete(session_id)

    def do_delete(self, session_id: str) -> bool:
        if not session_store.delete_session(session_id):
            return False
        if session_id == self._current_id:
            self._current_id = ""
        self.reload()
        self.session_deleted.emit(session_id)
        return True

    def _confirm(self, text: str) -> bool:
        box = QMessageBox(self)
        box.setIcon(QMessageBox.Icon.Warning)
        box.setWindowTitle(t("session.delete_title"))
        box.setText(text)
        ok_btn = box.addButton(t("common.ok"), QMessageBox.ButtonRole.DestructiveRole)
        box.addButton(t("common.cancel"), QMessageBox.ButtonRole.RejectRole)
        box.exec()
        return box.clickedButton() is ok_btn

    # --- 批量删除（第 15 条）--------------------------------------------
    def toggle_select_mode(self, on: bool | None = None) -> None:
        self._selecting = (not self._selecting) if on is None else bool(on)
        self.btn_select.setText(
            t("session.select_done") if self._selecting else t("session.select")
        )
        self.select_bar.setVisible(self._selecting)
        if not self._selecting:
            self.btn_delete_sel.setEnabled(False)
        self.reload()

    def _on_item_changed(self, _item) -> None:
        if self._loading or not self._selecting:
            return
        self._update_select_ui()

    def selected_ids(self) -> list[str]:
        picked: list[str] = []
        for row in range(self.list.count()):
            item = self.list.item(row)
            if item.checkState() == Qt.CheckState.Checked:
                session_id = item.data(Qt.ItemDataRole.UserRole)
                if session_id:
                    picked.append(str(session_id))
        return picked

    def select_all(self, on: bool = True) -> None:
        self._loading = True
        state = Qt.CheckState.Checked if on else Qt.CheckState.Unchecked
        for row in range(self.list.count()):
            self.list.item(row).setCheckState(state)
        self._loading = False
        self._update_select_ui()

    def _on_select_all_clicked(self) -> None:
        total = self.list.count()
        self.select_all(len(self.selected_ids()) < total)

    def _update_select_ui(self) -> None:
        if not self._selecting:
            return
        total = self.list.count()
        count = len(self.selected_ids())
        self.lb_count.setText(f"{count}/{total}")
        self.btn_delete_sel.setText(t("session.delete_selected", n=count))
        self.btn_delete_sel.setEnabled(count > 0)
        all_picked = total > 0 and count == total
        self.btn_select_all.setText(
            t("session.select_none") if all_picked else t("session.select_all")
        )

    def ask_delete_selected(self) -> None:
        ids = self.selected_ids()
        if not ids:
            return
        if self._confirm(t("session.delete_many_ask", n=len(ids))):
            self.delete_selected()

    def delete_selected(self) -> int:
        """删掉勾选的那些；删完退出选择模式。"""
        removed = 0
        for session_id in self.selected_ids():
            if session_id == self._current_id:
                self._current_id = ""
            if session_store.delete_session(session_id):
                removed += 1
                self.session_deleted.emit(session_id)
        self.toggle_select_mode(False)
        return removed

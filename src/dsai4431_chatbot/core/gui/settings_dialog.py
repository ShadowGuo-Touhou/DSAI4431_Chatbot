"""设置窗口：三个分页的**纯布局**实现。

对照三张手绘线框（asset/plan/setting-*.png，需顺时针旋转 90° 阅读）：

    左侧竖排导航               右侧内容区
    ┌──────────────┬──────────────────────────────────────┐
    │ API KEY      │  标题                                │
    │ Personality  │  若干字段 / 列表 / 按钮                │
    │ RAG          │                                      │
    │ Other        │                                      │
    └──────────────┴──────────────────────────────────────┘

本文件只做布局，**不接任何业务逻辑**：所有按钮都是空壳，点了没反应；
唯一连接的是左侧导航切换分页（否则看不到别的页面）。

草图里的矛盾：RAG 那张图第 4 个 tab 写的是「Live2D model」，
API KEY 和 Personality 两张图写的是「Other」。这里按出现两次的 Other 实现，
第四页留空，等确认。
"""

from __future__ import annotations

from pathlib import Path

from PySide6.QtCore import QEvent, QSize, QSignalBlocker, Qt, QUrl, Signal
from PySide6.QtGui import QColor, QDesktopServices, QFont
from PySide6.QtWidgets import (
    QApplication,
    QButtonGroup,
    QCheckBox,
    QComboBox,
    QDialog,
    QFileDialog,
    QFrame,
    QGraphicsDropShadowEffect,
    QGridLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QListWidget,
    QListWidgetItem,
    QMessageBox,
    QPlainTextEdit,
    QPushButton,
    QScrollArea,
    QSlider,
    QDoubleSpinBox,
    QSpinBox,
    QStackedWidget,
    QVBoxLayout,
    QWidget,
)

from dsai4431_chatbot.core.gui import (
    chat_config,
    i18n,
    live2d_embed,
    personas,
    relaunch,
    theme,
    themes,
)
from dsai4431_chatbot.core.gui.i18n import t

SHADOW = 18  # 圆角窗外留给投影的透明边距（窗口本身比可见卡片大一圈）
DIALOG_W, DIALOG_H = 980 + 2 * SHADOW, 660 + 2 * SHADOW
NAV_W = 172
ICON = 16

# 人格默认勾选：和对话配置用同一份定义（chat_config），别再各写一套
# 目录本身由 personas.personality_dir() 决定（<data>/personality）
PERSONA_DEFAULT_CHECKED = set(chat_config.DEFAULT_PERSONA_FILES)


# ---------------------------------------------------------------------------
# 小部件工厂（只为了少写重复代码，不含逻辑）
# ---------------------------------------------------------------------------
def field_label(text: str) -> QLabel:
    lab = QLabel(text)
    lab.setObjectName("fieldLabel")
    return lab


def field_input(placeholder: str = "") -> QLineEdit:
    edit = QLineEdit()
    edit.setObjectName("field")
    edit.setPlaceholderText(placeholder)
    return edit


def field_list(items: list[str] | None = None, min_height: int = 0) -> QListWidget:
    lst = QListWidget()
    lst.setObjectName("fieldList")
    if items:
        lst.addItems(items)
    if min_height:
        lst.setMinimumHeight(min_height)
    return lst


def scan_persona_files(directory: Path) -> list[tuple[str, int]]:
    """扫描人格目录下的 .md，返回 [(文件名, 字符数)]；目录不在就返回空表。"""
    return personas.scan_files(directory)


class FileCheckList(QScrollArea):
    """文件清单：每行 = 勾选框（文件名）+ 右侧字符数，**可滚动**。

    勾选结果会发 `changed`（set[str]），由 Personality 页存进配置 ——
    勾了哪些文件，对话时就把哪些文件拼成 system 提示词。

    为什么是 QScrollArea 而不是 QFrame：人格目录里文件数不固定（实测 6 个就
    顶出卡片了），用 QFrame 排会直接被裁掉、下面的文件点不到。box 外观
    （底色/描边/圆角）画在滚动区上，滚动条因此落在框内。
    """

    changed = Signal(object)          # set[str]

    def __init__(
        self,
        rows: list[tuple[str, int]],
        checked: set[str] | None = None,
        parent=None,
    ):
        super().__init__(parent)
        self.setObjectName("fileListScroll")
        self.setWidgetResizable(True)
        self.setFrameShape(QFrame.Shape.NoFrame)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)

        self.boxes: dict[str, QCheckBox] = {}
        self._building = False
        self._editable = True          # set_editable() 会改；set_rows 重建时要照旧

        # 滚动内容：透明容器，行都挂在它下面（QSS 用 #fileList > #fileRow 选中）
        self._body = QFrame()
        self._body.setObjectName("fileList")
        self._body.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)
        self._lay = QVBoxLayout(self._body)
        self._lay.setContentsMargins(6, 6, 6, 6)
        self._lay.setSpacing(1)
        self.setWidget(self._body)

        self.set_rows(rows, checked)

    # --- 内容 -----------------------------------------------------------
    def set_rows(self, rows: list[tuple[str, int]], checked: set[str] | None = None) -> None:
        """重建列表（换目录后重新扫描时用）。"""
        self._building = True
        while self._lay.count():
            item = self._lay.takeAt(0)
            widget = item.widget()
            if widget is not None:
                # 先摘掉父子关系再 deleteLater：只标 deleteLater 的话，旧行要等
                # 事件循环处理 DeferredDelete 才消失，这期间会和新行**叠在一起**
                # 被画出来（实测截图里两行文字糊成一团）。
                widget.setParent(None)
                widget.deleteLater()
        self.boxes.clear()

        names = checked if checked is not None else PERSONA_DEFAULT_CHECKED
        for name, chars in rows:
            row = QFrame()
            row.setObjectName("fileRow")
            row.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)
            row_lay = QHBoxLayout(row)
            row_lay.setContentsMargins(6, 3, 10, 3)
            row_lay.setSpacing(8)

            box = QCheckBox(name)
            box.setObjectName("fileCheck")
            box.setChecked(name in names)
            box.setEnabled(self._editable)
            box.setCursor(Qt.CursorShape.PointingHandCursor)
            box.toggled.connect(self._on_toggled)
            self.boxes[name] = box

            size = QLabel(t("common.chars", n=f"{chars:,}"))
            size.setObjectName("fileSize")

            row_lay.addWidget(box, 1)
            row_lay.addWidget(size)
            self._lay.addWidget(row)

        self._lay.addStretch(1)
        self._building = False

    def checked_names(self) -> set[str]:
        return {name for name, box in self.boxes.items() if box.isChecked()}

    def set_editable(self, editable: bool) -> None:
        """整体锁/解锁勾选（默认人格那套文件是固定的，不让改）。

        锁住的状态要记住：set_rows() 会把行全部重建，重建时要照旧上锁。
        """
        self._editable = bool(editable)
        for box in self.boxes.values():
            box.setEnabled(self._editable)

    def _on_toggled(self, _on: bool) -> None:
        if self._building:          # 建列表时 setChecked 的噪声不要往外发
            return
        self.changed.emit(self.checked_names())


def small_button(text: str, *, primary: bool = False) -> QPushButton:
    btn = QPushButton(text)
    btn.setObjectName("smallButton")
    if primary:
        btn.setProperty("variant", "primary")
    btn.setCursor(Qt.CursorShape.PointingHandCursor)
    return btn


def icon_button(icon: str, tooltip: str) -> QPushButton:
    btn = QPushButton()
    btn.setObjectName("iconButton")
    themes.bind(btn, icon)          # 换肤时自动重新上色
    btn.setIconSize(QSize(ICON, ICON))
    btn.setFixedSize(34, 34)
    btn.setCursor(Qt.CursorShape.PointingHandCursor)
    btn.setToolTip(tooltip)
    return btn


def page_title(text: str) -> QLabel:
    lab = QLabel(text)
    lab.setObjectName("pageTitle")
    return lab


def section_title(text: str) -> QLabel:
    lab = QLabel(text)
    lab.setObjectName("sectionTitle")
    return lab


def card() -> tuple[QFrame, QVBoxLayout]:
    """带描边的卡片容器。"""
    frame = QFrame()
    frame.setObjectName("surface")
    frame.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)
    lay = QVBoxLayout(frame)
    lay.setContentsMargins(16, 14, 16, 14)
    lay.setSpacing(8)
    return frame, lay


# ---------------------------------------------------------------------------
# 三个分页
# ---------------------------------------------------------------------------
class ApiKeyPage(QWidget):
    """API KEY 页：API 地址 / Key / 模型。

    草图只有「API」「Token」两个字段；模型名是本项目加的（不填就默认
    deepseek-flash，要换 deepseek-v4-pro 或者自定义网关时得有个地方写）。

    改完**自动存**进 settings.ini（和换肤、Live2D 一样的做法），没有"保存"按钮。
    """

    def __init__(self, parent=None):
        super().__init__(parent)
        self._cfg = chat_config.load()

        lay = QVBoxLayout(self)
        lay.setContentsMargins(28, 24, 28, 24)
        lay.setSpacing(10)

        lay.addWidget(page_title(t("settings.api_key.title")))
        lay.addSpacing(6)

        lay.addWidget(field_label(t("settings.api_key.api")))
        self.ed_base = field_input(t("settings.api_key.api_placeholder"))
        self.ed_base.setText(self._cfg.base_url)
        self.ed_base.editingFinished.connect(self.save)
        lay.addWidget(self.ed_base)

        lay.addSpacing(6)
        lay.addWidget(field_label(t("settings.api_key.token")))
        self.ed_key = field_input(t("settings.api_key.token_placeholder"))
        self.ed_key.setEchoMode(QLineEdit.EchoMode.Password)   # 别开着窗口就把 Key 晾在屏幕上
        self.ed_key.setText(self._cfg.api_key)
        self.ed_key.editingFinished.connect(self.save)
        lay.addWidget(self.ed_key)

        lay.addSpacing(6)
        lay.addWidget(field_label(t("settings.api_key.model")))
        self.ed_model = field_input(t("settings.api_key.model_placeholder"))
        self.ed_model.setText(self._cfg.model)
        self.ed_model.editingFinished.connect(self.save)
        lay.addWidget(self.ed_model)

        hint = QLabel(t("settings.api_key.key_hint"))
        hint.setObjectName("hintText")
        hint.setWordWrap(True)
        lay.addWidget(hint)

        lay.addStretch(1)

    def save(self) -> None:
        # 现读再改自己那几个字段：三个页面共用一份配置，谁都不能拿构造时的
        # 旧快照整体写回去（否则会把别的页刚存的值覆盖掉 —— 实测踩过）
        cfg = chat_config.load()
        cfg.base_url = self.ed_base.text().strip() or chat_config.DEFAULT_BASE_URL
        cfg.api_key = self.ed_key.text().strip()
        cfg.model = self.ed_model.text().strip() or chat_config.DEFAULT_MODEL
        chat_config.save(cfg)


class _TextDialog(QDialog):
    """只读文本窗（Preview 用）：可滚动、可复制。

    以前直接弹 QMessageBox.information —— 提示框不能滚，提示词一长就只能
    看到开头那几行。
    """

    def __init__(self, title: str, body: str, parent=None):
        super().__init__(parent)
        self.setWindowTitle(title)
        self.resize(760, 540)

        lay = QVBoxLayout(self)
        lay.setContentsMargins(18, 16, 18, 14)
        lay.setSpacing(10)

        view = QPlainTextEdit(body)
        view.setObjectName("field")
        view.setReadOnly(True)
        view.setLineWrapMode(QPlainTextEdit.LineWrapMode.WidgetWidth)
        # QPlainTextEdit 的正文用的是文档默认字体，QSS 只改控件字体、改不到文档，
        # 不显式设一遍会渲染成宋体（和界面其它地方不一致）
        doc_font = QFont("Microsoft YaHei UI")
        doc_font.setPixelSize(14)
        view.setFont(doc_font)
        view.document().setDefaultFont(doc_font)
        lay.addWidget(view, 1)

        row = QHBoxLayout()
        info = QLabel(t("settings.personality.preview_chars", n=f"{len(body):,}"))
        info.setObjectName("hintText")
        row.addWidget(info, 1)
        btn = small_button(t("common.ok"), primary=True)
        btn.clicked.connect(self.accept)
        row.addWidget(btn)
        lay.addLayout(row)

        view.setFocus()


class PersonalityPage(QWidget):
    """人格编辑页：左「Persona 列表」、右表单。

    这一页是人格清单的**唯一入口**，真正读写 `<data>/personality/personas.json`：
    左边列出清单里所有启用的人格，点一个就载进右边；右边改显示名、换目录、
    勾要注入的 .md，按 Save 写回清单。新建会话时下拉里看到的就是这些人格。

    id 建好就不许改（和 DSH 那个插件一致）：它会被用来命名记忆库等文件，
    改名等于新建一条。
    """

    saved = Signal()               # 写进清单了（主窗拿去刷新首页的人格下拉）

    def __init__(self, parent=None):
        super().__init__(parent)
        self._persona_id = ""      # 正在编辑哪一条；空 = 新建中
        self._order = 0
        # 新建时目录跟着 ID 走：<人格根目录>/<id>，用户自己挑过就不跟了
        self._dir_follows_id = True
        # 正在看默认人格（大肥鱼）时为 True：表单全锁、不能存也不能删
        self._readonly = False

        lay = QVBoxLayout(self)
        lay.setContentsMargins(28, 24, 28, 24)
        lay.setSpacing(14)

        lay.addWidget(page_title(t("settings.personality.title")))

        body = QHBoxLayout()
        body.setSpacing(16)

        # --- 左：Persona 列表 -------------------------------------------
        left_card, left = card()
        left.setSpacing(8)
        left.addWidget(section_title(t("settings.personality.list")))
        self.list_personas = field_list(min_height=90)
        self.list_personas.currentRowChanged.connect(self._on_row_changed)
        left.addWidget(self.list_personas, 1)

        list_btns = QHBoxLayout()
        list_btns.setSpacing(8)
        btn_new = small_button(t("settings.personality.new_button"))
        btn_new.clicked.connect(lambda: self._new())
        self.btn_del = small_button(t("settings.personality.delete_button"))
        self.btn_del.clicked.connect(lambda: self._delete())
        list_btns.addWidget(btn_new)
        list_btns.addWidget(self.btn_del)
        list_btns.addStretch(1)
        left.addLayout(list_btns)
        left_card.setFixedWidth(260)
        body.addWidget(left_card)

        # --- 右：表单 ---------------------------------------------------
        right_card, right = card()
        right.addWidget(section_title(t("settings.personality.new_title")))

        right.addWidget(field_label(t("settings.personality.id")))
        self.ed_id = field_input(t("settings.personality.id_placeholder"))
        self.ed_id.textEdited.connect(self._on_id_edited)
        right.addWidget(self.ed_id)

        right.addWidget(field_label(t("settings.personality.name")))
        self.ed_name = field_input(t("settings.personality.name_placeholder"))
        right.addWidget(self.ed_name)

        right.addWidget(field_label(t("settings.personality.files")))
        self.ed_dir = field_input(t("settings.personality.files_placeholder"))
        self.ed_dir.editingFinished.connect(lambda: self._on_dir_edited())
        right.addWidget(self.ed_dir)

        path_row = QHBoxLayout()
        path_row.setSpacing(8)
        # 两种都给：直接选文件夹，或者点一个 .md 文件（取它所在目录）。
        # 单靠「打开文件」会逼着用户必须先挑一个 .md，单靠「选文件夹」
        # 又看不见目录里有哪些文件 —— 两个按钮各管一种，都是系统原生对话框。
        self.btn_pick_dir = small_button(t("settings.personality.choose_dir"))
        self.btn_pick_dir.clicked.connect(lambda: self._pick_dir())
        self.btn_pick_file = small_button(t("settings.personality.choose_file"))
        self.btn_pick_file.clicked.connect(lambda: self._pick_file())
        self.btn_rescan = small_button(t("settings.personality.rescan"))
        self.btn_rescan.clicked.connect(lambda: self._rescan())
        path_row.addWidget(self.btn_pick_dir)
        path_row.addWidget(self.btn_pick_file)
        path_row.addWidget(self.btn_rescan)
        path_row.addStretch(1)
        right.addLayout(path_row)

        self.lb_dir_state = QLabel("")
        self.lb_dir_state.setObjectName("hintText")
        self.lb_dir_state.setWordWrap(True)
        right.addWidget(self.lb_dir_state)

        right.addWidget(field_label(t("settings.personality.file_list")))
        # 先建空的，内容交给 _rescan() 填
        self.file_list = FileCheckList([], checked=set())
        self.file_list.changed.connect(self._on_files_changed)
        right.addWidget(self.file_list, 1)

        footer = QHBoxLayout()
        self.lb_status = QLabel("")
        self.lb_status.setObjectName("hintText")
        footer.addWidget(self.lb_status, 1)
        btn_preview = small_button(t("settings.personality.preview"))
        btn_preview.clicked.connect(lambda: self._preview())
        self.btn_save = small_button(t("settings.personality.save"), primary=True)
        self.btn_save.clicked.connect(lambda: self.save())
        footer.addWidget(btn_preview)
        footer.addWidget(self.btn_save)
        right.addLayout(footer)

        body.addWidget(right_card, 1)
        lay.addLayout(body, 1)

        self.refresh()

    # --- 列表 -----------------------------------------------------------
    def refresh(self, select_id: str = "") -> None:
        """重读清单并重画左边的列表。"""
        items = personas.list_personas()
        self.list_personas.blockSignals(True)
        self.list_personas.clear()
        for item in items:
            row = QListWidgetItem(item.display)
            row.setData(Qt.ItemDataRole.UserRole, item.id)
            row.setToolTip(f"{item.id} · {item.path()}")
            self.list_personas.addItem(row)
        self.list_personas.blockSignals(False)

        wanted = select_id or self._persona_id
        for index in range(self.list_personas.count()):
            row = self.list_personas.item(index)
            if str(row.data(Qt.ItemDataRole.UserRole)) == wanted:
                self.list_personas.setCurrentRow(index)
                return
        if self.list_personas.count():
            self.list_personas.setCurrentRow(0)
        else:
            self._clear_form()

    def _on_row_changed(self, index: int) -> None:
        row = self.list_personas.item(index)
        if row is None:
            return
        found = personas.by_id(str(row.data(Qt.ItemDataRole.UserRole)))
        if found is not None:
            self._load(found)

    def _load(self, persona: personas.Persona) -> None:
        self._persona_id = persona.id
        self._order = persona.order
        self._dir_follows_id = False
        self.ed_id.setText(persona.id)
        self.ed_id.setReadOnly(True)
        self.ed_name.setText(persona.label)
        self.ed_dir.setText(str(persona.path()))
        self._rescan(checked=set(persona.files))
        self._set_readonly(persona.readonly)
        if persona.readonly:
            self.lb_status.setText(t("settings.personality.default_locked"))
        else:
            self.lb_status.setText("")

    def _set_readonly(self, locked: bool) -> None:
        """默认人格「大肥鱼」是固定的：名字/目录/勾选/保存/删除全都锁住。"""
        self._readonly = locked
        self.ed_name.setReadOnly(locked)
        self.ed_dir.setReadOnly(locked)
        self.btn_pick_dir.setEnabled(not locked)
        self.btn_pick_file.setEnabled(not locked)
        self.btn_rescan.setEnabled(not locked)
        self.btn_save.setEnabled(not locked)
        self.btn_del.setEnabled(not locked)
        self.file_list.set_editable(not locked)

    def _clear_form(self) -> None:
        self._persona_id = ""
        self._order = 0
        self._dir_follows_id = True
        self.ed_id.setReadOnly(False)
        self.ed_id.clear()
        self.ed_name.clear()
        self.ed_dir.setText(str(personas.personality_dir()))
        self._rescan(checked=set())
        self._set_readonly(False)
        self.lb_status.setText("")

    def _on_id_edited(self, text: str) -> None:
        """新建时目录跟着 ID 走（`<人格根目录>/<id>`），用户自己挑过就不跟。"""
        if not self._dir_follows_id:
            return
        name = text.strip()
        root = personas.personality_dir()
        self.ed_dir.setText(str(root / name) if name else str(root))

    def _on_dir_edited(self) -> None:
        """用户手改了路径：说明他想自己指目录，别再跟着 ID 覆盖他。"""
        self._dir_follows_id = False
        self._rescan()

    # --- 按钮 -----------------------------------------------------------
    def _new(self) -> None:
        # 用 -1 而不是 clearSelection()：currentRow 不清掉的话，用户再点
        # 原来那一行不会有 currentRowChanged，表单就停在"新建"状态不动
        self.list_personas.setCurrentRow(-1)
        self._clear_form()
        self.ed_id.setFocus()

    def _dir(self) -> Path:
        raw = self.ed_dir.text().strip()
        return Path(raw).expanduser() if raw else personas.personality_dir()

    def _pick_dir(self) -> None:
        """直接选文件夹（系统原生「选择文件夹」对话框）。"""
        chosen = QFileDialog.getExistingDirectory(
            self, t("settings.personality.files"), str(self._dir())
        )
        if not chosen:
            return
        self.ed_dir.setText(chosen)
        self._dir_follows_id = False      # 自己挑过了，别再跟着 ID 跑
        self._rescan()

    def _pick_file(self) -> None:
        """点一个 .md，取它所在目录当人格目录。

        这条的好处是对话框里能看见目录中有哪些 .md；系统原生「选文件夹」
        模式会把文件整个隐藏（IFileDialog 的 FOS_PICKFOLDERS），过滤参数
        也传不进去，目录看着像空的。
        """
        chosen, _flt = QFileDialog.getOpenFileName(
            self,
            t("settings.personality.files"),
            str(self._dir()),
            t("settings.personality.file_filter"),
        )
        if not chosen:
            return
        self.ed_dir.setText(str(Path(chosen).parent))
        self._dir_follows_id = False
        self._rescan()

    def _rescan(self, checked: set[str] | None = None) -> None:
        directory = self._dir()
        rows = personas.scan_files(directory)
        if checked is None:
            keep = {name for name, _ in rows}
            checked = self.file_list.checked_names() & keep
        self.file_list.set_rows(rows, checked=checked)
        if directory.is_dir():
            self.lb_dir_state.setText(t("settings.personality.dir_ok", n=len(rows)))
        else:
            self.lb_dir_state.setText(
                t("settings.personality.dir_missing", path=str(directory))
            )

    def _on_files_changed(self, _names) -> None:
        self.lb_status.setText(t("settings.personality.unsaved"))

    def _selected_files(self) -> list[str]:
        return sorted(self.file_list.checked_names())

    # --- 存盘 -----------------------------------------------------------
    def save(self) -> bool:
        """校验 + 写这一条定义（一个 id 一份 json）。返回是否真的写进去了。"""
        if self._readonly:
            self._complain(t("settings.personality.err_default_locked"))
            return False
        persona_id = self.ed_id.text().strip()
        label = self.ed_name.text().strip()
        if not persona_id:
            self._complain(t("settings.personality.err_id_empty"))
            return False
        if persona_id == personas.DEFAULT_ID:
            self._complain(t("settings.personality.err_id_reserved", id=persona_id))
            return False
        if not personas.ID_RE.match(persona_id):
            self._complain(t("settings.personality.err_id_chars"))
            return False
        if self._persona_id != persona_id and personas.by_id(persona_id) is not None:
            self._complain(t("settings.personality.err_id_dup", id=persona_id))
            return False
        # 新建、且目录还跟着 ID 走：直接把 <人格根目录>/<id> 建出来，塞一份模板，
        # 这样"新建"得到的是**属于这个人的一套 .md**，而不是共享默认目录里的文件
        if self._dir_follows_id:
            created = personas.create_persona_dir(persona_id)
            self.ed_dir.setText(str(created))
            self._dir_follows_id = False
            self._rescan(checked=set(personas.TEMPLATES))
        directory = self._dir()
        if not directory.is_dir():
            self._complain(t("settings.personality.err_dir", path=str(directory)))
            return False
        files = self._selected_files()
        if not files:
            self._complain(t("settings.personality.err_files"))
            return False

        personas.save_persona(
            personas.Persona(
                id=persona_id,
                label=label or persona_id,
                dir=str(directory),      # save_persona 会折算成相对人格根目录
                files=files,
                order=self._order,
            )
        )
        self._persona_id = persona_id
        self.refresh(select_id=persona_id)
        self.lb_status.setText(t("settings.personality.saved"))
        self.saved.emit()
        return True

    def _delete(self) -> None:
        """从清单里删掉这一条定义 —— **不动它的目录和 .md**。"""
        persona_id = self._persona_id
        if self._readonly or persona_id == personas.DEFAULT_ID:
            self._complain(t("settings.personality.err_default_delete"))
            return
        if not persona_id:
            self._complain(t("settings.personality.err_no_selection"))
            return
        target = personas.by_id(persona_id)
        if target is None:
            return
        if len(personas.list_personas()) <= 1:
            self._complain(t("settings.personality.err_last_persona"))
            return
        answer = QMessageBox.question(
            self,
            t("settings.personality.delete_button"),
            t("settings.personality.confirm_delete", name=target.display,
              path=str(target.path())),
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No,
        )
        if answer != QMessageBox.StandardButton.Yes:
            return
        if not personas.remove_persona(persona_id):
            self._complain(t("settings.personality.err_delete_failed"))
            return
        self._persona_id = ""
        self.refresh()
        self.lb_status.setText(t("settings.personality.deleted"))
        self.saved.emit()

    def _preview(self) -> None:
        """看一眼拼出来的 system 提示词 —— 排查"模型不按人格说话"用。"""
        body = personas.build_system_prompt(str(self._dir()), self._selected_files())
        _TextDialog(
            t("settings.personality.preview"),
            body or t("settings.personality.preview_empty"),
            self,
        ).exec()

    def _complain(self, message: str) -> None:
        self.lb_status.setText(message)
        QMessageBox.warning(self, t("settings.personality.title"), message)



class RagPage(QWidget):
    """RAG 页：服务配置 / 检索与切片参数 / 知识库。

    参数全部**立即存盘**（和别的页一样，没有保存按钮）：

    - 检索类（@k、超时、相似度、注入字数）：下一次提问生效
    - 切片类（块大小、重叠、单文件上限、块数上限）：下一次同步生效，
      点「重新扫描」可以立刻重建；改这两个会触发整库重切

    索引只在**启动时**同步一次（用户 2026-11-12 的要求），运行中想立刻生效就点
    「重新扫描」。
    """

    def __init__(self, parent=None, *, rag=None):
        super().__init__(parent)
        self.rag = rag
        self._cfg = chat_config.load()

        outer = QVBoxLayout(self)
        outer.setContentsMargins(0, 0, 0, 0)
        # 内容比一屏高：整页塞进滚动区，窗口小也都能改到
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.Shape.NoFrame)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        outer.addWidget(scroll)

        body = QWidget()
        lay = QVBoxLayout(body)
        lay.setContentsMargins(28, 24, 28, 24)
        lay.setSpacing(12)
        scroll.setWidget(body)

        lay.addWidget(page_title(t("settings.rag.title")))

        # --- 卡片一：服务与模型 -----------------------------------------
        top_card, top = card()
        top.addWidget(field_label(t("settings.rag.ollama")))
        row = QHBoxLayout()
        row.setSpacing(8)
        self.ed_ollama = field_input(t("settings.rag.ollama_placeholder"))
        self.ed_ollama.setText(self._cfg.rag_ollama)
        self.ed_ollama.editingFinished.connect(self.save)
        row.addWidget(self.ed_ollama, 1)
        top.addLayout(row)

        top.addWidget(field_label(t("settings.rag.embedding")))
        row = QHBoxLayout()
        row.setSpacing(8)
        self.ed_embedding = field_input(t("settings.rag.embedding_placeholder"))
        self.ed_embedding.setText(self._cfg.rag_embedding)
        self.ed_embedding.editingFinished.connect(self.save)
        row.addWidget(self.ed_embedding, 1)
        top.addLayout(row)

        self.cb_enabled = QCheckBox(t("settings.rag.enabled"))
        self.cb_enabled.setObjectName("fileCheck")
        self.cb_enabled.setChecked(bool(self._cfg.rag_enabled))
        self.cb_enabled.setCursor(Qt.CursorShape.PointingHandCursor)
        self.cb_enabled.toggled.connect(self.save)
        top.addWidget(self.cb_enabled)

        self.cb_autostart = QCheckBox(t("settings.rag.autostart"))
        self.cb_autostart.setObjectName("fileCheck")
        self.cb_autostart.setChecked(bool(self._cfg.rag_autostart))
        self.cb_autostart.setCursor(Qt.CursorShape.PointingHandCursor)
        self.cb_autostart.setToolTip(t("settings.rag.autostart_hint"))
        self.cb_autostart.toggled.connect(self.save)
        top.addWidget(self.cb_autostart)
        hint_auto = QLabel(t("settings.rag.autostart_hint"))
        hint_auto.setObjectName("hintText")
        hint_auto.setWordWrap(True)
        top.addWidget(hint_auto)
        lay.addWidget(top_card)

        # --- 卡片二：参数（两列，省竖向空间）----------------------------
        param_card, params = card()
        params.addWidget(field_label(t("settings.rag.params")))
        grid = QGridLayout()
        grid.setHorizontalSpacing(18)
        grid.setVerticalSpacing(8)

        self.sp_chunk_chars = self._spin("chunk_chars")
        self.sp_chunk_overlap = self._spin("chunk_overlap")
        self.sp_max_file = self._spin("max_file_mb")
        self.sp_max_chunks = self._spin("max_chunks")
        self.sp_top_k = self._spin("top_k")
        self.sp_timeout = self._spin("timeout_ms")
        self.sp_inject = self._spin("inject_chars")
        self.sp_min_score = self._score_spin()

        left = [
            (t("settings.rag.chunk_chars"), self.sp_chunk_chars,
             t("settings.rag.chunk_chars_hint")),
            (t("settings.rag.chunk_overlap"), self.sp_chunk_overlap,
             t("settings.rag.chunk_overlap_hint")),
            (t("settings.rag.max_file_mb"), self.sp_max_file, ""),
            (t("settings.rag.max_chunks"), self.sp_max_chunks, ""),
        ]
        right = [
            (t("settings.rag.top_k"), self.sp_top_k, t("settings.rag.top_k_hint")),
            (t("settings.rag.timeout"), self.sp_timeout, t("settings.rag.timeout_hint")),
            (t("settings.rag.min_score"), self.sp_min_score, ""),
            (t("settings.rag.inject_chars"), self.sp_inject, ""),
        ]
        for column, items in enumerate((left, right)):
            for index, (label, widget, hint) in enumerate(items):
                cell = QVBoxLayout()
                cell.setSpacing(2)
                head = QHBoxLayout()
                head.setSpacing(6)
                head.addWidget(field_label(label))
                head.addWidget(widget)
                head.addStretch(1)
                cell.addLayout(head)
                if hint:
                    note = QLabel(hint)
                    note.setObjectName("hintText")
                    note.setWordWrap(True)
                    cell.addWidget(note)
                grid.addLayout(cell, index, column)
        params.addLayout(grid)

        self.lb_params_note = QLabel(t("settings.rag.params_note"))
        self.lb_params_note.setObjectName("hintText")
        self.lb_params_note.setWordWrap(True)
        params.addWidget(self.lb_params_note)
        lay.addWidget(param_card)

        # --- 卡片三：知识库目录 + 文件清单 ------------------------------
        lib_card, lib = card()
        lib.addWidget(field_label(t("settings.rag.folder")))

        folder_row = QHBoxLayout()
        folder_row.setSpacing(8)
        self.ed_folder = field_input(t("settings.rag.folder_placeholder"))
        self.ed_folder.setText(self._cfg.rag_dir)
        self.ed_folder.editingFinished.connect(self._on_folder_edited)
        folder_row.addWidget(self.ed_folder, 1)
        btn_choose = small_button(t("common.choose"))
        btn_choose.clicked.connect(self._pick_folder)
        btn_open = small_button(t("common.edit"))
        btn_open.clicked.connect(self._open_folder)
        folder_row.addWidget(btn_choose)
        folder_row.addWidget(btn_open)
        lib.addLayout(folder_row)

        self.lb_resolved = QLabel("")
        self.lb_resolved.setObjectName("hintText")
        self.lb_resolved.setWordWrap(True)
        lib.addWidget(self.lb_resolved)

        lib.addWidget(field_label(t("settings.rag.file_list")))
        self.file_list = field_list()
        lib.addWidget(self.file_list, 1)

        self.lb_status = QLabel("")
        self.lb_status.setObjectName("hintText")
        self.lb_status.setWordWrap(True)
        lib.addWidget(self.lb_status)

        buttons = QHBoxLayout()
        buttons.setSpacing(10)
        self.btn_rescan = small_button(t("settings.rag.rescan"), primary=True)
        self.btn_rescan.setToolTip(t("settings.rag.rescan_hint"))
        self.btn_rescan.clicked.connect(self._rescan)
        self.btn_clear = small_button(t("settings.rag.clear_index"))
        self.btn_clear.setToolTip(t("settings.rag.clear_hint"))
        self.btn_clear.clicked.connect(self._clear_index)
        buttons.addWidget(self.btn_rescan)
        buttons.addWidget(self.btn_clear)
        buttons.addStretch(1)
        lib.addLayout(buttons)

        lay.addWidget(lib_card, 1)

        self._wire_service()
        self.refresh_status()
        self._refresh_files()

    # --- 参数控件 -------------------------------------------------------
    def _spin(self, field: str) -> QSpinBox:
        low, high, step = chat_config.RAG_LIMITS[field]
        box = QSpinBox()
        box.setRange(int(low), int(high))
        box.setSingleStep(max(1, int(step)))
        box.setValue(int(getattr(self._cfg, f"rag_{field}")))
        box.setFixedWidth(96)
        box.valueChanged.connect(self.save)
        setattr(self, f"_spin_{field}", box)
        return box

    def _score_spin(self) -> QDoubleSpinBox:
        low, high, step = chat_config.RAG_LIMITS["min_score"]
        box = QDoubleSpinBox()
        box.setRange(float(low), float(high))
        box.setSingleStep(float(step))
        box.setDecimals(2)
        box.setValue(float(self._cfg.rag_min_score))
        box.setFixedWidth(96)
        box.valueChanged.connect(self.save)
        return box

    # --- 路径 -----------------------------------------------------------
    def _pick_folder(self) -> None:
        chosen = QFileDialog.getExistingDirectory(
            self, self.ed_folder.placeholderText(), str(Path.home())
        )
        if chosen:
            self.ed_folder.setText(_store_path(chosen))
            self._on_folder_edited()

    def _open_folder(self) -> None:
        directory = _resolve_folder(self.ed_folder.text())
        if directory.is_dir():
            QDesktopServices.openUrl(QUrl.fromLocalFile(str(directory)))

    def _on_folder_edited(self) -> None:
        self.save()
        self._refresh_files()
        self.refresh_status()

    # --- 文件清单 / 状态 ------------------------------------------------
    def _refresh_files(self) -> None:
        self.file_list.clear()
        directory = _resolve_folder(self.ed_folder.text())
        self.lb_resolved.setText(
            t("settings.rag.resolved", path=_display_path(directory))
        )
        if not directory.is_dir():
            self.file_list.addItem(t("settings.rag.file_empty"))
            return

        from dsai4431_chatbot.core.rag import loader

        max_mb = chat_config.clamp_int(self.sp_max_file.value(), "max_file_mb")
        scanned = loader.scan(directory, max_mb)
        if not scanned.files:
            self.file_list.addItem(t("settings.rag.file_empty"))
        for rel, (size, _mtime) in sorted(scanned.files.items()):
            self.file_list.addItem(f"{rel}    ({_human_size(size)})")
        for item in scanned.skipped[:20]:
            reason = t(f"settings.rag.skip_{item['reason']}")
            self.file_list.addItem(f"{item['rel']}    ({reason})")
        if self.rag is None:
            self.lb_status.setText(t("settings.rag.status_no_service"))

    def _wire_service(self) -> None:
        if self.rag is None:
            self.btn_rescan.setEnabled(False)
            self.btn_clear.setEnabled(False)
            return
        self.rag.progress.connect(self._on_progress)
        self.rag.ollama_ready.connect(self._on_ollama_ready)
        self.rag.synced.connect(self._on_synced)
        self.rag.syncing_changed.connect(self._on_syncing)

    def _on_ollama_ready(self, launch) -> None:
        """Ollama 探测/拉起的结果（同步结果随后会覆盖这一行，正常）。"""
        if launch is None:
            return
        try:
            text = t(launch.message_key)
        except Exception:                       # noqa: BLE001 - 文案缺了也别炸
            text = str(launch.detail)
        self.lb_status.setText(text)

    def _on_progress(self, done: int, total: int, rel: str) -> None:
        self.lb_status.setText(
            t("settings.rag.syncing", done=done, total=total, name=rel)
        )

    def _on_syncing(self, running: bool) -> None:
        self.btn_rescan.setEnabled(not running)
        if running:
            self.lb_status.setText(t("settings.rag.syncing_start"))

    def _on_synced(self, result) -> None:
        if result is None:
            self.lb_status.setText(t("settings.rag.sync_failed_unknown"))
            return
        if result.status == "empty":
            self.lb_status.setText(t("settings.rag.sync_empty"))
        elif result.ok:
            self.lb_status.setText(
                t(
                    "settings.rag.sync_ok",
                    files=result.files,
                    chunks=result.chunks,
                    added=result.added,
                    updated=result.updated,
                    removed=result.removed,
                    seconds=f"{result.elapsed_s:.1f}",
                )
            )
        elif result.status == "too_many_chunks":
            self.lb_status.setText(t("settings.rag.sync_too_many", detail=result.error))
        else:
            self.lb_status.setText(t("settings.rag.sync_failed", detail=result.error))
        self._refresh_files()

    def refresh_status(self) -> None:
        """没用过 service（或者同步失败）时，至少把「盘上那份索引」说清楚。"""
        if self.rag is None:
            return
        if self.rag.is_syncing():
            return
        summary = self.rag.status()
        if summary.get("chunks"):
            self.lb_status.setText(
                t(
                    "settings.rag.index_ready",
                    files=summary["files"],
                    chunks=summary["chunks"],
                    dim=summary["dim"],
                )
            )
            self.btn_clear.setEnabled(True)
        else:
            self.lb_status.setText(t("settings.rag.status_not_built"))
            self.btn_clear.setEnabled(False)

    # --- 按钮 -----------------------------------------------------------
    def _rescan(self) -> None:
        self.save()
        if self.rag is None:
            return
        self.lb_status.setText(t("settings.rag.syncing_start"))
        self.rag.refresh(chat_config.load())

    def _clear_index(self) -> None:
        from dsai4431_chatbot.core.rag import store

        store.clear()
        if self.rag is not None:
            self.rag.reload_index()
        self.refresh_status()
        self.lb_status.setText(t("settings.rag.status_cleared"))

    # --- 存盘 -----------------------------------------------------------
    def save(self) -> None:
        cfg = chat_config.load()          # 现读，只改自己这些字段
        cfg.rag_ollama = self.ed_ollama.text().strip()
        cfg.rag_embedding = self.ed_embedding.text().strip()
        cfg.rag_dir = self.ed_folder.text().strip()
        cfg.rag_enabled = bool(self.cb_enabled.isChecked())
        cfg.rag_autostart = bool(self.cb_autostart.isChecked())
        cfg.rag_top_k = self.sp_top_k.value()
        cfg.rag_timeout_ms = self.sp_timeout.value()
        cfg.rag_min_score = float(self.sp_min_score.value())
        cfg.rag_chunk_chars = self.sp_chunk_chars.value()
        cfg.rag_chunk_overlap = self.sp_chunk_overlap.value()
        cfg.rag_max_file_mb = self.sp_max_file.value()
        cfg.rag_max_chunks = self.sp_max_chunks.value()
        cfg.rag_inject_chars = self.sp_inject.value()
        chat_config.save(cfg)


def _store_path(chosen: str) -> str:
    """选目录时尽量存相对仓库根的路径（换机器还能用）。"""
    from dsai4431_chatbot.core.gui import settings_store

    path = Path(chosen)
    try:
        return path.resolve().relative_to(settings_store.project_root().resolve()).as_posix()
    except (ValueError, OSError):
        return str(path)


def _resolve_folder(raw: str) -> Path:
    """把输入框里的字变成绝对目录（空 = 默认 asset/RAG）。"""
    from dsai4431_chatbot.core.rag import paths

    return paths.knowledge_root(raw)


def _display_path(path: Path) -> str:
    from dsai4431_chatbot.core.gui import settings_store

    try:
        return path.resolve().relative_to(settings_store.project_root().resolve()).as_posix()
    except (ValueError, OSError):
        return str(path)


def _human_size(size: int) -> str:
    value = float(size)
    for unit in ("B", "KB", "MB", "GB"):
        if value < 1024 or unit == "GB":
            return f"{value:.0f} {unit}" if unit == "B" else f"{value:.1f} {unit}"
        value /= 1024
    return f"{value:.1f} GB"


class Live2DModelPage(QWidget):
    """Live2D model 页：选模型 + 外观 / 行为 / 部件调整。

    所有改动都**立即生效**并写进 settings.ini（和换肤共用一份配置），
    下次启动自动还原。
    """

    def __init__(self, character, parent=None):
        super().__init__(parent)
        self.character = character          # main_window.CharacterPanel
        self._parts: list[dict] = []
        self._syncing = False

        lay = QVBoxLayout(self)
        lay.setContentsMargins(28, 24, 28, 24)
        lay.setSpacing(10)

        lay.addWidget(page_title(t("settings.live2d.title")))
        hint = QLabel(t("settings.live2d.hint"))
        hint.setObjectName("hintText")
        hint.setWordWrap(True)
        lay.addWidget(hint)

        body = QHBoxLayout()
        body.setSpacing(16)

        # --- 左：模型列表 -----------------------------------------------
        left_card, left = card()
        left_card.setFixedWidth(280)
        left.addWidget(section_title(t("settings.live2d.model")))
        self.model_list = field_list()
        self.model_list.setSpacing(1)
        left.addWidget(self.model_list, 1)

        scan_row = QHBoxLayout()
        scan_row.addWidget(small_button(t("settings.live2d.rescan"), primary=False))
        scan_row.itemAt(0).widget().clicked.connect(self._rescan_models)
        scan_row.addStretch(1)
        left.addLayout(scan_row)
        body.addWidget(left_card)

        # --- 右：调整 ---------------------------------------------------
        right_card, right = card()
        right.addWidget(section_title(t("settings.live2d.look")))

        framing_row = QHBoxLayout()
        framing_row.setSpacing(8)
        framing_row.addWidget(field_label(t("settings.live2d.framing")))
        self.cbo_framing = QComboBox()
        themes.round_popup(self.cbo_framing)      # 弹窗圆角（见 themes.round_popup）
        self.cbo_framing.addItem(t("settings.live2d.framing_bust"), "bust")
        self.cbo_framing.addItem(t("settings.live2d.framing_full"), "full")
        self.cbo_framing.currentIndexChanged.connect(self._on_framing)
        framing_row.addWidget(self.cbo_framing, 1)
        right.addLayout(framing_row)

        self.sl_scale, self.lb_scale = self._slider_row(
            right, t("settings.live2d.scale"), 40, 250, "%"
        )
        self.sl_offx, self.lb_offx = self._slider_row(
            right, t("settings.live2d.offset_x"), -300, 300, "px"
        )
        self.sl_offy, self.lb_offy = self._slider_row(
            right, t("settings.live2d.offset_y"), -300, 300, "px"
        )

        right.addSpacing(4)
        right.addWidget(section_title(t("settings.live2d.behavior")))
        behaviors = QVBoxLayout()
        behaviors.setSpacing(2)
        self.cb_physics = QCheckBox(t("settings.live2d.physics"))
        self.cb_blink = QCheckBox(t("settings.live2d.blink"))
        self.cb_breath = QCheckBox(t("settings.live2d.breath"))
        self.cb_follow = QCheckBox(t("settings.live2d.follow"))
        for box, name in (
            (self.cb_physics, "physics"),
            (self.cb_blink, "blink"),
            (self.cb_breath, "breath"),
            (self.cb_follow, "follow"),
        ):
            box.setObjectName("fileCheck")
            box.toggled.connect(lambda on, n=name: self._on_behavior(n, on))
            behaviors.addWidget(box)
        right.addLayout(behaviors)

        right.addSpacing(4)
        parts_head = QHBoxLayout()
        parts_head.addWidget(section_title(t("settings.live2d.parts")))
        parts_head.addStretch(1)
        btn_show_all = small_button(t("settings.live2d.show_all"))
        btn_show_all.clicked.connect(self._show_all_parts)
        parts_head.addWidget(btn_show_all)
        right.addLayout(parts_head)

        self.parts_list = field_list()
        self.parts_list.setMinimumHeight(120)
        self.parts_list.itemChanged.connect(self._on_part_toggled)
        right.addWidget(self.parts_list, 1)

        reset_row = QHBoxLayout()
        reset_row.addStretch(1)
        btn_reset = small_button(t("settings.live2d.reset_look"))
        btn_reset.clicked.connect(self._reset_look)
        reset_row.addWidget(btn_reset)
        right.addLayout(reset_row)

        body.addWidget(right_card, 1)
        lay.addLayout(body, 1)

        self._rescan_models()
        self._sync_from_config()
        # 换模型后 view 会重新就绪，这时候再去要一次部件清单
        if hasattr(character, "live2d_ready"):
            character.live2d_ready.connect(self.refresh_parts)
        self.refresh_parts()

    # --- 小工具 ---------------------------------------------------------
    def _slider_row(self, layout, label: str, lo: int, hi: int, unit: str):
        row = QHBoxLayout()
        row.setSpacing(8)
        row.addWidget(field_label(label))
        slider = QSlider(Qt.Orientation.Horizontal)
        slider.setRange(lo, hi)
        slider.setMinimumWidth(120)
        value = QLabel("")
        value.setObjectName("hintText")
        value.setFixedWidth(56)
        value.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
        row.addWidget(slider, 1)
        row.addWidget(value)
        layout.addLayout(row)

        def show(v: int) -> None:
            value.setText(f"{v}{unit}")

        slider.valueChanged.connect(show)
        return slider, show

    def _set_slider(self, slider: QSlider, value: int, formatter) -> None:
        blocker = QSignalBlocker(slider)
        slider.setValue(int(value))
        del blocker
        formatter(int(value))

    # --- 模型 -----------------------------------------------------------
    def _rescan_models(self) -> None:
        self._syncing = True
        self.model_list.clear()
        current = self.character.current_model()
        for path in live2d_embed.list_models():
            item = QListWidgetItem(live2d_embed.model_label(path))
            item.setData(Qt.ItemDataRole.UserRole, str(path))
            item.setToolTip(live2d_embed.model_key(path))   # 完整相对路径
            self.model_list.addItem(item)
            if current is not None and path == current:
                self.model_list.setCurrentItem(item)
        self._syncing = False
        if self.model_list.currentItem() is None and self.model_list.count():
            self.model_list.setCurrentRow(0)
        self.model_list.currentItemChanged.connect(self._on_model_changed)

    def _on_model_changed(self, item, _prev) -> None:
        if self._syncing or item is None:
            return
        path = item.data(Qt.ItemDataRole.UserRole)
        if not path:
            return
        self.character.set_model(Path(path))

    # --- 外观 -----------------------------------------------------------
    def _on_framing(self, index: int) -> None:
        if self._syncing:
            return
        self.character.set_framing(self.cbo_framing.itemData(index))

    def _on_scale(self, value: int) -> None:
        if not self._syncing:
            self.character.set_scale(value / 100.0)

    def _on_offset(self, _value: int) -> None:
        if not self._syncing:
            self.character.set_offset(self.sl_offx.value(), self.sl_offy.value())

    def _on_behavior(self, name: str, on: bool) -> None:
        if not self._syncing:
            self.character.set_behavior(name, on)

    def _reset_look(self) -> None:
        self._syncing = True
        self.cbo_framing.setCurrentIndex(0)
        self._set_slider(self.sl_scale, 100, self.lb_scale)
        self._set_slider(self.sl_offx, 0, self.lb_offx)
        self._set_slider(self.sl_offy, 0, self.lb_offy)
        self._syncing = False
        self.character.set_framing("bust")
        self.character.set_scale(1.0)
        self.character.set_offset(0, 0)

    def _sync_from_config(self) -> None:
        cfg = self.character.config
        self._syncing = True
        index = self.cbo_framing.findData(cfg.framing)
        self.cbo_framing.setCurrentIndex(max(0, index))
        self._set_slider(self.sl_scale, round(cfg.scale * 100), self.lb_scale)
        self._set_slider(self.sl_offx, cfg.offset_x, self.lb_offx)
        self._set_slider(self.sl_offy, cfg.offset_y, self.lb_offy)
        self.cb_physics.setChecked(cfg.physics)
        self.cb_blink.setChecked(cfg.blink)
        self.cb_breath.setChecked(cfg.breath)
        self.cb_follow.setChecked(cfg.follow)
        self._syncing = False
        # 滑块要在 init 之后才连信号，避免初始化时触发一次保存
        self.sl_scale.valueChanged.connect(self._on_scale)
        self.sl_offx.valueChanged.connect(self._on_offset)
        self.sl_offy.valueChanged.connect(self._on_offset)

    # --- 部件 -----------------------------------------------------------
    def refresh_parts(self) -> None:
        self.character.request_parts(self._fill_parts)

    def _fill_parts(self, payload) -> None:
        import json

        try:
            parts = json.loads(payload or "[]")
        except (TypeError, ValueError):
            parts = []
        self._parts = parts
        hidden = set(self.character.config.hidden_parts)
        self._syncing = True
        self.parts_list.clear()
        for part in parts:
            item = QListWidgetItem(
                t("settings.live2d.part", id=part["id"], n=part["drawables"])
            )
            item.setData(Qt.ItemDataRole.UserRole, part["index"])
            item.setData(Qt.ItemDataRole.UserRole + 1, part["id"])
            item.setFlags(item.flags() | Qt.ItemFlag.ItemIsUserCheckable)
            item.setCheckState(
                Qt.CheckState.Unchecked if part["id"] in hidden else Qt.CheckState.Checked
            )
            self.parts_list.addItem(item)
        self._syncing = False

    def _on_part_toggled(self, item: QListWidgetItem) -> None:
        if self._syncing or item is None:
            return
        index = item.data(Qt.ItemDataRole.UserRole)
        part_id = item.data(Qt.ItemDataRole.UserRole + 1)
        hidden = item.checkState() != Qt.CheckState.Checked
        self.character.set_part_hidden(index, part_id, hidden)

    def _show_all_parts(self) -> None:
        self._syncing = True
        for row in range(self.parts_list.count()):
            item = self.parts_list.item(row)
            if item.checkState() != Qt.CheckState.Checked:
                item.setCheckState(Qt.CheckState.Checked)
        self._syncing = False
        for part in self._parts:
            self.character.set_part_hidden(part["index"], part["id"], False)



class ThemeCard(QFrame):
    """一张主题卡：左边四个色块预览，右边名字和说明。点一下切过去。"""

    clicked = Signal(str)

    def __init__(self, item: themes.Theme, selected: bool, parent=None):
        super().__init__(parent)
        self.setObjectName("themeCard")
        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.theme_id = item.id
        # QSS 的 [selected="true"] 匹配的是字符串属性：这里必须存字符串，
        # 存 bool 会匹配不上（QSS 里 true/false 是字面量）。
        self.setProperty("selected", "true" if selected else "false")

        lay = QHBoxLayout(self)
        lay.setContentsMargins(14, 12, 16, 12)
        lay.setSpacing(16)

        # 预览色块：底 / 卡片 / 强调 / 正文
        swatches = QHBoxLayout()
        swatches.setContentsMargins(0, 0, 0, 0)
        swatches.setSpacing(3)
        for color in item.swatches:
            sw = QFrame()
            sw.setFixedSize(20, 30)
            sw.setStyleSheet(f"background: {color}; border-radius: 4px;")
            swatches.addWidget(sw)
        lay.addLayout(swatches)

        text_box = QVBoxLayout()
        text_box.setContentsMargins(0, 0, 0, 0)
        text_box.setSpacing(2)
        # 名字取自语言包；语言包里没有就用主题 toml 自带的 label/note 兜底，
        # 这样新加的主题不翻译也能正常显示。
        name = QLabel(t(f"theme.{item.id}.name", default=item.label))
        name.setObjectName("themeName")
        note = QLabel(t(f"theme.{item.id}.note", default=item.note or item.id))
        note.setObjectName("themeNote")
        text_box.addWidget(name)
        text_box.addWidget(note)
        lay.addLayout(text_box, 1)

        self.state_label = QLabel(t("settings.theme.in_use") if selected else "")
        self.state_label.setObjectName("hintText")
        lay.addWidget(self.state_label)

    def set_selected(self, on: bool) -> None:
        value = "true" if on else "false"
        if self.property("selected") == value:
            return
        self.setProperty("selected", value)
        self.state_label.setText(t("settings.theme.in_use") if on else "")
        themes.restyle(self)   # 动态属性改了必须重新 polish

    def mousePressEvent(self, event):  # noqa: N802 - Qt 命名
        if event.button() == Qt.MouseButton.LeftButton:
            self.clicked.emit(self.theme_id)
        super().mousePressEvent(event)


class ThemePage(QWidget):
    """Theme 页：换肤。点一下立即生效，选择写进 QSettings，下次启动保持。"""

    def __init__(self, parent=None):
        super().__init__(parent)
        self._cards: dict[str, ThemeCard] = {}

        lay = QVBoxLayout(self)
        lay.setContentsMargins(28, 24, 28, 24)
        lay.setSpacing(12)

        lay.addWidget(page_title(t("settings.theme.title")))

        hint = QLabel(t("settings.theme.hint"))
        hint.setObjectName("hintText")
        hint.setWordWrap(True)
        lay.addWidget(hint)
        lay.addSpacing(4)

        manager = themes.manager()
        for item in manager.available:
            card = ThemeCard(item, selected=item.id == manager.current.id)
            card.clicked.connect(self._on_pick)
            self._cards[item.id] = card
            lay.addWidget(card)

        lay.addStretch(1)
        manager.changed.connect(self._sync)

    def _on_pick(self, theme_id: str) -> None:
        themes.manager().apply(QApplication.instance(), theme_id)

    def _sync(self, theme_id: str) -> None:
        for tid, card in self._cards.items():
            card.set_selected(tid == theme_id)


class OtherPage(QWidget):
    """Other 页：界面语言。

    换语言**不热更新**：文案在构造窗口时取过一次，所以这里只负责存盘 +
    重启进程（用户选定的方案）。重启由 `relaunch` 负责等旧进程退干净再
    拉起新的，避免两份 QtWebEngine 抢 profile 目录。
    """

    def __init__(self, parent=None):
        super().__init__(parent)
        lay = QVBoxLayout(self)
        lay.setContentsMargins(28, 24, 28, 24)
        lay.setSpacing(12)

        lay.addWidget(page_title(t("settings.other.title")))

        card_frame, body = card()
        body.addWidget(section_title(t("settings.other.language")))

        row = QHBoxLayout()
        row.setSpacing(10)
        row.addWidget(field_label(t("settings.other.language_label")))
        self.cbo_language = QComboBox()
        themes.round_popup(self.cbo_language)     # 弹窗圆角（见 themes.round_popup）
        for lang in i18n.available():
            # 用各语言自己的写法（中文 / English），无论当前是哪套文案都认得
            self.cbo_language.addItem(lang.name, lang.code)
        self._select(i18n.current().code)
        self.cbo_language.currentIndexChanged.connect(self._on_language)
        row.addWidget(self.cbo_language, 1)
        body.addLayout(row)

        self.hint = QLabel(t("settings.other.language_hint"))
        self.hint.setObjectName("hintText")
        self.hint.setWordWrap(True)
        body.addWidget(self.hint)

        body.addSpacing(10)
        cfg = chat_config.load()
        self.cb_reasoning = QCheckBox(t("settings.other.show_reasoning"))
        self.cb_reasoning.setObjectName("fileCheck")
        self.cb_reasoning.setChecked(bool(cfg.show_reasoning))
        self.cb_reasoning.setCursor(Qt.CursorShape.PointingHandCursor)
        self.cb_reasoning.toggled.connect(self._on_reasoning_toggled)
        body.addWidget(self.cb_reasoning)

        hint2 = QLabel(t("settings.other.show_reasoning_hint"))
        hint2.setObjectName("hintText")
        hint2.setWordWrap(True)
        body.addWidget(hint2)

        lay.addWidget(card_frame)
        lay.addStretch(1)

    def _select(self, code: str) -> None:
        """按 code 选中下拉项（找不到就留在第一项），不触发切换逻辑。"""
        index = self.cbo_language.findData(code)
        if index < 0:
            return
        blocker = QSignalBlocker(self.cbo_language)
        self.cbo_language.setCurrentIndex(index)
        del blocker

    def _on_reasoning_toggled(self, on: bool) -> None:
        """显示思考链：现读配置、只改这一项（别把别的页刚存的覆盖掉）。"""
        cfg = chat_config.load()
        cfg.show_reasoning = bool(on)
        chat_config.save(cfg)

    def _on_language(self, index: int) -> None:
        code = self.cbo_language.itemData(index)
        if not code:
            return
        previous = i18n.current().code
        if code == previous:
            return

        i18n.set_language(code)              # 先落盘：重启后的新进程按它取文案
        self.hint.setText(t("settings.other.language_restarting"))
        self.cbo_language.setEnabled(False)

        if not relaunch.restart():
            # 拉不起新进程：回滚到原语言，不留一个"看着像换好了"的假状态
            i18n.set_language(previous)
            self.cbo_language.setEnabled(True)
            self._select(previous)
            self.hint.setText(t("settings.other.language_hint"))


# ---------------------------------------------------------------------------
# 弹窗
# ---------------------------------------------------------------------------
class SettingsDialog(QDialog):
    """六个分页，顺序照用户给的导航清单。

    草图里只画了前四项的图标；Theme 后来补了场记板（clapper.svg），
    Other 用齿轮（gear.svg），现在六项都有图标。
    """

    # 人格清单被改了（新建/改名/换目录），主窗拿去刷新首页下拉
    personas_changed = Signal()

    # (图标, 文案 key, 页面类)
    PAGES = [
        ("key", "settings.nav.api_key", ApiKeyPage),
        ("user", "settings.nav.personality", PersonalityPage),
        ("doc", "settings.nav.rag", RagPage),
        ("live2d", "settings.nav.live2d", Live2DModelPage),
        ("clapper", "settings.nav.theme", ThemePage),
        ("gear", "settings.nav.other", OtherPage),
    ]

    def __init__(self, parent=None, character=None, rag=None):
        super().__init__(parent)
        self.character = character          # 给 Live2D model 页用（可为 None）
        self.rag = rag                      # 给 RAG 页用（可为 None）
        self.setWindowTitle(t("settings.title"))
        # 无边框 + 透明底：圆角和外投影都要自己画（DSH 的设置窗就是这个样子）。
        # 无边框之后系统标题栏没了，窗口自然也不能拖动，符合"不可移动"。
        self.setWindowFlags(Qt.WindowType.Dialog | Qt.WindowType.FramelessWindowHint)
        self.setWindowModality(Qt.WindowModality.NonModal)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground, True)
        self.setMinimumSize(820 + 2 * SHADOW, 560 + 2 * SHADOW)
        self.resize(DIALOG_W, DIALOG_H)

        outer = QVBoxLayout(self)
        outer.setContentsMargins(SHADOW, SHADOW, SHADOW, SHADOW)
        outer.setSpacing(0)

        shell = QFrame()
        shell.setObjectName("settingsShell")
        shell.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)
        outer.addWidget(shell)
        self._shell = shell

        shadow = QGraphicsDropShadowEffect(shell)
        shadow.setBlurRadius(40)
        shadow.setColor(QColor(15, 17, 21, 70))
        shadow.setOffset(0, 10)
        shell.setGraphicsEffect(shadow)

        body = QVBoxLayout(shell)
        body.setContentsMargins(0, 0, 0, 0)
        body.setSpacing(0)

        # --- 顶栏：标题 + 关闭 -------------------------------------------
        header = QHBoxLayout()
        header.setContentsMargins(20, 14, 14, 4)
        header.setSpacing(8)
        title = QLabel(t("settings.title"))
        title.setObjectName("settingsTitle")
        header.addWidget(title)
        header.addStretch(1)
        self.btn_close = QPushButton()
        self.btn_close.setObjectName("iconButton")
        themes.bind(self.btn_close, "close")
        self.btn_close.setIconSize(QSize(ICON, ICON))
        self.btn_close.setFixedSize(30, 30)
        self.btn_close.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_close.setToolTip(t("settings.close"))
        self.btn_close.clicked.connect(self.reject)
        header.addWidget(self.btn_close)
        body.addLayout(header)

        # --- 导航 + 分页 -------------------------------------------------
        content = QHBoxLayout()
        content.setContentsMargins(0, 0, 0, 0)
        content.setSpacing(0)
        body.addLayout(content, 1)

        # 左侧导航
        nav = QFrame()
        nav.setObjectName("settingsNav")
        nav.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)
        nav.setFixedWidth(NAV_W)
        nav_lay = QVBoxLayout(nav)
        nav_lay.setContentsMargins(10, 8, 10, 16)
        nav_lay.setSpacing(4)

        self._group = QButtonGroup(self)
        self._group.setExclusive(True)

        for index, (icon, text_key, _page) in enumerate(self.PAGES):
            btn = QPushButton(t(text_key))
            btn.setObjectName("navButton")
            if icon:
                themes.bind(btn, icon)
                btn.setIconSize(QSize(ICON, ICON))
            btn.setCheckable(True)
            btn.setCursor(Qt.CursorShape.PointingHandCursor)
            btn.setChecked(index == 0)
            self._group.addButton(btn, index)
            nav_lay.addWidget(btn)

        nav_lay.addStretch(1)
        content.addWidget(nav)

        # 右侧分页
        self.stack = QStackedWidget()
        for _icon, _text_key, page_cls in self.PAGES:
            if page_cls is Live2DModelPage:
                page = page_cls(character)
            elif page_cls is RagPage:
                page = page_cls(rag=self.rag)     # 共用主窗口那份索引缓存
            else:
                page = page_cls()
            # 人格页保存后主窗要刷新首页的下拉，别让人新建完还看不到
            if isinstance(page, PersonalityPage):
                page.saved.connect(self.personas_changed)
            self.stack.addWidget(page)
        content.addWidget(self.stack, 1)

        # 唯一的行为：切页（否则其余两页看不到）
        self._group.idClicked.connect(self.stack.setCurrentIndex)

    # --- 点框外关闭 -------------------------------------------------------
    # 对话框不是模态（模态会把点击吃掉，外面根本收不到事件），
    # 所以在应用级装一个事件过滤器，按下点不在窗口范围内就关。
    def showEvent(self, event):  # noqa: N802 - Qt 命名
        super().showEvent(event)
        QApplication.instance().installEventFilter(self)

    def hideEvent(self, event):  # noqa: N802
        super().hideEvent(event)
        QApplication.instance().removeEventFilter(self)

    def eventFilter(self, obj, event):  # noqa: N802
        if event.type() == QEvent.Type.MouseButtonPress and self.isVisible():
            if not self.frameGeometry().contains(event.globalPosition().toPoint()):
                self.close()
        return super().eventFilter(obj, event)

    def set_page(self, index: int) -> None:
        """给截图/调试用：直接跳到某一页。"""
        self._group.button(index).setChecked(True)
        self.stack.setCurrentIndex(index)

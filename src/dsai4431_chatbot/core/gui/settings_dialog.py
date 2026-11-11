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

import os
from pathlib import Path

from PySide6.QtCore import QEvent, QSize, QSignalBlocker, Qt, Signal
from PySide6.QtGui import QColor
from PySide6.QtWidgets import (
    QApplication,
    QButtonGroup,
    QCheckBox,
    QComboBox,
    QDialog,
    QFrame,
    QGraphicsDropShadowEffect,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QListWidget,
    QListWidgetItem,
    QPushButton,
    QSlider,
    QStackedWidget,
    QVBoxLayout,
    QWidget,
)

from dsai4431_chatbot.core.gui import i18n, live2d_embed, relaunch, theme, themes
from dsai4431_chatbot.core.gui.i18n import t

SHADOW = 18  # 圆角窗外留给投影的透明边距（窗口本身比可见卡片大一圈）
DIALOG_W, DIALOG_H = 980 + 2 * SHADOW, 660 + 2 * SHADOW
NAV_W = 172
ICON = 16

# 人格文件目录：默认指向 DSH 那套 persona（大肥鲸），可用环境变量改写。
# 目录不存在时用演示数据 —— 这一页目前只有布局，不接业务。
PERSONA_DIR = Path(os.environ.get("DSAI_PERSONA_DIR", r"P:\.dsh\agentsoul"))
PERSONA_DEFAULT_CHECKED = {"IDENTITY.md", "SOUL.md", "USER.md"}
PERSONA_DEMO_FILES = [("IDENTITY.md", 619), ("SOUL.md", 1298), ("USER.md", 374)]


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
    """扫描人格目录下的 .md，返回 [(文件名, 字符数)]。

    目录不存在（或空）时退回演示数据 —— Personality 页目前只有布局。
    """
    try:
        paths = sorted(p for p in directory.iterdir() if p.suffix.lower() == ".md")
    except OSError:
        return list(PERSONA_DEMO_FILES)

    rows: list[tuple[str, int]] = []
    for path in paths:
        try:
            rows.append((path.name, len(path.read_text(encoding="utf-8", errors="ignore"))))
        except OSError:
            rows.append((path.name, 0))
    return rows or list(PERSONA_DEMO_FILES)


class FileCheckList(QFrame):
    """文件清单：每行 = 勾选框（文件名）+ 右侧字符数。

    勾选状态只存在控件里，暂不落盘（这一页是布局）。
    """

    def __init__(
        self,
        rows: list[tuple[str, int]],
        checked: set[str] | None = None,
        parent=None,
    ):
        super().__init__(parent)
        self.setObjectName("fileList")
        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)

        checked = checked if checked is not None else PERSONA_DEFAULT_CHECKED
        self.boxes: dict[str, QCheckBox] = {}

        lay = QVBoxLayout(self)
        lay.setContentsMargins(6, 6, 6, 6)
        lay.setSpacing(1)

        for name, chars in rows:
            row = QFrame()
            row.setObjectName("fileRow")
            row.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)
            row_lay = QHBoxLayout(row)
            row_lay.setContentsMargins(6, 3, 10, 3)
            row_lay.setSpacing(8)

            box = QCheckBox(name)
            box.setObjectName("fileCheck")
            box.setChecked(name in checked)
            box.setCursor(Qt.CursorShape.PointingHandCursor)
            self.boxes[name] = box

            size = QLabel(t("common.chars", n=f"{chars:,}"))
            size.setObjectName("fileSize")

            row_lay.addWidget(box, 1)
            row_lay.addWidget(size)
            lay.addWidget(row)

        lay.addStretch(1)


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
    """API KEY 页。

    草图只有两个字段：API、Token（没有页面标题，标题是这边补的，为了三页对齐）。
    """

    def __init__(self, parent=None):
        super().__init__(parent)
        lay = QVBoxLayout(self)
        lay.setContentsMargins(28, 24, 28, 24)
        lay.setSpacing(10)

        lay.addWidget(page_title(t("settings.api_key.title")))
        lay.addSpacing(6)

        lay.addWidget(field_label(t("settings.api_key.api")))
        lay.addWidget(field_input(t("settings.api_key.api_placeholder")))

        lay.addSpacing(6)
        lay.addWidget(field_label(t("settings.api_key.token")))
        lay.addWidget(field_input(t("settings.api_key.token_placeholder")))

        lay.addStretch(1)


class PersonalityPage(QWidget):
    """人格编辑页：左「Persona 列表」，右「New Persona」表单。"""

    def __init__(self, parent=None):
        super().__init__(parent)

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
        left.addWidget(
            field_list(
                [
                    t("settings.personality.list_default"),
                    t("settings.personality.list_test"),
                ],
                min_height=90,
            ),
            1,
        )
        left.addWidget(
            small_button(t("settings.personality.new_button")), 0, Qt.AlignmentFlag.AlignLeft
        )
        left_card.setFixedWidth(260)
        body.addWidget(left_card)

        # --- 右：New Persona 表单 ---------------------------------------
        right_card, right = card()
        right.addWidget(section_title(t("settings.personality.new_title")))

        right.addWidget(field_label(t("settings.personality.id")))
        right.addWidget(field_input(t("settings.personality.id_placeholder")))

        right.addWidget(field_label(t("settings.personality.name")))
        right.addWidget(field_input(t("settings.personality.name_placeholder")))

        right.addWidget(field_label(t("settings.personality.files")))
        right.addWidget(field_input(t("settings.personality.files_placeholder")))

        path_row = QHBoxLayout()
        path_row.setSpacing(8)
        path_row.addWidget(small_button(t("common.choose")))
        path_row.addWidget(small_button(t("common.edit")))
        path_row.addStretch(1)
        right.addLayout(path_row)

        right.addWidget(field_label(t("settings.personality.file_list")))
        right.addWidget(FileCheckList(scan_persona_files(PERSONA_DIR)), 1)

        footer = QHBoxLayout()
        footer.addStretch(1)
        footer.addWidget(small_button(t("settings.personality.preview")))
        footer.addWidget(small_button(t("settings.personality.save"), primary=True))
        right.addLayout(footer)

        body.addWidget(right_card, 1)
        lay.addLayout(body, 1)


class RagPage(QWidget):
    """RAG 页：上图检索配置，下图知识库。"""

    def __init__(self, parent=None):
        super().__init__(parent)

        lay = QVBoxLayout(self)
        lay.setContentsMargins(28, 24, 28, 24)
        lay.setSpacing(14)

        lay.addWidget(page_title(t("settings.rag.title")))

        # --- 卡片一：模型路径 -------------------------------------------
        top_card, top = card()
        top.addWidget(field_label(t("settings.rag.ollama")))
        row = QHBoxLayout()
        row.setSpacing(8)
        row.addWidget(field_input(t("settings.rag.ollama_placeholder")), 1)
        row.addWidget(icon_button("folder", t("common.browse")))
        top.addLayout(row)

        top.addWidget(field_label(t("settings.rag.embedding")))
        row = QHBoxLayout()
        row.setSpacing(8)
        row.addWidget(field_input(t("settings.rag.embedding_placeholder")), 1)
        row.addWidget(icon_button("folder", t("common.browse")))
        top.addLayout(row)

        lay.addWidget(top_card)

        # --- 卡片二：知识库 ---------------------------------------------
        bottom_card, bottom = card()
        bottom.addWidget(field_label(t("settings.rag.folder")))

        folder_row = QHBoxLayout()
        folder_row.setSpacing(8)
        folder_row.addWidget(field_input(t("settings.rag.folder_placeholder")), 1)
        folder_row.addWidget(small_button(t("common.choose")))
        folder_row.addWidget(small_button(t("common.edit")))
        bottom.addLayout(folder_row)

        bottom.addWidget(field_label(t("settings.rag.file_list")))
        bottom.addWidget(field_list([t("settings.rag.file_empty")]), 1)

        rebuild_row = QHBoxLayout()
        rebuild_row.setSpacing(10)
        rebuild_row.addWidget(small_button(t("settings.rag.rebuild")))
        rebuild_row.addStretch(1)
        status = QLabel(t("settings.rag.status"))
        status.setObjectName("hintText")
        rebuild_row.addWidget(status)
        bottom.addLayout(rebuild_row)

        lay.addWidget(bottom_card, 1)


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

    # (图标, 文案 key, 页面类)
    PAGES = [
        ("key", "settings.nav.api_key", ApiKeyPage),
        ("user", "settings.nav.personality", PersonalityPage),
        ("doc", "settings.nav.rag", RagPage),
        ("live2d", "settings.nav.live2d", Live2DModelPage),
        ("clapper", "settings.nav.theme", ThemePage),
        ("gear", "settings.nav.other", OtherPage),
    ]

    def __init__(self, parent=None, character=None):
        super().__init__(parent)
        self.character = character          # 给 Live2D model 页用（可为 None）
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
                self.stack.addWidget(page_cls(character))
            else:
                self.stack.addWidget(page_cls())
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

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

from PySide6.QtCore import QSize, Qt
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import (
    QButtonGroup,
    QCheckBox,
    QDialog,
    QFrame,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QListWidget,
    QPushButton,
    QStackedWidget,
    QVBoxLayout,
    QWidget,
)

from dsai4431_chatbot.core.gui import theme
from dsai4431_chatbot.core.gui.main_window import ICON_DIR, load_icon

DIALOG_W, DIALOG_H = 980, 660
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

            size = QLabel(f"{chars:,} 字符")
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
    btn.setIcon(QIcon(str(ICON_DIR / f"{icon}.svg")))
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

        lay.addWidget(page_title("API Key"))
        lay.addSpacing(6)

        lay.addWidget(field_label("API"))
        lay.addWidget(field_input("例：https://api.deepseek.com"))

        lay.addSpacing(6)
        lay.addWidget(field_label("Token"))
        lay.addWidget(field_input("粘贴你的 API Token"))

        lay.addStretch(1)


class PersonalityPage(QWidget):
    """人格编辑页：左「Persona 列表」，右「New Persona」表单。"""

    def __init__(self, parent=None):
        super().__init__(parent)

        lay = QVBoxLayout(self)
        lay.setContentsMargins(28, 24, 28, 24)
        lay.setSpacing(14)

        lay.addWidget(page_title("人格编辑"))

        body = QHBoxLayout()
        body.setSpacing(16)

        # --- 左：Persona 列表 -------------------------------------------
        left_card, left = card()
        left.setSpacing(8)
        left.addWidget(section_title("Persona 列表"))
        left.addWidget(
            field_list(["大肥鱼（默认）", "测试人格"], min_height=90), 1
        )
        left.addWidget(small_button("+ New"), 0, Qt.AlignmentFlag.AlignLeft)
        left_card.setFixedWidth(260)
        body.addWidget(left_card)

        # --- 右：New Persona 表单 ---------------------------------------
        right_card, right = card()
        right.addWidget(section_title("New Persona"))

        right.addWidget(field_label("ID"))
        right.addWidget(field_input("persona_id"))

        right.addWidget(field_label("NAME"))
        right.addWidget(field_input("显示名称"))

        right.addWidget(field_label("Persona Files"))
        right.addWidget(field_input("人格文件所在目录"))

        path_row = QHBoxLayout()
        path_row.setSpacing(8)
        path_row.addWidget(small_button("choose"))
        path_row.addWidget(small_button("edit"))
        path_row.addStretch(1)
        right.addLayout(path_row)

        right.addWidget(field_label("FileList"))
        right.addWidget(FileCheckList(scan_persona_files(PERSONA_DIR)), 1)

        footer = QHBoxLayout()
        footer.addStretch(1)
        footer.addWidget(small_button("Preview"))
        footer.addWidget(small_button("Save", primary=True))
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

        lay.addWidget(page_title("Retrieval-Augmented Generation"))

        # --- 卡片一：模型路径 -------------------------------------------
        top_card, top = card()
        top.addWidget(field_label("Ollama"))
        row = QHBoxLayout()
        row.setSpacing(8)
        row.addWidget(field_input("Ollama 可执行文件或服务地址"), 1)
        row.addWidget(icon_button("folder", "浏览（占位）"))
        top.addLayout(row)

        top.addWidget(field_label("Embedding"))
        row = QHBoxLayout()
        row.setSpacing(8)
        row.addWidget(field_input("Embedding 模型目录"), 1)
        row.addWidget(icon_button("folder", "浏览（占位）"))
        top.addLayout(row)

        lay.addWidget(top_card)

        # --- 卡片二：知识库 ---------------------------------------------
        bottom_card, bottom = card()
        bottom.addWidget(field_label("Folder"))

        folder_row = QHBoxLayout()
        folder_row.setSpacing(8)
        folder_row.addWidget(field_input("知识库目录"), 1)
        folder_row.addWidget(small_button("choose"))
        folder_row.addWidget(small_button("edit"))
        bottom.addLayout(folder_row)

        bottom.addWidget(field_label("FileList"))
        bottom.addWidget(field_list(["（还没有索引文件）"]), 1)

        rebuild_row = QHBoxLayout()
        rebuild_row.setSpacing(10)
        rebuild_row.addWidget(small_button("Full rebuild"))
        rebuild_row.addStretch(1)
        status = QLabel("索引状态：未构建")
        status.setObjectName("hintText")
        rebuild_row.addWidget(status)
        bottom.addLayout(rebuild_row)

        lay.addWidget(bottom_card, 1)


class Live2DModelPage(QWidget):
    """Live2D model 页：草图里只画了 tab，没有内容，先留空。"""

    def __init__(self, parent=None):
        super().__init__(parent)
        lay = QVBoxLayout(self)
        lay.setContentsMargins(28, 24, 28, 24)

        lay.addWidget(page_title("Live2D model"))

        hint = QLabel("草图里这一页没有内容。\n模型路径 / 显示尺寸 / 物理开关等，等确定后再画。")
        hint.setObjectName("hintText")
        hint.setAlignment(Qt.AlignmentFlag.AlignCenter)
        lay.addWidget(hint, 1)


class ThemePage(QWidget):
    """Theme 页：对应 TODO 第 6 条的换肤系统，目前只是占位。"""

    def __init__(self, parent=None):
        super().__init__(parent)
        lay = QVBoxLayout(self)
        lay.setContentsMargins(28, 24, 28, 24)

        lay.addWidget(page_title("Theme"))

        hint = QLabel("换肤系统还没做（见 TODO 第 6 条）。\n做好后这里用来选主题，含一套蓝色皮。")
        hint.setObjectName("hintText")
        hint.setAlignment(Qt.AlignmentFlag.AlignCenter)
        lay.addWidget(hint, 1)


class OtherPage(QWidget):
    """Other 页：草图里没有内容，留空占位。"""

    def __init__(self, parent=None):
        super().__init__(parent)
        lay = QVBoxLayout(self)
        lay.setContentsMargins(28, 24, 28, 24)

        lay.addWidget(page_title("Other"))

        hint = QLabel("草图里这一页没有内容。")
        hint.setObjectName("hintText")
        hint.setAlignment(Qt.AlignmentFlag.AlignCenter)
        lay.addWidget(hint, 1)


# ---------------------------------------------------------------------------
# 弹窗
# ---------------------------------------------------------------------------
class SettingsDialog(QDialog):
    """六个分页，顺序照用户给的导航清单。

    草图里前四项带图标，Theme 和 Other 没画图标 —— 这里照抄，
    所以后两项是纯文字（想要图标就把 icon 填上文件名即可）。
    """

    PAGES = [
        ("key", "API KEY", ApiKeyPage),
        ("user", "Personality", PersonalityPage),
        ("doc", "RAG", RagPage),
        ("live2d", "Live2D model", Live2DModelPage),
        (None, "Theme", ThemePage),
        (None, "Other", OtherPage),
    ]

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("设置")
        self.resize(DIALOG_W, DIALOG_H)
        self.setMinimumSize(820, 560)

        root = QHBoxLayout(self)
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(0)

        # --- 左侧导航 ---------------------------------------------------
        nav = QFrame()
        nav.setObjectName("settingsNav")
        nav.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)
        nav.setFixedWidth(NAV_W)
        nav_lay = QVBoxLayout(nav)
        nav_lay.setContentsMargins(10, 16, 10, 16)
        nav_lay.setSpacing(4)

        self._group = QButtonGroup(self)
        self._group.setExclusive(True)

        for index, (icon, text, _page) in enumerate(self.PAGES):
            btn = QPushButton(text)
            btn.setObjectName("navButton")
            if icon:  # Theme / Other 草图没画图标
                btn.setIcon(load_icon(icon))
                btn.setIconSize(QSize(ICON, ICON))
            btn.setCheckable(True)
            btn.setCursor(Qt.CursorShape.PointingHandCursor)
            btn.setChecked(index == 0)
            self._group.addButton(btn, index)
            nav_lay.addWidget(btn)

        nav_lay.addStretch(1)
        root.addWidget(nav)

        # --- 右侧分页 ---------------------------------------------------
        self.stack = QStackedWidget()
        for _icon, _text, page_cls in self.PAGES:
            self.stack.addWidget(page_cls())
        root.addWidget(self.stack, 1)

        # 唯一的行为：切页（否则其余两页看不到）
        self._group.idClicked.connect(self.stack.setCurrentIndex)

    def set_page(self, index: int) -> None:
        """给截图/调试用：直接跳到某一页。"""
        self._group.button(index).setChecked(True)
        self.stack.setCurrentIndex(index)

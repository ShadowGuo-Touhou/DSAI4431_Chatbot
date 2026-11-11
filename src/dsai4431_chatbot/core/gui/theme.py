"""界面样式表：把主题 token 填进 QSS 模板。

本文件只负责「形状」——字体、圆角、间距，以及每个控件引用哪个 token。
**具体颜色不写在这里**：配色来自 `gui/themes/*.toml`，由
`gui/themes/__init__.py` 的 ThemeManager 读出来再套进下面的模板。

加新控件时，只要在模板里用 `{token}` 引用现有 token 就行，不用管是哪套皮。
"""

from __future__ import annotations

from pathlib import Path
from typing import Mapping

ICON_DIR = Path(__file__).resolve().parent / "icons"

# QSS 的 url() 只吃文件路径（不吃 data URI），勾选标记做成一个 svg 文件引用；
# 这个图是白色描边，画在强调色底上，两套皮都不用改色。
_CHECK_SVG = (ICON_DIR / "check.svg").as_posix()
# 下拉框的小箭头。QSS 里的图片**不会被 themes 重新上色**（那是运行时换 SVG
# 文本里的 #1f2329），所以这个文件直接用中性灰 #8a9099：浅色皮和深色皮上都看得见。
_CHEVRON_SVG = (ICON_DIR / "chevron.svg").as_posix()

RADIUS_PANEL = 14
RADIUS_SMALL = 8
ROUND_BUTTON = 36              # 圆形按钮直径（顶栏）
ACTION_BUTTON = 32             # 输入卡里的操作按钮直径
ICON_SIZE = 18                 # 图标绘制尺寸
HEADER_HEIGHT = 48
SPLITTER_GAP = 24              # 左右两栏之间的距离（角色卡 ↔ 聊天列）

# 模板里用到的 token 必须全部存在，缺一个就直接报错（比 QSS 静默失效好查）
REQUIRED_TOKENS = (
    "bg",                  # 窗口底色
    "surface",             # 卡片 / 面板
    "surface_alt",         # 列表、输入框的浅一档底
    "border",              # 主描边
    "border_soft",         # 更浅的描边（输入框、列表）
    "border_dash",         # 虚线占位框
    "text",                # 正文
    "text_weak",           # 次要文字
    "text_on_accent",      # 强调色上的文字（发送按钮等）
    "accent",              # 强调色
    "accent_hover",
    "hover",               # 悬停底色
    "nav_hover",           # 设置导航悬停
    "nav_checked",         # 设置导航选中胶囊
    "selected_bg",         # 列表选中 / 主题卡选中
    "bubble_user_bg",      # 用户气泡
    "bubble_user_border",
    "check_border",        # 复选框描边
    "scroll",              # 滚动条滑块
    "scroll_hover",
    "icon",                # 图标描边
    "icon_on_accent",      # 强调色底上的图标
)

_TEMPLATE = """
QWidget {{
    color: {text};
    font-family: "Microsoft YaHei UI", "Segoe UI", sans-serif;
    font-size: 14px;
}}

QMainWindow, #windowBody {{
    background: {bg};
}}
/* QSplitter 的 handle 宽度不能用 QSS 的 width 设（实测无效，handle 会是 0，
   两栏直接贴在一起），必须在代码里 setHandleWidth()。这里只管透明。 */
QSplitter::handle {{
    background: transparent;
}}

/* 通用卡片：靠底色差和间距区分，不用描边（模仿 DSH，避免明显分界线） */
#surface {{
    background: {surface};
    border: none;
    border-radius: {radius_panel}px;
}}

/* 角色区（Live2D 待接入的占位） */
#characterPanel {{
    background: {surface};
    border: 1px dashed {border_dash};
    border-radius: {radius_panel}px;
}}
/* 模型已加载：虚线占位框去掉，只留一块卡片 */
#characterPanel[state="model"] {{
    border: none;
}}
#characterHint {{
    color: {text_weak};
    font-size: 13px;
}}

/* 圆形按钮：菜单 / 设置 / 附件 / 语音 / 发送 */
QPushButton[shape="round"] {{
    background: {surface};
    border: 1px solid {border};
    border-radius: {round_radius}px;
    padding: 0;
}}
QPushButton[shape="round"]:hover {{
    background: {hover};
}}
QPushButton[shape="round"]:pressed {{
    background: {border};
}}

/* 输入卡里的按钮小一号：圆角必须等于直径的一半才是正圆，
   32px 的按钮用 16px，不能用上面的 18px（超出一半会退化成方角） */
QPushButton[shape="round"][kind="action"] {{
    border-radius: {action_radius}px;
}}

/* 主操作按钮（发送）用强调色 */
QPushButton[shape="round"][variant="primary"] {{
    background: {accent};
    border: 1px solid {accent};
}}
QPushButton[shape="round"][variant="primary"]:hover {{
    background: {accent_hover};
    border-color: {accent_hover};
}}

/* 消息区 */
QScrollArea, #messageViewport {{
    background: transparent;
    border: none;
}}
#messageEmpty {{
    color: {text_weak};
    font-size: 14px;
}}

/* 消息气泡 */
#bubbleUser {{
    background: {bubble_user_bg};
    border: 1px solid {bubble_user_border};
    border-radius: {radius_small}px;
    padding: 10px 14px;
}}
#bubbleBot {{
    background: {surface};
    border: 1px solid {border};
    border-radius: {radius_small}px;
    padding: 10px 14px;
}}
/* 思考链气泡（第 16 条）：弱化、更小，视觉上明显不是正文 */
#bubbleReasoning {{
    background: {surface_alt};
    border: 1px dashed {border_soft};
    border-radius: {radius_small}px;
    padding: 8px 12px;
    color: {text_weak};
    font-size: 12px;
}}

/* 输入卡：一张圆角卡片把输入区和操作行包在一起（模仿 DSH） */
#inputCard {{
    background: {surface};
    border: 1px solid {border};
    border-radius: {radius_panel}px;
}}
QPlainTextEdit#inputEdit {{
    background: transparent;
    border: none;
    padding: 0;
    font-size: 14px;
    color: {text};
    selection-background-color: {accent};
}}

/* ---------- 新对话页（「新建对话」后右侧整块换成的空白首页）---------- */
#homePage {{
    background: transparent;
    border: none;
}}
#homeTitle {{
    font-size: 30px;
    font-weight: 600;
}}
/* 首页的大输入卡：和输入卡同一个形状，只是更高 */
#homeCard {{
    background: {surface};
    border: 1px solid {border};
    border-radius: {radius_panel}px;
}}
QPlainTextEdit#homeEdit {{
    background: transparent;
    border: none;
    padding: 2px;
    font-size: 15px;
    color: {text};
    selection-background-color: {accent};
}}

/* 人格选择器：一颗圆角胶囊（图标 + 名字 + 细箭头），
   不要系统默认那种「左边文字、右边一个带方框的三角按钮」的样子。
   底色用 chip_bg（比页面底色深/亮一档），才看得出形状 */
QComboBox#homePersona {{
    background: {chip_bg};
    border: 1px solid {border};
    border-radius: 11px;
    padding: 6px 4px 6px 12px;
    color: {text};
    font-size: 14px;
}}
QComboBox#homePersona:hover {{
    background: {chip_bg_hover};
}}
QComboBox#homePersona:on {{
    border-color: {accent};
}}
/* 模型选择器：输入卡右下角的一行小字，悬停才浮出底色（DSH 就是这种轻量做法） */
QComboBox#homeModel {{
    background: transparent;
    border: none;
    border-radius: 8px;
    padding: 4px 4px 4px 8px;
    color: {text_weak};
    font-size: 13px;
}}
QComboBox#homeModel:hover {{
    background: {hover};
    color: {text};
}}
/* 箭头自绘：drop-down 的方框去掉，只留一张图片 */
QComboBox#homePersona::drop-down,
QComboBox#homeModel::drop-down {{
    background: transparent;
    border: none;
    width: 20px;
}}
QComboBox#homePersona::down-arrow,
QComboBox#homeModel::down-arrow {{
    image: url("{chevron_svg}");
    width: 12px;
    height: 12px;
}}
/* 展开后的候选列表：别用系统那种贴边的白框。
   ⚠ 这里**不能画圆角**：弹窗是独立的原生窗口，它的 palette Window 是纯黑
   （#000000），item view 一圆角，四个角就露出黑色方块（2026-11-11 实测） */
QComboBox#homePersona QAbstractItemView,
QComboBox#homeModel QAbstractItemView {{
    background: {surface};
    border: 1px solid {border_soft};
    padding: 4px;
    outline: none;
    selection-background-color: {selected_bg};
    selection-color: {accent};
}}
QComboBox#homePersona QAbstractItemView::item,
QComboBox#homeModel QAbstractItemView::item {{
    min-height: 26px;
    padding: 2px 8px;
    border-radius: 6px;
}}
QComboBox#homePersona QAbstractItemView {{
    icon-size: 16px;
}}

/* ---------- 设置弹窗 ---------- */
/* 无边框窗口：圆角画在 shell 上（窗口本身透明，四周留出投影边距） */
#settingsShell {{
    background: {surface};
    border: 1px solid {border};
    border-radius: 16px;
}}
#settingsTitle {{
    font-size: 16px;
    font-weight: 600;
}}
/* 导航区不画分隔线：和内容区同底色，靠胶囊选中态与间距区分 */
#settingsNav {{
    background: transparent;
    border: none;
}}
QPushButton#navButton {{
    text-align: left;
    padding: 9px 12px;
    border: none;
    border-radius: 9px;
    background: transparent;
    color: {text};
}}
QPushButton#navButton:hover {{
    background: {nav_hover};
}}
QPushButton#navButton:checked {{
    background: {nav_checked};
    color: {text};
}}

#pageTitle {{
    font-size: 18px;
    font-weight: 600;
}}
#sectionTitle {{
    font-size: 14px;
    font-weight: 600;
}}
QLabel#fieldLabel {{
    color: {text_weak};
    font-size: 13px;
}}
#hintText {{
    color: {text_weak};
}}

QLineEdit#field {{
    background: {surface};
    border: 1px solid {border_soft};
    border-radius: 9px;
    padding: 8px 11px;
    selection-background-color: {accent};
}}
QLineEdit#field:focus {{
    border-color: {accent};
}}
/* Preview 的只读文本框：和 QLineEdit 同一套外观。
   font-size 必须显式写 —— QPlainTextEdit 不认 #field 里继承来的字号，
   不写会落回系统默认（实测渲染成宋体、比别的控件大一号）。 */
QPlainTextEdit#field {{
    background: {surface};
    border: 1px solid {border_soft};
    border-radius: 9px;
    padding: 8px 11px;
    color: {text};
    font-size: 14px;
    selection-background-color: {accent};
}}

QListWidget#fieldList {{
    background: {surface_alt};
    border: 1px solid {border_soft};
    border-radius: 9px;
    padding: 4px;
}}
QListWidget#fieldList::item {{
    padding: 6px 8px;
    border-radius: 6px;
}}
QListWidget#fieldList::item:selected {{
    background: {selected_bg};
    color: {accent};
}}

/* 会话抽屉：独立无边框窗口（QWebEngineView 是原生子窗口，会把同级控件盖住），
   所以不能画圆角 —— 窗口四角会露出底色 */
QFrame#sessionDrawer {{
    background: {surface};
    border: 1px solid {border_soft};
}}
QFrame#newSessionForm {{
    background: {surface_alt};
    border: 1px solid {border_soft};
    border-radius: 9px;
}}
QListWidget#sessionList {{
    background: transparent;
    border: none;
    padding: 0;
}}
QListWidget#sessionList::item {{
    padding: 5px 8px;
    border-radius: 6px;
    color: {text};
}}
QListWidget#sessionList::item:hover {{
    background: {hover};
}}
QListWidget#sessionList::item:selected {{
    background: {selected_bg};
    color: {accent};
}}

/* 勾选式文件清单（Personality 页）：勾选框 + 文件名 + 字符数
   外框画在滚动区上（滚动条才会在框内），里面的 #fileList 当透明容器 */
QScrollArea#fileListScroll {{
    background: {surface_alt};
    border: 1px solid {border_soft};
    border-radius: 9px;
}}
QScrollArea#fileListScroll > QWidget > QWidget {{
    background: transparent;
}}
QFrame#fileList {{
    background: transparent;
    border: none;
}}
QFrame#fileList > QFrame#fileRow {{
    background: transparent;
    border: none;
    border-radius: 6px;
}}
QFrame#fileList > QFrame#fileRow:hover {{
    background: {hover};
}}
QCheckBox#fileCheck {{
    spacing: 10px;
}}
QCheckBox#fileCheck::indicator {{
    width: 15px;
    height: 15px;
    border: 1px solid {check_border};
    border-radius: 4px;
    background: {surface};
}}
QCheckBox#fileCheck::indicator:hover {{
    border-color: {accent};
}}
QCheckBox#fileCheck::indicator:checked {{
    background: {accent};
    border-color: {accent};
    image: url("{check_svg}");
}}
QLabel#fileSize {{
    color: {text_weak};
    font-size: 12px;
}}

QPushButton#smallButton {{
    background: {surface};
    border: 1px solid {border_soft};
    border-radius: 9px;
    padding: 7px 15px;
}}
QPushButton#smallButton:hover {{
    background: {hover};
}}
QPushButton#smallButton[variant="primary"] {{
    background: {accent};
    border-color: {accent};
    color: {text_on_accent};
}}
QPushButton#smallButton[variant="primary"]:hover {{
    background: {accent_hover};
}}
/* 禁用态要看得出来：默认人格那页的按钮全是灰的，没有这条会和能点的一模一样 */
QPushButton#smallButton:disabled {{
    background: {surface_alt};
    border-color: {border_soft};
    color: {text_weak};
}}
QPushButton#smallButton[variant="primary"]:disabled {{
    background: {chip_bg};
    border-color: {chip_bg};
    color: {text_weak};
}}
QCheckBox#fileCheck:disabled {{
    color: {text_weak};
}}
QCheckBox#fileCheck::indicator:disabled {{
    background: {surface_alt};
    border-color: {border_soft};
}}
/* 锁住的但已经勾上的：要看出"它是选中的、只是不能改"，
   否则只看截图会以为一个都没勾 */
QCheckBox#fileCheck::indicator:checked:disabled {{
    background: {chip_bg_hover};
    border-color: {accent};
}}

QPushButton#iconButton {{
    background: {surface};
    border: 1px solid {border_soft};
    border-radius: 9px;
}}
QPushButton#iconButton:hover {{
    background: {hover};
}}

/* ---------- 主题选择（Theme 页） ---------- */
QFrame#themeCard {{
    background: {surface};
    border: 1px solid {border_soft};
    border-radius: 12px;
}}
QFrame#themeCard:hover {{
    border-color: {border};
}}
/* 选中的卡用强调色描边 + 淡色底，不用加粗边框（否则卡片会跳一下） */
QFrame#themeCard[selected="true"] {{
    border: 1px solid {accent};
    background: {selected_bg};
}}
QLabel#themeName {{
    font-size: 14px;
    font-weight: 600;
}}
QLabel#themeNote {{
    color: {text_weak};
    font-size: 12px;
}}

/* 滑条 / 下拉框（Live2D model 页用） */
QSlider::groove:horizontal {{
    height: 4px;
    background: {border};
    border-radius: 2px;
}}
QSlider::sub-page:horizontal {{
    background: {accent};
    border-radius: 2px;
}}
QSlider::handle:horizontal {{
    width: 14px;
    height: 14px;
    margin: -6px 0;
    border-radius: 7px;
    background: {accent};
    border: none;
}}
QSlider::handle:horizontal:hover {{
    background: {accent_hover};
}}
QComboBox {{
    background: {surface};
    border: 1px solid {border_soft};
    border-radius: 9px;
    padding: 6px 10px;
}}
QComboBox:hover {{
    border-color: {border};
}}
QComboBox QAbstractItemView {{
    background: {surface};
    border: 1px solid {border_soft};
    selection-background-color: {selected_bg};
    selection-color: {accent};
    outline: none;
}}

/* 滚动条：细一点，别抢视线 */
QScrollBar:vertical {{
    background: transparent;
    width: 8px;
    margin: 0;
}}
QScrollBar::handle:vertical {{
    background: {scroll};
    border-radius: 4px;
    min-height: 30px;
}}
QScrollBar::handle:vertical:hover {{
    background: {scroll_hover};
}}
QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
    height: 0;
}}
QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {{
    background: transparent;
}}
/* 横向滚动条同理（文件清单 / 长行时会出现） */
QScrollBar:horizontal {{
    background: transparent;
    height: 8px;
    margin: 0;
}}
QScrollBar::handle:horizontal {{
    background: {scroll};
    border-radius: 4px;
    min-width: 30px;
}}
QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal {{
    width: 0;
}}
QScrollBar::add-page:horizontal, QScrollBar::sub-page:horizontal {{
    background: transparent;
}}
"""


def stylesheet(palette: Mapping[str, str]) -> str:
    """把一套配色塞进 QSS 模板。缺 token 直接抛错，别让样式静默失效。"""
    missing = [k for k in REQUIRED_TOKENS if not palette.get(k)]
    if missing:
        raise KeyError(f"主题缺少 token：{', '.join(missing)}")
    values = dict(palette)
    # 后加的 token：老主题文件里没有也不该崩，退回最接近的现有色
    values.setdefault("chip_bg", values.get("surface_alt") or values["surface"])
    values.setdefault("chip_bg_hover", values.get("hover") or values["surface"])
    values.update(
        radius_panel=RADIUS_PANEL,
        radius_small=RADIUS_SMALL,
        round_radius=ROUND_BUTTON // 2,
        action_radius=ACTION_BUTTON // 2,
        splitter_gap=SPLITTER_GAP,
        check_svg=_CHECK_SVG,
        chevron_svg=_CHEVRON_SVG,
    )
    return _TEMPLATE.format(**values)

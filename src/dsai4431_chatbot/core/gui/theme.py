"""界面样式表。

所有视觉参数集中在这里，改配色/圆角/间距不用翻组件代码。
配色刻意保持中性，方便后面换成主题系统。
"""

from __future__ import annotations

# 设计基准：参考 asset/plan/main interface.png 的手绘线框
COLOR_BG = "#f2f3f5"          # 窗口底色
COLOR_SURFACE = "#ffffff"      # 卡片/面板
COLOR_BORDER = "#e2e4e8"       # 描边
COLOR_BORDER_DASH = "#c8ccd4"  # 虚线（占位区）
COLOR_TEXT = "#1f2329"
COLOR_TEXT_WEAK = "#8a9099"
COLOR_ACCENT = "#3b7ddd"       # 强调色：发送按钮等
COLOR_ACCENT_HOVER = "#2f6bc4"
COLOR_HOVER = "#f0f1f3"        # 圆形按钮悬停底色

RADIUS_PANEL = 14
RADIUS_SMALL = 8
ROUND_BUTTON = 36              # 圆形按钮直径（顶栏）
ACTION_BUTTON = 32             # 输入卡里的操作按钮直径
ICON_SIZE = 18                 # 图标绘制尺寸
HEADER_HEIGHT = 48

STYLESHEET = f"""
QWidget {{
    color: {COLOR_TEXT};
    font-family: "Microsoft YaHei UI", "Segoe UI", sans-serif;
    font-size: 14px;
}}

QMainWindow, #windowBody {{
    background: {COLOR_BG};
}}
QSplitter::handle {{
    background: transparent;
    width: 12px;
}}

/* 通用卡片：靠底色差和间距区分，不用描边（模仿 DSH，避免明显分界线） */
#surface {{
    background: {COLOR_SURFACE};
    border: none;
    border-radius: {RADIUS_PANEL}px;
}}

/* 角色区（Live2D 待接入的占位） */
#characterPanel {{
    background: {COLOR_SURFACE};
    border: 1px dashed {COLOR_BORDER_DASH};
    border-radius: {RADIUS_PANEL}px;
}}
#characterHint {{
    color: {COLOR_TEXT_WEAK};
    font-size: 13px;
}}

/* 圆形按钮：菜单 / 设置 / 附件 / 语音 / 发送 */
QPushButton[shape="round"] {{
    background: {COLOR_SURFACE};
    border: 1px solid {COLOR_BORDER};
    border-radius: {ROUND_BUTTON // 2}px;
    padding: 0;
}}
QPushButton[shape="round"]:hover {{
    background: {COLOR_HOVER};
}}
QPushButton[shape="round"]:pressed {{
    background: {COLOR_BORDER};
}}

/* 输入卡里的按钮小一号：圆角必须等于直径的一半才是正圆，
   32px 的按钮用 16px，不能用上面的 18px（超出一半会退化成方角） */
QPushButton[shape="round"][kind="action"] {{
    border-radius: {ACTION_BUTTON // 2}px;
}}

/* 主操作按钮（发送）用强调色 */
QPushButton[shape="round"][variant="primary"] {{
    background: {COLOR_ACCENT};
    border: 1px solid {COLOR_ACCENT};
}}
QPushButton[shape="round"][variant="primary"]:hover {{
    background: {COLOR_ACCENT_HOVER};
    border-color: {COLOR_ACCENT_HOVER};
}}

/* 消息区 */
QScrollArea, #messageViewport {{
    background: transparent;
    border: none;
}}
#messageEmpty {{
    color: {COLOR_TEXT_WEAK};
    font-size: 14px;
}}

/* 消息气泡 */
#bubbleUser {{
    background: #e8f1ff;
    border: 1px solid #d3e3fb;
    border-radius: {RADIUS_SMALL}px;
    padding: 10px 14px;
}}
#bubbleBot {{
    background: {COLOR_SURFACE};
    border: 1px solid {COLOR_BORDER};
    border-radius: {RADIUS_SMALL}px;
    padding: 10px 14px;
}}

/* 输入卡：一张圆角卡片把输入区和操作行包在一起（模仿 DSH） */
#inputCard {{
    background: {COLOR_SURFACE};
    border: 1px solid {COLOR_BORDER};
    border-radius: {RADIUS_PANEL}px;
}}
QPlainTextEdit#inputEdit {{
    background: transparent;
    border: none;
    padding: 0;
    font-size: 14px;
    color: {COLOR_TEXT};
    selection-background-color: {COLOR_ACCENT};
}}

/* ---------- 设置弹窗 ---------- */
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
    color: {COLOR_TEXT};
}}
QPushButton#navButton:hover {{
    background: #e9ebee;
}}
QPushButton#navButton:checked {{
    background: #e3e7ec;
    color: {COLOR_TEXT};
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
    color: {COLOR_TEXT_WEAK};
    font-size: 13px;
}}
#hintText {{
    color: {COLOR_TEXT_WEAK};
}}

QLineEdit#field {{
    background: {COLOR_SURFACE};
    border: 1px solid #ebedf0;
    border-radius: 9px;
    padding: 8px 11px;
    selection-background-color: {COLOR_ACCENT};
}}
QLineEdit#field:focus {{
    border-color: {COLOR_ACCENT};
}}

QListWidget#fieldList {{
    background: #fafbfc;
    border: 1px solid #f0f1f3;
    border-radius: 9px;
    padding: 4px;
}}
QListWidget#fieldList::item {{
    padding: 6px 8px;
    border-radius: 6px;
}}
QListWidget#fieldList::item:selected {{
    background: #e8f1ff;
    color: {COLOR_ACCENT};
}}

QPushButton#smallButton {{
    background: {COLOR_SURFACE};
    border: 1px solid #ebedf0;
    border-radius: 9px;
    padding: 7px 15px;
}}
QPushButton#smallButton:hover {{
    background: {COLOR_HOVER};
}}
QPushButton#smallButton[variant="primary"] {{
    background: {COLOR_ACCENT};
    border-color: {COLOR_ACCENT};
    color: #ffffff;
}}
QPushButton#smallButton[variant="primary"]:hover {{
    background: {COLOR_ACCENT_HOVER};
}}

QPushButton#iconButton {{
    background: {COLOR_SURFACE};
    border: 1px solid #ebedf0;
    border-radius: 9px;
}}
QPushButton#iconButton:hover {{
    background: {COLOR_HOVER};
}}

/* 滚动条：细一点，别抢视线 */
QScrollBar:vertical {{
    background: transparent;
    width: 8px;
    margin: 0;
}}
QScrollBar::handle:vertical {{
    background: #cdd1d8;
    border-radius: 4px;
    min-height: 30px;
}}
QScrollBar::handle:vertical:hover {{
    background: #b6bbc4;
}}
QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
    height: 0;
}}
QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {{
    background: transparent;
}}
"""

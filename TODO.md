# TODO / 待改清单

记录已确认但尚未实现的需求，攒够了一次性做。
新增条目请写清「谁定的、当时怎么说的」，避免以后重复确认。

最后更新：2026-11-11 15:21

---

## 一、已确认，待实现

### 1. 顶栏左侧 `≡` 按钮 → 打开会话列表

- **决策人**：用户（2026-11-11），原话「打开会话列表」
- **现状**：`core/gui/main_window.py` 里 `btn_menu` 只发 `menu_requested` 信号，
  `MainWindow` 没连槽，点了没有任何反应 —— 是纯占位
- **要做**：点击展开/收起会话列表抽屉（历史会话 + 新建会话入口）
- **注意**：这个按钮是线框里画的圆，但图形太草，功能是**后定的**，不是从图上读出来的

### 2. 图标 —— 已完成（手绘等价件，可替换）

- **状态**：已产出 `core/gui/icons/` 下 5 个 SVG：`plus` / `mic` / `gear` / `send` / `menu`
- **说明**：DSH 的界面图标**不是图片素材**，是内联在 React 里的 SVG 组件；它 asar 的
  `renderer/` 只有欢迎页和更新弹窗两个 SVG，主界面 bundle 需要带 token 的 URL 才能取。
  所以这些图标是按同一视觉语言（细描边、圆角端点）手绘的等价件
- **待办**：如果拿到正式素材，替换同名 SVG 即可，代码不用动（`load_icon()` 按名字加载）

### 3. 设置窗口 —— 布局已完成，待接功能

- **状态**：`core/gui/settings_dialog.py` 已渲染出**六个分页**的布局，
  `MainWindow.open_settings()` 已改为打开这个弹窗。**没有任何业务逻辑**：
  所有按钮都是空壳，唯一的行为是左侧导航切换分页
- **导航（顺序照用户 2026-11-11 给的清单）**：
  `API KEY` / `Personality` / `RAG` / `Live2D model` / `Theme` / `Other`
  - 前四项带图标，`Theme` 和 `Other` 草图没画图标 → 目前是纯文字
- **已完成内容的页**：API KEY、Personality、RAG（按三张草图铺好字段）
- **空占位页**：Live2D model、Theme、Other（草图只有 tab，没有内容）
- **待办**：
  - RAG 页底部草图还画着两个小控件（一串点和一个小圆角框），看不清是什么，
    现在只放了一个「索引状态：未构建」文字占位
  - API KEY 页草图没有页面标题，为了三页对齐补了「API Key」标题
  - `Theme` 页将来接 TODO 第 6 条的换肤系统
- **依据**：`asset/plan/setting-api_key.png`、`setting-persona.png`、`setting-RAG.png`
  （人格编辑页含 New Persona 表单：ID / NAME / Persona Files / Both-Close-Edit / FileList，
  以及 Persona 列表 + `+New`、Save / Preview）

### 4. Live2D 角色区接入

- **现状**：`CharacterPanel` 只有一行提示文字，是空占位
- **要做**：嵌入 `QWebEngineView`，加载 `asset/live2d` 的渲染页
- **参考**：`core/live2d/demo_interactive.py` 的 `Stage`（本地 HTTP + `/vendor/` `/model/` 路由）
- **注意**：`--no-sandbox` 等环境变量必须在创建 `QApplication` **之前**设置，
  见 `core/live2d/HANDOFF.md` §3.1

### 5. 对话后端

- **现状**：`ChatColumn._on_submit()` 只把用户输入回显成气泡，没有回复
- **要做**：接真实对话后端，回复用 `messages.add_message("bot", ...)` 追加

### 6. 主题 / 换肤系统 + 一套蓝色皮

- **决策人**：用户（2026-11-11），原话「后续可以通过加载不同预设改页面样貌吗」
  +「添加一个蓝色的皮。就是你自己的配色」
- **要做**：把 `theme.py` 里的常量抽成 token 集，做 `ThemeManager`，支持运行时切换
  （`app.setStyleSheet()` 是热替换的，不用重启），选择写进配置文件、启动时读取
- **建议结构**

  ```
  core/gui/themes/
  ├── __init__.py      # ThemeManager：加载 token → 套 QSS 模板 → setStyleSheet → 重刷图标
  ├── light.toml       # 现在的浅色（默认）
  ├── dark.toml
  └── deepseek-blue.toml   # 蓝色皮
  ```

- **蓝色皮配色（待细化）**：主色用 DeepSeek 品牌蓝 `#4D6BFE`，
  深色底 `#0F1115`、卡片 `#171A21`、描边 `#262B33`、正文 `#E6E8EC`、正文弱 `#8B93A1`
- **两个已知坑（务必处理）**
  1. **图标不会自动跟着变色**：SVG 里 `stroke` 是写死的，深色皮下会看不见。
     要读 SVG 文本→替换颜色→`QSvgRenderer` 渲染成 pixmap（别落临时文件）
  2. **动态属性变了必须重新 polish**：改完 `setProperty` 要
     `widget.style().unpolish(w); widget.style().polish(w)`，否则样式不更新
- **时机建议**：等界面控件定型后再抽。现在抽，后面每加一个控件都要回来改模板

---

## 二、待用户决定

### 7. `asset/plan/` 那 4 张设计图（共约 21 MB）要不要入库

- 目前未提交。是设计源图，体积偏大但不算离谱
- 用户尚未表态

### 8. `_plan_preview/` 临时目录

- 里面是界面渲染截图和放大用的裁剪图
- 属于临时产物，确认可以删就删

---

## 三、杂物 / 外部事项

### 9. 未提交的改动

截至本文档更新时，工作区未提交的内容：
- 新增：`src/dsai4431_chatbot/core/gui/`（含 `icons/` 5 个 SVG）、`启动GUI.bat`（项目根）、
  `asset/plan/`、`_plan_preview/`、`TODO.md`
- 修改：`pyproject.toml`（新增 `gui` 可选依赖组）、`README.md`（新增「主界面 GUI」小节）

### 10. 旧目录 `P:\Deekseek_playground\live2d-python-demo`

- 用户明确说「先别删了，到时候我自己处理」
- 内容已完整迁入本项目，占地 506 MB（含隐藏的 `.git`）

---

## 四、已确认的设计决策（别再重复问）

| 项目 | 结论 | 时间 |
|---|---|---|
| GUI 技术栈 | **PySide6（Qt6）原生控件**；2026-11-11 从 PyQt5 迁来（LGPL + Qt6 的 WebEngine 比 Qt5 的 Chromium 83 新得多）。Live2D 后续用 QWebEngineView 嵌入 | 2026-11-11 |
| `≡` 按钮职责 | 打开会话列表 | 2026-11-11 |
| 主界面布局 | 左栏 Live2D 角色区 + 右侧聊天列（顶栏 / 消息区 / 输入卡） | 2026-11-11 |
| 输入卡形态 | 模仿 DSH：输入区 + 操作行**同一张圆角卡片**，附件在左、语音发送在右 | 2026-11-11 |
| 换肤方向 | 做 QSS 预设系统，另加一套蓝色皮 | 2026-11-11 |

---

## 五、看图须知

`asset/plan/` 下的 4 张线框图是**竖着拍的**，需要**顺时针旋转 90°** 才是正常阅读方向。
（`core/live2d/HANDOFF.md` 里也提过类似问题，看图前先转正，别像我一样按正着的读了一遍。）

---

## 六、QSS 能力边界（给以后换肤的人看）

PyQt5 只支持 **QSS**，是 CSS 的子集：

| 支持 | 类型/`#objectName`/属性选择器 `[shape="round"]`/后代选择器；`:hover :pressed :checked :focus :disabled`；`background` `border` `border-radius` `padding` `margin` `color` `font-*`；`qlineargradient` |
|---|---|
| **不支持** | `box-shadow`（用 `QGraphicsDropShadowEffect`）、`transition`/`animation`/`@keyframes`（用 `QPropertyAnimation`）、`var()` CSS 变量（只能在 Python 侧拼字符串）、`::before`/`::after`/`content`、`flex`/`grid`（布局只能 QLayout）、`calc()`、`!important` |

另外两个已经踩过的坑：
- 普通 `QWidget` 子类默认忽略 QSS 的 `background`/`border`，必须
  `setAttribute(Qt.WA_StyledBackground, True)`；
- 动态属性的**名字不能撞** Qt 自带属性。比如用 `setProperty("size", ...)` 会静默失败
  （`QWidget.size` 是 QSize 类型，转换不过去），导致 `[size="action"]` 规则永不生效。
  现改用 `kind`。

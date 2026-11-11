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

### 3. 设置窗口 —— 三页已接配置落盘（Live2D / Theme / 其他页早就完成）

- **状态（2026-11-11 更新）**：六个分页都能用。API KEY / Personality / RAG 三页
  **改完自动存**进 `settings.ini`（没有"保存"按钮，和换肤、Live2D 页一个套路）；
  Live2D model 页、Theme 页之前就接了
  - API KEY：地址 / Key（密码框）/ 模型；Key 明文存在本机 ini（用户在选项里确认过）
  - Personality：人格目录（可 choose 选目录 / edit 打开目录 / 重新扫描）+ 勾选文件，
    勾选结果落盘并作为对话的 system 提示词；Preview 直接看拼出来的全文
    - 文件清单是**滚动区**（`FileCheckList` 继承 QScrollArea，2026-11-11 补）：
      之前用 QFrame 手工排行，文件一多就被卡片裁掉、下面的点不到
    - 坑：`set_rows()` 被调两次（构造一次 + `_load_files()` 一次）时，旧行
      `deleteLater()` 要等事件循环才消失，期间会和新行**叠着画**（截图里两行文字糊成一团）
      → 先 `setParent(None)` 再 deleteLater；另外构造时传空列表，只让 `_load_files()` 填一次
  - RAG：三条路径落盘 + 目录里的文件清单（带大小）；「Full rebuild」是灰的 ——
    索引还没实现，不做假按钮
- **外观与交互（2026-11-11 照 DSH 改）**
  - 无边框 + 圆角（`#settingsShell` 16px）+ 外投影；窗口本身透明，四周留 18px 给投影
  - 顶部有「设置」标题 + `×` 关闭按钮（`icons/close.svg`）
  - **不可拖动**：无边框后没有标题栏，也没实现拖动
  - **点框外关闭**：对话框必须是 **modeless**（模态会把外部点击吃掉），
    在 `QApplication` 上装事件过滤器，判断按下的全局坐标是否在 `frameGeometry()` 外
  - Esc 也能关（QDialog 默认）
- **导航（顺序照用户 2026-11-11 给的清单）**：
  `API KEY` / `Personality` / `RAG` / `Live2D model` / `Theme` / `Other`
  - 前四项带图标，`Theme` 和 `Other` 草图没画图标 → 目前是纯文字
- **已完成内容的页**：API KEY、Personality、RAG（按三张草图铺好字段）
- **Live2D model 页（2026-11-11 实现，不再是占位）**
  - 左：`asset/live2d/models` 扫出来的模型列表（现 4 个 `*.model3.json`），选中即换模型
    （重新装载渲染页，约 3 秒）
  - 右：取景（上半身/全身）、缩放 40–250%、左右/上下偏移 ±300px、
    行为开关（物理 / 自动眨眼 / 呼吸 / 视线跟随）
  - 部件显隐：`l2d.parts()` 拿部件清单做勾选列表，取消勾选 = 隐藏
  - 全部改动立即生效并存盘（`live2d_config.py`，与换肤共用 `settings.ini`）
  - 已知限制：部件 id 来自 moc3，这个模型就叫 `PartNN`（model3 里没有 `Parts`
    命名表），所以列表只能按「绘制单元数」排序；被别的部件盖住的部件
    勾掉也看不出变化（实测只藏 Part48 几乎无变化，藏前 5 大部件掉 14% 像素）
- **Personality 页文件清单（2026-11-11 补）**：改成「勾选框 + 文件名 + 字符数」的
  `FileCheckList`，数据从 `P:\.dsh\agentsoul` 实扫（可用环境变量
  `DSAI_PERSONA_DIR` 改目录），目录不存在时退回演示数据。
  勾选状态目前只存在控件里，不落盘
- **Other 页（2026-11-11）**：原本是空占位，现在放「界面语言」切换（中文 / English），
  见第 11 条
- **待办**：
  - RAG 页底部草图还画着两个小控件（一串点和一个小圆角框），看不清是什么，
    现在只放了一个「索引状态：未构建」文字占位
  - API KEY 页草图没有页面标题，为了三页对齐补了「API Key」标题
  - `Theme` 页将来接 TODO 第 6 条的换肤系统
- **依据**：`asset/plan/setting-api_key.png`、`setting-persona.png`、`setting-RAG.png`
  （人格编辑页含 New Persona 表单：ID / NAME / Persona Files / Both-Close-Edit / FileList，
  以及 Persona 列表 + `+New`、Save / Preview）

### 4. Live2D 角色区接入 —— 已完成（内嵌并实测渲染成功）

- **状态**：`CharacterPanel` 已内嵌 `Live2DView`（`core/gui/live2d_embed.py`，458 行），
  加载 `asset/live2d` 的渲染页并显示大肥鱼；模型就绪后虚线占位框自动去掉
  （`#characterPanel[state="model"]`）。加载失败/超时会摘掉 view、退回占位文字 + 一行诊断
- **实测数据**（Qt6.12）：`loadFinished` 0.4–1.2s，`window.l2dReady` 2.2–3.0s，
  console 无报错（只有黑层修复的预期 warn）
- **⚠ `--no-sandbox` 在 Qt6 下仍然必需**：不加就渲染进程 `code=18` 死掉、
  `loadFinished` 永不触发（与 Qt5 同症状）；只加 `--disable-gpu` 也没用。
  现在模块默认设置它，想收回控制用 `L2D_KEEP_SANDBOX=1`，
  额外加 flag 用 `L2D_CHROMIUM_FLAGS`
- **Qt6 顺带解决了的老坑**：`HANDOFF.md` §3.4「Chromium 83 没有顶层 await」在
  Chromium 140 下已不成立；§4.1 的 Core6 `renderOrders` 崩溃也不会触发
  （vendor 里实际是 Cubism Core 5.1）
- **对外接口备好但未接业务**：`CharacterPanel.react() / stop_reaction() / snapshot()`
- **取景**：默认 `framing=bust`（上半身特写，宽度铺满、头顶留白、下方裁掉），
  `zoom=1.9` 是照用户给的裁剪参考图定的。想换成全身或调远近不用改代码：
  `$env:L2D_FRAMING="full"` / `$env:L2D_ZOOM="1.5"`
  （渲染页 `demo_live2d.html` 支持 `?framing=bust&zoom=1.9&top=0.02`，默认仍是 full，
  所以旧 PyQt5 demo 行为不变）

### 4b. 角色区虚线边框（已解决，记录用）

模型加载成功后不再需要占位虚线框，已用 QSS 状态属性
`#characterPanel[state="model"] { border: none; }` 处理，
失败时自动退回虚线态。改这个属性必须 `unpolish/polish`，见第六节的坑。

### 5. 对话后端 —— 已完成（流式）

- **用户要求（2026-11-11）**：「接对话后端」+「设置页的输入落盘」
- **已完成**
  - `chat_config.py`：`base_url` / `api_key` / `model` / 人格目录 / 人格文件 / RAG 三条路径，
    全部存 `settings.ini` 的 `[chat]` 段。`endpoint()` 认三种填法
    （`…/`、`…/v1`、`…/v1/chat/completions`）
  - `chat_client.py`：OpenAI 兼容 `/chat/completions`，**流式 SSE**，用
    `QNetworkAccessManager`（不引第三方库、不开线程）。三种收尾都处理：
    正常流式 / 网关直接回整包 JSON / 出错（HTTP 状态 + 服务端 `error.message` 一起给）
  - 主窗：用户气泡 → 空机器人气泡（先显示「正在输入…」）→ 逐字回填 → 收尾；
    失败时气泡写「请求失败：…」。等回复时按 Enter **不发也不清空输入框**（不丢字）
  - 人格文件（勾选的那些）拼成 `system` 消息一起发；设置页的「Preview」能看拼出来的全文
  - 历史保留最近 20 条（`MAX_HISTORY_MESSAGES`）
- **实测（本地假 SSE 服务器，不烧真额度）**
  - 请求体：model / stream / Authorization 头 / messages 顺序全对，system 里含勾选文件内容
  - 流式拼接成一个气泡；历史两条；401 显示「HTTP 401 · Authentication Fails (no such user)」
  - 没配 Key 时**不发请求**，直接提示去设置
- **两个 bug 是测试抓出来的，已修**
  1. 401 的响应体被流式解析提前 `readAll()` 吃掉，错误信息退化成 Qt 的通用文案
     → 另存一份 `_raw_text` 专门用来抠错误
  2. 设置三页各自持有构造时的配置**快照**，存盘时互相覆盖（改完 API 页再动 RAG 页，
     API 的值被写回默认）→ 改成「存盘前现读，只改自己那几个字段」
- **待做**：真 Key 的端到端（要用户自己填进设置页）；`deepseek-reasoner` 的
  `reasoning_content` 目前不单独展示（只取 `content`）；没有「停止生成」按钮（`abort()` 已备好）

### 6. 主题 / 换肤系统 + 一套蓝色皮 —— 已完成

- **决策人**：用户（2026-11-11），原话「后续可以通过加载不同预设改页面样貌吗」
  +「添加一个蓝色的皮。就是你自己的配色」
- **已完成（2026-11-11）**
  - `core/gui/themes/`：`__init__.py`（ThemeManager）+ `light.toml` + `deepseek-blue.toml`
  - 一套主题 = 一个 toml：`label` / `note` / `dark` + 一张 `[palette]` 表（22 个 token）
  - `theme.py` 变成 QSS 模板：只写形状，颜色全部 `{token}`；缺 token 直接抛错
  - 切肤：`app.setStyleSheet()` 热替换，不用重启；选择存 `data/settings.ini`，启动时
    `apply_saved()` 读回（2026-11-11 起配置都在项目内，见第 12 条）
  - 蓝色皮：底 `#0F1115`、卡片 `#171A21`、描边 `#262B33`、正文 `#E6E8EC`、
    正文弱 `#8B93A1`、主色 `#4D6BFE`（悬停 `#5F7BFF`）
  - 设置 → Theme 页做成真的选皮界面（色块预览 + 选中态 + 「使用中」）
- **两个坑都处理了**
  1. **图标不跟 QSS 变色**：`themes.icon()` 读 SVG 文本 → 替换 `#1f2329` /
     白色描边 → `QSvgRenderer` 渲染成 pixmap（不落临时文件）；
     要跟随换肤的按钮必须用 `themes.bind(btn, name, role)` 注册
  2. **动态属性改了要重新 polish**：`themes.restyle(w)`（unpolish + polish + update）
- **额外踩到的坑**：`QSettings(org, app)` 在这台机器上写注册表返回
  `AccessError`（写不进也读不回），所以改成 INI 文件
  （`settings_path()`，可用 `DSAI_CONFIG_DIR` 覆盖）
- **待做**：`dark.toml` 没做（只做了浅色 + 蓝）。真要加，复制一份 toml 改配色即可，
  代码一行都不用动
- **时机**：现在抽完了，以后加控件只要引用现有 token

### 11. 界面语言（中文 / English）—— 已完成

- **用户要求（2026-11-11）**：「在 setting 添加英文和中文。不同的文本保存在
  `asset/language` 中」；确认过：范围是**整个 GUI**、格式 **TOML**、切换后**自动重启**
- **已完成**
  - `asset/language/zh.toml` + `en.toml`：各 87 条文案，键名是点分路径
    （`[settings.nav]` 的 `api_key` → `t("settings.nav.api_key")`）
  - `core/gui/i18n.py`：扫目录、加载（TOML 嵌套表摊平成点分键）、
    `t(key, default, **fmt)` 四级回退（当前语言 → 中文 → default → 键名）
  - `core/gui/settings_store.py`：把「配置在哪儿」从 themes 里抽出来，
    theme / i18n / live2d 共用同一份 `settings.ini`（不然 i18n 和 themes 会互相 import 成环）
  - `core/gui/relaunch.py`：重启助手。**不直接 startDetached**——旧进程没退干净时
    两份 QtWebEngine 会抢同一个 profile 目录，所以先起一个无控制台的助手进程，
    按 PID 轮询等旧进程退出（上限 12s + 0.6s 余量），再拉起主程序
  - 设置 → Other 页：语言下拉 + 说明；换语言 = 存盘 `language/code` + 重启；
    拉不起新进程会回滚到原语言，不留「看着像换好了」的假状态
  - 主题卡的名字/说明也走语言包，语言包里没有就用主题 toml 自带的 `label`/`note` 兜底
- **实测**（2026-11-11）
  - 键名对齐、占位符成对、空值：全过（87 / 87）
  - 英文界面 184 条文案零漏翻（语言下拉的「中文」和模型文件名是原文，属预期）
  - 重启链路：旧进程 exit 0 → 助手等它退出 → 新 GUI 起来（用新的 `language/code`）
  - 中英两套主窗 + 设置窗截图都验过
- **注意**：换语言**不是热更新**。文案在构造窗口时取一次；要真热更新得给每个控件记 key、
  再挨个 setText，复杂度不值当（用户也选的是重启）

### 12. 运行时数据全部落在项目内 —— 已完成

- **用户要求（2026-11-11）**：「所有产生的附带文件都直接写项目文件夹内部，不出项目文件夹」
- **改了什么**
  - 配置从 `%USERPROFILE%\AppData\LocalLow\DSAI4431_Chatbot\settings.ini` 搬到
    `<repo>/data/settings.ini`（`settings_store.project_root()` 靠 `pyproject.toml` 定位）
  - 首次启动会把老位置那份**自动复制**过来（不删旧的，怕新位置出问题还能对账）
  - QtWebEngine 的缓存/storage 路径显式指到 `<repo>/data/webengine/`
  - `.gitignore` 加 `data/*` —— 里面有**明文 API Key**，绝不能入库
  - 我的测试脚本和截图从 `P:\Deekseek_playground\_plan_preview\` 移到项目内同名目录
  - 清掉用户目录里的旧残留：`LocalLow\DSAI4431_Chatbot`、`LocalLow\DSAI4431 Chatbot`、
    `LocalLow\python`（后两个是更早版本用应用名 python 时留下的，含 30 多个 WebEngine 缓存）
- **实测**：跑一次 GUI 前后对比用户目录 —— 三个旧目录的文件数、mtime 都没变；
  项目内 `data/settings.ini` 正常生成并带着原来的主题/语言/Live2D 配置
- **一个发现**：`QWebEngineProfile.defaultProfile()` 是 off-the-record
  （`MemoryHttpCache`），本来就不落盘，所以 `data/webengine/` 一直是空的；
  路径设置留着当双保险

### 13. 新建对话窗口 + 会话落盘 `data/session/` —— 已完成（2026-11-11）

- **用户要求**：「提供新建对话的窗口：打开新页面并提供一个选择 persona
  的选项，提供选择模型的选项。新建的 session 保存在 `data\session` 中。需要储存的内容与 dsh 相同」
- **已完成**
  - `core/gui/session_store.py`：`data/session/index.json` + `data/session/<slug>/<id>/session.v1.jsonl`
  - `core/gui/personas.py`：人格清单直接读 DSH 那份
    `P:\.dsh\persona-inject\personas.json`（赤蛮奇 / 大肥鲸），读不到就退回
    「设置页那个目录 + 勾选文件」；模型候选 `deepseek-chat` / `deepseek-reasoner`
  - `core/gui/session_drawer.py`：≡ 打开左侧抽屉（「会话」新页面）→「＋ 新建对话」；
    列表按最近更新排序，双击进入
    - **2026-11-11 改版**：抽屉里的「选人格 + 选模型 + 创建/取消」表单已删，
      「＋ 新建对话」改成切到右侧的**整页新对话页**（见第 17 条）
  - 主窗：抽屉叠在左侧、Esc 关闭；选中/新建会话后收起抽屉并把历史读进聊天区
    - **坑（2026-11-11 用户反馈）**：抽屉原来是主窗的子控件，被 Live2D 整个盖住、点不到——
      `QWebEngineView` 是原生子窗口，永远压在兄弟 Qt 控件上面，`raise_()` 无效。
      改成 **`Qt.Tool` + 无边框的独立窗口**，按主窗客户区左上角算全局坐标贴上去，
      主窗 move/resize 时跟随、close 时一起关。窗口化之后不能画圆角（四角会露底色）
    - **坑二**：列表为空/隐藏时，QVBoxLayout 把剩余高度分给新建表单，把「创建/取消」
      挤出可视区 → 表单 `SizePolicy(Preferred, Maximum)` + `AlignTop`；
      表单展开时把「＋ 新建对话」按钮收起，避免同时出现两个「取消」
  - 不手动建会话直接发消息时，自动建一条（第一个人格 + 当前模型）
  - 每条会话自己记着 persona 和 model，发请求时按会话的来
- **DSH 那边实际存了什么**（我解了一份真实 session 看的，`session.v4.jsonl.zstd`）：
  - 第一行是头：`{"type":"session","version":4,"id","createdAt","cwd","parentSession",
    "isSeeded","origin","agentPreset"}`
  - 之后每行一个事件：`{"type","seq","time","data"}`
  - 关键事件：`session/title`（`data.title` + `messageSeqs` + `source.kind`）、
    `user/message`（`data.content=[{type:"text",text}]`）、
    `assistant/message`（`data.message.content` 里 `reasoning` / `text` / `tool-call` 块 +
    `data.usage` + `data.stream`）、`turn/start`、`turn/end`（`reason.kind`）、
    `request/header`（`config.provider/model/reasoningEffort/maxTokens`）
- **本项目要照抄的部分**（去掉 `tool/*`、`job/*`、`approval/*` 这些我们还没有的事件）
  - 目录：`data/session/<workspace-slug>/<session-id>/`
  - 头：type/version/id/createdAt/cwd/persona/model（`agentPreset` 换成人格目录）
  - 消息：`user/message` / `assistant/message`（content 块数组，`text` + `reasoning`，
    带 `usage`），`session/title` 用于改名，`turn/start|end`
  - **格式差异（有意）**：不压缩，写 `session.v1.jsonl`（纯文本，方便肉眼查/自带 grep）；
    DSH 用 `zstd` 需要额外依赖。若以后要互通再加压缩
  - 另加 `data/session/index.json`：会话列表索引（id/标题/时间/persona/model/消息数/token），
    列表页不用逐个读大文件
- **UI**：点 ≡ 打开「会话」抽屉（新页面）→ 顶部「新建对话」→ 选 persona + 选模型 → 创建并进入

### 14. 修改对话名称 / 删除单个对话 —— 已完成（2026-11-11）

- 列表右键 →「重命名」/「删除」（删除二次确认，写明会删文件）
- 重命名写 `session/title` 事件（和 DSH 一致）+ 同步 `index.json`
- 删除 = 删整个 `data/session/<slug>/<id>/` 目录 + 索引项；
  删的正好是当前打开的会话时，右侧聊天区自动清空

### 15. 批量删除对话 —— 已完成（2026-11-11）

- 抽屉标题栏「选择」→ 每行出勾选框，底部出现「全选/取消全选」+「删除选中(n)」
- 删除前按勾选数量二次确认；删完自动退出选择模式

### 16. 通用设置：显示思考链（默认关）—— 已完成（2026-11-11）

- 设置 → Other 页加「显示思考链」，默认**关**，存 `chat/show_reasoning`
- `chat_client` 解析流里的 `delta.reasoning_content`，发 `reasoning_delta` 信号
- 开关开：思考内容以独立的弱化气泡（虚线框、12px、`text_weak`）显示在回答**上面**；
  开关关：不画，但**照样存进会话**（`assistant/message` 的 `reasoning` 块）
- 重开会话时也按当前开关决定要不要把历史思考链画回来
- `deepseek-chat` 不返回思考内容，所以这个开关只对 `deepseek-reasoner` 有实际效果

### 17. 新对话页（整页空白首页）+ 启动自动续上最近会话 —— 已完成（2026-11-11）

- **用户要求**（对照 DSH 首页截图）：「点击新建对话后应该跳这样一个窗口才对
  （忽略上面的 logo），然后在刚打开时自动加载最近更新过的对话，没有对话就直接
  打开这样一个新建对话的窗口」
- **确认过的三个选择**：新对话页占**右侧聊天列**（左边 Live2D 保留）；抽屉里的
  新建表单**删掉**；发出第一条消息后**自动切成普通对话视图**
- 实现
  - `main_window.HomePage`：大标题 + 人格下拉 + 大输入卡（模型下拉 + 发送在卡片
    右下角，附件图标在左下角，和 DSH 一样）。输入框宽 760 居中，上下留白 3:5
  - `ChatColumn` 里改成 `QStackedWidget`：0 = 对话页（消息 + 输入卡），
    1 = 新对话页；顶栏（≡ / ⚙）两页共用
  - `start_new_conversation()` 只清状态、**不建会话**；第一句话发出时
    `_ensure_session()` 才按首页选的人格/模型落盘（空会话文件没有意义）
  - `MainWindow._restore_last_session()`：启动时 `list_sessions()[0]`
    （已按 `updated_at` 倒序）直接打开；一条都没有才停在首页
  - 抽屉 `session_created` / `NewSessionForm` / `toggle_form` 全部删掉，
    `btn_new` 改为发 `new_session_requested` → `MainWindow` 收起抽屉 + 切首页
    → 全程序**只有一条创建路径**
- **顺手修的 bug**：`MainWindow.closeEvent` 有两份定义，后一份把前一份（含
  `self._drawer.close()`）整个覆盖掉了 → 删掉重复的那份
- **坑**：`HomePage` 写在 `main_window.py` 里而不是单独模块 —— 它要用
  `_InputEdit`（Enter 发送）和 `round_button`，单独成模块会和本模块循环导入
- **第二轮：选择器的「质感」**（用户 20:05 反馈「质感做得不行」，给了 DSH 的截图）
  - 人格选择器改成**胶囊**：圆角 11px、底色 `chip_bg`（不是系统那种白底 + 带方框
    的三角按钮）、左侧图标 + 名字 + 细箭头
  - 图标直接用设置页 Personality 那颗（`icons/user.svg`），每次 `refresh()` 重新取，
    换主题时颜色跟着走
  - 箭头是 `icons/chevron.svg`。**坑**：QSS 里的 `image: url()` 不会被 `themes`
    重新上色（那是运行时替换 SVG 文本里的 `#1f2329`），所以这个文件直接用中性灰
    `#8a9099`，浅色/深色两套皮上都看得见
  - **坑**：`QComboBox` 默认按**最长的一项**算宽度，选中短名字时右边留一截空白、
    箭头离文字老远 → `HomePage._fit_combo()` 按当前文字宽度重算（`PERSONA_CHROME`
    / `MODEL_CHROME` 是 QSS 里内边距+箭头区+图标的常量，改 QSS 要一起改）
  - 模型选择器做成输入卡右下角的一行小字（无边框、悬停才浮底色），和 DSH 一致
  - 新增主题 token `chip_bg` / `chip_bg_hover`（老主题文件没有也不会崩：
    `stylesheet()` 里 `setdefault` 退回 `surface_alt` / `hover`）
- 验证：`_plan_preview/i18n/test_p_home.py`（32 项全过），截图
  `home_no_session.png` / `home_autoopened.png` / `home_page.png`；
  选择器的三倍放大对照图 `look_{light,dark}.png`、`look_pill_*.png`、`look_model_*.png`
  （`test_q_combo_look.py`，不建主窗口、不拉 Live2D，秒出）

---

## 二、待用户决定

### 7. `asset/plan/` 那 4 张设计图 —— 已决定入库

- 4 张 PNG，共 20.9 MB：`main interface.png`、`setting-api_key.png`、
  `setting-persona.png`、`setting-RAG.png`
- 2026-11-11 用户决定提交进仓库（设计源图跟代码一起版本化）

### 8. `_plan_preview/` 临时目录

- 里面是界面渲染截图、调试脚本、放大裁剪图
- 属于临时产物（`.gitignore` 里），确认可以删就删
- 2026-11-11 起统一放在**项目内**的 `_plan_preview/`，不再散在 `P:\Deekseek_playground\` 下

---

## 三、杂物 / 外部事项

### 9. 未提交的改动

截至 2026-11-11 最后一次提交，工作区是干净的：
- 早期那批（`core/gui/` 全套、`icons/`、`启动GUI.bat`、`asset/plan/`、`README`、`pyproject.toml`）
  已按用户指示入库并推到 `origin/main`
- 之后的设置窗外观、Live2D model 页、主题系统、启动崩溃修复、多语言都是逐个提交的
- `_plan_preview/` 仍在 `.gitignore` 里（临时截图与测试脚本），没有入库

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

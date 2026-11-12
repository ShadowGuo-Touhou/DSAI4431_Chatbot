# DSAI4431 Chatbot

### For my teammates:

* This installation guide is written for AI, not human, it's going to be painful to set it up yourself. You better let AI do it.

* You can change the language in the setting page on top right coner, Chinese and English are supported.

* The personality plugin is ready, I still working on RAG, but you can now write your chatbot persona.

* To create new personality, just create a new directory somewhere and write perosnality for your chatbot in .md files.
  
  * Refer to the default "FatWhale" persona for reference



## 环境要求

- **Windows 10 / 11** —— Ollama 接管用 `netstat` / `taskkill` / Win32 API，自动下载的
  也是 Windows 版 Ollama；macOS / Linux 上跑不了这套
- Python >= 3.12（3.13+ 也行，但只测过 3.12）
- Git
- **磁盘约 3 GB**：Ollama 1.6 GB + 向量模型 0.2 GB + 语音模型 0.23 GB + 索引与缓存
- 麦克风（可选，用语音输入才需要）

## 快速开始

**跑主界面**（最省事，两步）：

```powershell
# 1. 装依赖：脚本自己找 Python 3.12+、建 .venv、pip install -e ".[gui,rag]"
.\安装依赖.bat
#    网络慢就走清华镜像：.\安装依赖.bat --mirror

# 2. 启动
.\启动GUI.bat
```

首次启动会显示一个**加载页**，把 Ollama（约 1.6 GB）、向量模型、语音模型一项项
准备好才进主界面；不想等可以点「跳过下载」，之后在设置 → RAG 里手动配。
具体每一步做什么见 [0.5 程序启动时会做什么](#05-程序启动时会做什么)。

手工等价命令（不想用脚本时）：

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -e ".[gui,rag]"
```

**只要核心包的命令行**（echo 占位，不装 Qt，几十秒就装完）：

```powershell
python -m pip install -e .
dsai4431-chatbot --version
dsai4431-chatbot "你好"
# 或者不安装，直接：$env:PYTHONPATH = "src"; python -m dsai4431_chatbot "你好"
```

> `pip install -e` 第一次执行需要联网下载 `setuptools`，可能比较慢。

## 目录结构

```
DSAI4431_Chatbot/
├── pyproject.toml              # 项目与构建配置（PEP 621）
├── README.md
├── .gitignore
├── .venv/                      # 本地虚拟环境（不入库）
├── asset/                      # 资源：数据、模型、素材（见下节）
│   ├── persona/                # 人格设定文本
│   ├── language/               # 界面文案（zh.toml / en.toml）
│   ├── live2d/                 # Live2D 依赖库、Cubism Core、模型
│   │   ├── vendor/             # pixi / cubism4 / cubismcore 三件套（入库）
│   │   ├── cubism-core/        # 官方 Cubism Core 原始文件（入库）
│   │   ├── models/             # 全部模型
│   │   │   ├── Hiyori/         # 示例模型（入库）
│   │   │   ├── Natori/         # 示例模型（入库）
│   │   │   └── DeepSeek免费公皮/ # 大肥鱼模型 + PSD 源文件（**不入库**）
│   ├── RAG/                    # 检索用的知识库原始文件（.md/.txt）
│   ├── embedding/              # 检索用的模型（OLLAMA_MODELS 指这里，不入库）
│   └── ollama/                 # 没装系统版时，便携版 Ollama 解压到这里（不入库）
└── src/
    └── dsai4431_chatbot/       # 代码包
        ├── __init__.py         # 包元信息（__version__）
        ├── __main__.py         # python -m dsai4431_chatbot
        ├── main.py             # CLI 入口与 reply() 占位实现
        ├── py.typed            # 声明本包带类型标注
        └── core/               # 核心业务逻辑（随包安装）
            ├── __init__.py
            └── live2d/         # Live2D 桌面演示（PyQt5 + QWebEngineView）
                ├── demo_interactive.py   # 主程序
                ├── demo_live2d.html      # 渲染页
                ├── demo_probe.html       # 无素材时的占位页
                ├── make_demo_model.py    # 生成 *.demo.model3.json
                ├── 启动.bat                # 启动器（纯 ASCII 内容）
                ├── HANDOFF.md            # 开发交接笔记与全部踩坑记录
                └── legacy/               # 早期版本，保留备查
```

## 资源目录 `asset/`

| 目录                                      | 放什么                                                      | 是否入库    |
| --------------------------------------- | -------------------------------------------------------- | ------- |
| `asset/persona/`                        | 人格设定文本（`.md` / `.json`）                                  | 入库      |
| `asset/language/`                       | 界面文案：`zh.toml` / `en.toml`                               | 入库      |
| `asset/live2d/vendor/`                  | `pixi.min.js`、`cubism4.min.js`、`live2dcubismcore.min.js` | 入库      |
| `asset/live2d/cubism-core/`             | 官方 Cubism SDK for Web 的 Core 原始文件                        | 入库      |
| `asset/live2d/models/Hiyori/`、`Natori/` | 示例模型                                                     | 入库      |
| `asset/live2d/models/DeepSeek免费公皮/`     | 大肥鱼模型 + 125 MB PSD 源文件                                   | **不入库** |
| `asset/RAG/`                            | 检索知识库的原始文档（`.md` / `.txt`）                             | 入库      |
| `asset/embedding/`                      | **检索用的模型**（Ollama 的 `OLLAMA_MODELS` 指到这里）            | **不入库** |
| `asset/ollama/`                         | **Ollama 本身**：没装系统版时，便携版解压到这里                    | **不入库** |

### 关于模型文件不入库

`asset/embedding/`、`asset/ollama/`、`asset/live2d/models/DeepSeek免费公皮/` 里放的是模型权重和
大体积素材，单个动辄几百 MB 到数 GB，提交进 git 会让仓库变得极难维护（clone 慢、
历史不可回收）。因此 `.gitignore` 中已排除这些目录：

```gitignore
asset/embedding/*
!asset/embedding/.gitkeep
asset/ollama/*
!asset/ollama/.gitkeep
asset/live2d/models/DeepSeek免费公皮/
```

前两个目录保留 `.gitkeep` 是因为 git 记录不了空目录；`DeepSeek免费公皮/` 整个目录不需要占位。

**换机器或重新 clone 之后，模型需要自己重新准备**，例如：

```powershell
# Ollama 模型
ollama pull bge-m3

# embedding 模型权重放到 asset/embedding/ 下
```

空目录在 git 里不会被追踪，所以新建空文件夹时同样要放一个 `.gitkeep`，
否则别人 clone 下来会看不到这个目录。

## Live2D 桌面演示

`src/dsai4431_chatbot/core/live2d/` 是一个在 PyQt5 里渲染 Live2D 的可交互演示
（大肥鱼模型，8 组换装/手势动作 + 23 个表情、戳一下、摸头、头部跟随）。

### 依赖

Qt 相关依赖是可选组，核心包不依赖它们：

```powershell
.\.venv\Scripts\Activate.ps1
pip install -e ".[live2d]"        # 或手动：
# pip install -i https://pypi.tuna.tsinghua.edu.cn/simple PyQt5 PyQtWebEngine
```

实际版本：PyQt5 5.15.11 / PyQtWebEngine 5.15.7 / Qt 5.15.2（内嵌 Chromium 83）。

### 启动

```powershell
# 方式一：双击启动器（自动找模型）
src\dsai4431_chatbot\core\live2d\启动.bat

# 方式二：显式指定模型
.\.venv\Scripts\python.exe -m dsai4431_chatbot.core.live2d.demo_interactive `
  --model "asset\live2d\models\DeepSeek免费公皮\DeepSeek\大肥鱼.demo.model3.json"

# 方式三：无素材自检（不加载 Core 和模型）
.\.venv\Scripts\python.exe -m dsai4431_chatbot.core.live2d.demo_interactive --probe
```

> **必须用 `.demo.model3.json`，不能用原始 `.model3.json`。** 这是 VTS 风格模型，
> 动作/表情不在 model3.json 里；`make_demo_model.py` 扫描 `Animation/` 与 `Exp3/`
> 后生成带 `Motions` + `Expressions` 的版本。原始文件不要改。
> 因为模型目录已排除出 git，clone 后需要重新生成一次：
> 
> ```powershell
> .\.venv\Scripts\python.exe src\dsai4431_chatbot\core\live2d\make_demo_model.py `
>   "asset\live2d\models\DeepSeek免费公皮\DeepSeek\大肥鱼.model3.json"
> ```

### 资源位置如何解析

代码在 `src/`，资源在 `asset/live2d/`，所以 `demo_interactive.py` 会从自身所在目录
逐级向上找 `<repo>/asset/live2d`；目录结构变了用环境变量指定：

```powershell
$env:L2D_ASSET_DIR = "D:\somewhere\live2d"
```

本地静态服务把 `/vendor/` 和 `/model/` 分别映射到 `asset/live2d/vendor` 和模型目录，
因此 HTML 里的相对引用不需要改。

### 踩坑记录

`src/dsai4431_chatbot/core/live2d/HANDOFF.md` 记了全部技术细节：黑块是 drawable 级问题、
参数写入的唯一有效位置、物理会锁死头部角度、`--no-sandbox` 必须开、Chromium 83 没有
顶层 await 等。改这个演示之前先读它。

## 主界面 GUI（框架阶段）

`src/dsai4431_chatbot/core/gui/` 是按 `asset/plan/main interface.png` 搭的主界面骨架：
左栏 Live2D 角色区、右侧聊天列（顶栏 / 消息区 / 输入框 / 操作条）。
目前只有结构与样式，业务逻辑全部留空并标了 TODO。

```powershell
pip install -e ".[gui]"
python -m dsai4431_chatbot.core.gui
```

- `main_window.py`：窗口与各面板组件
- `live2d_config.py`：Live2D 显示配置（模型 / 取景 / 缩放 / 偏移 / 行为开关 / 隐藏部件），
  存在 `settings.ini`；设置 → Live2D model 页改的就是它，启动时自动还原
- `theme.py`：QSS 模板（字体、圆角、间距，以及每个控件引用哪个 token）
- `themes/`：换肤系统。一套主题 = 一个 `.toml`（`label` / `note` + `[palette]` 配色表）
  - `light.toml`：默认浅色
  - `deepseek-blue.toml`：DeepSeek 蓝（深色底 + `#4D6BFE`）
  - 切换：设置 → Theme，点一下立即生效（`app.setStyleSheet()` 热替换），
    选择记在 `data/settings.ini`（见下面「运行时数据放哪」），下次启动保持
  - 加新皮肤：丢一个 `.toml` 进这个目录，重启后自动出现在列表里
  - 注意：图标颜色不跟着 QSS 走，是读 SVG 文本替换颜色再渲染成 pixmap
    （要跟随换肤的按钮得通过 `themes.bind()` 设置图标）
- `i18n.py` + `asset/language/`：界面语言（中文 / English）。一套语言 = 一个 `.toml`，
  键名是点分路径（`[settings.nav]` 的 `api_key` → `t("settings.nav.api_key")`）
  - 切语言在 设置 → Other；**换语言会重启程序**（文案在构造窗口时取一次），
    重启由 `relaunch.py` 负责：它先等旧进程退干净，再拉起新的，避免两份
    QtWebEngine 抢同一个 profile 目录
  - 选择记在 `settings.ini` 的 `language/code`，默认中文
  - 缺键按「当前语言 → 中文 → 调用方 default → 键名」四级回退，
    所以 en 少翻译一条只会显示中文，不会空白
  - 加新语言：往 `asset/language/` 丢一个 `<code>.toml`（带 `[meta]` 的 `code`/`name`），
    重启后自动出现在下拉里
- `settings_store.py`：配置文件的读写位置（`settings.ini`），theme / i18n / live2d / chat 共用
- `chat_config.py`：对话配置（API 地址 / Key / 模型 / 人格目录与勾选文件 / RAG 三条路径），
  存 `settings.ini` 的 `[chat]` 段；设置页改完即存，启动后按它发请求
- `chat_client.py`：对话后端。OpenAI 兼容 `/chat/completions`，**流式 SSE**，
  用 Qt 自带的 `QNetworkAccessManager`（不引第三方库、不开线程）

### 接上对话（需要自己填 Key）

```powershell
python -m dsai4431_chatbot.core.gui
# 点右上角齿轮 → API KEY：填地址（默认 https://api.deepseek.com）、Key、模型（默认 deepseek-chat）
# 再点 Personality：选人格文件目录，勾上要发给模型的 .md（拼成 system 提示词）
# 回主界面输入框打字 → Enter
```

- Key 是**明文**存在 `data/settings.ini` 里的；那个文件已在 `.gitignore` 里，
  但别忘了它随项目文件夹走 —— 别把整个文件夹打包发给别人

### 运行时数据放哪

**程序产生的东西全部留在项目目录里，不写用户目录**（用户 2026-11-11 要求）：

```
<repo>/data/settings.ini     # 主题 / 语言 / Live2D / 对话配置（含明文 API Key）
<repo>/data/webengine/       # QtWebEngine 缓存与 storage（当前 profile 是
                             # off-the-record，实测不落盘；路径先占好）
<repo>/data/rag/             # 知识库索引（meta.json + index.npz），启动时自动生成；
                             # 删掉没关系，下次启动会重建
```

知识库的**源文件**放在 `<repo>/asset/RAG/`（只收 `.md` / `.txt`），
索引与格式细节见仓库根的 `RAG_PLAN.md`。

- `data/` 在 `.gitignore` 里，**不要** `git add -f`
- 老版本存在用户目录里的 `settings.ini` 会在首次启动时自动复制过来
  （`%USERPROFILE%\AppData\LocalLow\DSAI4431_Chatbot\settings.ini`，复制后不删）
- 想换位置：`DSAI_DATA_DIR` 指定目录，`DSAI_CONFIG_DIR` 只改 ini 所在目录
- 回复是流式的：先出现「正在输入…」的气泡，然后逐字填进去
- 等回复时按 Enter 不会发、也不会清空你正在敲的内容
- 出错时气泡里直接写原因（`HTTP 401 · Authentication Fails…` 这类）
- `Preview` 按钮能看到当前勾选的文件拼出来的 system 提示词全文
- 点左上角 `≡` 打开会话列表：右键可以改名/删除，标题栏「选择」进批量删除
- 「＋ 新建对话」会把右侧聊天列整块换成**新对话页**：上面选人格（读 DSH 的
  `personas.json`），大输入卡右下角选模型；敲下第一句话才真正建会话（空会话不落盘）
- **打开程序时不用点**：直接接上最近更新过的那条对话；一条对话都没有才停在新对话页
- 设置 → Other 里有「显示思考链」（默认关）：只有 `deepseek-reasoner` 会返回思考内容

### 会话数据 `data/session/`

结构照 DSH（头 + 逐行事件），只是不压缩：

```
data/session/index.json                       # 列表索引（标题/时间/人格/模型/token）
data/session/<workspace-slug>/<session-id>/session.v1.jsonl
```

每行事件：`{"type","seq","time","data"}`，类型有 `session`（头）、`user/message`、
`assistant/message`（content 块含 `text` / `reasoning`，带 `usage`）、`session/title`、`turn/*`。

> 截图和线框图在 `asset/plan/` 下，原图是竖排的，**需要顺时针旋转 90° 才是正的**。

## 语音输入

点输入卡右边的麦克风 → 说话 → **再点一次麦克风**结束 → 文字落进输入框（插在
光标处，不会覆盖你已经打的字）。全程本地识别，音频不上传。

> **麦克风在「对话页」的输入卡里**，首页那张大卡片上没有 —— 先发一句话、或点开
> 一个会话进到对话页，才看得到麦克风按钮。

| 时机 | 会看到什么 |
|---|---|
| 启动时 | 加载页多一行「语音识别模型」；`asset/stt` 里没有就自动下载 228 MB（可以点「跳过下载」） |
| 第一次点麦克风 | 多等 2~3 秒（模型读进内存），之后每次约 0.3 秒 |
| 录音中 | 麦克风淡红底 + 输入卡里出现声纹；最长 60 秒自动停 |
| 失败 | 输入卡顶部一行提示：「太短了，没听清」/「没听清，再说一次？」/「没找到麦克风…」 |

### 引擎与模型

- 引擎 [sherpa-onnx](https://github.com/k2-fsa/sherpa-onnx)：纯 CPU 的 ONNX 推理，
  Windows 轮子**自带 onnxruntime**，不引入 torch。随 `pip install -e ".[gui]"` 装好。
- 模型 **SenseVoiceSmall int8** + **Silero VAD**：中/英/粤/日/韩，`language="auto"`
  自己判语种，不用选。
- 文件在 `asset/stt/`，**不入库**，缺了启动时自动下：

  ```
  asset/stt/sensevoice/model.int8.onnx    228 MB
  asset/stt/sensevoice/tokens.txt         0.3 MB
  asset/stt/silero_vad.onnx               1.7 MB
  ```

- 下载先走 `hf-mirror.com`，失败回退 `huggingface.co`；revision 固定、逐个校验
  sha256（对不上就删掉重来）。

### 出问题先看这张表

| 现象 | 原因 |
|---|---|
| 「没找到麦克风」 | Windows → 设置 → 隐私和安全性 → 麦克风，给桌面应用开权限 |
| 声纹一直是平的 | 麦克风增益太低（系统声音设置里调）；静音时本来就接近一条线 |
| 识别成乱码 / 老是英文 | 说得太短或太小声；`auto` 偶尔会猜错语种 |
| 「语音模型还没装好」 | `asset/stt` 缺文件 —— 重启让它自动下，或看加载页那行是不是失败了 |

## 知识库检索（RAG）怎么配

**一句话**：设置 → RAG 里那两格，一格填**服务地址**，一格填**模型名字**；
Ollama 自己按名字找文件，**没有「导入模型」这一步**，也不能填文件夹。

| 设置项 | 填什么 | 千万别填 |
|---|---|---|
| `Ollama` | `http://127.0.0.1:11434` | Ollama 的 exe 路径、`models` 目录 |
| `Embedding` | 模型名，例如 `bge-m3` / `nomic-embed-text` / `quentinz/bge-base-zh-v1.5` | `P:\...` 这种路径、`.gguf` 文件名 |

### 0. 用哪份 Ollama：程序会**接管**端口

**规则（2026-11-13 起）**：启动时先看 `11434` —— 上面已经有别的 Ollama 在跑
（系统装的、你手动 `ollama serve` 起的、上次遗留的），**就先关掉它**，再按设置页
那两格路径重新起一个。这样「实际在用的模型」永远等于设置页显示的那份，不会
悄悄复用外面的服务。

| 设置 → RAG 里的两格 | 留空时用 | 填了但这台机器上不存在 |
|---|---|---|
| **Ollama 目录** | `asset/ollama` | 自动退回 `asset/ollama`（日志会打一行） |
| **模型目录** | `asset/embedding` | 自动退回 `asset/embedding` |

两种情况**不动手**：

- 端口上那个进程**不是 ollama**（比如被别的软件占了）→ 报「端口被别的程序占着」，不硬起
- 确实是 ollama 但**关不掉**（权限不足）→ 报「关不掉，可能需要管理员权限」

> ⚠ 只 kill 进程名是 `ollama` 的。但如果你机器上还有别的东西连着那个 Ollama
> （别的 AI 工具、别的会话），接管那一下它会短暂断掉。

`asset/ollama/` 和 `asset/embedding/` 都在 `.gitignore` 里（几百 MB~几 GB 的二进制），
**不要 `git add -f`**。换机器时不用手动放——首次启动会自动下载。

### 0.5 程序启动时会做什么

**不用你手动开服务**，加载页会把这些一项项做掉：

| 加载页那一行 | 动作 |
|---|---|
| Ollama 运行时 | 探测 `GET /api/tags` → 通着就按上面的规则接管；不通就找 `asset\ollama\ollama.exe` 后台 `serve`，最多等 20 秒 |
| 向量模型（bge） | 按设置里的模型名检查 `<模型目录>/manifests/...` 在不在；不在就 `ollama pull` |
| 语音识别模型 | 检查 `asset/stt` 三个文件；缺了就下载（可点「跳过下载」） |
| 构建知识库索引 | 扫描知识库目录、切块、算向量 |
| 回收站以外的收尾 | 预热 embedding 模型（跑完才进主界面） |

| 情况 | 行为 |
|---|---|
| 找不到 exe 也没有网络 | 那一行标红报错，聊天照常用（只是查不了知识库） |
| 中途点「跳过下载」 | 停掉自动安装，先放你进主界面；之后可以在设置 → RAG 里手动配 |
| 退出程序 | **只关程序自己拉起的那份** |

对应设置项：**设置 → RAG → 「启动时自动检测并拉起 Ollama」**（默认开）。
关掉它之后不会接管端口，端口上有什么就用什么。

> 拉起时程序会**显式**把 `OLLAMA_MODELS` 设成模型目录再启动，不沿用你环境里
> 那句（机器上那份只读目录曾经让它启动失败，见 `manifests-v2: Access is denied`）。

### 1. 模型放哪：`asset/embedding/`

模型**不要**留在系统盘默认位置，统一放本项目的 `asset/embedding/`
（这个目录已经建好，里面只有个 `.gitkeep`）：

```
<repo>/asset/embedding/
    blobs/        ← ollama pull 时自动生成
    manifests/    ← ollama pull 时自动生成（模型名就是这里的目录结构）
```

⚠ **顺序很重要**：先设 `OLLAMA_MODELS`，再 `pull`。反了会拉到默认位置
（`%USERPROFILE%\.ollama\models`），`asset/embedding/` 里就是空的。

已经有模型的话（比如以前拉到 `P:\.Ollama\models` 的那份），两种做法任选：

- 把那个目录下的 `manifests\` 和 `blobs\` 整个**复制**到 `asset/embedding/`（推荐，和仓库在一起）
- 或者不复制，继续把 `OLLAMA_MODELS` 指到原来那个目录（那就不看本节，模型名按第 3 节推）

> 两条路只选一条。**别让两个 `OLLAMA_MODELS` 打架**：一个是系统环境变量、
> 一个是当前终端的 `$env:`，同时存在时只认其中一个，`ollama list` 里会莫名其妙少模型。

分两种情况，别搞混：

| 谁起的服务 | 模型目录由谁决定 |
|---|---|
| **程序自己拉起**（绝大多数情况） | 设置 → RAG → **模型目录**，程序会把它写进 `OLLAMA_MODELS` 传给子进程；不看你环境里那句 |
| **你在终端手动 `ollama serve`** | 只认环境变量 `OLLAMA_MODELS`，此时设置页填什么都管不着 |

手动调试时才需要自己设（要指向**包含 `blobs\` 和 `manifests\` 的那一层**）：

```powershell
# 临时（只对当前这个终端窗口有效，调试时最省事）
$env:OLLAMA_MODELS = "<repo>\asset\embedding"

# 永久（新开终端才生效；如果用系统装的那份，要退出托盘图标再重开）
setx OLLAMA_MODELS "<repo>\asset\embedding"
```

### 2. 拉模型 + 起服务

```powershell
# 便携版；装过系统的就直接用 ollama
asset\ollama\ollama.exe pull bge-m3         # 中文效果更好，1024 维，约 1.2 GB
asset\ollama\ollama.exe list                # 能看到 bge-m3:latest 才算成功

asset\ollama\ollama.exe serve               # 前台启动服务，默认监听 11434
```

用系统版的话：双击托盘里的 Ollama，或 `ollama serve`。
服务起没起，用一条命令判断：

```powershell
curl http://127.0.0.1:11434/api/tags        # 返回一段 JSON 就是活着
```

### 3. 模型名怎么从路径推出来

模型名就是 `asset\embedding\manifests\`（或你原有的 models 目录）下的相对路径——
去掉 `registry.ollama.ai/`、去掉 tag：

| 磁盘上的路径 | 设置里填 |
|---|---|
| `asset\embedding\manifests\registry.ollama.ai\library\bge-m3\latest` | `bge-m3` |
| `asset\embedding\manifests\registry.ollama.ai\library\nomic-embed-text\latest` | `nomic-embed-text` |
| `manifests\registry.ollama.ai\quentinz\bge-base-zh-v1.5\latest`（你已有的那份） | `quentinz/bge-base-zh-v1.5` |

规则：`library` 这个命名空间可以省，`latest` 是默认 tag 也可以省；
别的命名空间必须带上，形如 `命名空间/模型名`。最稳的办法是直接抄 `ollama list` 里那一列。

### 4. 生效

1. 填好两格（值一变就自动存盘，没有保存按钮）
2. **重启程序**（索引在启动时建一次），或点「重新扫描」
3. 状态行出现 `索引状态：38 个文件 · 512 块 · 1024 维` 就是成功了
4. 往 `asset/RAG/` 里放 `.md` / `.txt`，问里面的内容，回答会带上资料

索引存在 `data/rag/`，删掉没关系，下次启动自动重建。换模型 / 改块长度或重叠会
**整库重切**；只是加改文件则走增量（没变的文件不会重新算向量）。

**文件清单右边的绿/红标记**：

| 标记 | 含义 | 怎么判的 |
|---|---|---|
| ● 已入库（绿） | 这份内容已经在语料库里 | 台账里的 `sha256` 和磁盘一致（大小 + 修改时间都没变就直接算一致，变了才算 hash） |
| ● 未入库 · 有改动（红） | 改过了，索引里还是旧版本 | 台账里有这条，但 hash 不同 |
| ● 未入库 · 新文件（红） | 还没进过语料库 | 台账里没有这条 |
| ● 已跳过（灰） | 按规则不收 | 太大 / 扩展名不收 / 读不出来 |

「重新扫描」后标记立刻刷新；「清空索引」后全部变红（语料库真的空了）。

### 5. 出问题先看这张表

| 现象 | 原因 | 怎么办 |
|---|---|---|
| 状态行「同步失败：连不上 Ollama」 | 服务没起 / 地址写错 / 端口被另一个 Ollama 占着 | 先 `curl http://127.0.0.1:11434/api/tags`；只留一个 Ollama 在跑 |
| `ollama list` 里没有模型，但文件确实在 | `OLLAMA_MODELS` 没设或指错层（要指向含 `blobs\`+`manifests\` 的那层） | 按第 1 节设 `OLLAMA_MODELS`，重启 Ollama |
| 两个 Ollama（系统的 + `asset/ollama`）抢端口 | 同时跑了两个 `serve` | 只留一个；要么用系统那份，要么用 `asset\ollama` 那份 |
| `HTTP 404 model not found` | 名字写错，或填了路径/`.gguf` | 用 `ollama list` 里那一列**原样复制** |
| 总是「检索超时」 | 首次加载模型慢，而超时只有 3000 ms | 先点一次「重新扫描」热身，或把超时调到 15000 |
| 答案里带不出知识库内容 | 阈值太高 / 块太长 / 模型弱 | 阈值降到 0.25；块长度 300~500；换 `bge-m3` |
| 「该模型不支持 embeddings」 | 那份 GGUF 不是 embedding 版 | 换 `nomic-embed-text` 或 `bge-m3` |

> 维度和模型绑死：`bge-m3` 1024 维、`bge-base-zh-v1.5` 与 `nomic-embed-text` 768 维。
> 换模型会自动重建索引，不用手动删 `data/rag/`。

## 后续可以加

- 测试：`tests/` + `pytest`（在 `pyproject.toml` 加 `[tool.pytest.ini_options]`）
- 代码检查：`ruff`
- 依赖：写进 `pyproject.toml` 的 `[project].dependencies`

# DSAI4431 Chatbot

DSAI4431 课程聊天机器人项目。

## 环境要求

- Python >= 3.12
- Git

## 快速开始

```powershell
# 1. 激活虚拟环境
.\.venv\Scripts\Activate.ps1

# 2. 以可编辑模式安装本项目
python -m pip install -e .

# 3. 试运行
dsai4431-chatbot --version
dsai4431-chatbot "你好"
# 或者：python -m dsai4431_chatbot
```

不安装也可以直接跑（把 `src` 加进 `PYTHONPATH`）：

```powershell
$env:PYTHONPATH = "src"; python -m dsai4431_chatbot "你好"
```

> `pip install -e .` 第一次执行需要联网下载 `setuptools`，可能比较慢。

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
│   ├── RAG/                    # 检索用的知识库原始文件
│   ├── embedding/              # 向量模型权重（不入库）
│   └── ollama/                 # Ollama 本地模型（不入库）
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

| 目录 | 放什么 | 是否入库 |
|---|---|---|
| `asset/persona/` | 人格设定文本（`.md` / `.json`） | 入库 |
| `asset/language/` | 界面文案：`zh.toml` / `en.toml` | 入库 |
| `asset/live2d/vendor/` | `pixi.min.js`、`cubism4.min.js`、`live2dcubismcore.min.js` | 入库 |
| `asset/live2d/cubism-core/` | 官方 Cubism SDK for Web 的 Core 原始文件 | 入库 |
| `asset/live2d/models/Hiyori/`、`Natori/` | 示例模型 | 入库 |
| `asset/live2d/models/DeepSeek免费公皮/` | 大肥鱼模型 + 125 MB PSD 源文件 | **不入库** |
| `asset/RAG/` | 检索知识库的原始文档 | 入库 |
| `asset/embedding/` | 向量模型权重 | **不入库** |
| `asset/ollama/` | Ollama 拉取的本地模型 | **不入库** |

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
    选择记在本地 `settings.ini`（Windows 上是 `%USERPROFILE%\AppData\LocalLow\DSAI4431_Chatbot\settings.ini`，
    可用 `DSAI_CONFIG_DIR` 改写），下次启动保持
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
- `settings_store.py`：配置文件的读写位置（`settings.ini`），theme / i18n / live2d 共用

> 截图和线框图在 `asset/plan/` 下，原图是竖排的，**需要顺时针旋转 90° 才是正的**。

## 后续可以加

- 测试：`tests/` + `pytest`（在 `pyproject.toml` 加 `[tool.pytest.ini_options]`）
- 代码检查：`ruff`
- 依赖：写进 `pyproject.toml` 的 `[project].dependencies`

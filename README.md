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
│   ├── live2d/                 # Live2D 模型与贴图
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
            └── __init__.py
```

## 资源目录 `asset/`

| 目录 | 放什么 | 是否入库 |
|---|---|---|
| `asset/persona/` | 人格设定文本（`.md` / `.json`） | 入库 |
| `asset/live2d/` | Live2D 模型、贴图、动作文件 | 视体积而定，模型本体建议不入库 |
| `asset/RAG/` | 检索知识库的原始文档 | 入库 |
| `asset/embedding/` | 向量模型权重 | **不入库** |
| `asset/ollama/` | Ollama 拉取的本地模型 | **不入库** |

### 关于模型文件不入库

`asset/embedding/` 和 `asset/ollama/` 里放的是模型权重，单个动辄几百 MB 到数 GB，
提交进 git 会让仓库变得极难维护（clone 慢、历史不可回收）。因此 `.gitignore` 中已排除这两个目录：

```gitignore
asset/embedding/*
!asset/embedding/.gitkeep
asset/ollama/*
!asset/ollama/.gitkeep
```

每个目录保留一个 `.gitkeep` 只是为了 git 能记录空目录本身。

**换机器或重新 clone 之后，模型需要自己重新准备**，例如：

```powershell
# Ollama 模型
ollama pull bge-m3

# embedding 模型权重放到 asset/embedding/ 下
```

空目录在 git 里不会被追踪，所以新建空文件夹时同样要放一个 `.gitkeep`，
否则别人 clone 下来会看不到这个目录。

## 后续可以加

- 测试：`tests/` + `pytest`（在 `pyproject.toml` 加 `[tool.pytest.ini_options]`）
- 代码检查：`ruff`
- 依赖：写进 `pyproject.toml` 的 `[project].dependencies`

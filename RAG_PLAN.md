# RAG 实装计划（切片 + 启动时差量同步）

> 状态：**计划稿，未实装**。写于 2026-11-12 00:10。
> 本文档只描述「要做成什么样、东西存在哪、什么格式」，不含实现代码。
> 实装进度请同步更新 `TODO.md`。

---

## 0. 一句话结论

**知识库是一堆用户自己放进去的 `.md/.txt`。程序每次启动扫一次，和上次的台账比对，
只对「新增 / 改过」的文件重新切片和算向量，结果写进 `data/rag/` 两个文件里。
用户不需要点任何按钮。**

---

## 1. 数据存放总表（最重要的一节）

### 1.1 目录布局

```
<repo>/                              ← 仓库根，代码里从不写盘符
├── asset/RAG/                       ← ① 知识库源文件（用户自己往里放，进 git）
│   ├── 课程笔记.md
│   ├── faq.txt
│   └── 子目录/xxx.md
├── asset/ollama/                    ← ② 便携版 Ollama（没有系统版时用；不进 git）
│   ├── ollama.exe
│   └── lib/…
├── asset/embedding/                 ← ③ 模型（OLLAMA_MODELS 指这里；不进 git）
│   ├── blobs/
│   └── manifests/registry.ollama.ai/library/bge-m3/latest
└── data/                            ← 全部运行时数据（.gitignore：data/*）
    └── rag/                         ← ④ 索引（自动生成，删了重启会自动重建）
        ├── meta.json                ←   台账 + 切片文本（人可读）
        ├── index.npz                ←   向量（二进制）
        └── .tmp/                    ←   原子写入用的临时文件（成功即删）
            ├── meta.json.tmp
            └── index.npz.tmp
```

### 1.2 逐个文件说清楚

| 文件 | 路径 | 格式 | 谁写 | 什么时候写 | 进 git？ | 能删吗 |
|---|---|---|---|---|---|---|
| 知识库源文件 | `asset/RAG/**/*.md\|*.txt` | 纯文本（UTF-8） | **用户**手工放 | 任意时间 | ✅ 进 | 删了索引下次启动自动剔除 |
| Ollama 程序 | `asset/ollama/`（没有系统版时才放） | zip 解压出来的 exe + lib | **用户**手工解压 | 一次性 | ❌ 不进（`.gitignore`） | 换机器重新解压 |
| Embedding 模型 | `asset/embedding/{blobs,manifests}` | Ollama 自己的模型仓库格式 | `ollama pull`（`OLLAMA_MODELS` 指这里） | 一次性 / 换模型时 | ❌ 不进（`.gitignore`） | 换机器重新 pull，或从旧机器复制 |
| 索引台账 + 切片 | `data/rag/meta.json` | JSON（UTF-8，2 空格缩进） | 程序 | 每次启动同步后 | ❌ 不进（`data/*`） | ✅ 删了自动重建 |
| 向量矩阵 | `data/rag/index.npz` | NumPy `.npz`（未压缩，`float32`） | 程序 | 同上，与 json 成对 | ❌ 不进 | ✅ 删了自动重建 |
| 临时文件 | `data/rag/.tmp/*` | 同目标文件 | 程序 | 写入过程中 | ❌ 不进 | ✅ 残留文件启动时清理 |
| 配置 | `data/settings.ini` | INI（`QSettings`） | 程序 + 用户可手改 | 设置页改动时 | ❌ 不进 | 删了回到默认值 |

**为什么不用 sqlite**：数据量在几 MB 级别（512 块 × 1024 维 ≈ 2 MB），
两个文件就能装完；`.npz` + `json` 用 numpy 直接读，少一个依赖、少一层事务语义。
块数上限 2000（见第 6 节），超过这个量级再考虑 sqlite。

### 1.3 路径规则（和人格那套一致，避免再吵一次）

- 代码里**不出现任何盘符**：根目录从 `settings_store.data_dir()` 派生，
  可用环境变量 `DSAI_DATA_DIR` 整体覆盖（测试用）。
- 知识库目录 `rag_dir` 在 `settings.ini` 里存**相对仓库根的路径**（如 `asset/RAG`）。
  用户在设置页选到仓库外的目录时才存绝对路径——那是数据，不是代码。
- `data/rag/` 位置不单独配置：永远是 `<data_dir>/rag`。

---

## 2. 文件格式（逐字段）

### 2.1 `data/rag/meta.json`

```jsonc
{
  "version": 1,                       // 格式版本；将来改结构靠它判断
  "signature": "sha1:9f3c2a…",        // 见 2.3，任何一项变了就全量重建
  "signature_parts": {                // 参与 signature 的原始值，方便排查
    "root": "asset/RAG",              // 知识库目录（相对仓库根）
    "model": "bge-m3",                // embedding 模型名
    "dim": 1024,                      // 向量维度
    "chunk_chars": 480,
    "chunk_overlap": 64,
    "max_file_mb": 2,
    "exts": [".md", ".txt"]
  },
  "built_at": "2026-11-12T00:20:11+08:00",
  "stats": {
    "files": 38,                      // 成功入库的文件数
    "chunks": 512,                    // 块总数
    "skipped": [                      // 跳过原因要能看见，别静默吞掉
      {"rel": "huge.pdf", "reason": "unsupported_ext"},
      {"rel": "big.md",  "reason": "too_large"},
      {"rel": "lock.md", "reason": "read_failed"}
    ]
  },

  // ---- 台账：这就是「记录选定文件夹里有哪些文件」 ----
  "files": {
    "课程笔记.md": {
      "size": 8421,                   // 字节
      "mtime_ns": 1765812345678901234,// 纳秒级；比对变化只看 size+mtime
      "sha256": "9f3c2a…",            // 只在 size/mtime 变了才算
      "chunks": 7,                    // 该文件贡献了几块
      "indexed_at": 1765812400        // unix 秒
    }
  },

  // ---- 切片正文：顺序即 index.npz 的行号 ----
  "chunks": [
    {
      "i": 0,                         // 行号，等于数组下标，冗余存一份便于校验
      "digest": "a1b2c3d4e5f6",       // text 的 sha1 前 12 位；与 npz 里对齐
      "text": "资料：安装 › 后端\n（来源：课程笔记.md L42-L58）\n\nOllama 默认监听 11434 端口…",
      "source": "课程笔记.md",         // 主来源（相对 rag_dir）
      "heading": "安装 › 后端",        // 标题链，没有标题就是空串
      "start_line": 42,
      "end_line": 58,
      "dupes": []                     // 内容完全相同的其它文件（去重后记在这里）
    }
  ]
}
```

- **`text` 是切片进 embedding 的原文**，也是将来拼进提示词的原文。
  前缀 `资料：<heading>` 与 `（来源：<file> L<起>-<止>）` 在**切片阶段就写进 text**，
  保证单块可读、可回溯；模型回答时也自然能引用来源。
- 编码：UTF-8，`ensure_ascii=False`（中文直接可读，不用转义）。
- 写盘方式：**临时文件 → `os.replace` 原子替换**（先 npz 后 json，见第 5 节）。

### 2.2 `data/rag/index.npz`

`.npz` 其实是 zip 包，里面两个数组：

| 键 | 形状 / dtype | 含义 |
|---|---|---|
| `vectors` | `float32 [N, D]` | 每块 L2 归一化后的单位向量，`N = len(meta.chunks)` |
| `digests` | `str [N]`（`<U12`） | 与 `meta.chunks[i].digest` 逐行对齐，用来交叉校验 |

- **归一化在存的时候做**，检索时直接点积就等于余弦，省一次除法：

  $$\cos(\mathbf{q},\mathbf{d}) = \mathbf{q}\cdot\mathbf{d}
  \quad\text{（两者都已是单位向量）}$$

- 大小估算：512 块 × 1024 维 × 4 B ≈ **2.1 MB**；2000 块 ≈ 8 MB，可接受。
- 不需要向量数据库：查一次是全矩阵乘向量（`vectors @ q`），512 行是微秒级。

### 2.3 signature（什么时候必须全量重建）

```
signature = sha1( root | model | dim | chunk_chars | chunk_overlap | max_file_mb | exts )
```

任何一项变化 → 旧向量的维度和口径都不对了 → **整库重切**，并在设置页明说
「embedding 模型变了，正在重建」。只是加/改文件 → 走差量，永远不重建。

启动时还要做一次**一致性校验**（比 signature 更狠，防人为篡改/半截写入）：

1. `len(meta.chunks) == vectors.shape[0] == len(npz["digests"])`
2. 每行 `npz["digests"][i] == meta.chunks[i].digest`
3. `vectors.shape[1] == signature_parts.dim`

任一条不过 → 丢弃缓存，当作「首次」，整库重建。

---

## 3. 配置项（`data/settings.ini`，`[chat]` 段）

沿用已有的三个键名，其余新增；**全部有默认值，坏了不影响启动**。

```ini
[chat]
rag_dir=asset/RAG                     ; 相对仓库根；空 = asset/RAG
rag_ollama=http://127.0.0.1:11434     ; Ollama 地址
rag_embedding=bge-m3                  ; 模型名
rag_enabled=true                      ; 总开关（演示时可关掉对比）
rag_top_k=4                           ; 每次检索注入几块（设置页可调，1~20）
rag_timeout_ms=3000                   ; 单次检索最长等待（设置页可调，200~15000）
rag_min_score=0.35                    ; 余弦下限，低于此值宁可不注入
rag_chunk_chars=480                   ; 切块目标字数
rag_chunk_overlap=64                  ; 超长段滑窗重叠
rag_max_file_mb=2                     ; 单文件上限，超过跳过并记 skipped
rag_max_chunks=2000                   ; 块数上限，超了报错提示精简知识库
rag_inject_chars=3000                 ; 注入内容总字数上限（防爆上下文）
```

**迁移**：现在 `settings.ini` 里的 `rag_dir` 误指到
`data/personality/FatWhale`。启动时若 `rag_dir` 落在 `data/personality/` 内 →
当空处理并用 `asset/RAG`（不静默改用户 ini，只在设置页显示真实生效值）。

### 3.1 用户可调的检索参数（全部搬进了设置页）

2026-11-12 用户要求「把 ini 里那几个选项也加到设置里，给用户更多操作空间」，
所以下面**每一项都有界面控件**，不用再手改 ini：

| 设置项 | ini 键 | 控件 | 范围 | 默认 |
|---|---|---|---|---|
| 启用知识库检索 | `rag_enabled` | 勾选框 | — | 开 |
| Ollama 地址 | `rag_ollama` | 输入框 | — | `http://127.0.0.1:11434` |
| Embedding 模型名 | `rag_embedding` | 输入框 | — | `bge-m3` |
| 返回条数 @k | `rag_top_k` | `QSpinBox` | 1–20 | **4** |
| 检索超时 | `rag_timeout_ms` | `QSpinBox`（步长 500） | 200–15000 ms | **3000** |
| 相似度阈值 | `rag_min_score` | `QDoubleSpinBox`（两位小数） | 0–1 | **0.35** |
| **块长度** | `rag_chunk_chars` | `QSpinBox`（步长 20） | 120–2000 | **480** |
| **块重叠** | `rag_chunk_overlap` | `QSpinBox`（步长 8） | 0–500 | **64** |
| 单文件上限 | `rag_max_file_mb` | `QSpinBox` | 1–64 MB | **2** |
| 块数上限 | `rag_max_chunks` | `QSpinBox` | 50–20000 | **2000** |
| 注入字数上限 | `rag_inject_chars` | `QSpinBox` | 200–20000 | **3000** |

越界一律**夹到边界**（手改 ini 写 `999` / `-5` / `abc` 都不会让程序崩，测试里盯着）。
控件值一变就落盘，没有保存按钮。

**生效时机**：检索类（@k / 超时 / 阈值 / 注入字数）下一次提问生效；
**切块类（块长度 / 重叠 / 单文件上限 / 块数上限）会改签名 → 整库重切**，
下一次同步生效，点「重新扫描」立即执行。

**@k 的含义**：一次提问最多把 **@k 块**资料塞进提示词。
- 它还受两个上限夹击：`rag_inject_chars`（默认 3000 字）与「低于 `rag_min_score` 的块直接丢」。
  所以「@k=8」也可能只注入 3 块——**@k 是上限，不是保证**。
- 语义：`@k` 大 → 召回更全但提示词更长、更容易被无关内容干扰；小 → 更聚焦但可能漏。
  演示时先 3~5，需要「多角度」时再调大。

**超时的含义**：从「用户按下发送」到「检索结果到手」的**最长等待**。
- 只作用于**查询**这一步（一次 `/api/embed` + 一次矩阵乘）。
  建索引那一步是后台跑的，用固定 60 秒/批，不受这个值影响（也不能被它拖成 200 ms）。
- 到点没回来 → **放弃本次检索，照常把消息发出去**（不注入、不报错、不弹窗），
  原因打到控制台 + 会话事件里。
- 默认 3000 ms 的理由：本机 Ollama 查一次通常 30~200 ms，3 秒足够兜住冷启动
  （模型首次加载），又不至于让人明显感到「发送慢」。
- 取值太小（< 200 ms）基本等于关掉 RAG，所以下限卡 200。

> 索引阶段的 60 秒/批是常量，不进设置页：它只在首次全量或大改时用一次，
> 暴露出来只会让人误以为调小它就能加速。

---

## 4. 代码模块（新建 / 修改）

### 4.1 新增：`src/dsai4431_chatbot/core/rag/`

| 文件 | 职责 | 依赖 |
|---|---|---|
| `paths.py` | 产出 `asset/RAG`、`data/rag` 的绝对路径；算 signature | stdlib |
| `loader.py` | 扫目录（`os.scandir` 递归）、忽略规则、读文本（`utf-8-sig`）、跳过原因 | stdlib |
| `chunker.py` | **纯函数**：文档 → `Chunk` 列表（三级切分，见第 5 节） | stdlib |
| `embedder.py` | 调 Ollama `POST /api/embed`，批量；不可用抛 `EmbedError` | stdlib `urllib` |
| `store.py` | `meta.json` + `index.npz` 读写、原子替换、一致性校验 | numpy |
| `indexer.py` | 差量同步编排（启动时调一次）；进度回调 | 上面几个 |
| `retriever.py` | 问题 → 向量 → 点积排序 → top-k/阈值 → 拼注入块 | numpy |
| `__init__.py` | 对外只暴露 `sync_once()` / `search()` / `IndexStatus` | — |

### 4.2 修改

| 文件 | 改什么 |
|---|---|
| `core/gui/rag_service.py`（新） | Qt 侧封装：`QThreadPool` 跑 `sync_once()`，`progress/ready/failed` 信号；持有只读索引 |
| `core/gui/chat_config.py` | 新增第 3 节那些字段的读写（含 bool/int 的容错，沿用 `_get_bool`） |
| `core/gui/settings_dialog.py` `RagPage` | 状态行变实时；**11 个参数全部有控件**（见 3.1），改动即时存盘；「Full rebuild」→「重新扫描」+「清空索引」；显示 skipped 原因与真实生效目录 |
| `core/gui/main_window.py` | 启动后台同步；`_send` 里在人格 system 之后插检索片段（第 6 节） |
| `core/gui/session_store.py` | 新事件类型 `rag/retrieved`（记录本次注入了哪些块） |
| `asset/language/zh.toml` / `en.toml` | 新增状态/错误文案 |
| `pyproject.toml` | 新 extra：`rag = ["numpy>=1.26"]` |
| `README.md` / `TODO.md` | 目录说明 + 进度 |

---

## 5. 关键算法

### 5.1 切片（三级，纯函数，可复现）

1. **按 markdown 标题切**，记标题链 `安装 › 后端`；
2. **节内按段落累积**到 480 字封块；列表/表格/代码块**不跨块切**；
   碎片（< 120 字且同节有下一块）并进下一块；
3. **只有超长段落**（> 700 字）才滑窗，且**按句子边界**对齐，相邻块重叠 64 字。

每块 `text` 生成时即带上前缀（第 2.1 节示例），`digest = sha1(text)[:12]`。
内容完全相同的块按 `digest` 去重：只 embed 一次，其它来源记进 `dupes`。

### 5.2 启动时差量同步（每次启动一次，不监听、不轮询）

```
扫目录 → {rel: (size, mtime_ns)}
比对 meta.files
├ 新文件      → 切片 → embed
├ size/mtime 变 → 重切片 → embed（只这一个文件）
├ 台账有、盘上没了 → 摘掉它的块
└ 其它        → 直接复用旧向量（零成本）
改名识别：内容 sha256 相同 → 搬向量，不重新 embed
```

并发策略：同步器只有**一个后台任务**，运行中被再次触发（启动 + 用户点「重新扫描」）
就合并成一次，绝不并发写索引。

### 5.3 写入协议（防半截文件）

```
1) 内存里算出 meta dict 与 vectors 数组
2) 写 data/rag/.tmp/index.npz.tmp、.tmp/meta.json.tmp（flush + fsync）
3) os.replace(.tmp/index.npz.tmp → index.npz)
4) os.replace(.tmp/meta.json.tmp → meta.json)
5) 清空 .tmp/
```

第 3、4 步之间被打断 → 下次启动靠 2.3 的一致性校验发现，自动重建。
**任何时刻磁盘上都有一份完整可用的旧索引。**

---

## 6. 检索与注入（发消息时发生什么）

1. 用户发消息 → 读当前配置：`@k = rag_top_k`、`budget = rag_timeout_ms`；
2. 拿**当前这一句**（不含历史）去 embed，**整个检索过程套一个 `budget` 的截止时间**；
3. `scores = vectors @ q`，取前 `@k` 个，再过滤 `score < rag_min_score`
   （两步是「先取 @k 再卡阈值」，所以实际注入数 ≤ @k）；
4. 拼成**一条独立的 `system` 消息**，插在「人格 system」之后、历史之前：

```
以下是与当前问题相关的资料片段，请优先依据它们回答；
若资料没有相关内容，就照常回答并说明资料里没有。

[片段 1｜来源：课程笔记.md L42-L58｜相关度 0.78]
Ollama 默认监听 11434 端口……

[片段 2｜来源：faq.txt L3-L9｜相关度 0.61]
……
```

5. 超过 `rag_inject_chars` 就按相关度截断；
6. 往 `session.v1.jsonl` 追加一条：

```json
{"type":"rag/retrieved","seq":9,"time":1765812400,
 "data":{"query":"ollama 端口","top_k":4,"elapsed_ms":86,
         "injected":["a1b2c3d4e5f6"],"scores":[0.78,0.61]}}
```

**失败降级**（四种都走同一条路：不注入、照常发）：

| 情况 | 表现 |
|---|---|
| `rag_enabled=false` | 完全不检索 |
| 索引未就绪（启动同步还没跑完） | 不注入 |
| Ollama 不可用 / 返回错误 | 不注入，状态栏「未连接」 |
| **超过 `rag_timeout_ms`** | 不注入，状态栏「检索超时，本次未用知识库」 |
| 无命中（都低于阈值） | 不注入（不提示，等同于正常聊天） |

**RAG 永远不能挡住发消息，也不能让发送慢过 `rag_timeout_ms`。**

---

## 7. 分阶段与验收

| 阶段 | 内容 | 产出 | 验收 | 估时 |
|---|---|---|---|---|
| **S0** | 依赖 + 切片器 | `chunker.py`、`paths.py` | 第 8 节切片测试 8 条全过 | 1.5 h |
| **S1** | 台账 + 差量（不联网，embedder 用假实现） | `loader/store/indexer` | 第 8 节同步测试 9 条全过 | 2 h |
| **S2** | Ollama 接线 + 启动同步 + 设置页状态 + **@k / 超时两个数字框** | `embedder`、`rag_service`、`RagPage` | 真实知识库启动即可用；Ollama 关闭时不崩；改 @k / 超时立刻落盘 | 2 h |
| **S3** | 检索注入 + 会话记录（含超时降级） | `retriever`、`main_window._send` | 第 8 节端到端 4 条 | 1 h |
| **S4**（可选） | 命中来源在气泡上方折叠显示；其余参数（阈值/字数）也可在设置页调 | UI | 截图确认 | 1 h |

---

## 8. 测试清单

### 切片（S0）
| 用例 | 期望 |
|---|---|
| 只有标题无正文 | 不产生空块 |
| 900 字代码块 | 单独成块，不被切断 |
| 3000 字无标点 | 滑窗多块，重叠恰 64 |
| 中英混排 | 不切断英文单词 |
| 同文件切两次 | digest 序列完全相同 |
| 两个文件同段「版权所有」 | 去重后 1 块，`dupes` 记另一个 |
| 标题前缀 | 不重复叠加 |
| 行号 | 块首尾行号与原文对得上（真读原文核） |

### 同步（S1）
| 用例 | 期望 |
|---|---|
| 空 → 放 1 个 md → 同步 | 台账 1 条、块 > 0 |
| 改 1 个字 → 同步 | 只重切该文件，其它 `indexed_at` 不变 |
| 删文件 → 同步 | 块消失，检索不再命中 |
| 改名（内容同） | 不重新 embed（`embed_calls` 计数为 0） |
| 同一内容两个文件 | 按 digest 去重，`dupes` 有值 |
| 超 2 MB 文件 | 进 `skipped`，不中断 |
| 读失败（占用） | 进 `skipped`，不中断 |
| 同步中再次触发 | 合并成一次，索引不坏 |
| 手动毁掉 npz 行数 | 启动时校验失败 → 自动重建 |

### 参数（S2）
| 用例 | 期望 |
|---|---|
| 设置页把 @k 改成 1 | 注入块数 = 1（`rag/retrieved.injected` 只有 1 条） |
| 改成 20 但库里只有 3 块够阈值 | 注入 3 块（@k 是上限，不补足） |
| 数字框输入 0 / 999 | 夹到 1 / 20；ini 里写 `abc` → 回默认 4 |
| 改 @k 后不重启直接提问 | 立刻按新值生效（不用重建索引） |
| 超时设 200 ms + 让 embedder 睡 2 s | 发送不卡、不注入、状态栏提示超时，会话里没有 `rag/retrieved` |
| 超时设 8000 ms + embedder 正常（80 ms） | 注入正常，`elapsed_ms` ≈ 80 |
| 手改 ini 里 `rag_timeout_ms=-1` | 回默认 3000，程序照常启动 |

### 端到端（S3）
| 用例 | 期望 |
|---|---|
| 知识库放一句独有的话，问它 | 回答里出现，且会话有 `rag/retrieved` |
| 问知识库没有的东西 | 不注入（或注入后模型说没有），回答正常 |
| Ollama 未启动时发消息 | 正常聊天，状态栏提示未连接 |
| @k=4 时把注入字数上限压到 200 字 | 注入被截断，`injected` 少于 4 条，不发出去超长内容 |

---

## 9. 明确「这次不做」

- ❌ PDF / DOCX / HTML 解析（只收 `.md` `.txt`；要加再说）
- ❌ 运行中监听文件变化（**只在启动时扫一次**，运行中可用「重新扫描」按钮）
- ❌ 定时轮询
- ❌ 向量数据库 / sqlite / 外置服务
- ❌ 父块-子块（retrieve small, feed large）
- ❌ 重排序模型（rerank）
- ❌ 多知识库切换（一个程序只有一个 `rag_dir`）

---

## 10. 风险与对策

| 风险 | 对策 |
|---|---|
| 首次全量 embed 慢，用户以为卡死 | 后台线程 + 设置页进度 `12/38`；聊天照常可用 |
| 用户把整个盘当知识库 | 块数上限 2000 → 明确报错「知识库太大，请精简」 |
| Ollama 没装/没开 | 索引跳过、聊天正常、状态栏红字说明；不弹窗 |
| 中文文件名/长路径 | 全程 `pathlib`；台账存 POSIX 相对路径 |
| `settings.ini` 里 rag_dir 指错（当前就指到了人格目录） | 启动检测并在设置页显示真实生效目录 |
| 用户手动改 meta.json | 一致性校验失败 → 自动重建，不信任缓存 |

---

## 11. 需要你确认的项（默认值已写进正文）

| 项 | 默认 | 位置 |
|---|---|---|
| 重复内容去重 | 按 digest 去重，`dupes` 记其它来源 | 5.1 |
| embedding 模型 | `bge-m3`（1024 维，中文强）；换成 `nomic-embed-text` 也行，改 ini 后全量重建 | 3 |
| 触发时机 | **只在启动时同步一次** | 5.2 |
| @k 上限 | 4（设置页可调 1~20） | 3.1 |
| 检索超时 | 3000 ms（设置页可调 200~15000） | 3.1 |

除这几处外，其余按本文档执行即可。

---

## 12. 变更记录

| 日期 | 变更 |
|---|---|
| 2026-11-12 00:10 | 初稿：存储规范、切片、启动时差量同步、分阶段 |
| 2026-11-12 00:12 | 新增 3.1：用户可调 @k 与检索超时（设置页两个数字框）；同步更新第 6/7/8 节 |
| 2026-11-12 12:20 | 3.1 扩成「11 个参数全进设置页」（用户要求）；补 §13 实装进度 |
| 2026-11-12 12:30 | 明确 Ollama / 模型放哪：系统已装就用系统的，没装解压到 `asset/ollama`；模型统一 `asset/embedding`（`OLLAMA_MODELS` 指这里） |

---

## 13. 实装进度（2026-11-12 12:20，分支 `RAG`）

| 阶段 | 状态 | 说明 |
|---|---|---|
| S0 切片器 | ✅ | `core/rag/chunker.py`，`test_an_rag_chunker.py` **22/22** |
| S1 台账 / 差量 / store | ✅ | `loader/store/indexer`，`test_ao_rag_index.py` **45/45**（含改名复用向量、去重、坏索引自愈、签名变更重切） |
| S2 设置页 + 启动同步 | ✅ | `RagPage` 11 个控件 + 状态行 + 两个按钮；`rag_service` 后台同步；`test_ap_rag_ui.py` **30/30** |
| S3 检索注入 | ✅ | `main_window._payload` 插第二条 system；会话追加 `rag/retrieved` 事件 |
| Ollama 真联调 | ⏳ **未做**（按用户安排：最后再导模型） | `embedder.py` 已按 `/api/embed` 写好，但**没有对真实 Ollama 跑过**；上模型前先 `ollama pull bge-m3`，再把设置页的模型名改成 `bge-m3` |
| S4 气泡里显示来源 | ❌ 未做（可选） | 计划里的 S4 |

**调试后端**：`DSAI_RAG_EMBED=debug` 时用 `DebugEmbedder`（字符三元组哈希，**无语义**），
只用于没有 Ollama 时走通「扫描→切片→落盘→检索→注入」。测试全用它；
因为向量无语义，测试里查询句要和原文高度重合，否则可能算出负相关被阈值吃掉。

**已知取舍**：
- 启动同步未完成时发消息 → 不注入（`RagService.index()` 在索引为 None 时每次都会重试读盘，
  所以同步一完成，下一条消息就能用，不用重启）
- 运行中改了知识库文件 → 下次启动才生效（或点「重新扫描」）
- 超时/失败原因只打到控制台 + 会话事件，界面上不弹窗（避免打断聊天）

"""RAG 的路径与签名（不含切片/检索逻辑）。

存储规范见仓库根 `RAG_PLAN.md`：

    <repo>/asset/RAG/          知识库源文件（用户放，进 git）
    <data>/rag/meta.json       台账 + 切片文本
    <data>/rag/index.npz       向量（与 meta.chunks 逐行对应）
    <data>/rag/.tmp/           原子写入的临时文件

**这里不写任何盘符**：仓库根从 settings_store.project_root() 拿，
数据目录从 settings_store.data_dir() 拿（可被 DSAI_DATA_DIR 覆盖，测试用）。
"""

from __future__ import annotations

import hashlib
from pathlib import Path

from dsai4431_chatbot.core.gui import settings_store

# 知识库默认目录（相对仓库根）
DEFAULT_KNOWLEDGE_DIR = "asset/RAG"
# 索引目录名（在 data 下）
INDEX_DIRNAME = "rag"
INDEX_VERSION = 1


def project_root() -> Path:
    return settings_store.project_root()


def index_dir() -> Path:
    """`<data>/rag`，不存在就建。"""
    root = settings_store.data_dir() / INDEX_DIRNAME
    root.mkdir(parents=True, exist_ok=True)
    (root / ".tmp").mkdir(exist_ok=True)
    return root


def knowledge_root(raw: str = "") -> Path:
    """把配置里的 `rag_dir` 变成绝对路径。

    - 空 → `<repo>/asset/RAG`
    - 相对 → `<repo>/<raw>`（存 ini 的默认写法，换机器照样能用）
    - 绝对 → 原样（用户自己挑的仓库外目录）
    """
    value = (raw or "").strip().replace("\\", "/")
    if not value:
        return project_root() / DEFAULT_KNOWLEDGE_DIR
    path = Path(value).expanduser()
    if path.is_absolute():
        return path
    return project_root() / path


def rel_to_project(path: Path) -> str:
    """尽量存相对仓库根的 POSIX 路径；在仓库外就返回绝对路径。"""
    path = path.expanduser()
    try:
        return path.resolve().relative_to(project_root().resolve()).as_posix()
    except (ValueError, OSError):
        return str(path)


def signature(cfg) -> str:
    """索引签名：任何一项变了都必须整库重切（维度/口径都不同了）。"""
    parts = [
        "v1",
        str(knowledge_root(getattr(cfg, "rag_dir", "")).resolve()),
        str(getattr(cfg, "rag_embedding", "") or ""),
        str(int(getattr(cfg, "rag_chunk_chars", 480))),
        str(int(getattr(cfg, "rag_chunk_overlap", 64))),
        str(int(getattr(cfg, "rag_max_file_mb", 2))),
        "md,txt",
    ]
    return hashlib.sha1("|".join(parts).encode("utf-8")).hexdigest()


def file_stamp(size: int, mtime_ns: int) -> tuple[int, int]:
    return int(size), int(mtime_ns)

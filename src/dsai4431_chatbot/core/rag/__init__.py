"""本地知识库检索（RAG）。

对外只需要四个函数：

    sync_once(cfg)       启动时跑一次：扫目录 → 差量切片 → 算向量 → 落盘
    load_index()         读回索引（校验不过返回 None）
    search(query, cfg)   查一次（自动套 top-k / 阈值 / 超时）
    build_block(hits)    拼成可注入提示词的一条 system 消息

存储格式见仓库根 `RAG_PLAN.md`。

⚠ **本包顶层不 import numpy**：`store` / `embedder` / `retriever` / `indexer` 用到
numpy，但它们只在函数内部被导入。这样 `chat_config` 之类只想拿个默认值的模块
可以放心 import 这个包，不会因为缺 numpy 就把整个界面拖垮。
"""

from __future__ import annotations

# 纯 stdlib 的子模块：顶层安全
from dsai4431_chatbot.core.rag import chunker, loader, paths

__all__ = [
    "chunker",
    "loader",
    "paths",
    "sync_once",
    "load_index",
    "search",
    "build_block",
    "index_status",
]


def sync_once(cfg, **kwargs):
    from dsai4431_chatbot.core.rag import indexer

    return indexer.sync_once(cfg, **kwargs)


def load_index():
    from dsai4431_chatbot.core.rag import store

    return store.load()


def index_status() -> dict:
    """索引摘要（给状态栏）：文件数 / 块数 / 维度 / 建库时间。"""
    from dsai4431_chatbot.core.rag import store

    return store.summary(store.load())


def search(query: str, cfg, *, index=None, runtime=None):
    from dsai4431_chatbot.core.rag import retriever, store

    current = index if index is not None else store.load()
    return retriever.search(query, current, cfg, runtime=runtime)


def build_block(hits, limit_chars: int = 3000) -> str:
    from dsai4431_chatbot.core.rag import retriever

    return retriever.build_block(hits, limit_chars)

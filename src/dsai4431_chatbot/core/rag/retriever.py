"""检索：问题 → 向量 → 余弦排序 → top-k → 阈值 → 拼成可注入提示词的块。

超时的处理（用户 2026-11-12 要求可配）：整个检索套一个 `rag_timeout_ms` 的预算。
查不动就**放弃本次检索**，让消息照常发出去——RAG 永远不能挡住发送。
"""

from __future__ import annotations

import time
from dataclasses import dataclass, field

import numpy as np

from dsai4431_chatbot.core.rag import embedder as embedder_mod
from dsai4431_chatbot.core.rag import store

# 注入块顶部那句「请依据资料回答」的说明
PROMPT_HEADER = (
    "以下是与当前问题相关的资料片段，请优先依据它们回答；"
    "若资料没有相关内容，就照常回答并说明资料里没有。"
)
# 片段标题行
SNIPPET_TITLE = "[片段 {n}｜来源：{source}{lines}｜相关度 {score:.2f}]"


@dataclass
class Hit:
    text: str
    source: str
    heading: str
    start_line: int
    end_line: int
    score: float
    digest: str

    def where(self) -> str:
        if self.start_line == self.end_line:
            return f" L{self.start_line}"
        return f" L{self.start_line}-L{self.end_line}"


@dataclass
class Retrieval:
    hits: list[Hit] = field(default_factory=list)
    elapsed_ms: int = 0
    timed_out: bool = False
    error: str = ""

    def ok(self) -> bool:
        return bool(self.hits)


def bounds(cfg) -> tuple[int, int, float, int]:
    """从配置里取 (top_k, timeout_ms, min_score, inject_chars)，都带安全夹取。"""
    top_k = _clamp(_int(getattr(cfg, "rag_top_k", 4), 4), 1, 20)
    timeout_ms = _clamp(_int(getattr(cfg, "rag_timeout_ms", 3000), 3000), 200, 15000)
    min_score = _clamp(_float(getattr(cfg, "rag_min_score", 0.35), 0.35), 0.0, 1.0)
    inject_chars = _clamp(_int(getattr(cfg, "rag_inject_chars", 3000), 3000), 200, 20000)
    return top_k, timeout_ms, min_score, inject_chars


def search(
    query: str,
    index: store.Index | None,
    cfg,
    *,
    runtime=None,
) -> Retrieval:
    """查一次。任何失败都返回空 hits + 原因，不抛异常。"""
    started = time.perf_counter()
    top_k, timeout_ms, min_score, _chars = bounds(cfg)

    query = (query or "").strip()
    if not query or index is None or len(index) == 0:
        return Retrieval()

    engine = runtime or embedder_mod.make_embedder(
        cfg, timeout_s=max(0.2, timeout_ms / 1000.0)
    )
    # 查询用的超时必须比建索引小得多：这里按预算现造一个（或改临时的 timeout）
    _apply_timeout(engine, timeout_ms / 1000.0)

    try:
        vector = engine.embed([query])[0]
    except embedder_mod.EmbedError as exc:
        timed_out = "超时" in str(exc) or exc.kind == "unreachable"
        return Retrieval(
            elapsed_ms=int((time.perf_counter() - started) * 1000),
            timed_out=timed_out and exc.kind == "unreachable",
            error=str(exc),
        )

    if time.perf_counter() - started > timeout_ms / 1000.0:
        return Retrieval(
            elapsed_ms=int((time.perf_counter() - started) * 1000),
            timed_out=True,
            error="检索超时",
        )

    scores = index.vectors @ np.asarray(vector, dtype=np.float32)
    order = np.argsort(-scores)[: max(1, top_k)]
    hits: list[Hit] = []
    for row in order:
        score = float(scores[row])
        if score < min_score:
            continue
        chunk = index.chunks[int(row)]
        hits.append(
            Hit(
                text=chunk.get("text", ""),
                source=chunk.get("source", ""),
                heading=chunk.get("heading", ""),
                start_line=int(chunk.get("start_line", 0)),
                end_line=int(chunk.get("end_line", 0)),
                score=score,
                digest=chunk.get("digest", ""),
            )
        )
    return Retrieval(
        hits=hits,
        elapsed_ms=int((time.perf_counter() - started) * 1000),
    )


def build_block(hits: list[Hit], limit_chars: int = 3000) -> str:
    """把命中块拼成一条 system 消息；按相关度顺序，超长就截断。"""
    if not hits:
        return ""
    parts: list[str] = [PROMPT_HEADER, ""]
    used = len(PROMPT_HEADER)
    for number, hit in enumerate(hits, start=1):
        title = SNIPPET_TITLE.format(
            n=number, source=hit.source, lines=hit.where(), score=hit.score
        )
        body = hit.text
        room = limit_chars - used - len(title) - 4
        if room <= 40:
            break
        if len(body) > room:
            body = body[:room].rstrip() + "…"
        parts.append(title)
        parts.append(body)
        parts.append("")
        used += len(title) + len(body) + 2
    return "\n".join(parts).strip()


# ---------------------------------------------------------------------------
# 小工具
# ---------------------------------------------------------------------------
def _apply_timeout(engine, seconds: float) -> None:
    if hasattr(engine, "timeout_s"):
        engine.timeout_s = max(0.2, float(seconds))


def _int(value, default: int) -> int:
    try:
        return int(str(value).strip())
    except (TypeError, ValueError):
        return default


def _float(value, default: float) -> float:
    try:
        return float(str(value).strip())
    except (TypeError, ValueError):
        return default


def _clamp(value, low, high):
    return max(low, min(high, value))

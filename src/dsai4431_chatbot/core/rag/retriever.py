"""检索：问题 → 向量 → 余弦排序 → top-k → 阈值 → 拼成可注入提示词的块。

超时的处理（用户 2026-11-12 要求可配）：整个检索套一个 `rag_timeout_ms` 的预算。
查不动就**放弃本次检索**，让消息照常发出去——RAG 永远不能挡住发送。
"""

from __future__ import annotations

import re
import time
from dataclasses import dataclass, field

import numpy as np

from dsai4431_chatbot.core.rag import embedder as embedder_mod
from dsai4431_chatbot.core.rag import query_terms
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

    pairs = query_terms.variants(query)
    try:
        vectors = engine.embed([text for text, _weight in pairs])
    except embedder_mod.EmbedError as exc:
        timed_out = "超时" in str(exc) or exc.kind == "unreachable"
        return Retrieval(
            elapsed_ms=int((time.perf_counter() - started) * 1000),
            timed_out=timed_out and exc.kind == "unreachable",
            error=str(exc),
        )

    vector = _merge_vectors(vectors, [weight for _text, weight in pairs])

    if time.perf_counter() - started > timeout_ms / 1000.0:
        return Retrieval(
            elapsed_ms=int((time.perf_counter() - started) * 1000),
            timed_out=True,
            error="检索超时",
        )

    scores = index.vectors @ np.asarray(vector, dtype=np.float32)
    scores = _lexical_boost(scores, index.chunks, query)
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
# 查询里出现这类 token 时（缩写、型号、英文舰名），字面命中要额外加权：
# bge-base-zh 对 "MMT"、"AE-10" 这种短词的语义不敏感，纯向量会把正确文档排到 0.4 以下。
LEX_TOKEN = re.compile(r"[A-Za-z][A-Za-z0-9\-]{1,}|[A-Z]{2,}")
# 舰级代号（450 CH / missile CC / S2CC）：文档名和标题里出现整串才算命中，
# 否则 "CH" 会把 250 CH、missile CH 全拉进来，把用户问的那一类挤掉。
CLASS_CODE = re.compile(r"\b(\d{2,4}|[A-Za-z][A-Za-z0-9]{1,3})\s+(CH|CC|BB|LN|CL|DD|FF|FFL|CVE|CVL|MN)\b", re.I)


def _lexical_boost(scores, chunks: list[dict], query: str):
    """字面命中加权：查询里的英文/型号 token 在片段里出现，就加一点分。"""
    tokens: list[str] = []
    for token in LEX_TOKEN.findall(query or ""):
        low = token.lower()
        if len(low) >= 2 and low not in tokens:
            tokens.append(low)
    phrases = [" ".join(m).lower() for m in CLASS_CODE.findall(query or "")]
    if not tokens and not phrases:
        return scores
    out = np.array(scores, dtype=np.float32, copy=True)
    for row, chunk in enumerate(chunks):
        text = (chunk.get("text") or "").lower()
        if not text:
            continue
        # "450mm" 在资料里常写成 "450 mm"，去掉空格再比一次
        squashed = text.replace(" ", "")
        bonus = 0.0
        for token in tokens:
            if f"**{token}**" in text:
                bonus += 0.2          # 术语表里的加粗词条（`- **MMT** …`）
            elif len(token) <= 3:
                # 两三个字母的型号/阵营缩写（SA、OSP、PDT）要整词命中，
                # 否则 "sa" 会命中 "mass"、"sarissa" 这类无关片段。
                if re.search(rf"\b{re.escape(token)}\b", text):
                    bonus += 0.2
            elif token in text or token in squashed:
                bonus += 0.12
        for phrase in phrases:
            slug = (chunk.get("source") or "").rsplit("/", 1)[-1].removesuffix(".md")
            heading = (chunk.get("heading") or "").lower()
            if phrase == slug.replace("-", " ") or phrase in heading:
                bonus += 0.3          # 问的就是这一类，标题/文件名对上了
        if bonus:
            # 每个 token 最多 +0.2，整片最多 +0.36；上限 0.99 保持余弦分数的可比性
            out[row] = min(0.99, float(out[row]) + min(0.5, bonus))
    return out


def _merge_vectors(vectors: list, weights: list[float]) -> np.ndarray:
    """多个查询变体按权重求平均向量（中文原句 + 英文术语补充），再归一化。"""
    matrix = np.asarray(vectors, dtype=np.float32)
    if len(vectors) == 1:
        return matrix[0]
    w = np.asarray(weights, dtype=np.float32)
    w = w / w.sum() if float(w.sum()) > 0 else np.full(len(vectors), 1.0 / len(vectors), dtype=np.float32)
    merged = (matrix * w[:, None]).sum(axis=0)
    norm = float(np.linalg.norm(merged))
    return merged / norm if norm > 0 else merged


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

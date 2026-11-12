"""RAG 的工具调用（tool calling）路由。

模型的 `search_knowledge` 请求 → 我们真去检索 → 变成一条 `role="tool"` 消息回灌。
本模块**不碰界面**，只做「一次调用 ↔ 一次检索」的翻译，方便单测。
"""

from __future__ import annotations

import json
import time
from dataclasses import dataclass

TOOL_NAME = "search_knowledge"
# 一次问答里最多来回几轮工具调用（防止模型无限查）
MAX_ROUNDS = 3

TOOL_SPEC = {
    "type": "function",
    "function": {
        "name": TOOL_NAME,
        "description": (
            "检索用户本地的知识库（项目文档、笔记、配置文件说明），"
            "返回若干资料片段（带来源文件与行号）。"
            "当问题涉及项目细节、既定约定、具体配置这类需要事实依据的内容时，"
            "先调用它再回答；不要凭记忆猜这些细节。"
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "检索用的关键词或问题，用中文即可",
                }
            },
            "required": ["query"],
        },
    },
}


@dataclass
class ToolOutcome:
    """一次工具调用的结果（同时用于回灌模型和界面展示）。"""

    ok: bool
    content: str
    query: str = ""
    hits: int = 0
    top_score: float = 0.0
    elapsed_ms: int = 0
    error: str = ""
    call_id: str = ""

    def summary(self) -> str:
        """界面上那一行小字用。"""
        if not self.ok:
            return f"检索失败：{self.error or '未知原因'}"
        if not self.hits:
            return f"检索「{self.query}」· 没有找到相关资料"
        return (
            f"检索「{self.query}」· {self.hits} 段 · "
            f"最高 {self.top_score:.2f} · {self.elapsed_ms}ms"
        )


def assistant_message(calls: list[dict]) -> dict:
    """把模型这一轮的 tool_calls 还原成要追加进 messages 的 assistant 消息。"""
    return {
        "role": "assistant",
        "content": "",
        "tool_calls": [
            {
                "id": call.get("id") or f"call_{index}",
                "type": "function",
                "function": {
                    "name": call.get("name") or TOOL_NAME,
                    "arguments": call.get("arguments") or "{}",
                },
            }
            for index, call in enumerate(calls)
        ],
    }


class ToolRouter:
    """把一次工具调用变成一次检索 + 一条 tool 消息。"""

    def __init__(self, rag, *, max_chars: int = 3000) -> None:
        self.rag = rag
        self.max_chars = int(max_chars)

    def run(self, call: dict) -> ToolOutcome:
        call_id = str(call.get("id") or "")
        name = str(call.get("name") or "")
        if name and name != TOOL_NAME:
            return ToolOutcome(
                ok=False,
                content=f"没有名为 {name} 的工具，只能调用 {TOOL_NAME}。",
                error=f"未知工具 {name}",
                call_id=call_id,
            )

        raw = call.get("arguments") or "{}"
        query = ""
        try:
            args = json.loads(raw) if isinstance(raw, str) else dict(raw)
            if isinstance(args, dict):
                query = str(args.get("query") or args.get("q") or "").strip()
        except (ValueError, TypeError):
            # 模型偶尔给出不合法 JSON：把原文当查询词兜一层
            query = str(raw).strip()[:200]

        if not query:
            return ToolOutcome(
                ok=False,
                content="检索失败：没有给出 query 参数。",
                error="缺少 query",
                call_id=call_id,
            )

        started = time.perf_counter()
        try:
            result = self.rag.search(query) if self.rag is not None else None
        except Exception as exc:                 # noqa: BLE001 - 工具不能把异常抛给模型
            return ToolOutcome(
                ok=False,
                content=f"检索失败：{exc}",
                query=query,
                error=str(exc),
                call_id=call_id,
                elapsed_ms=int((time.perf_counter() - started) * 1000),
            )

        from dsai4431_chatbot.core.rag import retriever

        hits = list(getattr(result, "hits", []) or [])
        elapsed = int((time.perf_counter() - started) * 1000)
        error = str(getattr(result, "error", "") or "")
        if not hits:
            content = (
                f"检索「{query}」没有命中任何资料"
                + (f"（{error}）" if error else "")
                + "。请如实告诉用户资料里没有相关内容，不要编造。"
            )
            return ToolOutcome(
                ok=bool(error) is False,
                content=content,
                query=query,
                error=error,
                elapsed_ms=elapsed,
                call_id=call_id,
            )

        block = retriever.build_block(hits, self.max_chars)
        content = f"检索「{query}」命中 {len(hits)} 段资料：\n\n{block}"
        return ToolOutcome(
            ok=True,
            content=content,
            query=query,
            hits=len(hits),
            top_score=float(hits[0].score),
            elapsed_ms=elapsed,
            call_id=call_id,
        )

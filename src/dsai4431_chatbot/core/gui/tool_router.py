"""RAG 的工具调用（tool calling）路由。

模型的 `search_knowledge` 请求 → 我们真去检索 → 变成一条 `role="tool"` 消息回灌。
本模块**不碰界面**，只做「一次调用 ↔ 一次检索」的翻译，方便单测。
"""

from __future__ import annotations

import json
import re
import time
from dataclasses import dataclass

TOOL_NAME = "search_knowledge"
# 第二个工具：拼一条 `.fleet` 写盘。
# 模型写不了这个文件（槽位 key 是 22 字符随机串，手写的 MT1/CMP1 会被游戏静默跳过），
# 所以「给我个舰队文件」这类请求必须落到代码上：模型只挑船，序列化由 core.fleet.compose 做。
FLEET_TOOL_NAME = "build_fleet_file"
# 一次问答里最多来回几轮工具调用（防止模型无限查）。
# 造舰/配队这类请求要连着查「舰级要求 → 槽位表 → 部件尺寸与点数」，3 轮根本走不完，
# 于是一直停在「我还没查到槽位表」上；6 轮够走完三跳还留一次回查。
MAX_ROUNDS = 6
# 结果最低分（B 防线）：最高分低于它 → 干脆告诉模型「没查到」，不塞噪声片段。
# bge-base 的分数会压缩（相关 0.6~0.85、无关 0.33~0.5），实测卡 0.5 比较稳。
MIN_TOOL_SCORE = 0.5
# 工具调用协议提示：DeepSeek 偶尔把调用写成 DSML 文本混进正文（用户会看到一堆
# `<｜｜DSML｜｜ calls>` 垃圾）。明确要求走工具通道，同时客户端另有兜底解析。
PROTOCOL_HINT = (
    "调用工具时请使用工具通道（tool_calls），不要在回答正文里手写 "
    "XML / DSML 之类的标记文本；正文只写给用户看的内容。"
)

TOOL_SPEC = {
    "type": "function",
    "function": {
        "name": TOOL_NAME,
        "description": (
            "检索用户本地的知识库（按主题分成的文档集合），返回若干资料片段，"
            "每段都带来源文件路径、行号与相关度。\n"
            "用法：query 写关键词，不要写整句；一条查询只查一件事；中文问题要附上资料里的英文名"
            "（例如「脊髓炮 spinal mount」「贪污 greed」）；同一问题通常 2-3 次调用。\n"
            "接续：如果片段里出现「见 xxx.md」「详见 …」或某个文件名，直接拿那个文件名作下一次查询；"
            "如果一个片段只给出了「去哪查」而没有关键数字（尺寸、点数、供电、口径），继续查，不要拿它当结论。\n"
            "需要事实依据（项目细节、既定约定、具体数值）时先调用它再回答，不要凭记忆猜。"
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "检索关键词：实体名 + 想知道的属性，中文英文混写即可",
                }
            },
            "required": ["query"],
        },
    },
}


FLEET_TOOL_SPEC = {
    "type": "function",
    "function": {
        "name": FLEET_TOOL_NAME,
        "description": (
            "把现成的样板船拼成一条可以直接载入游戏的舰队文件（`.fleet`），写到本地磁盘，"
            "返回绝对路径、船数、点数、模板库数量和校验结果。\n"
            "什么时候用：用户要「给我一条舰队」「造好发我」「生成 .fleet」「贴出来我复制」时，"
            "**必须调用它**；不要在回答正文里手写 XML——槽位 key 是 22 字符的随机串，"
            "手写的 `MT1`/`CMP1` 会被游戏当成无效 key 静默跳过，槽位全空。\n"
            "samples 填样板船的文件名（`sample fleets/` 里那 61 条，形如 `gun MN - Excuse The Interruption`），"
            "**留空就返回全部可选项**；重复写同一个名字 = 多带几艘。名字可以只写舰级或模糊关键词。\n"
            "命名：用户点了名（「叫 XX 一号」「命名为 …」）就逐条填 `renames`；"
            "没点名就**不要**填，工具会按舰级自动编号（`450 CH 1`、`450 CH 2`、`450 CC 1`），"
            "比样板原名（`Umber Ox`）清楚得多；用户说「保留原名」才填 `keep_names: true`。\n"
            "ship 阵营不能混：一条 `.fleet` 只有一个 `FactionKey`，混了会被拒绝。"
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "samples": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "样板船文件名或关键词，可重复；留空 = 列出全部可选项",
                },
                "name": {
                    "type": "string",
                    "description": "舰队名（也会当文件名），例如「3k 前线 Garnet」",
                },
                "renames": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": (
                        "可选：按顺序给每艘船起的新名字（用户明确点名时才填）。"
                        "个数少于船数时，剩下的按舰级自动编号。"
                    ),
                },
                "keep_names": {
                    "type": "boolean",
                    "description": "可选：保留样板船原来的名字（只在用户明确要求时用）",
                },
            },
            "required": [],
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
    kind: str = TOOL_NAME          # 哪个工具（界面提示行的图标与文案按它分）
    path: str = ""                 # 生成文件时的落盘路径
    ships: int = 0                 # 生成文件时的船数

    def summary(self) -> str:
        """界面上那一行小字用。"""
        if self.kind == FLEET_TOOL_NAME:
            if self.ok and self.path:
                return f"已生成舰队文件 · {self.ships} 艘 · {self.path}"
            if self.ok:
                return f"样板船清单 · {self.hits} 条"
            return f"生成舰队文件失败：{self.error or self.content[:60]}"
        if self.hits:
            return (
                f"检索「{self.query}」· {self.hits} 段 · "
                f"最高 {self.top_score:.2f} · {self.elapsed_ms}ms"
            )
        if self.error == "相关度不足":
            return f"检索「{self.query}」· 相关度不足（最高 {self.top_score:.2f}）"
        if self.error:
            return f"检索「{self.query}」失败：{self.error}"
        return f"检索「{self.query}」· 没有找到相关资料"


def assistant_message(calls: list[dict], reasoning: str = "") -> dict:
    """把模型这一轮的 tool_calls 还原成要追加进 messages 的 assistant 消息。

    **思考模式下必须把 `reasoning_content` 原样带回去**，否则服务端直接 400：
    `The reasoning_content in the thinking mode must be passed back to the API.`
    """
    message = {
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
    if reasoning:
        message["reasoning_content"] = reasoning
    return message


class ToolRouter:
    """把一次工具调用变成一次检索 + 一条 tool 消息。"""

    def __init__(self, rag, *, max_chars: int = 3000) -> None:
        self.rag = rag
        self.max_chars = int(max_chars)

    def run(
        self,
        call: dict,
        *,
        min_score: float | None = None,
        max_chars: int | None = None,
    ) -> ToolOutcome:
        """执行一次工具调用。

        `min_score` 是可信度门槛（设置页可调）；不给就用模块默认值。
        `max_chars` 覆盖回灌给模型的资料总字数（设置页的「注入字数上限」）。
        """
        threshold = MIN_TOOL_SCORE if min_score is None else float(min_score)
        limit_chars = self.max_chars if max_chars is None else int(max_chars)
        call_id = str(call.get("id") or "")
        name = str(call.get("name") or "")
        raw = call.get("arguments") or "{}"
        args: dict = {}
        try:
            parsed = json.loads(raw) if isinstance(raw, str) else dict(raw)
            if isinstance(parsed, dict):
                args = parsed
        except (ValueError, TypeError):
            args = {}

        if name == FLEET_TOOL_NAME:
            return self._run_fleet(args, call_id=call_id)
        if name and name != TOOL_NAME:
            return ToolOutcome(
                ok=False,
                content=f"没有名为 {name} 的工具，只能调用 {TOOL_NAME} 或 {FLEET_TOOL_NAME}。",
                error=f"未知工具 {name}",
                call_id=call_id,
            )

        query = ""
        try:
            if args:
                query = str(args.get("query") or args.get("q") or "").strip()
        except (ValueError, TypeError):
            query = ""
        if not query and not args:
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
        # B 防线：不够相关的一律不给模型，免得它被噪声带偏、或误判「知识库里没有」
        strong = [hit for hit in hits if float(hit.score) >= threshold]
        if hits and not strong:
            best = float(hits[0].score)
            return ToolOutcome(
                ok=False,
                content=(
                    f"检索「{query}」没有找到足够相关的资料"
                    f"（最高相关度只有 {best:.2f}，低于 {threshold:.2f} 的可信阈值）。"
                    "请如实告诉用户知识库里没有相关内容，不要编造；也不要拿低分片段当依据。"
                ),
                query=query,
                hits=0,
                top_score=best,
                elapsed_ms=elapsed,
                error="相关度不足",
                call_id=call_id,
            )
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

        block = retriever.build_block(strong, limit_chars)
        content = f"检索「{query}」命中 {len(strong)} 段资料：\n\n{block}"
        return ToolOutcome(
            ok=True,
            content=content,
            query=query,
            hits=len(strong),
            top_score=float(strong[0].score),
            elapsed_ms=elapsed,
            call_id=call_id,
        )

    # --- 生成舰队文件 ---------------------------------------------------
    def _run_fleet(self, args: dict, *, call_id: str) -> ToolOutcome:
        """`build_fleet_file`：挑样板船 → 写 `.fleet` → 校验 → 报路径。"""
        from dsai4431_chatbot.core.fleet import compose

        started = time.perf_counter()
        raw_samples = args.get("samples") or []
        if isinstance(raw_samples, str):
            raw_samples = [raw_samples]
        samples = [str(x).strip() for x in raw_samples if str(x).strip()]
        name = str(args.get("name") or args.get("fleet_name") or "").strip()
        renames = args.get("renames") or args.get("names") or []
        if isinstance(renames, str):
            renames = [renames]
        renames = [str(x).strip() for x in renames]
        # 模型偶尔把一串名字塞进一个字符串里
        if len(renames) == 1 and ("," in renames[0] or "、" in renames[0]):
            renames = [x.strip() for x in re.split(r"[,、]", renames[0]) if x.strip()]
        keep_names = bool(args.get("keep_names"))

        try:
            if not samples:
                rows = compose.list_samples()
                lines = [f"可选样板船 {len(rows)} 条（阵营 · 点数 · 文件名）："]
                lines += [
                    f"- {r['class']} · {r['points']:.0f} 点 · {r['faction'].split('/')[-1]} · {r['name']}"
                    for r in rows
                ]
                lines.append(
                    "挑好后带上 samples 再调一次；samples 留空只是列清单，不会生成文件。"
                )
                return ToolOutcome(
                    ok=True,
                    content="\n".join(lines),
                    kind=FLEET_TOOL_NAME,
                    hits=len(rows),
                    elapsed_ms=int((time.perf_counter() - started) * 1000),
                    call_id=call_id,
                )
            report = compose.compose(
                samples, name=name, renames=renames, keep_names=keep_names
            )
        except Exception as exc:                  # noqa: BLE001 - 工具不能把异常抛给模型
            return ToolOutcome(
                ok=False,
                content=f"生成舰队文件失败：{exc}",
                error=str(exc),
                kind=FLEET_TOOL_NAME,
                elapsed_ms=int((time.perf_counter() - started) * 1000),
                call_id=call_id,
            )

        elapsed = int((time.perf_counter() - started) * 1000)
        if not report.get("ok"):
            reason = report.get("error") or "；".join(report.get("problems") or [])
            return ToolOutcome(
                ok=False,
                content=f"生成失败：{reason}",
                error=reason,
                kind=FLEET_TOOL_NAME,
                elapsed_ms=elapsed,
                call_id=call_id,
            )
        return ToolOutcome(
            ok=True,
            content=compose.summary_text(report),
            query=" / ".join(samples),
            hits=1,
            kind=FLEET_TOOL_NAME,
            path=str(report.get("path") or ""),
            ships=int(report.get("ships") or 0),
            elapsed_ms=elapsed,
            call_id=call_id,
        )

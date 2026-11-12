"""切片：把一份文本切成「语义自足、可回溯来源」的块。

三级切分（见 `RAG_PLAN.md` §5.1）：

1. 按 markdown 标题切节，记下标题链（如 `安装 › 后端`）与行号；
2. 节内按**块**（段落 / 列表 / 表格 / 代码块）累积到目标字数；代码块、表格不跨块切；
3. 只有比硬上限还长的块才滑窗，且**按句子边界**对齐、带重叠。

全是纯函数：同样的输入永远得到同样的块（含 digest），方便增量同步与测试。
"""

from __future__ import annotations

import hashlib
import re
from dataclasses import dataclass
from pathlib import Path

# 目标块大小；调用方可以按配置覆盖
DEFAULT_SIZE = 480
DEFAULT_OVERLAP = 64
# 超过这个长度就必须滑窗（不管 size 配得多大，避免单块把上下文撑爆）
HARD_MAX = 700
# 小于这个长度的碎片并进相邻块
MIN_CHARS = 120
# 占位：句末标点 + 换行（中文长句主要靠这些断）
SENT_END = set("。！？；…!?;\n")
HEADING_RE = re.compile(r"^(#{1,6})\s+(.*\S)\s*$")
LIST_RE = re.compile(r"^\s*(?:[-*+]|\d+[.)])\s+")


@dataclass(frozen=True)
class Chunk:
    """一块切片。`text` 已经带好「标题 + 来源」前缀，可直接 embed / 注入提示词。"""

    text: str
    source: str
    heading: str
    start_line: int
    end_line: int
    digest: str


def digest_of(text: str) -> str:
    return hashlib.sha1(text.encode("utf-8")).hexdigest()[:12]


# ---------------------------------------------------------------------------
# 对外入口
# ---------------------------------------------------------------------------
def split_document(
    source: str,
    text: str,
    *,
    size: int = DEFAULT_SIZE,
    overlap: int = DEFAULT_OVERLAP,
    hard_max: int = HARD_MAX,
    min_chars: int = MIN_CHARS,
) -> list[Chunk]:
    """把一份文档切成若干个 `Chunk`。`source` 只用于记录来源，不做 IO。"""
    size = max(80, int(size))
    overlap = max(0, min(int(overlap), size // 2))
    hard_max = max(int(hard_max), size)

    text = (text or "").replace("\r\n", "\n").replace("\r", "\n")
    if not text.strip():
        return []

    chunks: list[Chunk] = []
    for heading, lines, first_line in _split_sections(text):
        pieces = _pack_section(lines, first_line, size, hard_max, min_chars)
        for body, start, end in pieces:
            full = _with_prefix(body, source, heading, start, end)
            chunks.append(
                Chunk(
                    text=full,
                    source=source,
                    heading=heading,
                    start_line=start,
                    end_line=end,
                    # digest 只算**正文**，不含「资料：…（来源：…）」前缀：
                    # 这样「同一个文件改名」「两个文件里有同一段文字」都能识别成
                    # 同一块 → 向量可以直接搬，不用重新 embed（RAG_PLAN 5.1 去重）
                    digest=digest_of(body),
                )
            )
    return _dedupe(chunks)


def split_text_only(source: str, text: str, **kwargs) -> list[str]:
    """测试/调试用：只要正文。"""
    return [c.text for c in split_document(source, text, **kwargs)]


# ---------------------------------------------------------------------------
# 第一级：按标题切节
# ---------------------------------------------------------------------------
def _split_sections(text: str) -> list[tuple[str, list[str], int]]:
    """→ [(标题链, 正文行, 正文首行行号)]；标题行本身不进正文。"""
    lines = text.split("\n")
    sections: list[tuple[str, list[str], int]] = []
    stack: list[tuple[int, str]] = []          # (级别, 标题)
    body: list[str] = []
    body_start = 1

    def flush() -> None:
        nonlocal body, body_start
        if any(line.strip() for line in body):
            heading = " › ".join(name for _lvl, name in stack)
            sections.append((heading, body, body_start))
        body = []

    for index, line in enumerate(lines, start=1):
        match = HEADING_RE.match(line)
        if match:
            flush()
            level = len(match.group(1))
            while stack and stack[-1][0] >= level:
                stack.pop()
            stack.append((level, match.group(2)))
            body_start = index + 1
            continue
        if not body:
            body_start = index
        body.append(line)
    flush()

    # 一个字都没有的文档（只有标题）返回空：调用方天然得到 0 块
    return sections


# ---------------------------------------------------------------------------
# 第二级：节内按块累积
# ---------------------------------------------------------------------------
def _blocks(lines: list[str], first_line: int) -> list[tuple[list[str], int, int, str]]:
    """把节内正文切成「块」：段落 / 列表 / 表格 / 代码块。

    → [(各行, 起始行号, 结束行号, 类型)]，行号按**原文**计（first_line 是这段第一行）。
    类型是 `para` / `list` / `table` / `fence`；后两种**不切开**（见 _pack_section）。
    """
    blocks: list[tuple[list[str], int, int, str]] = []
    buf: list[str] = []
    buf_start = first_line
    buf_kind = "para"
    line_no = first_line - 1
    in_fence = False
    mode = ""            # "" / "list" / "table" / "fence"

    def push(end_line: int) -> None:
        nonlocal buf
        if any(item.strip() for item in buf):
            blocks.append((buf, buf_start, end_line, buf_kind))
        buf = []

    for raw in lines:
        line_no += 1
        stripped = raw.strip()

        if in_fence:
            buf.append(raw)
            if stripped.startswith("```"):
                in_fence = False
                mode = ""
                push(line_no)
            continue

        if stripped.startswith("```"):
            push(line_no - 1)
            in_fence = True
            mode = "fence"
            buf = [raw]
            buf_start = line_no
            buf_kind = "fence"
            continue

        if not stripped:                        # 空行 = 块边界
            push(line_no - 1)
            mode = ""
            continue

        kind = "table" if stripped.startswith("|") else ("list" if LIST_RE.match(raw) else "para")
        if mode and kind != mode:
            push(line_no - 1)                   # 段落/列表/表格互相切换也断开
        if not buf:
            buf_start = line_no
            buf_kind = kind
        mode = kind
        buf.append(raw)

    push(line_no)
    return [(raws, start, end, kind) for raws, start, end, kind in blocks]


def _pack_section(
    lines: list[str],
    first_line: int,
    size: int,
    hard_max: int,
    min_chars: int,
) -> list[tuple[str, int, int]]:
    """把一节内的块累积成 ≤ size 的片段；超长块滑窗。"""
    blocks = _blocks(lines, first_line)
    pieces: list[tuple[str, int, int]] = []
    buf: list[str] = []
    buf_start = 0
    buf_end = 0

    def flush() -> None:
        nonlocal buf, buf_start, buf_end
        if buf:
            pieces.append(("\n".join(buf).strip("\n"), buf_start, buf_end))
        buf = []

    for raws, start, end, kind in blocks:
        block_text = "\n".join(raws).strip("\n")
        # 代码块 / 表格：整块带走，就算超上限也不切（切了就看不懂了）
        if kind in ("fence", "table"):
            flush()
            pieces.append((block_text, start, end))
            continue
        if len(block_text) > hard_max:
            flush()
            pieces.extend(_slide(block_text, start, size, hard_max))
            continue
        if buf and (sum(len(item) + 1 for item in buf) + len(block_text)) > size:
            flush()
        if not buf:
            buf_start = start
        buf.append(block_text)
        buf_end = end
    flush()

    return _merge_small(pieces, min_chars)


def _merge_small(
    pieces: list[tuple[str, int, int]], min_chars: int
) -> list[tuple[str, int, int]]:
    """碎片（< min_chars）并进下一块；最后一块并入上一块。"""
    merged: list[tuple[str, int, int]] = []
    for text, start, end in pieces:
        if merged and len(merged[-1][0]) < min_chars:
            prev_text, prev_start, _prev_end = merged.pop()
            text = f"{prev_text}\n{text}"
            start = prev_start
        merged.append((text, start, end))
    if len(merged) >= 2 and len(merged[-1][0]) < min_chars:
        last_text, last_start, last_end = merged.pop()
        prev_text, prev_start, _prev_end = merged.pop()
        merged.append((f"{prev_text}\n{last_text}", prev_start, last_end))
    return merged


# ---------------------------------------------------------------------------
# 第三级：超长块滑窗（按句子边界对齐）
# ---------------------------------------------------------------------------
def _sentences(text: str, first_line: int) -> list[tuple[str, int, int]]:
    """按句末标点/换行断句，并记每句的起止行号。"""
    out: list[tuple[str, int, int]] = []
    buf: list[str] = []
    line = first_line
    start_line = first_line
    for ch in text:
        buf.append(ch)
        if ch == "\n":
            line += 1
        if ch in SENT_END:
            out.append(("".join(buf), start_line, line))
            buf = []
            start_line = line
    if buf:
        out.append(("".join(buf), start_line, line))
    return out


def _slide(text: str, first_line: int, size: int, hard_max: int) -> list[tuple[str, int, int]]:
    """超长块 → 若干窗口；窗口之间按句子边界回退 `overlap` 个字。

    单个句子本身还超长（没有标点的长串）时，退化成按字符硬切。
    """
    overlap = max(0, min(DEFAULT_OVERLAP, size // 2))
    sentences = _sentences(text, first_line)
    if not sentences:
        return []

    out: list[tuple[str, int, int]] = []
    index = 0
    total = len(sentences)
    while index < total:
        sentence, s_line, e_line = sentences[index]
        if len(sentence) > hard_max:
            for piece_text, piece_start in _hard_split(sentence, size, overlap, s_line):
                out.append((piece_text.strip("\n"), piece_start, e_line))
            index += 1
            continue

        cursor = index
        length = 0
        while cursor < total and (length + len(sentences[cursor][0]) <= size or cursor == index):
            length += len(sentences[cursor][0])
            cursor += 1
        window = "".join(item[0] for item in sentences[index:cursor])
        out.append((window.strip("\n"), sentences[index][1], sentences[cursor - 1][2]))
        if cursor >= total:
            break

        # 下一窗口起点：从 cursor 往回退到「大致 overlap 字」的句子边界
        back = cursor
        shifted = 0
        while back - 1 > index and shifted + len(sentences[back - 1][0]) <= overlap:
            back -= 1
            shifted += len(sentences[back][0])
        index = back if back > index else cursor

    return out


def _hard_split(text: str, size: int, overlap: int, first_line: int) -> list[tuple[str, int]]:
    """完全没标点的长串：按字符窗口切，块间重叠 overlap 个字符。"""
    step = max(1, size - overlap)
    out: list[tuple[str, int]] = []
    for offset in range(0, len(text), step):
        piece = text[offset : offset + size]
        if not piece:
            break
        newlines = text[:offset].count("\n")
        out.append((piece, first_line + newlines))
        if offset + size >= len(text):
            break
    return out


# ---------------------------------------------------------------------------
# 前缀与去重
# ---------------------------------------------------------------------------
def _with_prefix(body: str, source: str, heading: str, start: int, end: int) -> str:
    title = heading or Path(source).stem
    where = f"L{start}" if start == end else f"L{start}-L{end}"
    return f"资料：{title}\n（来源：{source} {where}）\n\n{body.strip()}"


def _dedupe(chunks: list[Chunk]) -> list[Chunk]:
    seen: set[str] = set()
    out: list[Chunk] = []
    for chunk in chunks:
        if chunk.digest in seen:
            continue
        seen.add(chunk.digest)
        out.append(chunk)
    return out

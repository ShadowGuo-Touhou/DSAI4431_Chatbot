"""轻量 Markdown → Qt 富文本 HTML。

只用 `QLabel` 能显示的 HTML 子集，不引第三方依赖，也不影响流式追加。
覆盖范围（用户 2026-11-12 定）：

- 标题、粗体、斜体、删除线、行内代码
- 有序/无序/任务列表、引用、分隔线
- 表格、围栏代码块
- 链接（渲染成 <a>，能否点由 QLabel 设置决定）

**不处理数学公式**（`$...$` / `$$...$$` 原样显示），这是用户明确要求跳过的。
"""
from __future__ import annotations

import html
import re

# 代码块 ```lang ... ```（未闭合时吃到结尾，流式过程中也能看）
_FENCE = re.compile(r"```([\w+#.-]*)\n(.*?)(?:```|$)", re.S)
_HEADING = re.compile(r"^\s{0,3}(#{1,6})\s+(.*)$")
_HR = re.compile(r"^\s{0,3}(?:-{3,}|\*{3,}|_{3,})\s*$")
_TABLE_SEP = re.compile(r"^\s*\|?[\s:|-]+\|[\s:|-]*$")
_UL = re.compile(r"^\s{0,3}[-*+]\s+(.*)$")
_OL = re.compile(r"^\s{0,3}\d+[.)]\s+(.*)$")
_TASK = re.compile(r"^\s{0,3}[-*+]\s+\[([ xX])\]\s+(.*)$")
_QUOTE = re.compile(r"^\s{0,3}>\s?(.*)$")

_CODE_STYLE = "font-family:Consolas,'Courier New',monospace; color:#b5651d;"
# Qt 的富文本对 8 位十六进制（带 alpha）支持不稳，这里用纯色 + 左边框，明暗主题都能看清
_PRE_STYLE = (
    "font-family:Consolas,'Courier New',monospace; white-space:pre-wrap; "
    "border-left:3px solid #808080; padding:2px 0 2px 8px;"
)
_QUOTE_STYLE = "border-left:3px solid #808080; margin:2px 0; padding-left:8px; color:#808080;"
_TABLE_ATTRS = 'border="1" cellspacing="0" cellpadding="6"'


def to_html(text: str, *, max_chars: int = 60_000) -> str:
    """把 Markdown 转成 QLabel 能显示的 HTML。超长文本原样返回（不折腾）。"""
    raw = "" if text is None else str(text)
    if not raw.strip():
        return ""
    if len(raw) > max_chars:
        return html.escape(raw).replace("\n", "<br>")

    out: list[str] = []
    pos = 0
    for match in _FENCE.finditer(raw):
        if match.start() > pos:
            out.append(_blocks(raw[pos:match.start()]))
        lang = match.group(1).strip()
        code = html.escape(match.group(2).rstrip("\n"))
        label = (
            f'<span style="{_CODE_STYLE}"><b>{html.escape(lang)}</b></span><br>'
            if lang and lang.lower() not in ("text", "txt", "plain")
            else ""
        )
        out.append(f'<pre style="{_PRE_STYLE}">{label}{code}</pre>')
        pos = match.end()
    if pos < len(raw):
        out.append(_blocks(raw[pos:]))
    return "".join(out).strip()


# ---------------------------------------------------------------------------
# 块级
# ---------------------------------------------------------------------------
def _blocks(text: str) -> str:
    lines = text.split("\n")
    out: list[str] = []
    index = 0
    while index < len(lines):
        line = lines[index]

        if not line.strip():
            # 连续空行只留一个 <br>，否则段落之间会撑出两倍空白
            if not out or out[-1] != "<br>":
                out.append("<br>")
            index += 1
            continue

        # 表格：当前行有竖线，下一行是分隔行
        if "|" in line and index + 1 < len(lines) and _TABLE_SEP.match(lines[index + 1]):
            block, index = _table(lines, index)
            out.append(block)
            continue

        heading = _HEADING.match(line)
        if heading:
            level = len(heading.group(1))
            size = {1: 20, 2: 18, 3: 16}.get(level, 15)
            out.append(
                f'<p style="font-size:{size}px; margin:6px 0 2px 0;">'
                f"<b>{_inline(heading.group(2).strip())}</b></p>"
            )
            index += 1
            continue

        if _HR.match(line):
            out.append('<hr style="border:none; border-top:1px solid #88888855; margin:6px 0;">')
            index += 1
            continue

        # 引用（连续多行合成一段）
        if _QUOTE.match(line):
            chunk: list[str] = []
            while index < len(lines) and _QUOTE.match(lines[index]):
                chunk.append(_QUOTE.match(lines[index]).group(1))
                index += 1
            body = "<br>".join(_inline(item) for item in chunk)
            out.append(f'<div style="{_QUOTE_STYLE}">{body}</div>')
            continue

        # 列表（连续同类行）
        if _TASK.match(line) or _UL.match(line) or _OL.match(line):
            block, index = _list(lines, index)
            out.append(block)
            continue

        out.append(f"<p style='margin:2px 0;'>{_inline(line.strip())}</p>")
        index += 1
    return "".join(out)


def _list(lines: list[str], index: int) -> tuple[str, int]:
    ordered = bool(_OL.match(lines[index])) and not _UL.match(lines[index])
    tag = "ol" if ordered else "ul"
    items: list[str] = []
    tasks_only = True
    while index < len(lines):
        line = lines[index]
        task = _TASK.match(line)
        if task:
            mark = "☑" if task.group(1).lower() == "x" else "☐"
            items.append(f"<li>{mark} {_inline(task.group(2).strip())}</li>")
        elif _UL.match(line) and not ordered:
            tasks_only = False
            items.append(f"<li>{_inline(_UL.match(line).group(1).strip())}</li>")
        elif _OL.match(line) and ordered:
            tasks_only = False
            items.append(f"<li>{_inline(_OL.match(line).group(1).strip())}</li>")
        elif not line.strip():
            break
        else:
            # 列表项里的续行：接到上一项后面
            if items:
                items[-1] = items[-1][:-5] + " " + _inline(line.strip()) + "</li>"
            else:
                break
        index += 1
    inner = "".join(items)
    # 纯任务列表不要圆点（否则会出现「• ☑」这种双符号）
    # Qt 的列表默认缩进很大，这里把外边距收到最小
    style = "margin:2px 0 2px 2px;"
    if tasks_only and not ordered:
        style += " list-style-type:none;"
    return f'<{tag} style="{style}">{inner}</{tag}>', index


def _table(lines: list[str], index: int) -> tuple[str, int]:
    header = _cells(lines[index])
    index += 2                     # 跳过表头与分隔行
    body: list[list[str]] = []
    while index < len(lines) and "|" in lines[index] and lines[index].strip():
        body.append(_cells(lines[index]))
        index += 1
    head_html = "".join(
        f'<th align="left" style="padding:4px 8px;"><b>{_inline(cell)}</b></th>'
        for cell in header
    )
    rows = []
    for row in body:
        cells = "".join(
            f'<td style="padding:4px 8px;">{_inline(cell)}</td>' for cell in row
        )
        rows.append(f"<tr>{cells}</tr>")
    table = (
        f'<table {_TABLE_ATTRS} style="margin:4px 0; border-collapse:collapse;">'
        f"<tr>{head_html}</tr>{''.join(rows)}</table>"
    )
    return table, index


def _cells(line: str) -> list[str]:
    text = line.strip()
    if text.startswith("|"):
        text = text[1:]
    if text.endswith("|"):
        text = text[:-1]
    return [cell.strip() for cell in text.split("|")]


# ---------------------------------------------------------------------------
# 行内
# ---------------------------------------------------------------------------
_INLINE_CODE = re.compile(r"`([^`]+)`")
_BOLD = re.compile(r"\*\*(.+?)\*\*|__(.+?)__")
_ITALIC = re.compile(r"(?<!\*)\*([^*\n]+)\*(?!\*)|(?<!_)_([^_\n]+)_(?!_)")
_STRIKE = re.compile(r"~~(.+?)~~")
_LINK = re.compile(r"\[([^\]]+)\]\(([^)\s]+)\)")


def _inline(text: str) -> str:
    """行内规则。顺序很重要：先抠行内代码，别让它内部再被解析。"""
    codes: list[str] = []

    def stash(match: re.Match) -> str:
        codes.append(match.group(1))
        return f"\x00{len(codes) - 1}\x00"

    work = _INLINE_CODE.sub(stash, text)
    work = html.escape(work, quote=False)
    work = _LINK.sub(r'<a href="\2">\1</a>', work)
    work = _STRIKE.sub(r"<s>\1</s>", work)
    work = _BOLD.sub(lambda m: f"<b>{m.group(1) or m.group(2)}</b>", work)
    work = _ITALIC.sub(lambda m: f"<i>{m.group(1) or m.group(2)}</i>", work)
    for offset, code in enumerate(codes):
        work = work.replace(
            f"\x00{offset}\x00",
            f'<code style="{_CODE_STYLE}">{html.escape(code, quote=False)}</code>',
        )
    return work

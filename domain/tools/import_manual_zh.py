"""把 `other info/` 里玩家整理的中文资料转成 markdown，放进 `domain/kb/manual_zh/`。

这些是社群资料、不是官方 wiki：标题里会标明来源与"非官方"，build_official.py 会把它们
以 `zh/` 前缀并入知识库（中文原文保持中文，不做翻译）。

依赖 python-docx / pypdf —— 用装了它们的 Python 3.10 跑：
    python domain/tools/import_manual_zh.py
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

import docx
import pypdf

ROOT = Path(__file__).resolve().parents[1]           # domain/
SRC = ROOT.parent / "other info"
OUT = ROOT / "kb" / "manual_zh"

NOTE = "来源：玩家整理（中文，非官方，可能早于游戏 0.6.2.6）"


def _table_md(table) -> str:
    rows = []
    for row in table.rows:
        cells = [c.text.strip().replace("\n", " ").replace("|", "/") for c in row.cells]
        rows.append(cells)
    if not rows:
        return ""
    width = max(len(r) for r in rows)
    rows = [r + [""] * (width - len(r)) for r in rows]
    lines = ["| " + " | ".join(rows[0]) + " |", "|" + "---|" * width]
    lines += ["| " + " | ".join(r) + " |" for r in rows[1:]]
    return "\n".join(lines)


def docx_to_md(path: Path, title: str) -> str:
    doc = docx.Document(str(path))
    parts: list[str] = [f"# {title}", "", NOTE, ""]
    tables = list(doc.tables)
    for para in doc.paragraphs:
        text = para.text.strip()
        if not text:
            continue
        style = (para.style.name or "").lower()
        if style.startswith("heading") or style.startswith("标题"):
            level = re.sub(r"\D", "", style) or "2"
            level = min(max(int(level), 2), 4)
            parts.append(f"{'#' * level} {text}")
        else:
            parts.append(text)
    for idx, table in enumerate(tables, start=1):
        md = _table_md(table)
        if md:
            parts += ["", f"## 表 {idx}", "", md]
    return "\n\n".join(parts) + "\n"


def pdf_to_md(path: Path, title: str) -> str:
    reader = pypdf.PdfReader(str(path))
    body: list[str] = []
    for page in reader.pages:
        text = (page.extract_text() or "").replace("\r", "")
        for raw in text.splitlines():
            line = raw.strip()
            if not line:
                continue
            if re.fullmatch(r"\d{1,2}", line):        # 页码
                continue
            if re.fullmatch(r"[.·…\s]{6,}", line):    # 目录点线
                continue
            body.append(line)
    text = "\n".join(body)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return f"# {title}\n\n{NOTE}\n\n{text}\n"


def main() -> int:
    OUT.mkdir(parents=True, exist_ok=True)
    jobs = [
        ("优势交战距离.docx", "交战距离及其推导", docx_to_md),
        ("软杀原理与软杀教学_重排版_v6.docx", "软杀原理与软杀教学", docx_to_md),
        ("新手常用知识整合包.pdf", "新手常用知识整合包", pdf_to_md),
    ]
    for name, title, convert in jobs:
        path = SRC / name
        if not path.is_file():
            print(f"missing: {path}")
            continue
        text = convert(path, title)
        target = OUT / (path.stem + ".md")
        target.write_text(text, encoding="utf-8")
        print(f"{name} -> {target.name}  {len(text)} chars")
    return 0


if __name__ == "__main__":
    sys.exit(main())

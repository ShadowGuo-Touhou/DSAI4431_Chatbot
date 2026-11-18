"""用项目自己的 chunker 预检 KB：切块数量、长度分布、样例。

用法：python domain/tools/check_chunks.py [--size 480] [--overlap 64] [--show 2]
"""

from __future__ import annotations

import argparse
import collections
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]          # domain/
DOCS = ROOT / "kb" / "docs"
REPO = ROOT.parent          # <repo>
sys.path.insert(0, str(REPO / "src"))

from dsai4431_chatbot.core.rag.chunker import (  # noqa: E402
    DEFAULT_OVERLAP,
    DEFAULT_SIZE,
    HARD_MAX,
    split_document,
)

BUCKETS = [(0, 200), (200, 400), (400, 500), (500, 700), (700, 10_000)]


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--size", type=int, default=DEFAULT_SIZE)
    parser.add_argument("--overlap", type=int, default=DEFAULT_OVERLAP)
    parser.add_argument("--show", type=int, default=2, help="打印几段样例全文")
    args = parser.parse_args(argv)

    files = sorted(DOCS.rglob("*.md"))
    if not files:
        print("docs 还是空的，先跑 build_kb.py")
        return 1

    chunks = []
    for path in files:
        rel = path.relative_to(DOCS).as_posix()
        text = path.read_text(encoding="utf-8")
        chunks.extend(split_document(rel, text, size=args.size, overlap=args.overlap))

    lengths = [len(chunk.text) for chunk in chunks]
    hist = collections.Counter()
    for length in lengths:
        for low, high in BUCKETS:
            if low <= length < high:
                hist[f"{low}-{high if high < 10_000 else '+'}"] += 1
                break

    print(f"文档 {len(files)} 份 → 块 {len(chunks)} 个（size={args.size} overlap={args.overlap} hard_max={HARD_MAX}）")
    print(f"长度 平均 {sum(lengths)/len(lengths):.0f}｜最长 {max(lengths)}｜超过 hard_max 的 {sum(1 for l in lengths if l > HARD_MAX)} 个")
    print("分布：" + "，".join(f"{name}:{count}" for name, count in sorted(hist.items())))
    print(f"不同 heading 数：{len({c.heading for c in chunks})}｜不同 source：{len({c.source for c in chunks})}")

    longest = sorted(chunks, key=lambda c: -len(c.text))[:5]
    print("\n最长的 5 块：")
    for chunk in longest:
        print(f"  {len(chunk.text):5d} 字  {chunk.source}  [{chunk.heading}] L{chunk.start_line}-{chunk.end_line}")

    for index, chunk in enumerate(longest[: args.show], start=1):
        print(f"\n----- 样例 {index}（{len(chunk.text)} 字）-----")
        print(chunk.text[:900])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

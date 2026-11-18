"""体检：官方 wiki 每页/每节的表格行数 vs 真正生成的知识库文档数。

回答「是不是只有舱室漏了」：对 Components / Ships / Munitions / Spacecraft 等页面的
每一张表，看行数、抽出实体数、以及整张表被跳过的情况。

    python domain/tools/audit_kb.py               # 汇总
    python domain/tools/audit_kb.py --tables      # 逐表明细
    python domain/tools/audit_kb.py --missing     # 列出缺失的实体文档
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "kb" / "raw_official"
DOCS = ROOT / "kb" / "docs"

# 这些表不是实体表（控件说明、数值对照），被跳过是正常的
NON_ENTITY_HINTS = (
    "controls", "guidelines", "stance", "commands", "detection ranges", "signature",
    "cross-section", "countermeasure", "chaff cloud", "when craft", "loadouts",
    "ammo selection", "hit probability", "damage", "penetration", "armor",
)


def slugify(name: str) -> str:
    slug = re.sub(r"[^0-9a-z]+", "-", name.strip().lower())
    return re.sub(r"-{2,}", "-", slug).strip("-")[:80]


def main() -> int:
    show_tables = "--tables" in sys.argv
    show_missing = "--missing" in sys.argv
    total_rows = total_used = 0
    skipped: list[tuple[str, dict]] = []
    missing: list[str] = []
    for path in sorted(RAW.rglob("*.json")):
        rec = json.loads(path.read_text(encoding="utf-8"))
        cat = rec["category"]
        title = rec["title"]
        tables = rec.get("tables") or []
        used = [t for t in tables if t["used"]]
        ent = rec.get("entities") or []
        if tables and show_tables:
            print(f"== {title} ({cat})  entities={len(ent)}")
            for t in tables:
                mark = "" if t["used"] == t["rows"] else f"   (skip {t['rows'] - t['used']})"
                print(f"   {t['used']:3d}/{t['rows']:3d}  {t['header'][:20]:20} {t['section'][:64]}{mark}")
        total_rows += sum(t["rows"] for t in used)
        total_used += sum(t["used"] for t in used)
        for t in tables:
            if t["used"]:
                continue
            section = t["section"].lower()
            if any(h in section for h in NON_ENTITY_HINTS):
                continue
            if t["rows"] >= 3:
                skipped.append((title, t))
        for e in ent:
            if not (DOCS / cat / f"{slugify(e['name'])}.md").is_file():
                missing.append(f"{cat}/{slugify(e['name'])}.md  ({title} › {e['section']})")

    print(f"\nentity tables: rows={total_rows} entities_used={total_used}")
    if skipped:
        print(f"\npossible missed tables: {len(skipped)}")
        for title, t in skipped:
            print(f"  - {title} › {t['section']}  header={t['header']!r} rows={t['rows']}")
    if missing:
        print(f"\nmissing entity docs: {len(missing)}")
        if show_missing:
            for line in missing:
                print("  -", line)
    else:
        print("no missing entity docs")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

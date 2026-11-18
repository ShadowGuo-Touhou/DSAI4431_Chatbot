"""Write one reviewable overview of every hull's socket layout, plus an editable CSV.

The layout tables live inside the socket docs (`domain/kb/docs/sockets/*.md`), one
page per hull — fine for the chatbot, awkward for a human who wants to read all of
them at once and mark the rows that look wrong.

This script produces two files:

* ``domain/reports/socket-layouts-overview.md`` — everything on one page, grouped by
  hull, with fill rate, the observed go-to part, alternatives and the suggested
  part type for every socket.
* ``domain/data/layout_review.csv`` — the same rows, with two blank columns at the
  end: ``corrected_part`` and ``note``.  Fill them in, run ``--apply``, and the
  corrections are written to ``domain/data/layout_corrections.json`` (which the doc
  builders read, marking corrected rows with ✎).

Usage::

    .venv\\Scripts\\python.exe domain\\tools\\build_layout_overview.py
    .venv\\Scripts\\python.exe domain\\tools\\build_layout_overview.py --apply
"""

from __future__ import annotations

import argparse
import csv
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "domain" / "tools"))

import build_layouts as bl  # noqa: E402  (shares _label and the fixture paths)
import build_family_layouts as bf  # noqa: E402

DATA = ROOT / "domain" / "data"
REPORT = ROOT / "domain" / "reports" / "socket-layouts-overview.md"
CSV_PATH = DATA / "layout_review.csv"
KB_DOC = ROOT / "domain" / "kb" / "manual_zh" / "槽位配置总表.md"
CORR_PATH = DATA / "layout_corrections.json"

FIELDS = [
    "hull", "socket", "size", "fill_pct", "pair", "top_part", "top_n",
    "alternatives", "suggestion", "corrected_part", "note",
]


def load_corrections() -> dict:
    if CORR_PATH.exists():
        return json.loads(CORR_PATH.read_text(encoding="utf-8-sig"))
    return {}


def rows_for(hull: str, data: dict, comps: dict) -> list[dict]:
    out = []
    for short, e in data["sockets"].items():
        top = e["top"]
        specific = [tag for tag, _ in e["fit_tags"] if tag not in {"舱室", "通用模块", "船体自带"}]
        out.append(
            {
                "hull": hull,
                "socket": short,
                "size": "×".join(str(x) for x in e["size"]),
                "fill_pct": int(e["fill_rate"] * 100),
                "pair": e.get("pair") or "",
                "top_part": top[0]["part"] if top else "",
                "top_n": top[0]["n"] if top else 0,
                "alternatives": "、".join(t["part"] for t in top[1:4]),
                "suggestion": "、".join(specific[:4] or [tag for tag, _ in e["fit_tags"][:3]]),
            }
        )
    return out


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true", help="read the edited CSV back into layout_corrections.json")
    args = ap.parse_args()

    if args.apply:
        if not CSV_PATH.exists():
            print("no layout_review.csv yet — run without --apply first")
            return 1
        corrections: dict[str, dict] = {}
        with CSV_PATH.open(encoding="utf-8-sig", newline="") as fh:
            for row in csv.DictReader(fh):
                part = (row.get("corrected_part") or "").strip()
                note = (row.get("note") or "").strip()
                if not part and not note:
                    continue
                corrections.setdefault(row["hull"], {})[row["socket"]] = {
                    "part": part or None,
                    "note": note or None,
                }
        CORR_PATH.write_text(json.dumps(corrections, ensure_ascii=False, indent=2), encoding="utf-8")
        total = sum(len(v) for v in corrections.values())
        print(f"wrote {CORR_PATH.relative_to(ROOT)} ({total} corrected rows over {len(corrections)} hulls)")
        print("now rerun: build_layouts.py --docs / build_family_layouts.py --docs, then build_official.py + index_kb.py")
        return 0

    layouts = json.loads((DATA / "hull_layouts.json").read_text(encoding="utf-8"))
    comps = {c.name: c for c in bl.fl.WikiIndex().components}
    corrections = load_corrections()

    blocks: list[dict] = []
    for hull, data in layouts.items():
        if data.get("modular") or " - " in hull:
            continue
        blocks.append({"hull": hull, "data": data, "rows": rows_for(hull, data, comps)})

    # modular families, merged the same way the socket pages do it
    for stem, sections in bf.families().items():
        merged = bf.merged(sections, layouts, comps)
        if merged["sockets"]:
            blocks.append({"hull": stem, "data": merged, "rows": rows_for(stem, merged, comps)})

    blocks.sort(key=lambda b: b["hull"])
    total_sockets = sum(len(b["rows"]) for b in blocks)

    lines = [
        "# 槽位布局总览（所有船体一页看完）",
        "",
        f"生成自 `domain/data/hull_layouts.json`（{len(blocks)} 个船体 / {total_sockets} 个槽位 / "
        "461 艘样本舰）。想改哪行，就去改 `domain/data/layout_review.csv` 的 "
        "`corrected_part` / `note` 两列，然后 `--apply`。",
        "",
        "读法：`填充率` = 样本里装了这一格的比例；`常用部件 ×n` = 样本里真实出现的首选部件和艘次；"
        "`建议` = 从尺寸/类型推出的可选定位；`配对` = 左右镜像的另一格（建议两边同款，不是强制）。",
        "",
    ]
    for block in blocks:
        data, rows = block["data"], block["rows"]
        pairs = "、".join(f"{a}↔{b}" for a, b in data["pairs"]) or "无"
        lines += [
            f"## {block['hull']}（{data['ships']} 艘样本）",
            "",
            f"配对槽位：{pairs}",
            "",
            "| 槽位 | 尺寸 | 填充率 | 配对 | 常用部件 | 备选 | 建议 | 校正 |",
            "|---|---|---:|---|---|---|---|---|",
        ]
        for row in rows:
            corr = corrections.get(row["hull"], {}).get(row["socket"], {})
            mark = ""
            if corr.get("part"):
                mark = f"✎ {corr['part']}"
            if corr.get("note"):
                mark += ("；" if mark else "✎ ") + corr["note"]
            top = f"{row['top_part']} ×{row['top_n']}" if row["top_part"] else "—"
            lines.append(
                f"| {row['socket']} | {row['size']} | {row['fill_pct']}% | {row['pair'] or '—'} | "
                f"{top} | {row['alternatives'] or '—'} | {row['suggestion'] or '—'} | {mark or '—'} |"
            )
        lines.append("")

    REPORT.write_text("\n".join(lines), encoding="utf-8")
    print(f"report: {REPORT.relative_to(ROOT)} ({len(blocks)} hulls / {total_sockets} sockets)")

    # the same tables as a knowledge-base page, so the bot can read them too
    doc = [
        "# 槽位配置总表（按船体）",
        "",
        "这张表按**船体**列出每个槽位在真实存档里通常装什么，用来代替「凭手感配船」。",
        "`填充率` 是样本里装了这一格的比例：>90% 是骨架槽位，别留空；<40% 通常是可选项。",
        "`常用部件（艘次）` 是样本里真实出现的前几名，配船时优先照抄；`备选` 是同槽位出现过的其它部件。",
        "`配对` 是左右镜像的另一个槽位，**建议两边装同款**（这是鼓励，不是规则）。",
        "",
        f"共 {len(blocks)} 个船体 / {total_sockets} 个槽位，来自真实存档样本。要人工改某一格："
        "编辑 `domain/data/layout_review.csv` 的 `corrected_part` / `note`，再运行 "
        "`python domain/tools/build_layout_overview.py --apply` 与 `build_layouts.py --docs`。",
        "",
    ]
    for block in blocks:
        data, rows = block["data"], block["rows"]
        pairs = "、".join(f"{a}↔{b}" for a, b in data["pairs"]) or "无"
        doc += [
            f"## {block['hull']}（{data['ships']} 艘样本）",
            "",
            f"配对槽位：{pairs}",
            "",
            "| 槽位 | 尺寸 | 填充率 | 配对 | 常用部件（艘次） | 备选 | 适合装 |",
            "|---|---|---:|---|---|---|---|",
        ]
        for row in rows:
            top = f"{row['top_part']}（×{row['top_n']}）" if row["top_part"] else "—"
            doc.append(
                f"| {row['socket']} | {row['size']} | {row['fill_pct']}% | {row['pair'] or '—'} | "
                f"{top} | {row['alternatives'] or '—'} | {row['suggestion'] or '—'} |"
            )
        doc.append("")
    KB_DOC.write_text("\n".join(doc), encoding="utf-8")
    print(f"kb:     {KB_DOC.relative_to(ROOT)}")

    with CSV_PATH.open("w", encoding="utf-8-sig", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=FIELDS)
        writer.writeheader()
        for block in blocks:
            for row in block["rows"]:
                corr = corrections.get(row["hull"], {}).get(row["socket"], {})
                row = dict(row, corrected_part=corr.get("part") or "", note=corr.get("note") or "")
                writer.writerow(row)
    print(f"csv:    {CSV_PATH.relative_to(ROOT)} ({total_sockets} rows)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

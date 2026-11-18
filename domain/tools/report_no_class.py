"""List every ship the classifier could not place in any class.

Output: domain/reports/no-class-ships.md  (Markdown, grouped by hull)
"""

from __future__ import annotations

import json
import pathlib
from collections import Counter, defaultdict

ROOT = pathlib.Path(Path(__file__).resolve().parents[2])
SRC = ROOT / "domain" / "data" / "ship_classification.json"
OUT = ROOT / "domain" / "reports" / "no-class-ships.md"


def short_fails(fails: list[str], limit: int = 4) -> str:
    if not fails:
        return "—"
    txt = "；".join(fails[:limit])
    if len(fails) > limit:
        txt += f" …(+{len(fails) - limit})"
    return txt


def weapons(r: dict) -> str:
    bits = []
    for name, n in (r.get("calibers") or {}).items():
        bits.append(f"{n}×{name}")
    for name, n in (r.get("launchers") or {}).items():
        bits.append(f"{n}×{name.split(' ')[0]}")
    return ", ".join(bits) or "—"


def main() -> int:
    data = json.loads(SRC.read_text(encoding="utf-8"))
    rows = data["rows"]
    nc = [r for r in rows if r["verdict"] == "no_class"]
    bc = [r for r in rows if r["verdict"] == "bad_class"]

    by_hull: dict[str, list[dict]] = defaultdict(list)
    for r in nc:
        by_hull[r["hull_abbr"] or "?"].append(r)

    lines = ["# 未归类舰船清单（no_class）", ""]
    lines += [
        f"语料：**{len(rows)}** 艘舰 / 判定口径为 `Ship Builds.txt` 的 must 条件；",
        f"本表收录 **{len(nc)}** 艘「哪个舰级都对不上」的舰（另有 `bad_class` {len(bc)} 艘，"
        "它们只符合 bad 舰级，单列在文末）。",
        "",
        "列说明：`closest` = 最接近的舰级（差的 must 条件最少）；`差的 must` = 它缺哪几条硬性要求。",
        "",
    ]

    # 汇总结论
    lines += ["## 一览", "", "| 舰体 | 艘数 | 点数范围 | 最常见的缺口 |", "| --- | ---: | --- | --- |"]
    for hull, rs in sorted(by_hull.items(), key=lambda kv: -len(kv[1])):
        costs = [r["cost"] for r in rs]
        fails = Counter()
        for r in rs:
            q = r["class_quality"].get(r.get("closest") or "", {})
            for f in q.get("fails", []):
                fails[f] += 1
        top = "；".join(f"{k} ×{v}" for k, v in fails.most_common(2)) or "—"
        lines.append(f"| {hull} | {len(rs)} | {min(costs):.0f}–{max(costs):.0f} | {top} |")
    lines.append("")

    for hull, rs in sorted(by_hull.items(), key=lambda kv: -len(kv[1])):
        lines += [f"## {hull}（{len(rs)} 艘）", ""]
        lines += [
            "| 舰队 | 舰名 | 点数 | 武器 | 最接近 | 它差的 must |",
            "| --- | --- | ---: | --- | --- | --- |",
        ]
        for r in sorted(rs, key=lambda x: (x["closest"] or "", x["fleet"], x["ship"])):
            q = r["class_quality"].get(r.get("closest") or "", {})
            lines.append(
                f"| {r['fleet']} | {r['ship']} | {r['cost']:.0f} | {weapons(r)} | "
                f"{r.get('closest') or '—'} | {short_fails(q.get('fails', []))} |"
            )
        lines.append("")

    if bc:
        lines += ["## 附：bad_class（只符合 bad 舰级）", ""]
        lines += ["| 舰队 | 舰名 | 舰体 | 点数 | 舰级 |", "| --- | --- | --- | ---: | --- |"]
        for r in sorted(bc, key=lambda x: (x["class"], x["fleet"])):
            lines.append(f"| {r['fleet']} | {r['ship']} | {r['hull_abbr']} | {r['cost']:.0f} | {r['class']} |")
        lines.append("")

    OUT.write_text("\n".join(lines), encoding="utf-8")
    print(f"wrote {OUT}  no_class={len(nc)}  bad_class={len(bc)}")
    for hull, rs in sorted(by_hull.items(), key=lambda kv: -len(kv[1])):
        print(f"  {hull:4} {len(rs):3}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

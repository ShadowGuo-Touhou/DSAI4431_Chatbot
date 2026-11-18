"""Write the compact「部件速查」page from parts_facets.csv.

The CSV is the machine-readable source; the bot can only read markdown chunks, so
this projects the same numbers into one table per kind:

    部件 | 尺寸(格) | 点数 | 供电(kW) | 关键数值

Usage::

    .venv\\Scripts\\python.exe domain\\tools\\build_facets.py
"""

from __future__ import annotations

import csv
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
CSV = ROOT / "domain" / "data" / "parts_facets.csv"
OUT = ROOT / "domain" / "kb" / "manual_zh" / "部件速查（尺寸 点数 供电 射速）.md"

TITLES = {
    "Surface": "挂载（武器 / 传感器 / 发射器）",
    "Compartment": "舱室",
    "Module": "模块",
}


def fmt_num(text: str) -> str:
    try:
        value = float(text)
    except (TypeError, ValueError):
        return text or ""
    return f"{value:g}"


def fmt_power(text: str) -> str:
    try:
        value = float(text)
    except (TypeError, ValueError):
        return ""
    if not value:
        return ""
    return f"+{value:g}" if value > 0 else f"{value:g}"


def key_numbers(row: dict) -> str:
    bits = []
    if row["rpm"]:
        bits.append(f"{row['barrels']} 管 / {row['reload_s']} s → {row['rpm']} 发/分")
    if row["ammo"]:
        bits.append(row["ammo"].replace("Ballistic/Chemical - ", "").replace("Ballistic/Magnetic - ", ""))
    if row["cells_launcher"]:
        bits.append(f"cell 容量 {row['cells_launcher']}")
    if row["storage_m3"]:
        bits.append(f"弹库 {row['storage_m3']}")
    if not bits and row["faction"]:
        bits.append("")
    return "；".join(b for b in bits if b)


def main() -> int:
    rows = list(csv.DictReader(CSV.open(encoding="utf-8-sig")))
    by_kind: dict[str, list[dict]] = {}
    for row in rows:
        by_kind.setdefault(row["kind"], []).append(row)

    lines = [
        "# 部件速查（尺寸 / 点数 / 供电 / 射速）",
        "",
        "Tags: kind=reference; topic=part facets, 部件速查, 尺寸, 点数, 供电, 射速, 装得下",
        "Keywords: 部件速查, 尺寸速查, parts facets table, 速查表, 全表, 部件数据, 尺寸, "
        "点数, 价格, 供电, 功率, 射速, 装得下吗, 哪个部件, "
        "parts list, 挂载, 舱室, 模块, 全表",
        "Summary: 全部可装部件的一张速查表：尺寸（格）、点数、供电（kW）、关键数值（口径/管数/装填/射速、cell 数、弹库容量）。",
        "",
        "用途：**回答「这个部件多大、多少点、多少电、打多快」以及「这块槽位装不装得下」**。",
        "尺寸是 0.25 m 为一格的格数，`6x3x6` 表示长宽高各 6/3/6 格（1.5 m × 0.75 m × 1.5 m）；"
        "装不装得下看三个轴都不超过槽位即可（允许旋转的对齐方式见 `sockets/<hull>.md`）。",
        "",
        "> 机读版本：`domain/data/parts_facets.csv`（所有字段），"
        "本页是它的可检索投影；槽位→可装部件清单见 `domain/data/socket_fit.json`。",
        "",
    ]
    for kind, title in TITLES.items():
        group = sorted(by_kind.get(kind, []), key=lambda r: (r["section"], -float(r["cost"] or 0)))
        if not group:
            continue
        lines += [f"## {title}（{len(group)} 件）", "",
                  "| 部件 | 尺寸(格) | 点数 | 供电(kW) | 关键数值 | 阵营 |",
                  "|---|---|---:|---:|---|---|"]
        for row in group:
            faction = row["faction"].replace("Shelter Alliance (SA)", "SA").replace(
                "Outlying Systems Protectorate (OSP)", "OSP"
            )
            lines.append(
                f"| {row['name']} | {row['dims']} | {fmt_num(row['cost'])} | {fmt_power(row['power_kw'])} "
                f"| {key_numbers(row)} | {faction or 'both'} |"
            )
        lines.append("")
    OUT.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"wrote {OUT.relative_to(ROOT)} ({len(rows)} parts)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

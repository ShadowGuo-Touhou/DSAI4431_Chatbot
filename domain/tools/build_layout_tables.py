"""Write the 槽位配置总表 page: one table per hull *group*, merged and ordered.

The raw data (`domain/data/hull_layouts.json`) is one table per socket, per hull
part.  That is the right shape for the machine but the wrong shape for a player:

* the section hulls (LN / CLN / CVLN) all use the same compartments, so the LN and
  Moorline tables were 90 % identical;
* the A/B/C parts of a section are the same sockets, so their rows are
  duplicates;
* which `MODn` socket holds which module is mostly irrelevant (only the size
  matters), so the module rows are pooled per size;
* the rows came out ordered by fill rate, not by socket name.

This script folds all of that: hull groups, one row per mount / compartment, one
row per module size, ordered MT → CT → CMP → MOD.

Usage::

    .venv\\Scripts\\python.exe domain\\tools\\build_layout_tables.py
"""

from __future__ import annotations

import csv
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "domain" / "tools"))

import build_layouts as bl  # noqa: E402
import build_family_layouts as bf  # noqa: E402

DATA = ROOT / "domain" / "data"
KB_DOC = ROOT / "domain" / "kb" / "manual_zh" / "槽位配置总表.md"
REPORT = ROOT / "domain" / "reports" / "socket-layouts-overview.md"
CSV_PATH = DATA / "layout_review.csv"

# hull group -> (display name, [section hull keys in hull_layouts.json])
#
# The save file only knows the *base* hull (``Stock/Bulk Hauler`` …); the clipper
# prefabs carry different names entirely.  Mapping verified against the wiki slot
# counts: Flathead Monitor 6 mounts / 6 compartments / 7 modules = 19 sockets =
# ``Bulk Clipper``; Ferryman 3/3/4 = ``Shuttle Clipper``; Draugr 5/5/4 = ``Tug Clipper``.
GROUPS = [
    ("LN 线列舰（Marauder）", ["Bulk - Bow", "Bulk - Core", "Bulk - Stern"]),
    ("MN 监视舰（Flathead）", ["Bulk Clipper"]),
    ("CLN 集装箱班轮（Moorline）/ CVLN（Container Hauler Refit）",
     ["Container - Bow", "Container - Core", "Container - Stern"]),
    ("CVL 轻型航母（Journeyman / Ore Carrier）", ["Ore Carrier"]),
]

SOCKET_ORDER = {"MT": 0, "CT": 1, "CMP": 2, "MOD": 3}

# the clipper prefabs are named after the hull shape, the game calls the classes
# differently; keep both so a player can find either name
DISPLAY = {
    "Shuttle Clipper": "Ferryman Clipper（Shuttle Clipper）",
    "Tug Clipper": "Draugr Clipper（Tug Clipper）",
}

FIELDS = [
    "hull", "socket", "size", "fill_pct", "pair", "top_part", "top_n",
    "alternatives", "suggestion", "corrected_part", "note",
]


def socket_key(name: str) -> tuple:
    m = re.match(r"([A-Za-z]+)\s*(\d+)", name)
    if m:
        return (SOCKET_ORDER.get(m.group(1).upper(), 9), int(m.group(2)), name)
    return (9, 0, name)


def size_tuple(text: str) -> tuple[int, ...]:
    try:
        return tuple(int(x) for x in text.split("×"))
    except ValueError:
        return (0, 0, 0)


def load_rows(hull: str, data: dict) -> list[dict]:
    seg = data.get("canonical") or (hull if " - " in hull else "")
    out = []
    for short, e in data["sockets"].items():
        out.append(
            {
                "hull": hull,
                "seg": seg,
                "socket": short,
                "size": "×".join(str(x) for x in e["size"]),
                "type": e.get("type", ""),
                "filled": e.get("filled", 0),
                "ships": data["ships"],
                "parts": {t["part"]: t["n"] for t in e.get("top", [])},
                "pair": e.get("pair") or "",
            }
        )
    return out


def merge_rows(rows: list[dict]) -> list[dict]:
    """Pool rows with the same segment + socket name, then one row per module size.

    不同分段的同名槽不是同一个位置（`Bulk - Bow` 的 `MT1` 与 `Bulk - Core` 的 `MT1`
    在船上是两门炮），所以按「段 + 槽位」做键；只有模块槽按尺寸合并，因为
    2×2×2 / 3×3×3 的模块放置顺序不影响结果。
    """
    by_key: dict[tuple, dict] = {}
    for row in rows:
        key = (row["socket"],) if row["socket"].startswith("MOD") else (row["seg"], row["socket"])
        cur = by_key.get(key)
        if cur is None:
            cur = dict(row, parts=dict(row["parts"]), pairs={row["pair"]} if row["pair"] else set())
            by_key[key] = cur
            continue
        if size_tuple(row["size"]) > size_tuple(cur["size"]):
            cur["size"] = row["size"]
        cur["filled"] += row["filled"]
        cur["ships"] += row["ships"]
        cur["pairs"].add(row["pair"]) if row["pair"] else None
        for part, n in row["parts"].items():
            cur["parts"][part] = cur["parts"].get(part, 0) + n

    # modules keep their own row: MOD1 and MOD2 are separate slots, only the size
    # decides what fits.  When a pooled family gives the same MODn two sizes the
    # size is appended so the rows stay distinguishable.
    sizes: dict[str, set[str]] = {}
    for key, row in by_key.items():
        if key[0].startswith("MOD"):
            sizes.setdefault(key[0], set()).add(row["size"])

    merged: list[dict] = []
    for key, row in by_key.items():
        if key[0].startswith("MOD") and len(sizes[key[0]]) > 1:
            row = {**row, "socket": f"{key[0]}（{row['size']}）"}
        if len(row.get("pairs", ())) != 1 and not key[0].startswith("MOD"):
            row["pair"] = ""
        merged.append(row)

    for row in merged:
        row.setdefault("sort", (seg_key(row["seg"]), socket_key(row["socket"])))
    merged.sort(key=lambda r: r["sort"])
    return merged


SEG_ORDER: list[str] = []


def seg_key(seg: str) -> int:
    try:
        return SEG_ORDER.index(seg)
    except ValueError:
        return len(SEG_ORDER)


def cells(row: dict) -> tuple[str, str]:
    # a weighted sample can round a rare part down to 0 — do not print "×0"
    items = [(k, v) for k, v in sorted(row["parts"].items(), key=lambda kv: -kv[1]) if v >= 0.5]
    top = items[0] if items else None
    main = f"{top[0]}（×{top[1]}）" if top else "—"
    alt = "、".join(f"{name}（×{n}）" for name, n in items[1:4]) or "—"
    return main, alt


def render_block(name: str, group: list[dict], sample_n: int, raw_n: int = 0) -> list[str]:
    count = f"{sample_n} 有效样本 / {raw_n} 艘原始" if raw_n else f"{sample_n} 艘样本"
    rows = merge_rows(group)
    multi = len({r["seg"] for r in rows if r["seg"]}) > 1
    head = "| 段 | 槽位 | 尺寸 | 填充率 | 配对 | 常用部件（艘次） | 备选 |" if multi else \
        "| 槽位 | 尺寸 | 填充率 | 配对 | 常用部件（艘次） | 备选 |"
    rule = "|---|---|---|---:|---|---|---|" if multi else "|---|---|---:|---|---|---|"
    lines = [
        f"## {name}（{count}）",
        "",
        head,
        rule,
    ]
    for row in rows:
        pct = int(round(100 * row["filled"] / row["ships"])) if row["ships"] else 0
        main, alt = cells(row)
        lead = f"| {row['seg']} | " if multi else "| "
        lines.append(
            f"{lead}{row['socket']} | {row['size']} | {pct}% | {row['pair'] or '—'} | {main} | {alt} |"
        )
    lines.append("")
    return lines


def main() -> int:
    layouts = json.loads((DATA / "hull_layouts.json").read_text(encoding="utf-8"))
    comps = {c.name: c for c in bl.fl.WikiIndex().components}

    # ---- CSV first: the raw per-socket rows are what a human edits
    corrections = json.loads((DATA / "layout_corrections.json").read_text(encoding="utf-8-sig")) \
        if (DATA / "layout_corrections.json").exists() else {}
    with CSV_PATH.open("w", encoding="utf-8-sig", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=FIELDS)
        writer.writeheader()
        for hull, data in layouts.items():
            if data.get("modular"):
                continue
            for row in load_rows(hull, data):
                corr = corrections.get(hull, {}).get(row["socket"], {})
                writer.writerow({
                    "hull": hull,
                    "socket": row["socket"],
                    "size": row["size"],
                    "fill_pct": int(round(100 * row["filled"] / row["ships"])) if row["ships"] else 0,
                    "pair": row["pair"],
                    "top_part": max(row["parts"], key=row["parts"].get) if row["parts"] else "",
                    "top_n": max(row["parts"].values()) if row["parts"] else 0,
                    "alternatives": "、".join(sorted(row["parts"], key=row["parts"].get, reverse=True)[1:4]),
                    "suggestion": "",
                    "corrected_part": corr.get("part") or "",
                    "note": corr.get("note") or "",
                })

    # ---- build the grouped tables
    blocks: list[tuple[str, list[dict], int, int]] = []
    SEG_ORDER.clear()
    SEG_ORDER.extend(section for _, sections in GROUPS for section in sections)

    grouped_sections: set[str] = set()
    for display, sections in GROUPS:
        rows: list[dict] = []
        sample_n = 0
        raw_n = 0
        for section in sections:
            data = layouts.get(section)
            if not data or not data["sockets"]:
                continue
            grouped_sections.add(section)
            rows.extend(load_rows(section, data))
            sample_n = max(sample_n, data["ships"])
            raw_n = max(raw_n, data.get("ships_raw", 0))
        if rows:
            blocks.append((display, rows, sample_n, raw_n))

    for hull, data in sorted(layouts.items()):
        if data.get("modular") or " - " in hull or hull in grouped_sections:
            continue
        if not data["sockets"]:
            continue
        blocks.append((DISPLAY.get(hull, hull), load_rows(hull, data),
                       data["ships"], data.get("ships_raw", 0)))

    total_rows = sum(len(merge_rows(rows)) for _, rows, *_ in blocks)
    total_ships = sum(n for _, _, n, *_ in blocks)

    head = [
        "# 槽位配置总表（按船体）",
        "",
        "每张表来自真实存档样本：`填充率` 是这一格被装上东西的比例（>90% 是骨架，<40% 通常是可选），",
        "`常用部件（艘次）` 是出现最多的部件，`备选` 是其余常见的几种。",
        "炮位号（`MT1`…）用的是**游戏里的挂载号**，也就是 `Ship Builds.txt` 里 `(mount 1-3)` 指的那个号：",
        "分段船体（LN / CLN / CVLN）的炮位号全船连续（LN 是 MT1–MT17，6×10×6 主炮 = MT1–8；"
        "CLN / CVLN 是 MT1–MT11）",
        "所以同一个 `MTn` 在三段里不会重复；舱室/模块游戏不编号，按分段内从 1 起（`CMP1`…/`MOD1`…），",
        "所以这类表都带 `段` 列——先看段，再看号。同一分段内 A/B/C 三种外观共用一张表。",
        "单体 prefab 的船（MN Flathead、CVL Journeyman 等）没有 `段` 列，`MTn` 就是 prefab 里的槽位号。",
        "尺寸相同的模块槽内容可以互换，编号只影响外观顺序。",
        "存档里的旧名字已经换算成当前版本的部件名（`Mk550 Mass Driver` → `Mk550 Railgun`）；",
        "当前版本里已经不存在的部件（如 `C54 Cannon`）一律不出现在表里。",
        "",
        f"共 {len(blocks)} 个船体分组 / {total_rows} 行 / {total_ships} 艘样本。"
        "样本按质量加权：符合舰级要求且点数在区间内的算 1 份，价格偏高算 0.6、偏低（greed）算 0.35，"
        "被判为 `bad_class` 的只算 0.1，未参与分类的算 0.25 —— 所以「艘次」是加权后的数量，不总是整数。",
        "",
    ]
    body: list[str] = []
    for name, rows, n, raw in blocks:
        body.extend(render_block(name, rows, n, raw))

    KB_DOC.write_text("\n".join(head + body), encoding="utf-8")
    REPORT.write_text("\n".join([
        "# 槽位布局总览（所有船体一页看完）",
        "",
        "同一份数据，供人工核对；KB 页面见 `domain/kb/manual_zh/槽位配置总表.md`。",
        "",
        *body,
    ]), encoding="utf-8")
    print(f"groups: {len(blocks)}  rows: {total_rows}  -> {KB_DOC.relative_to(ROOT)}")
    print(f"csv:    {CSV_PATH.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

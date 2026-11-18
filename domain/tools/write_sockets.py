"""Write one KB document per hull listing every socket (mount / compartment / module).

The socket numbers are the prefab hierarchy order recovered in
`extract_socket_order.py`, which is the order the game itself enumerates them in
(`HullSocket.Key` insertion order in `Hull.AllSockets`).  That makes "mount 1",
"mount 7" and the `Ship Builds.txt` conditions checkable.

Two kinds of page come out of here:

  * one per prefab / section in `hull_sockets.json` — the actual socket tables;
  * one per hull that is assembled from bow + core + stern sections
    (`hulls.SECTIONS`: the Marauder, the Moorline and the Container Hauler Refit).
    Those hulls have no single prefab, so their page lists the section tables, the
    segment GUIDs a `.fleet` needs and the socket totals — the rows live in the
    section pages.

Everything else — Flathead Monitor, Journeyman Light Carrier, Draugr, Ferryman … — is
one prefab, so it gets a plain socket map (with an alias page for the modern name).

Usage: python domain/tools/write_sockets.py [--out domain/kb/socket_docs]
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "domain" / "tools"))
import hulls as hu  # noqa: E402

DATA = ROOT / "domain" / "data" / "hull_sockets.json"
DEFAULT_OUT = ROOT / "domain" / "kb" / "socket_docs"

# 槽位 key -> 游戏挂载号。同一 key 在不同船体族里的号一致（Bulk/Container 的
# `Bulk - X - Bow` 与 `Container - X - Bow` 共享 11 个 key，号完全相同），
# 所以可以建成一张全局表；查不到号时退回该段内的顺序号。
MOUNT_NO: dict[str, int] = {}
for _fam in ("Marauder Line Ship", "Moorline Line Ship", "Container Hauler Refit",
             "Flathead Monitor", "Ferryman Clipper", "Draugr Clipper",
             "Journeyman Light Carrier"):
    for _key, _num in hu.mount_numbers(_fam).items():
        MOUNT_NO.setdefault(_key, _num)

TYPE_LABEL = {"Surface": "Mount", "Compartment": "Compartment", "Module": "Module"}

#: prefab name -> (modern wiki name, in-game `Stock/…` key).  The alias page is how a
#: model searching for the modern ship finds the socket map of the prefab it really is.
ALIAS_PAGES = {
    "Ocello Cruiser": ("Ocello Command Cruiser", "Stock/Ocello Cruiser"),
    "Shuttle Clipper": ("Ferryman Clipper", "Stock/Shuttle"),
    "Tug Clipper": ("Draugr Clipper", "Stock/Tugboat"),
    "Mercator Oiler": ("Mercator Replenishment Oiler", "Stock/Mercator Oiler"),
    # Journeyman Light Carrier: one `Ore Carrier` prefab, 17 sockets = 3 / 8 / 6.
    "Ore Carrier": ("Journeyman Light Carrier", "Stock/Ore Carrier"),
    # Flathead Monitor: one `Bulk Clipper` prefab, 19 sockets = 6 / 6 / 7.  It is *not*
    # built from sections — no saved Flathead carries a <HullConfig>.
    "Bulk Clipper": ("Flathead Monitor", "Stock/Bulk Feeder"),
}

#: 舰级缩写只用于分段船体页的标题（与 `kb/manual_zh/缩写与术语表.md` 一致）。
#: 注：`hull_abbr.json` 把 Moorline 写成 LN，术语表与玩家习惯是 CLN，这里跟随术语表。
SECTION_ABBR = {
    "Marauder Line Ship": "LN",
    "Moorline Line Ship": "CLN",
    "Container Hauler Refit": "CVLN",
}


def slug(name: str) -> str:
    out = name.lower().replace(" ", "-")
    return "".join(ch for ch in out if ch.isalnum() or ch in "-_")


def cell(size) -> str:
    try:
        a, b, c = (int(x) for x in size)
    except (TypeError, ValueError):
        return "-"
    return f"{a}×{b}×{c}"


def metres(size_m) -> str:
    try:
        a, b, c = (float(x) for x in size_m)
    except (TypeError, ValueError):
        return "-"
    return f"{a:g}×{b:g}×{c:g} m"


def counts(sockets: list[dict]) -> str:
    n = {t: sum(1 for s in sockets if s.get("type") == t) for t in TYPE_LABEL}
    return f"{len(sockets)} sockets = {n['Surface']} mount / {n['Compartment']} compartment / {n['Module']} module"


def render(hull: str, entry: dict) -> str:
    # 之前只保留带 prefab 序号 `i` 的槽位，结果 A 变体（不带 `i`）一整个文件都不生成，
    # 模型查 Bow A/C 时查不到东西。挂载号现在由 `MOUNT_NO` 全局给出，不再依赖 `i`，
    # 所以整段槽位都写出来，只在文件里标一句「A/B/C 只是外观，槽位相同」。
    raw = list(entry.get("sockets", []))
    seen: set[str] = set()
    sockets = []
    for s in raw:
        k = s.get("key")
        if k in seen:
            continue
        seen.add(k)
        sockets.append(s)
    sockets.sort(key=lambda s: (s.get("i") or 10**6,))
    groups: dict[str, list[dict]] = {"Surface": [], "Compartment": [], "Module": []}
    for s in sockets:
        groups.setdefault(s.get("type", "Surface"), []).append(s)
    # `#` 列对炮位是**游戏里的挂载号**（`Ship Builds.txt` 的 `(mount 1-3)` 用的那个），
    # 舱室和模块游戏不编号，按分段内同类型从 1 起。
    mount_no = MOUNT_NO
    section = " - " in hull

    lines = [
        f"# {hull} — socket map",
        "",
        f"Tags: kind=hull sockets; hull={hull}; sockets={len(sockets)}; "
        f"mounts={len(groups['Surface'])}; "
        f"compartments={len(groups.get('Compartment') or [])}; "
        f"modules={len(groups.get('Module') or [])}",
        f"Keywords: socket, sockets, mount, mounts, slot, 槽位, 挂载位, 挂载点, 尺寸, 多大, "
        f"能装什么, 装得下, {hull}",
        f"Summary: {counts(sockets)}. The mount / compartment / module number is the one the "
        "game counts in (mount 1)/(mount 1-3) conditions — mounts are numbered 1..N across the "
        "whole ship, compartments and modules restart at 1 per "
        f"{'section (this page is one section, so the mount numbers are ship-wide)' if section else 'hull'}.",
        "Section: hull sockets;source=game prefab hierarchy (Nebulous stock/stock-f1/stock-f2 bundles)",
        "",
        "## How to read this",
        "- `Mount` = a surface mount for a weapon or a sensor.",
        "- `Compartment` = the hull cut-outs that take CIC, damage control, magazines, crew spaces.",
        "- `Module` = internal bays for reactors, drives, radar, jammers, hangars.",
        "- Size is given both in 0.25 m cells and in metres; the volume is the cell product.",
        "",
    ]
    for key in ("Surface", "Compartment", "Module"):
        rows = groups.get(key) or []
        if not rows:
            continue
        if key == "Surface":
            rows.sort(key=lambda s: MOUNT_NO.get(s["key"], 10**6))
        lines.append(f"## {TYPE_LABEL[key]}s ({len(rows)})")
        lines.append("")
        lines.append("| # | Short | Size (cells) | Size (m) | Volume (cells) | Position (m) | Default part |")
        lines.append("|---:|---|---|---|---:|---|---|")
        for order, s in enumerate(rows, start=1):
            num = s.get("i")
            if key == "Surface":
                num = mount_no.get(s["key"], order)
            elif key in ("Compartment", "Module"):
                num = order
            vol = 1
            for x in s.get("size") or []:
                try:
                    vol *= int(x)
                except (TypeError, ValueError):
                    vol = 0
            pos = s.get("pos") or [0, 0, 0]
            pos_txt = " / ".join(f"{float(p):g}" for p in pos)
            default = s.get("default_component") or "-"
            short = s.get("short") or "-"
            # 分段 prefab 里 ShortName 会重复（`Bulk - B - Bow` 有四个 `MT1`），拿它当
            # 标签会互相冲突；文档里直接写全船挂载号，和 `#` 列保持一致。
            if section and key == "Surface":
                short = f"MT{num}"
            lines.append(f"| {num} | {short} | {cell(s.get('size'))} | "
                         f"{metres(s.get('size_m'))} | {vol} | {pos_txt} | {default} |")
        lines.append("")
    return "\n".join(lines)


def render_sections(name: str) -> str:
    """Page for a hull built from bow + core + stern sections."""
    family = hu.section_family(name)
    guids = hu.segment_guids(name)
    catalog_name = ((hu.section_table().get("families") or {}).get(family) or {}).get(
        "catalog_name", family)
    save_key = hu.save_key(name)
    abbr = SECTION_ABBR.get(name) or hu.abbr(name) or "-"
    by_part = hu.sockets_by_part(name)
    merged = [entry for _, entry in by_part]
    per_part = {p: [e for q, e in by_part if q == p] for p in hu.PARTS}
    letters = sorted(guids) or ["A", "B", "C"]

    lines = [
        f"# {name} — section hull ({abbr})",
        "",
        f"Tags: kind=hull sockets; hull={name}; modular=true; sections=3; abbr={abbr}; "
        f"save_key={save_key}; total={len(by_part)}",
        f"Keywords: socket, sockets, mount, mounts, slot, 槽位, 挂载位, 分段, 船段, bow, core, stern, "
        f"random hull, HullConfig, SegmentConfiguration, 分段组装, {name}, {save_key}",
        f"Summary: {name} (save key `{save_key}`) is assembled from one bow + one core + one stern: "
        f"{len(letters)} variants per part, {len(letters) ** 3} combinations, all variants of a part "
        f"carry the same sockets. Any complete set gives {counts(merged)}; the `#` of a mount is "
        "ship-wide (continuous over the three parts), compartments and modules restart at 1 in each part.",
        "Section: hull sockets;source=game prefab hierarchy + NLHC catalog (segment GUIDs)",
        "",
        "## Parts",
        "| Part | # | Letter | Segment GUID | Sockets | Socket table |",
        "|---|---:|---|---|---|---|",
    ]
    for part in hu.PARTS:
        sockets = per_part.get(part) or []
        n = {t: sum(1 for s in sockets if s.get("type") == t) for t in TYPE_LABEL}
        doc = f"sockets/{slug(f'{family} - A - {part}')}.md"
        for i, letter in enumerate(letters, start=1):
            guid = (guids.get(letter) or {}).get(part, "-")
            lines.append(
                f"| {part} | {i} | `{letter}` | `{guid}` | "
                f"{n['Surface']} / {n['Compartment']} / {n['Module']} | {doc} |")
    lines += [
        "",
        (f"资产树里这些分段 piece 的名字是 `{catalog_name} - <letter> - <part>`，"
         f"槽位表在 `hull_sockets.json` 里按 `{family} - <letter> - <part>` 存 —— 两套名字指的是"
         "同一批 prefab。" if catalog_name != family else
         f"分段 piece 与槽位表同名：`{family} - <letter> - <part>`。"),
        "",
        "## Rules (from `zh/fleet文件结构与校验.md`)",
        "- `<HullConfig xsi:type=\"RandomHullConfiguration\">` 里 `<PrimaryStructure>` 必须正好 3 个 "
        "`<SegmentConfiguration>`：bow、core、stern。",
        "- `<SecondaryStructure />` 必须存在（哪怕没有舰桥），否则读档崩溃。",
        "- 舰桥最多一个；没有舰桥的船体只会让编辑器图形出问题。",
        "- 左右/上下分段由游戏自动镜像，同一份存档在两边都能读。",
        "",
        "## Counting",
        "- 挂载号（`#`）在这条船上是**全船连续**的：三段合起来的 surface 槽位按游戏顺序编号，"
        "`Ship Builds.txt` 的 `(mount 1-3)` 用的就是这个号；分段页的 `#` 列已经是全船号，不要按段重数。",
        "- 舱室与模块每段从 1 重新数，所以 `CMP1` 在 bow 和 core 各有一个。",
        "",
    ]
    return "\n".join(lines)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default=str(DEFAULT_OUT))
    args = ap.parse_args()
    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=True)
    for old in out.glob("*.md"):
        old.unlink()

    data = json.loads(DATA.read_text(encoding="utf-8"))
    written = 0
    for hull, entry in sorted(data.items()):
        # 以前这里要求有 `order_source`（prefab 层级证据）才写文档，于是 `Bulk - A - Bow`
        # 这类没提取到序号的变体整个文件缺失；挂载号现在按 key 全局查 `MOUNT_NO`，
        # 有没有 `i` 都不影响可读性，所以只要段里有槽位就写。
        if not entry.get("sockets"):
            continue
        # `CivBulk - *` 只记下了 Marauder 分段与基础 prefab 不同的那 3 个槽位，整页写出来
        # 会像是「core 只有 1 个舱室」；完整表在 `Bulk - *`，GUID 在 Marauder 页上。
        if hull.startswith("CivBulk - "):
            continue
        text = render(hull, entry)
        (out / f"{slug(hull)}.md").write_text(text, encoding="utf-8")
        written += 1
        alias = ALIAS_PAGES.get(hull)
        if alias:
            modern, save_key = alias
            head = (
                f"# {hull} (today: {modern}) — socket map\n\n"
                f"Alias: {hull} — in-game save key `{save_key}`; the hull is the modern {modern}, "
                "one prefab, not a segment hull."
            )
            body = text.replace(f"# {hull} — socket map", head, 1)
            (out / f"{slug(modern)}.md").write_text(body, encoding="utf-8")
            written += 1
    for name in hu.SECTIONS:
        (out / f"{slug(name)}.md").write_text(render_sections(name), encoding="utf-8")
        written += 1
    print(f"hull socket docs {written} -> {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

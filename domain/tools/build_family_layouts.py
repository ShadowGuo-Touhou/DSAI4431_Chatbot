"""Merge the section hull families (LN / CLN / CVLN) into per-hull layouts.

A section hull (`Marauder Line Ship`, `Moorline Line Ship`, `Container Hauler
Refit`) is assembled from one bow + one core + one stern chosen out of nine
prefab parts.  Saves store the base hull name (`Stock/Bulk Hauler`) and the socket
keys tell which section was used, so the layout builder already collects stats
under `Bulk - A - Bow` etc.  Those nine tables are pretty useless to a player who
thinks in "Marauder Line Ship", so this script folds them back together: every
family gets one table, one row per (section part, socket), with the part letter in
its own column.

Everything else — the Flathead Monitor, the Journeyman Light Carrier, the
clippers — is a *single* prefab with its own socket table, so it needs no merging.

It reads the socket docs (which declare `modular=true` for the three section hulls
and list the part → doc mapping) and rewrites the「样本里的常见配置」block of each
family page.

Usage::

    .venv\\Scripts\\python.exe domain\\tools\\build_family_layouts.py --docs
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "domain" / "tools"))

import build_layouts as bl  # noqa: E402  (shares slug rules and the renderer)

DATA = ROOT / "domain" / "data"
DOCS = ROOT / "domain" / "kb" / "docs" / "sockets"
SRC = ROOT / "domain" / "kb" / "socket_docs"

SECTION_ORDER = {"Bow": 0, "Core": 1, "Stern": 2}
SOCKET_ORDER = {"MT": 0, "CT": 1, "CMP": 2, "MOD": 3}


def key_of(stem: str) -> str | None:
    """`bulk---a---bow` -> `Bulk - A - Bow` using the layout table's own keys."""
    probe = re.sub(r"[^A-Za-z0-9]", "", stem).lower()
    for key in bl.SOCKETS:
        if re.sub(r"[^A-Za-z0-9]", "", key).lower() == probe:
            return key
    return None


def families() -> dict[str, list[tuple[str, str]]]:
    """{doc stem: [(part label, section hull key), …]} for every modular hull page."""
    out: dict[str, list[tuple[str, str]]] = {}
    for path in sorted(SRC.glob("*.md")):
        text = path.read_text(encoding="utf-8")
        if "modular=true" not in text:
            continue
        rows: list[tuple[str, str]] = []
        for row in re.findall(
            r"\|\s*(Bow|Core|Stern)\s*\|\s*\d+\s*\|\s*`(\w)`\s*\|\s*(sockets/[^|]+?)\s*\|", text
        ):
            section, letter, target = row
            hull = key_of(Path(target.strip()).stem)
            if hull:
                rows.append((f"{section[:1]}{letter}", hull))
        if rows:
            out[path.stem] = rows
    return out


def merged(rows: list[tuple[str, str]], layouts: dict, comps: dict) -> dict:
    """Pool the samples of a part.

    ``A``/``B``/``C`` are three prefabs of the same segment with **identical**
    sockets (same keys, sizes, types — only the visuals differ), so their tables
    are not shown three times: one row per part (Bow/Core/Stern).
    """
    sockets: dict[str, dict] = {}
    ships = 0
    seen_parts: set[str] = set()
    for label, hull in rows:
        part = label[:1]
        if part in seen_parts:
            continue
        data = layouts.get(hull)
        if not data:
            continue
        ships = max(ships, data["ships"])
        seen_parts.add(part)
        for short, entry in data["sockets"].items():
            row = dict(entry)
            row["pair"] = entry["pair"] or ""  # 号是全船唯一的游戏挂载号，加前缀会读成另一个槽
            sockets[f"{part} · {short}"] = row
    return {"ships": ships, "pairs": [], "sockets": sockets, "modular": True}


def render(name: str, data: dict, comps: dict) -> str:
    corrections = bl.CORRECTIONS.get(name, {})
    n = data["ships"]
    if not n:
        return "## 样本里的常见配置\n\n该船体目前没有样本舰，本表无法给出常见配置。\n\n"
    lines = [
        "## 样本里的常见配置（按分段部件）",
        "",
        f"来源：{n} 艘样本舰。本船是**分段船体**：先选艏/中/艉部件（`A/B/C`），"
        "三套变体的**槽位完全相同**（键、尺寸、类型都一致，只有外观不同），所以下表按「部件 · 槽位」合并列出，不再区分字母。",
        "",
        "- 配对列形如 `A6`：同一分段里左右对称的那个槽位，**两边装同款**只是建议。",
        "- 填充率 < 40% 的槽位通常是可选项；> 90% 是骨架，别空。",
        "",
        "| 部件 · 槽位 | 尺寸(格) | 配对 | 填充率 | 常用部件（价格） | 备选部件 | 这块槽位适合装 |",
        "|---|---|---|---:|---|---|---|",
    ]
    def order(item: tuple[str, dict]) -> tuple:
        label = item[0]
        part, _, socket = label.partition(" · ")
        m = re.match(r"([A-Za-z]+)(\d+)$", socket or label)
        kind = m.group(1).upper() if m else ""
        num = int(m.group(2)) if m else 0
        return (SECTION_ORDER.get(part, 3), SOCKET_ORDER.get(kind, 9), num)

    ordered = sorted(data["sockets"].items(), key=order)
    for label, e in ordered:
        top = e["top"]
        main = f"{bl._label(comps, top[0]['part'])} ×{top[0]['n']}" if top else "—"
        corr = corrections.get(label, {})
        if corr.get("part"):
            main = f"✎ {corr['part']}（人工校正）"
            if corr.get("note"):
                main += f"；{corr['note']}"
        alts = "、".join(bl._label(comps, t["part"]) for t in top[1:4]) or "—"
        specific = [tag for tag, _ in e["fit_tags"] if tag not in {"舱室", "通用模块", "船体自带"}]
        tags = "、".join(specific[:4] or [tag for tag, _ in e["fit_tags"][:3]]) or "—"
        size = "×".join(str(x) for x in e["size"])
        lines.append(
            f"| {label} | {size} | {e['pair'] or '—'} | {int(e['fill_rate'] * 100)}% "
            f"| {main} | {alts} | {tags} |"
        )
    lines += [
        "",
        "读法：`A`/`B`/`C` 只是同一分段的外观差异，槽位表通用；下表把三段合并，`艏 · MT1` 这类标签指「哪个分段的哪个槽位」。",
        "",
    ]
    return "\n".join(lines)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--docs", action="store_true")
    args = ap.parse_args()

    layouts = json.loads((DATA / "hull_layouts.json").read_text(encoding="utf-8"))
    wiki = bl.fl.WikiIndex()
    comps = {c.name: c for c in wiki.components}

    fams = families()
    print("modular families:", ", ".join(fams) or "(none)")
    for stem, rows in fams.items():
        data = merged(rows, layouts, comps)
        if not data["sockets"]:
            print(f"  {stem}: no section data")
            continue
        if args.docs:
            path = DOCS / f"{stem}.md"
            if not path.exists():
                print(f"  {stem}: doc missing")
                continue
            text = path.read_text(encoding="utf-8")
            block = render(stem, data, comps)
            start, end = "<!-- layouts:start -->", "<!-- layouts:end -->"
            if start in text and end in text:
                text = text.split(start)[0] + f"{start}\n{block}{end}" + text.split(end)[1]
            else:
                text = f"{text.rstrip()}\n\n{start}\n{block}{end}\n"
            path.write_text(text, encoding="utf-8")
        print(f"  {stem}: {len(rows)} parts, {len(data['sockets'])} slots, {data['ships']} ships")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

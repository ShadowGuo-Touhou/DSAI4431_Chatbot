"""Per-hull layout knowledge: what real fleets put in each socket.

Three outputs, all derived from the 1000+ ships we already parse:

* ``domain/data/parts_facets.csv`` — every wiki part with its numeric facets
  (size, price, power, armour-less stats, barrels, reload, sustained rpm).
* ``domain/data/hull_layouts.json`` — per hull and per socket: how often it is
  filled, which parts are used (counts), which sockets are mirrored pairs, and
  which part *types* fit the socket by size.
* ``domain/data/socket_fit.json`` — per hull and per socket: every part whose
  dimensions fit (rotation allowed) and whose kind matches the socket type.

``--docs`` then rewrites the「常见配置」section of ``docs/sockets/<hull>.md`` so
the retrieval layer sees "copy this layout" instead of "invent one".

Usage::

    .venv\\Scripts\\python.exe domain\\tools\\build_layouts.py
    .venv\\Scripts\\python.exe domain\\tools\\build_layouts.py --docs
"""

from __future__ import annotations

import argparse
import csv
import json
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path

TOOLS = Path(__file__).resolve().parent
ROOT = TOOLS.parents[1]
sys.path.insert(0, str(TOOLS))

import fleet_lib as fl  # noqa: E402
import hulls as hu  # noqa: E402

DATA = ROOT / "domain" / "data"
DOCS = ROOT / "domain" / "kb" / "docs" / "sockets"

SOCKETS = json.loads((DATA / "hull_sockets.json").read_text(encoding="utf-8"))
CORR_PATH = ROOT / "domain" / "data" / "layout_corrections.json"


PART_ALIAS = {
    # 存档里存的是**旧名**：游戏当前 prefab 已经改叫别的了。
    # `Mk550 Mass Driver` 是 SA 脊髓炮的老名字，现在叫 `Mk550 Railgun`
    #（`TE45 Mass Driver` 是 OSP 的另一门 500mm 炮，不是同一个部件）。
    "Mk550 Mass Driver": "Mk550 Railgun",
    "E15 'Masquerade' Signature Booster": "E15 'Masquerade' Deception Module",
    "P20 Flak PDT": "P20 'Bastion' PDT",
    "P11 PDT": "P11 'Pavise' PDT",
    "P60 Laser PDT": "P60 'Grazer' PDT",
    "ML-9 Mine Launcher": "ML-9 'Mine' Launcher",
    "L50 Laser Dazzler": "L50 'Blackjack' Laser Dazzler",
    "J15 Jammer": "J15 'Bellbird' Jammer",
    "J75 Jammer": "J75 'Warbler' Jammer",
    "J360 Jammer": "J360 'Lyrebird' Jammer",
    "R400 Radar": "R400 'Bloodhound' LRT Radar",
}

# 游戏当前版本里**已经不存在**的部件（老存档残留）。统计时丢掉，推荐时也不出现。
PART_DROP = {"C54 Cannon", "C4 Mount Hangar", "S2 Bandit Launcher", "S2 Twin Bandit Launcher"}

GAME_PARTS_PATH = DATA / "game_parts.json"
_ALIAS_TARGETS = set(PART_ALIAS.values())


def _tokens(text: str) -> tuple[str, ...]:
    text = text.lower().replace("'", "").replace("’", "")
    toks = re.findall(r"[a-z0-9]+", text)
    # 存档里是单数、prefab 里常是复数（`Ammunition Elevator` / `ammunition elevators`），
    # 简单去尾 s 就够用，不做完整的词形还原。
    return tuple(t[:-1] if len(t) > 3 and t.endswith("s") else t for t in toks)


def _load_inventory() -> list[set[str]]:
    try:
        names = json.loads(GAME_PARTS_PATH.read_text(encoding="utf-8"))["all"]
    except (OSError, ValueError, KeyError):
        return []
    return [set(_tokens(name)) for name in names]


INVENTORY = _load_inventory()


def canonical_part(name: str) -> str | None:
    """存档部件名 → 当前版本的部件名；返回 ``None`` 表示这个部件已经不存在了。"""
    name = PART_ALIAS.get(name, name)
    if name in PART_DROP:
        return None
    if name in _ALIAS_TARGETS:
        return name
    if not INVENTORY:
        return name
    toks = set(_tokens(name))
    if not toks:
        return name
    for game in INVENTORY:
        if toks == game or toks <= game or game <= toks:
            return name
    return None


def load_corrections() -> dict:
    try:
        return json.loads(CORR_PATH.read_text(encoding="utf-8-sig"))
    except (OSError, ValueError):
        return {}


CORRECTIONS = load_corrections()
PAIR_TOLERANCE = 0.15  # metres; mirrored prefabs are usually exact, tolerance is for float noise

KIND_BY_SOCKET = {"Surface": ("Surface",), "Compartment": ("Compartment",), "Module": ("Module",)}



PRE = {"Surface": "MT", "Compartment": "CMP", "Module": "MOD"}


def display_short(hull: str, sock: dict, order: int | None = None) -> str:
    """Slot label used in tables.

    Modular section prefabs (``Bulk - B - Bow`` …) reuse the bare prefab names
    (several sockets called ``MT1``), so there the game index ``i`` is the only
    unambiguous label — and that index is what the in-game mount numbers and the
    ``(mount 1)`` conditions refer to.
    """
    short = sock.get("short") or ""
    num = order if order is not None else (sock.get("i") or 0)
    label = f"{PRE.get(sock['type'], 'X')}{num}"
    if " - " in hull:
        return label
    return short or label


SECTION_RE = re.compile(r" - [ABC] - ")


def canon_hull(name: str) -> str:
    """``Bulk - A - Bow`` → ``Bulk - Bow``.

    The three variants of a modular segment are three *prefabs* with the same
    sockets (same keys, sizes and types — only the visuals differ), so samples
    must be pooled per part instead of being split by letter.
    """
    return SECTION_RE.sub(" - ", name)


def slugify(text: str) -> str:
    text = re.sub(r"[^A-Za-z0-9\u4e00-\u9fff]+", "-", text).strip("-").lower()
    return re.sub(r"-{2,}", "-", text)[:80] or "doc"


def dims(text: str) -> tuple[int, int, int] | None:
    m = re.match(r"^\s*(\d+)\s*x\s*(\d+)\s*x\s*(\d+)\s*$", text or "", re.I)
    return (int(m.group(1)), int(m.group(2)), int(m.group(3))) if m else None


def num(text, default=0.0) -> float:
    value = fl.to_number(text)
    return default if value is None else value


def barrels(comp: fl.Component) -> int | None:
    raw = comp.fields.get("Autoloader Capacity")
    value = fl.to_number(raw) if raw else None
    return int(value) if value else None


def reload_s(comp: fl.Component) -> float | None:
    value = fl.to_number(comp.fields.get("Reload time (s)"))
    return value if value else None


def rpm(comp: fl.Component) -> float | None:
    """Sustained rounds per minute: barrels x 60 / reload (recycle time ignored)."""
    b, r = barrels(comp), reload_s(comp)
    if not b or not r:
        return None
    return round(b * 60.0 / r, 1)


def part_kind(comp: fl.Component) -> str:
    """Which socket type a wiki part belongs to (Surface / Compartment / Module)."""
    section = comp.section.split("›")[0].strip().lower()
    if section.startswith("compartment"):
        return "Compartment"
    if section.startswith("module"):
        return "Module"
    if section.startswith("mount"):
        return "Surface"
    if section.startswith("integrated"):
        return "Integrated"  # built into a hull; never mountable
    # fall back on the record key
    return {"Weapon": "Surface", "Mount": "Surface"}.get(comp.kind, "unknown")


def part_tag(comp: fl.Component) -> str:
    """Short Chinese type label used in the「建议类型」column."""
    name = comp.name.lower()
    if "beam" in name or "beam" in comp.fields.get("Ammo", "").lower():
        return "光束武器"
    ammo = comp.fields.get("Ammo", "")
    m = re.search(r"(\d{2,3})\s*mm", ammo)
    if m and part_kind(comp) == "Surface":
        caliber = m.group(1)
        if "plasma" in name:
            return f"等离子{caliber}mm"
        return f"{caliber}mm炮"
    section = comp.section.split("›")[-1].strip()
    table = {
        "Integrated Components": "船体自带",
        "Propulsion": "推进",
        "Communications, Ewar, & Sensors": "电子战/传感器",
        "Missile Launchers": "导弹发射器",
        "Projectile weapons": "弹道武器",
        "Modules": "通用模块",
        "Compartments": "舱室",
        "Weapon support": "武器支持",
        "Flight Support": "舰载机支持",
        "Point defense weapons": "近防武器",
        "Damage control": "损管",
        "Radar": "雷达",
        "Powerplants": "供电",
        "Command": "指挥",
        "Energy weapons": "能量武器",
        "Spinal weapons": "脊炮",
    }
    return table.get(section, section or comp.kind)


def fits(part: tuple[int, int, int], socket: list[int]) -> bool:
    """Axis-aligned fit with free rotation: length-3 multiset comparison."""
    return all(p <= s for p, s in zip(sorted(part), sorted(tuple(int(x) for x in socket))))


def mirrored(a: list[float], b: list[float]) -> bool:
    return abs(a[0] + b[0]) <= PAIR_TOLERANCE and abs(a[1] - b[1]) <= PAIR_TOLERANCE and abs(a[2] - b[2]) <= PAIR_TOLERANCE


def collect_fleets() -> list[Path]:  # same corpus as classify_ships.collect_fleets
    # our own generated demo fleets must never teach the corpus (the game re-saved
    # copies of them into Saves\Fleets after the user opened them in the editor)
    generated = ("Two 450 CH", "Ten Gun Sprinters", "450 CH KB-only")
    paths: list[Path] = []
    for pattern in ("other info/fleets/**/*.fleet", "other info/ v1.12/**/*.fleet"):
        paths += sorted(ROOT.glob(pattern))
    kept_path = DATA / "fleets_kept.json"
    if kept_path.exists():
        for rec in json.loads(kept_path.read_text(encoding="utf-8")):
            p = Path(rec["path"])
            if p.exists():
                paths.append(p)
    save_root = Path(r"E:\SteamLibrary\steamapps\common\Nebulous\Saves\Fleets")
    if save_root.exists():
        for p in sorted(save_root.rglob("*.fleet")):
            text = p.read_text(encoding="utf-8", errors="ignore")
            m = re.search(r"<ModDependencies>(.*?)</ModDependencies>", text, re.S)
            ids = set(re.findall(r"<unsignedLong>(\d+)</unsignedLong>", m.group(1))) if m else set()
            # keep unmodded fleets and the one accepted mod; skip anything else
            if not ids or ids == {"3236417337"}:
                paths.append(p)
    seen, out = set(), []
    for p in paths:
        if any(token in p.name for token in generated):
            continue
        try:
            digest = p.stat().st_size, p.name
        except OSError:
            continue
        if digest in seen:
            continue
        seen.add(digest)
        out.append(p)
    return out


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--docs", action="store_true", help="rewrite the layout section of docs/sockets/*.md")
    args = ap.parse_args()

    wiki = fl.WikiIndex()
    comps: dict[str, fl.Component] = {c.name: c for c in wiki.components}

    # ---------------------------------------------------------------- facets
    facet_rows = []
    for comp in wiki.components:
        size = dims(comp.fields.get("Dimensions", ""))
        cells = size[0] * size[1] * size[2] if size else ""
        facet_rows.append(
            {
                "name": comp.name,
                "kind": part_kind(comp),
                "section": comp.section,
                "tag": part_tag(comp),
                "dims": comp.fields.get("Dimensions", ""),
                "cells": cells,
                "cost": num(comp.fields.get("Cost (pts)")),
                "mass_t": num(comp.fields.get("Mass (Tonnes)")),
                "hp": num(comp.fields.get("Hitpoints")),
                "dt": num(comp.fields.get("Damage Threshold")),
                "power_kw": comp.power,
                "ammo": comp.fields.get("Ammo", ""),
                "barrels": barrels(comp) or "",
                "reload_s": reload_s(comp) or "",
                "rpm": rpm(comp) or "",
                "faction": comp.fields.get("Faction (wiki logo)", "both"),
                "cells_launcher": comp.fields.get("Capacity (cells, minimum)", ""),
                "storage_m3": comp.fields.get("Storage Capacity", ""),
            }
        )
    csv_path = DATA / "parts_facets.csv"
    with csv_path.open("w", encoding="utf-8-sig", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=list(facet_rows[0]))
        writer.writeheader()
        writer.writerows(facet_rows)
    print(f"facets: {len(facet_rows)} parts -> {csv_path.relative_to(ROOT)}")

    # 编号规则：**用游戏自己的挂载号**。
    # 固定船体：prefab 里每个槽位带 `short`（MT7 这种），直接用它。
    # 拼接船体（LN 的 Bulk/Container 三段、MN/CLN/CVL 的整块 prefab）：同一分段变体之间
    # 槽位 key 相同但顺序不同、`short` 还会重名（三个 `MT1`），所以只能回到游戏的判定
    # 依据 —— `Ship Builds.txt` 的 `(mount 1-3)` 指的是 `hulls.mount_numbers()` 给出的
    # **全船连续挂载号**（6×10×6 主炮 = 1-8，3×4×3 = 9-13，2×2×2 = 14-17）。用连续号
    # 的好处：A/B/C 三个变体对同一个槽位给出同一个号，和游戏内看到的号一致。
    # 舱室 / 模块游戏不编号，仍按分段内同类型从 1 起（CMP1… / MOD1…），表里带 `段` 列。
    # 只有部分变体写了 `i`（A 变体全都缺），但槽位 key 在 A/B/C 之间是共享的，所以按
    # key 建一张全局 `i` 表就够；没 `i` 的槽位退回归一化后的坐标排序，保证每次生成一致。
    key_i: dict[str, int] = {}
    for info in SOCKETS.values():
        for sock in info["sockets"]:
            if sock.get("i"):
                key_i.setdefault(sock["key"], int(sock["i"]))

    def order_key(sock: dict, fallback: int) -> tuple:
        return (key_i.get(sock["key"], 10**6), tuple(sock.get("pos") or ()), fallback)

    label_of: dict[tuple[str, str], str] = {}
    canon_ordered: dict[str, list[dict]] = {}
    game_mounts = {
        fam: hu.mount_numbers(fam)
        for fam in ("Bulk Hauler", "Container Hauler", "Container Hauler Refit",
                    "Bulk Feeder", "Shuttle", "Tugboat", "Ore Carrier")
    }
    for hull, info in SOCKETS.items():
        canon = canon_hull(hull)
        if " - " not in hull:  # 固定船体：直接用 prefab 自带的短名（MT7 等）
            for order, sock in enumerate(info["sockets"], start=1):
                label_of[(canon, sock["key"])] = display_short(hull, sock, order)
            continue
        socks = canon_ordered.setdefault(canon, [])
        seen = {s["key"] for s in socks}
        for order, sock in enumerate(info["sockets"], start=1):
            if sock["key"] not in seen:
                socks.append(dict(sock, _fallback=order))
                seen.add(sock["key"])
    for canon, socks in canon_ordered.items():
        numbers: dict[str, int] = {}
        for family, table in game_mounts.items():
            for key, mount_no in table.items():
                numbers.setdefault(key, mount_no)
        counters: dict[str, int] = {}
        for sock in sorted(socks, key=lambda s: order_key(s, s["_fallback"])):
            kind = sock["type"]
            counters[kind] = counters.get(kind, 0) + 1
            if kind == "Surface" and sock["key"] in numbers:
                label_of[(canon, sock["key"])] = f"MT{numbers[sock['key']]}"
            else:
                label_of[(canon, sock["key"])] = f"{PRE.get(kind, 'X')}{counters[kind]}"

    # ------------------------------------------------------------ socket fit
    socket_fit: dict[str, dict[str, list[str]]] = {}
    for hull, info in SOCKETS.items():
        canon = canon_hull(hull)
        per_socket: dict[str, list[str]] = {}
        for sock in info["sockets"]:
            allowed = KIND_BY_SOCKET.get(sock["type"], ())
            names = []
            for comp in wiki.components:
                if part_kind(comp) not in allowed:
                    continue
                size = dims(comp.fields.get("Dimensions", ""))
                if not size:
                    continue
                if not fits(size, sock["size"]):
                    continue
                if sock["type"] != "Compartment":
                    # surface/module parts cannot be tiled; exact overhang matters less,
                    # but a part larger than the socket can never mount
                    if not all(abs(size[i]) <= sock["size"][i] for i in range(3)):
                        continue
                names.append(comp.name)
            per_socket[label_of[(canon, sock["key"])]] = sorted(names)
        socket_fit[hull] = per_socket
        socket_fit.setdefault(canon, per_socket)
    fit_path = DATA / "socket_fit.json"
    fit_path.write_text(json.dumps(socket_fit, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"socket fit: {sum(len(v) for v in socket_fit.values())} sockets -> {fit_path.relative_to(ROOT)}")

    # ------------------------------------------------------------- layouts
    # 槽位 key 是 prefab 全局的，但 24 个 key 同时出现在两个分段 prefab 里
    # （例如 `Container - Core` 与 `Container Refit - Core` 共用 13 个 key），
    # 所以归属必须按**存档船体族**解析，不能只看 key。
    # `Stock/Container Hauler Refit` 的 48 艘存档全部用 `Container - *` 的段 GUID（没有一艘
    # 用过 `Container Refit - *`），所以两个船体族都指向 Container 段。
    FAMILY_SECTIONS = {
        "Bulk Hauler": ("Bulk - ",),
        "Container Hauler": ("Container - ",),
        "Container Hauler Refit": ("Container - ",),
        "Bulk Feeder": ("Bulk Clipper",),
        "Shuttle": ("Shuttle Clipper",),
        "Tugboat": ("Tug Clipper",),
        "Ore Carrier": ("Ore Carrier",),
    }
    key_index: dict[tuple[str, str], tuple[str, str]] = {}
    canon_sockets: dict[str, list[dict]] = {}
    for hull, info in SOCKETS.items():
        canon = canon_hull(hull)
        canon_sockets.setdefault(canon, info["sockets"])
        for sock in info["sockets"]:
            key_index[(canon, sock["key"])] = (canon, label_of[(canon, sock["key"])])
    for family, prefixes in FAMILY_SECTIONS.items():
        for section in SOCKETS:
            canon = canon_hull(section)
            if not any(canon.startswith(p) for p in prefixes):
                continue
            for sock in SOCKETS[section]["sockets"]:
                key_index[(family, sock["key"])] = (canon, label_of[(canon, sock["key"])])

    # ------------------------------------------------------ quality weighting
    verdicts: dict[tuple[str, str], tuple[str, str]] = {}
    cls_file = DATA / "ship_classification.json"
    if cls_file.exists():
        for row in json.loads(cls_file.read_text(encoding="utf-8")).get("rows", []):
            key = (str(row.get("fleet_path", "")), str(row.get("ship", "")))
            verdicts[key] = (str(row.get("verdict", "")), str(row.get("cost_band", "")))
    WEIGHT = {
        # 好的样本最重要；价格偏离的样本打折扣（低于价位区间就是 greed/贪污）；
        # 判成 bad_class 的样本几乎不参与统计；没分类的样本只作低权重补充。
        ("match", "in"): 1.0,
        ("match", "over"): 0.6,
        ("match", "under"): 0.35,
        ("bad_class", "*"): 0.1,
    }
    DEFAULT_WEIGHT = 0.25

    def weight_of(verdict: str, band: str) -> float:
        return WEIGHT.get((verdict, band), WEIGHT.get((verdict, "*"), DEFAULT_WEIGHT))

    # faction legality: a part may only be fitted by its own faction, except on CC hulls
    hull_faction: dict[str, str] = {}
    for h in wiki.hulls:
        sec = (h.section or "").lower()
        value = "SA" if "shelter" in sec else ("OSP" if "outlying" in sec else "")
        hull_faction[h.name] = value
        hull_faction[h.name.removesuffix(" Class")] = value
    part_faction = {c.name: (c.fields.get("Faction (wiki logo)", "") or "") for c in wiki.components}
    BOTH_FACTION_HULLS = {"Ocello Cruiser"}

    def legal(hull: str, part: str) -> bool:
        pf = part_faction.get(part, "")
        if not pf:
            return True
        hf = hull_faction.get(hull, "")
        if not hf or hull in BOTH_FACTION_HULLS:
            return True
        if "Shelter" in pf:
            return hf == "SA"
        if "Outlying" in pf:
            return hf == "OSP"
        return True

    stats: dict[str, dict[str, Counter]] = defaultdict(lambda: defaultdict(Counter))
    ships_seen: Counter = Counter()
    ships_raw: Counter = Counter()
    raw: dict[tuple, tuple] = {}
    fleets = collect_fleets()
    for path in fleets:
        try:
            fleet = fl.parse_fleet(path)
        except Exception:  # noqa: BLE001 — a broken save must not kill the build
            continue
        for ship in fleet.ships:
            parts = []
            hulls: set[str] = set()
            family = ship.hull_type.split("/")[-1]
            for sock in ship.sockets:
                hit = key_index.get((family, sock.key)) or key_index.get((family.split(" ")[0], sock.key))
                if not hit or not sock.component_name:
                    continue
                hull, short = hit
                bare = sock.component_name.split("/")[-1]
                name = canonical_part(bare)
                if name is None:  # 已从游戏删除的部件
                    continue
                if not legal(hull, name):
                    continue
                hulls.add(hull)
                parts.append((hull, short, name))
            if not parts:
                continue
            verdict, band = verdicts.get((str(path), ship.name), ("", ""))
            weight = weight_of(verdict, band)
            if weight <= 0:
                continue
            for hull, short, name in parts:
                stats[hull][short][name] += weight
            for hull in hulls:
                ships_seen[hull] += weight
                ships_raw[hull] += 1

    layouts: dict[str, dict] = {}
    for hull, socks in canon_sockets.items():
        n = int(round(ships_seen[hull]))
        pairs = []
        for i, a in enumerate(socks):
            for b in socks[i + 1:]:
                if a["type"] != b["type"] or a["size"] != b["size"]:
                    continue
                if mirrored(a["pos"], b["pos"]):
                    pairs.append([label_of[(hull, a["key"])], label_of[(hull, b["key"])]])
        entries = {}
        for sock in socks:
            label = label_of[(hull, sock["key"])]
            counter = stats[hull][label]
            filled = int(round(sum(counter.values())))
            top = [{"part": name, "n": int(round(n_used))} for name, n_used in counter.most_common(6)]
            tags = Counter()
            for name, n_used in counter.items():
                comp = comps.get(name)
                tags[part_tag(comp) if comp else "未知"] += n_used
            fit_names = socket_fit[hull][label]
            fit_tags = Counter()
            for name in fit_names:
                comp = comps.get(name)
                if comp:
                    fit_tags[part_tag(comp)] += 1
            entries[label] = {
                "type": sock["type"],
                "size": sock["size"],
                "pos": sock["pos"],
                "filled": filled,
                "fill_rate": round(filled / n, 3) if n else 0.0,
                "top": top,
                "observed_tags": tags.most_common(),
                "fit_count": len(fit_names),
                "fit_tags": fit_tags.most_common(),
                "pair": next((b for a, b in pairs if a == label), None)
                or next((a for a, b in pairs if b == label), None),
                "index": sock.get("i"),
            }
        layouts[hull] = {
            "ships": n,
            "ships_raw": int(round(ships_raw[hull])),
            "pairs": pairs,
            "sockets": entries,
        }

    # every section variant points at the pooled part table
    for section in list(SOCKETS):
        canon = canon_hull(section)
        if canon in layouts and section not in layouts:
            layouts[section] = {**layouts[canon], "canonical": canon}
    lay_path = DATA / "hull_layouts.json"
    lay_path.write_text(json.dumps(layouts, ensure_ascii=False, indent=1), encoding="utf-8")
    filled_ships = sum(v["ships"] for v in layouts.values())
    print(f"layouts: {len(layouts)} hulls / {filled_ships} ships -> {lay_path.relative_to(ROOT)}")

    if args.docs:
        written = patch_docs(layouts, comps)
        print(f"docs: patched {written} socket pages")

    empty = [h for h, v in layouts.items() if not v["ships"]]
    if empty:
        print(f"hulls without samples: {', '.join(empty)}")
    return 0


def patch_docs(layouts: dict[str, dict], comps: dict) -> int:
    written = 0
    for hull, data in layouts.items():
        path = DOCS / f"{slugify(hull)}.md"
        if not path.exists():
            continue
        text = path.read_text(encoding="utf-8")
        block = render_section(hull, data, comps)
        start, end = "<!-- layouts:start -->", "<!-- layouts:end -->"
        if start in text and end in text:
            head_part = text.split(start)[0]
            tail_part = text.split(end)[1]
            text = f"{head_part}{start}\n{block}{end}{tail_part}"
        else:
            text = f"{text.rstrip()}\n\n{start}\n{block}{end}\n"
        path.write_text(text, encoding="utf-8")
        written += 1
    return written


def _label(comps: dict, name: str) -> str:
    """`Mk66 Cannon（45 点）` — price from the wiki record, when known."""
    comp = comps.get(name)
    if comp is None:
        return name
    return f"{name}（{int(num(comp.fields.get('Cost (pts)')))} 点）"


def render_section(hull: str, data: dict, comps: dict) -> str:
    n = data["ships"]
    if not n:
        return "## 样本里的常见配置\n\n该船体目前没有样本舰（语料里出现 0 次），本表无法给出常见配置。\n\n"
    pairs = "、".join(f"{a} ↔ {b}" for a, b in data["pairs"]) or "无"
    lines = [
        "## 样本里的常见配置",
        "",
        f"来源：{n} 艘样本舰（存档 + 语料）。**配船时优先照抄本表的「常用部件」**，不要自己发明；"
        "本表之外的部件要么没人用，要么根本不配套。",
        "",
        f"- 镜像配对槽位（左右同位置；**建议两边装同一种部件**，这是鼓励不是强制）：{pairs}",
        "- 填充率 < 40% 的槽位通常是可选项，空着也正常；> 90% 的槽位是这级船的骨架，别空。",
        "",
        "| 槽位 | 尺寸(格) | 配对 | 填充率 | 常用部件（价格） | 备选部件 | 这块槽位适合装 |",
        "|---:|---|---|---:|---|---|---|",
    ]
    for short, e in data["sockets"].items():
        top = e["top"]
        main = f"{_label(comps, top[0]['part'])} ×{top[0]['n']}" if top else "—"
        corr = CORRECTIONS.get(hull, {}).get(short, {})
        if corr.get("part"):
            main = f"✎ {corr['part']}（人工校正）"
            if corr.get("note"):
                main += f"；{corr['note']}"
        alts = "、".join(_label(comps, t["part"]) for t in top[1:4]) or "—"
        specific = [tag for tag, _ in e["fit_tags"] if tag not in {"舱室", "通用模块", "船体自带"}]
        tags = "、".join(specific[:4] or [tag for tag, _ in e["fit_tags"][:3]]) or "—"
        size = "×".join(str(x) for x in e["size"])
        pair = e["pair"] or "—"
        lines.append(
            f"| {short} | {size} | {pair} | {int(e['fill_rate'] * 100)}% | {main} | {alts} | {tags} |"
        )
    lines += [
        "",
        "读法：「常用部件」是样本里真实装过的（艘次 = 有多少艘这么装）；「适合装」是从尺寸/类型推出的可选定位。"
        "配对两边写同款、按表挑件、别空骨架槽位——做到这三点，结果就已经在样本水平了。",
        "",
    ]
    return "\n".join(lines)


if __name__ == "__main__":
    raise SystemExit(main())

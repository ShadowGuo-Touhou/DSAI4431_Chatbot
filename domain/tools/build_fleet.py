"""Build a valid `.fleet` from scratch.

The rules come from `other info/Nebulous.decompiled.cs`; the practical
requirements are written up in `domain/kb/manual_zh/fleet文件结构与校验.md`.

What it guarantees:
  * fleet level: Name / Version / TotalPoints / FactionKey / ModDependencies /
    Ships / MissileTypes / CraftTypes -- every array present, empty if unused.
  * fixed hulls: no <HullConfig> at all (the game randomises nothing for them).
  * section hulls (`hulls.SECTIONS`: Marauder Line Ship, Moorline Line Ship,
    Container Hauler Refit): <HullConfig xsi:type="RandomHullConfiguration"> with
    exactly 3 <SegmentConfiguration>, a non-null <SecondaryStructure />, tint and
    texture variation -- the missing SecondaryStructure is what crashed the game.
    The segment GUIDs come from `domain/data/hull_sections.json`; the three
    families there are the only ones any saved hull uses.
  * sockets: real socket keys from `domain/data/hull_sockets.json`, components
    placed only when they fit by volume (rotation allowed).
  * point cost: hull cost + sum of the wiki component costs.

Usage
  build_fleet.py --hull "Stock/Sprinter Corvette" --count 10 \
      --fill MT1="Stock/Mk64 Cannon" --name "Ten Gun Sprinters" --out out.fleet
  build_fleet.py --hull "Stock/Bulk Hauler" --sections B,B,B --fill MT1="Stock/C65 Cannon"
  build_fleet.py --plan plan.json        # {"fleet": {...}, "ships": [{"hull": ..., "fills": {...}}]}

The `--fill` value is `<socket short>=<component>`; repeatable and optional --
whatever is left empty stays empty.  CIC / drive / reactor are *not* forced in;
this tool builds what you ask for, so the caller decides.
"""

from __future__ import annotations

import argparse
import json
import pathlib
import re
import sys
import uuid

ROOT = pathlib.Path(Path(__file__).resolve().parents[2])
sys.path.insert(0, str(ROOT / "domain" / "tools"))

import hulls as hu  # noqa: E402

DIMS = re.compile(r"(\d+)\s*x\s*(\d+)\s*x\s*(\d+)")


def segment_guid(hull: str, part: str, letter: str) -> str:
    """`<SegmentConfiguration><Key>` for one part of a section hull."""
    guids = hu.segment_guids(hull)
    guid = (guids.get(letter) or {}).get(part)
    if not guid:
        raise SystemExit(
            f"{hull}: no {part} segment for letter {letter!r} in hull_sections.json")
    return guid


def is_section_hull(hull: str) -> bool:
    return hu.is_segmented(hull)


def wiki_parts() -> dict[str, dict]:
    """name(norm) -> {"name","cost","dims"} for every component and hull."""
    out: dict[str, dict] = {}
    for p in (ROOT / "domain" / "kb" / "raw_official").rglob("*.json"):
        d = json.loads(p.read_text(encoding="utf-8"))
        for e in d.get("entities", []):
            f = e.get("fields", {})
            cost = f.get("Cost (pts)") or f.get("Point Cost") or f.get("Base Cost (pts)")
            m = DIMS.search(str(f.get("Dimensions") or ""))
            rec = {
                "name": e["name"],
                "cost": int(re.match(r"\d+", str(cost)).group(0)) if cost and re.match(r"\d+", str(cost)) else 0,
                "dims": tuple(int(g) for g in m.groups()) if m else None,
            }
            for variant in (e["name"], re.sub(r"\s+Class$", "", e["name"])):
                out.setdefault(re.sub(r"[^a-z0-9]+", "", variant.lower()), rec)
    return out


PARTS: dict[str, dict] = {}

GAME = json.loads((ROOT / "domain" / "data" / "game_names.json").read_text(encoding="utf-8"))
COMP_KEYS: list[str] = GAME["components"]
FACTIONS: list[str] = GAME["factions"]
_NORM_COMP = {re.sub(r"[^a-z0-9]+", "", k.split("/", 1)[-1].lower()): k for k in COMP_KEYS}
FACTION_ALIAS = {
    "stock/shelter alliance": "Stock/Alliance",
    "shelter alliance": "Stock/Alliance",
    "alliance": "Stock/Alliance",
    "protectorate": "Stock/Protectorate",
    "osp": "Stock/Protectorate",
}


def hull_key(name: str) -> str:
    """wiki/存档名 -> 游戏认的 <HullType>（`hulls.SAVE_KEY` 是唯一来源）。"""
    key = hu.save_key(name)
    if key:
        return key
    return name if name.startswith("Stock/") else name.split("/", 1)[-1]


def part_key(name: str) -> str:
    """部件显示名 -> 游戏认的 <ComponentName>（Stock/...）。"""
    short = name.split("/")[-1]
    if short in COMP_KEYS:
        return short
    key = _NORM_COMP.get(re.sub(r"[^a-z0-9]+", "", short.lower()))
    return key or f"Stock/{short}"


def faction_key(name: str) -> str:
    low = (name or "").strip().lower()
    if low in FACTION_ALIAS:
        return FACTION_ALIAS[low]
    for cand in FACTIONS:
        if cand.lower() == low:
            return cand
    return FACTIONS[0] if FACTIONS else name


def part(name: str) -> dict | None:
    short = name.split("/")[-1]
    return PARTS.get(re.sub(r"[^a-z0-9]+", "", short.lower()))


def fits(part_dims, socket) -> bool:
    if part_dims is None:
        return True
    a = sorted(part_dims)
    b = sorted(socket)
    return all(x <= y for x, y in zip(a, b))


def sockets_for(hull: str, sections: tuple[str, str, str] | None) -> list[dict]:
    """Socket list for the hull, honouring a `--sections B,B,C` letter choice."""
    return [entry for _, entry in hu.sockets_by_part(hull, sections)]


def escape(text: str) -> str:
    return (
        str(text)
        .replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
    )


def ship_xml(*, hull: str, wiki_hull: str, name: str, callsign: str, number: int,
             sockets: list[dict], fills: dict[str, str],
             sections: tuple[str, str, str] | None) -> tuple[str, int]:
    cost = part(wiki_hull)["cost"] if part(wiki_hull) else 0
    counters = {"Surface": 0, "Compartment": 0, "Module": 0}
    resolved: list[tuple[dict, str]] = []
    for sock in sockets:
        counters[sock["type"]] += 1
        idx = counters[sock["type"]]
        comp = ""
        for key in (sock["short"], f"{sock['type']}:{idx}", sock["type"], "*"):
            if key and key in fills:
                comp = fills[key]
                break
        if comp:
            resolved.append((sock, comp))
    lines: list[str] = []
    for sock, comp in resolved:
        p = part(comp)
        if p is None:
            raise SystemExit(f"unknown component: {comp}")
        if not fits(p["dims"], sock["size"]):
            raise SystemExit(
                f"{comp} {p['dims']} does not fit {sock['short'] or sock['type']} {sock['size']} on {hull}"
            )
        cost += p["cost"]
        lines.append(
            "        <HullSocket>\n"
            f"          <Key>{sock['key']}</Key>\n"
            f"          <ComponentName>{escape(part_key(comp))}</ComponentName>\n"
            "        </HullSocket>"
        )
    hull_config = ""
    if is_section_hull(wiki_hull or hull):
        scheme = sections or ("A", "A", "A")
        segs = []
        for kind, letter in zip(hu.PARTS, scheme):
            guid = segment_guid(wiki_hull or hull, kind, letter)
            segs.append(
                "          <SegmentConfiguration>\n"
                f"            <Key>{guid}</Key>\n"
                "            <Dressing />\n"
                "          </SegmentConfiguration>"
            )
        hull_config = (
            '      <HullConfig xsi:type="RandomHullConfiguration">\n'
            "        <PrimaryStructure>\n" + "\n".join(segs) + "\n        </PrimaryStructure>\n"
            "        <SecondaryStructure />\n"
            "        <HullTint>\n"
            "          <r>0.5</r>\n          <g>0.5</g>\n          <b>0.5</b>\n          <a>1</a>\n"
            "        </HullTint>\n"
            "        <TextureVariation>\n          <x>0</x>\n          <y>0</y>\n          <z>0</z>\n"
            "        </TextureVariation>\n"
            "      </HullConfig>\n"
        )
    xml = (
        "    <Ship>\n"
        '      <SaveID xsi:nil="true" />\n'
        f"      <Key>{uuid.uuid4()}</Key>\n"
        f"      <Name>{escape(name)}</Name>\n"
        f"      <Cost>{cost}</Cost>\n"
        f"      <Callsign>{escape(callsign)}</Callsign>\n"
        f"      <Number>{number}</Number>\n"
        "      <SymbolOption>0</SymbolOption>\n"
        f"      <HullType>{escape(hull_key(hull))}</HullType>\n"
        f"{hull_config}"
        "      <ModDependencies />\n"
        "      <SocketMap>\n" + "\n".join(lines) + ("\n" if lines else "") + "      </SocketMap>\n"
        "      <WeaponGroups />\n"
        "      <InitialFormation xsi:nil=\"true\" />\n"
        "      <TemplateMissileTypes />\n"
        "      <TemplateSpacecraftTypes />\n"
        "    </Ship>"
    )
    return xml, cost


def build(spec: dict) -> pathlib.Path:
    hull = spec["hull"]
    wiki_hull = hu.resolve(hull) or hull
    count = int(spec.get("count", 1))
    scheme = spec.get("sections")
    sections = tuple(scheme) if scheme else None
    sockets = sockets_for(wiki_hull, sections)
    if not sockets:
        raise SystemExit(f"no socket table for {hull}")
    fills = spec.get("fills") or {}
    ships: list[str] = []
    total = 0
    for i in range(count):
        name = spec.get("ship_name") or f"{spec.get('name', 'Ship')} {i + 1}"
        xml, cost = ship_xml(
            hull=hull, wiki_hull=wiki_hull, name=name, callsign=spec.get("callsign", name),
            number=100 + i, sockets=sockets, fills=fills, sections=sections,
        )
        ships.append(xml)
        total += cost
    out = pathlib.Path(spec["out"])
    out.parent.mkdir(parents=True, exist_ok=True)
    text = (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<Fleet xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">\n'
        f"  <Name>{escape(spec.get('name', 'Built Fleet'))}</Name>\n"
        "  <Version>3</Version>\n"
        f"  <TotalPoints>{total}</TotalPoints>\n"
        f"  <FactionKey>{escape(faction_key(spec['faction']))}</FactionKey>\n"
        "  <Description>generated by domain/tools/build_fleet.py</Description>\n"
        "  <ModDependencies />\n"
        "  <Ships>\n" + "\n".join(ships) + "\n  </Ships>\n"
        "  <MissileTypes />\n"
        "  <CraftTypes />\n"
        "</Fleet>\n"
    )
    out.write_text(text, encoding="utf-8")
    print(f"wrote {out} | {count} x {hull} | {total} pts")
    return out


def parse_fill(pairs: list[str]) -> dict[str, str]:
    out: dict[str, str] = {}
    for item in pairs:
        key, _, value = item.partition("=")
        out[key.strip()] = value.strip()
    return out


def main(argv: list[str]) -> int:
    global PARTS
    PARTS = wiki_parts()
    ap = argparse.ArgumentParser()
    ap.add_argument("--plan")
    ap.add_argument("--hull")
    ap.add_argument("--count", type=int, default=1)
    ap.add_argument("--sections")
    ap.add_argument("--faction", default="Stock/Shelter Alliance")
    ap.add_argument("--name", default="Built Fleet")
    ap.add_argument("--callsign")
    ap.add_argument("--ship-name")
    ap.add_argument("--out")
    ap.add_argument("--fill", action="append", default=[])
    ap.add_argument("--list", action="store_true", help="print the socket table for --hull and exit")
    args = ap.parse_args(argv)

    if args.list:
        wiki_hull = hu.resolve(args.hull) or args.hull
        sections = tuple(args.sections.split(",")) if args.sections else None
        sockets = sockets_for(wiki_hull, sections)
        counters = {"Surface": 0, "Compartment": 0, "Module": 0}
        for sock in sockets:
            counters[sock["type"]] += 1
            label = sock["short"] or f"{sock['type']}:{counters[sock['type']]}"
            print(f"{label:16} {sock['type']:12} {str(sock['size']):16} {sock['key']}")
        return 0

    if args.plan:
        data = json.loads(pathlib.Path(args.plan).read_text(encoding="utf-8"))
        for ship in data["ships"]:
            spec = {
                "hull": ship["hull"],
                "count": ship.get("count", 1),
                "sections": ship.get("sections"),
                "fills": ship.get("fills", {}),
                "faction": ship.get("faction") or data["fleet"]["faction"],
                "name": ship.get("name") or data["fleet"]["name"],
                "out": ship["out"],
            }
            build(spec)
        return 0

    if not args.hull or not args.out:
        ap.error("--hull and --out are required (or use --plan)")
    build({
        "hull": args.hull,
        "count": args.count,
        "sections": args.sections.split(",") if args.sections else None,
        "fills": parse_fill(args.fill),
        "faction": args.faction,
        "name": args.name,
        "callsign": args.callsign,
        "ship_name": args.ship_name,
        "out": args.out,
    })
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))

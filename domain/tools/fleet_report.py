"""Render a readable report for a NEBULOUS `.fleet` file.

Usage
-----
    python fleet_report.py "S2 DIR OCELLO.fleet"
    python fleet_report.py --json "S2 DIR OCELLO.fleet"
    python fleet_report.py --all "E:\\...\\Saves\\Fleets"     # folder summary

Everything comes from the wiki (game 0.6.2.6:260903-1430), the file itself, and
`socket_lib` -- hull socket sizes/types/positions extracted from the game's own
asset bundles.  That makes a real fit check possible: every fitted component is
matched against the socket it sits in.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from collections import Counter
from pathlib import Path

from fleet_lib import (
    Fleet,
    Hull,
    WikiIndex,
    is_modded,
    parse_fleet,
    save_key_name,
)
from socket_lib import SocketTables, dims, fits, socket_type_for_section

CATEGORY_ORDER = (
    "Missile Launchers",
    "Point Defense",
    "Projectile Weapons",
    "Energy Weapons",
    "Spinal Weapons",
    "Sensors & Radar",
    "EWar",
    "Command",
    "Damage Control",
    "Powerplants",
    "Propulsion",
    "Weapon Support",
    "Flight Support",
    "Storage",
    "Communications",
    "Intelligence",
    "Engineering",
    "Crew",
    "Psyops",
)

CATEGORY_CANON = {
    "missile launchers": "Missile Launchers",
    "point defense": "Point Defense",
    "point defense weapons": "Point Defense",
    "projectile": "Projectile Weapons",
    "projectile weapons": "Projectile Weapons",
    "energy": "Energy Weapons",
    "energy weapons": "Energy Weapons",
    "spinal": "Spinal Weapons",
    "spinal weapons": "Spinal Weapons",
    "sensors": "Sensors & Radar",
    "radar": "Sensors & Radar",
    "ewar": "EWar",
    "command": "Command",
    "damage control": "Damage Control",
    "powerplant": "Powerplants",
    "powerplants": "Powerplants",
    "propulsion": "Propulsion",
    "weapon support": "Weapon Support",
    "flight support": "Flight Support",
    "storage": "Storage",
    "communications": "Communications",
    "intelligence": "Intelligence",
    "engineering": "Engineering",
    "crew": "Crew",
    "psyops": "Psyops",
}


def canon(category: str) -> str:
    return CATEGORY_CANON.get(category.strip().lower(), category.strip())


def human(number: float) -> str:
    if abs(number - round(number)) < 0.05:
        return f"{round(number):,}"
    return f"{number:,.1f}"


def ordered(counter: Counter[str]) -> list[tuple[str, int]]:
    def key(item: tuple[str, int]) -> tuple[int, str]:
        name = item[0]
        return (CATEGORY_ORDER.index(name) if name in CATEGORY_ORDER else 99, name)

    return sorted(counter.items(), key=key)


def analyse_ship(ship, index: WikiIndex, tables: SocketTables | None = None) -> dict:
    hull: Hull | None = index.hull(ship.hull_type)
    hull_sockets = tables.hull(ship.hull_type) if tables is not None and tables.available else None
    if hull_sockets is None and tables is not None and ship.sockets:
        hull_sockets = tables.hull_by_keys({s.key for s in ship.sockets})
    known: list[tuple[str, object]] = []
    unknown: list[str] = []
    mods: list[str] = []
    slots: list[dict] = []
    mass = press = supply = listed_cost = 0.0
    categories: Counter[str] = Counter()
    ammo: Counter[str] = Counter()
    munitions: Counter[str] = Counter()

    for socket in ship.sockets:
        component = index.component(socket.component_name)
        for item in socket.ammo:
            name = save_key_name(item.item).strip("$").upper()
            ammo[name] += 1
            munitions[save_key_name(item.item)] += item.quantity
        slot = {
            "key": socket.key,
            "socket": hull_sockets.get(socket.key) if hull_sockets else None,
            "component": component,
            "name": socket.component_name,
            "verdict": "",
        }
        if hull_sockets is not None:
            if slot["socket"] is None:
                slot["verdict"] = "socket key not on this hull"
            elif component is None:
                slot["verdict"] = "unknown component"
            else:
                want = socket_type_for_section(component.section)
                size = dims(component.fields.get("Dimensions"))
                if want and want != slot["socket"].type:
                    slot["verdict"] = f"{want} in a {slot['socket'].type} socket"
                elif size and not fits(size, slot["socket"].cells):
                    slot["verdict"] = f"{'x'.join(map(str, size))} does not fit"
                else:
                    slot["verdict"] = "ok"
        slots.append(slot)
        if component is None:
            (mods if is_modded(socket.component_name) else unknown).append(socket.component_name)
            continue
        known.append((component.name, component))
        mass += component.mass
        press += component.draw
        supply += component.supply
        listed_cost += component.cost
        categories[canon(component.category)] += 1

    slots_wiki = hull.slots if hull else {}
    used = len(ship.sockets)
    warnings: list[str] = []
    if hull is None:
        warnings.append(f"hull not documented: {ship.hull_type}")
    elif used > hull.total_slots:
        warnings.append(f"sockets {used} > wiki slots {hull.total_slots}")
    if unknown:
        warnings.append(f"{len(unknown)} component(s) not in wiki: {', '.join(sorted(set(unknown)))}")
    if supply and press > supply * 1.02:
        warnings.append(f"power draw {human(press)} kW > supply {human(supply)} kW")
    if hull is not None and not any(canon(c.category) == "Powerplants" for _, c in known):
        warnings.append("no powerplant fitted")
    bad = [s for s in slots if s["verdict"] not in ("", "ok")]
    if bad:
        warnings.append(
            f"{len(bad)} socket(s) fail the fit check: "
            + "; ".join(f"{save_key_name(s['name'])} -> {s['socket'].short if s['socket'] else '?'} "
                        f"({s['verdict']})" for s in bad[:4])
        )

    return {
        "name": ship.name,
        "callsign": ship.callsign,
        "hull_type": ship.hull_type,
        "hull": hull,
        "hull_sockets": hull_sockets,
        "slots_fit": slots,
        "cost": ship.cost,
        "listed_cost": listed_cost,
        "slots_used": used,
        "slots": slots_wiki,
        "mass": mass,
        "draw": press,
        "supply": supply,
        "categories": categories,
        "known": known,
        "unknown": unknown,
        "mods": mods,
        "ammo": ammo,
        "munitions": munitions,
        "warnings": warnings,
    }


def render(fleet: Fleet, index: WikiIndex, verbose: bool = True, tables: SocketTables | None = None) -> str:
    ships = [analyse_ship(ship, index, tables) for ship in fleet.ships]
    out: list[str] = []
    add = out.append

    add(f"# Fleet: {fleet.name or fleet.path.stem}")
    add("")
    add(f"- faction: {fleet.faction}")
    add(f"- ships: {len(fleet.ships)}")
    add(f"- points: {human(fleet.ship_cost)} (file declares {human(fleet.total_points)})")
    add(f"- source: {fleet.path.name}, format v{fleet.version}")
    add("- stats: official wiki, game 0.6.2.6:260903-1430")
    add("")

    totals = Counter()
    for info in ships:
        for name, count in info["categories"].items():
            totals[name] += count

    if totals:
        add("## Fleet composition")
        for name, count in ordered(totals):
            add(f"- {name}: {count}")
        add("")

    for info in ships:
        hull = info["hull"]
        hull_name = hull.name if hull else f"{info['hull_type']} (not documented)"
        add(f"## {info['name']}" + (f"  [{info['callsign']}]" if info["callsign"] else ""))
        add("")
        line = f"- hull: {hull_name}; cost {human(info['cost'])} pts; sockets used {info['slots_used']}"
        if hull:
            line += f" of {hull.total_slots} documented ({hull.fields.get('Slots', '')})"
        add(line)
        if hull:
            add(
                f"- armor {hull.fields.get('Armor Thickness (cm)', '?')} cm, "
                f"integrity {hull.fields.get('Structural Integrity', '?')} hp, "
                f"signature {hull.fields.get('Radar Signature (m2)', '?')} m2"
            )
        mass = human(info["mass"]) + " t"
        if hull:
            mass += f" (hull {human(hull.mass)} t)"
        add(f"- fitted mass: {mass}")
        add(f"- wiki list price: {human(info['listed_cost'])} pts (compounding rules ignored)")
        if info["supply"] or info["draw"]:
            add(
                f"- power: draw {human(info['draw'])} kW / supply {human(info['supply'])} kW "
                f"→ margin {human(info['supply'] - info['draw'])} kW"
            )
        for name, count in ordered(info["categories"]):
            add(f"- {name}: {count}")
        if info["ammo"]:
            short = ", ".join(f"{k}×{v}" for k, v in sorted(info["ammo"].items()))
            add(f"- munition families: {short}")
        if info["mods"]:
            add(f"- mod components ({len(info['mods'])}): {', '.join(sorted(set(info['mods'])))}")
        if info["unknown"]:
            add(f"- NOT in wiki ({len(info['unknown'])}): {', '.join(sorted(set(info['unknown'])))}")
        for warning in info["warnings"]:
            add(f"- ! {warning}")
        if verbose:
            add("")
            if info["hull_sockets"] is not None:
                add(f"| socket | type | size (cells) | fitted | check |")
                add("|---|---|---|---|---|")
                rows = [s for s in info["slots_fit"] if s["socket"] is not None]
                rows.sort(key=lambda s: (s["socket"].type, s["socket"].short))
                for slot in rows:
                    socket = slot["socket"]
                    fitted = socket_name = save_key_name(slot["name"])
                    if slot["component"] is not None:
                        socket_name = slot["component"].name
                    add(
                        f"| {socket.short} | {socket.type} | {'x'.join(str(c) for c in socket.cells)} "
                        f"| {socket_name} | {slot['verdict'] or '-'} |"
                    )
                for slot in (s for s in info["slots_fit"] if s["socket"] is None):
                    add(f"| ? | ? | ? | {save_key_name(slot['name'])} | socket key not on this hull |")
            else:
                add("| component | category | pts | mass t | kW |")
                add("|---|---|---|---|---|")
                for _, component in info["known"]:
                    add(
                        f"| {component.name} | {canon(component.category)} | {human(component.cost)} | "
                        f"{human(component.mass)} | {human(component.power)} |"
                    )
                if info["mods"] or info["unknown"]:
                    for name in sorted(set(info["mods"] + info["unknown"])):
                        add(f"| {save_key_name(name)} | (mod / undocumented) | ? | ? | ? |")
        add("")

    warnings = [w for info in ships for w in info["warnings"]]
    add("## Checks")
    if warnings:
        for warning in warnings:
            add(f"- {warning}")
    else:
        add("- no issues found")
    add("")
    add(
        "Socket sizes/types come from the game's own asset bundles (`HullSocket`, 0.25 m "
        "grid cells), so the `check` column applies the same rule the game applies when you "
        "place a component. Names in `?` rows are mod components or game builds newer than the wiki."
    )
    return "\n".join(out)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Render a NEBULOUS fleet report.")
    parser.add_argument("path", type=Path, help="a .fleet file or a folder of them")
    parser.add_argument("--json", action="store_true", help="machine readable output")
    parser.add_argument("--brief", action="store_true", help="skip the per-ship component table")
    parser.add_argument("--limit", type=int, default=0, help="with a folder: only the first N files")
    args = parser.parse_args(argv)

    index = WikiIndex()
    tables = SocketTables()
    path: Path = args.path
    if path.is_dir():
        files = sorted(path.rglob("*.fleet"))
        if args.limit:
            files = files[: args.limit]
        print(f"{len(files)} fleet file(s) under {path}")
        for item in files:
            try:
                fleet = parse_fleet(item)
            except Exception as error:  # noqa: BLE001 - a bad save must not stop the run
                print(f"  ! {item.name}: {error}")
                continue
            ships = [analyse_ship(ship, index, tables) for ship in fleet.ships]
            unknown = sum(len(s["unknown"]) for s in ships)
            print(
                f"  {item.stem[:44]:44s} ships={len(fleet.ships):2d} "
                f"pts={human(fleet.ship_cost):>7s} unknown={unknown}"
            )
        return 0

    fleet = parse_fleet(path)
    if args.json:
        payload = []
        for ship in fleet.ships:
            info = analyse_ship(ship, index, tables)
            payload.append(
                {
                    "name": info["name"],
                    "hull": info["hull"].name if info["hull"] else None,
                    "cost": info["cost"],
                    "slots_used": info["slots_used"],
                    "slots": info["slots"],
                    "mass": info["mass"],
                    "power_draw": info["draw"],
                    "power_supply": info["supply"],
                    "categories": dict(info["categories"]),
                    "unknown": info["unknown"],
                    "mods": info["mods"],
                    "warnings": info["warnings"],
                    "socket_check": [
                        {
                            "socket": s["socket"].short if s["socket"] else None,
                            "type": s["socket"].type if s["socket"] else None,
                            "size": list(s["socket"].cells) if s["socket"] else None,
                            "fitted": save_key_name(s["name"]),
                            "check": s["verdict"],
                        }
                        for s in info["slots_fit"]
                    ],
                }
            )
        print(json.dumps({"fleet": fleet.name, "points": fleet.ship_cost, "ships": payload}, ensure_ascii=False, indent=2))
        return 0

    sys.stdout.write(render(fleet, index, verbose=not args.brief, tables=tables) + "\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())


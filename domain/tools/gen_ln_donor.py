"""Generate hybrid-LN test fleets by *editing real fleets*, so every structural
field (HullConfig, Dressing, SecondaryStructure, WeaponGroups, socket keys) is
copied verbatim from a fleet the game itself wrote.

Only <ComponentName> values and the ship <Cost> / fleet <TotalPoints> change.

Loadout rule (OSP, fits by volume and faction):
    6x10x6 mount -> Stock/C65 Cannon 450mm
    3x4x3 mount -> Stock/RL18 Launcher
    2x2x2 mount -> Stock/P20 'Bastion' PDT
    compartment -> Stock/Basic CIC (first only)
    3x3x3 module -> Stock/Light Civilian Reactor
    6x6x6 module -> Stock/Boosted Reactor
    12x12x12 module -> Stock/BW1500 Drive
"""

from __future__ import annotations

import json
import pathlib
import re
import xml.etree.ElementTree as ET

ROOT = pathlib.Path(Path(__file__).resolve().parents[2])
OUT = ROOT / "other info" / "LN test fleets"
SAVES = pathlib.Path(r"E:\SteamLibrary\steamapps\common\Nebulous\Saves\Fleets")
SOCKETS = json.loads((ROOT / "domain" / "data" / "hull_sockets.json").read_text(encoding="utf-8"))

# key -> (size, type) across every extracted table
KEY_SIZE: dict[str, tuple[list[int], str]] = {}
for _entry in SOCKETS.values():
    for _s in _entry["sockets"]:
        KEY_SIZE.setdefault(_s["key"], (_s["size"], _s["type"]))

MOUNTS = [
    ((6, 10, 6), "Stock/C65 Cannon", 40),
    ((3, 4, 3), "Stock/RL18 Launcher", 30),
    ((2, 2, 2), "Stock/P20 'Bastion' PDT", 15),
]
MODULES = [
    ((12, 12, 12), "Stock/BW1500 Drive", 10),
    ((6, 6, 6), "Stock/Boosted Reactor", 10),
    ((3, 3, 3), "Stock/Light Civilian Reactor", 10),
]

DONORS = [
    "S2LN NEO.fleet",
    "LIGHT max.fleet",
    "Azur Lame.fleet",
    "CC mdln test 6.fleet",
    "CC LN test 4 450.fleet",
]


def fits(socket: list[int], part: list[int]) -> bool:
    vol_s = socket[0] * socket[1] * socket[2]
    vol_p = part[0] * part[1] * part[2]
    if vol_p > vol_s:
        return False
    # a part that is larger than the socket on two axes can never be placed
    return sum(1 for i in range(3) if part[i] > socket[i]) <= 1


def choose(size: list[int], table):
    for dims, comp, cost in table:
        if fits(size, dims):
            return comp, cost
    return None, 0


def rebuild(fleet_path: pathlib.Path, tag: str) -> pathlib.Path | None:
    text = fleet_path.read_text(encoding="utf-8", errors="ignore")
    ships = list(re.finditer(r"<Ship>.*?</Ship>", text, re.S))
    if not ships:
        return None
    pick = None
    for mo in ships:
        if "Stock/Bulk Hauler" in mo.group(0) and "<HullConfig" in mo.group(0):
            pick = mo
            break
    if pick is None:
        return None
    ship = pick.group(0)

    used_cic = False
    used_drive = False
    total = 0
    names: dict[str, str] = {}

    def repl(mo: re.Match[str]) -> str:
        nonlocal used_cic, used_drive, total
        key, old = mo.group(1), mo.group(2)
        size, stype = KEY_SIZE.get(key, ([0, 0, 0], ""))
        comp, cost = old, 0
        if stype == "Surface":
            comp, cost = choose(size, MOUNTS)
            if comp is None:
                comp, cost = "", 0
        elif stype == "Compartment":
            if not used_cic:
                comp, cost, used_cic = "Stock/Basic CIC", 10, True
            else:
                comp, cost = "", 0
        elif stype == "Module":
            comp, cost = choose(size, MODULES)
            if comp is None:
                comp, cost = "", 0
            elif "Drive" in comp:
                if used_drive:
                    comp, cost = "", 0
                else:
                    used_drive = True
        if comp:
            names[key] = comp
            total += cost
            return f"<Key>{key}</Key>\n          <ComponentName>{comp}</ComponentName>"
        return f"<Key>{key}</Key>\n          <ComponentName />"

    new_ship = re.sub(
        r"<Key>([^<]+)</Key>\s*<ComponentName>([^<]*)</ComponentName>",
        repl,
        ship,
    )
    new_ship = re.sub(r"<Cost>\d+</Cost>", f"<Cost>{total}</Cost>", new_ship, count=1)
    new_ship = re.sub(r"<Name>[^<]*</Name>", f"<Name>LN {tag}</Name>", new_ship, count=1)
    new_ship = re.sub(r"<Callsign>[^<]*</Callsign>", f"<Callsign>{tag}</Callsign>", new_ship, count=1)

    head = text[: pick.start()]
    tail = text[pick.end():]
    # keep a single ship: drop every other <Ship> block
    head = re.sub(r"<Ship>.*?</Ship>", "", head, flags=re.S)
    tail = re.sub(r"<Ship>.*?</Ship>", "", tail, flags=re.S)
    head = re.sub(r"<Name>[^<]*</Name>", f"<Name>LN {tag}</Name>", head, count=1)
    head = re.sub(r"<TotalPoints>\d+</TotalPoints>", f"<TotalPoints>{total}</TotalPoints>", head, count=1)
    for elem in ("ModDependencies", "MissileTypes", "CraftTypes"):
        if f"<{elem}" not in head + tail:
            head = head.replace("<Ships>", f"<{elem} />\n  <Ships>", 1)
    out = OUT / f"LN {tag}.fleet"
    out.write_text(head + new_ship + tail, encoding="utf-8")
    normalise(out)
    return out


def normalise(path: pathlib.Path) -> None:
    """Guarantee the fleet-level arrays exist as elements, touching nothing else."""
    text = path.read_text(encoding="utf-8")
    cut = text.find("<Ships>")
    head, rest = (text[:cut], text[cut:]) if cut > 0 else ("", text)
    if "<ModDependencies" not in head:
        head = head.rstrip() + "\n  <ModDependencies />\n  "
        text = head + rest
    if "<CraftTypes" not in text.rsplit("</Ships>", 1)[-1]:
        text = text.replace("</Fleet>", "  <CraftTypes />\n</Fleet>", 1)
    if "<MissileTypes" not in text.rsplit("</Ships>", 1)[-1]:
        text = text.replace("</Fleet>", "  <MissileTypes />\n</Fleet>", 1)
    path.write_text(text, encoding="utf-8")


def main() -> int:
    OUT.mkdir(parents=True, exist_ok=True)
    found: dict[str, pathlib.Path] = {}
    for f in SAVES.rglob("*.fleet"):
        if f.name in DONORS and f.name not in found:
            found[f.name] = f
    made = 0
    for name in DONORS:
        p = found.get(name)
        if p is None:
            print("missing donor:", name)
            continue
        root = ET.fromstring(p.read_text(encoding="utf-8", errors="ignore"))
        ship_el = None
        for cand in root.findall("./Ships/Ship"):
            if "Stock/Bulk Hauler" in (cand.findtext("HullType") or ""):
                ship_el = cand
                break
        segs = [
            (k.text or "")[:8]
            for k in ship_el.findall("./HullConfig/PrimaryStructure/SegmentConfiguration/Key")
        ] if ship_el is not None else []
        tag = "-".join(segs[:3]) if segs else name.replace(".fleet", "")[:8]
        out = rebuild(p, tag)
        if out:
            made += 1
            print(f"{out.name}  <- {name}  segs={segs}")
    print("total", made)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

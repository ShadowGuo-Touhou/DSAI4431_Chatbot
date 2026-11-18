"""Read a filled LN test fleet and report each socket's section + local position.

The `.fleet` file stores, for every fitted component, the socket `<Key>`; those keys
are the same strings `domain/data/hull_sockets.json` carries, so the saved fleet is
a direct key -> (section, short name, local position) lookup.  The user fitted the
cannons on the **left** and the PD/launchers on the **right**, which turns the sign
of the local X coordinate into the left/right convention.

    python domain/tools/read_orientation.py "other info/LN orientation/ORI all.fleet"
"""

from __future__ import annotations

import json
import pathlib
import sys
import xml.etree.ElementTree as ET

ROOT = pathlib.Path(__file__).resolve().parents[2]
SOCKETS = ROOT / "domain" / "data" / "hull_sockets.json"

PART_SIDE = {
    "C65 Cannon": "L", "T81 Plasma Cannon": "L", "T30 Cannon": "L",
    "C54 Cannon": "L", "C56 Cannon": "L", "C53 Cannon": "L",
    "P60 Laser PDT": "R", "P20 Flak PDT": "R", "RL18 Launcher": "R",
    "VLS-1-46 Launcher": "R", "VLS-1-23 Launcher": "R", "Aurora": "R",
}


def by_key() -> dict[str, dict]:
    data = json.loads(SOCKETS.read_text(encoding="utf-8"))
    out: dict[str, dict] = {}
    for name, entry in data.items():
        if not isinstance(entry, dict) or "sockets" not in entry:
            continue
        for s in entry["sockets"]:
            k = s.get("key")
            if k:
                out[k] = {**s, "table": name}
    print(f"indexed {len(out)} socket keys from {len(data)} tables")
    return out


def fmt_pos(pos) -> str:
    if not isinstance(pos, list) or len(pos) != 3:
        return "?"
    return f"({pos[0]:+.2f}, {pos[1]:+.2f}, {pos[2]:+.2f})"


def main(argv: list[str]) -> int:
    rel = argv[1] if len(argv) > 1 else r"other info\LN orientation\ORI all.fleet"
    path = pathlib.Path(rel)
    if not path.is_absolute():
        path = ROOT / path
    keys = by_key()
    root = ET.parse(path).getroot()

    agree = disagree = 0
    for ship in root.iter("Ship"):
        name = ship.findtext("Name") or "?"
        smap = ship.find("SocketMap")
        if smap is None:
            continue
        print(f"\n== {name}")
        for hs in smap.findall("HullSocket"):
            key = (hs.findtext("Key") or "").strip()
            comp = (hs.findtext("ComponentName") or "").split("/")[-1]
            info = keys.get(key)
            if not info:
                print(f"   key {key!r} not found  <- {comp}")
                continue
            pos = info.get("pos")
            side = "?"
            if isinstance(pos, list) and len(pos) == 3:
                side = "L" if pos[0] < 0 else "R"
            want = PART_SIDE.get(comp, "?")
            ok = "ok" if want == side else ("? skip" if want == "?" else "MISMATCH")
            if want != "?":
                if ok == "ok":
                    agree += 1
                else:
                    disagree += 1
            print(f"   {info['table']:<18} {info['short']:<6} {info['type']:<11} "
                  f"x={pos[0]:+7.2f} y={pos[1]:+6.2f} z={pos[2]:+7.2f}  {comp:<26} "
                  f"side={side} want={want} {ok}")
    print(f"\nagree={agree} disagree={disagree}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))

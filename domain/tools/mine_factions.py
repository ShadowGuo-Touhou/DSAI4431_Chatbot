"""Mine component/munition faction membership from the player's own fleet files.

Nothing on the wiki lists which faction a part belongs to, but every ``.fleet``
file carries ``<FactionKey>`` and the parts the player fitted.  Aggregating 344
saved fleets gives a reliable faction tag for every part that has ever been
fitted, plus a count so the generator can flag parts seen under both factions.

Usage:
    python domain/tools/mine_factions.py [--saves DIR] [--out FILE]
"""

from __future__ import annotations

import argparse
import json
import re
import xml.etree.ElementTree as ET
from collections import Counter, defaultdict
from pathlib import Path

PROJECT = Path(__file__).resolve().parents[2]
DEFAULT_SAVES = Path(r"E:\SteamLibrary\steamapps\common\Nebulous\Saves\Fleets")
DEFAULT_OUT = PROJECT / "domain" / "data" / "factions.json"

FACTION_ALIAS = {
    "Stock/Protectorate": "OSP",
    "Stock/Shelter Alliance": "SA",
}


def short_faction(key: str) -> str:
    key = (key or "").strip()
    if key in FACTION_ALIAS:
        return FACTION_ALIAS[key]
    return key.rsplit("/", 1)[-1] or "unknown"


def iter_parts(root: ET.Element) -> tuple[str, set[str]]:
    faction = short_faction(root.findtext("FactionKey", ""))
    names: set[str] = set()
    for component in root.iter("ComponentName"):
        if component.text:
            names.add(component.text.strip())
    for munition in root.iter("MunitionKey"):
        if munition.text and not munition.text.startswith("$MODMIS$"):
            names.add("munition:" + munition.text.strip())
    return faction, names


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--saves", type=Path, default=DEFAULT_SAVES)
    parser.add_argument("--out", type=Path, default=DEFAULT_OUT)
    args = parser.parse_args()

    per_faction: dict[str, Counter] = defaultdict(Counter)
    fleets = 0
    errors = 0
    for path in sorted(args.saves.rglob("*.fleet")):
        try:
            root = ET.parse(path).getroot()
        except ET.ParseError:
            errors += 1
            continue
        fleets += 1
        faction, names = iter_parts(root)
        for name in names:
            per_faction[faction][name] += 1

    components: dict[str, dict[str, int]] = {}
    for faction, counter in per_faction.items():
        for name, count in counter.items():
            components.setdefault(name, {})[faction] = count

    summary = {
        "fleets": fleets,
        "errors": errors,
        "factions": {f: sum(c.values()) for f, c in per_faction.items()},
        "parts": len(components),
        "exclusive": sum(1 for v in components.values() if len(v) == 1),
        "shared": sum(1 for v in components.values() if len(v) > 1),
        "data": components,
    }
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(summary, ensure_ascii=False, indent=1), encoding="utf-8")

    print(f"fleets {fleets} (parse errors {errors}), parts {len(components)}")
    for faction, total in sorted(summary["factions"].items(), key=lambda kv: -kv[1]):
        print(f"  {faction:16s} {total:6d} fittings")
    print(f"  exclusive {summary['exclusive']}, shared {summary['shared']} -> {args.out}")
    shared = [(k, v) for k, v in components.items() if len(v) > 1]
    for name, counts in shared[:15]:
        print("   shared:", name, counts)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

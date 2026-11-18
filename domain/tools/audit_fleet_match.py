"""How many sockets in the player's 344 fleets resolve against the wiki DB?"""
from __future__ import annotations

import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from fleet_lib import WikiIndex, parse_fleet  # noqa: E402

FLEETS = Path(r"E:\SteamLibrary\steamapps\common\Nebulous\Saves\Fleets")


def main() -> int:
    index = WikiIndex()
    matched: Counter[str] = Counter()
    missed: Counter[str] = Counter()
    hull_hit: Counter[str] = Counter()
    hull_miss: Counter[str] = Counter()
    files = 0
    bad: list[str] = []
    for path in sorted(FLEETS.rglob("*.fleet")):
        try:
            fleet = parse_fleet(path)
        except Exception as error:  # noqa: BLE001
            bad.append(f"{path.name}: {error}")
            continue
        files += 1
        for ship in fleet.ships:
            (hull_hit if index.hull(ship.hull_type) else hull_miss)[ship.hull_type] += 1
            for socket in ship.sockets:
                prefix = socket.component_name.split("/", 1)[0]
                bucket = matched if index.component(socket.component_name) else missed
                bucket[prefix] += 1
    total = sum(matched.values()) + sum(missed.values())
    print(f"files parsed: {files}, unreadable: {len(bad)}")
    print(f"sockets: {total}, matched: {sum(matched.values())} "
          f"({sum(matched.values()) / max(total, 1):.1%}), unmatched: {sum(missed.values())}")
    print("matched by faction:", dict(matched.most_common()))
    print("unmatched by faction:", dict(missed.most_common()))
    print(f"hulls: matched {sum(hull_hit.values())}, unmatched {sum(hull_miss.values())}")
    print("unmatched hull types:", dict(hull_miss.most_common()))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

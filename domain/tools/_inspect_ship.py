"""Ad-hoc: print the fitted sockets of a few ships with their in-game mount numbers."""

from __future__ import annotations

import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))

import fleet_lib as fl  # noqa: E402
import hulls as hu  # noqa: E402

WANTED = {"Hello"}


def main() -> int:
    idx = fl.WikiIndex()
    seen: set[tuple[str, int]] = set()
    for root in (r"E:\SteamLibrary\steamapps\common\Nebulous\Saves\Fleets", r"other info\fleets"):
        for path in pathlib.Path(root).rglob("*.fleet"):
            try:
                fleet = fl.parse_fleet(path)
            except Exception:  # noqa: BLE001
                continue
            for ship in fleet.ships:
                tag = (ship.name, int(ship.cost or 0))
                if ship.name not in WANTED or tag in seen:
                    continue
                seen.add(tag)
                numbers = hu.mount_numbers(ship.hull_type)
                print(f"== {ship.name} {tag[1]} {ship.hull_type} ({path.name})")
                for sock in ship.sockets:
                    comp = idx.component(sock.component_name)
                    num = numbers.get(getattr(sock, "key", ""), "-")
                    print(f"    MT{num:<4} {sock.component_name:<44} {comp.section if comp else '?'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

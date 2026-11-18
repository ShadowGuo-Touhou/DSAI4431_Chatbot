"""Generate minimal LN hybrids whose only big mounts (the 1-8 mounts) carry four
distinct guns, so the user can read off which way each mount points.

One fleet per tested section letter:
    ORI bow A/B/C   -> triple (X, B, B), guns only in the bow's 4 big mounts
    ORI core A/B/C  -> triple (B, X, B), guns only in the core's 4 big mounts

Every gun has a different silhouette, so the report can be made by name:
    C65 Cannon (450mm, 6x10x6)   T81 Plasma Cannon (400mm, 6x3x6)
    T30 Cannon (100mm, 6x3x6)    C56 Cannon (250mm, 4x6x4)
"""

from __future__ import annotations

import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).parent))

import build_fleet as bf  # noqa: E402

OUT = pathlib.Path(Path(__file__).resolve().parents[2] / "other info" / "LN orientation")
GUNS = ["C65 Cannon", "T81 Plasma Cannon", "T30 Cannon", "C56 Cannon"]
BIG = (6, 10, 6)
LETTERS = ("A", "B", "C")


def surface_index(sockets: list[dict]) -> list[tuple[int, dict]]:
    """1-based Surface index for every Surface socket, in file order."""
    out = []
    n = 0
    for sock in sockets:
        if sock["type"] != "Surface":
            continue
        n += 1
        out.append((n, sock))
    return out


def main() -> int:
    bf.PARTS.update(bf.wiki_parts())
    made = []
    for section, kind in (("bow", "Bow"), ("core", "Core")):
        for letter in LETTERS:
            triple = ("B", "B", "B")
            idx = 0 if section == "bow" else 1
            triple = tuple(letter if i == idx else "B" for i in range(3))
            sockets = bf.sockets_for("Marauder Line Ship", triple)
            numbered = surface_index(sockets)
            targets = [(n, s) for n, s in numbered if tuple(s["size"]) == BIG]
            if len(targets) != 8:
                print(f"!! {section} {letter}: {len(targets)} big sockets, expected 8 (4 bow + 4 core)")
                continue
            # sockets_for() emits bow first, so targets[0:4] are the bow's and targets[4:8] the core's
            span = slice(0, 4) if section == "bow" else slice(4, 8)
            want = targets[span]
            fills = {}
            for (n, _sock), gun in zip(want, GUNS):
                fills[f"Surface:{n}"] = gun
            name = f"ORI {section} {letter}"
            made.append(
                bf.build(
                    {
                        "hull": "Stock/Bulk Hauler",
                        "name": name,
                        "ship_name": name,
                        "callsign": name,
                        "faction": "Stock/Protectorate",
                        "sections": triple,
                        "fills": fills,
                        "out": str(OUT / f"ORI {section} {letter}.fleet"),
                    }
                )
            )
    print(f"generated {len(made)} fleets in {OUT}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

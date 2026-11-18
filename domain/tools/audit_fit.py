"""Audit fit legality of every fitted socket in a folder of `.fleet` files.

For each ship it looks up the hull's socket table (extracted from the game's asset
bundles), then checks each fitted component against its socket:

* the socket key must exist on that hull,
* the component's category must match the socket type (Surface/Compartment/Module),
* the component's `Dimensions` box must fit inside the socket's `size` box.

The game enforces those three rules at build time, so a healthy extraction should
produce **zero** violations on fleets that were saved by the game itself -- making
this the check that proves the bundle extraction is correct.

    python audit_fit.py "E:\\...\\Nebulous\\Saves\\Fleets"
    python audit_fit.py --limit 40 "E:\\...\\Saves\\Fleets"
"""

from __future__ import annotations

import argparse
import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from fleet_lib import WikiIndex, is_modded, parse_fleet, save_key_name  # noqa: E402
from socket_lib import SocketTables, dims, fits, socket_type_for_section  # noqa: E402


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("path", type=Path, help="a .fleet file or a folder of them")
    parser.add_argument("--limit", type=int, default=0)
    parser.add_argument("--quiet", action="store_true", help="only the tallies")
    parser.add_argument("--examples", type=int, default=8)
    args = parser.parse_args(argv)

    index = WikiIndex()
    tables = SocketTables()
    if not tables.available:
        print(f"socket table missing: {tables.path}", file=sys.stderr)
        return 2

    files = sorted(args.path.rglob("*.fleet")) if args.path.is_dir() else [args.path]
    if args.limit:
        files = files[: args.limit]

    tally = Counter()
    hull_missing: Counter[str] = Counter()
    violations: list[str] = []
    per_hull: Counter[str] = Counter()

    for path in files:
        try:
            fleet = parse_fleet(path)
        except Exception as error:  # noqa: BLE001 - one bad save must not stop the run
            tally["fleet_parse_error"] += 1
            if len(violations) < args.examples:
                violations.append(f"{path.name}: parse error {error}")
            continue
        tally["fleets"] += 1
        for ship in fleet.ships:
            tally["ships"] += 1
            hull = tables.hull(ship.hull_type) or tables.hull_by_keys({s.key for s in ship.sockets})
            if hull is None:
                hull_missing[ship.hull_type] += 1
                tally["hull_unknown"] += 1
                continue
            per_hull[hull.name] += 1
            for socket in ship.sockets:
                tally["sockets"] += 1
                info = hull.get(socket.key)
                if info is None:
                    tally["key_unknown"] += 1
                    if len(violations) < args.examples:
                        violations.append(f"{path.stem} / {ship.name}: socket key {socket.key} not in {hull.name}")
                    continue
                component = index.component(socket.component_name)
                if component is None:
                    tally["mod" if is_modded(socket.component_name) else "component_unknown"] += 1
                    continue
                want_type = socket_type_for_section(component.section)
                if want_type and want_type != info.type:
                    tally["type_mismatch"] += 1
                    if len(violations) < args.examples:
                        violations.append(
                            f"{path.stem} / {ship.name}: {component.name} ({want_type}) in {info.describe()}"
                        )
                    continue
                comp_dims = dims(component.fields.get("Dimensions"))
                if comp_dims and not fits(comp_dims, info.cells):
                    tally["too_large"] += 1
                    if len(violations) < args.examples:
                        violations.append(
                            f"{path.stem} / {ship.name}: {component.name} "
                            f"{'x'.join(map(str, comp_dims))} > {info.describe()}"
                        )
                    continue
                tally["fit_ok"] += 1

    print(f"files={tally['fleets']} ships={tally['ships']} sockets={tally['sockets']}")
    print(f"  fit_ok={tally['fit_ok']} type_mismatch={tally['type_mismatch']} "
          f"too_large={tally['too_large']} key_unknown={tally['key_unknown']}")
    print(f"  component_unknown={tally['component_unknown']} mod={tally['mod']} "
          f"hull_unknown={tally['hull_unknown']} parse_error={tally['fleet_parse_error']}")
    if hull_missing:
        print("  hulls without a socket table:")
        for name, count in hull_missing.most_common(12):
            print(f"    {count:4d}  {name}")
    if not args.quiet and violations:
        print("  examples:")
        for line in violations:
            print(f"    ! {line}")
    if not args.quiet:
        print("  hulls covered (ships):", ", ".join(f"{k} {v}" for k, v in per_hull.most_common(8)))
    return 0 if tally["type_mismatch"] == 0 and tally["too_large"] == 0 and tally["key_unknown"] == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())

"""Recover per-round prices for stock munitions the wiki does not list.

Model: every `<Ship>` stores the game-computed `<Cost>` =
hull + components + magazines + ammunition.  With every part resolved, the
remainder of a ship that carries exactly one unpriced munition *is* that
munition's bill, so such ships pin the price exactly; the rest is a linear
system across the corpus.

Run with repo/.venv python.
"""
from __future__ import annotations

import json
import pathlib
import re
import sys
from collections import defaultdict

import numpy as np

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import fleet_lib as fl  # noqa: E402
import build_layouts as bl  # noqa: E402

DOMAIN = pathlib.Path(__file__).resolve().parents[1]
COSTS = json.loads((DOMAIN / "data" / "ammo_costs.json").read_text("utf-8"))
MAG = COSTS["magazines"]
COST_RE = re.compile(r"Cost \(pts per [^)]*\)\s*:?\s*([0-9.]+)\s*/\s*([0-9.]+)")


def norm(name: str) -> str:
    return re.sub(r"[^a-z0-9]+", "", name.lower())


def short(item: str) -> str:
    return re.sub(r"^(?:\$MODMIS\$|Stock)/", "", item)


def shell_prices() -> dict[str, float]:
    out: dict[str, float] = {}
    for page in (DOMAIN / "kb" / "docs" / "munition").glob("*.md"):
        text = page.read_text("utf-8", errors="replace")
        m = COST_RE.search(text)
        if not m:
            continue
        title = text.splitlines()[0].lstrip("# ").strip()
        out[norm(title)] = float(m.group(1)) / float(m.group(2))
    return out


ALIASES = {"100mm Grapeshot": "100mm Grape", "Flak Round": "50mm Flak Shell"}
NOT_AMMO = ("Decoy Container", "Mine Container", "Container")


def collect() -> tuple[list[tuple[str, str, float, dict[str, float]]], dict[str, int]]:
    idx = fl.WikiIndex()
    fixed = shell_prices()
    rows = []
    counts: dict[str, int] = defaultdict(int)
    skipped_missing = 0
    for path in bl.collect_fleets():
        fleet = fl.parse_fleet(path)
        embedded = {norm(short(k)): v for k, v in fleet.missile_costs.items()}
        for ship in fleet.ships:
            hull = idx.hull(ship.hull_type)
            parts = hull.point_cost if hull else 0.0
            missing = hull is None
            mags: list[str] = []
            ammo: dict[str, int] = defaultdict(int)
            for sock in ship.sockets:
                comp = idx.component(sock.component_name)
                if comp is None:
                    missing = True
                else:
                    parts += comp.cost
                    if "magazine" in comp.name.lower():
                        mags.append(comp.name)
                for entry in sock.ammo:
                    ammo[short(entry.item)] += entry.quantity
            if missing:
                skipped_missing += 1
                continue
            mag_cost = sum(sorted((MAG.get(m, {}).get("next", 0.0) for m in mags), reverse=True)[1:])
            known = 0.0
            unknown: dict[str, float] = defaultdict(float)
            for name, qty in ammo.items():
                if any(tok.lower() in name.lower() for tok in NOT_AMMO):
                    continue
                key = norm(ALIASES.get(name, name))
                if key in embedded:
                    known += embedded[key] * qty
                elif key in fixed:
                    known += fixed[key] * qty
                else:
                    unknown[name] += qty
                    counts[name] += 1
            gap = ship.cost - parts - mag_cost - known
            if unknown:
                rows.append((path.stem, ship.name, gap, dict(unknown)))
    print(f"clean ships with unpriced ammo {len(rows)}   skipped for unresolved parts {skipped_missing}")
    return rows, counts


def main() -> None:
    rows, counts = collect()
    print(f"unknown names {len(counts)}")
    for name, n in sorted(counts.items(), key=lambda kv: -kv[1]):
        print(f"  {n:4d}  {name}")

    print("\n-- ships with exactly one unpriced munition --")
    single: dict[str, list[float]] = defaultdict(list)
    for fleet, ship, gap, unknown in rows:
        if len(unknown) == 1:
            (name, qty), = unknown.items()
            single[name].append(gap / qty)
    for name, values in sorted(single.items(), key=lambda kv: -len(kv[1])):
        uniq = sorted({round(v, 2) for v in values})
        print(f"  {name:28} n={len(values):3d} unit {uniq[:8]}")

    cols = sorted({name for *_, u in rows for name in u})
    index = {name: i for i, name in enumerate(cols)}
    a = np.zeros((len(rows), len(cols)))
    b = np.zeros(len(rows))
    for r, (_, _, gap, u) in enumerate(rows):
        b[r] = gap
        for name, qty in u.items():
            a[r, index[name]] = qty
    p, *_ = np.linalg.lstsq(a, b, rcond=None)
    resid = a @ p - b
    print(f"\nlstsq {len(rows)}x{len(cols)}: median |resid| {np.median(np.abs(resid)):.2f} "
          f"p90 {np.percentile(np.abs(resid), 90):.2f} max {np.abs(resid).max():.1f}")
    for name, value in sorted(zip(cols, p), key=lambda kv: -kv[1]):
        print(f"  {value:8.2f}  {name}")


if __name__ == "__main__":
    main()

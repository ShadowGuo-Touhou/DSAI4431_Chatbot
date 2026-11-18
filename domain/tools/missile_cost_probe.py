"""Inventory the missile templates: which components are unknown-cost, and the body/engine pairs."""

from __future__ import annotations

import json
import xml.etree.ElementTree as ET
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SRC = ROOT / "other info" / "missles"
WIKI = ROOT / "domain" / "kb" / "raw_official" / "munition" / "munitions-missiles.json"

# wiki component prices, keyed by in-game save key name (last path segment)
def wiki_costs() -> dict[str, tuple[float, float]]:
    data = json.loads(WIKI.read_text(encoding="utf-8"))
    out: dict[str, tuple[float, float]] = {}
    for ent in data["entities"]:
        if ent.get("section", "").startswith("Missile Construction") is False:
            continue
        f = ent["fields"]
        base = f.get("Base Cost (pts)") or f.get("Base Cost")
        val = f.get("Validator Cost")
        if base is None:
            continue
        # "Base Cost / Validator Cost: 1 / 0.25" arrives as two fields or one string
        txt = str(base)
        if "/" in txt and val is None:
            parts = [p.strip() for p in txt.split("/")]
            base, val = parts[0], parts[-1]
        out[ent["name"]] = (float(base), float(val) if val is not None else float(base))
    return out


def main() -> int:
    costs = wiki_costs()
    print(f"wiki priced components: {len(costs)}")
    unknown = Counter()
    bodies = Counter()
    rows = []
    for path in sorted(SRC.glob("*.missile")):
        tree = ET.parse(path)
        root = tree.getroot()
        body = root.findtext("BodyKey")
        cost = float(root.findtext("Cost"))
        keys = []
        for sock in root.iter("MissileSocket"):
            comp = sock.find("InstalledComponent")
            if comp is None:
                continue
            key = comp.findtext("ComponentKey") or "?"
            mode = comp.findtext("Mode")
            keys.append((key.split("/")[-1], mode))
        bodies[body] += 1
        total_known = 0.0
        for name, mode in keys:
            if name in costs:
                base, val = costs[name]
                total_known += val if mode == "Validation" else base
            else:
                unknown[name] += 1
        rows.append((path.stem, body, cost, total_known, keys))
    print("\nbodies:", dict(bodies))
    print("\nunknown components:", dict(unknown))
    print("\nper template:")
    for name, body, cost, known, keys in rows:
        print(f"  {name:<34} {str(body):<26} cost={cost:<5g} known={known:<6g} gap={cost - known:g}")
    print("\ncomponents used:")
    for k, v in Counter(k for _, _, _, _, keys in rows for k, _ in keys).most_common():
        print(f"  {k:<48} x{v:<3} {'wiki' if k in costs else 'UNKNOWN'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

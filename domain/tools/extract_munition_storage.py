"""Extract per-round storage volume (m^3) for every munition from the game bundles.

Why this file exists: neither the wiki nor the `.fleet` saves record how much
volume one round takes, so "how many 450mm shells fit in 640 m^3" could not be
answered.  The value lives in `_storageVolume` on the ScriptableObjects
(`LightweightMunitionBase` for shells, the modular-missile base for missiles),
and those prefabs *do* ship typetrees, so UnityPy can read them directly.

Run:  .venv-tools\\Scripts\\python.exe domain\\tools\\extract_munition_storage.py
Out:  domain\\data\\munition_storage.json
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

import UnityPy

BUNDLES = ["stock", "stock-f1", "stock-f2"]
GAME = Path(r"E:\SteamLibrary\steamapps\common\Nebulous")
OUT = Path(__file__).resolve().parent.parent / "data" / "munition_storage.json"

# Names that are VFX / audio helpers, not loadable munitions.
JUNK = re.compile(r"Penetrate|Detonate|Burst|Hit|Ricochet|Launch|Fire|Rock|Impact|Trail", re.I)


def main() -> int:
    rows: dict[str, dict] = {}
    for bundle in BUNDLES:
        path = GAME / "Assets" / "AssetBundles" / bundle
        if not path.exists():
            print(f"missing bundle {path}", file=sys.stderr)
            continue
        env = UnityPy.load(str(path))
        kept = 0
        for obj in env.objects:
            if obj.type.name != "MonoBehaviour":
                continue
            try:
                tree = obj.read_typetree()
            except Exception:
                continue
            volume = tree.get("_storageVolume")
            if volume is None:
                continue
            name = str(tree.get("_munitionName") or tree.get("m_Name") or "").strip()
            if not name or JUNK.search(name):
                continue
            # Newer missiles carry `_munitionKey`; shells carry `_factionKey`.
            rows.setdefault(
                name,
                {
                    "storage_volume_m3": round(float(volume), 6),
                    "point_cost": tree.get("_pointCost"),
                    "point_division": tree.get("_pointDivision"),
                    "faction": str(tree.get("_factionKey") or "").replace("Stock/", ""),
                    "bundle": bundle,
                },
            )
            kept += 1
        print(f"{bundle}: {kept} munitions with _storageVolume")
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(dict(sorted(rows.items())), ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {OUT} ({len(rows)} unique munitions)")
    # Validation anchors supplied by the project owner:
    for probe, expected in (("450mm AP Shell", 0.8), ("250mm AP Shell", 0.15)):
        got = rows.get(probe, {}).get("storage_volume_m3")
        ok = got is not None and abs(got - expected) < 1e-6
        print(f"check {probe}: {got} (expected {expected}) {'OK' if ok else 'MISMATCH'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

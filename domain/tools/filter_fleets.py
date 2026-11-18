"""Filter the fleet library: kept only fleets edited after the 0.6.2.6 update and free of mods."""

from __future__ import annotations

import re
import xml.etree.ElementTree as ET
import json
from collections import Counter
from datetime import datetime
from pathlib import Path

GAME_UPDATE = datetime(2026, 9, 3, 14, 30)  # 0.6.2.6:260903-1430
ROOT = Path(Path(__file__).resolve().parents[2])
SAVES = Path(r"E:\SteamLibrary\steamapps\common\Nebulous\Saves\Fleets")
EXTRA = Path(Path(__file__).resolve().parents[2] / "other info" / "fleets")
MOD_KEY = re.compile(r"^\$MOD(?![A-Z]*\$)|^\$MOD(?!MIS)")


def mod_markers(path: Path) -> list[str]:
    text = path.read_text(encoding="utf-8", errors="replace")
    hits = set()
    for dep in re.findall(r"<ModDependencies>(.*?)</ModDependencies>", text, re.S):
        if dep.strip():
            hits.add("ModDependencies")
    for key in re.findall(r"<ComponentName>([^<]*)</ComponentName>", text):
        if key.startswith("$MOD"):
            hits.add("mod part")
    for key in re.findall(r"<MunitionKey>([^<]*)</MunitionKey>", text):
        if key.startswith("$MOD") and not key.startswith("$MODMIS$"):
            hits.add("mod munition")
    if "<MunitionKey>$MODMIS$" in text:
        hits.add("custom missile")
    return sorted(hits)


def fleet_info(path: Path) -> dict:
    root = ET.parse(path).getroot()
    ships = list(root.iter("Ship"))
    return {
        "name": root.findtext("Name") or path.stem,
        "points": root.findtext("TotalPoints") or "0",
        "declared": sum(int(s.findtext("Cost") or 0) for s in ships),
        "ships": len(ships),
        "faction": (root.findtext("FactionKey") or "?").split("/")[-1],
        "markers": mod_markers(path),
        "mtime": datetime.fromtimestamp(path.stat().st_mtime),
    }


def main() -> int:
    rows = []
    for base in (SAVES, EXTRA):
        if not base.exists():
            print(f"missing: {base}")
            continue
        for path in base.rglob("*.fleet"):
            try:
                info = fleet_info(path)
            except ET.ParseError:
                continue
            info["path"] = path
            info["src"] = "saves" if base == SAVES else "extra"
            rows.append(info)

    print(f"scanned {len(rows)} fleet files")
    fresh = [r for r in rows if r["mtime"] >= GAME_UPDATE]
    print(f"  edited after {GAME_UPDATE:%Y-%m-%d %H:%M}: {len(fresh)}")
    clean = [r for r in fresh if not ({"ModDependencies", "mod part", "mod munition"} & set(r["markers"]))]
    custom = [r for r in clean if "custom missile" in r["markers"]]
    print(f"  of those, no mods: {len(clean)}  (of which use player-made missile templates: {len(custom)})")
    print(f"  dropped for mods among fresh: {len(fresh) - len(clean)}")
    print(f"  dropped for age: {len(rows) - len(fresh)}")
    print()
    unique = {}
    for r in clean:
        unique.setdefault((r["name"], r["points"], r["mtime"].replace(microsecond=0)), r)
    clean = list(unique.values())
    print(f"unique kept fleets: {len(clean)}")
    print(f"{'points':>7}{'ships':>6}  {'faction':<14}{'edited':<17}name")

    for r in sorted(clean, key=lambda x: (x["faction"], -int(x["points"] or 0))):
        flag = " (custom missiles)" if "custom missile" in r["markers"] else ""
        print(f"{r['points']:>7}{r['ships']:>6}  {r['faction']:<14}{r['mtime']:%Y-%m-%d %H:%M}  {r['name']}{flag}")
    print()
    print("marker histogram (all files):", dict(Counter(m for r in rows for m in r["markers"])))
    out = ROOT / "domain" / "data" / "fleets_kept.json"
    out.write_text(
        json.dumps(
            [
                {
                    "name": r["name"],
                    "points": int(r["points"] or 0),
                    "ships": r["ships"],
                    "faction": r["faction"],
                    "edited": r["mtime"].strftime("%Y-%m-%d %H:%M"),
                    "path": str(r["path"]),
                    "custom_missiles": "custom missile" in r["markers"],
                }
                for r in sorted(clean, key=lambda x: (-int(x["points"] or 0), x["name"]))
            ],
            ensure_ascii=False,
            indent=1,
        ),
        encoding="utf-8",
    )
    print(f"written: {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

"""从真实存档里提取「游戏认的」舰体键、部件名、阵营键，供 build_fleet/validate_fleet 使用。

输出 domain/data/game_names.json：
  hulls:      ["Stock/Sprinter Corvette", ...]         # <HullType> 的真实取值
  components: ["Stock/Mk64 Cannon", ...]               # <ComponentName> 的真实取值
  factions:   ["Stock/Alliance", "Stock/Protectorate"] # <FactionKey> 的真实取值
  hull_by_wiki: {"Axford Heavy Cruiser Class": "Stock/Axford Heavy Cruiser", ...}
"""

from __future__ import annotations

import collections
import json
import pathlib
import re
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))

import fleet_lib as fl  # noqa: E402

OUT = pathlib.Path(__file__).resolve().parents[1] / "data" / "game_names.json"
SAVE_ROOTS = [
    pathlib.Path(r"E:\SteamLibrary\steamapps\common\Nebulous\Saves"),
]


def main() -> int:
    hulls: collections.Counter[str] = collections.Counter()
    comps: collections.Counter[str] = collections.Counter()
    facs: collections.Counter[str] = collections.Counter()
    for root in SAVE_ROOTS:
        if not root.exists():
            continue
        for p in root.rglob("*.fleet"):
            try:
                f = fl.parse_fleet(p)
            except Exception:  # noqa: BLE001 - 坏档跳过
                continue
            facs[f.faction] += 1
            for s in f.ships:
                hulls[s.hull_type] += 1
                for sock in s.sockets:
                    if sock.component_name:
                        comps[sock.component_name] += 1
    # 只保留原版（Stock/）键，模组键不进表
    # 有些部件从没被玩家装进过存档（例如 P60 'Grazer' PDT），再从游戏本地化补一遍
    loc = pathlib.Path(
        r"E:\SteamLibrary\steamapps\common\Nebulous\Nebulous_Data\StreamingAssets\Localization\en-US\en_assets.json"
    )
    if loc.exists():
        table = json.loads(loc.read_text(encoding="utf-8"))
        for key, value in table.items():
            if key.startswith("HULLCOMPNAME_") and isinstance(value, str) and value:
                comps.setdefault(f"Stock/{value}", 0)
    # 去掉我早期生成产物里带 " Class" 的错误键
    hull_keys = sorted(k for k in hulls if k.startswith("Stock/") and not k.endswith(" Class"))
    comp_keys = sorted(k for k in comps if k.startswith("Stock/"))
    fac_keys = [k for k in ("Stock/Alliance", "Stock/Protectorate") if k in facs]
    hull_by_wiki = {}
    for key in hull_keys:
        name = key.split("/", 1)[1]
        hull_by_wiki[name] = key
        hull_by_wiki[name + " Class"] = key
    data = {
        "hulls": hull_keys,
        "components": comp_keys,
        "factions": fac_keys,
        "hull_by_wiki": hull_by_wiki,
        "counts": {
            "fleets": sum(facs.values()),
            "hulls": len(hull_keys),
            "components": len(comp_keys),
        },
    }
    OUT.write_text(json.dumps(data, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"wrote {OUT} | hulls={len(hull_keys)} components={len(comp_keys)} factions={fac_keys}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

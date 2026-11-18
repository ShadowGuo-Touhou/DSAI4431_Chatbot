"""收集所有玩家自制导弹的单价。

两个来源：
  * `Saves\\MissileTemplates\\*.missile` —— 玩家在导弹编辑器里存下来的模板；
  * 每条 `.fleet` 里内嵌的 `<MissileTemplates>` —— 有些导弹从没单独存过档，
    只存在于舰队文件里（`build_classes.load_saved_missile_prices` 已覆盖第一种）。

输出 `domain/data/missile_prices.json`：`{弹名: {cost, designation, source}}`，
弹名用存档里的 SaveKey 去掉 `$MODMIS$/` 前缀。

Run with repo/.venv python.
"""

from __future__ import annotations

import json
import re
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "domain" / "tools"))

import build_layouts as bl  # noqa: E402
import fleet_lib as fl  # noqa: E402

DATA = ROOT / "domain" / "data"
SAVES = Path(r"E:\SteamLibrary\steamapps\common\Nebulous\Saves\MissileTemplates")


def short(key: str) -> str:
    return re.sub(r"^\$MODMIS\$/", "", (key or "").strip())


def from_template_file(path: Path) -> dict | None:
    try:
        root = ET.parse(path).getroot()
    except ET.ParseError:
        return None
    cost = root.findtext("Cost")
    if cost is None:
        return None
    key = root.findtext("SaveKey") or path.stem
    nickname = (root.findtext("Nickname") or "").strip()
    designation = (root.findtext("Designation") or "").strip()
    name = short(key)
    if nickname and nickname not in name:
        name = f"{name} {nickname}".strip()
    return {
        "name": name,
        "designation": designation,
        "cost": float(cost),
        "source": f"missile template {path.name}",
    }


def main() -> int:
    prices: dict[str, dict] = {}
    if SAVES.exists():
        for path in sorted(SAVES.glob("*.missile")):
            rec = from_template_file(path)
            if rec:
                prices[rec["name"]] = {k: v for k, v in rec.items() if k != "name"}
    embedded = 0
    for fleet_path in bl.collect_fleets():
        try:
            fleet = fl.parse_fleet(fleet_path)
        except Exception:
            continue
        for key, cost in fleet.missile_costs.items():
            name = short(key)
            if not name or name in prices:
                continue
            prices[name] = {
                "cost": float(cost),
                "designation": (fleet.missile_meta.get(key) or {}).get("designation", ""),
                "source": fleet_path.name,
            }
            embedded += 1
    out = {
        "note": "玩家自制导弹单价：模板存档 + 舰队内嵌模板；cost 单位是点/发",
        "count": len(prices),
        "from_fleets": embedded,
        "prices": dict(sorted(prices.items(), key=lambda kv: kv[0].lower())),
    }
    path = DATA / "missile_prices.json"
    path.write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8")
    costs = sorted({v["cost"] for v in prices.values()})
    print(f"{len(prices)} missiles ({embedded} only in fleets) -> {path}")
    print("cost values:", costs[:20], "…" if len(costs) > 20 else "")
    return 0


if __name__ == "__main__":
    sys.exit(main())

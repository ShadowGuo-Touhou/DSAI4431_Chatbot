"""从存档里反解 EA20 单价，并把舰载机（CraftTemplate）单价抽成 `craft_prices.json`。

- EA20：挑「除了 EA20 之外所有弹药都有价」的船，余数 ÷ 发数 = 单价；没有独占样本时
  把多艘船当方程组一起解（逐船余数必须同号、同量级）。
- 舰载机：舰队根节点 `<CraftTypes><CraftTemplate>` 自带 `<Cost>`，按 `<SaveKey>` 归并。

Run with repo/.venv python.
"""

from __future__ import annotations

import json
import math
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "domain" / "tools"))

import build_layouts as bl  # noqa: E402
import fleet_lib as fl  # noqa: E402

DATA = ROOT / "domain" / "data"
AMMO = DATA / "ammo_costs.json"


def craft_library() -> dict[str, dict]:
    """所有存档舰队里的舰载机模板：SaveKey → {nickname, cost, frame}。"""
    out: dict[str, dict] = {}
    seen = 0
    for path in bl.collect_fleets():
        try:
            root = ET.parse(str(path[0] if isinstance(path, tuple) else path)).getroot()
        except (ET.ParseError, OSError):
            continue
        lib = root.find("CraftTypes")
        if lib is None:
            continue
        for node in lib:
            key = (node.findtext("SaveKey") or "").strip()
            if not key:
                continue
            seen += 1
            cost = node.findtext("Cost")
            out.setdefault(
                key,
                {
                    "nickname": (node.findtext("Nickname") or "").strip(),
                    "cost": float(cost) if cost not in (None, "") else None,
                    "frame": (node.findtext("FrameKey") or "").strip(),
                },
            )
    print(f"craft templates seen {seen}, unique {len(out)}")
    return out


def main() -> int:
    ammo = json.loads(AMMO.read_text(encoding="utf-8"))
    shells = ammo.get("shells") or {}
    decoys = ammo.get("decoys") or {}
    missiles = ammo.get("missiles") or {}

    def price_of(name: str) -> float | None:
        for table in (decoys, missiles, shells):
            if name in table:
                val = table[name]
                return float(val) if isinstance(val, (int, float)) else None
        return None

    idx = fl.WikiIndex()
    rows: list[tuple[str, float, float, list[str]]] = []  # ship, residual, count, other unpriced
    for fleet in bl.collect_fleets():
        path = fleet[0] if isinstance(fleet, tuple) else fleet
        try:
            f = fl.parse_fleet(str(path))
        except Exception:  # noqa: BLE001 - 坏存档跳过
            continue
        for ship in f.ships:
            hull = idx.hull(ship.hull_type) or idx.hull(ship.hull_type.split("/")[-1])
            parts = 0.0
            ok = True
            for sock in ship.sockets:
                comp = idx.component(sock.component_name) if sock.component_name else None
                if sock.component_name and comp is None:
                    ok = False
                    break
                parts += comp.cost if comp else 0.0
            if not ok:
                continue
            mags = 0.0
            ea20 = 0.0
            other_unpriced: list[str] = []
            for sock in ship.sockets:
                for item in sock.ammo:
                    name = item.item.split("/")[-1]
                    qty = float(item.quantity)
                    unit = price_of(name)
                    if unit is None:
                        if "EA20" in name:
                            ea20 += qty
                        else:
                            other_unpriced.append(f"{name}×{qty:.0f}")
                        continue
                    mags += unit * qty
            if ea20 <= 0 or other_unpriced:
                continue
            residual = ship.cost - parts - (hull.point_cost if hull else 0.0) - mags
            rows.append((ship.name, residual, ea20, other_unpriced))

    print(f"\nships carrying EA20 with everything else priced: {len(rows)}")
    est: list[float] = []
    for name, residual, qty, _ in rows[:12]:
        per = residual / qty
        print(f"  {name[:28]:28} residual {residual:7.1f} / {qty:4.0f} = {per:5.2f}")
        if 0 < per < 50:
            est.append(per)
    if est:
        mean = sum(est) / len(est)
        print(f"median-ish estimate: {mean:.2f} (n={len(est)}, range {min(est):.2f}-{max(est):.2f})")

    craft = craft_library()
    priced = {k: v for k, v in craft.items() if v["cost"]}
    (DATA / "craft_prices.json").write_text(
        json.dumps(
            {
                "note": "舰载机单价：存档舰队 <CraftTypes><CraftTemplate><Cost>，按 SaveKey 归并",
                "count": len(priced),
                "seat": priced,
                "unpriced": sorted(k for k, v in craft.items() if not v["cost"]),
            },
            ensure_ascii=False,
            indent=1,
        ),
        encoding="utf-8",
    )
    print(f"craft priced {len(priced)} / {len(craft)} -> domain/data/craft_prices.json")
    by_cost = sorted(((v["cost"], k) for k, v in priced.items()))
    for cost, key in by_cost[:6]:
        print(f"  {cost:5.0f}  {key}")
    return 0


if __name__ == "__main__":
    sys.exit(main())

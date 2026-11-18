"""Classify ships by build type from their fitted loadout, and estimate what the ship costs.

Label = main armament + hull class ("450 CH", "VLS-2 CC", "Mk600 Beam DD"); tags come from
supporting gear. Cost is reported two ways: declared (what the file says the ship cost) and
predicted (hull + components + ammunition priced from the wiki / missile templates).

Nothing here is written into the RAG corpus — this is the review copy.

Outputs:
  domain/data/build_classes.json
  domain/reports/build-classes.md

Usage:
  python domain/tools/build_classes.py --packs
  python domain/tools/build_classes.py --steam
  python domain/tools/build_classes.py --all
"""

from __future__ import annotations

import json
import re
import sys
import xml.etree.ElementTree as ET
from collections import Counter, defaultdict
from dataclasses import dataclass, field
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "domain" / "tools"))

import fleet_lib as fl  # noqa: E402

RAW = ROOT / "domain" / "kb" / "raw_official"
DATA = ROOT / "domain" / "data"
REPORTS = ROOT / "domain" / "reports"
PACKS = ROOT / "other info" / "fleets"
KEPT = DATA / "fleets_kept.json"

WEAPON_SECTIONS = {
    "projectile weapons",
    "energy weapons",
    "spinal weapons",
    "missile launchers",
    "point defense weapons",
}
PD_SECTION = "point defense weapons"
CALIBER = re.compile(r"(\d+)\s*mm")
PER_AMOUNT = re.compile(r"1\s*/\s*(\d+)")

# 游戏内字符串 -> wiki 条目名（wiki 写 E55，游戏写 E57，等等）
ALIASES = {
    "e57 floodlight illuminator": "E55 'Floodlight' Illuminator",
    "mk550 mass driver": "Mk550 Railgun",
    "p11 pdt": "P11 'Aegis' PDT",
    "p20 flak pdt": "P20 'Bastion' PDT",
    "j75 jammer": "J75 'Warbler' Jammer",
    "j15 jammer": "J15 'Prowler' Jammer",
    "l50 laser dazzler": "L50 'Blackjack' Laser Dazzler",
    "r400 radar": "R400 'Stalker' Radar",
    "c4 mount hangar": "Medium Mounted Hangar",
    "c5 mount hangar": "Large Mounted Hangar",
}

ALIASES_NORM = {fl.norm(k): v for k, v in ALIASES.items()}

GUN_FAMILY = {450: "450", 250: "250", 120: "120", 100: "100", 75: "75", 50: "50PD", 30: "30PD", 20: "20PD"}


@dataclass
class Weapon:
    name: str
    section: str
    cost: float
    caliber: int | None = None
    launcher: bool = False
    pd: bool = False


@dataclass
class ShipRecord:
    fleet: str
    fleet_path: str
    faction: str
    ship_name: str
    hull: str
    hull_abbr: str
    declared: float
    hull_cost: float | None
    fitted: float
    ammo: float
    ammo_unknown: int
    predicted: float
    label: str
    main: str
    tags: list[str] = field(default_factory=list)
    weapons: list[dict] = field(default_factory=list)
    unknown: list[str] = field(default_factory=list)


def load_prices() -> dict[str, float]:
    """munition name -> points per unit (shells are 1/N per round)."""
    prices: dict[str, float] = {}
    for path in (RAW / "munition").glob("*.json"):
        page = json.loads(path.read_text(encoding="utf-8"))
        for entity in page.get("entities", []):
            fields = entity.get("fields", {})
            name = fl.norm(entity.get("name") or "")
            per_unit = fl.to_number(fields.get("Cost (pts)"))
            block = next((v for k, v in fields.items() if k.lower().startswith("cost (")), None)
            match = PER_AMOUNT.search(block or "")
            if per_unit is not None and per_unit >= 1:
                prices[name] = per_unit
            elif match:
                prices[name] = 1.0 / int(match.group(1))
    return prices


def load_saved_missile_prices() -> dict[str, float]:
    """`Designation Nickname` -> points, from `Saves\\MissileTemplates\\*.missile`.

    Player-saved missiles are not in the wiki, but every `.missile` file carries the
    in-game `<Cost>`, so a fleet that only stores the name can still be priced.
    """
    out: dict[str, float] = {}
    folder = Path(r"E:\\SteamLibrary\\steamapps\\common\\Nebulous\\Saves\\MissileTemplates")
    if not folder.is_dir():
        return out
    for path in folder.glob("*.missile"):
        try:
            root = ET.parse(path).getroot()
        except (ET.ParseError, OSError):
            continue
        cost = fl.to_number(root.findtext("Cost"))
        if cost is None or cost <= 0:
            continue
        designation = (root.findtext("Designation") or "").strip()
        nickname = (root.findtext("Nickname") or "").strip()
        for key in (f"{designation} {nickname}", nickname, designation):
            if key.strip():
                out.setdefault(fl.norm(key), float(cost))
    return out


def load_civilian_hull_prices() -> dict[str, float]:
    path = ROOT / "domain" / "data" / "civilian_hull_prices.json"
    if not path.exists():
        return {}
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return {}
    return {str(k): float(v) for k, v in (data.get("hulls") or {}).items()}


_CIVILIAN_CACHE: dict[str, float] | None = None


def civilian_hull_prices() -> dict[str, float]:
    global _CIVILIAN_CACHE
    if _CIVILIAN_CACHE is None:
        _CIVILIAN_CACHE = load_civilian_hull_prices()
    return _CIVILIAN_CACHE


def load_missile_costs() -> dict[str, float]:
    path = DATA / "missile_templates.json"
    if not path.exists():
        return {}
    raw = json.loads(path.read_text(encoding="utf-8"))
    items = raw if isinstance(raw, list) else raw.get("templates", [])
    out: dict[str, float] = {}
    for item in items:
        name = item.get("name") or ""
        cost = item.get("cost")
        if name and cost is not None:
            out[fl.norm(name)] = float(cost)
    return out


def ammo_price(item: str, quantity: int, *, prices: dict[str, float], missiles: dict[str, float]) -> tuple[float, bool]:
    name = item.split("/")[-1]
    key = fl.norm(name)
    if key in missiles:
        return missiles[key] * quantity, True
    if key in prices:
        return prices[key] * quantity, True
    for candidate, value in prices.items():
        if candidate and candidate in key:
            return value * quantity, True
    return 0.0, False


def weapon_of(entry: dict) -> Weapon | None:
    section = entry["section"].lower()
    if section not in WEAPON_SECTIONS:
        return None
    fields = entry["fields"]
    ammo = fields.get("Ammo", "") or ""
    match = CALIBER.search(ammo) or CALIBER.search(entry["name"])
    return Weapon(
        name=entry["name"],
        section=entry["section"],
        cost=entry["cost"],
        caliber=int(match.group(1)) if match else None,
        launcher=section == "missile launchers",
        pd=section == PD_SECTION,
    )


def lookup(index, save_key: str):
    component = index.component(save_key)
    if component is not None:
        return component
    alias = ALIASES_NORM.get(fl.norm(fl.save_key_name(save_key)))
    return index.component(alias) if alias else None


def classify_ship(
    fleet: fl.Fleet,
    ship: fl.Ship,
    *,
    index,
    abbr: dict[str, str],
    prices: dict[str, float],
    missiles: dict[str, float],
) -> ShipRecord:
    hull_name = fl.save_key_name(ship.hull_type)
    hull_entry = index.hull(ship.hull_type)
    hull_abbr = (
        abbr.get(hull_name)
        or abbr.get(hull_name.replace(" Class", ""))
        or (abbr.get(hull_entry.name.replace(" Class", "")) if hull_entry else None)
        or (abbr.get(hull_entry.name) if hull_entry else None)
        or ""
    )
    hull_cost = fl.to_number(hull_entry.fields.get("Point Cost")) if hull_entry else None
    if not hull_cost:
        civilian = civilian_hull_prices()
        hull_cost = civilian.get(ship.hull_type.split("/")[-1].replace(" Class", "")) or civilian.get(
            (hull_entry.name.replace(" Class", "") if hull_entry else "")
        )

    weapons: list[Weapon] = []
    fitted = 0.0
    ammo_total = 0.0
    ammo_unknown = 0
    unknown: list[str] = []

    for socket in ship.sockets:
        component = lookup(index, socket.component_name)
        if component is None:
            unknown.append(fl.save_key_name(socket.component_name))
            continue
        entry = {
            "name": component.name,
            "section": component.section.split("›")[-1].strip(),
            "fields": component.fields,
            "cost": fl.to_number(component.fields.get("Cost (pts)")) or 0.0,
        }
        fitted += entry["cost"]
        weapon = weapon_of(entry)
        if weapon:
            weapons.append(weapon)
        for ammo in socket.ammo:
            price, known = ammo_price(ammo.item, ammo.quantity, prices=prices, missiles=missiles)
            ammo_total += price
            if not known:
                ammo_unknown += ammo.quantity

    guns = [w for w in weapons if w.caliber and not w.pd and not w.launcher]
    launchers = [w for w in weapons if w.launcher]
    if guns:
        by_caliber: dict[int, list[Weapon]] = defaultdict(list)
        for gun in guns:
            by_caliber[gun.caliber].append(gun)
        caliber, group = max(by_caliber.items(), key=lambda kv: (len(kv[1]), sum(w.cost for w in kv[1])))
        main = f"{GUN_FAMILY.get(caliber, str(caliber))}mm ×{len(group)}（{int(sum(w.cost for w in group))} 点）"
        label_weapon = GUN_FAMILY.get(caliber, str(caliber))
    elif launchers:
        best = max(launchers, key=lambda w: w.cost)
        count = sum(1 for w in launchers if w.name == best.name)
        main = f"{best.name} ×{count}（{int(best.cost * count)} 点）"
        label_weapon = re.sub(r"\s*Launcher$", "", best.name).strip()
    elif weapons:
        best = max(weapons, key=lambda w: w.cost)
        main = f"{best.name}（{int(best.cost)} 点）"
        label_weapon = re.sub(r"\s*(Cannon|PDT|Turret|Dazzler|Jammer)$", "", best.name).strip()
    else:
        main = ""
        label_weapon = "unarmed"

    tag_hull = hull_abbr or (hull_name.split()[0] if hull_name else "")
    label = f"{label_weapon} {tag_hull}".strip()

    names = [fl.save_key_name(socket.component_name) for socket in ship.sockets]
    pd_count = sum(1 for weapon in weapons if weapon.pd)
    ewar = sum(1 for name in names if re.search(r"Jammer|Dazzler|Blanket|Interruption|Masquerade|Floodlight|Spotlight", name))
    air = sum(1 for name in names if re.search(r"VLS-1|Chaff|Flare|Decoy|Aurora|Stonewall|Rebound|Defender|Sarissa|Pavise|PDT", name))
    hangar = any(re.search(r"Hangar|Flight", name) for name in names)
    radar = any(re.search(r"Radar|EWR|LRT|Spyglass|Parallax|Bullseye|Scryer|Antenna", name) for name in names)
    support = any(re.search(r"Workshop|Replenishment|Cargo|Berthing", name) for name in names)

    tags: list[str] = []
    if hangar:
        tags.append("carrier")
    if pd_count >= 2 or air >= 3:
        tags.append("air-defence")
    if ewar >= 2:
        tags.append("softkill")
    if any("EWR" in name or "LRT" in name for name in names):
        tags.append("picket")
    elif radar and hull_abbr in {"FFL", "FF"}:
        tags.append("scout")
    if support:
        tags.append("support")
    if hull_abbr == "FFL" and (ship.cost or 0) <= 320 and not any((w.caliber or 0) >= 250 for w in weapons):
        tags.append("cap")
    if any((w.caliber or 0) >= 450 for w in weapons):
        tags.append("line")

    predicted = (hull_cost or 0.0) + fitted + ammo_total
    return ShipRecord(
        fleet=fleet.name,
        fleet_path=str(fleet.path),
        faction=fleet.faction,
        ship_name=ship.name,
        hull=hull_name,
        hull_abbr=hull_abbr,
        declared=ship.cost,
        hull_cost=hull_cost,
        fitted=round(fitted, 2),
        ammo=round(ammo_total, 2),
        ammo_unknown=ammo_unknown,
        predicted=round(predicted, 2),
        label=label,
        main=main,
        tags=tags,
        weapons=[
            {"name": w.name, "section": w.section, "cost": w.cost, "caliber": w.caliber, "launcher": w.launcher, "pd": w.pd}
            for w in weapons
        ],
        unknown=unknown,
    )


def collect(paths: list[Path], **kwargs) -> list[ShipRecord]:
    out: list[ShipRecord] = []
    for path in paths:
        try:
            fleet = fl.parse_fleet(path)
        except Exception as exc:  # noqa: BLE001 - one bad file must not stop the run
            print(f"  !! {path.name}: {exc}", file=sys.stderr)
            continue
        for ship in fleet.ships:
            out.append(classify_ship(fleet, ship, **kwargs))
    return out


def pack_paths() -> list[Path]:
    return sorted(PACKS.rglob("*.fleet"))


def steam_paths() -> list[Path]:
    if not KEPT.exists():
        return []
    kept = json.loads(KEPT.read_text(encoding="utf-8"))
    if isinstance(kept, dict):
        kept = kept.get("kept") or kept.get("fleets") or []
    return [Path(item["path"]) for item in kept]


def report(records: list[ShipRecord], *, title: str) -> str:
    lines = [f"# {title}", ""]
    lines.append(f"共 {len({r.fleet_path for r in records})} 个舰队文件、{len(records)} 艘船。")
    lines.append("")

    errors = sorted(abs(r.predicted - r.declared) for r in records if r.declared)
    exact = sum(1 for r in records if r.declared and abs(r.predicted - r.declared) < 1)
    if errors:
        lines.append(
            f"成本模型校验：精确命中 {exact}/{len(records)}，中位偏差 {errors[len(errors) // 2]:.0f} 点（以 declared 为准）。"
        )
        lines.append("")

    groups: dict[str, list[ShipRecord]] = defaultdict(list)
    for record in records:
        groups[record.label].append(record)

    lines.append("## 构建类型汇总")
    lines.append("")
    lines.append("| 构建 | 船数 | 舰体 | 实际点数（min / 中位 / max） | 舰体点数 | 舰体占比 | 主武器 | 标签 |")
    lines.append("|---|---|---|---|---|---|---|---|")
    for label, group in sorted(groups.items(), key=lambda kv: (-len(kv[1]), kv[0])):
        costs = sorted(r.declared for r in group if r.declared)
        hulls = sorted(r.hull_cost for r in group if r.hull_cost is not None)
        hulls_counter = Counter(r.hull_abbr or r.hull.split()[0] for r in group)
        mid = costs[len(costs) // 2] if costs else 0
        hull_mid = hulls[len(hulls) // 2] if hulls else 0
        share = f"{hull_mid / mid:.0%}" if mid else "-"
        lines.append(
            "| {label} | {n} | {hull} | {lo:.0f} / {mid:.0f} / {hi:.0f} | {hullcost:.0f} | {share} | {main} | {tags} |".format(
                label=label,
                n=len(group),
                hull="、".join(f"{k}×{v}" for k, v in hulls_counter.most_common(3)),
                lo=costs[0] if costs else 0,
                mid=mid,
                hi=costs[-1] if costs else 0,
                hullcost=hull_mid,
                share=share,
                main=group[0].main.split("（")[0],
                tags="、".join(tag for tag, _ in Counter(t for r in group for t in r.tags).most_common(4)) or "-",
            )
        )

    lines.append("")
    lines.append("## 逐船明细")
    by_fleet: dict[str, list[ShipRecord]] = defaultdict(list)
    for record in records:
        by_fleet[record.fleet].append(record)
    for fleet_name, ships in sorted(by_fleet.items()):
        lines.append("")
        lines.append(f"### {fleet_name}")
        lines.append("")
        lines.append("| 舰名 | 构建 | 舰体 | 实际点数 | 舰体+部件+弹药 | 标签 |")
        lines.append("|---|---|---|---|---|---|")
        for ship in ships:
            lines.append(
                "| {name} | {label} | {hull} | {declared:.0f} | {predicted:.0f} | {tags} |".format(
                    name=ship.ship_name,
                    label=ship.label,
                    hull=ship.hull,
                    declared=ship.declared,
                    predicted=ship.predicted,
                    tags="、".join(ship.tags) or "-",
                )
            )
    return "\n".join(lines)


def main(argv: list[str]) -> int:
    mode = "--all"
    for arg in argv[1:]:
        if arg in {"--packs", "--steam", "--all"}:
            mode = arg

    index = fl.WikiIndex()
    raw_abbr = json.loads((DATA / "hull_abbr.json").read_text(encoding="utf-8"))
    abbr = {k: v["abbr"] for k, v in raw_abbr.items() if isinstance(v, dict) and v.get("abbr")}
    prices = load_prices()
    missiles = load_missile_costs()

    records: list[ShipRecord] = []
    if mode in {"--packs", "--all"}:
        packs = collect(pack_paths(), index=index, abbr=abbr, prices=prices, missiles=missiles)
        print(f"packs: {len(packs)} ships / {len(pack_paths())} fleets")
        records.extend(packs)
    if mode in {"--steam", "--all"}:
        steam = collect(steam_paths(), index=index, abbr=abbr, prices=prices, missiles=missiles)
        print(f"steam: {len(steam)} ships / {len(steam_paths())} fleets")
        records.extend(steam)

    DATA.mkdir(parents=True, exist_ok=True)
    REPORTS.mkdir(parents=True, exist_ok=True)
    (DATA / "build_classes.json").write_text(
        json.dumps({"ships": [r.__dict__ for r in records]}, ensure_ascii=False, indent=1), encoding="utf-8"
    )

    title = {
        "--packs": "构建类型识别：攻略与起始舰队",
        "--steam": "构建类型识别：筛选后的玩家舰队",
        "--all": "构建类型识别：全部",
    }[mode]
    out = REPORTS / "build-classes.md"
    out.write_text(report(records, title=title), encoding="utf-8")
    print(f"records: {len(records)} -> {out}")

    unknown = Counter(name for record in records for name in record.unknown)
    if unknown:
        print("unmatched components:", ", ".join(f"{k}×{v}" for k, v in unknown.most_common(10)))
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))

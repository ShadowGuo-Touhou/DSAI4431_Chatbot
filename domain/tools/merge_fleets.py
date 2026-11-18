"""把 `sample fleets/` 里的每一次样板船合进一个「全样板船」舰队。

用途：配合无船数上限的 mod，一次看/改所有样板船。
按阵营分开（Alliance / Protectorate）—— 存档的 `<FactionKey>` 是舰队级的，
两个阵营的部件混在一条舰队里加载会被游戏踢掉。

Run with repo/.venv python.
"""

from __future__ import annotations

import sys
import uuid
import xml.etree.ElementTree as ET
from pathlib import Path

import fleet_templates

ROOT = Path(__file__).resolve().parents[2]
SRC = ROOT / "sample fleets"
OUT = ROOT / "sample fleets" / "_all"

XSI = "http://www.w3.org/2001/XMLSchema-instance"
XSD = "http://www.w3.org/2001/XMLSchema"
ET.register_namespace("xsi", XSI)
ET.register_namespace("xsd", XSD)


def collect() -> dict[str, list[tuple[Path, ET.Element]]]:
    groups: dict[str, list[tuple[Path, ET.Element]]] = {}
    for path in sorted(SRC.glob("*.fleet")):
        root = ET.parse(path).getroot()
        faction = (root.findtext("FactionKey") or "Stock/Alliance").strip()
        for ship in root.findall("Ships/Ship"):
            groups.setdefault(faction, []).append((path, ship))
    return groups


def build(faction: str, items: list[tuple[Path, ET.Element]]) -> tuple[ET.Element, float]:
    root = ET.Element("Fleet")
    label = "Alliance" if faction.endswith("Alliance") else "Protectorate"
    total = 0.0
    ET.SubElement(root, "Name").text = f"All {len(items)} sample ships · {label}"
    ET.SubElement(root, "Version").text = "3"
    points = ET.SubElement(root, "TotalPoints")
    ET.SubElement(root, "FactionKey").text = faction
    ET.SubElement(root, "Description").text = (
        f"每条样板船原样复制自 sample fleets/，共 {len(items)} 艘。"
        "需要「无船数上限」mod 才能载入。"
    )
    ships = ET.SubElement(root, "Ships")
    remap: dict[str, str] = {}
    for index, (path, node) in enumerate(items, start=1):
        ship = ET.fromstring(ET.tostring(node))
        old = (ship.findtext("Key") or "").strip()
        key = ship.find("Key")
        if key is not None:
            key.text = new_key = str(uuid.uuid4())
            if old:
                remap[old] = new_key
        number = ship.find("Number")
        if number is not None:
            number.text = str(index)
        total += float(ship.findtext("Cost") or 0)
        ships.append(ship)
    # `<InitialFormation><GuideKey>` 指向编队向导船的 `<Key>`；换 Key 后必须一起换，
    # 否则游戏报 `Fleet is missing guide with GUID …`，那艘船「start independently」。
    for ship in ships:
        guide = ship.find("InitialFormation/GuideKey")
        if guide is None:
            continue
        old_guide = (guide.text or "").strip()
        guide.text = remap.get(old_guide, (ship.findtext("Key") or "").strip())
    # 每条样板船自带的导弹 / 舰载机模板库（按 TemplateKey 去重）—— 缺了游戏会报
    # `Fleet is missing guide with GUID …`，船上的导弹和飞机就不加载。
    fleet_templates.emit(root, fleet_templates.gather(p for p, _ in items))
    # 「无船数上限」mod 的依赖号：游戏自己存盘时会写，手工拼的舰队也写上，
    # 免得 34 艘的舰队在没有 mod 的环境里被拒。
    mods: set[str] = set()
    for path, _ in items:
        try:
            dep = ET.parse(path).getroot().find("ModDependencies")
        except (ET.ParseError, OSError):
            continue
        if dep is not None:
            mods |= {(n.text or "").strip() for n in dep if (n.text or "").strip()}
    if mods:
        dep = ET.SubElement(root, "ModDependencies")
        for mod in sorted(mods):
            ET.SubElement(dep, "unsignedLong").text = mod
    points.text = f"{total:.0f}"
    return root, total


def write(root: ET.Element, out: Path) -> None:
    ET.indent(root, space="  ")
    body = ET.tostring(root, encoding="unicode")
    body = body.replace("<Fleet>", f'<Fleet xmlns:xsd="{XSD}" xmlns:xsi="{XSI}">', 1)
    out.write_text('<?xml version="1.0" encoding="UTF-8"?>\n' + body, encoding="utf-8")


def main() -> None:
    OUT.mkdir(exist_ok=True)
    groups = collect()
    for faction, items in sorted(groups.items()):
        root, total = build(faction, items)
        name = "all-samples-alliance" if faction.endswith("Alliance") else "all-samples-protectorate"
        path = OUT / f"{name}.fleet"
        write(root, path)
        print(f"{path.name}: {len(items)} ships, {total:.0f} pts")


if __name__ == "__main__":
    sys.exit(main())

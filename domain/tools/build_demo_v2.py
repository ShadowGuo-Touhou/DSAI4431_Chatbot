"""按舰级预设生成合法 .fleet（含弹药/弹库的 ComponentData，价格按游戏规则估算）。

与 demo_fleet_3000.py 的区别：
  1. 只允许该舰级该有的角色（禁 MPB、舰载机支援、第二个内部雷达、工程模块等）；
  2. 弹库/发射器直接从真实舰队里克隆 <ComponentData>，所以不会是空壳；
  3. 弹库按 wiki 规则计价："最贵的那个免费，其余照价"。

用法:
  python domain/tools/build_demo_v2.py CH 2 3000 "Two 450 CH (v2)" --out "other info/chatbot output/Two 450 CH (v2).fleet"
  python domain/tools/build_demo_v2.py SPRINTER 10 3000 "Ten Gun Sprinters (v2)" --out "..."
"""

from __future__ import annotations

import argparse
import pathlib
import re
import sys
import xml.sax.saxutils as sx

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))

import fleet_lib as fl  # noqa: E402
import build_fleet as bf  # noqa: E402

SAVE_ROOTS = [pathlib.Path(r"E:/SteamLibrary/steamapps/common/Nebulous/Saves/Fleets")]
NAME = re.compile(r"<ComponentName>(.*?)</ComponentName>")
DATA = re.compile(r"<ComponentName>(.*?)</ComponentName>\s*(<ComponentData\b.*?</ComponentData>)", re.S)

HULL = {
    "CH": {"wiki": "Axford Heavy Cruiser", "key": "Stock/Axford Heavy Cruiser", "faction": "Stock/Protectorate"},
    "SPRINTER": {"wiki": "Sprinter Corvette", "key": "Stock/Sprinter Corvette", "faction": "Stock/Alliance"},
}

# 大挂载位（6x10x6）优先按这个顺序装；后面几位是备用
BIG = {
    "CH": [
        "Mk66 Cannon", "Mk66 Cannon", "Mk68 Cannon",
        "VLS-1-46 Launcher", "VLS-1-46 Launcher",
        "Mk20 'Defender' PDT", "Mk20 'Defender' PDT", "P20 'Bastion' PDT",
        "T30 Cannon", "T30 Cannon", "Mk20 'Defender' PDT", "P20 'Bastion' PDT",
        "L50 Laser Dazzler", "E57 'Floodlight' Illuminator",
    ],
    "SPRINTER": [
        "Mk64 Cannon", "Mk64 Cannon", "Mk62 Cannon", "Mk62 Cannon",
        "Mk20 'Defender' PDT", "Mk20 'Defender' PDT", "VLS-1-23 Launcher",
    ],
}
COMPARTMENT = {
    "CH": ["Reinforced CIC", "Citadel Magazine", "Reinforced Magazine", "Bulk Magazine",
           "Large DC Locker", "Large DC Locker", "Small DC Locker", "Rapid DC Locker",
           "Rapid DC Locker", "Damage Control Complex", "Large DC Storage", "Small DC Locker"],
    "SPRINTER": ["Basic CIC", "Reinforced Magazine", "Small DC Locker", "Rapid DC Locker", "Bulk Magazine"],
}
MODULE = {
    "CH": ["RM50 'Parallax' Radar", "Boosted Reactor", "Boosted Reactor", "Light Civilian Reactor",
           "CHI-7700 Drive", "Gun Plotting Center", "Plant Control Center", "Ammunition Elevators",
           "Auxiliary Steering", "Mount Gyros", "Light Civilian Reactor", "Energy Regulator",
           "FR3300 Micro Reactor", "Mount Gyros"],
    "SPRINTER": ["FR3300 Micro Reactor", "FM200 Drive", "RS35 'Frontline' Radar", "Ammunition Elevators",
                 "Auxiliary Steering", "FM200 Drive", "FR3300 Micro Reactor"],
}
FORBIDDEN = re.compile(
    r"missile programming|parallel interface|missile id|mounted hangar|internal hangar|craft|spacecraft|"
    r"strikedown|repair station|analysis annex|intelligence|signature scrambler|elint|datalink|"
    r"targeting uplink|battle dressing|launcher deluge|mine|torpedo",
    re.I,
)


def load_donors() -> dict[str, str]:
    """部件名 -> 真实舰队里的 <ComponentData> 片段（弹库/发射器/弹药都靠它）。"""
    out: dict[str, str] = {}
    for root in SAVE_ROOTS:
        for path in root.rglob("*.fleet"):
            try:
                text = path.read_text(encoding="utf-8", errors="ignore")
            except OSError:
                continue
            for name, block in DATA.findall(text):
                key = name.strip().replace("Stock/", "")
                if key and key not in out:
                    out[key] = block.strip()
    return out


def socket_volume(dims: list[int]) -> int:
    return dims[0] * dims[1] * dims[2]


def pick_socket(sockets: list[dict], dims: list[int], used: set[int]) -> dict | None:
    for socket in sockets:
        index = id(socket)
        if index in used:
            continue
        if bf.fits(dims, socket["size"]):
            used.add(index)
            return socket
    return None


def price(parts: list[dict]) -> tuple[int, int]:
    """返回 (部件点数, 弹库点数)。弹库规则：最贵的免费，其余按 wiki 价。"""
    mags = [p for p in parts if "magazine" in p["name"].lower()]
    rest = sum(p["cost"] for p in parts if p not in mags)
    mags.sort(key=lambda p: -p["cost"])
    mag_cost = sum(p["cost"] for p in mags[1:])
    return rest + mag_cost, mag_cost


def fit_ship(kind: str, donors: dict[str, str], index: int) -> tuple[list[dict], list[dict], list[str]]:
    """按槽位顺序逐个装：大挂载位用 BIG 队列，舱室/模块各用各的队列，装不下就留空。"""
    hull = HULL[kind]
    if not bf.PARTS:
        bf.PARTS.update(bf.wiki_parts())
    sockets = bf.sockets_for(hull["wiki"], None)
    queues = {
        "Surface": [(name, bf.part(name)) for name in BIG[kind]],
        "Compartment": [(name, bf.part(name)) for name in COMPARTMENT[kind]],
        "Module": [(name, bf.part(name)) for name in MODULE[kind]],
    }
    mounted: list[dict] = []
    notes: list[str] = []
    for socket in sorted(sockets, key=lambda s: -socket_volume(s["size"])):
        kind_of_socket = socket.get("type", "Surface")
        queue = queues.get(kind_of_socket, [])
        for position, (name, part) in enumerate(queue):
            if part is None or FORBIDDEN.search(name):
                continue
            if bf.fits(part["dims"], socket["size"]):
                mounted.append({"name": name, "socket": socket, "cost": part["cost"]})
                queue.pop(position)
                break
    missing = len(sockets) - len(mounted)
    if missing:
        notes.append(f"{missing} 个槽位空着（队列里没有装得下的部件）")
    return mounted, sockets, notes


def ship_xml(kind: str, mounted: list[dict], donors: dict[str, str], name: str, number: int,
             hull_cost: int) -> str:
    hull = HULL[kind]
    total = hull_cost + sum(item["cost"] for item in mounted)
    lines = [
        "    <Ship>",
        '      <SaveID xsi:nil="true" />',
        f"      <Key>{number:08d}-0000-4000-8000-00000000{number:04d}</Key>",
        f"      <Name>{sx.escape(name)}</Name>",
        f"      <Cost>{total}</Cost>",
        "      <Callsign />",
        f"      <Number>{number}</Number>",
        "      <SymbolOption>0</SymbolOption>",
        f"      <HullType>{hull['key']}</HullType>",
        "      <SocketMap>",
    ]
    for item in mounted:
        socket = item["socket"]
        lines.append("        <HullSocket>")
        lines.append(f"          <Key>{socket['key']}</Key>")
        lines.append(f"          <ComponentName>{bf.part_key(item['name'])}</ComponentName>")
        block = donors.get(item["name"])
        if block:
            lines.append("          " + block.replace("\n", "\n          ").strip())
        lines.append("        </HullSocket>")
    lines += [
        "      </SocketMap>",
        "      <WeaponGroups />",
        "      <TemplateMissileTypes />",
        "      <TemplateSpacecraftTypes />",
        "    </Ship>",
    ]
    return "\n".join(lines)


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("kind", choices=sorted(HULL))
    parser.add_argument("count", type=int)
    parser.add_argument("total", type=float)
    parser.add_argument("name")
    parser.add_argument("--out", required=True)
    parser.add_argument("--per-ship", type=float, default=None)
    args = parser.parse_args(argv)

    donors = load_donors()
    hull_cost = 600 if args.kind == "CH" else 75
    per_ship = args.per_ship or args.total / args.count

    mounted, sockets, notes = fit_ship(args.kind, donors, 0)
    parts_cost, mag_cost = price(mounted)
    estimate = hull_cost + parts_cost
    junk = [item["name"] for item in mounted if FORBIDDEN.search(item["name"])]
    print(f"每舰估算 {estimate} 点（舰体 {hull_cost} + 部件 {parts_cost}，其中弹库 {mag_cost}）；目标 {per_ship:.0f}")
    print(f"装了 {len(mounted)} 件 / 共 {len(sockets)} 槽；含弹药数据的部件 "
          f"{sum(1 for i in mounted if i['name'] in donors)} 个；违禁件 {len(junk)}")
    for note in notes:
        print("  备注:", note)

    ships = [ship_xml(args.kind, mounted, donors, f"{args.name} {i + 1}", 700 + i, hull_cost)
             for i in range(args.count)]
    xml = (
        '<?xml version="1.0" encoding="utf-8"?>\n'
        '<Fleet xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" '
        'xmlns:xsd="http://www.w3.org/2001/XMLSchema">\n'
        f"  <Name>{sx.escape(args.name)}</Name>\n"
        "  <Version>3</Version>\n"
        f"  <TotalPoints>{round(estimate * args.count)}</TotalPoints>\n"
        f"  <FactionKey>{HULL[args.kind]['faction']}</FactionKey>\n"
        "  <Description />\n"
        "  <ModDependencies />\n"
        "  <Ships>\n" + "\n".join(ships) + "\n  </Ships>\n"
        "  <MissileTypes />\n"
        "  <CraftTypes />\n"
        "</Fleet>\n"
    )
    out = pathlib.Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(xml, encoding="utf-8")
    print("wrote", out, "ships=", args.count, "total=", round(estimate * args.count))
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))

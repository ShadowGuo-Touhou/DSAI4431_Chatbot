"""Generate hybrid LN test fleets so the user can read mount directions.

Valid OSP-only loadout, every part fits its socket box:
  6x10x6 mount -> C65 Cannon (450mm)   3x4x3 mount -> RL18 Launcher   2x2x2 mount -> P20 'Bastion' PDT
  compartment  -> Basic CIC (once)     module 3x3x3 -> Light Civilian Reactor
  module 6x6x6 -> Boosted Reactor      module 12x12x12 -> BW1500 Drive
"""

from __future__ import annotations

import json
import pathlib
import re

ROOT = pathlib.Path(Path(__file__).resolve().parents[2])
DONOR = pathlib.Path(
    r"E:\SteamLibrary\steamapps\common\Nebulous\Saves\Fleets\Custom Protectorate\Azur Lame.fleet"
)
OUT = ROOT / "other info" / "LN test fleets"
SOCKETS = json.loads((ROOT / "domain" / "data" / "hull_sockets.json").read_text(encoding="utf-8"))

BOW = {"A": "38e7a28f-1b06-4b73-98ee-f03d1d8a81fe", "B": "29eb9c63-6c47-40f2-8f46-4ed4da8d3386", "C": "c534a876-3f8a-4315-a194-5dda0f84c2b3"}
CORE = {"A": "d4c9a66d-81e6-49ee-9b33-82d7a1522bbf", "B": "e2c11e02-b770-495e-a3c2-3dc998eac5a6", "C": "429f178e-e369-4f51-8054-2e01dd0abea1"}
STERN = {"A": "78d72a9a-893c-41c6-bddd-f198dfcf77ee", "B": "2f2b451c-4776-405c-9914-cad4764f1072", "C": "a8bf77b9-b7e3-4498-bf91-d3e777a7f688"}

MOUNTS = [
    ((6, 10, 6), "Stock/C65 Cannon", 40),
    ((3, 2, 3), "Stock/RL18 Launcher", 30),
    ((2, 1, 2), "Stock/P20 'Bastion' PDT", 15),
]
MODULES = [
    ((12, 12, 12), "Stock/BW1500 Drive", 10),
    ((6, 6, 6), "Stock/Boosted Reactor", 10),
    ((3, 3, 3), "Stock/Light Civilian Reactor", 10),
]
# Dressing ints per section piece, taken from NLHC catalog.json dressingPoints
# (index, allowEmpty, variants) -- one int per dressing point, first variant id.
DRESSING = {
    "BowA": [24, 35, 46],
    "BowB": [23, 35, 43],
    "BowC": [23, 27],
    "CoreA": [14, 22, 30, 35],
    "CoreB": [14, 31, 42, 57, 61],
    "CoreC": [14, 44, 55],
    "SternA": [],
    "SternB": [],
    "SternC": [],
}

SHIP = """    <Ship>
      <Key>{key}</Key>
      <Name>{name}</Name>
      <Cost>{cost}</Cost>
      <Callsign>{callsign}</Callsign>
      <Number>{number}</Number>
      <SymbolOption>0</SymbolOption>
      <HullType>Stock/Bulk Hauler</HullType>
      <HullConfig xsi:type="RandomHullConfiguration">
        <PrimaryStructure>
{segments}
        </PrimaryStructure>
        <SecondaryStructure />
        <HullTint>
          <r>0.62</r>
          <g>0.62</g>
          <b>0.62</b>
          <a>1</a>
        </HullTint>
        <TextureVariation>
          <x>0</x>
          <y>0</y>
          <z>0</z>
        </TextureVariation>
      </HullConfig>
      <ModDependencies />
      <SocketMap>
{sockets}
      </SocketMap>
      <WeaponGroups />
      <TemplateMissileTypes />
      <TemplateSpacecraftTypes />
    </Ship>"""


def pick(size: list[int], table) -> tuple[str, int] | None:
    for dims, comp, cost in table:
        if all(size[i] >= dims[i] for i in range(3)):
            return comp, cost
    return None


def dressing_block(kind: str, letter: str) -> str:
    vals = DRESSING.get(f"{kind}{letter}") or []
    if not vals:
        return "            <Dressing />"
    body = "\n".join(f"              <int>{v}</int>" for v in vals)
    return f"            <Dressing>\n{body}\n            </Dressing>"


def build(bow: str, core: str, stern: str, index: int) -> pathlib.Path:
    label = f"{bow}{core}{stern}"
    segs = [
        "          <SegmentConfiguration>\n"
        f"            <Key>{guid}</Key>\n"
        f"{dressing_block(kind, letter)}\n"
        "          </SegmentConfiguration>"
        for kind, letter, guid in [
            ("Bow", bow, BOW[bow]),
            ("Core", core, CORE[core]),
            ("Stern", stern, STERN[stern]),
        ]
    ]
    lines = []
    cost = 5  # 弹药占位
    used_cic = used_drive = False
    for sec in (f"Bulk - {bow} - Bow", f"Bulk - {core} - Core", f"Bulk - {stern} - Stern"):
        for s in SOCKETS[sec]["sockets"]:
            comp = cost_add = None
            if s["type"] == "Surface":
                got = pick(s["size"], MOUNTS)
                if got is None:
                    continue
                comp, cost_add = got
            elif s["type"] == "Compartment" and not used_cic:
                comp, cost_add, used_cic = "Stock/Basic CIC", 10, True
            elif s["type"] == "Module":
                got = pick(s["size"], MODULES)
                if got is None:
                    continue
                comp, cost_add = got
                if "Drive" in comp:
                    if used_drive:
                        continue
                    used_drive = True
            if not comp:
                continue
            cost += cost_add
            lines.append(
                "        <HullSocket>\n"
                f"          <Key>{s['key']}</Key>\n"
                f"          <ComponentName>{comp}</ComponentName>\n"
                "        </HullSocket>"
            )
    body = SHIP.format(
        key=f"00000000-0000-4000-8000-{index:012d}",
        name=f"LN hybrid {label}",
        cost=cost,
        callsign=f"BOW {bow} CORE {core} STERN {stern}",
        number=100 + index,
        segments="\n".join(segs),
        sockets="\n".join(lines),
    )
    text = DONOR.read_text(encoding="utf-8", errors="ignore")
    head_i = text.find("<Ships>") + len("<Ships>")
    tail_i = text.find("</Ships>")
    head = text[:head_i]
    tail = text[tail_i:]
    head = re.sub(r"<Name>[^<]*</Name>", f"<Name>LN hybrid {label}</Name>", head, count=1)
    head = re.sub(r"<TotalPoints>\d+</TotalPoints>", f"<TotalPoints>{cost}</TotalPoints>", head, count=1)
    out = OUT / f"LN {label}.fleet"
    out.write_text(head + "\n" + body + "\n  " + tail, encoding="utf-8")
    return out


def main() -> int:
    OUT.mkdir(parents=True, exist_ok=True)
    made = []
    n = 1
    for b in "ABC":
        made.append(build(b, "B", "B", n)); n += 1
    for c in "AC":
        made.append(build("B", c, "B", n)); n += 1
    for s in "AC":
        made.append(build("B", "B", s, n)); n += 1
    for p in made:
        print(p.name)
    print("total", len(made))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

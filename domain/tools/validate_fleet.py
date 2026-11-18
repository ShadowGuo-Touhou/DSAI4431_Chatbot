"""Check a .fleet against the hard rules: structure, socket box size and faction.

Rules implemented (see domain/kb/manual_zh/fleet文件结构与校验.md):
  * <HullConfig> for a random hull must carry exactly 3 <SegmentConfiguration>.
  * <SecondaryStructure> must be present as an element (empty = no bridge);
    omitting it makes SecondaryStructure null and crashes the load
    (Nebulous.decompiled.cs 69582).
  * every <HullSocket><Key> must exist on the assembled hull.
  * component volume must not exceed the socket volume; faction must match.

Usage: validate_fleet.py <fleet|dir> [<fleet|dir> ...]
"""

from __future__ import annotations

import json
import pathlib
import re
import sys
import xml.etree.ElementTree as ET

ROOT = pathlib.Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "domain" / "tools"))

import fleet_lib as fl  # noqa: E402
import hulls as hu  # noqa: E402

DIMS = re.compile(r"(\d+)\s*x\s*(\d+)\s*x\s*(\d+)")


def load_dims(idx: fl.WikiIndex) -> dict[str, tuple[int, int, int]]:
    out = {}
    for p in (ROOT / "domain" / "kb" / "raw_official").rglob("*.json"):
        d = json.loads(p.read_text(encoding="utf-8"))
        for e in d.get("entities", []):
            m = DIMS.search(str(e.get("fields", {}).get("Dimensions") or ""))
            if m:
                out[fl.norm(e["name"])] = tuple(int(g) for g in m.groups())
    return out


def load_faction() -> dict[str, str]:
    out = {}
    for p in (ROOT / "domain" / "kb" / "raw_official").rglob("*.json"):
        d = json.loads(p.read_text(encoding="utf-8"))
        for e in d.get("entities", []):
            f = str(e.get("fields", {}).get("Faction (wiki logo)") or "")
            if f:
                out[fl.norm(e["name"])] = f
    return out


SECTION_TYPE = {"mount": "Surface", "compartment": "Compartment", "module": "Module"}


def load_kind() -> dict[str, str]:
    """wiki part -> socket type it can go into (Mount / Compartment / Module)."""
    out = {}
    for p in (ROOT / "domain" / "kb" / "raw_official").rglob("*.json"):
        d = json.loads(p.read_text(encoding="utf-8"))
        for e in d.get("entities", []):
            kind = SECTION_TYPE.get(str(e.get("section") or "").split("›")[0].strip().lower())
            if kind:
                out[fl.norm(e["name"])] = kind
    return out


def fits_axes(dims, box) -> bool:
    """RotateAxis.None default: every axis must fit as-is."""
    return dims[0] <= box[0] and dims[1] <= box[1] and dims[2] <= box[2]


def fits_squared(dims, box) -> bool:
    """RotateAxis.AnyAxis: only the diagonal length is compared."""
    return sum(x * x for x in dims) <= sum(x * x for x in box)


def sizes_for(hull: str) -> dict[str, tuple[int, int, int]]:
    """Socket boxes for one hull. Section hulls are stored as bow + core + stern."""
    return {s["key"]: tuple(s["size"]) for s in hu.sockets(hull)}


def types_for(hull: str) -> dict[str, str]:
    """Socket key -> Surface / Compartment / Module for one hull."""
    return {s["key"]: s["type"] for s in hu.sockets(hull)}


def structure_issues(path: pathlib.Path) -> list[str]:
    """Hull-config structure rules that decide whether the game can load the file."""
    out: list[str] = []
    try:
        root = ET.parse(path).getroot()
    except ET.ParseError as exc:
        return [f"  XML 解析失败：{exc}"]
    # 实测：游戏自己写出的 .fleet（如 Imported\S2LN NEO.fleet）同样省略这三个空元素，
    # 反序列化仍然成功 —— 所以只提示，不计为错误。
    for elem in ("ModDependencies", "MissileTypes", "CraftTypes"):
        if root.find(elem) is None:
            out.append(f"  (提示) 省略了 <{elem} />；游戏存档也会省略，不影响加载")
    for sh in root.findall("./Ships/Ship"):
        name = sh.findtext("Name") or "?"
        hc = sh.find("./HullConfig")
        if hc is None:
            continue  # 非随机舰体，随机生成
        kind = hc.get("{http://www.w3.org/2001/XMLSchema-instance}type") or ""
        if kind != "RandomHullConfiguration":
            continue
        segs = hc.findall("./PrimaryStructure/SegmentConfiguration")
        if len(segs) != 3:
            out.append(f"  [{name}] PrimaryStructure 段数 = {len(segs)}，必须为 3")
        keys = [(s.findtext("Key") or "").strip() for s in segs]
        hull_type = (sh.findtext("HullType") or "").strip()
        guids = hu.segment_guids(hull_type)
        if not guids:
            # only the three section hulls get a <HullConfig>; a Flathead/Journeyman
            # with one is a bug (the game randomises or ignores the structure)
            out.append(f"  [{name}] HullType {hull_type!r} 是单体 prefab，不该带 <HullConfig>")
        else:
            for part, key in zip(hu.PARTS, keys):
                allowed = {guids.get(letter, {}).get(part) for letter in ("A", "B", "C")} - {None}
                if key and allowed and key not in allowed:
                    out.append(f"  [{name}] {part} 段 GUID {key} 不属于该船体的分段表（会被随机替换）")
        if hc.find("./SecondaryStructure") is None:
            out.append(f"  [{name}] 缺少 <SecondaryStructure />（缺了会崩，空元素=无舰桥）")
        else:
            bridges = hc.findall("./SecondaryStructure/SecondaryStructureConfig")
            if len(bridges) > 1:
                out.append(f"  [{name}] 舰桥数量 {len(bridges)} > 1（会坏档）")
            for b in bridges:
                seg = b.findtext("Segment") or "0"
                if seg.strip() not in {"0", "1", "2"}:
                    out.append(f"  [{name}] 舰桥 Segment={seg} 越界")
    return out


def main(argv: list[str]) -> int:
    idx = fl.WikiIndex()
    dims = load_dims(idx)
    faction = load_faction()
    kinds = load_kind()
    game = json.loads((pathlib.Path(__file__).resolve().parents[1] / "data" / "game_names.json").read_text(encoding="utf-8"))
    hull_set = set(game["hulls"])
    comp_set = set(game["components"])
    fac_set = set(game["factions"])
    files: list[pathlib.Path] = []
    for arg in argv:
        p = pathlib.Path(arg)
        files.extend(sorted(p.glob("*.fleet")) if p.is_dir() else [p])
    bad = 0
    for path in files:
        fleet = fl.parse_fleet(path)
        print(f"== {path.name}: {fleet.name} | {len(fleet.ships)} ships | {fleet.total_points} pts")
        structural = structure_issues(path)
        for line in structural:
            print(line)
        bad += len([x for x in structural if "(提示)" not in x])
        if fleet.faction not in fac_set:
            print(f"  阵营键无效 FactionKey={fleet.faction!r}（游戏只认 {sorted(fac_set)}）")
            bad += 1
        for ship in fleet.ships:
            if ship.hull_type not in hull_set:
                print(f"  舰体键无效 HullType={ship.hull_type!r}（游戏里会找不到船体）")
                bad += 1
            hull = hu.resolve(ship.hull_type)
            sizes = sizes_for(hull)
            sock_key_type = types_for(hull)
            hull_faction = "Outlying Systems Protectorate (OSP)" if "Marauder" in hull else ""
            issues = []
            for sock in ship.sockets:
                box = sizes.get(sock.key)
                comp = idx.component(sock.component_name)
                name = comp.name if comp else fl.save_key_name(sock.component_name)
                d = dims.get(fl.norm(name))
                fac = faction.get(fl.norm(name), "")
                kind = kinds.get(fl.norm(name), "")
                if box is None:
                    issues.append(f"  槽位未知 {sock.key} ({name})")
                if kind and sock_key_type.get(sock.key) and kind != sock_key_type[sock.key]:
                    issues.append(
                        f"  类型不符 {name} 是 {kind}，槽位是 {sock_key_type[sock.key]}"
                        "（游戏里会静默留空）"
                    )
                if box and d:
                    if not fits_axes(d, box) and not fits_squared(d, box):
                        issues.append(f"  装不下 {name} {d} > 槽位 {box}（游戏里静默留空）")
                    elif not fits_axes(d, box) and fits_squared(d, box):
                        issues.append(
                            f"  (提示) {name} {d} 只能靠 RotateAxis.AnyAxis 装进 {box}"
                            "（对角线通过、逐轴不通过）"
                        )
                if fac and hull_faction and hull_faction not in fac and "both" not in fac:
                    issues.append(f"  阵营不符 {name} [{fac}] 装到 {hull}")
            issues_only = [x for x in issues if "(提示)" not in x]
            print(f"  {ship.name} ({hull}) sockets={len(ship.sockets)} issues={len(issues_only)}")
            for i in issues[:8]:
                print(i)
            bad += len(issues_only)
    print("total issues:", bad)
    return 0 if bad == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))

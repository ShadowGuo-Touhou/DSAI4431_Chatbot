"""`.fleet` 的模板库工具：把源舰队里的导弹/舰载机模板搬进新舰队。

舰队根节点里有 `<MissileTypes>` 和 `<CraftTypes>` 两个库，每个条目（`MissileTemplate` /
`CraftTemplate`）靠 `<TemplateKey>` 这个 GUID 被船上的发射器 / 机库引用。手工拼舰队
（`merge_fleets.py`、`export_samples.py`）如果只搬 `<Ship>`，游戏就会报
`Fleet is missing guide with GUID …; the ship … will start independently` —— 导弹和舰载机
全空。这里负责按 `TemplateKey` 去重搬运。

Run with repo/.venv python.
"""

from __future__ import annotations

import xml.etree.ElementTree as ET
from pathlib import Path

LIBRARIES = ("MissileTypes", "CraftTypes")

#: 库名 → 条目 tag
ENTRY = {"MissileTypes": "MissileTemplate", "CraftTypes": "CraftTemplate"}


def template_key(node: ET.Element) -> str:
    """条目的唯一键：`TemplateKey`，退回 `BodyKey` / `FrameKey`，再退回整段 XML。"""
    for tag in ("TemplateKey", "BodyKey", "FrameKey"):
        value = (node.findtext(tag) or "").strip()
        if value:
            return value
    return ET.tostring(node, encoding="unicode")[:200]


def collect_libraries(path: str | Path) -> dict[str, list[ET.Element]]:
    """读一个 `.fleet`，返回它根节点下两个模板库的条目（原样，不深拷贝）。"""
    root = ET.parse(str(path)).getroot()
    out: dict[str, list[ET.Element]] = {}
    for lib in LIBRARIES:
        node = root.find(lib)
        out[lib] = list(node) if node is not None else []
    return out


def gather(paths) -> dict[str, dict[str, ET.Element]]:
    """多份舰队 → 每个库一份 `TemplateKey → 条目` 的字典（先到先得）。"""
    pool: dict[str, dict[str, ET.Element]] = {lib: {} for lib in LIBRARIES}
    for path in paths:
        for lib, entries in collect_libraries(path).items():
            for entry in entries:
                pool[lib].setdefault(template_key(entry), entry)
    return pool


def emit(root: ET.Element, pool: dict[str, dict[str, ET.Element]]) -> None:
    """把模板库按游戏的文件顺序挂到舰队根节点上（`<Ships>` 之后）。"""
    for lib in LIBRARIES:
        entries = pool.get(lib) or {}
        if not entries:
            continue
        node = ET.SubElement(root, lib)
        for entry in entries.values():
            node.append(ET.fromstring(ET.tostring(entry)))


def missing(root: ET.Element) -> list[str]:
    """检查舰队里被引用、但库里没有的模板 GUID（游戏里表现为「start independently」）。"""
    pool = {template_key(n) for lib in LIBRARIES if (node := root.find(lib)) is not None for n in node}
    refs: set[str] = set()
    for node in root.iter():
        if node.tag != "MissileTemplate" and node.tag != "CraftTemplate":
            text = (node.text or "").strip()
            if text in pool:
                continue
    # 引用以 `<TemplateKey>` 出现在船内（`TemplateMissileTypes` / `TemplateSpacecraftTypes`）
    for ship in root.iter("Ship"):
        for lib in ("TemplateMissileTypes", "TemplateSpacecraftTypes"):
            node = ship.find(lib)
            if node is None:
                continue
            for entry in node:
                refs.add(template_key(entry))
    return sorted(r for r in refs if r and r not in pool)

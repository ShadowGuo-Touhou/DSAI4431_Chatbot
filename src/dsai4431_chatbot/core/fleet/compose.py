"""把 `sample fleets/` 里的样板船拼成一条可直接载入游戏的 `.fleet`。

为什么要有这个模块：模型**写不了** `.fleet`。文件里的槽位 key 是 22 字符的随机串
（`4V6twrIUcEKE11tom-tDXQ`），手写的 `MT1`/`CMP1` 只会被游戏当成「无效 key → 跳过」，
槽位静默空着；再加上 `<InitialFormation><GuideKey>` 要跟着 `<Key>` 改、
导弹/舰载机模板库 `<MissileTypes>` / `<CraftTypes>` 必须带，手搓几乎必错。

所以交付物交给代码：模型只负责挑船（samples）+ 起名，序列化、重排 key、修 guide、
搬模板库、写文件、校验全部在这里做。

用法（包内）::

    from dsai4431_chatbot.core.fleet import compose
    compose.list_samples()                       # 61 条样板船
    compose.compose(["gun MN - Excuse The Interruption"] * 5, name="Garnet Copy")
"""

from __future__ import annotations

import re
import uuid
import xml.etree.ElementTree as ET
from pathlib import Path

XSI = "http://www.w3.org/2001/XMLSchema-instance"
XSD = "http://www.w3.org/2001/XMLSchema"
ET.register_namespace("xsi", XSI)
ET.register_namespace("xsd", XSD)

# 舰队级模板库：发射器里的 `$MODMIS$/…`、机库里的 `$CRAFT$/…` 都靠它们解析
LIBRARIES = ("MissileTypes", "CraftTypes")
# 输出目录（仓库根下，和 `sample fleets/` 并列，不进 git）
OUT_DIRNAME = "fleet output"
BAD_CHARS = re.compile(r'[\\/:*?"<>|]')


def samples_dir() -> Path:
    from dsai4431_chatbot.core.gui import settings_store

    return settings_store.project_root() / "sample fleets"


def output_dir() -> Path:
    from dsai4431_chatbot.core.gui import settings_store

    root = settings_store.project_root() / OUT_DIRNAME
    root.mkdir(exist_ok=True)
    return root


def safe_name(text: str, *, fallback: str = "fleet") -> str:
    cleaned = BAD_CHARS.sub("-", str(text or "")).strip().strip(".")
    return cleaned or fallback


# --- 读样板船 ---------------------------------------------------------------


def _ship_name(ship: ET.Element) -> str:
    return (ship.findtext("Name") or "").strip()


def _ship_cost(ship: ET.Element) -> float:
    try:
        return float((ship.findtext("Cost") or "0").strip() or 0)
    except ValueError:
        return 0.0


def read_sample(path: Path) -> dict:
    """读一条样板船文件，返回 {path, name, ships:[{name,cost,hull}], points, faction}。"""
    root = ET.parse(path).getroot()
    ships = [
        {
            "name": _ship_name(ship),
            "cost": _ship_cost(ship),
            "hull": (ship.findtext("HullType") or "").strip(),
        }
        for ship in root.findall("Ships/Ship")
    ]
    return {
        "path": path,
        "name": path.stem,
        "class": path.stem.split(" - ")[0].strip(),
        "faction": (root.findtext("FactionKey") or "").strip(),
        "points": sum(s["cost"] for s in ships),
        "ships": ships,
    }


def list_samples() -> list[dict]:
    """所有可选样板船（按舰级、点数排序）。"""
    rows = [read_sample(p) for p in sorted(samples_dir().glob("*.fleet"))]
    rows.sort(key=lambda r: (r["class"], r["points"], r["name"]))
    return rows


def _resolve(entries: list[str]) -> tuple[list[dict], list[str]]:
    """把用户/模型给的名字对到真实文件（容忍大小写、省略 .fleet、模糊包含）。"""
    available = [p.stem for p in sorted(samples_dir().glob("*.fleet"))]
    lowered = {stem.lower(): stem for stem in available}
    found: list[dict] = []
    errors: list[str] = []
    for raw in entries:
        want = str(raw or "").strip()
        if want.lower().endswith(".fleet"):
            want = want[:-6]
        stem = lowered.get(want.lower())
        if stem is None:                       # 退一步：包含匹配，唯一才算
            hits = [s for s in available if want.lower() in s.lower()]
            if len(hits) == 1:
                stem = hits[0]
            elif len(hits) > 1:
                errors.append(f"「{raw}」匹配到多条：{'；'.join(hits[:6])}")
                continue
            else:
                errors.append(f"没有「{raw}」这条样板船（先不填 samples 调用一次可以列出全部）")
                continue
        found.append(read_sample(samples_dir() / f"{stem}.fleet"))
    return found, errors


# --- 拼舰队 -----------------------------------------------------------------


def _gather_libraries(paths: list[Path]) -> dict[str, list[ET.Element]]:
    """把各样板船的模板库按 key 去重（先出现的优先）。"""
    pool: dict[str, dict[str, ET.Element]] = {tag: {} for tag in LIBRARIES}
    for path in paths:
        try:
            root = ET.parse(path).getroot()
        except (ET.ParseError, OSError):
            continue
        for tag in LIBRARIES:
            holder = root.find(tag)
            if holder is None:
                continue
            for entry in holder:
                key = template_key(entry)
                if key and key not in pool[tag]:
                    pool[tag][key] = entry
    return {tag: list(entries.values()) for tag, entries in pool.items()}


def template_key(node: ET.Element) -> str:
    for tag in ("TemplateKey", "BodyKey", "FrameKey"):
        text = (node.findtext(tag) or "").strip()
        if text:
            return text
    return ""


def compose(
    entries: list[str],
    *,
    name: str = "",
    out: Path | str | None = None,
    renames: list[str] | None = None,
    description: str = "",
) -> dict:
    """按样板船列表拼一条舰队并写盘。

    `entries` 是样板船文件名（可重复，重复几次就是几艘）；`renames` 可选，逐条改船名。
    """
    picks, errors = _resolve(entries)
    if errors:
        return {"ok": False, "error": "；".join(errors), "ships": 0}

    factions = {p["faction"] for p in picks}
    if len(factions) > 1:
        return {
            "ok": False,
            "error": (
                "`<FactionKey>` 是舰队级的，混阵营的舰队游戏会拒绝载入："
                + "、".join(sorted(factions))
                + "。请拆成两条舰队。"
            ),
            "ships": 0,
        }

    fleet_name = safe_name(name or "New Fleet")
    root = ET.Element("Fleet")
    ET.SubElement(root, "Name").text = fleet_name
    ET.SubElement(root, "Version").text = "3"
    points_node = ET.SubElement(root, "TotalPoints")
    if factions:
        ET.SubElement(root, "FactionKey").text = sorted(factions)[0]
    ET.SubElement(root, "Description").text = description or (
        f"由 {len(picks)} 艘样板船拼成（sample fleets/），船体与挂载未改动。"
    )
    ships_node = ET.SubElement(root, "Ships")

    remap: dict[str, str] = {}
    total = 0.0
    warnings: list[str] = []
    used_names: set[str] = set()
    rename_list = [str(x).strip() for x in (renames or [])]

    for index, pick in enumerate(picks, start=1):
        src_ships = ET.parse(pick["path"]).getroot().findall("Ships/Ship")
        if not src_ships:
            warnings.append(f"{pick['name']} 里没有船，跳过")
            continue
        node = ET.fromstring(ET.tostring(src_ships[0]))
        old_key = (node.findtext("Key") or "").strip()
        key_node = node.find("Key")
        if key_node is not None:
            key_node.text = new_key = str(uuid.uuid4())
            if old_key:
                remap[old_key] = new_key
        number = node.find("Number")
        if number is not None:
            number.text = str(index)
        wanted = rename_list[index - 1] if index - 1 < len(rename_list) else ""
        if wanted:
            name_node = node.find("Name")
            if name_node is not None:
                name_node.text = wanted
        # 同名船在舰队里会互相覆盖，补个序号
        display = (node.findtext("Name") or "").strip()
        if display in used_names:
            display = f"{display} {index}"
            name_node = node.find("Name")
            if name_node is not None:
                name_node.text = display
            warnings.append(f"第 {index} 艘与前面同名，已改成「{display}」")
        used_names.add(display)
        total += _ship_cost(node)
        ships_node.append(node)

    if not ships_node:
        return {"ok": False, "error": "没有任何船可以写进舰队", "ships": 0}

    # `<InitialFormation><GuideKey>` 必须指回这次新分配的 `<Key>`
    for ship in ships_node:
        guide = ship.find("InitialFormation/GuideKey")
        if guide is None:
            continue
        old = (guide.text or "").strip()
        guide.text = remap.get(old, (ship.findtext("Key") or "").strip())

    libraries = _gather_libraries([p["path"] for p in picks])
    for tag in LIBRARIES:
        holder = ET.SubElement(root, tag)
        for entry in libraries.get(tag, []):
            holder.append(ET.fromstring(ET.tostring(entry)))

    points_node.text = f"{total:.0f}"

    target = Path(out) if out else output_dir() / f"{fleet_name}.fleet"
    if not target.is_absolute():
        target = output_dir() / safe_name(target.name)
    target.parent.mkdir(parents=True, exist_ok=True)
    _write(root, target)

    report = check(target)
    report.update(
        {
            "name": fleet_name,
            "path": str(target),
            "ships": len(ships_node),
            "points": round(total, 1),
            "faction": (sorted(factions)[0] if factions else ""),
            "sources": [p["name"] for p in picks],
            "templates": {tag: len(items) for tag, items in libraries.items()},
            "warnings": warnings + report.get("warnings", []),
        }
    )
    return report


def _write(root: ET.Element, path: Path) -> None:
    ET.indent(root, space="  ")
    body = ET.tostring(root, encoding="unicode")
    body = body.replace("<Fleet>", f'<Fleet xmlns:xsd="{XSD}" xmlns:xsi="{XSI}">', 1)
    path.write_text('<?xml version="1.0" encoding="UTF-8"?>\n' + body, encoding="utf-8")


# --- 校验 -------------------------------------------------------------------


def check(path: Path | str) -> dict:
    """重新读一遍写出来的文件：能不能解析、guide 有没有断、模板库缺不缺。"""
    target = Path(path)
    problems: list[str] = []
    try:
        root = ET.parse(target).getroot()
    except (ET.ParseError, OSError) as exc:
        return {"ok": False, "error": f"文件读不回来：{exc}", "problems": [str(exc)]}

    ships = root.findall("Ships/Ship")
    keys = {(ship.findtext("Key") or "").strip() for ship in ships}
    for index, ship in enumerate(ships, start=1):
        guide = (ship.findtext("InitialFormation/GuideKey") or "").strip()
        if guide and guide not in keys:
            problems.append(f"第 {index} 艘的 GuideKey 指向不存在的船")
        cost = _ship_cost(ship)
        if cost <= 0:
            problems.append(f"第 {index} 艘点数为 0")

    have = {tag: {template_key(e) for e in (root.find(tag) or [])} for tag in LIBRARIES}
    missing_missiles, missing_craft = set(), set()
    for ship in ships:
        for ref in ship.iter("TemplateMissileTypeKey"):
            text = (ref.text or "").strip()
            if text.startswith("$MODMIS$/") and text not in have["MissileTypes"]:
                missing_missiles.add(text)
        for ref in ship.iter("CraftTemplateKey"):
            text = (ref.text or "").strip()
            if text and text not in have["CraftTypes"]:
                missing_craft.add(text)
    if missing_missiles:
        problems.append(f"缺导弹模板：{'、'.join(sorted(missing_missiles)[:4])}")
    if missing_craft:
        problems.append(f"缺舰载机模板：{'、'.join(sorted(missing_craft)[:4])}")

    total = sum(_ship_cost(s) for s in ships)
    return {
        "ok": not problems,
        "problems": problems,
        "warnings": [],
        "path": str(target),
        "ships": len(ships),
        "points": round(total, 1),
    }


def summary_text(report: dict) -> str:
    """给模型看的一段话（也是界面上那行小字）。"""
    if not report.get("ok"):
        return f"生成失败：{report.get('error') or '；'.join(report.get('problems') or [])}"
    templates = report.get("templates") or {}
    bits = [
        f"已生成舰队文件：{report['path']}",
        f"{report['ships']} 艘 · {report['points']:.0f} 点"
        + (f" · 阵营 {report['faction']}" if report.get("faction") else ""),
    ]
    if templates:
        bits.append(
            "模板库：导弹 "
            + str(templates.get("MissileTypes", 0))
            + " / 舰载机 "
            + str(templates.get("CraftTypes", 0))
        )
    bits.append("校验通过（能解析、guide 无断链、模板库齐全、每条船点数 > 0）")
    if report.get("warnings"):
        bits.append("注意：" + "；".join(report["warnings"][:4]))
    bits.append(
        "告诉用户：把上面这个文件复制进游戏的舰队目录"
        "（`Nebulous\\Saves\\Fleets\\`），再在游戏里「载入舰队」里选它。"
        "**不要把整份 XML 粘到聊天里**——几千行，用户也复制不动。"
    )
    return "\n".join(bits)

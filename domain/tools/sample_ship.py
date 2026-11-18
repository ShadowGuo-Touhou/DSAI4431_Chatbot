"""把一艘真实样本船渲染成「槽位 → 部件 → 点数」的完整装配表。

知识库以前只有两张半成品：
  * `builds/<class>.md` —— 舰级硬性要求 + 部件**频率**（`FR3300 (3/3)`），不是装配；
  * `zh/槽位配置总表.md` —— 每个槽位最常见的部件，也不是某一条船的装配。

于是模型要凭这两张表自己拼一艘船：先查舰级、再查槽位、再逐个部件查尺寸点数，
三跳检索走不完就停在「我还没查槽位表」。这里直接给出**一条真实好船的完整装配**，
让它整艘照抄（这也正是 `zh/造舰 SOP.md` 的第一步「整艘复制」）。

只用存档里读得到的事实：槽位号来自 hull_sockets.json（游戏 prefab 的短名 / 连续挂载号），
部件点数与供电来自官方 wiki 的部件条目。
"""

from __future__ import annotations

import json
import re
from pathlib import Path

import fleet_lib as fl
import hulls as hu

ROOT = Path(__file__).resolve().parents[2]

KIND_CN = {"Surface": "挂载", "Compartment": "舱段", "Module": "模块"}
KIND_ORDER = {"Surface": 0, "Compartment": 1, "Module": 2}
#: 舰体自带的部件（Main 01 / Thruster 01 …）在存档里也用 `Stock/…` 前缀，但 wiki
#: 里没有条目；它们已经算在舰体的 Point Cost 里，不能重复计点。
BUILTIN_HINT = ("main ", "thruster", "rct ", "antenna", "berthing", "hangar ")


def _sections(hull_type: str) -> list[tuple[str, dict]]:
    """[(section_name, socket)]；单体 prefab 的 section_name 为空。"""
    return hu.sockets_by_part(hull_type)


def labels(hull_type: str) -> dict[str, tuple[str, str]]:
    """socket key -> (kind, label)。

    单体船体用游戏自己的短名（`MT3` / `CMP5` / `MOD11`）。模块化船体（LN/CLN/CVL/MN）
    的分段 prefab 每条都从 `MT1`/`CMP1` 重新数，所以标签前面加段名：`Bow·MT3`。
    """
    mounts = hu.mount_numbers(hull_type)
    out: dict[str, tuple[str, str]] = {}
    groups: dict[tuple[str, str], list[dict]] = {}
    for section, entry in _sections(hull_type):
        key = str(entry.get("key") or "")
        kind = str(entry.get("type") or "")
        if kind == "Surface":
            num = mounts.get(key)
            label = f"MT{num}" if num else str(entry.get("short") or "?")
            out[key] = (kind, f"{section}·{label}" if section else label)
            continue
        groups.setdefault((section, kind), []).append(entry)
    for (section, kind), entries in groups.items():
        prefix = "CMP" if kind == "Compartment" else "MOD"
        entries.sort(key=lambda e: (e.get("i") or 10**6, str(e.get("short") or "")))
        # 单体船体自带 `MOD1`/`CMP5` 这种编号（就是游戏号）；模块化分段里短名会重复或缺失，
        # 那种情况按 `i` 排序后在本段内从 1 数。
        for n, entry in enumerate(entries, start=1):
            short = str(entry.get("short") or "")
            label = short if re.fullmatch(rf"{prefix}\d+", short) else f"{prefix}{n}"
            out[str(entry.get("key") or "")] = (kind, f"{section}·{label}" if section else label)
    return out


FACTION_KEYS = {
    "Shelter Alliance": "Stock/Shelter Alliance",
    "Outlying Systems Protectorate": "Stock/Outlying Systems Protectorate",
}

#: 存档里的舰体键 → wiki 的船体页。模块化家族在存档里按「段」存（`Bulk Hauler`、`Ore Carrier`…），
#: wiki 只有同一条生产线的固定船体名，报价时按这里的对应关系取舰体点数。
HULL_ALIAS = {
    "Bulk Hauler": "Marauder Line Ship Class",
    "Container Hauler": "Moorline Line Ship Class",
    "Container Hauler Refit": "Moorline Line Ship Class",
    "Ore Carrier": "Journeyman Light Carrier Class",
    "Bulk Feeder": "Flathead Monitor Class",
    "Shuttle": "Ferryman Clipper Class",
    "Tugboat": "Draugr Clipper Class",
}


def _faction_key(hull) -> str:
    """wiki 的阵营 → `.fleet` 里要写的 `FactionKey`。

    固定船体的 wiki `section` 是 `Ship hulls › Shelter Alliance hulls` 这种；模块化船体
    （LN/CLN/CVL/MN 的存档名）没有 section，就留空 —— 这类船体的阵营由玩家选的舰体决定。
    """
    section = str(getattr(hull, "section", "") or "")
    if "Shelter Alliance" in section:
        return "Stock/Shelter Alliance"
    if "Outlying Systems Protectorate" in section:
        return "Stock/Outlying Systems Protectorate"
    return ""


def _ammo_points(ship, idx) -> tuple[float, list[str], float]:
    """按 `domain/data/ammo_costs.json` 估算这艘船的弹药点与弹库点。"""
    path = ROOT / "domain" / "data" / "ammo_costs.json"
    if not path.exists():
        return 0.0, [], 0.0
    table = json.loads(path.read_text(encoding="utf-8"))
    prices: dict[str, float] = {}
    for group in ("shells", "missiles", "decoys"):
        prices.update({_norm(k): v for k, v in (table.get(group) or {}).items()})

    def price(name: str) -> float | None:
        key = _norm(name)
        if key in prices:
            return prices[key]
        for k, v in prices.items():
            if len(k) > 6 and (k in key or key in k):
                return v
        # 存档里有些弹用的是旧名/缩写（`Flak Round`、`Slug`…），按口径数字猜：
        # 450mm 0.04、250mm 0.02、120mm 0.01、100mm 0.004；没有口径数字就当小口径高炮。
        m = re.search(r"\b(\d{2,3})\s*mm\b", key)
        caliber = {"450": 0.04, "400": 0.04, "300": 0.04, "250": 0.02, "120": 0.01, "100": 0.004}
        if m and m.group(1) in caliber:
            return caliber[m.group(1)]
        if any(tag in key for tag in ("sgm", "sdm", "sgt", "cm-", "decoy", "ea12", "ea14", "ea20", "ea99")):
            return None  # 导弹/诱饵走下面的 1 点/发
        return 0.01  # 无口径的炮弹（Flak Round / Slug 之类）

    total = 0.0
    unknown: list[str] = []
    for sock in ship.sockets:
        for ammo in sock.ammo or []:
            name = fl.save_key_name(ammo.item)
            per = price(name)
            if per is None:
                total += ammo.quantity  # 无公开价的导弹/诱饵按 1 点/发
                unknown.append(name)
            else:
                total += per * ammo.quantity

    mags = []
    for sock in ship.sockets:
        comp = idx.component(sock.component_name)
        if comp and "Magazine" in comp.name:
            mags.append(comp.name)
    mag_pts = 0.0
    if mags:
        priced = sorted(
            (table.get("magazines", {}).get(name, {}).get("next", 20.0) for name in mags),
            reverse=True,
        )
        mag_pts = sum(priced[1:])  # 最贵的一座免点
    return round(total), sorted(set(unknown)), round(mag_pts)


def _norm(text: str) -> str:
    """弹名归一：去引号与 `[PD Prio Fired]` 这类后缀、压空格、小写。"""
    text = re.sub(r"\[[^\]]*\]", "", text or "")
    text = text.replace("'", "'").replace("`", "'")
    return re.sub(r"\s+", " ", text).strip().lower()


def _is_builtin(name: str) -> bool:
    low = name.lower()
    return any(hint in low for hint in BUILTIN_HINT)


def _cost_label(comp) -> str:
    """弹库的价格是「第一座免费、之后 40」这种字符串，直接照抄比编一个数清楚。"""
    if comp is None:
        return "—"
    raw = str(comp.fields.get("Cost (pts)") or "")
    if "compounding" in raw:
        import re

        m = re.match(r"\s*(\d+)\s*,\s*(\d+)", raw)
        return f"{m.group(1)} → 之后 {m.group(2)}/座" if m else raw[:20]
    return f"{comp.cost:.0f}"


def _fits(part: str, sock: str) -> bool:
    """部件的三边能否塞进槽位（允许任意轴向旋转）；解析失败就当能装。"""
    def dims(text: str) -> list[int]:
        nums = [int(n) for n in re.findall(r"\d+", text or "")]
        return sorted(nums[:3]) if len(nums) >= 3 else []

    p, s = dims(part), dims(sock)
    if not p or not s:
        return True
    return all(a <= b for a, b in zip(p, s))


def _craft_points(ship) -> tuple[float, int, list[str]]:
    """机库里的舰载机点数（`domain/data/craft_prices.json`，来自存档 `<CraftTypes>`）。"""
    path = ROOT / "domain" / "data" / "craft_prices.json"
    if not path.exists():
        return 0.0, 0, []
    table = json.loads(path.read_text(encoding="utf-8")).get("seat") or {}
    total = 0.0
    count = 0
    unknown: list[str] = []
    for sock in ship.sockets:
        for key in getattr(sock, "craft", []) or []:
            count += 1
            entry = table.get(key)
            cost = entry.get("cost") if isinstance(entry, dict) else None
            if isinstance(cost, (int, float)):
                total += float(cost)
            else:
                label = key.split("/")[-1]
                if label not in unknown:
                    unknown.append(label)
    return total, count, unknown


def render(
    path: str | Path,
    ship_name: str,
    *,
    idx: fl.WikiIndex | None = None,
    fleet: fl.Fleet | None = None,
    heading: str = "##",
) -> str:
    """一艘船的完整装配表（markdown）；找不到船就返回空串。"""
    fleet = fleet or fl.parse_fleet(str(path))
    ship = next((s for s in fleet.ships if s.name == ship_name), None)
    if ship is None:
        return ""
    idx = idx or fl.WikiIndex()
    lab = labels(ship.hull_type)
    sizes = {r["key"]: "×".join(str(v) for v in r["size"]) for r in hu.sockets(ship.hull_type)}
    rows: list[tuple[int, int, str, str, str, object, float]] = []
    parts_pts = 0.0
    draw = supply = 0.0
    builtin: list[str] = []
    ammo_lines: list[str] = []
    for sock in ship.sockets:
        kind, label = lab.get(sock.key, ("", sock.key[:6]))
        comp = idx.component(sock.component_name)
        name = comp.name if comp else fl.save_key_name(sock.component_name)
        if comp is None and _is_builtin(name):
            builtin.append(name)
            continue
        cost = comp.cost if comp else 0.0
        power = comp.power if comp else 0.0
        dims = (comp.fields.get("Dimensions") if comp else "") or "—"
        parts_pts += cost
        draw += max(-power, 0.0)
        supply += max(power, 0.0)
        num = 0
        digits = "".join(ch for ch in label.split("·")[-1] if ch.isdigit())
        if digits:
            num = int(digits)
        rows.append((KIND_ORDER.get(kind, 9), num, label, name, dims, comp, power, sizes.get(sock.key, "")))
        if sock.ammo:
            items = "、".join(f"{a.item.split('/')[-1]} ×{a.quantity}" for a in sock.ammo)
            ammo_lines.append(f"{label} {name}：{items}")
    rows.sort(key=lambda r: (r[0], r[1]))
    hull = idx.hull(ship.hull_type) or idx.hull(HULL_ALIAS.get(fl.save_key_name(ship.hull_type), ""))
    hull_pts = hull.point_cost if hull else 0.0
    faction = _faction_key(hull) if hull else ""
    ammo_pts, unknown, mag_pts = _ammo_points(ship, idx)
    craft_pts, craft_count, craft_unknown = _craft_points(ship)
    out = [
        f"{heading} 样板船完整装配（整艘照抄）：{ship.name}（{fleet.name}）",
        "",
        f"**整艘照抄**：舰体 `{fl.save_key_name(ship.hull_type)}`"
        f"（阵营键 `{faction}`），存档原值 **{ship.cost:.0f} 点**，"
        f"共 {len(ship.sockets)} 个槽位。复制这艘船时连它自带的导弹一起抄，只改船名、呼号和导弹名。",
        "",
        "| 槽位 | 部件 | 尺寸 | 点数 | 供电 kW |",
        "|---|---|---|---:|---:|",
    ]
    tight: list[str] = []
    for _, _, label, name, dims, comp, power, sock_size in rows:
        power_txt = f"{power:+.0f}" if power else "0"
        warn = ""
        if sock_size and dims and dims != "—" and not _fits(dims, sock_size):
            warn = f" ⚠ 槽只有 {sock_size}"
            tight.append(f"{label} {name}（{dims}）塞不进 {sock_size}")
        out.append(f"| {label} | {name}{warn} | {dims} | {_cost_label(comp)} | {power_txt} |")
    out.append("")
    out.append(
        f"- 合计：部件 {parts_pts:.0f} 点 + 舰体 {hull_pts:.0f} 点 = **{parts_pts + hull_pts:.0f} 点**"
        f"（不含弹库与弹药，见下）"
    )
    if mag_pts or ammo_pts or craft_pts:
        note = f"另有弹库 {mag_pts:.0f} 点 + 弹药 {ammo_pts:.0f} 点"
        if craft_count:
            note += f" + 舰载机 {craft_count} 架 {craft_pts:.0f} 点"
        if unknown:
            note += f"（{'、'.join(unknown)} 无公开单价，按 1 点/发估）"
        if craft_unknown:
            note += f"（{'、'.join(craft_unknown)} 无单价，未计入）"
        total = parts_pts + hull_pts + mag_pts + ammo_pts + craft_pts
        out.append(
            f"- {note} ⇒ **全价约 {total:.0f} 点**（估算；游戏里以存档原值 {ship.cost:.0f} 为准，"
            "单价见 `zh/弹药点数表.md`）"
        )
    if draw or supply:
        out.append(f"- 供电：发电 {supply:.0f} kW / 耗电 {draw:.0f} kW（余量 {supply - draw:+.0f} kW）")
    if builtin:
        uniq = sorted(set(builtin))
        out.append(f"- 舰体自带（不计点）：{'、'.join(uniq)}")
    if ammo_lines:
        out.append("- 弹库装载：" + "；".join(ammo_lines))
    if tight:
        out.append(
            "- ⚠ 存档里这几个槽装的东西比槽位大（旧版本留下的，当前版本装不进去）："
            + "；".join(tight)
            + "。照抄时换小一号的部件，或改用同功能的小件。"
        )
    out.append("")
    return "\n".join(out)

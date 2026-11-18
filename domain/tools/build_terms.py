"""Build the Chinese <-> English term reference used to review the domain vocabulary.

Sources
  * ``<game>/Nebulous_Data/StreamingAssets/Localization/en-US/en_assets.json``
  * ``<game>/.../zh-CN/cn_assets.json``  (``cn_ui.json`` is exported separately, it is too big)
  * ``domain/kb/raw_official/{component,hull,munition}/*.json`` — dimensions, cost, power,
    penetration, launcher cells, magazine capacity, the wiki's faction logo
  * ``domain/data/{munition_storage,munition_costs,hull_armour,game_names}.json``
  * real fleet saves — which faction actually fields a part (``observed`` column)
  * ``dsai4431_chatbot.core.rag.query_terms`` — the player shorthand the retriever maps

Outputs
  domain/reports/terms-zh-en.md      review document (hand-editable)
  domain/data/terms_zh_en.json       machine readable, with the extra columns
  domain/data/ui_terms_zh_en.csv     every UI key pair
"""

from __future__ import annotations

import csv
import json
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "domain" / "tools"))
import hulls as hu  # noqa: E402

GAME = Path(r"E:\SteamLibrary\steamapps\common\Nebulous")
LOC = GAME / "Nebulous_Data" / "StreamingAssets" / "Localization"
DOCS = ROOT / "domain" / "kb" / "docs"
RAW = ROOT / "domain" / "kb" / "raw_official"
DATA = ROOT / "domain" / "data"
OUT_MD = ROOT / "domain" / "reports" / "terms-zh-en.md"
OUT_JSON = ROOT / "domain" / "data" / "terms_zh_en.json"
OUT_UI = ROOT / "domain" / "data" / "ui_terms_zh_en.csv"

NAME_FAMILIES = [
    ("HULLCOMPNAME", "部件 / 挂载", "part"),
    ("HULLPARTNAME", "舰体自带部件", "builtin"),
    ("CRAFTCOMPNAME", "舰载机部件", "craft"),
    ("AMMONAME", "弹药", "ammo"),
    ("MISSILECOMPNAME", "导弹部件", "missile"),
]

# 官方译名明显是机翻、玩家有通行叫法的，按玩家叫法覆盖（原始译名仍保留在 JSON 的 chinese_official 字段）
TERM_FIX = {
    "Ferryman Masquerade": "小艇欺骗模块（伪装成渡船 / 官方机翻「船夫化装舞会」）",
    "Size 3 Torpedo": "尺寸 3 鱼雷（官方误作“导弹”）",
    "M-50 'Auger' Sprint Mine": "M-50「螺旋钻」冲刺水雷",
    "R-3 'Sailfish' Rocket": "R-3「旗鱼」火箭",
    "Fire": "火灾（船体着火减益）",
}

# wiki 没标阵营、但游戏里只给一家用的部件（玩家实测 / 官方数据）
FACTION_OVERRIDES = {
    "Citadel Magazine": "OSP 专属",
}

SECTION_ZH = {
    "Missile Construction": "弹体 / 引擎",
    "Missile Construction › Payload": "战斗部",
    "Missile Construction › Avionics Package": "航电",
    "Missile Construction › Seekers": "引导头",
    "Missile Construction › Auxiliary": "辅助",
    "Special Missiles › Decoys": "诱饵",
    "Special Missiles › Decoy Containers": "诱饵容器",
    "Special Missiles › Mines": "水雷",
    "Special Missiles › Bombs": "航弹",
    "Special Missiles › Rockets": "火箭",
}

FACTION_SHORT = {
    "Shelter Alliance (SA)": "SA 专属",
    "Outlying Systems Protectorate (OSP)": "OSP 专属",
}


def load(path: Path) -> dict[str, str]:
    return json.loads(path.read_text(encoding="utf-8-sig"))


def load_raw(folder: str, name: str) -> dict[str, dict]:
    """name -> fields, with the wiki section stored under ``_section``."""
    path = RAW / folder / name
    if not path.exists():
        return {}
    data = json.loads(path.read_text(encoding="utf-8"))
    out: dict[str, dict] = {}
    for entity in data.get("entities", []):
        fields = dict(entity.get("fields", {}))
        fields["_section"] = entity.get("section", "")
        out[entity["name"]] = fields
    return out


def wiki_entities() -> dict[str, dict]:
    """name(lower) -> {faction, kind, doc} from the built KB docs."""
    index: dict[str, dict] = {}
    for path in DOCS.rglob("*.md"):
        text = path.read_text(encoding="utf-8")
        name = re.search(r"^# (.+)$", text, re.M)
        tags = re.search(r"^Tags: (.+)$", text, re.M)
        if not name:
            continue
        kind = faction = ""
        if tags:
            m2 = re.search(r"kind=([^;]+)", tags.group(1))
            if m2:
                kind = m2.group(1).strip()
            m3 = re.search(r"faction=([^;]+)", tags.group(1))
            if m3:
                faction = m3.group(1).strip()
        index[name.group(1).strip().lower()] = {
            "faction": faction,
            "kind": kind,
            "doc": str(path.relative_to(ROOT)),
        }
    return index


def shorthand_terms() -> list[tuple[str, str]]:
    sys.path.insert(0, str(ROOT / "repo" / "src"))
    from dsai4431_chatbot.core.rag import query_terms  # noqa: PLC0415

    return list(query_terms.TERMS)


def observed_factions() -> dict[str, Counter]:
    """component name -> Counter(Alliance / Protectorate) over the real save corpus."""
    sys.path.insert(0, str(ROOT / "domain" / "tools"))
    import build_layouts  # noqa: PLC0415
    import fleet_lib as fl  # noqa: PLC0415

    seen: dict[str, Counter] = defaultdict(Counter)
    for path in build_layouts.collect_fleets():
        try:
            fleet = fl.parse_fleet(path)
        except Exception:  # noqa: BLE001 — a broken save must not kill the report
            continue
        faction = (fleet.faction or "").split("/")[-1] or "?"
        for ship in fleet.ships:
            for sock in ship.sockets:
                if sock.component_name:
                    seen[sock.component_name.split("/")[-1]][faction] += 1
    return seen


def clean_cell(text: str) -> str:
    text = (text or "").replace("\r", " ").replace("\n", " ").replace("\t", " ")
    text = text.replace("|", "\\|")
    return " ".join(text.split())


def md_table(rows: list[list[str]], header: list[str]) -> list[str]:
    out = ["| " + " | ".join(clean_cell(h) for h in header) + " |", "|" + "|".join("---" for _ in header) + "|"]
    for row in rows:
        out.append("| " + " | ".join(clean_cell(cell) for cell in row) + " |")
    return out



WIKI_NOISE_RE = re.compile(r"\[math\]|\[\d+\]|\displaystyle|\(\^2\)|\^2")


def tidy(value: str) -> str:
    """Strip wiki footnote / LaTeX noise out of a scraped field."""
    text = re.sub(r"\\displaystyle\{\s*\^2\s*\}", "²", value or "")
    text = re.sub(r"\[math\]|\[/math\]", "", text)
    text = re.sub(r"\[\d+\]", "", text)
    text = re.sub(r"\s*–\s*", "–", text)
    return " ".join(text.split()).strip()


def num(value: str, pattern: str = r"-?\d+(?:\.\d+)?") -> float | None:
    m = re.search(pattern, value or "")
    return float(m.group()) if m else None


def cost_text(value: str) -> str:
    """`10; 1x Compounding cost` -> `10（1x 叠加价）`."""
    text = tidy(value)
    m = re.match(r"(\d+)\s*[;,.]\s*(\d+)\s*after", text)
    if m:
        return f"{m.group(2)}（{m.group(1)}x 叠加价）"
    m = re.match(r"(\d+)\s*[;,.]\s*(\d+)x\s+Compounding", text, re.I)
    if m:
        return f"{m.group(1)}（{m.group(2)}x 叠加价）"
    m = re.match(r"(\d+)", text)
    return m.group(1) if m else (text or "-")


def power_text(fields: dict) -> str:
    for key in ("Required Power (kW)", "Power (kW)"):
        if key in fields:
            value = num(fields[key])
            if value is not None:
                return f"{abs(value):.0f} kW"
    for key in ("Provided Power (kW)",):
        if key in fields:
            value = num(fields[key])
            if value is not None:
                return f"+{value:.0f} kW"
    return "-"


def key_numbers(fields: dict) -> str:
    """The one number a player cares about for this kind of part."""
    parts: list[str] = []
    if "Autoloader Capacity" in fields and "Reload time (s)" in fields:
        cap = num(fields["Autoloader Capacity"])
        reload_ = num(fields["Reload time (s)"])
        if cap and reload_:
            parts.append(f"{cap:.0f} 发/{reload_:g}s · {cap * 60 / reload_:.1f} 发/分")
    if "Capacity (cells, minimum)" in fields:
        cells = num(fields["Capacity (cells, minimum)"])
        size = num(fields.get("Missile Size", ""))
        text = f"≤{cells:.0f} 发" if cells else ""
        if size:
            text += f" × S{size:.0f}"
        parts.append(text.strip())
    effects = fields.get("Effects", "")
    if "Storage Capacity" in effects:
        cap = re.search(r"\+(\d+)\s*m\s+Storage Capacity", effects)
        if cap:
            parts.append(f"+{cap.group(1)} m³/格")
    for label, key in (("射程", "Max Range (km)"), ("伤害", "Damage (Hp)"), ("穿深", "Penetration (cm)")):
        if key in fields:
            value = fields[key].split()[0]
            parts.append(f"{label} {value}")
    if "Max Speed (m/s)" in fields:
        parts.append(f"{fields['Max Speed (m/s)']} m/s")
    return " · ".join(p for p in parts if p) or "-"


def faction_cell(wiki_faction: str, obs: Counter, override: str = "") -> tuple[str, str, str, bool]:
    """(declared by wiki, observed evidence, suggestion, conflict?) for a part."""
    declared = override or FACTION_SHORT.get(wiki_faction, "") or "通用"
    sa, osp = obs.get("Alliance", 0), obs.get("Protectorate", 0)
    if not sa and not osp:
        return declared, "未见样本", declared, False
    seen = f"SA {sa} / OSP {osp}"
    if not osp:
        suggested = "SA 专属（实测）"
    elif not sa:
        suggested = "OSP 专属（实测）"
    elif sa and osp:
        suggested = "通用（实测）"
    else:  # pragma: no cover — keeps mypy honest
        suggested = declared
    conflict = declared in ("SA 专属", "OSP 专属") and bool(sa and osp)
    if conflict:
        seen += "（含 CC 跨阵营）"
        suggested = declared + "（CC 例外）"
    return declared, seen, suggested, conflict




BUILTIN_CATEGORY = [
    ("Radar", "雷达"), ("Main", "主引擎"), ("Thruster", "姿控/侧推"), ("Braking", "制动引擎"),
    ("Pad", "停机坪"), ("Hangar", "机库"), ("Resupply", "补给"), ("Weapon", "武器"),
    ("Silo", "发射井"), ("Armour", "装甲"), ("Anchor", "锚"),
]
CRAFT_CATEGORY = [
    ("Coilgun", "磁轨炮"), ("Pod", "荚舱"), ("Gun", "机炮"), ("Cannon", "火炮"), ("Beam", "光束"), ("Laser", "激光"),
    ("Missile", "导弹"), ("Rocket", "火箭"), ("Bomb", "炸弹"), ("PDT", "点防"),
    ("Engine", "引擎"), ("Thruster", "推进"), ("Armour", "装甲"), ("Shield", "护盾"), ("Scanner", "扫描"),
    ("ECM", "电子战"), ("Warhead", "战斗部"),
]


def guess_category(name: str, table: list[tuple[str, str]], default: str) -> str:
    low = name.lower()
    for token, label in table:
        if token.lower() in low:
            return label
    return default


def ammo_section(en: dict[str, str], cn: dict[str, str], munitions: dict[str, dict],
                 storage: dict[str, dict], costs: dict[str, str]) -> list[str]:
    """Detailed shell table: caliber, damage, penetration, rounds per point, volume, faction."""
    rows: list[list[str]] = []
    for key, zh in sorted(cn.items()):
        if not key.startswith("AMMONAME_"):
            continue
        english = en.get(key, "").strip()
        if not english:
            continue
        fields = munitions.get(english, {})
        per = costs.get(english) or fields.get("Cost (pts per X amount)", "")
        rounds = re.search(r"/(\d+)", str(per))
        store = storage.get(english, {})
        faction = {"Protectorate": "OSP", "Alliance": "SA", "": "通用"}.get(store.get("faction", ""), "-")
        rows.append([
            english,
            TERM_FIX.get(english, zh.strip()),
            fields.get("Shell classification", "-").split()[0] if fields else "-",
            fields.get("Damage (Hp)", "-"),
            fields.get("Penetration (cm)", "-"),
            f"{rounds.group(1)} 发/点" if rounds else "-",
            f"{store.get('storage_volume_m3', '-')} m³" if store else "-",
            faction,
        ])
    rows.sort(key=lambda r: r[0].lower())
    out = [
        f"## 弹药（{len(rows)} 条：口径 / 伤害 / 穿深 / 每点发数 / 单发体积 / 阵营）",
        "",
        "每点发数 = 官方 `Cost (pts per X amount)=1/N` 里的 N；单发体积取自游戏资源（`munition_storage.json`），"
        "装弹上限用 `弹库容量(m³) ÷ 单发体积` 算。",
        "",
        *md_table(rows, ["English", "中文", "口径", "伤害", "穿深 (cm)", "每点发数", "单发体积", "阵营"]),
        "",
    ]
    return out


def main() -> int:
    en = load(LOC / "en-US" / "en_assets.json")
    cn = load(LOC / "zh-CN" / "cn_assets.json")
    wiki = wiki_entities()

    components = load_raw("component", "components.json")
    hulls = load_raw("hull", "ships.json")
    munitions = load_raw("munition", "munitions-missiles.json")
    storage = json.loads((DATA / "munition_storage.json").read_text(encoding="utf-8"))
    costs = json.loads((DATA / "munition_costs.json").read_text(encoding="utf-8"))
    armour_doc = json.loads((DATA / "hull_armour.json").read_text(encoding="utf-8"))
    armour = armour_doc.get("hulls", {})
    names = json.loads((DATA / "game_names.json").read_text(encoding="utf-8"))
    observed = observed_factions()

    def comp_fields(english: str) -> dict:
        return components.get(english, {})

    lines: list[str] = [
        "# 中英术语总表",
        "",
        "数据来源：`en-US/en_assets.json` + `zh-CN/cn_assets.json`（同一 key 对照，游戏 0.6.2.6 自带）、"
        "`raw_official/*`（尺寸 / 点数 / 供电 / 穿深 / 弹舱值）、`domain/data/`（单发体积、每点发数、装甲、存档键）、"
        "352 份存档（实测某部件被哪家实际使用）、`query_terms.py` 与 `manual_zh/`（玩家口语）。",
        "",
        "**列说明**",
        "",
        "- `类别` 取自 wiki 页面（挂载 / 舱室 / 模块）。",
        "- `阵营`：wiki 有阵营图标写「SA 专属 / OSP 专属」，**没有图标 = 通用**（游戏里双方都能装）。",
        "- `实测（存档）` = 352 份真实存档里这个部件被 SA / OSP 各装了多少次；`⚠` 表示 wiki 说专属、但另一家也在用。",
        "",
        "## 译名优先级（冲突时按顺序采纳）",
        "",
        "1. **`other info` 里的玩家表格**（`Neb英文缩写.jpg`、`NEB简明指挥术语v0.1.png`，已转成 `domain/kb/manual_zh/缩写与术语表.md`、`指挥术语.md`）——最高，玩家实际在用。",
        "2. **中文舰队包 readme**（`群新手舰队包 v1.12` 的 `使用说明.txt`）——高，作者行文用语。",
        "3. **游戏官方中文本地化**（`zh-CN/cn_*.json`）——**最低**：机翻痕迹明显（点防炮/战情室/损管机柜），简体包里还混着繁体字（石牆、修復、彈艙）。术语表里所有「中文」列都来自这一层，仅作参考。",
        "",
        "## 已知译名冲突（按上表取舍）",
        "",
        "| 概念 | 官方本地化（低） | 玩家表 / readme（优先） |",
        "|---|---|---|",
        "| PDT | 点防炮 | 点防御炮、近防炮、PDT |",
        "| CIC | 战情室、强化型战情室 | CIC、指挥舱 |",
        "| DC Locker | 损管机柜 | 损管舱、损管柜 |",
        "| Chaff | 无「箔条」一词，统一译「诱饵」 | 箔条（EA12 chaff） |",
        "| Soft-kill / Hard-kill | 软杀 / 硬杀（仅教程与 UI 零星出现） | 软杀 / 硬杀（口语高频） |",
        "| 舰船级别 CC/DD/CH… | 无 | CC/DD/CH/BB/FF/FFL/LN/MN/CV/CVL/CVE（玩家约定，见 `舰船级别对照.md`） |",
        "| 导弹口语 S3 / S3F | 无 | S3=SGT-3、S3F=SGM-3 |",
        "| 繁简混用 | 石牆 / 修復 / 彈艙 | 石墙 / 修复 / 弹舱 |",
        "| 炸弹 | 250mm Bomb Shell 译「250mm 炸弹外壳」 | 直接叫「250 航弹」，和 250 RPF 一样用来打小艇 |",
        "",
        "## 玩家用词习惯（很重要）",
        "",
        "- 这款游戏中文社区长期没有可用本地化，**绝大多数中文玩家直接用英文原名与缩写**（Ocello、VLS-2、PDT、softkill）。",
        "- 所以知识库与人设要**同时支持两种输入**：英文名照常检索；中文名按本表映射后再检索。",
        "- **回答跟随提问语言**：用户用中文问就用中文答，但凡是中文译名（尤其是舰级/舰名）要提醒一句「中文译名不一定准确，以英文名为准」。",
        "- 舰船名优先用英文原名，需要时补官方中文；官方中文目前只有零星几条（见下）。",
        "",
        "## 舰船总表（16 艘，阵营 / 装甲 / 结构 / 价格 / 存档键）",
        "",
        "装甲与 DR 取自玩家在游戏面板实测（`domain/data/hull_armour.json`）并与 wiki 记录一致；"
        "价格取 wiki 舰体页；存档键来自 `domain/data/game_names.json`。",
        "",
    ]
    hull_rows: list[list[str]] = []
    for name in sorted(hulls, key=str.lower):
        fields = hulls[name]
        short = name.replace(" Class", "")
        key = names.get("hull_by_wiki", {}).get(name) or names.get("hull_by_wiki", {}).get(short) or ""
        if not key:
            # `hulls.SAVE_KEY` 是唯一来源；不确定就留 "-"，不要在这里编描述。
            key = hu.save_key(short) or "-"
        section = fields.get("_section", "")
        if "Shelter Alliance" in section:
            faction = "SA 专属"
        elif "Outlying" in section or "Protectorate" in section:
            faction = "OSP 专属"
        else:
            faction = "通用"
        thickness = fields.get("Armor Thickness (cm)") or armour.get(short, "-")
        hull_rows.append([
            name.replace(" Class", ""),
            faction,
            str(thickness),
            fields.get("Component DR (%)", "-"),
            fields.get("Structural Integrity", "-"),
            tidy(fields.get("Radar Signature (m2)", "-")),
            fields.get("Point Cost", "-"),
            fields.get("Slots", "-"),
            key,
        ])
    lines.extend(md_table(hull_rows, ["English", "阵营", "装甲 (cm)", "部件 DR", "结构值", "雷达信号", "价格 (pts)", "槽位", "存档键"]))
    lines.append("")
    lines.append(
        "> 15 艘主力舰都在上表；`Shuttle` / `Tugboat` 之类的民船没有装甲数据（5 cm 左右）。"
        "舰级缩写（FFL/DD/CH/LN/CV…）见 `舰船级别对照.md`，本表不重复。"
    )
    lines.append("")

    lines.extend([
        "## 舰级名称（官方 `HULLCLASSIFICATION_*`，在 `cn_ui.json` 里）",
        "",
        "| English | 官方中文 | 建议用法 |",
        "|---|---|---|",
        "| Corvette | 轻型护卫舰 | 口语 FFL |",
        "| Frigate | 护卫舰 | 口语 FF |",
        "| Destroyer | 驱逐舰 | 口语 DD |",
        "| Light Cruiser | 轻型巡洋舰 | 口语 CL |",
        "| Heavy Cruiser | 重型巡洋舰 | 口语 CH |",
        "| Command Cruiser | 指挥巡洋舰 | 口语 CC |",
        "| **Line Ship** | **战列舰** | ⚠️ 官方误译，正确是**线列舰**；口语 LN |",
        "| **Battleship** | **战舰** | ⚠️ 官方误译，正确是**战列舰**；口语 BB |",
        "| Monitor | 炮舰 | 口语 MN |",
        "| Clipper | 飞剪舰 | Ferryman / Draugr |",
        "| Escort Carrier | 护卫航母 | 口语 CVE |",
        "| Light Carrier | 轻型航母 | 口语 CVL |",
        "| Fleet Carrier | 舰队航母 | 口语 CV（Worden） |",
        "| Replenishment Oiler | 补给舰 | Mercator，无缩写 |",
        "",
        "> 官方把 Line Ship 译成「战列舰」、Battleship 译成「战舰」，**两个是反的**。中文里说「线列舰 / 战列舰」区分，英文优先 `line ship` / `battleship`。",
        "",
        "## 舰段与阵营键（存档相关）",
        "",
        "- **线列舰 / 航母的 A/B/C 只是外观**：`Bulk - A - Bow` 与 `B`、`C` 的 14 个槽位**键、尺寸、类型完全一致**（已用 `hull_sockets.json` 逐键比对），所以配装表对三种舰段通用。",
        "- 存档里的 `<FactionKey>` 只有两个值：`Stock/Alliance`（SA）、`Stock/Protectorate`（OSP）。部件键是 `Stock/<部件名>`，**不带阵营前缀**；写了不存在的阵营键会让整船槽位清空。",
        "- 舰体键 `Stock/<HullName>`（例如 `Stock/Axford Heavy Cruiser`，去掉「Class」）。",
        "",
        "> 中文列填“待补”的就是缺译名的；改完告诉我，我重新生成知识库。",
        "",
    ])

    payload: dict[str, list[dict]] = {}

    for prefix, label, kind in NAME_FAMILIES:
        rows: list[list[str]] = []
        records: list[dict] = []
        for key, zh in cn.items():
            if not key.startswith(prefix + "_"):
                continue
            english = en.get(key, "")
            if not english:
                continue
            short_key = key.replace(prefix + "_", "HULLCOMPSHORTNAME_", 1) if prefix == "HULLCOMPNAME" else ""
            short_zh = cn.get(short_key, "") if short_key else ""
            short_en = en.get(short_key, "") if short_key else ""
            ent = wiki.get(english.strip().lower(), {})
            zh_text = TERM_FIX.get(english.strip(), zh.strip())
            fields = comp_fields(english.strip())
            declared, note, suggested, conflict = faction_cell(
                ent.get("faction", "") or fields.get("Faction (wiki logo)", ""),
                observed.get(english.strip(), Counter()),
                FACTION_OVERRIDES.get(english.strip(), ""))
            category = ""
            if kind == "missile":
                section = fields.get("_section", "")
                category = SECTION_ZH.get(section, "")
                if not category and section.startswith("Missile Construction"):
                    tail = section.split("›")[-1].strip().lower()
                    category = {"engines": "引擎", "payload": "战斗部", "avionics package": "航电",
                                "seekers": "引导头", "auxiliary": "辅助"}.get(tail, "弹体 / 引擎")
                if not category:
                    low = english.strip().lower()
                    if "seeker" in low:
                        category = "引导头"
                    elif any(w in low for w in ("engine", "booster", "cruise", "sprint")):
                        category = "引擎"
                    elif any(w in low for w in ("warhead", "blast", "fragmentation", "penetrator",
                                                "impact", "kill mass", "dispenser")):
                        category = "战斗部"
                    elif any(w in low for w in ("guidance", "receiver", "avionics")):
                        category = "航电"
                    elif any(w in low for w in ("jammer", "bottle", "skin", "coating", "module",
                                                "launcher", "decoy")):
                        category = "辅助"
                    else:
                        category = "弹体 / 引擎"
            record = {
                "key": key,
                "category": category,
                "english": english.strip(),
                "chinese": zh_text,
                "short_en": short_en.strip(),
                "short_zh": short_zh.strip(),
                "kind_wiki": ent.get("kind", ""),
                "faction": declared,
                "faction_suggest": suggested,
                "faction_conflict": conflict,
                "faction_note": note,
                "kind": kind,
                "chinese_official": zh.strip(),
                "dims": fields.get("Dimensions", ""),
                "cost": cost_text(fields.get("Cost (pts)", "")),
                "power": power_text(fields) if fields else "",
                "numbers": (
                    f"{storage.get(english.strip(), {}).get('storage_volume_m3', '-')} m³/发"
                    if kind == "ammo" else (key_numbers(fields) if fields else "")
                ),
                "section": fields.get("_section", ""),
            }
            records.append(record)
            if kind == "part":
                rows.append([record["english"], record["chinese"], record["dims"] or "-",
                             record["cost"] or "-", record["power"] or "-", record["numbers"],
                             declared, note, suggested])
            else:
                if kind == "builtin":
                    category = guess_category(record["english"], BUILTIN_CATEGORY, "舰体")
                elif kind == "craft":
                    category = guess_category(record["english"], CRAFT_CATEGORY, "舰载机")
                if kind == "builtin":
                    declared = "随舰体"
                elif kind == "craft":
                    declared = "通用（未单列）"
                rows.append([record["english"], record["chinese"], record["short_en"] or "-",
                             record["short_zh"] or "-", category or "-", declared])
        payload[kind] = records
        if kind == "ammo":
            rows = []
            payload[kind] = records
        if kind == "part":
            best: dict[str, dict] = {}
            for record in records:
                current = best.get(record["english"])
                if current is None or (not current["short_en"] and record["short_en"]):
                    best[record["english"]] = record
            records = list(best.values())
            payload[kind] = records
            rows = [[r["english"], r["chinese"], r["dims"] or "-", r["cost"] or "-", r["power"] or "-",
                     r["numbers"], r["faction"], r["faction_note"], r["faction_suggest"]] for r in records]
        rows.sort(key=lambda r: r[0].lower())
        if kind == "ammo":
            lines.extend(ammo_section(en, cn, munitions, storage, costs))
            continue
        lines.append(f"## {label}（{len(rows)} 条）")
        lines.append("")
        if kind == "part":
            lines.extend(md_table(rows, ["English", "中文", "尺寸(格)", "点数", "供电", "关键数值", "阵营（wiki）", "存档实测", "建议"]))
        else:
            lines.extend(md_table(rows, ["English", "中文", "短名", "短名中文", "类别", "阵营"]))
        lines.append("")

    extra: list[list[str]] = []
    for key, zh in cn.items():
        if not re.match(r"^(MISSILE_|AMMO_|CRAFT_|DEBUFFNAME_|FACTIONNAME_)", key):
            continue
        if key.endswith("_DESC"):
            continue
        english = en.get(key, "")
        if not english or english == zh:
            continue
        if len(english) > 90 or "\n" in english:
            continue
        extra.append([english.strip(), TERM_FIX.get(english.strip(), zh.strip()), key])
    extra.sort(key=lambda r: r[2])
    lines.append(f"## 其它（导弹型号 / 舰载机 / 减益 / 阵营名称，{len(extra)} 条）")
    lines.append("")
    lines.append("`_DESC` 结尾的说明文字已过滤（太长，不适合当术语；它们本来就在知识库里）。")
    lines.append("")
    lines.extend(md_table(extra, ["English", "中文", "key"]))
    lines.append("")

    lines.extend([
        "## 装甲与伤害术语",
        "",
        "| 术语 | 中文 | 含义 / 公式 |",
        "|---|---|---|",
        "| Armour / Armor Thickness | 装甲厚度 | 整船一个值（cm），不分艏侧艉；来源 `hull_armour.json` |",
        "| Effective Armor | 等效装甲 | `Clamp(装甲 / cos(入射角), 0, 装甲×2.5)`，角度越大越厚 |",
        "| Ricochet | 跳弹 | `等效装甲×2 ≥ 伤害 且 入射角 ≥ 80°`，只造成 20% 伤害 |",
        "| Penetration | 穿深 | 弹药字段（cm），`伤害 ≥ 等效装甲×剩余结构比例` 才击穿 |",
        "| Over-penetration | 过穿 | 穿深用完前穿出船体，内部伤害按剩余穿深折算 |",
        "| Interior travel / Density | 内部行程 / 内部密度 | `剩余穿深 = 剩余穿深 / 内部密度`，每 cm 消耗对应穿深 |",
        "| DR (Damage Reduction) | 减伤 | 部件减伤，槽位填充率 20%–60% 之间线性变化，最高 90% |",
        "| DT (Damage Threshold) | 伤害阈值 | 单发伤害 ≤ DT 打不掉这个部件 |",
        "| Reinforced | 加固 | DR 下限 ×0.25 与 Catastrophic 概率相关，具体见 wiki |",
        "| Structure break | 结构断裂 | 命中 < 20 伤害的炮击不计入结构损伤 |",
        "",
        "## 弹库与装载术语",
        "",
        "| 术语 | 中文 | 含义 |",
        "|---|---|---|",
        "| Magazine | 弹库 | 按**体积**存炮弹：`容量(m³) = 每格容量 × 格数`；Reinforced 10 / Bulk 15 / Citadel 3.33 |",
        "| Citadel Magazine | 要塞弹库 | OSP 专属，占 1x3x1×N 格，**槽位至少 6x3x8**，10 m³/格 |",
        "| VLS / CLS | 垂发 / 冷发射 | 按**格数**存导弹：每个 cell 一发，尺寸受发射器限制 |",
        "| MLS / SALS | 导弹弹库 / 软发射 | 导弹也按体积存在弹库里，由 Launcher 装填 |",
        "| Arming missile | 武装弹 | 1 点 1 发的 S1 进攻导弹（SGM-114 Wuffer 是现成模板） |",
        "| Storage Volume | 单发体积 | 炮弹 0.0025–0.8 m³；导弹 S1 4 / S2 20 / S3 30 m³ |",
        "| Rounds per point | 每点发数 | 官方 `1/N`：450mm AP 1/25 = 25 发/点 |",
        "",
        "## 编成与配合术语",
        "",
        "| 术语 | 中文 | 含义 |",
        "|---|---|---|",
        "| Remote track | 遥测航迹 | 靠友军传感器共享的航迹，自己看不到也能打 |",
        "| Lock / Fire control | 锁定 / 火控 | 一艘船同时锁定的目标数受 CIC 限制 |",
        "| Comms jamming | 通信干扰 | 让共享航迹断链：`d ≈ d_A·√(K/P_A·G_A)`，CR75 能把距离压到一半 |",
        "| Hard kill / Soft kill | 硬杀 / 软杀 | 打掉船体 vs 打掉导弹/传感器/航迹 |",
        "| Tank / Anchor | 抗线 / 锚点 | 前排吃伤害的船 |",
        "| Flank / Pincer | 绕侧 / 夹击 | 从侧翼或两面包夹 |",
        "",
    ])

    terms = shorthand_terms()
    lines.append(f"## 玩家口语 → 官方英文（{len(terms)} 条，来自 `query_terms.py`）")
    lines.append("")
    lines.append("这一列是**检索用的映射**，不是官方译名：左边是玩家会说/会打的中文，右边是知识库文档里实际用的英文词。")
    lines.append("")
    lines.extend(md_table([[zh, en_] for zh, en_ in terms], ["中文口语", "映射到的英文"]))
    lines.append("")

    conflicts = [r for r in payload["part"] if r.get("faction_conflict")]
    lines.append(f"## 阵营特例：CC 的特权（{len(conflicts)} 条）")
    lines.append("")
    if conflicts:
        lines.append("下面这些部件 wiki 标了「专属」，但真实存档里另一家也在用。**wiki 是对的**："
                     "`CC`（Ocello Cruiser）的特权是**可以装两家的部件**，所以 OSP 存档里出现 SA 专属件只会发生在 CC 身上，"
                     "换到非 CC 船体就是非法配装。")
        lines.append("配装时按「wiki 声明」执行；只有在配 `CC` 时才允许跨阵营，别把这条特权抄到其它船体上。")
        lines.append("")
        lines.extend(md_table(
            [[r["english"], r["faction"], r["faction_note"], r["faction_suggest"]] for r in conflicts],
            ["部件", "wiki 声明", "存档实测", "配装规则"],
        ))
    else:
        lines.append("没有发现跨阵营使用。")
    lines.append("")

    lines.extend([
        "## 已知缺口",
        "",
        "1. **舰船名没有官方中文名**：本地化里只有 `HULL_*_DESC` 长描述，没有 `HULL_*_NAME`，所以舰名只有英文（本表已给出存档键与数据）。",
        "2. `HULLCOMPSHORTNAME` 只有 108 条，比 145 个部件少，缺的那批在“短名”列会显示 `-`。",
        "3. 界面文案 3669 条已单独导出到 `domain/data/ui_terms_zh_en.csv`，没混进这张表。",
        "4. 舰体自带部件（`Main 01`、`Thruster S 03` 之类）是实例名，没有尺寸/点数数据，只能按舰体查。",
        "5. 部件表 143 条（本地化有 145 条）：`CR10 Antenna` / `CR70 Antenna` 各有长短两个名字，已合并成一行。",
        "6. 「建议」列只是存档统计：通用部件也可能只被一家用过（样本偏差），专属部件被另一家用过则优先怀疑 wiki 图标口径。",
        "",
    ])

    OUT_MD.parent.mkdir(parents=True, exist_ok=True)
    OUT_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")
    with (ROOT / "domain" / "data" / "faction_conflicts.csv").open(
        "w", encoding="utf-8-sig", newline=""
    ) as fh:
        writer = csv.writer(fh)
        writer.writerow(["english", "chinese", "wiki", "observed", "suggestion"])
        for r in conflicts:
            writer.writerow([r["english"], r["chinese"], r["faction"], r["faction_note"], r["faction_suggest"]])
    OUT_JSON.parent.mkdir(parents=True, exist_ok=True)
    OUT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")

    ui_en = load(LOC / "en-US" / "en_ui.json")
    ui_cn = load(LOC / "zh-CN" / "cn_ui.json")
    with OUT_UI.open("w", encoding="utf-8-sig", newline="") as fh:
        writer = csv.writer(fh)
        writer.writerow(["key", "english", "chinese"])
        for key in sorted(set(ui_en) & set(ui_cn)):
            writer.writerow([key, ui_en[key], ui_cn[key]])

    print(f"parts: {len(payload['part'])}  builtin: {len(payload['builtin'])}  "
          f"craft: {len(payload['craft'])}  ammo: {len(payload['ammo'])}  missile: {len(payload['missile'])}")
    print(f"hulls: {len(hull_rows)}  ammo: {len(payload['ammo'])}  faction conflicts: {len(conflicts)}")
    print(f"extra rows: {len(extra)}  shorthand: {len(terms)}")
    print(f"wrote {OUT_MD}")
    print(f"wrote {OUT_JSON}")
    print(f"wrote {OUT_UI} (ui pairs: {len(set(ui_en) & set(ui_cn))})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

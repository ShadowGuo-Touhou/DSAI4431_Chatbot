"""Render the official NEBULOUS wiki (game 0.6.2.6) into English knowledge-base markdown.

Input:  `domain/kb/raw_official/`  (produced by import_official.py from the saved HTML pages)
Output: `domain/kb/docs/`          (wiped first)

Rules
-----
* Source language is English, so the documents stay English: original field names,
  original section names, original prose. No translation.
* Entity tables  -> one document per row, grouped under the wiki section it came from.
* Every wiki section with 2+ rows also gets an index document that lists that whole
  section, so "list all compartments / modules / launchers" questions hit one chunk.
* Non-entity tables and prose under a heading become a section document.
"""

from __future__ import annotations

import json
import re
import shutil
import unicodedata
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]          # domain/
RAW = ROOT / "kb" / "raw_official"
DOCS = ROOT / "kb" / "docs"

VERSION_LABEL = "Official wiki (wiki.hoodedhorse.com), game 0.6.2.6:260903-1430"

SKIP_SECTION_PREFIXES = ("Posture controls",)

# Columns that hold the entity name rather than a stat.
NAME_FIELDS = {
    "Mount", "Weapon", "Compartment", "Module", "Name", "Ship", "Gun",
    "Shell classification", "Missile Body", "Payload", "Avionics Package", "Seeker",
    "Auxiliary", "Mine Body", "Bomb Body", "Rocket Body", "Decoy Body",
}
# Long prose columns rendered as a Notes section instead of a bullet.
NOTE_FIELDS = {"Ability", "Description", "Notes"}

# wiki 名字 → 游戏内字符串（en_assets.json）里实际叫的名字。
# 只收已核实的改号 / 改名；wiki 独有的旧设计与游戏独有的部件见 reference/naming-differences.md
ALIASES = {
    "E55 'Floodlight' Illuminator": "E57 'Floodlight' Illuminator",
    "E15 'Masquerade' Signature Booster": "E15 'Masquerade' Deception Module",
    "CR10": "CR10 Antenna (module) / CR10 Ant (built-in)",
    "CR75": "CR75 Antenna (module) / CR75 Ant (built-in)",
    "250mm Bombshell": "250mm Bomb Shell",
    "CM-4D1 Decoy Container (Line Ship)": "CM-4D2 Decoy Container (Line Ship)",
    "Wake-Homing Seeker (THERM)": "Wake-Thermal Seeker",
}

INDEX_COLUMNS = ["Category", "Class", "Dimensions", "Hitpoints", "Damage Threshold",
                 "Mass (Tonnes)", "Required Power (kW)", "Point Cost", "Cost (pts)"]

# --- tag system ------------------------------------------------------------
# Every entity document opens with a machine-friendly tag line and a one-line
# summary so that (a) Chinese questions resolve through the English term map,
# (b) the model can filter by kind / type / resource effect instead of guessing
# from prose.  Tags are derived from the wiki section + stat columns; nothing is
# invented.
KIND_BY_PREFIX = (
    ("Mounts", "mount"),
    ("Compartments", "compartment"),
    ("Modules", "module"),
    ("Integrated Components", "integrated part"),
    ("Ship hulls", "hull"),
    ("Munitions & Missiles", "munition"),
    ("Ballistic", "munition"),
    ("Missile Construction", "munition"),
    ("Special Missiles", "munition"),
    ("Point Defense", "munition"),
    ("Spacecraft", "spacecraft"),
    ("List of Maps", "map"),
    ("Factions", "faction"),
)

# Faction a hull belongs to, straight from the wiki table it sits in.
HULL_FACTION_BY_SECTION = {
    "Shelter Alliance hulls": ("SA", "Shelter Alliance"),
    "Outlying Systems Protectorate hulls": ("OSP", "Outlying Systems Protectorate"),
}

TYPE_ROLE = {
    "missile launchers": "offence: missiles",
    "point defense weapons": "defence: point defence",
    "projectile weapons": "offence: guns",
    "energy weapons": "offence: energy weapons",
    "spinal weapons": "offence: spinal weapon",
    "communications, ewar, & sensors": "sensors and electronic warfare",
    "sensors": "sensors",
    "radar": "sensors: radar",
    "command": "command",
    "damage control": "survivability: damage control",
    "powerplants": "power generation",
    "propulsion": "mobility",
    "weapon support": "buff: weapons",
    "flight support": "carrier: spacecraft support",
    "storage": "ammunition storage",
    "intelligence": "intelligence",
    "engineering": "engineering",
    "crew": "crew",
    "psyops": "psyops",
}

# Catalog documents: one table per kind so "list every module / compartment"
# questions can be answered from a single chunk.
CATALOGS = (
    ("weapons", "Weapons", "mount", ("Missile Launchers", "Point defense weapons",
                                     "Projectile weapons", "Energy weapons", "Spinal weapons")),
    ("mounts-support", "Support Mounts", "mount",
     ("Communications, Ewar, & Sensors", "Flight Support")),
    ("compartments", "Compartments", "compartment", None),
    ("modules", "Modules", "module", None),
    ("integrated", "Integrated Parts", "integrated part", None),
    ("hulls", "Hulls", "hull", None),
    ("munitions", "Munitions", "munition", None),
    ("craft", "Spacecraft", "spacecraft", None),
    ("maps", "Maps", "map", None),
)

OFFICIAL_COMPONENTS = "https://wiki.hoodedhorse.com/NEBULOUS_Fleet_Command/Components"

# Official pages sometimes still link to the old community wiki (0.5.2.2 data).
# Point those links at the official page so the knowledge base never advertises a stale source.
WIKIDOT_URL = re.compile(r"https?://nebfltcom\.wikidot\.com/[^\s)\]>,]*")


def sanitize(text: str) -> str:
    return WIKIDOT_URL.sub(OFFICIAL_COMPONENTS, text)


def slugify(text: str) -> str:
    text = unicodedata.normalize("NFKD", text)
    text = text.encode("ascii", "ignore").decode("ascii") or text
    text = re.sub(r"[^A-Za-z0-9\u4e00-\u9fff]+", "-", text).lower()
    return re.sub(r"-{2,}", "-", text).strip("-")[:80] or "doc"


def md_table(rows: list[list[str]]) -> str:
    if not rows:
        return ""
    width = max(len(r) for r in rows)
    norm = [r + [""] * (width - len(r)) for r in rows]
    head = norm[0]
    lines = ["| " + " | ".join(c.replace("|", "/") for c in head) + " |",
             "|" + "---|" * width]
    for row in norm[1:]:
        lines.append("| " + " | ".join(c.replace("|", "/") for c in row) + " |")
    return "\n".join(lines)


def _num(text: object) -> float | None:
    if text is None:
        return None
    match = re.search(r"[-+]?\d+(?:\.\d+)?", str(text).replace(",", ""))
    return float(match.group(0)) if match else None


def _pretty(value: float) -> str:
    return f"{value:,.0f}" if abs(value - round(value)) < 0.05 else f"{value:,.1f}"


def split_section(section: str) -> tuple[str, str]:
    parts = [p.strip() for p in section.split("›")]
    return parts[0], (parts[1] if len(parts) > 1 else "")


def kind_of(section: str) -> str:
    head = split_section(section)[0].lower()
    for prefix, kind in KIND_BY_PREFIX:
        if head.startswith(prefix.lower()):
            return kind
    return head


# name -> {faction: fittings}, filled from domain/data/factions.json by main().
FACTION_HINTS: dict[str, dict[str, int]] = {}
FACTION_MIN_FITTINGS = 3
# Hull short name -> faction, taken from the wiki's own hull sections
# ("Shelter Alliance hulls" / "Outlying Systems Protectorate hulls").
HULL_FACTION_BY_SHORT: dict[str, str] = {}
HULL_SECTION_FACTION = {
    "shelter alliance hulls": "Shelter Alliance (SA)",
    "outlying systems protectorate hulls": "Outlying Systems Protectorate (OSP)",
}


def load_hull_factions(entities: dict) -> int:
    """Built-in parts of a hull belong to that hull's faction."""
    for ent in entities.values():
        if kind_of(ent["section"]) != "hull":
            continue
        _, leaf = split_section(ent["section"])
        label = HULL_SECTION_FACTION.get(leaf.lower())
        if not label:
            continue
        short = ent["name"].split()[0]
        HULL_FACTION_BY_SHORT[short] = label
    return len(HULL_FACTION_BY_SHORT)


HULL_ABBR: dict[str, dict] = {}


def load_hull_abbr() -> int:
    """Player-confirmed class abbreviations (domain/data/hull_abbr.json)."""
    path = ROOT / "data" / "hull_abbr.json"
    if not path.exists():
        return 0
    for name, info in json.loads(path.read_text(encoding="utf-8")).items():
        if name.startswith("_"):
            continue
        HULL_ABBR[name.lower()] = info
    return len(HULL_ABBR)


def hull_abbr(name: str) -> str:
    key = name.lower().removesuffix(" class").strip()
    info = HULL_ABBR.get(key)
    return (info or {}).get("abbr", "")


def hull_note(name: str) -> str:
    key = name.lower().removesuffix(" class").strip()
    info = HULL_ABBR.get(key)
    return (info or {}).get("note", "")


def load_faction_hints(path: Path) -> int:
    """Faction membership observed in the player's own saved fleets."""
    if not path.exists():
        return 0
    data = json.loads(path.read_text(encoding="utf-8"))
    for name, counts in (data.get("data") or {}).items():
        FACTION_HINTS[name] = {k: int(v) for k, v in counts.items()}
    return len(FACTION_HINTS)


def lookup_factions(name: str) -> list[tuple[str, int]]:
    key = name if name in FACTION_HINTS else f"Stock/{name}"
    counts = FACTION_HINTS.get(key) or FACTION_HINTS.get(name) or {}
    items = [(f, c) for f, c in counts.items() if c >= FACTION_MIN_FITTINGS]
    items.sort(key=lambda kv: -kv[1])
    return items


def faction_text(name: str, section: str) -> str:
    """Hull faction comes from the wiki table; part faction is mined from saves."""
    _, leaf = split_section(section)
    shortcut = HULL_FACTION_BY_SECTION.get(leaf)
    if shortcut:
        return f"{shortcut[1]} ({shortcut[0]})"
    items = lookup_factions(name)
    if not items:
        return ""
    total = sum(c for _, c in items)
    parts = []
    for faction, count in items[:3]:
        share = 100.0 * count / total
        parts.append(f"{faction} {share:.0f}%" if len(items) > 1 else faction)
    return ", ".join(parts)


def hull_faction(name: str, section: str) -> str:
    _, leaf = split_section(section)
    shortcut = HULL_FACTION_BY_SECTION.get(leaf)
    return f"{shortcut[1]} ({shortcut[0]})" if shortcut else ""


def power_text(fields: dict[str, str]) -> tuple[str, float | None]:
    """Return (display text, signed kW).  Drives generate power via Provided Power."""
    provided = _num(fields.get("Provided Power (kW)"))
    if provided:
        return f"+{_pretty(provided)}", provided
    power = _num(fields.get("Power (kW)"))
    if power is not None:
        return (f"+{_pretty(power)}", power) if power > 0 else (_pretty(power), power)
    required = _num(fields.get("Required Power (kW)"))
    if required is not None:
        return f"-{_pretty(abs(required))}", -abs(required)
    return "", None


def resource_tags(fields: dict[str, str]) -> list[str]:
    tags: list[str] = []
    provided = _num(fields.get("Provided Power (kW)"))
    if provided:
        tags.append(f"provides power {_pretty(provided)} kW")
    power = _num(fields.get("Power (kW)"))
    if power:
        tags.append(f"provides power {_pretty(power)} kW" if power > 0
                    else f"consumes power {_pretty(abs(power))} kW")
    required = _num(fields.get("Required Power (kW)"))
    if required:
        tags.append(f"consumes power {_pretty(abs(required))} kW")
    if fields.get("Commands Enabled"):
        tags.append(f"provides command ({fields['Commands Enabled'].lower()})")
    if _num(fields.get("Intelligence Effort")):
        tags.append("uses intelligence effort")
    if str(fields.get("Reinforced", "")).strip().lower() == "yes":
        tags.append("reinforced")
    if fields.get("Missile Size"):
        tags.append(f"missile size {fields['Missile Size']}")
    return tags


def wiki_faction(ent: dict) -> str:
    """Faction that the wiki page itself assigns: the roundel PNG behind the name.

    One roundel = that faction only, two roundels = both factions, no roundel =
    the page does not restrict it (i.e. available to both).
    """
    return (ent["fields"].get("Faction (wiki logo)") or "").strip()


def tag_line(ent: dict) -> str:
    kind = kind_of(ent["section"])
    head, leaf = split_section(ent["section"])
    category = ent["fields"].get("Category", "")
    type_name = category or leaf
    role = TYPE_ROLE.get((leaf or category).lower(), "")
    parts = [f"kind={kind}"]
    if type_name:
        parts.append(f"type={type_name.lower()}")
    if leaf and category and leaf.lower() != category.lower():
        parts.append(f"section={leaf.lower()}")
    if role:
        parts.append(f"role={role}")
    wiki = wiki_faction(ent)
    if kind == "hull":
        faction = hull_faction(ent["name"], ent["section"])
        if faction:
            parts.append(f"faction={faction}")
    elif kind == "integrated part" and HULL_FACTION_BY_SHORT.get(ent["fields"].get("Ship", "")):
        parts.append(f"faction={HULL_FACTION_BY_SHORT[ent['fields']['Ship']]}")
        parts.append(f"hull={ent['fields']['Ship']}")
    elif wiki:
        parts.append(f"faction={wiki}")
    else:
        observed = faction_text(ent["name"], ent["section"])
        if observed:
            parts.append(f"observed-faction={observed}")
    resources = resource_tags(ent["fields"])
    if resources:
        parts.append("resources=" + ", ".join(resources))
    return "Tags: " + "; ".join(parts)


def _cost_text(fields: dict[str, str]) -> str:
    """`Cost (pts)` sometimes carries '25; 1x Compounding cost' — keep the number."""
    raw = fields.get("Cost (pts)", "")
    value = _num(raw)
    if value is None:
        return ""
    text = f"{_pretty(value)} pts"
    if "compounding" in raw.lower():
        text += " (1x compounding)"
    elif "per" in raw.lower():
        text += f" ({raw.split('per', 1)[1].strip().rstrip(')')} per unit)"
    return text


def summary_line(ent: dict) -> str:
    fields = ent["fields"]
    kind = kind_of(ent["section"])
    head, leaf = split_section(ent["section"])
    category = fields.get("Category", "")
    type_name = category or leaf
    bits: list[str] = []
    if kind == "hull":
        for label, key in (("pts", "Point Cost"), ("t", "Mass (tonnes)"),
                           ("armour cm", "Armor Thickness (cm)"), ("hp", "Structural Integrity"),
                           ("slots", "Slots")):
            if fields.get(key):
                bits.append(f"{fields[key]} {label}")
    elif kind in ("munition", "map"):
        for key in ("Damage (Hp)", "Penetration (cm)", "Range (m)", "Speed (m/s)",
                    "Cost (pts per X amount)", "Base Cost (pts)", "Max Players", "Creator"):
            if fields.get(key):
                bits.append(f"{key}: {fields[key]}")
    else:
        for label, key in (("dims", "Dimensions"), ("hp", "Hitpoints"), ("t", "Mass (Tonnes)")):
            if key and fields.get(key):
                bits.append(f"{fields[key]} {label}")
        cost = _cost_text(fields)
        if cost:
            bits.append(cost)
        shown, _ = power_text(fields)
        if shown:
            bits.append(f"{shown} kW")
        for key in ("Missile Size", "Capacity (cells, minimum)", "Functioning Threshold",
                    "Damage Control Priority", "Commands Enabled",
                    "Thrust (%)", "Top Speed (%)", "Turn Rate (%)"):
            if fields.get(key) and fields[key] not in ("0", ""):
                bits.append(f"{key.lower()} {fields[key]}".rstrip())
    label = f"{kind} ({type_name})" if type_name else kind
    return f"Summary: {label}; " + "; ".join(bits)


def render_entity(ent: dict, count: int) -> str:
    name = ent["name"]
    section = ent["section"]
    return_line = f"Section: {section}"
    if count:
        return_line += f" ({count} entries in this section)"
    lines = [f"# {name}", "", tag_line(ent), summary_line(ent)]
    alias = ALIASES.get(name)
    if alias:
        lines.append(f"Alias (in-game string): {alias}")
    lines += ["", return_line, f"Source: {VERSION_LABEL}", "", "## Stats", ""]
    notes = ""
    for head, value in ent["fields"].items():
        if head in NAME_FIELDS:
            continue
        if head in NOTE_FIELDS:
            notes = value
            continue
        pretty_head = re.sub(r"\(\s+", "(", re.sub(r"\s+\)", ")", head))
        lines.append(f"- {pretty_head}: {value}")
    if notes:
        lines += ["", "## Notes", "", notes]
    derived = firing_block(ent["fields"])
    if derived:
        lines += ["", "## 火力换算", "", *derived]
    return sanitize("\n".join(lines).strip() + "\n")


def firing_block(fields: dict[str, str]) -> list[str]:
    """Turn「每次装填发数 + 装填时间」into sustained rounds per minute.

    ``Autoloader Capacity`` is the number of rounds a completed reload cycle
    feeds (barrels for a turret, cells for a cassette), so sustained rpm is
    ``capacity x 60 / reload``.  Ammunition Elevators shave 15 % off the reload
    each (stat modifiers stack multiplicatively in 0.6.2.6).
    """
    reload_raw = fields.get("Reload time (s)")
    reload_s = _num(reload_raw)
    if reload_s is None or reload_s <= 0:
        return []
    cap_raw = fields.get("Autoloader Capacity")
    capacity = _num(cap_raw) if cap_raw else None
    if capacity is None:
        return [
            f"- 装填时间：{_pretty(reload_s)} s（单发武器，无弹巢/管数数据）",
            f"- 持续射速：60 ÷ {_pretty(reload_s)} = **{_pretty(60.0 / reload_s)} 发/分**",
        ]
    rpm = capacity * 60.0 / reload_s
    out = [
        f"- 每次装填发数（炮管/弹巢数，`Autoloader Capacity`）：{_pretty(capacity)}",
        f"- 装填时间：{_pretty(reload_s)} s",
        f"- 持续射速：{_pretty(capacity)} × 60 ÷ {_pretty(reload_s)} = **{_pretty(rpm)} 发/分**"
        "（理论值，忽略炮管回坐/`Recycle Time`，也忽略升降机加成）",
        "- 弹药升降机（Ammunition Elevators，每台 −15% 装填时间，按乘算叠加）："
        + "；".join(
            f"{n} 台 → 装填 ×{0.85 ** n:.3f} → {_pretty(rpm / 0.85 ** n)} 发/分" for n in (1, 2, 3, 4)
        ),
    ]
    return out


def render_catalog(title: str, ents: list[dict]) -> str:
    """One table with every entry of a kind, so a whole category is one chunk."""
    ents = sorted(ents, key=lambda e: (e["section"], e["name"].lower()))
    kind = kind_of(ents[0]["section"]) if ents else ""
    head = ["Name", "Type", "Role", "Faction", "Power (kW)", "Mass (t)", "Cost (pts)",
            "Hitpoints", "Notes"]
    rows = [head]
    for ent in ents:
        fields = ent["fields"]
        _, leaf = split_section(ent["section"])
        category = fields.get("Category", "")
        type_name = category or leaf
        role = TYPE_ROLE.get((leaf or category).lower(), "")
        power = _num(fields.get("Power (kW)"))
        required = _num(fields.get("Required Power (kW)"))
        provided = _num(fields.get("Provided Power (kW)"))
        if provided is not None:
            power_text = f"+{_pretty(provided)}"
        elif power is not None:
            power_text = f"+{_pretty(power)}" if power > 0 else _pretty(power)
        elif required is not None:
            power_text = f"-{_pretty(abs(required))}"
        else:
            power_text = ""
        note = fields.get("Commands Enabled") or ""
        if kind == "hull":
            faction = hull_faction(ent["name"], ent["section"])
        else:
            faction = wiki_faction(ent)
            if not faction:
                faction = "both (unmarked)"
        rows.append([
            ent["name"], type_name, role, faction, power_text,
            fields.get("Mass (Tonnes)", fields.get("Mass (tonnes)", "")),
            fields.get("Cost (pts)", fields.get("Point Cost", "")),
            fields.get("Hitpoints", fields.get("Structural Integrity", "")),
            note,
        ])
    lines = [f"# Catalog: {title} ({len(ents)} entries)", "", md_table(rows), "",
             f"All {len(ents)} entries of this kind. Power is negative when the part draws power. "
             f"Source: {VERSION_LABEL}.",
             "",
             "Faction rule: a hull's faction is fixed by the game. For parts the faction comes from "
             "the roundel icon next to the part name on the official wiki page (the game's own "
             "rule), so a part marked Shelter Alliance (SA) can only be fitted on SA hulls. Two "
             "roundels = both factions; no roundel / `both (unmarked)` = not restricted."]
    return sanitize("\n".join(lines) + "\n")


def render_faction_catalog(ents: list[dict]) -> dict[str, str]:
    """Parts split by the wiki's own faction marking, so 'who can use X' is answerable.

    One document per faction: a single combined table would be one 20 k-char chunk
    and neither retrieval nor the injected context could carry it.
    """
    sa: list[dict] = []
    osp: list[dict] = []
    both: list[dict] = []
    unrestricted = 0
    for ent in ents:
        if kind_of(ent["section"]) == "hull":
            continue
        wiki = wiki_faction(ent)
        if not wiki:
            unrestricted += 1
        elif "Alliance" in wiki and "Protectorate" in wiki:
            both.append(ent)
        elif "Alliance" in wiki:
            sa.append(ent)
        elif "Protectorate" in wiki:
            osp.append(ent)

    def table(rows_ents: list[dict]) -> str:
        rows = [["Name", "Kind", "Type", "Cost (pts)", "Power (kW)"]]
        for ent in sorted(rows_ents, key=lambda e: (kind_of(e["section"]), e["name"].lower())):
            fields = ent["fields"]
            power_txt, _ = power_text(fields)
            _, leaf = split_section(ent["section"])
            rows.append([
                ent["name"], kind_of(ent["section"]),
                fields.get("Category", "") or leaf,
                fields.get("Cost (pts)", ""),
                power_txt,
            ])
        return md_table(rows)

    def doc(title: str, applies: str, rows_ents: list[dict]) -> str:
        lines = [
            f"# Catalog: {title} ({len(rows_ents)} parts)", "",
            f"Faction rule taken from the official wiki tables: a part whose name carries a "
            f"faction roundel is restricted to that faction's hulls — {applies}. Two roundels "
            f"means both factions. **No roundel means the page does not restrict the part**, so "
            f"it is available to both; across the whole wiki {unrestricted} parts carry no "
            f"faction marking.",
            f"Source: {VERSION_LABEL}", "", "## Table", "", table(rows_ents),
        ]
        return sanitize("\n".join(lines) + "\n")

    out = {
        "faction-sa.md": doc("parts exclusive to Shelter Alliance (SA)",
                             "these can only be fitted on SA hulls", sa),
        "faction-osp.md": doc("parts exclusive to Outlying Systems Protectorate (OSP)",
                              "these can only be fitted on OSP hulls", osp),
        "faction-both.md": doc("parts marked for both factions",
                               "these are marked with both roundels", both),
    }
    return out


def render_index(section: str, ents: list[dict]) -> str:
    """One document per wiki section listing every entry in that section."""
    cols = [c for c in INDEX_COLUMNS if any(c in e["fields"] for e in ents)]
    rows = [["Name", *cols]]
    for e in ents:
        rows.append([e["name"], *[e["fields"].get(c, "") for c in cols]])
    names = ", ".join(e["name"] for e in ents)
    lines = [f"# {section} ({len(ents)} entries)", "",
             f"Section: {section}",
             f"Source: {VERSION_LABEL}",
             "",
             f"All {len(ents)} entries in this section: {names}.",
             "", "## Table", "", md_table(rows)]
    return sanitize("\n".join(lines) + "\n")


def render_section(page: str, heading: str, blocks: list[dict]) -> str:
    title = page if heading == "(页面开头)" else f"{page} › {heading}"
    lines = [f"# {title}", "", f"Source: {VERSION_LABEL}", "", "## Body", ""]
    body: list[str] = []
    for blk in blocks:
        if blk["kind"] == "table":
            if blk.get("entity_table"):
                continue
            body.append(md_table(blk["rows"]))
        elif blk["kind"] == "li":
            body.append(("  " * max(0, blk["depth"] - 1)) + f"- {blk['text']}")
        else:
            body.append(blk["text"])
    text = "\n\n".join(x for x in body if x.strip())
    if len(text) < 120:
        return ""
    return sanitize("\n".join(lines) + text + "\n")


def game_only_names() -> tuple[list[str], list[str]]:
    """Names the installed build has but the wiki never lists (for the reverse lookup doc)."""
    import check_conflicts as cc

    groups = cc.load_loc()
    wiki = cc.load_wiki()
    modules_only = {k: v for k, v in groups["part"].items() if k.startswith("HULLCOMPNAME_")}
    parts = cc.match_names(wiki["part"], modules_only)
    munitions = cc.match_names(wiki["munition"], {**groups["ammo"], **groups["missile"]})
    return (
        sorted({value for _, value, _ in parts["game_only"]}),
        sorted({value for _, value, _ in munitions["game_only"]}),
    )


def write_game_only(out: Path) -> int:
    parts, munitions = game_only_names()
    lines = [
        "# Names that exist in the game but not on the wiki",
        "",
        "Source: `en_assets.json` of the installed build (game 0.6.2.6:260903-1430) compared against "
        "the saved official wiki pages. Built-in hull instances (`Main 01`, `Thruster 03`, "
        "`TR Radar Panel` ...) are covered by `reference/naming-differences.md` and are not repeated "
        "here.",
        "",
        "## Parts and modules",
        "",
        "These have in-game strings but no wiki row, so no stats are available:",
        "",
    ]
    lines += [f"- {name}" for name in parts] or ["- (none)"]
    lines += ["", "## Munitions, missile parts and decoys", "",
              "The wiki has no row for these, which is why missile building advice quotes the "
              "construction tables (bodies, payloads, avionics, seekers) instead of these names:", ""]
    lines += [f"- {name}" for name in munitions] or ["- (none)"]
    lines += ["", "## Rule", "",
              "If asked about a name in these lists, say the wiki does not document it and quote "
              "only what the construction tables do cover. Never invent numbers for them.", ""]
    (out / "game-only-names.md").write_text("\n".join(lines), encoding="utf-8")
    return 1


def render_power_catalog(ents: list[dict], *, supply: bool,
                         lo: float = 0.0, hi: float | None = None) -> str:
    """Every part with a power figure, sorted by absolute kW.

    Split by magnitude so each table stays inside one injectable chunk.
    """
    picked: list[tuple[float, dict, float]] = []
    for ent in ents:
        _, kw = power_text(ent["fields"])
        if kw is None:
            continue
        if supply and kw <= 0:
            continue
        if not supply and kw >= 0:
            continue
        size = abs(kw)
        if size < lo or (hi is not None and size >= hi):
            continue
        picked.append((size, ent, kw))
    picked.sort(key=lambda item: (-item[0], item[1]["name"].lower()))
    if not picked:
        return ""
    what = "provide" if supply else "consume"
    if supply:
        scope = ""
    elif hi is None:
        scope = " (at least {:.0f} kW)".format(lo)
    else:
        scope = " (under {:.0f} kW)".format(hi)
    rows = [["Name", "Kind", "Role", "Faction", "Power (kW)", "Cost (pts)", "Mass (t)"]]
    for _, ent, kw in picked:
        fields = ent["fields"]
        _, leaf = split_section(ent["section"])
        category = fields.get("Category", "")
        role = TYPE_ROLE.get((leaf or category).lower(), "")
        faction = wiki_faction(ent) or "both (unmarked)"
        rows.append([
            ent["name"], kind_of(ent["section"]), role or leaf,
            faction.replace("Shelter Alliance (SA)", "SA").replace("Outlying Systems Protectorate (OSP)", "OSP"),
            _pretty(kw), _cost_text(fields), _pretty(_num(fields.get("Mass (Tonnes)")) or 0),
        ])
    lines = [
        f"# Parts that {what} power{scope} ({len(picked)} entries)",
        "",
        md_table(rows),
        "",
        f"Every part in the knowledge base that {what}s power{scope}, sorted by absolute power draw. "
        f"Source: {VERSION_LABEL}",
        "",
    ]
    return sanitize("\n".join(lines))


def ammo_price_by_caliber() -> dict[int, float]:
    """口径 → 每发点数（来自 `domain/data/ammo_costs.json`，由 build_ammo_costs.py 生成）。"""
    path = Path(__file__).resolve().parents[1] / "data" / "ammo_costs.json"
    if not path.exists():
        return {}
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return {}
    out: dict[int, float] = {}
    for name, price in (data.get("shells") or {}).items():
        m = re.search(r"(\d+)\s*mm", name)
        if m and float(price) > 0:
            out.setdefault(int(m.group(1)), float(price))
    return out


def render_caliber_catalog(ents: list[dict]) -> str:
    """Cannons grouped by shell caliber, with the dimensions a socket must fit."""
    picked = []
    for ent in ents:
        fields = ent["fields"]
        ammo = str(fields.get("Ammo") or "")
        m = re.search(r"(\d+)\s*mm", ammo)
        if not m:
            continue
        picked.append((int(m.group(1)), ent))
    if not picked:
        return ""
    picked.sort(key=lambda item: (-item[0], item[1]["name"].lower()))
    rows = [["Caliber", "Name", "Dimensions", "Cost (pts)", "Power (kW)", "Mass (t)", "Faction"]]
    for cal, ent in picked:
        fields = ent["fields"]
        _, kw = power_text(fields)
        rows.append([
            f"{cal} mm", ent["name"], str(fields.get("Dimensions") or "-"),
            _pretty(_num(fields.get("Cost (pts)")) or 0),
            _pretty(kw) if kw is not None else "-",
            _pretty(_num(fields.get("Mass (Tonnes)")) or 0),
            (wiki_faction(ent) or "both (unmarked)")
             .replace("Shelter Alliance (SA)", "SA")
             .replace("Outlying Systems Protectorate (OSP)", "OSP"),
        ])
    lines = [
        f"# Cannons by shell caliber ({len(picked)} entries)",
        "",
        "Keywords: cannon, gun, artillery, caliber, 火炮, 炮, 口径, 450mm, 250mm, 120mm, 100mm, 75mm",
        "",
        "The caliber comes from each cannon's Ammo field (Ballistic/Chemical - 450mm). "
        "Dimensions are the footprint the mounting socket must accept: compare them to the "
        "socket table of the hull (sockets/<hull>.md); a part fits when every dimension fits "
        "after rotating around the vertical axis.",
        "",
        f"Source: {VERSION_LABEL}.",
        "",
    ]
    by_caliber: dict[int, list[dict]] = {}
    for cal, ent in picked:
        by_caliber.setdefault(cal, []).append(ent)
    prices = ammo_price_by_caliber()
    for cal in sorted(by_caliber, reverse=True):
        ents = by_caliber[cal]
        lines += [
            f"## {cal} mm cannons ({len(ents)} entries)",
            "",
        ]
        per_round = prices.get(cal)
        if per_round:
            lines += [
                f"弹药单价：**{per_round:g} 点/发**（{int(round(1 / per_round))} 发 = 1 点，"
                f"100 发 ≈ {100 * per_round:g} 点，1000 发 ≈ {1000 * per_round:g} 点）。"
                "换口径/换弹种不影响这个单价的量级，换算见 `zh/弹药点数表.md`。",
                "",
            ]
        lines += [
            md_table([
                ["Name", "Dimensions", "Cost (pts)", "Power (kW)", "Mass (t)", "Faction"],
            ] + [
                [
                    ent["name"], str(ent["fields"].get("Dimensions") or "-"),
                    _pretty(_num(ent["fields"].get("Cost (pts)")) or 0),
                    _pretty(power_text(ent["fields"])[1])
                    if power_text(ent["fields"])[1] is not None else "-",
                    _pretty(_num(ent["fields"].get("Mass (Tonnes)")) or 0),
                    (wiki_faction(ent) or "both (unmarked)")
                    .replace("Shelter Alliance (SA)", "SA")
                    .replace("Outlying Systems Protectorate (OSP)", "OSP"),
                ]
                for ent in ents
            ]),
            "",
        ]
    return "\n".join(lines)


def render_cost_catalog(ents: list[dict]) -> str:
    """Single list: every part and munition that has a point cost, most expensive first."""
    picked: list[tuple[float, dict]] = []
    for ent in ents:
        fields = ent["fields"]
        cost = _num(fields.get("Cost (pts)")) 
        if cost is None:
            cost = _num(fields.get("Cost"))
        if cost is None:
            continue
        picked.append((cost, ent))
    picked.sort(key=lambda item: (-item[0], item[1]["name"].lower()))
    if not picked:
        return ""
    rows = [["Name", "Kind", "Role", "Faction", "Cost (pts)", "Power (kW)", "Mass (t)", "Hitpoints"]]
    for cost, ent in picked:
        fields = ent["fields"]
        _, leaf = split_section(ent["section"])
        role = TYPE_ROLE.get((leaf or fields.get("Category", "")).lower(), "") or leaf
        _, kw = power_text(fields)
        rows.append([
            ent["name"], kind_of(ent["section"]), role,
            (wiki_faction(ent) or "both (unmarked)")
             .replace("Shelter Alliance (SA)", "SA")
             .replace("Outlying Systems Protectorate (OSP)", "OSP"),
            _pretty(cost), _pretty(kw) if kw is not None else "-",
            _pretty(_num(fields.get("Mass (Tonnes)")) or 0),
            _pretty(_num(fields.get("Hitpoints")) or 0),
        ])
    lines = [
        f"# All parts by point cost, most expensive first ({len(picked)} entries)",
        "",
        md_table(rows),
        "",
        "One row per part or munition that carries a point cost. Component cost is the "
        "price of one item; a hull prices separately. Munitions are per round where the "
        "wiki lists them. Sorted from most to least expensive.",
        "",
        f"Source: {VERSION_LABEL}, plus the player-built templates where noted.",
        "",
    ]
    return sanitize("\n".join(lines))


def render_hull_catalog(title: str, ents: list[dict], *, faction: str | None) -> str:
    """One row per hull: class abbreviation, cost, durability, slots."""
    rows = [["Class", "Hull", "Point Cost", "Mass (t)", "Integrity (hp)", "Armor (cm)",
             "Signature (m2)", "Crew", "Slots"]]
    picked = []
    for ent in ents:
        if kind_of(ent["section"]) != "hull":
            continue
        label = hull_faction(ent["name"], ent["section"])
        if faction and faction not in label:
            continue
        picked.append((_num(ent["fields"].get("Point Cost")) or 0.0, ent))
    picked.sort(key=lambda item: (-item[0], item[1]["name"].lower()))
    for _, ent in picked:
        f = ent["fields"]
        rows.append([
            hull_abbr(ent["name"]) or "-",
            ent["name"].removesuffix(" Class"),
            _pretty(_num(f.get("Point Cost")) or 0),
            _pretty(_num(f.get("Mass (tonnes)")) or 0),
            _pretty(_num(f.get("Structural Integrity")) or 0),
            _pretty(_num(f.get("Armor Thickness (cm)")) or 0),
            _pretty(_num(f.get("Radar Signature (m2)")) or 0),
            _pretty(_num(f.get("Crew")) or 0),
            re.sub(r"(\d+)\s+Mounts\s+(\d+)\s+Compartments\s+(\d+)\s+Modules",
                    r"\1 / \2 / \3", f.get("Slots", "-")),
        ])
    if not picked:
        return ""
    names = ", ".join(ent["name"].removesuffix(" Class") for _, ent in picked)
    lines = [
        f"# {title} ({len(picked)} entries)",
        "",
        md_table(rows),
        "",
        f"Hulls covered: {names}. Point cost is the hull price alone; weapons, modules and "
        f"compartments are priced separately. Slots are printed as Mounts / Compartments / Modules.",
        "",
        f"Source: {VERSION_LABEL}",
        "",
    ]
    return sanitize("\n".join(lines))


def write_missile_storage(out: Path) -> int:
    lines = [
        "# Missiles: launchers, storage and the designer",
        "",
        f"Source: {VERSION_LABEL}; launcher capacities are read from each launcher's own Stats block.",
        "",
        "## How a missile gets to the target",
        "",
        "A missile is a special munition. It is not fired from a gun: it is launched by a missile "
        "launcher, and the player builds it in the in-game missile designer from a body, a payload, "
        "avionics and a seeker package.",
        "",
        "## VLS and TLS: cells inside the launcher",
        "",
        "Vertical and trainable launch systems keep their missiles in the launcher itself. Each "
        "launcher's Stats block has `Capacity (cells, minimum)` and `Missile Size`; the wiki's "
        "\"minimum\" is the cell count in the launcher's own footprint, and the real ceiling is that "
        "count scaled by the slot (empty cells are the floor, never the ceiling). Fixed-cell launchers "
        "do not scale: VLS-1-23 always holds 23 S1 cells, VLS-1-46 always 46. Resizable ones "
        "(VLS-2 / VLS-3 / CLS-3) scale as `floor(slot.x / module.x) * floor(slot.z / module.z) * "
        "cells_per_module` — see `zh/弹药装载与弹库规则.md` for the measured table "
        "(VLS-2: 16 cells in a 3x4x3 slot, 24 in 3x4x5, 64 in 6x4x6, 80 in 8x7x8; VLS-3 and CLS-3 "
        "hold exactly a quarter of that). When planning a VLS/TLS ship, look up the slot, take the "
        "cell count, and put one missile of the matching size in each cell.",
        "",
        "## MLS and SALS: magazine-fed",
        "",
        "Missile launch systems that draw from the ship's ammunition storage do not carry cells of "
        "their own: their missiles compete with shells for the same magazine space. For these, plan "
        "magazine capacity and ammunition mixes, not launcher cells.",
        "",
        "## Working rule for missile builds",
        "",
        "Use the player-supplied missile templates as the reference loadout. Change only the seeker "
        "package the player asks for (primary, secondary, validation) and recompute the point cost "
        "from the component table. Do not design a missile from scratch unless the player explicitly "
        "asks for a new design; the named designs on the wiki are examples, not fixed loadouts.",
        "",
    ]
    (out / "missile-storage.md").write_text("\n".join(lines), encoding="utf-8")
    return 1


def write_reference() -> int:
    """Cross-check the wiki against the installed game's string table."""
    out = DOCS / "reference"
    out.mkdir(parents=True, exist_ok=True)
    lines = [
        "# Wiki vs in-game naming differences",
        "",
        f"Source: {VERSION_LABEL}; game strings from "
        "`Nebulous_Data/StreamingAssets/Localization/en-US/en_assets.json` (same installed build).",
        "",
        "## How this was checked",
        "",
        "Every name on the official wiki was normalised (lower case, punctuation and apostrophes "
        "dropped) and matched against the game's own strings: `HULLCOMPNAME_*` for mounts, "
        "compartments and modules, `HULLPARTNAME_*` for built-in hull parts, `AMMONAME_*` for "
        "munitions and `MISSILECOMPNAME_*` for missile components. Numbers and roles always come "
        "from the wiki; the in-game name always comes from these strings.",
        "",
        "## Renamed or renumbered (the game wins)",
        "",
        "- The wiki row **E55 'Floodlight' Illuminator** is a wiki typo: in the game E55 is the "
        "**'Spotlight'** and E57 is the **'Floodlight' Illuminator**. The stats on that row belong to "
        "the Floodlight, so quote them as E57; use E55 only for the Spotlight.",
        "- E15 'Masquerade' Signature Booster (wiki) = **E15 'Masquerade' Deception Module** in game. "
        "Same device, different function word.",
        "- **CR10**: available to both factions, and most hulls also carry an integrated CR10 - that is "
        "why two entries exist. **CR70**: Shelter Alliance (ANS) only. **CR75**: only exists as an "
        "integrated part on some hulls, there is no CR75 module.",
        "",
        "## Spellings that differ",
        "",
        "- 250mm Bombshell (wiki) = **250mm Bomb Shell** in game.",
        "- CM-4D1 Decoy Container (Line Ship) (wiki) = **CM-4D2 Decoy Container (Line Ship)** in game.",
        "- Wake-Homing Seeker (THERM) (wiki) = **Wake-Thermal Seeker** in game.",
        "",
        "- Missile engines and missile class names: SGM-1/SDM-1/SGM-2/SDM-2/SGM-H-2/SGM-H-3/SGT-3/CM-4 "
        "engines and boosters, plus Size 1/2/3 Missile, Size 3 Torpedo and Size 1/2/3 Hybrid Missile.",
        "- Decoys and dispensed munitions: EA12 Chaff, EA14 Chaff, EA20 Flare, EA99 'Conure' Active "
        "Decoy, 250mm Flak Shell, 500mm Fragmentation Block, Submunition Dispenser, Kinetic Kill Mass.",
        "",
        "## On the wiki but not in the game strings",
        "",
        "- Named missile designs: SGM-100 Balestra, SDM-100 Lunge, SSM-100 Remise, SGM-200 Tempest, "
        "SDM-200 Typhoon, SGM-300 Flail, SGT-300 Pilum, SGM-H-200 Cyclone, SGM-H-300 Atlatl, "
        "CM-400 Container, CM-S-400 Container. The game builds missiles from bodies, payloads, "
        "avionics and seekers, so these are wiki examples rather than fixed loadouts.",
        "- Seeker variants: Fixed Anti-Radiation Seeker (Home On Jam) and (Pulsed Radar). The game "
        "only names one `Fixed Anti-Radiation Seeker`; the two variants have no separate entry.",
        "- Radar Array and Resupply are listed as built-in hull parts with no matching game string.",
        "",
        "## Built-in hull parts: function names vs instance names",
        "",
        "The wiki lists one row per function per hull (`Sprinter Main`, `Levy Large Pad`, `Radar "
        "Panel`), while the game names each physical instance (`Main 01`..`Main 10`, `Thruster "
        "01`..`Thruster 20`, `Thruster S/B 01`..`10`, `Braking S/B 01`..`10`, `Small Pad "
        "01`..`15`, `Large Pad 01`..`10`, and 12 radar-panel positions such as `TR Radar Panel`, "
        "`BL Radar Panel`). There is no name-level join between the two, and the wiki gives no "
        "position for any of them, so slot positions are still unknown.",
        "",
        "## Rule for answers",
        "",
        "The installed game is the default source. Use the game's names, the game's mechanics and the "
        "game's launcher/storage behaviour; quote wiki numbers only where they do not contradict the "
        "game, and always say which build the numbers come from (0.6.2.6:260903-1430). When a name "
        "does not exist in the game at all, say so instead of inventing numbers.",
        "",
    ]
    (out / "naming-differences.md").write_text("\n".join(lines), encoding="utf-8")
    return 1 + write_game_only(out) + write_missile_storage(out)


def write_baseline() -> int:
    """The `Baseline: For all ships` block of Ship Builds.txt, as a KB doc.

    Generated from domain/spec/ship_builds.json on every rebuild, so edits to the
    source file can never go stale in the KB.
    """
    spec_path = ROOT / "spec" / "ship_builds.json"
    if not spec_path.is_file():
        return 0
    spec = json.loads(spec_path.read_text(encoding="utf-8"))
    base = spec.get("baseline") or {}
    out = DOCS / "reference"
    out.mkdir(parents=True, exist_ok=True)
    lines = [
        "# Baseline requirements (every ship, before its class rules)",
        "",
        "Keywords: baseline, all ships, 基线, 通用要求, 通用基线, 每一艘船, 硬性要求, 必须满足, "
        "must, should, avoid, 合格, 不合规, 合法性",
        "Summary: 所有舰船的通用基线（Ship Builds.txt 的 Baseline 段）：must 必须全部满足才算合法配装，"
        "should 是良好标准，avoid 是要避免的做法；先过基线，再对照 builds/<class>.md 的舰级要求。",
        "",
        "Source: `other info/Ship Builds.txt`, section 「Baseline: For all ships」. "
        "Class-specific rules live in `builds/<class>.md`; both apply, baseline first.",
        "",
        "## Must (missing any of these means the ship is not a legal build)",
        "",
    ]
    lines += [f"- {item}" for item in base.get("must", [])] or ["- (none)"]
    lines += ["", "## Should (a ship that misses these is a flawed build, not an illegal one)", ""]
    lines += [f"- {item}" for item in base.get("should", [])] or ["- (none)"]
    avoid = base.get("avoid", [])
    if avoid:
        lines += ["", "## Avoid", ""]
        lines += [f"- {item}" for item in avoid]
    lines += [
        "",
        "## How to use this in a review",
        "",
        "1. Check every Must first; report each failed Must explicitly instead of giving a score.",
        "2. `Required power < 110% provided` is the 「one switchable part over budget」 allowance: "
        "jammers and radars can be shut down, cannons and drives cannot (see "
        "`zh/供电预算与(n-1)规则.md`).",
        "3. Ammo-duration rules (10 min cannons, 1 min hardkill PDT) cannot be computed from a "
        "`.fleet` file — say so instead of inventing a number.",
        "4. Only after the baseline passes, check the class rules.",
        "",
    ]
    (out / "baseline-requirements.md").write_text("\n".join(lines), encoding="utf-8")
    return 1


def main() -> int:
    if DOCS.exists():
        shutil.rmtree(DOCS)
    DOCS.mkdir(parents=True)

    hints = load_faction_hints(ROOT / "data" / "factions.json")
    print(f"hull abbreviations {load_hull_abbr()}")
    print(f"faction hints {hints}")

    entities: dict[tuple[str, str], dict] = {}
    for path in sorted(RAW.rglob("*.json")):
        rec = json.loads(path.read_text(encoding="utf-8"))
        cat = rec["category"]
        page = rec["title"]
        for ent in rec.get("entities") or []:
            key = (cat, slugify(ent["name"]))
            if key in entities:
                kept = entities[key]
                for head, value in ent["fields"].items():
                    kept["fields"].setdefault(head, value)
            else:
                entities[key] = {"name": ent["name"], "section": ent["section"],
                                 "fields": dict(ent["fields"]), "page": page, "cat": cat}

    counts: dict[tuple[str, str], int] = {}
    for ent in entities.values():
        k = (ent["cat"], ent["section"])
        counts[k] = counts.get(k, 0) + 1

    print(f"hull factions {load_hull_factions(entities)}")

    n_ent = n_idx = n_sec = 0
    for (cat, slug), ent in entities.items():
        out_dir = DOCS / cat
        out_dir.mkdir(parents=True, exist_ok=True)
        (out_dir / f"{slug}.md").write_text(
            render_entity(ent, counts[(cat, ent["section"])]), encoding="utf-8")
        n_ent += 1

    groups: dict[tuple[str, str], list[dict]] = {}
    for ent in entities.values():
        groups.setdefault((ent["cat"], ent["section"]), []).append(ent)
    for (cat, section), ents in groups.items():
        if len(ents) < 2:
            continue
        out_dir = DOCS / cat
        (out_dir / f"_index--{slugify(section)}.md").write_text(
            render_index(section, ents), encoding="utf-8")
        n_idx += 1

    # Catalog documents: one table per kind (whole category in a single chunk).
    catalog_dir = DOCS / "catalog"
    catalog_dir.mkdir(parents=True, exist_ok=True)
    n_cat = 0
    for slug, title, kind, types in CATALOGS:
        picked = []
        for ent in entities.values():
            if kind_of(ent["section"]) != kind:
                continue
            if types is not None:
                _, leaf = split_section(ent["section"])
                if leaf not in types:
                    continue
            picked.append(ent)
        if len(picked) < 2:
            continue
        (catalog_dir / f"{slug}.md").write_text(
            render_catalog(title, picked), encoding="utf-8")
        n_cat += 1

    # Hull tables: two per faction plus one sorted by point cost (class abbreviations
    # come from domain/data/hull_abbr.json, written by the user).
    hull_ents = [ent for ent in entities.values() if kind_of(ent["section"]) == "hull"]
    for slug, title, faction in (
        ("hulls-sa", "Shelter Alliance (SA / ANS) hulls", "Shelter Alliance"),
        ("hulls-osp", "Outlying Systems Protectorate (OSP) hulls", "Protectorate"),
        ("hulls-by-cost", "All hulls by point cost, most expensive first", None),
    ):
        doc = render_hull_catalog(title, hull_ents, faction=faction)
        if doc:
            (catalog_dir / f"{slug}.md").write_text(doc, encoding="utf-8")
            n_cat += 1

    cost_doc = render_cost_catalog(list(entities.values()))
    if cost_doc:
        (catalog_dir / "parts-by-cost.md").write_text(cost_doc, encoding="utf-8")
        n_cat += 1

    cal_doc = render_caliber_catalog(list(entities.values()))
    if cal_doc:
        (catalog_dir / "cannons-by-caliber.md").write_text(cal_doc, encoding="utf-8")
        n_cat += 1

    # Missile templates written by import_missiles.py (player's .missile saves).
    missile_src = ROOT / "kb" / "missile_templates"
    n_missile = 0
    if missile_src.exists():
        target = DOCS / "missile"
        target.mkdir(parents=True, exist_ok=True)
        for src in sorted(missile_src.glob("*.md")):
            shutil.copy2(src, target / src.name)
            n_missile += 1

    # Power lookup tables: the "list every part that draws power" question needs a
    # single table, not one row per part document.
    for slug, title, supply, lo, hi in (
        ("by-power-consume", "Parts that consume power (high)", False, 500.0, None),
        ("by-power-consume-low", "Parts that consume power (low)", False, 0.0, 500.0),
        ("by-power-supply", "Parts that provide power", True, 0.0, None),
    ):
        text = render_power_catalog(list(entities.values()), supply=supply, lo=lo, hi=hi)
        if text:
            (catalog_dir / f"{slug}.md").write_text(text, encoding="utf-8")
            n_cat += 1

    # Faction catalogs: parts the wiki marks as exclusive vs unrestricted.
    for name, text in render_faction_catalog(list(entities.values())).items():
        (catalog_dir / name).write_text(text, encoding="utf-8")
        n_cat += 1

    for path in sorted(RAW.rglob("*.json")):
        rec = json.loads(path.read_text(encoding="utf-8"))
        cat = rec["category"]
        page = rec["title"]
        out_dir = DOCS / cat
        out_dir.mkdir(parents=True, exist_ok=True)
        for sec in rec.get("sections") or []:
            if sec["heading"].startswith(SKIP_SECTION_PREFIXES):
                continue
            text = render_section(page, sec["heading"], sec["blocks"])
            if not text:
                continue
            slug = f"{slugify(page)}--{slugify(sec['heading'])}"
            (out_dir / f"{slug}.md").write_text(text, encoding="utf-8")
            n_sec += 1

    # 玩家整理的中文资料（非官方，来源标在文首），单独放 zh/ 下，与官方 wiki 分开
    manual = ROOT / "kb" / "manual_zh"
    n_zh = 0
    if manual.is_dir():
        zh_dir = DOCS / "zh"
        zh_dir.mkdir(parents=True, exist_ok=True)
        for path in sorted(manual.glob("*.md")):
            shutil.copyfile(path, zh_dir / path.name)
            n_zh += 1

    n_ref = write_reference()
    n_ref += write_baseline()

    # 舰级模板（由 match 的实战舰队归纳，tools/build_templates.py 生成）
    builds_src = ROOT / "kb" / "builds"
    n_builds = 0
    if builds_src.is_dir():
        build_dir = DOCS / "builds"
        build_dir.mkdir(parents=True, exist_ok=True)
        for path in sorted(builds_src.glob("*.md")):
            shutil.copyfile(path, build_dir / path.name)
            n_builds += 1

    # 舰体插槽表（tools/write_sockets.py 生成）
    sock_src = ROOT / "kb" / "socket_docs"
    n_sock = 0
    if sock_src.is_dir():
        sock_dir = DOCS / "sockets"
        sock_dir.mkdir(parents=True, exist_ok=True)
        for path in sorted(sock_src.glob("*.md")):
            shutil.copyfile(path, sock_dir / path.name)
            n_sock += 1

    print(f"entity docs {n_ent}, section indexes {n_idx}, catalogs {n_cat}, "
          f"article docs {n_sec}, zh guides {n_zh}, build templates {n_builds}, sockets {n_sock}, "
          f"reference {n_ref} -> {DOCS}")
    total = sum(len(p.read_text(encoding="utf-8")) for p in DOCS.rglob("*.md"))
    print(f"total {len(list(DOCS.rglob('*.md')))} docs / {total / 1000:.1f} k chars")
    print(f"missile templates {n_missile}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

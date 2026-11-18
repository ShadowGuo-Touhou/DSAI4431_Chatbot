"""Turn the player's `.missile` template files into knowledge-base documents.

Source of truth: `other info/missles/*.missile` (the game's own XML save format) plus
`missles templates.txt` (the shorthand list of body/payload combinations the player keeps).

Output: `domain/kb/missile_templates/<slug>.md` + `_catalog.md`, copied into the KB by
`build_official.py`.

    python domain/tools/import_missiles.py
"""

from __future__ import annotations

import json
import re
import shutil
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SRC = ROOT / "other info" / "missles"
OUT = ROOT / "domain" / "kb" / "missile_templates"

SRC_LINE = "Player-built missile template (.missile save file); seeker/guidance settings and point cost read from the file."

TAG = re.compile(r"<[^>]+>")
TOKEN = re.compile(r"\$([A-Z0-9_]+)(?:\|([^|]*)\|)?")

TOKEN_WORDS = {
    "UNIT_METERSPERSEC": "m/s",
    "UNIT_METERS": "m",
    "UNIT_CENTIMETERS": "cm",
    "UNIT_HP": "hp",
    "UNIT_SECONDS": "s",
    "UNIT_GS": "G",
    "UNIT_DEGREES": "deg",
}


def token_text(match: re.Match) -> str:
    name, inline = match.group(1), match.group(2)
    if inline:
        return inline
    if name in TOKEN_WORDS:
        return TOKEN_WORDS[name]
    label = name
    for prefix in ("MISSILESTAT_", "MISSILEENGINE_", "MISSILEGUIDANCE_", "MISSILESEEKER_",
                   "MISSILEWARHEAD_", "UNIT_"):
        label = label.removeprefix(prefix)
    label = label.replace("_", " ").strip().lower()
    return label


def clean(text: str) -> str:
    text = text or ""
    text = text.replace("&lt;", "<").replace("&gt;", ">").replace("&amp;", "&")
    text = TOKEN.sub(token_text, text)
    text = TAG.sub("", text)
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


def inner(elem: ET.Element | None) -> str:
    return (elem.text or "").strip() if elem is not None else ""


def parse(path: Path) -> dict:
    tree = ET.parse(path)
    root = tree.getroot()
    name = inner(root.find("AssociatedTemplateName")) or path.stem
    cost = inner(root.find("Cost"))
    body = inner(root.find("BodyKey")).removeprefix("Stock/")
    sockets = []
    for sock in root.findall("./Sockets/MissileSocket"):
        size = inner(sock.find("Size"))
        comp = sock.find("InstalledComponent")
        if comp is None:
            sockets.append({"size": size, "type": "", "key": "", "settings": {}})
            continue
        kind = ""
        for key, value in comp.attrib.items():
            if key.endswith("type"):
                kind = value
        key = inner(comp.find("ComponentKey"))
        settings: dict[str, str] = {}
        for child in comp:
            tag = child.tag.split("}")[-1]
            if tag in ("ComponentKey", "BalanceValues"):
                continue
            if tag == "DefensiveDoctrine":
                parts = [f"{c.tag.split('}')[-1]}={inner(c)}" for c in child if inner(c)]
                if parts:
                    settings["DefensiveDoctrine"] = ", ".join(parts)
                continue
            text = inner(child)
            if text:
                settings[tag] = text
        sockets.append({"size": size, "type": kind, "key": key.removeprefix("Stock/"),
                        "settings": settings})
    return {
        "file": path.name,
        "name": name,
        "designation": inner(root.find("Designation")),
        "nickname": inner(root.find("Nickname")),
        "description": clean(inner(root.find("Description"))),
        "long": clean(inner(root.find("LongDescription"))),
        "cost": cost,
        "body": body,
        "sockets": sockets,
    }


def load_component_costs() -> dict[str, float]:
    """Point cost per missile component, from the wiki's Missile Construction tables."""
    costs: dict[str, float] = {}
    src = ROOT / "domain" / "kb" / "raw_official" / "munition" / "munitions-missiles.json"
    if not src.exists():
        return costs
    rec = json.loads(src.read_text(encoding="utf-8"))
    for ent in rec.get("entities") or []:
        fields = ent["fields"]
        if "Base Cost / Validator Cost" in fields:
            costs[ent["name"]] = float(str(fields["Base Cost / Validator Cost"]).split("/")[0])
        elif "Base Cost (pts)" in fields:
            costs[ent["name"]] = float(fields["Base Cost (pts)"])
    return costs


COMPONENT_COST: dict[str, float] = {}


def cost_note(rec: dict) -> str:
    total = 0.0
    missing = []
    for sock in rec["sockets"]:
        key = sock["key"]
        if not key:
            continue
        if key in COMPONENT_COST:
            total += COMPONENT_COST[key]
        else:
            missing.append(key)
    parts = [f"wiki component cost {total:g} pts"]
    if missing:
        parts.append("not priced in the wiki: " + ", ".join(sorted(set(missing))))
    try:
        delta = float(rec["cost"]) - total
        parts.append(f"template total {float(rec['cost']):g} pts, difference {delta:g} pts = body + engine")
    except (TypeError, ValueError):
        pass
    return "; ".join(parts)


def slugify(text: str) -> str:
    text = re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")
    return text or "template"


def summarise(rec: dict) -> str:
    parts = []
    if rec["body"]:
        parts.append(f"body {rec['body']}")
    for sock in rec["sockets"]:
        key = sock["key"]
        if not key:
            continue
        low = key.lower()
        if "seeker" in low:
            role = sock["settings"].get("Mode", "Targeting")
            parts.append(f"{role.lower()} seeker {key}")
        elif "guidance" in low:
            parts.append(f"guidance {key}")
        elif any(word in low for word in ("impact", "he", "frag", "hekp", "submunition",
                                          "blast", "thermal", "shaped")):
            parts.append(f"payload {key}")
    text = "; ".join(parts) or "no components"
    return f"Size-{rec['sockets'][0]['size'] if rec['sockets'] else '?'} missile, {text}; {rec['cost']} points"


def render(rec: dict) -> str:
    lines = [f"# {rec['name']}" + (f" ({rec['designation']})" if rec["designation"] else ""), ""]
    lines.append(f"Tags: kind=missile template; cost={rec['cost']} pts; body={rec['body'] or '?'}")
    lines.append(f"Summary: {summarise(rec)}")
    lines.append(f"Source: {SRC_LINE}")
    lines.append(f"Cost: {cost_note(rec)}")
    lines.append("")
    lines.append("## Slots")
    lines.append("")
    lines.append("| # | Size | Component | Type | Settings |")
    lines.append("|---|---|---|---|---|")
    for index, sock in enumerate(rec["sockets"], 1):
        settings = "; ".join(f"{k}={v}" for k, v in sock["settings"].items()) or "-"
        price = COMPONENT_COST.get(sock["key"])
        name = sock["key"] or "-"
        if price is not None:
            name = f"{name} (+{price:g} pts)"
        lines.append(f"| {index} | {sock['size']} | {name} | "
                     f"{sock['type'] or '-'} | {settings} |")
    lines.append("")
    if rec["description"]:
        lines.append(f"Description: {rec['description']}")
        lines.append("")
    lines.append("## In-game stats")
    lines.append("")
    lines.append("```")
    lines.append(rec["long"] or "(no long description)")
    lines.append("```")
    lines.append("")
    return "\n".join(lines)


def main() -> int:
    if not SRC.exists():
        print(f"missing source folder: {SRC}")
        return 1
    if OUT.exists():
        shutil.rmtree(OUT)
    OUT.mkdir(parents=True)

    COMPONENT_COST.update(load_component_costs())
    print(f"component costs {len(COMPONENT_COST)}")

    records = []
    for path in sorted(SRC.glob("*.missile")):
        try:
            records.append(parse(path))
        except ET.ParseError as exc:  # noqa: PERF203
            print(f"skip {path.name}: {exc}")
    records.sort(key=lambda rec: rec["name"].lower())

    rows = [["Template", "Cost (pts)", "Body", "Seekers", "Guidance", "Payload"]]
    for rec in records:
        seekers, guidance, payload = [], [], []
        for sock in rec["sockets"]:
            key = sock["key"]
            low = key.lower()
            if "seeker" in low:
                role = sock["settings"].get("Mode", "Targeting")
                seekers.append(f"{key} ({role})")
            elif "guidance" in low:
                guidance.append(f"{key} ({sock['settings'].get('Maneuvers', '-')})")
            elif key:
                payload.append(key)
        rows.append([
            f"{rec['name']}", rec["cost"], rec["body"] or "-",
            "; ".join(seekers) or "-", "; ".join(guidance) or "-",
            "; ".join(payload) or "-",
        ])

    for rec in records:
        (OUT / f"{slugify(rec['name'])}.md").write_text(render(rec), encoding="utf-8")

    from build_official import md_table  # local helper to keep one table style

    catalog = [
        f"# Missile templates ({len(records)} entries)",
        "",
        md_table(rows),
        "",
        "Every missile template the player has built and saved. Swapping seekers "
        "(primary / backup / validator), their settings (Mode, RejectUnvalidated, "
        "DetectPDTargets) and guidance settings (Maneuvers, HotLaunch, Role, "
        "DefensiveDoctrine) only ever changes the point cost by a whole number, so the "
        "cost of an edited template can be recomputed; body, payload and engine are "
        "fixed by the template.",
        "",
        "Source: player-built templates (.missile save files), not the official wiki.",
        "",
    ]
    (OUT / "_catalog.md").write_text("\n".join(catalog), encoding="utf-8")
    (ROOT / "domain" / "data" / "missile_templates.json").write_text(
        json.dumps(records, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"missile templates {len(records)} -> {OUT}")
    return 0


if __name__ == "__main__":
    sys.exit(main())

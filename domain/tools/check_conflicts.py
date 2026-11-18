"""Reconcile the official wiki (0.6.2.6) against the installed game's own string tables.

The player's 344 saved fleets are deliberately NOT used here: most predate the
current version or carry mods, so their names are evidence of nothing.

What we compare instead:
  wiki component pages  <-> en-US\\en_assets.json HULLCOMPNAME_*
  wiki munition pages   <-> AMMONAME_* + MISSILECOMPNAME_* + missile class names
  wiki craft pages      <-> CRAFT_*_DESC keys (craft names are not localised)

Report buckets:
  MATCH       same string after normalisation
  SPELLING    same thing, different characters (the join would fail)
  WIKI-ONLY   wiki has it, the installed game's strings do not
  GAME-ONLY   the installed game has it, no wiki page
"""

from __future__ import annotations

import difflib
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "kb" / "raw_official"
REPORT = ROOT / "reports" / "wiki-vs-game-names.md"

LOC = Path(
    r"E:\SteamLibrary\steamapps\common\Nebulous\Nebulous_Data\StreamingAssets"
    r"\Localization\en-US\en_assets.json"
)

KIND_OF_CATEGORY = {
    "component": "part",
    "munition": "munition",
    "craft": "craft",
}

PUNCT = re.compile(r"[’'`´]")
DROP = re.compile(r"[^a-z0-9 %\-.]+")


def norm(text: str) -> str:
    """Compare only the characters that matter: case, quotes, punctuation."""
    s = PUNCT.sub("", (text or "").lower())
    s = DROP.sub(" ", s)
    return " ".join(s.split())


def load_loc() -> dict[str, dict[str, str]]:
    data = json.loads(LOC.read_text(encoding="utf-8-sig"))
    groups: dict[str, dict[str, str]] = {
        "part": {},
        "ammo": {},
        "missile": {},
        "craft": {},
    }
    for key, value in data.items():
        if key.endswith("_DESC"):
            continue
        if key.startswith("HULLCOMPNAME_"):
            groups["part"][key] = value
        elif key.startswith("HULLPARTNAME_"):
            # built-in hull parts (thrusters, radar panels, pads) also live in the
            # wiki's "Integrated Components" tables
            groups["part"][key] = value
        elif key.startswith("AMMONAME_"):
            groups["ammo"][key] = value
        elif key.startswith(("MISSILECOMPNAME_", "MISSILE_")):
            groups["missile"][key] = value
        elif key.startswith("CRAFT_"):
            groups["craft"][key] = value
    return groups


def load_wiki() -> dict[str, list[dict]]:
    wiki: dict[str, list[dict]] = {"part": [], "munition": [], "craft": []}
    for path in sorted(RAW.rglob("*.json")):
        rec = json.loads(path.read_text(encoding="utf-8"))
        kind = KIND_OF_CATEGORY.get(rec.get("category", ""))
        if not kind:
            continue
        for ent in rec.get("entities") or []:
            wiki[kind].append({
                "name": ent["name"],
                "section": ent["section"],
                "page": rec["title"],
            })
    return wiki


def match_names(wiki_names: list[dict], game: dict[str, str]) -> dict[str, list]:
    """Pair wiki entities with game strings: exact first, then fuzzy on the leftovers."""
    by_norm: dict[str, list[str]] = {}
    for key, value in game.items():
        by_norm.setdefault(norm(value), []).append(key)

    result: dict[str, list] = {"match": [], "spelling": [], "wiki_only": [], "game_only": []}
    used_keys: set[str] = set()
    left: list[dict] = []

    # Pass 1: exact matches only, so a fuzzy guess can never steal an exact pair.
    for ent in wiki_names:
        keys = by_norm.get(norm(ent["name"]))
        if keys:
            # the string table often holds duplicate keys for one display name
            # (HULLCOMPNAME_CR10_ANT + HULLCOMPNAME_CR10_ANTENNA): consume them all
            used_keys.update(keys)
            result["match"].append((ent, game[keys[0]], keys[0]))
        else:
            left.append(ent)

    # Pass 2: close spellings (acronym drift, apostrophes, singular/plural).
    free = {n: keys for n, keys in by_norm.items() if any(k not in used_keys for k in keys)}
    for ent in left:
        best = difflib.get_close_matches(norm(ent["name"]), list(free), n=1, cutoff=0.9)
        if best:
            key = next(k for k in free[best[0]] if k not in used_keys)
            used_keys.add(key)
            result["spelling"].append((ent, game[key], key))
        else:
            result["wiki_only"].append((ent, "", ""))
    for key, value in game.items():
        if key not in used_keys:
            result["game_only"].append(({"name": value, "section": "", "page": ""}, value, key))
    return result


def section_list(items: list) -> list[str]:
    lines = []
    for ent, value, key in items:
        page = f" — wiki page `{ent['page']}`" if ent.get("page") else ""
        key_text = f" — game key `{key}`" if key else ""
        lines.append(f"- **{ent['name']}** → game: `{value}`{key_text}{page}")
    return lines


def main() -> int:
    groups = load_loc()
    wiki = load_wiki()
    pairs = [
        ("Parts (mounts / compartments / modules / built-in hull parts)", "part", groups["part"]),
        ("Munitions (shells, missiles, seekers, mines, bombs)",
         "munition", {**groups["ammo"], **groups["missile"]}),
    ]

    lines = [
        "# Wiki (0.6.2.6) vs installed game strings",
        "",
        "Source A: the saved official wiki pages (game 0.6.2.6:260903-1430).",
        "Source B: `Nebulous_Data/StreamingAssets/Localization/en-US/en_assets.json`,",
        "i.e. the string table of the installed build itself.",
        "",
        "The player's own `.fleet` files are **not** used: most are older-version or modded.",
        "",
    ]
    summary: list[str] = []
    for title, kind, game in pairs:
        result = match_names(wiki[kind], game)
        summary.append(
            f"| {title} | {len(wiki[kind])} | {len(game)} | {len(result['match'])} | "
            f"{len(result['spelling'])} | {len(result['wiki_only'])} | "
            f"{len(result['game_only'])} |"
        )
        lines.append(f"## {title}")
        lines.append("")
        if result["spelling"]:
            lines.append(f"### Spelling conflicts ({len(result['spelling'])})")
            lines += section_list(result["spelling"])
            lines.append("")
        if result["wiki_only"]:
            lines.append(f"### In the wiki, absent from the installed game's strings ({len(result['wiki_only'])})")
            lines += section_list(result["wiki_only"])
            lines.append("")
        if result["game_only"]:
            lines.append(f"### In the installed game, absent from the wiki ({len(result['game_only'])})")
            lines += section_list(result["game_only"])
            lines.append("")
        lines.append("")

    head = [
        "## Counts",
        "",
        "| Group | wiki entries | game strings | matched | spelling | wiki-only | game-only |",
        "|---|---|---|---|---|---|---|",
        *summary,
        "",
    ]
    REPORT.parent.mkdir(parents=True, exist_ok=True)
    REPORT.write_text("\n".join(lines[:6] + head + lines[6:]) + "\n", encoding="utf-8")
    print("\n".join(head))
    print(f"report → {REPORT}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

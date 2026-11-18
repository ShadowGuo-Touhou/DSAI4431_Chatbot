"""Hull resolution shared by the classifiers.

`domain/data/hull_abbr.json` keys are the wiki hull names, `.fleet` files use the
in-game save keys, and the prefab table (`hull_sockets.json`) uses the prefab names
(`Ocello Cruiser`, `Shuttle Clipper`, …).  This module maps all three onto one
canonical wiki name and exposes the ordered socket list of that hull.

Exactly three hulls are assembled from bow/core/stern prefabs (`SECTIONS`); every
other hull — Flathead Monitor and Journeyman Light Carrier included — is one prefab.
That split comes from the save files, not from guesswork: `<HullConfig>` appears on
those three HullTypes and no other, and each of the three has a `<HullSocket>` key set
that is a subset of one prefab table and a superset of nothing else.
`domain/tools/audit_sockets.py` re-checks both properties against every `.fleet`.
"""

from __future__ import annotations

import json
import re
from functools import lru_cache
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "domain" / "data"

#: The three section kinds of a segmented hull, in the order the save file lists them.
PARTS = ("Bow", "Core", "Stern")

# in-game / prefab / player spelling -> wiki spelling of the *same ship today*
# The stock civilian names are legacy save keys: the hull is the modern one.
ALIASES = {
    "ocello cruiser": "Ocello Command Cruiser",
    "ocello command cruiser": "Ocello Command Cruiser",
    # player nicknames: shuttle = small clipper, tug = the other clipper
    "shuttle": "Ferryman Clipper",
    "shuttle clipper": "Ferryman Clipper",
    "ferryman": "Ferryman Clipper",
    "tugboat": "Draugr Clipper",
    "tug clipper": "Draugr Clipper",
    "draugr": "Draugr Clipper",
    # civilian freighters -> the combat hulls they became
    "bulk feeder": "Flathead Monitor",
    "bulk hauler": "Marauder Line Ship",
    "ore carrier": "Journeyman Light Carrier",
    "container hauler": "Moorline Line Ship",
    # the refit (CVLN) is a hull of its own: its saves carry a different HullType key
    "container hauler refit": "Container Hauler Refit",
    "worden fleet carrier": "Worden Fleet Carrier",
    "merca tor": "Mercator Replenishment Oiler",
    "mercator oiler": "Mercator Replenishment Oiler",
}

# wiki name -> prefab name in hull_sockets.json.  A hull that is not listed here has a
# prefab of the same name; the two single-prefab civilian conversions are spelled out
# because their prefab keeps the old name.
PREFAB = {
    "Ocello Command Cruiser": "Ocello Cruiser",
    "Ferryman Clipper": "Shuttle Clipper",
    "Draugr Clipper": "Tug Clipper",
    "Mercator Replenishment Oiler": "Mercator Oiler",
    # Stock/Bulk Feeder: a `Bulk Clipper` prefab, 19 sockets = 6 mount / 6 compartment / 7 module
    "Flathead Monitor": "Bulk Clipper",
    # Stock/Ore Carrier: a single `Ore Carrier` prefab, 17 sockets = 3 / 8 / 6
    "Journeyman Light Carrier": "Ore Carrier",
}

#: The only hulls built from bow + core + stern sections: wiki name -> section family.
#: The Marauder's sections are the `CivBulk - *` pieces and the CLN/CVLN's are the
#: `Container - *` pieces; `Container Refit - *` exists in the asset tree but no saved
#: hull uses it.
SECTIONS = {
    "Marauder Line Ship": "Bulk",
    "Moorline Line Ship": "Container",
    "Container Hauler Refit": "Container",
}

#: wiki name -> `<HullType>` the game writes into a `.fleet`.
SAVE_KEY = {
    "Axford Heavy Cruiser": "Stock/Axford Heavy Cruiser",
    "Container Hauler Refit": "Stock/Container Hauler Refit",
    "Draugr Clipper": "Stock/Tugboat",
    "Ferryman Clipper": "Stock/Shuttle",
    "Flathead Monitor": "Stock/Bulk Feeder",
    "Journeyman Light Carrier": "Stock/Ore Carrier",
    "Keystone Destroyer": "Stock/Keystone Destroyer",
    "Levy Escort Carrier": "Stock/Levy Escort Carrier",
    "Marauder Line Ship": "Stock/Bulk Hauler",
    "Mercator Replenishment Oiler": "Stock/Mercator Oiler",
    "Moorline Line Ship": "Stock/Container Hauler",
    "Ocello Command Cruiser": "Stock/Ocello Cruiser",
    "Raines Frigate": "Stock/Raines Frigate",
    "Solomon Battleship": "Stock/Solomon Battleship",
    "Sprinter Corvette": "Stock/Sprinter Corvette",
    "Vauxhall Light Cruiser": "Stock/Vauxhall Light Cruiser",
    "Worden Fleet Carrier": "Stock/Worden Fleet Carrier",
}


@lru_cache(maxsize=1)
def abbr_table() -> dict[str, str]:
    raw = json.loads((DATA / "hull_abbr.json").read_text(encoding="utf-8"))
    return {k: v.get("abbr", "") for k, v in raw.items() if not k.startswith("_")}


@lru_cache(maxsize=1)
def socket_table() -> dict[str, dict]:
    path = DATA / "hull_sockets.json"
    if not path.exists():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))


@lru_cache(maxsize=1)
def section_table() -> dict:
    path = DATA / "hull_sections.json"
    if not path.exists():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))


def resolve(hull_type: str) -> str:
    """Return the canonical wiki hull name for a `.fleet` HullType."""
    name = (hull_type or "").split("/")[-1].strip()
    # wiki hull names carry a " Class" suffix ("Ocello Command Cruiser Class")
    if name.lower().endswith(" class"):
        name = name[:-6].strip()
    low = name.lower()
    if low in ALIASES:
        return ALIASES[low]
    table = abbr_table()
    for key in table:
        if key.lower() == low:
            return key
    for key in table:
        if key.lower().startswith(low) or low.startswith(key.lower()):
            return key
    # last resort: match on the first word ("Ocello", "Keystone", …)
    head = low.split()[0] if low else ""
    for key in table:
        if key.lower().split()[0] == head:
            return key
    return name


def abbr(hull_type: str) -> str:
    return abbr_table().get(resolve(hull_type), "")


def save_key(hull_type: str) -> str:
    """`<HullType>` for a wiki/prefab/save spelling ("" when the hull is unknown)."""
    name = resolve(hull_type)
    if name in SAVE_KEY:
        return SAVE_KEY[name]
    tables = socket_table()
    for cand in (hull_type, (hull_type or "").split("/")[-1], name):
        key = f"Stock/{cand}"
        if cand and key in tables:
            return key
    return ""


def is_segmented(hull_type: str) -> bool:
    """True for the three hulls whose `<HullConfig>` picks bow/core/stern sections."""
    return resolve(hull_type) in SECTIONS


def section_family(hull_type: str) -> str:
    """Socket-table prefix of the hull's sections ("" for a single-prefab hull)."""
    return SECTIONS.get(resolve(hull_type), "")


def segment_guids(hull_type: str) -> dict[str, dict[str, str]]:
    """letter -> part -> segment GUID for a segmented hull; {} for anything else."""
    family = section_family(hull_type)
    families = section_table().get("families") or {}
    return (families.get(family) or {}).get("guid") or {}


def has_table(hull_type: str) -> bool:
    name = resolve(hull_type)
    return bool(sockets(name))


def _direct(name: str) -> dict | None:
    """Prefab table for `name`, trying the alias-resolved and the raw spelling."""
    tables = socket_table()
    for cand in (PREFAB.get(name, name), name):
        entry = tables.get(cand)
        if entry and entry.get("sockets"):
            return entry
    return None


def sockets_by_part(hull_type: str,
                    letters: str | tuple[str, ...] | None = None) -> list[tuple[str, dict]]:
    """`[(part, socket)]` in game order; `part` is "" for a single-prefab hull.

    `letters` picks the section variant per part (`"BBB"`), default all-`A`: every
    variant of a section exposes the same sockets, only the dressing differs.  A
    segmented hull whose section table is missing returns [] rather than falling back
    to another family's sockets.
    """
    name = resolve(hull_type)
    family = SECTIONS.get(name)
    if family:
        scheme = tuple(letters) if letters else tuple("A" for _ in PARTS)
        tables = socket_table()
        out: list[tuple[str, dict]] = []
        for part_name, letter in zip(PARTS, scheme):
            entry = tables.get(f"{family} - {letter} - {part_name}")
            if not entry or not entry.get("sockets"):
                return []
            out.extend((part_name, e) for e in entry["sockets"])
        return out
    direct = _direct(name) or _direct((hull_type or "").split("/")[-1])
    return [("", e) for e in direct["sockets"]] if direct else []


def sockets(hull_type: str) -> list[dict]:
    """Ordered socket list (1..N) for the hull, or [] when unknown."""
    return [entry for _, entry in sockets_by_part(hull_type)]


def order(hull_type: str) -> dict[str, int]:
    """socket key -> 1-based index in `sockets()` (NOT the in-game mount number)."""
    return {e["key"]: n for n, e in enumerate(sockets(hull_type), 1)}


def _volume(entry) -> int:
    size = entry.get("size") or [0, 0, 0]
    return int(size[0]) * int(size[1]) * int(size[2])


def mount_numbers(hull_type: str) -> dict[str, int]:
    """socket key -> in-game mount number (Surface sockets only).

    Ship Builds.txt says "(mount 1-3)", meaning the number the game shows next to a
    weapon mount.  That number is the socket ShortName (`MT3`), not the position in
    the prefab walk: on the Axford, `MT3` is the 12th socket in depth-first order.

    Segmented hulls are the exception: their socket table is a concatenation of three
    sections, each restarting its own `MT1/MT5/MT6` labels, so the labels collide.
    There the game numbers the surface sockets continuously, which is why an LN's main
    mounts are "mount 1-8" no matter which sections it uses.
    """
    surfaces = [e for e in sockets(hull_type) if str(e.get("type") or "") == "Surface"]
    shorts = [str(e.get("short") or "") for e in surfaces]
    if len(set(shorts)) != len(shorts):
        # segmented hull: the big (6x10x6) main mounts are mount 1-8, the small ones follow
        ranked = sorted(range(len(surfaces)),
                        key=lambda i: (-_volume(surfaces[i]), i))
        return {surfaces[i]["key"]: n for n, i in enumerate(ranked, 1)}
    out: dict[str, int] = {}
    for entry in surfaces:
        m = re.search(r"(\d+)$", str(entry.get("short") or ""))
        out[entry["key"]] = int(m.group(1)) if m else 0
    return out


def socket_by_index(hull_type: str) -> dict[int, dict]:
    return {n: e for n, e in enumerate(sockets(hull_type), 1)}


# 旧版本存档里的 HullType 可能是通用名（不是今天的舰体名）。
# 按用户给的表对应到今天的舰级缩写，用于「舰体是否符合该舰级」这一关。
CLASS_ALIAS = {
    "bulk feeder": "MN",
    "bulk hauler": "LN",
    "ore carrier": "CVL",
    "sprinter": "FFL",
    "ocello": "CC",
}


def class_hint(hull_type: str) -> str:
    """旧存档舰体名 → 今天的舰级缩写（找不到就返回空串）。"""
    low = (hull_type or "").lower()
    for key, abbr in CLASS_ALIAS.items():
        if key in low:
            return abbr
    return ""

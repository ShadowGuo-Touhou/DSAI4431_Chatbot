"""Parse NEBULOUS `.fleet` files and join them with the wiki component/hull data.

Design notes
------------
* A `.fleet` file is XML.  Each `<HullSocket>` carries an opaque per-ship socket
  GUID, a `ComponentName` (the in-game *save key*, e.g. ``Stock/VLS-2 Launcher``)
  and an optional `ComponentData` blob (missile load, ammo selection, craft load).
  Socket **position / size / type are not in the file** -- that information only
  exists inside the game's asset bundles, so nothing here may claim a fit check.
* Save keys and wiki names differ: the wiki keeps the marketing nickname
  (``L50 'Blackjack' Laser Dazzler``) while the save key drops it
  (``Stock/L50 Laser Dazzler``).  Matching therefore compares token sets.
"""

from __future__ import annotations

import json
import re
import xml.etree.ElementTree as ET
from dataclasses import dataclass, field
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
RAW_OFFICIAL = ROOT / "domain" / "kb" / "raw_official"
COMPONENTS_JSON = RAW_OFFICIAL / "component" / "components.json"
HULLS_JSON = RAW_OFFICIAL / "hull" / "ships.json"

CATEGORY_WORDS = {
    "mounts": "mount",
    "compartments": "compartment",
    "modules": "module",
}

_QUOTES = str.maketrans({"\u2019": "'", "\u2018": "'", "\u201c": '"', "\u201d": '"'})
_TOKEN = re.compile(r"[a-z0-9]+")
_NICKNAME = re.compile(r"['\"][^'\"]+['\"]")


def norm(text: str) -> str:
    return "".join(_TOKEN.findall(text.translate(_QUOTES).lower()))


def tokens(text: str) -> tuple[str, ...]:
    return tuple(_TOKEN.findall(text.translate(_QUOTES).lower()))


def save_key_name(name: str) -> str:
    """``Stock/VLS-2 Launcher`` -> ``VLS-2 Launcher``."""
    return name.split("/", 1)[-1].strip()


def to_number(text: object) -> float | None:
    if text is None:
        return None
    match = re.search(r"[-+]?\d+(?:\.\d+)?", str(text).replace(",", ""))
    return float(match.group(0)) if match else None


@dataclass(frozen=True)
class Component:
    name: str
    section: str
    fields: dict[str, str]

    @property
    def kind(self) -> str:
        for key in ("Weapon", "Mount", "Compartment", "Module"):
            if key in self.fields:
                return key
        return "unknown"

    @property
    def category(self) -> str:
        return self.fields.get("Category", self.section.split("›")[-1].strip())

    @property
    def cost(self) -> float:
        return to_number(self.fields.get("Cost (pts)")) or 0.0

    @property
    def mass(self) -> float:
        return to_number(self.fields.get("Mass (Tonnes)")) or 0.0

    @property
    def power(self) -> float:
        """Signed power budget: ``+`` generation, ``-`` consumption (kW).

        The wiki is not consistent: reactors carry ``Power (kW) = +5000`` while
        some modules carry a *negative* ``Power (kW)`` (``RM50 'Parallax' Radar``
        = ``-3600``) and most draws use ``Required Power (kW) = 200``.
        """
        raw = self.fields.get("Power (kW)")
        if raw is not None:
            return to_number(raw) or 0.0
        draw = to_number(self.fields.get("Required Power (kW)")) or 0.0
        return -abs(draw)

    @property
    def draw(self) -> float:
        return max(-self.power, 0.0)

    @property
    def supply(self) -> float:
        return max(self.power, 0.0)


@dataclass(frozen=True)
class Hull:
    name: str
    section: str
    fields: dict[str, str]

    @property
    def point_cost(self) -> float:
        return to_number(self.fields.get("Point Cost")) or 0.0

    @property
    def mass(self) -> float:
        return to_number(self.fields.get("Mass (tonnes)")) or 0.0

    @property
    def slots(self) -> dict[str, int]:
        text = self.fields.get("Slots", "")
        out: dict[str, int] = {}
        for count, word in re.findall(r"(\d+)\s+(Mounts|Compartments|Modules)", text):
            out[word.rstrip("s").lower()] = int(count)
        return out

    @property
    def total_slots(self) -> int:
        return sum(self.slots.values())


class WikiIndex:
    """Name lookup for the wiki components and hulls."""

    def __init__(self) -> None:
        self.components: list[Component] = [
            Component(e["name"], e["section"], e["fields"])
            for e in json.load(COMPONENTS_JSON.open(encoding="utf-8"))["entities"]
        ]
        self.hulls: list[Hull] = [
            Hull(e["name"], e["section"], e["fields"])
            for e in json.load(HULLS_JSON.open(encoding="utf-8"))["entities"]
        ]
        self._comp_norm = {norm(c.name): c for c in self.components}
        self._comp_tokens = [(tokens(c.name), c) for c in self.components]
        self._hull_norm = {norm(h.name): h for h in self.hulls}

    # -- components -----------------------------------------------------
    def component(self, save_key: str) -> Component | None:
        name = save_key_name(save_key)
        hit = self._comp_norm.get(norm(name))
        if hit is not None:
            return hit
        want = tokens(name)
        best: tuple[int, Component] | None = None
        for have, comp in self._comp_tokens:
            if all(token in have for token in want):
                extra = len(set(have) - set(want))
                if best is None or extra < best[0]:
                    best = (extra, comp)
        if best is not None:
            return best[1]
        # Last resort: the save key drops the nickname *and* keeps only the model
        # code plus a generic noun ("P20 Flak PDT" vs "P20 'Bastion' PDT").
        stripped = set(tokens(_NICKNAME.sub(" ", name)))
        for have, comp in self._comp_tokens:
            core = set(tokens(_NICKNAME.sub(" ", comp.name)))
            if core and core <= (stripped | {"pdt", "radar", "jammer", "launcher", "cannon", "gun", "turret"}):
                if len(core & stripped) >= 1:
                    return comp
        return None

    # -- hulls ----------------------------------------------------------
    def hull(self, hull_type: str) -> Hull | None:
        name = save_key_name(hull_type)
        hit = self._hull_norm.get(norm(name)) or self._hull_norm.get(norm(f"{name} Class"))
        if hit is not None:
            return hit
        want = [t for t in tokens(name) if t not in {"class", "stock"}]
        best: tuple[int, Hull] | None = None
        for hull in self.hulls:
            have = set(tokens(hull.name))
            if set(want) <= have:
                extra = len(have - set(want))
                if best is None or extra < best[0]:
                    best = (extra, hull)
        return best[1] if best else None


# -- fleet parsing ------------------------------------------------------
@dataclass
class Ammo:
    item: str
    quantity: int


@dataclass
class Socket:
    key: str
    component_name: str
    ammo: list[Ammo] = field(default_factory=list)
    extra: dict[str, str] = field(default_factory=dict)
    craft: list[str] = field(default_factory=list)


@dataclass
class Ship:
    key: str
    name: str
    hull_type: str
    cost: float
    callsign: str
    number: str
    sockets: list[Socket] = field(default_factory=list)


@dataclass
class Fleet:
    path: Path
    name: str
    version: str
    total_points: float
    faction: str
    ships: list[Ship]
    #: `SaveKey -> Cost` for missile templates embedded in the fleet file itself
    #: (player-built missiles that were never saved to Saves\MissileTemplates).
    missile_costs: dict[str, float] = field(default_factory=dict)
    #: `SaveKey -> {designation, size, control}` for the same embedded templates.
    missile_meta: dict[str, dict] = field(default_factory=dict)

    @property
    def ship_cost(self) -> float:
        return sum(ship.cost for ship in self.ships)


def _truthy(text: str | None) -> str:
    return (text or "").strip()


#: "…为尺寸2…" / "…is a size 2…" inside a missile template's long description
MISSILE_SIZE_RE = re.compile(r"(?:size|尺寸)\s*([1-4])", re.I)
#: `$MISSILEGUIDANCE_MODE_DIRECT` / `$MISSILEGUIDANCE_MODE_CRUISE_LONG`
MISSILE_CONTROL_RE = re.compile(r"MISSILEGUIDANCE_MODE_([A-Z_]+)")


def _missile_meta(template: ET.Element) -> dict:
    """Designation + body size + guidance mode of an embedded missile template."""
    designation = _truthy(template.findtext("Designation"))
    long_desc = _truthy(template.findtext("LongDescription"))
    short_desc = _truthy(template.findtext("Description"))
    text = f"{designation} {short_desc} {long_desc}"
    size = 0
    m = MISSILE_SIZE_RE.search(long_desc) or MISSILE_SIZE_RE.search(short_desc)
    if m:
        size = int(m.group(1))
    if not size:
        # designations encode the body class: SGM-1xx = size 1, SGM-2xx / SGM-H-2 = size 2 …
        d = re.search(r"(?:SGM|SDM|SGT|SGH|CM|SM)-?(?:H-?)?([1-4])", designation, re.I)
        if d:
            size = int(d.group(1))
    control = ""
    c = MISSILE_CONTROL_RE.search(text)
    if c:
        name = c.group(1)
        control = "cruise" if "CRUISE" in name else "direct"
    return {"designation": designation, "size": size, "control": control}


def _read_component_data(node: ET.Element | None) -> tuple[list[Ammo], dict[str, str]]:
    """Flatten a `<ComponentData>` blob into ammo entries + simple fields."""
    if node is None:
        return [], {}
    ammo: list[Ammo] = []
    extra: dict[str, str] = {}

    def walk(element: ET.Element, path: str) -> None:
        children = [c for c in element if isinstance(c.tag, str)]
        if not children:
            value = _truthy(element.text)
            if not value:
                return
            leaf = str(element.tag).split("}")[-1]
            if leaf in {"MunitionKey", "AmmoKey"}:
                return  # paired with the sibling Quantity below
            if leaf in {"Quantity", "MagazineKey", "MagazineSize"}:
                return
            extra[path or leaf] = value
            return
        for child in children:
            walk(child, f"{path}.{child.tag.split('}')[-1]}" if path else child.tag.split("}")[-1])

    # ammo: any element that carries MunitionKey/AmmoKey + Quantity
    for holder in node.iter():
        key_text = None
        quantity = 1
        for leaf in holder:
            tag = str(leaf.tag).split("}")[-1]
            if tag in {"MunitionKey", "AmmoKey"}:
                key_text = _truthy(leaf.text)
            elif tag == "Quantity":
                quantity = int(to_number(_truthy(leaf.text)) or 1)
        if key_text:
            ammo.append(Ammo(key_text, quantity))

    for child in node:
        walk(child, "")
    return ammo, extra


def parse_fleet(path: Path) -> Fleet:
    root = ET.parse(path).getroot()
    ships: list[Ship] = []
    missile_costs: dict[str, float] = {}
    missile_meta: dict[str, dict] = {}
    for template in root.iter("MissileTemplate"):
        key = _truthy(template.findtext("SaveKey"))
        cost = to_number(template.findtext("Cost"))
        meta = _missile_meta(template)
        # the game writes most embedded templates **without** a `<SaveKey>`; the ammo
        # in the fleet then references the missile by "Designation Nickname" (often under
        # the `$MODMIS$/` prefix), so register that spelling as an alias too.
        names = [key] if key else []
        if meta["designation"]:
            names.append(f"{meta['designation']} {_truthy(template.findtext('Nickname'))}".strip())
            names.append(meta["designation"])
        for name in names:
            if cost:
                missile_costs.setdefault(name, float(cost))
            missile_meta.setdefault(name, meta)
    for ship_node in root.iter("Ship"):
        sockets: list[Socket] = []
        socket_map = ship_node.find("SocketMap")
        if socket_map is not None:
            for item in socket_map.iter("HullSocket"):
                component = _truthy(item.findtext("ComponentName"))
                if not component:
                    continue
                ammo, extra = _read_component_data(item.find("ComponentData"))
                craft_data = item.find("ComponentData")
                craft = [
                    _truthy(n.text)
                    for n in (craft_data.iter("CraftTemplateKey") if craft_data is not None else [])
                    if _truthy(n.text)
                ]
                sockets.append(
                    Socket(
                        key=_truthy(item.findtext("Key")),
                        component_name=component,
                        ammo=ammo,
                        extra=extra,
                        craft=craft,
                    )
                )
        ships.append(
            Ship(
                key=_truthy(ship_node.findtext("Key")),
                name=_truthy(ship_node.findtext("Name")),
                hull_type=_truthy(ship_node.findtext("HullType")),
                cost=to_number(ship_node.findtext("Cost")) or 0.0,
                callsign=_truthy(ship_node.findtext("Callsign")),
                number=_truthy(ship_node.findtext("Number")),
                sockets=sockets,
            )
        )
    return Fleet(
        path=path,
        name=_truthy(root.findtext("Name")),
        version=_truthy(root.findtext("Version")),
        total_points=to_number(root.findtext("TotalPoints")) or 0.0,
        faction=_truthy(root.findtext("FactionKey")),
        ships=ships,
        missile_costs=missile_costs,
        missile_meta=missile_meta,
    )


def is_modded(save_key: str) -> bool:
    return not save_key.startswith("Stock/")

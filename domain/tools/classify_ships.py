"""Classify every ship in the fleet corpus against domain/spec/ship_builds.json."""

from __future__ import annotations

import json
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path

TOOLS = Path(__file__).resolve().parent
sys.path.insert(0, str(TOOLS))

import fleet_lib as fl  # noqa: E402
import build_classes as bc  # noqa: E402
import hashlib
import hulls as hu
import power_model  # noqa: E402
from build_classes import load_prices, load_missile_costs, load_saved_missile_prices  # noqa: E402

ROOT = TOOLS.parent.parent
SPEC = ROOT / "domain" / "spec" / "ship_builds.json"
OUT_JSON = ROOT / "domain" / "data" / "ship_classification.json"
OUT_MD = ROOT / "domain" / "reports" / "ship-classification.md"
HULL_ABBR_PATH = ROOT / "domain" / "data" / "hull_abbr.json"

HULL_ABBR = {k: v["abbr"] for k, v in json.loads(HULL_ABBR_PATH.read_text(encoding="utf-8")).items()
             if not k.startswith("_")}

# names that differ between the .fleet save and the wiki page
#: parts that no longer exist in 0.6.2.6 -> the whole fleet is stale (user, m03562)
LEGACY_PARTS = {
    "berthing", "c54 cannon", "s2 bandit launcher", "s2 twin bandit launcher",
    "torpedo turret",
}
LEGACY_NORM = {fl.norm(x) for x in LEGACY_PARTS}

MOUNT_SPEC = re.compile(r"\(mounts?\s*([\d,\-\s]+)\)", re.I)


def cost_band(cls, cost) -> str:
    """Cost is a "should" in Ship Builds.txt: report进区间/偏高/偏低 instead of failing.

    偏低 = underpriced = 玩家口语的 greed / shell / 贪污（把该带的东西省掉了）。
    偏高 = overpriced = 堆料 / 装备过剩。
    """
    lo, hi = (cls.get("cost") or [0, 0])[:2]
    if cls.get("any_cost") or hi <= 0:
        return "in"
    value = float(cost or 0)
    if value > hi:
        return "over"
    if value < lo:
        return "under"
    return "in"


def mount_set(cond):
    """(mount 1-3, 6) -> {1,2,3,6}; None when the condition names no mounts."""
    m = MOUNT_SPEC.search(cond)
    if not m:
        return None
    out = set()
    for part in m.group(1).split(","):
        part = part.strip()
        if "-" in part:
            a, b = part.split("-", 1)
            if a.strip().isdigit() and b.strip().isdigit():
                out.update(range(int(a), int(b) + 1))
        elif part.isdigit():
            out.add(int(part))
    return out or None

COUNTERMEASURE = ("chaff", "flare", "decoy", "conure", "killjoy", "chimney")
MISSILE_AMMO = ("sgm", "sdm", "sgt", "cm-", "cm ", "missile", "asm", "srm", "torpedo",
                "rocket", "mine", "bomb")


EXTRA_ALIASES = {
    "r400radar": "R400 'Bloodhound' LRT Radar",
    "e57floodlightilluminator": "E55 'Floodlight' Illuminator",
    "c5largemounthangar": "Large Mounted Hangar",
    "c4mounthangar": "Medium Mounted Hangar",
    "c4mediummounthangar": "Medium Mounted Hangar",
}

CLASS_TOKEN = re.compile(r"\b(ffl|ff|dd|cl|mn|ch|cc|bb|ln|cve/cvl|cve|cvln|cvl)\b", re.I)


def class_token(name: str) -> str | None:
    low = name.lower()
    if "cvln" in low:
        return "CVL"
    if "cve/cvl" in low:
        return "CARRIER"
    if "cve" in low:
        return "CVE"
    m = CLASS_TOKEN.search(low)
    return m.group(1).upper() if m else None


def ship_hull_abbr(hull_name: str) -> str | None:
    for key, abbr in HULL_ABBR.items():
        if hull_name.startswith(key):
            return abbr
    return None

CALIBER = re.compile(r"(\d+)\s*mm", re.I)
#: "vls-2", "cls-3", "tls", "mls", "sals-2", "rl18"
LAUNCH_TOKEN = re.compile(r"\b(vls|cls|tls|mls|sals|rl)-?\s*(\d+)?(?:-(\d+))?\b", re.I)
#: "large VLS" = the big launch cells only: VLS-2 and VLS-3, never VLS-1.
#: A bare `vls-1` means the whole VLS-1 family (VLS-1-23 and VLS-1-46).
LARGE_BY_KIND = {"VLS": ("VLS-2", "VLS-3"), "CLS": ("CLS-3",)}
#: "have at least 3 450 turrets" / "have 3 450 turrets" / "have at least 2 450 cannons"
ARMAMENT_REQ = re.compile(r"(?:at least |exactly )?(\d+)\s+(\d{2,3})\s*(?:mm)?\s*(?:turret|cannon)s?", re.I)
#: "have 3 - 4 mass drivers total" / "have 2-3 large vls"
RANGE_RE = re.compile(r"(\d+)\s*(?:-|–|to)\s*(\d+)")


def launcher_models(cond: str) -> tuple[str, ...]:
    """Which launcher models a "have N vls-2, vls-3 or cls-3 launchers" line means.

    - an explicit number is used literally: `vls-2` -> VLS-2, `cls-3` -> CLS-3
    - a bare family word expands by the `large` qualifier: `large vls` -> VLS-2 + VLS-3
      (never VLS-1), `large cls` -> CLS-3, `large vls or cls` -> all three
    - without `large`, the bare family matches every member: `vls-1` -> VLS-1
      (i.e. both VLS-1-23 and VLS-1-46), `cls` -> CLS
    """
    text = cond.lower()
    out: list[str] = []
    for kind, first, _second in LAUNCH_TOKEN.findall(text):
        kind = kind.upper()
        if kind == "RL":
            out.append("RL18")
        elif first:
            out.append(f"{kind}-{first}")
        elif "large" in text:
            out.extend(LARGE_BY_KIND.get(kind, (kind,)))
        else:
            out.append(kind)
    return tuple(dict.fromkeys(out)) or LARGE_BY_KIND["VLS"]


def armament_req(cond: str) -> tuple[int, int] | tuple[None, None]:
    """Parse (count, caliber) out of a must/should sentence; (None, None) if absent."""
    m = ARMAMENT_REQ.search(cond)
    if not m:
        return None, None
    return int(m.group(1)), int(m.group(2))

SOFTKILL = ("Jammer", "Chaff", "Flare", "Decoy", "Dazzler", "EA99", "EA20", "EA12", "Blackjack")
PDT = ("PDT", "Point Defense", "Defender", "Aurora", "Sarissa", "Stonewall", "Rebound", "Pavise", "Flak", "CIWS")
BEAM = ("Mk600", "Beam", "Mk45", "Particle")

#: words that carry no meaning when resolving a free-text part phrase
STOP = {
    "have", "has", "at", "least", "more", "than", "exactly", "total", "the", "a", "an",
    "and", "or", "of", "with", "on", "main", "for", "ships", "ship", "should", "must",
    "1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "any", "type", "types", "if",
    "using", "it", "its", "carry", "can", "amount", "max", "number", "compartment",
    "internal", "other",
}

#: short/in-game names players use in Ship Builds.txt -> substring on the wiki name
FRAGMENT_ALIASES = {
    "mount hanger": "hangar",
    "mount hangar": "hangar",
    "sarissa": "sarissa",
    "aurora": "aurora",
    "defender": "defender",
    "pavise": "pavise",
    "stonewall": "stonewall",
    "rebound": "rebound",
    "bastion": "bastion",
    "bullseye": "bullseye",
    "pinpoint": "pinpoint",
    "spyglass": "spyglass",
    "huntress": "huntress",
    "parallax": "parallax",
    "bellbird": "bellbird",
    "floodlight": "floodlight",
    "spotlight": "E55",
    "citadel": "citadel",
    "track correlator": "track correlator",
    "missile programming bus": "programming bus",
    "es32": "scryer",
    "scryer": "scryer",
    "blackjack": "blackjack",
    "energy regulator": "energy regulator",
    "auxiliary steering": "auxiliary",
    "aptitude": "aptitude",
    "strikedown": "strikedown",
}



def field(comp, key):
    if comp is None:
        return None
    for k, v in comp.fields.items():
        if k.strip().lower() == key.lower():
            return v
    return None


def num(value):
    if value is None:
        return None
    m = re.search(r"-?\d+(?:\.\d+)?", str(value).replace(",", ""))
    return float(m.group()) if m else None


class ShipFacts:
    def __init__(self, ship, fleet, idx, prices):
        #: missile templates embedded in the fleet file (unsaved player missiles)
        self.embedded = getattr(fleet, "missile_costs", {}) or {}
        self.missile_meta = getattr(fleet, "missile_meta", {}) or {}
        self.ship = ship
        self.fleet = fleet
        hull = idx.hull(hu.resolve(ship.hull_type))
        self.hull = hull
        self.hull_name = hull.name if hull else fl.save_key_name(ship.hull_type)
        self.cost = ship.cost
        self.comps = []
        unresolved = []
        for sock in ship.sockets:
            name = fl.save_key_name(sock.component_name)
            alias = EXTRA_ALIASES.get(fl.norm(name)) or bc.ALIASES_NORM.get(fl.norm(name))
            comp = idx.component(alias or name)
            if comp is None:
                unresolved.append(name)
            self.comps.append((sock, comp, name))
        self.unresolved = unresolved
        self.hull_abbr = hu.abbr(self.hull_name)
        self.orders = hu.mount_numbers(ship.hull_type)  # in-game mount number (MTn), not prefab index
        self.sections = Counter((c.section or "").split(" › ")[0].strip() for _, c, _ in self.comps if c)
        self.turrets = []      # (caliber, name, cost)
        self.casemates = []
        self.launchers = []    # (model, name)
        self.spinal = []
        self.spinal_idx = []
        self.draw = 0.0
        self.supply = 0.0
        self.parts = []
        self.missile_points = 0.0
        self.missile_s2_direct_points = 0.0
        self.missile_rounds = 0
        self.missile_unknown = 0
        self.cm_types: set[str] = set()
        self.dc = 0
        self.jammers = []
        self.illuminators = []
        self.offensive_ammo = 0
        self.radars = []
        self.cic = False
        self.cic_n = 0
        self.magazine = False
        self.ammo_storage = 0
        self.elevators = 0
        self.restores = 0
        self.drives = 0
        self.hangars = 0
        self.craft_pad = 0
        for sock, comp, name in self.comps:
            self._consume(sock, comp, name, prices)

    def _consume(self, sock, comp, name, prices):
        mnt = self.orders.get(sock.key)
        section = (comp.section if comp else "") or ""
        low = name.lower()
        if comp:
            p = num(field(comp, "Required Power (kW)"))
            prov = num(field(comp, "Provided Power (kW)"))
            # some wiki rows only carry a signed `Power (kW)`: reactors +5000,
            # radars -3600. Treat the sign literally instead of dropping the row.
            signed = num(field(comp, "Power (kW)"))
            if prov and prov > 0:
                self.supply += prov
                self.parts.append({"name": name, "section": section,
                                   "draw": 0.0, "supply": float(prov)})
            elif prov and prov < 0:
                self.draw += abs(prov)
                self.parts.append({"name": name, "section": section,
                                   "draw": float(abs(prov)), "supply": 0.0})
            elif p:
                self.draw += abs(p)
                self.parts.append({"name": name, "section": section,
                                   "draw": float(abs(p)), "supply": 0.0})
            elif signed and signed > 0:
                self.supply += signed
                self.parts.append({"name": name, "section": section,
                                   "draw": 0.0, "supply": float(signed)})
            elif signed and signed < 0:
                self.draw += abs(signed)
                self.parts.append({"name": name, "section": section,
                                   "draw": float(abs(signed)), "supply": 0.0})
        if "Spinal" in section:
            self.spinal.append(name)
            self.spinal_idx.append((name, mnt))
        if "Missile Launchers" in section:
            model = "VLS-2" if "VLS-2" in name else "VLS-3" if "VLS-3" in name else \
                    "VLS-1-46" if "VLS-1-46" in name else "VLS-1-23" if "VLS-1-23" in name else \
                    "VLS-1" if "VLS-1" in name else "MLS" if "MLS" in name else \
                    "RL18" if "RL18" in name else "CLS-3" if "CLS-3" in name else \
                    "CLS" if "CLS" in name else "TLS" if "TLS" in name else name
            self.launchers.append((model, name, mnt))
        is_launcher = "Missile Launchers" in section
        for ammo in sock.ammo:
            short = ammo.item.split("/")[-1]
            low_ammo = short.lower()
            # unsaved missiles are referenced by a bare key that names nothing,
            # so "is this ammo a missile" has to come from the embedded templates
            embedded_key = (short in self.embedded
                            or f"$MODMIS$/{short}" in self.embedded
                            or ammo.item in self.embedded)
            is_cm = any(t in low_ammo for t in COUNTERMEASURE)
            is_missile = any(t in low_ammo for t in MISSILE_AMMO) or embedded_key
            if not is_cm:
                self.offensive_ammo += ammo.quantity
            else:
                if "chaff" in low_ammo or "ea12" in low_ammo:
                    self.cm_types.add("chaff")
                elif "flare" in low_ammo or "ea20" in low_ammo:
                    self.cm_types.add("flare")
                elif any(t in low_ammo for t in ("decoy", "conure", "ea99", "killjoy", "chimney")):
                    self.cm_types.add("decoy")
            if not is_missile:
                continue
            key = fl.norm(short)
            price = prices.get(key, 0.0) or prices.get(fl.norm(fl.save_key_name(ammo.item)), 0.0)
            if price <= 0:
                # unsaved missiles are priced inside the .fleet itself; magazine ammo
                # stores the bare key while the template names it `$MODMIS$/<key>`
                price = (self.embedded.get(ammo.item, 0.0)
                         or self.embedded.get(f"$MODMIS$/{short}", 0.0)
                         or self.embedded.get(short, 0.0))
            self.missile_rounds += ammo.quantity
            self.missile_points += price * ammo.quantity
            if price <= 0:
                self.missile_unknown += ammo.quantity
            # "S2 direct straightrunner" = size-2 body, direct (non-cruise) guidance
            meta = (self.missile_meta.get(ammo.item)
                    or self.missile_meta.get(f"$MODMIS$/{short}")
                    or self.missile_meta.get(short) or {})
            size = int(meta.get("size") or 0)
            if not size:
                d = re.search(r"(?:SGM|SDM|SGT|CM|SM)-?(?:H-?)?([1-4])", short, re.I)
                size = int(d.group(1)) if d else 0
            control = (meta.get("control") or "").lower()
            if not control:
                control = ("cruise" if re.search(r"cruise|waypoint", short, re.I) else "direct")
            if size == 2 and control == "direct" and price > 0:
                self.missile_s2_direct_points += price * ammo.quantity
        if any(t in low for t in ("jammer", "dazzler", "commjam")):
            self.jammers.append(name)
        if any(t in low for t in ("illuminator", "floodlight", "spotlight")):
            self.illuminators.append(name)
        if "Projectile weapons" in section or "Energy weapons" in section:
            m = CALIBER.search(field(comp, "Ammo") or "") if comp else None
            caliber = int(m.group(1)) if m else 0
            if comp and field(comp, "Turret / Casemate"):
                self.turrets.append((caliber, name, mnt))
            elif comp:
                self.casemates.append((caliber, name, mnt))
        if any(p.lower() in low for p in PDT) or "Point Defense" in section:
            pass
        if any(k.lower() in low for k in SOFTKILL):
            pass
        if "damage control" in section.lower():
            self.dc += 1
            self.restores += int(num(field(comp, "Restores Provided")) or 0) if comp else 0
        if "CIC" in name:
            self.cic = True
            self.cic_n += 1
        if "Magazine" in name:
            self.magazine = True
        if any(t in low for t in ("magazine", "ammunition storage", "ammo storage", "bulk storage")):
            self.ammo_storage += 1
        if "ammunition elevator" in low:
            self.elevators += 1
        if "Propulsion" in section:
            self.drives += 1
        if "hangar" in low:
            self.hangars += 1
        if "launch pad" in low:
            self.craft_pad += 1
        if "Sensors" in section or "Radar" in name:
            self.radars.append(name)

    # ---- derived features -------------------------------------------------
    def pdt_count(self):
        return sum(1 for _, c, n in self.comps
                   if (c and "Point Defense" in ((c.section or ""))) or any(p in n for p in ("PDT",)))

    def softkill(self):
        return [n for _, _, n in self.comps if any(k.lower() in n.lower() for k in SOFTKILL)]

    def softkill_level(self) -> str:
        """minimal / good / full - how many countermeasure kinds are fitted."""
        low = [n.lower() for _, _, n in self.comps]
        kinds = set(self.cm_types)
        if any(t in n for n in low for t in ("jammer", "commjam", "dazzler")):
            kinds.add("jammer")
        if any(t in n for n in low for t in ("decoy", "conure", "ea99", "killjoy", "chimney")):
            kinds.add("decoy")
        n = len(kinds)
        if n == 0:
            return "none"
        if n == 1:
            return "minimal"
        return "full" if n >= 3 else "good"

    def count_caliber(self, cal, kind="turret", mounts=None):
        pool = self.turrets if kind == "turret" else self.turrets + self.casemates
        return sum(1 for c, _, i in pool if c == cal and (mounts is None or i in mounts))

    def count_any_turret(self, mounts=None):
        pool = self.turrets + self.casemates
        return sum(1 for _, _, i in pool if mounts is None or i in mounts)

    def caliber_counts(self):
        """{caliber: count} for turrets and casemates combined."""
        out: dict[str, int] = {}
        for cal, _name, _i in self.turrets + self.casemates:
            if cal:
                out[str(cal)] = out.get(str(cal), 0) + 1
        return out

    @property
    def power_boost(self) -> float:
        """Powerplant-efficiency bonus in percent.

        Plant Control Center (compartment) gives +20 % each, Small Reactor
        Booster (module) +10 % each — both multiply the *generator* total, which
        is what the in-game power panel shows. Hull modifiers can add more.
        """
        pct = 0.0
        for _sock, comp, name in self.comps:
            low = (comp.name if comp else name).lower()
            if "plant control center" in low:
                pct += 20.0
            elif "small reactor booster" in low:
                pct += 10.0
        mods = " ".join(str(v) for v in (self.hull.fields or {}).values()) if self.hull else ""
        for m in re.finditer(r"(\d+)\s*%\s*Powerplant Efficiency", mods, re.I):
            pct += float(m.group(1))
        return pct

    def beam_turrets(self, mounts=None):
        return [n for _, n, i in self.turrets
                if any(k.lower() in n.lower() for k in BEAM) and (mounts is None or i in mounts)]

    def rail(self, mounts=None):
        out = []
        for n in (n for _, c, n in self.comps if "Mk550" in n or "Railgun" in n):
            out.append(n)
        return out

    def mass_drivers(self, mounts=None):
        """TE45 Mass Driver is what players mean by "md" (the Mk550 is a railgun)."""
        out = []
        for sock, comp, name in self.comps:
            if "mass driver" not in name.lower():
                continue
            mnt = self.orders.get(sock.key)
            if mounts is None or mnt in mounts:
                out.append(name)
        return out

    def count_launchers(self, models, mounts=None):
        """Count launchers by model token; a token also matches longer model names.

        `("VLS-2",)` counts `VLS-2 Launcher`, `("CLS",)` counts `CLS-3 Launcher`,
        `("MLS",)` counts `MLS-2 Launcher`, and `("VLS-1",)` also counts `VLS-1-46`.
        """
        wanted = tuple(m.upper() for m in models)
        return sum(1 for model, _, i in self.launchers
                   if any(model.upper() == w or model.upper().startswith(w) for w in wanted)
                   and (mounts is None or i in mounts))

    def count_model(self, token, mounts=None):
        """Count guns whose name carries a model token (T20 / Mk66 / TE45 ...)."""
        t = token.lower().replace("-", "").replace(" ", "")
        n = 0
        for _cal, name, i in self.turrets + self.casemates:
            flat = name.lower().replace("-", "").replace(" ", "")
            if t in flat and (mounts is None or i in mounts):
                n += 1
        return n

    def has(self, *words):
        return any(all(w.lower() in n.lower() for w in words) for _, c, n in [(s, c, n) for s, c, n in self.comps])

    def named(self, *words):
        return [n for _, _, n in self.comps if any(all(w.lower() in n.lower() for w in words) for w in [words])]

    def count_fragment(self, frag: str):
        """Count components matching a free-text phrase from Ship Builds.txt.

        Used by the generic fallback so new conditions written by the user keep
        working without a code change.  Returns None when nothing in the phrase
        can be resolved to a known component name.
        """
        text = re.sub(r"\(.*?\)", " ", frag.lower()).replace("-", " ")
        text = re.sub(r"\b(turret|turrets|cannon|cannons|launcher|launchers|module|modules|"
                      r"compartment|compartments|mount|mounts|drives?|drive)\b", " ", text)
        text = re.sub(r"[^a-z0-9% ]+", " ", text)
        tokens = [t for t in text.split() if len(t) > 1 and t not in STOP]
        if not tokens:
            return None
        best = 0
        for _sock, comp, name in self.comps:
            hay = (name + " " + (comp.section if comp else "")).lower()
            for alias, canon in FRAGMENT_ALIASES.items():
                if alias in " ".join(tokens) and canon.lower() in hay:
                    best += 1
                    break
            else:
                if all(t in hay for t in tokens):
                    best += 1
        return best


# ---------------------------------------------------------------------------
# condition -> check
# ---------------------------------------------------------------------------
def build_checks(f):
    """Return dict condition -> True/False/None."""
    res = {}
    for cond in f:
        res[cond] = check_one(cond)
    return res


def check_one(cond: str):
    c = cond.strip().lower()
    ms = mount_set(cond)

    # baseline block
    if "at least 1 drive" in c:
        m = re.search(r"at least (\d+) drive", c)
        need = int(m.group(1)) if m else 1
        return self_current.drives >= need
    if "at least 1 cic" in c:
        m = re.search(r"at least (\d+) cic", c)
        need = int(m.group(1)) if m else 1
        return self_current.cic_n >= need
    if "at least 1 ammo storage" in c:
        m = re.search(r"at least (\d+) ammo storage", c)
        need = int(m.group(1)) if m else 1
        return self_current.ammo_storage >= need
    if re.search(r"\bdrives?\b", c):
        m = re.search(r"(\d+)\s*drives?", c)
        need = int(m.group(1)) if m else 1
        return self_current.drives >= need
    if "cic" in c:
        m = re.search(r"(\d+)", c)
        need = int(m.group(1)) if m else 1
        if "auxiliary" in c or "auxillary" in c:
            return self_current.cic_n + len(self_current.named("Auxiliary")) >= need
        return self_current.cic_n >= need
    if "ammo storage" in c:
        m = re.search(r"(\d+)", c)
        need = int(m.group(1)) if m else 1
        return self_current.ammo_storage >= need
    if "ammo elevator" in c:
        m = re.search(r"(\d+)", c)
        need = int(m.group(1)) if m else 1
        return self_current.elevators >= need
    if "restore" in c:
        m = re.search(r"(\d+)", c)
        need = int(m.group(1)) if m else 1
        return self_current.restores >= need
    if "required power" in c:
        budget = power_model.analyse(self_current.parts, boost_pct=self_current.power_boost)
        if budget["verdict"] == "no_powerplant":
            return None
        return budget["verdict"] in ("ok", "ok_shutdown")
    if "placeholder-never" in c:
        draw, supply = self_current.draw, self_current.supply
        if supply <= 0:
            return None
        pct = draw / supply * 100
        m = re.search(r"([<≤=]+)\s*(\d+)\s*%", c)
        if not m:
            return True
        op, limit = m.group(1), float(m.group(2))
        return pct <= limit if "<" in op or "≤" in op else abs(pct - limit) < 1e-6
    if "never run out of ammo before" in c or "min of cannon ammo" in c or "pdt should have" in c:
        return None

    # weapons
    if "no offensive weapons" in c:
        # "armed" = a gun, a missile/rocket round, or a jammer. Cannon shells in a
        # magazine are ammunition for a gun that is already counted, not a weapon of
        # their own; the user's definition names cannon / turret / offensive missile /
        # jammer / arming missile, not "any ammo".
        armed = (bool(self_current.turrets) or bool(self_current.casemates)
                 or bool(self_current.spinal) or self_current.missile_rounds > 0
                 or bool(self_current.jammers))
        return not armed
    if "jammer and/or illuminator" in c:
        m = re.search(r"at least (\d+)", c)
        need = int(m.group(1)) if m else 1
        return len(self_current.jammers) + len(self_current.illuminators) >= need
    if "illuminator" in c and "jammer" not in c:
        return bool(self_current.illuminators)
    if "arming missile" in c:
        # an arming missile is a *missile* round; cannon shells in the magazine are not
        return self_current.missile_rounds > 0
    if c.lower().startswith("have a radar"):
        return len(self_current.radars) > 0
    if "long range radar" in c:
        return bool(self_current.named("Huntress")) or bool(self_current.named("Spyglass"))
    if "spyglass" in c:
        return bool(self_current.named("Spyglass"))
    if "radar" in c and "lrt" in c or "early warning" in c:
        return bool(self_current.named("R400")) or bool(self_current.named("Early Warning")) \
            or bool(self_current.named("Huntress"))
    if "track correlator" in c:
        return bool(self_current.named("Track Correlator"))
    if "rl-18" in c or "rl18" in c:
        return bool(self_current.named("RL18"))
    if "mk600" in c:
        return bool(self_current.named("Mk600"))
    if "mk550" in c or "railgun" in c:
        return bool(self_current.rail())
    if "no spinal" in c:
        return not self_current.spinal
    if "spinal" in c:
        return len(self_current.spinal) > 0
    if "beam" in c:
        m = re.search(r"(\d+)", c)
        need = int(m.group(1)) if m else 1
        return len(self_current.beam_turrets(ms)) >= need
    if "rail turret" in c:
        m = re.search(r"(\d+)", c)
        need = int(m.group(1)) if m else 1
        return len(self_current.rail()) >= need
    if "mass driver" in c:
        if "face" in c:
            # .fleet stores no muzzle facing: the gun's arc is not in the save file.
            return None
        rng = RANGE_RE.search(c)
        n = len(self_current.mass_drivers(ms))
        if rng:
            return int(rng.group(1)) <= n <= int(rng.group(2))
        m = re.search(r"(\d+)", c)
        need = int(m.group(1)) if m else 1
        return n >= need
    if "track" in c:
        return None
    if re.search(r"\b(vls|cls|tls|mls|sals|rl)\b", c, re.I):
        models = launcher_models(c)
        n = self_current.count_launchers(models, ms)
        if "2-3" in c:
            return 2 <= n <= 3
        if "exactly" in c:
            need = int(re.search(r"(\d+)", c).group(1)) if re.search(r"(\d+)", c) else 1
            return n == need
        need = int(re.search(r"(?:at least\s+)?(\d+)", c).group(1)) if re.search(r"(?:at least\s+)?(\d+)", c) else 1
        return n >= need
    if "does not satisfy any other class" in c:
        # fallback class ("A Cap (Any ship)"): only true when nothing else matched,
        # which is decided in main() after every class has been evaluated.
        return None
    if "mount hanger" in c or "mount hangar" in c:
        m = re.search(r"(\d+)", c)
        need = int(m.group(1)) if m else 1
        if "more than" in c:
            return self_current.hangars > need
        return self_current.hangars >= need
    if "same type" in c and ("mls" in c or "launcher" in c):
        models = {mo for mo, _n, _i in self_current.launchers}
        if not models:
            return None
        return len(models) == 1
    if "damage control complex" in c:
        return bool(self_current.named("Damage Control Complex"))
    if "citadel magazine" in c:
        return bool(self_current.named("Citadel"))
    if "craft launch pad" in c or "craft launch" in c:
        return bool(self_current.craft_pad) or bool(self_current.hangars)
    _kw = re.search(r">\s*(\d{4,})\s*kw", c)
    if _kw:
        # "have >16000kW power required" - an avoid rule on the raw draw
        return self_current.draw <= int(_kw.group(1))
    if re.search(r"either\s+t30\s+or\s+t81|either\s+t81\s+or\s+t30", c):
        # "all 8 turrets are either T30 or T81" — every main-mount turret is one of
        # the two, and there must actually be eight of them.
        n = self_current.count_model("T30", ms) + self_current.count_model("T81", ms)
        return n >= 8 and n == self_current.count_any_turret(ms)
    if "container bank" in c:
        # "have at least 1 Container Bank Launcher" / "Container Bank Hanger"
        if "hang" in c:
            return bool(self_current.named("Container Bank Hangar")) or self_current.hangars > 0
        return len(self_current.named("Container Bank")) > 0
    _model = re.search(r"\b(t20|t30|t81|c30|c53|c56|c65|c81|c90|te45|mk61|mk62|mk64|mk65|"
                       r"mk66|mk68|mk81|mk550|rl18)\b", c, re.I)
    if _model and ("turret" in c or "cannon" in c):
        # "have gun turrets (T20 or Mk61,Mk62,Mk64)" lists interchangeable models:
        # any of them counts, and the required number only ever comes from an
        # explicit "at least N" / "exactly N" -- never from the digits inside a
        # model name (that bug read "T20" as "20 turrets").
        models = {m.upper() for m in re.findall(
            r"\b(t20|t30|t81|c30|c53|c56|c65|c81|c90|te45|mk61|mk62|mk64|mk65|"
            r"mk66|mk68|mk81|mk550|rl18)\b", c, re.I)}
        m = re.search(r"(?:at least|exactly)\s+(\d+)", c)
        need = int(m.group(1)) if m else 1
        n = sum(self_current.count_model(tok, ms) for tok in models)
        if "exactly" in c:
            return n == need
        return n >= need
    if "no turrets" in c:
        return self_current.count_any_turret(ms) == 0
    if "turret and/or cannon" in c or "cannon or turret" in c:
        return self_current.count_any_turret(ms) >= 1
    if "t30" in c:
        m = re.search(r"(\d+)", c)
        need = int(m.group(1)) if m else 1
        return bool(self_current.named("T30")) and \
            len(self_current.named("T30")) >= need
    if "all cannons face" in c:
        return None
    if "rapid-cycle cradle" in c:
        m = re.search(r"(\d+)", c)
        need = int(m.group(1)) if m else 1
        return len(self_current.named("Rapid-Cycle")) >= need
    if "good dc (include" in c:
        # "have good DC (include a large DC Storage and a Damage Control Complex)"
        return (self_current.restores >= 4
                and bool(self_current.named("Large DC Storage"))
                and bool(self_current.named("Damage Control Complex")))
    if "good dc" in c or "better dc" in c:
        m = re.search(r"(\d+)", c)
        need = int(m.group(1)) if m else 4
        return self_current.restores >= need
    if "turret" in c:
        count, cal = armament_req(c)
        if "250 or 450" in c:
            return (self_current.count_caliber(250, mounts=ms)
                    + self_current.count_caliber(450, mounts=ms)) >= 2
        if cal:
            return self_current.count_caliber(cal, mounts=ms) == count if "exactly" in c \
                else self_current.count_caliber(cal, mounts=ms) >= count
        return self_current.count_any_turret(ms) >= (count or 1)
    if "cannon" in c:
        count, cal = armament_req(c)
        if cal:
            return self_current.count_caliber(cal, kind="cannon", mounts=ms) == count if "exactly" in c \
                else self_current.count_caliber(cal, kind="cannon", mounts=ms) >= count
        return self_current.count_any_turret(ms) >= (count or 1)
    if "point" in c and "missile" in c:
        m = re.search(r">?\s*(\d+)", c)
        need = int(m.group(1)) if m else 0
        if self_current.missile_rounds and self_current.missile_unknown / self_current.missile_rounds > 0.4:
            return None
        # "S2 direct straightrunner" only counts size-2 missiles with direct guidance
        if "straightrunner" in c or re.search(r"\bS2\b", c):
            return self_current.missile_s2_direct_points > need
        return self_current.missile_points > need
    if "energy regulator" in c:
        m = re.search(r"(\d+)", c)
        need = int(m.group(1)) if m else 1
        return len(self_current.named("Energy Regulator")) >= need
    if "focused particle accelerator" in c:
        m = re.search(r"(\d+)", c)
        need = int(m.group(1)) if m else 1
        return len(self_current.named("Focused Particle Accelerator")) >= need
    if "r2 rocket" in c or "rockets it can carry" in c:
        # The game's save key is still `Stock/S1 Rocket` for the size-2 rocket that the
        # RL-18 fires (R-2 'Piranha' = "turreted rocket launchers"); the key is legacy,
        # so match any rocket round rather than the literal "R2" token.
        rockets = sum(a.quantity for s in self_current.ship.sockets for a in s.ammo
                      if "rocket" in a.item.lower())
        if "can carry" in c:
            # "max amount of R2 Rockets it can carry (18 for each launcher)"
            return rockets >= 18 * max(1, len(self_current.named("RL18")))
        return rockets > 0
    if "blanket jammer" in c:
        m = re.search(r"(\d+)", c)
        need = int(m.group(1)) if m else 1
        return sum(1 for j in self_current.jammers if "blanket" in j.lower()) >= need
    if "good hardkill or good softkill" in c:
        # heuristic: "good hardkill" is not machine-checkable (>6 PDT mixing CIWS/Flak),
        # so accept a good/full softkill suite or a >=6 PDT fit, else unknown
        if self_current.softkill_level() in ("good", "full"):
            return True
        if self_current.pdt_count() >= 6:
            return True
        return None
    if "hardkill or softkill" in c:
        # "have hardkill or softkill" — either counts, so only False when both are absent
        return self_current.pdt_count() >= 1 or self_current.softkill_level() != "none"
    if "hardkill" in c and "softkill" in c and " and " in c:
        parts = [p.strip() for p in re.split(r"\s+and\s+", c) if p.strip()]
        vals = [check_one(p) for p in parts]
        if any(v is False for v in vals):
            return False
        if any(v is None for v in vals):
            return None
        return True
    if "aurora" in c:
        m = re.search(r"(\d+)", c)
        need = int(m.group(1)) if m else 1
        n = sum(1 for _, comp, name in self_current.comps
                if "aurora" in name.lower() and comp
                and "point defense" in (comp.section or "").lower())
        return n >= need
    if "pinpoint" in c:
        return bool(self_current.named("Pinpoint"))
    if "bellbird" in c:
        return bool(self_current.named("Bellbird"))
    if "reinforced" in c and "magazine" in c:
        return bool(self_current.named("Reinforced Magazine"))
    if "hardkill" in c:
        if "good" in c or "better" in c:
            return None
        if "minimal" in c:
            return self_current.pdt_count() >= 1
        m = re.search(r"(\d+)", c)
        need = int(m.group(1)) if m else 1
        return self_current.pdt_count() >= need
    if "softkill" in c:
        level = self_current.softkill_level()
        if level == "none":
            return False
        if "full" in c:
            return level == "full"
        if "good" in c or "better" in c:
            return level in ("good", "full")
        return True
    if "bullseye" in c:
        return bool(self_current.named("Bullseye"))
    if "dc" in c:
        m = re.search(r"(\d+)", c)
        need = int(m.group(1)) if m else 1
        return self_current.dc >= need
    return None


self_current: ShipFacts | None = None


def hull_allowed(cls, facts):
    tokens = cls.get("hulls") or []
    if not tokens:
        return True
    abbr = (facts.hull_abbr or hu.class_hint(facts.hull_name) or "").upper()
    # strip the wiki's " Class" suffix: without it the token "CL" also matched
    # "Sprinter Corvette Class" and a 127-point corvette became a "120 gun CL".
    name = re.sub(r"\s*class$", "", (facts.hull_name or "").lower())
    for tok in tokens:
        t = tok.strip()
        if not t:
            continue
        if t.upper() == abbr:
            return True
        if re.search(rf"\b{re.escape(t.lower())}\b", name):
            return True
    return False


def fleet_has_legacy(path):
    try:
        text = Path(path).read_text(encoding="utf-8", errors="ignore")
    except OSError:
        return False
    low = text.lower()
    return any(tok in low for tok in ("berthing", "c54 cannon", "s2 bandit", "bandit launcher", "torpedo turret"))


def ship_has_legacy(ship) -> bool:
    """Skip only the ships that still mount a removed part, not the whole fleet."""
    for sock in ship.sockets:
        if fl.norm(fl.save_key_name(sock.component_name)) in LEGACY_NORM:
            return True
    return False


MOD_NO_SHIP_LIMITS = "2938277064"


def _mod_ids(path) -> list[str]:
    import re as _re
    try:
        text = Path(path).read_text(encoding="utf-8", errors="ignore")
    except OSError:
        return []
    m = _re.search(r"<ModDependencies>(.*?)</ModDependencies>", text, _re.S)
    return _re.findall(r"<unsignedLong>(\d+)</unsignedLong>", m.group(1)) if m else []


def collect_fleets():
    paths = []
    for pattern in ("other info/fleets/**/*.fleet", "other info/ v1.12/**/*.fleet"):
        paths += sorted(ROOT.glob(pattern))
    kept = json.loads((ROOT / "domain" / "data" / "fleets_kept.json").read_text(encoding="utf-8"))
    for rec in kept:
        p = Path(rec["path"])
        if p.exists():
            paths.append(p)
    save_root = Path(r"E:\SteamLibrary\steamapps\common\Nebulous\Saves\Fleets")
    if save_root.exists():
        for p in sorted(save_root.rglob("*.fleet")):
            ids = _mod_ids(p)
            if not ids or set(ids) == {MOD_NO_SHIP_LIMITS}:
                paths.append(p)
    # 人工白名单：个别舰队即使早于更新日、或带模组，也被用户点名纳入
    exc_path = ROOT / "domain" / "data" / "fleet_exceptions.json"
    if exc_path.exists():
        try:
            exc = json.loads(exc_path.read_text(encoding="utf-8"))
            for rec in exc.get("fleets", []):
                p = Path(rec["path"])
                if p.exists():
                    paths.append(p)
        except (OSError, ValueError, KeyError):
            pass

    seen, out = set(), []
    for p in paths:
        try:
            digest = hashlib.sha1(Path(p).read_bytes()).hexdigest()
        except OSError:
            continue
        if digest not in seen:
            seen.add(digest)
            out.append(p)

    # Byte-identical files are already gone, but the same fleet also exists as
    # several near-copies (starter pack + `Saves\Fleets\Imported\…` + a re-save
    # after a rename), which differ by a `<Description>` or `<Number>` only and
    # would otherwise count the same ship two or three times in the statistics.
    # Signature = display name + point total + the sorted ship names.
    seen_sig, uniq = set(), []
    for p in out:
        try:
            fleet = fl.parse_fleet(p)
            sig = (fleet.name, round(float(fleet.total_points or 0), 1),
                   tuple(sorted(s.name for s in fleet.ships)))
        except Exception:  # unreadable file: keep it so the error surfaces downstream
            uniq.append(p)
            continue
        if sig in seen_sig:
            continue
        seen_sig.add(sig)
        uniq.append(p)
    return uniq


def main() -> int:
    global self_current
    spec = json.loads(SPEC.read_text(encoding="utf-8"))
    classes = spec["classes"]
    for cls in classes:
        cls["token"] = class_token(cls["name"])
    idx = fl.WikiIndex()
    prices = load_prices()
    for _name, _cost in load_saved_missile_prices().items():
        prices.setdefault(_name, _cost)
    prices.update({k: v for k, v in load_missile_costs().items() if v})

    fleets = collect_fleets()
    rows = []
    errors = 0
    skipped = []
    for path in fleets:
        try:
            fleet = fl.parse_fleet(str(path))
        except Exception as exc:  # noqa: BLE001
            errors += 1
            print(f"[skip] {path.name}: {exc}")
            continue
        for ship in fleet.ships:
            if ship_has_legacy(ship):
                skipped.append(f"{path.name}:{ship.name}")
                continue
            facts = ShipFacts(ship, fleet, idx, prices)
            self_current = facts
            base = [(c, check_one(c)) for c in spec["baseline"]["must"]]
            base_known = [(c, v) for c, v in base if v is not None]
            base_fails = [c for c, v in base_known if not v]
            results = []
            for cls in classes:
                checks = {}
                for cond in cls["must"]:
                    checks[cond] = check_one(cond)
                known = {k: v for k, v in checks.items() if v is not None}
                fails = [k for k, v in known.items() if not v]
                s_checks = {cond: check_one(cond) for cond in cls.get("should", [])}
                s_known = {k: v for k, v in s_checks.items() if v is not None}
                s_fails = [k for k, v in s_known.items() if not v]
                hull_ok = hull_allowed(cls, facts)
                results.append({
                    "class": cls["name"],
                    "cost": cls["cost"],
                    "bad": cls["bad"],
                    "fallback": cls["name"].startswith("A Cap (Any ship)"),
                    # "does not satisfy any other class" can only be decided after every
                    # other class has been evaluated, so it is resolved right below.
                    "exclusive": any("does not satisfy any other class" in m for m in cls["must"]),
                    "any_cost": cls.get("any_cost", False),
                    "variant_of": cls.get("variant_of"),
                    "must_total": len(cls["must"]),
                    "must_known": len(known),
                    "unknown": len(cls["must"]) - len(known),
                    "should_total": len(cls.get("should", [])),
                    "should_known": len(s_known),
                    "should_fails": s_fails,
                    "hull_ok": hull_ok,
                    "fails": fails,
                })
            # resolve the exclusivity must: true only when no ordinary class fits
            plain = [r for r in results
                     if not r["exclusive"] and not r["fails"] and not r["unknown"]
                     and not r["bad"] and r["hull_ok"]]
            for r in results:
                if not r["exclusive"]:
                    continue
                r["unknown"] = max(0, r["unknown"] - 1)
                if plain:
                    r["fails"] = r["fails"] + ["does not satisfy any other class"]
                else:
                    r["must_known"] = min(r["must_total"], r["must_known"] + 1)
            # range-only classes (carriers) carry no must line in Ship Builds.txt:
            # they are legitimate classes whose only requirement is the price band,
            # so a hull match is enough to make them a candidate.
            usable = [r for r in results if r["hull_ok"]]
            # a must that cannot be evaluated is not a pass: never award a class we
            # cannot verify (e.g. unpriced player missiles behind a ">1000 points" rule).
            fit = [r for r in usable if not r["fails"] and not r["unknown"] and not r["bad"]]
            in_range = [r for r in fit
                        if r.get("any_cost") or r["cost"][0] <= (ship.cost or 0) <= r["cost"][1]]
            # a class with fewer unsatisfied "should" lines is the better description;
            # then more verifiable musts; the price width is only the last tie-break.
            key = lambda r: (r["unknown"] == 0,
                             -(len(r["should_fails"]) if r["should_known"] else 0),
                             r["must_known"],
                             -(r["cost"][1] - r["cost"][0]))
            matched = sorted(in_range, key=key, reverse=True)
            bad_fit = [r for r in usable if not r["fails"] and not r["unknown"] and r["bad"] and not r.get("fallback")]
            fallback = next((r for r in results if r.get("fallback")), None)
            armed = bool(facts.turrets or facts.casemates or facts.spinal or facts.launchers
                         or facts.jammers)
            if in_range:
                verdict, best = "match", matched[0]
            elif fit:
                # Ship Builds.txt says the cost band is a reference, not a hard gate:
                # a build that meets every must is still that class, just an unusual
                # price point (report it, do not demote it to "unclassifiable").
                verdict, best = "match", max(fit, key=key)
            elif bad_fit:
                verdict, best = "bad_class", max(bad_fit, key=key)
            elif fallback is not None and armed:
                # "A Cap (Any ship) (Bad)": an armed ship that satisfies no other class
                verdict, best = "bad_class", fallback
            else:
                pool = usable or results
                best = max(pool, key=lambda r: (r["must_known"] - len(r["fails"]), -r["unknown"], r["must_known"]))
                verdict = "no_class"
            rows.append({
                "fleet": fleet.name,
                "fleet_path": str(path),
                "faction": fleet.faction,
                "ship": ship.name,
                "near": [
                    {
                        "class": r["class"],
                        "fails": r["fails"],
                        "unknown": r["unknown"],
                        "must_total": r["must_total"],
                        "cost": r["cost"],
                        "bad": r["bad"],
                        "in_band": (r.get("any_cost") or r["cost"][0] <= (ship.cost or 0) <= r["cost"][1]),
                    }
                    for r in sorted(
                        [r for r in usable if not r["bad"] and not r.get("fallback")],
                        key=lambda r: (len(r["fails"]), r["unknown"], -(r["must_known"])),
                    )[:4]
                ],
                "hull": facts.hull_name,
                "hull_abbr": facts.hull_abbr,
                "cost": ship.cost,
                "verdict": verdict,
                "class": best["class"] if verdict not in ("no_class", "bad_class") else
                         ("未归类" if verdict == "no_class" else best["class"]),
                "classes": ([r["class"] for r in matched] if matched
                            else ([best["class"]] if verdict in ("match", "bad_class") else [])),
                "cost_band": cost_band(best, ship.cost),
                "class_quality": {r["class"]: {
                    "must_total": r["must_total"], "must_known": r["must_known"],
                    "unknown": r["unknown"], "fails": r["fails"],
                    "should_total": r["should_total"], "should_known": r["should_known"],
                    "should_fails": r["should_fails"],
                    # Ship Builds.txt: the cost band is a "should", not a must.
                    "cost_ok": bool(r.get("any_cost") or r["cost"][0] <= (ship.cost or 0) <= r["cost"][1]),
                    "cost": r["cost"],
                } for r in (matched or [best])},
                "closest": best["class"],
                "class_cost": best["cost"],
                "must_total": best["must_total"],
                "must_known": best["must_known"],
                "fails": best["fails"],
                "baseline": f"{len(base_known) - len(base_fails)}/{len(base_known)}",
                "baseline_fails": base_fails,
                "draw_kw": round(facts.draw),
                "supply_kw": round(facts.supply),
                "power": power_model.analyse(facts.parts, boost_pct=facts.power_boost),
                "missile_pts": round(facts.missile_points),
                "calibers": facts.caliber_counts(),
                "launchers": {model: sum(1 for m, _, _i in facts.launchers if m == model)
                              for model in sorted({m for m, _n, _i in facts.launchers})},
                "jammers": len(facts.jammers),
                "unresolved": facts.unresolved,
            })
    self_current = None

    OUT_JSON.write_text(json.dumps({"rows": rows, "errors": errors}, ensure_ascii=False, indent=1),
                        encoding="utf-8")

    by_class = defaultdict(list)
    for r in rows:
        for name in (r.get("classes") or [r["class"]]):
            by_class[name].append(r)
    order = {c["name"]: i for i, c in enumerate(classes)}

    lines = ["# 舰船分类结果（依据 `Ship Builds.txt`）", ""]
    lines.append(
        f"舰队 {len({r['fleet_path'] for r in rows})} 支 · 舰船 {len(rows)} 艘 · 解析失败 {errors} 艘"
    )
    lines.append("")
    lines.append(
        "判定口径：**must 全部满足 + 价格落在区间 + 非 bad 类** = `match`；"
        "价格区间只是参考（Ship Builds.txt 明说不是硬门槛，Cost 按 should 处理）：must 全过的就是该舰级，价格出区间标 `偏高`（overpriced，堆料）或 `偏低`（underpriced，玩家口语 greed / shell / 贪污）。整艘船没有任何 must 全过的 class = `bad_class`（A Cap 兜底）。"
        "一艘船可以同时属于多个舰级（例如 Sprinter 同时是 `A Cap ffl` 与 `gun/cap ffl`），"
        "满足的会全部并列列出。"
    )
    lines.append(
        "`mount N` 类条件按 **Unity 预制体层级顺序**核对（序号取自游戏资源，已用 52 艘样本验证单调递增）。"
        "模块化民船（Bulk / Container 系列）没有顺序数据，相关条目按未知处理。"
    )
    lines.append("")
    lines.append("| 舰级 | 价格区间 | 艘数 | match | 偏高 | 偏低 |")
    lines.append("|---|---|---:|---:|---:|---:|")
    for name, items in sorted(by_class.items(), key=lambda kv: order.get(kv[0], 999)):
        m = sum(1 for r in items if r["verdict"] == "match")
        hi = sum(1 for r in items if r.get("cost_band") == "over")
        lo = sum(1 for r in items if r.get("cost_band") == "under")
        rng = next((r["class_cost"] for r in items if r["class_cost"]), [0, 0])
        lines.append(f"| {name} | {rng[0]}-{rng[1]} | {len(items)} | {m} | {hi} | {lo} |")
    lines.append("")

    for name, items in sorted(by_class.items(), key=lambda kv: order.get(kv[0], 999)):
        rng = next((r["class_cost"] for r in items if r["class_cost"]), [0, 0])
        items.sort(key=lambda r: (r["verdict"] != "match", r["cost"] or 0))
        lines.append(f"## {name}（{rng[0]}-{rng[1]}，共 {len(items)} 艘）")
        lines.append("")
        lines.append(
            "| 舰队 | 舰名 | 舰体 | 点数 | 判定 | 本类 must | 通用 must | 耗电/供电 (kW) | (n-1) 判定 |"
        )
        lines.append("|---|---|---|---:|---|---|---|---|---|")
        for r in items[:14]:
            tag = ""
            if r.get("cost_band") == "over":
                tag = " 偏高"
            elif r.get("cost_band") == "under":
                tag = " 偏低"
            if r.get("classes") and len(r["classes"]) > 1:
                r = dict(r, verdict=r["verdict"] + " [" + " / ".join(r["classes"]) + "]" + tag)
            elif tag:
                r = dict(r, verdict=r["verdict"] + tag)
            fails = "，".join(r["fails"])[:60]
            pw = r.get("power") or {}
            ptag = {
                "ok": "OK",
                "ok_shutdown": "(n-1) 可关",
                "overload": "超载",
                "no_powerplant": "无反应堆",
            }.get(pw.get("verdict"), "-")
            lines.append(
                f"| {r['fleet']} | {r['ship']} | {r['hull']} | {r['cost']} | "
                f"{r['verdict']}{(' (' + fails + ')') if fails else ''} | "
                f"{r['must_known']}/{r['must_total']} | {r['baseline']} | "
                f"{r['draw_kw']}/{r['supply_kw']} | {ptag} |"
            )
        if len(items) > 14:
            lines.append(f"| 等 | 共 {len(items) - 14} 艘 | | | | | | |")
        lines.append("")
    OUT_MD.write_text("\n".join(lines), encoding="utf-8")

    print(f"fleets={len({r['fleet_path'] for r in rows})} ships={len(rows)} classes={len(by_class)} skipped_legacy={len(skipped)}")
    print("verdicts:", dict(Counter(r["verdict"] for r in rows)))
    print("power:", dict(Counter((r.get("power") or {}).get("verdict") for r in rows)))
    print("legacy skipped:", len(skipped))
    print("unresolved components:", dict(Counter(n for r in rows for n in r["unresolved"]).most_common(8)))
    print("wrote", OUT_JSON, OUT_MD)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

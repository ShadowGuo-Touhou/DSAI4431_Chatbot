"""Missile point-cost calculator (NEBULOUS: Fleet Command).

Formula taken from the decompiled source `other info/Nebulous.decompiled.cs`:

  ModularMissile.PointCost                     line 117571
      cost = max(ceil(bodyCost + sum(socket.Installed.PointCost)), 1)

  MissileComponentDescriptor.PointCost         line 123736
      cost = _pointCost * body.UniformCostScaling          (scaling is 1.0 for every stock body)

  Seeker.PointCost                             line 125858
      Mode=Targeting  -> base cost
      Mode=Validation -> validator cost

  MissileEngineDescriptor.PointCost            line 123961
      cost = lerp(_speedCost, BalanceValues.A)
           + lerp(_thrustCost, BalanceValues.C)
           + lerp(_flightTimeCost, BalanceValues.B)

  GuidanceComponent.PointCost                  line 126641
      cost = base cost + _maneuverCost[maneuvers]

The per-component `_pointCost` values come from the official wiki (Base Cost / Validator Cost).
The three engine cost ranges and the body `_pointCost` live in Unity assets, not in code or on the
wiki, so the calculator carries them as one measured residual per template and reports a range:

    body+engine in (total - sum, total - sum + 1]

Usage
-----
    python missile_cost.py --list
    python missile_cost.py --show "SGM-101 Violence"
    python missile_cost.py "SGM-101 Violence" --swap 1=Electro-Optical Seeker --mode 1=Targeting
"""

from __future__ import annotations

import argparse
import json
import math
import re
import xml.etree.ElementTree as ET
from dataclasses import dataclass, field, replace
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
TEMPLATES = ROOT / "other info" / "missles"
WIKI = ROOT / "domain" / "kb" / "raw_official" / "munition" / "munitions-missiles.json"
CALIBRATION = ROOT / "domain" / "data" / "missile_body_engine.json"

NUM = re.compile(r"-?\d+(?:\.\d+)?")


def _number(text: str | None) -> float | None:
    if text is None:
        return None
    hit = NUM.search(str(text))
    return float(hit.group()) if hit else None


@dataclass(frozen=True)
class Price:
    base: float
    validator: float

    def of(self, mode: str | None) -> float:
        return self.validator if (mode or "").lower().startswith("valid") else self.base


def load_prices() -> dict[str, Price]:
    """Component prices from the official wiki, keyed case-insensitively."""
    data = json.loads(WIKI.read_text(encoding="utf-8"))
    out: dict[str, Price] = {}
    for ent in data["entities"]:
        fields = ent["fields"]
        combined = fields.get("Base Cost / Validator Cost")
        if combined is not None:
            parts = [p.strip() for p in str(combined).split("/")]
            base = _number(parts[0])
            validator = _number(parts[-1]) if len(parts) > 1 else base
        else:
            base = _number(fields.get("Base Cost (pts)") or fields.get("Base Cost"))
            validator = base
        if base is None:
            continue
        out[ent["name"].casefold()] = Price(base, float(validator if validator is not None else base))
    return out


def lookup(prices: dict[str, Price], name: str | None) -> Price | None:
    if not name:
        return None
    return prices.get(name.casefold())


@dataclass
class Slot:
    index: int
    size: int
    component: str | None
    mode: str | None
    settings: dict[str, str] = field(default_factory=dict)

    def clone(self) -> "Slot":
        return replace(self, settings=dict(self.settings))


@dataclass
class Template:
    slug: str
    designation: str
    nickname: str
    body: str
    cost: int
    slots: list[Slot]

    @property
    def title(self) -> str:
        return f"{self.designation} {self.nickname}".strip()


def parse_template(path: Path) -> Template:
    root = ET.parse(path).getroot()
    slots: list[Slot] = []
    for index, sock in enumerate(root.iter("MissileSocket"), start=1):
        comp = sock.find("InstalledComponent")
        name = mode = None
        settings: dict[str, str] = {}
        if comp is not None:
            key = comp.findtext("ComponentKey")
            name = key.split("/")[-1] if key else None
            mode = comp.findtext("Mode")
            for child in comp:
                if isinstance(child.tag, str) and len(child) == 0 and child.text:
                    settings[child.tag] = child.text.strip()
        slots.append(Slot(index, int(sock.findtext("Size") or 0), name, mode, settings))
    return Template(
        slug=path.stem,
        designation=(root.findtext("Designation") or "").strip(),
        nickname=(root.findtext("Nickname") or "").strip(),
        body=(root.findtext("BodyKey") or "?").split("/")[-1],
        cost=int(root.findtext("Cost") or 0),
        slots=slots,
    )


def component_sum(template: Template, prices: dict[str, Price]) -> tuple[float, list[str]]:
    total = 0.0
    unknown: list[str] = []
    for slot in template.slots:
        price = lookup(prices, slot.component)
        if price is None:
            if slot.component is None:
                unknown.append(f"#{slot.index} engine (not priced on the wiki)")
            else:
                unknown.append(f"#{slot.index} {slot.component} (not priced on the wiki)")
            continue
        total += price.of(slot.mode)
    return total, unknown


def body_engine_range(template: Template, prices: dict[str, Price]) -> tuple[float, float]:
    """The body+engine term can only be bounded: (total - sum, total - sum + 1]."""
    comp_sum, _ = component_sum(template, prices)
    low = template.cost - comp_sum
    return low, low + 1.0


def load_calibration() -> dict[str, float]:
    if not CALIBRATION.exists():
        return {}
    return {k: float(v) for k, v in json.loads(CALIBRATION.read_text(encoding="utf-8")).items()}


def predict(template: Template, prices: dict[str, Price], *, calibrated: float | None = None) -> dict:
    """Cost bounds for the current (possibly edited) template."""
    comp_sum, unknown = component_sum(template, prices)
    if calibrated is not None:
        return {"comp_sum": comp_sum, "unknown": unknown, "low": math.ceil(calibrated + comp_sum), "high": math.ceil(calibrated + comp_sum)}
    base = template.cost - comp_sum  # measured with the *original* component set
    # Recover the original sum so a replacement keeps the same unknown engine term:
    return {"comp_sum": comp_sum, "unknown": unknown, "low": math.ceil(base + comp_sum), "high": math.ceil(base + 1 + comp_sum)}


def simulate(original: Template, edited: Template, prices: dict[str, Price], calibrated: float | None) -> dict:
    orig_sum, _ = component_sum(original, prices)
    origin_term = original.cost - orig_sum  # body+engine as measured
    if calibrated is not None:
        origin_term = calibrated
    new_sum, unknown = component_sum(edited, prices)
    low = math.ceil(origin_term + new_sum)
    high = math.ceil(origin_term + 1.0 + new_sum) if calibrated is None else low
    return {"origin_term": origin_term, "new_comp_sum": new_sum, "low": low, "high": high, "unknown": unknown}


def apply_edits(template: Template, swaps: list[str], modes: list[str], maneuvers: list[str]) -> Template:
    slots = [s.clone() for s in template.slots]
    by_index = {s.index: s for s in slots}
    for spec in swaps:
        if "=" not in spec:
            raise SystemExit(f"--swap expects N=Component, got {spec!r}")
        where, name = spec.split("=", 1)
        slot = by_index[int(where)]
        slot.component = name.strip()
        slot.mode = "Targeting"
    for spec in modes:
        where, value = spec.split("=", 1)
        by_index[int(where)].mode = value.strip()
    for spec in maneuvers:
        where, value = spec.split("=", 1)
        by_index[int(where)].settings["Maneuvers"] = value.strip()
    return replace(template, slots=slots)


def print_template(template: Template, prices: dict[str, Price], calibrated: float | None) -> None:
    comp_sum, unknown = component_sum(template, prices)
    print(f"{template.title}  [{template.slug}]")
    print(f"  body      : {template.body}")
    print(f"  saved cost: {template.cost}")
    print(f"  {'#':<3}{'size':<5}{'component':<44}{'mode':<11}{'pts':>6}")
    for slot in template.slots:
        price = lookup(prices, slot.component)
        value = price.of(slot.mode) if price else None
        shown = f"{value:g}" if value is not None else "?"
        label = slot.component or "engine (balance values)"
        print(f"  {slot.index:<3}{slot.size:<5}{label:<44}{(slot.mode or '-'):<11}{shown:>6}")
    print(f"  components: {comp_sum:g} pts (unknown: {', '.join(unknown) if unknown else 'none'})")
    low, high = body_engine_range(template, prices)
    print(f"  body+engine: ({low:g}, {high:g}]   measured from this template")
    if calibrated is not None:
        print(f"  body+engine (calibrated): {calibrated:g}")


def main() -> int:
    ap = argparse.ArgumentParser(description="Missile point-cost calculator")
    ap.add_argument("template", nargs="?", help="template name fragment, e.g. 'SGM-101 Violence'")
    ap.add_argument("--list", action="store_true", help="list every template with its residual")
    ap.add_argument("--show", action="store_true", help="print the slot table")
    ap.add_argument("--swap", action="append", default=[], metavar="N=COMPONENT")
    ap.add_argument("--mode", action="append", default=[], metavar="N=TARGETING|VALIDATION")
    ap.add_argument("--maneuver", action="append", default=[], metavar="N=LEVEL")
    args = ap.parse_args()

    prices = load_prices()
    calibration = load_calibration()
    templates = [parse_template(p) for p in sorted(TEMPLATES.glob("*.missile"))]

    if args.list or not args.template:
        print(f"wiki-priced components: {len(prices)}   templates: {len(templates)}\n")
        print(f"{'template':<34}{'body':<16}{'cost':>5}{'comps':>7}{'body+engine':>13}")
        for t in templates:
            comp_sum, _ = component_sum(t, prices)
            low, high = body_engine_range(t, prices)
            cal = calibration.get(t.slug)
            note = f"{cal:g} (calibrated)" if cal is not None else f"({low:g}, {high:g}]"
            print(f"{t.slug:<34}{t.body:<16}{t.cost:>5}{comp_sum:>7.2f}{note:>13}")
        return 0

    needle = args.template.casefold()
    match = [t for t in templates if needle in t.title.casefold() or needle in t.slug.casefold()]
    if not match:
        raise SystemExit(f"no template matches {args.template!r}")
    template = match[0]
    calibrated = calibration.get(template.slug)

    if not (args.swap or args.mode or args.maneuver):
        print_template(template, prices, calibrated)
        return 0

    edited = apply_edits(template, args.swap, args.mode, args.maneuver)
    print(f"{template.title}: {template.cost} pts")
    result = simulate(template, edited, prices, calibrated)
    print(f"  body+engine term: {result['origin_term']:g}")
    print(f"  components now  : {result['new_comp_sum']:g} pts")
    if result["unknown"]:
        print(f"  unpriced        : {', '.join(result['unknown'])}")
    if result["low"] == result["high"]:
        print(f"  => new cost: {result['low']} pts (exact)")
    else:
        print(f"  => new cost: {result['low']} or {result['high']} pts "
              f"(the +1 depends on whether the fractional body+engine part crosses an integer)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

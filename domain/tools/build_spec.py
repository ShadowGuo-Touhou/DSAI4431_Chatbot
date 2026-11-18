"""Parse `other info/Ship Builds.txt` into a machine-readable class spec.

Format facts that drive the parser:
  - preamble explains Must/Should/Optional/Costs, then `Baseline: For all ships`
  - each class = a name line, then `Cost: a - b` (carriers use a bare `a - b` line),
    then optional `must:` / `should:` / `optional` / `avoid:` sub-sections
  - one stray alias line exists (`mass driver (md) ln` right before `450 ln`), so the
    class name is taken as the last non-header line before the cost line
  - `(variant of X)` and `(bad)` markers live inside the class name
  - a trailing glossary starts at `definition of hardkill:`
"""

from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SRC = ROOT / "other info" / "Ship Builds.txt"
OUT = ROOT / "domain" / "spec" / "ship_builds.json"

COST_RE = re.compile(r"^cost\w*\s*:?\s*(\d+)\s*-\s*(\d+)\s*$", re.I)
RANGE_RE = re.compile(r"^(\d+)\s*-\s*(\d+)\s*$")
#: `must:` / `must` — some entries omit the colon, some carry the condition inline
SECTION_RE = re.compile(r"^(must|should|optional|avoid)s?\s*:?\s*(.*)$", re.I)
VARIANT_RE = re.compile(r"\(variant of ([^)]+)\)", re.I)
BAD_RE = re.compile(r"\(bad\)", re.I)
DIVIDER_RE = re.compile(r"^-{2,}.*-{2,}$")
GLOSSARY_RE = re.compile(r"^definition of (.+?):\s*$", re.I)
NOTE_RE = re.compile(r"^\*")

PREAMPLE_STOP = "Baseline"
PREAMBLE_STOP = PREAMPLE_STOP


def load_lines(path: Path) -> list[str]:
    text = path.read_text(encoding="utf-8-sig")
    return [ln.rstrip() for ln in text.splitlines()]


def parse(path: Path = SRC) -> dict:
    lines = load_lines(path)
    cost_idx: list[int] = []
    for i, ln in enumerate(lines):
        s = ln.strip()
        if not s:
            continue
        if COST_RE.match(s) or RANGE_RE.match(s):
            cost_idx.append(i)

    # class name = last meaningful line before each cost line, skipping headers/costs
    name_of: dict[int, str] = {}
    for c in cost_idx:
        j = c - 1
        while j >= 0:
            s = lines[j].strip()
            if not s or SECTION_RE.match(s) or COST_RE.match(s) or RANGE_RE.match(s):
                j -= 1
                continue
            name_of[c] = s
            break

    # locate the actual index of each name we picked (last non-skipped line before c)
    boundaries: list[tuple[int, str, int]] = []  # (start_idx, name, cost_idx or -1)
    for c, name in sorted(name_of.items()):
        start = None
        for j in range(c - 1, -1, -1):
            if lines[j].strip() == name:
                start = j
                break
        if start is not None:
            boundaries.append((start, name, c))

    # `(bad)` classes carry no cost line at all -> they never matched a boundary above
    baseline_idx = 0
    for i, ln in enumerate(lines):
        if ln.strip().startswith(PREAMBLE_STOP):
            baseline_idx = i
            break
    used_starts = {b[0] for b in boundaries}
    for i, ln in enumerate(lines):
        if i in used_starts or i <= baseline_idx:
            continue
        s = ln.strip()
        if not s or SECTION_RE.match(s):
            continue
        if not re.search(r"\(bad\)\s*$", s, re.I):
            continue
        boundaries.append((i, s, -1))

    boundaries.sort(key=lambda b: b[0])
    first_class = boundaries[0][0] if boundaries else len(lines)

    # baseline block
    baseline_start = None
    for i, ln in enumerate(lines):
        if ln.strip().startswith(PREAMBLE_STOP):
            baseline_start = i
            break

    classes: list[dict] = []
    for k, (start, name, cost_idx_line) in enumerate(boundaries):
        end = boundaries[k + 1][0] if k + 1 < len(boundaries) else len(lines)
        if cost_idx_line >= 0:
            cost_line = lines[cost_idx_line].strip()
            m = COST_RE.match(cost_line) or RANGE_RE.match(cost_line)
            cost_lo, cost_hi = (int(m.group(1)), int(m.group(2))) if m else (0, 0)
        else:
            cost_lo = cost_hi = 0
        variant = VARIANT_RE.search(name)
        bad = bool(BAD_RE.search(name))
        clean = BAD_RE.sub("", VARIANT_RE.sub("", name)).strip()
        prev_line = lines[start - 1].strip() if start > 0 else ""
        block = lines[start + 1 : end]
        sections: dict[str, list[str]] = {"must": [], "should": [], "optional": [], "avoid": []}
        cur = None
        for ln in block:
            s = ln.strip()
            if not s:
                continue
            if COST_RE.match(s) or RANGE_RE.match(s):
                continue
            sec = SECTION_RE.match(s)
            if sec:
                cur = sec.group(1).lower()
                inline = sec.group(2).strip()
                if inline:  # e.g. `must: have a EWR radar and/or LRT radar`
                    sections[cur].append(inline)
                continue
            if DIVIDER_RE.match(s) or NOTE_RE.match(s):
                continue
            if cur is None:
                continue
            sections[cur].append(s)
        classes.append({
            "name": clean,
            "raw_name": name,
            "prev_line": prev_line,
            "bad": bad,
            "variant_of": variant.group(1).strip() if variant else "",
            "cost": [cost_lo, cost_hi],
            # a class written without a Cost line (most `(bad)` ones) has no band to
            # compare against, so its cost check is vacuous rather than always failing.
            "any_cost": cost_hi <= 0,
            "recommend": not (bad or clean.startswith("unarmed")),
            "must": sections["must"],
            "should": sections["should"],
            "optional": sections["optional"],
            "avoid": sections["avoid"],
        })

    # the source has one block whose name line is a leftover alias followed by a typo
    # (`mass driver (md) ln` then `450 ln`); rename duplicates from the preceding line
    seen: dict[str, int] = {}
    for c in classes:
        key = c["name"].lower()
        if key in seen:
            prev = c["prev_line"]
            if prev and not SECTION_RE.match(prev) and not prev.startswith(("-", "*")):
                c["alias_of"] = c["name"]
                c["name"] = prev
        else:
            seen[key] = 1

    baseline: dict[str, list[str]] = {"must": [], "should": [], "avoid": []}
    if baseline_start is not None:
        cur = None
        for ln in lines[baseline_start + 1 : first_class]:
            s = ln.strip()
            if not s:
                continue
            sec = SECTION_RE.match(s)
            if sec and sec.group(1).lower() in baseline:
                cur = sec.group(1).lower()
                continue
            if cur:
                baseline[cur].append(s)

    glossary: dict[str, list[str]] = {}
    gstart = None
    for i, ln in enumerate(lines):
        if GLOSSARY_RE.match(ln.strip()):
            gstart = i
            break
    if gstart is not None:
        cur = None
        for ln in lines[gstart:]:
            s = ln.strip()
            g = GLOSSARY_RE.match(s)
            if g:
                cur = g.group(1).strip()
                glossary[cur] = []
                continue
            if cur and s:
                glossary[cur].append(s)

    return {"baseline": baseline, "classes": classes, "glossary": glossary}


#: Every class also requires the right hull.  The source file only encodes that in
#: the class name, which is why a 425-point Bulk Feeder used to satisfy "greed CH".
#: A token is either a hull abbreviation (`CH`) or a substring of the hull name
#: (`Tug`, `Shuttle`, `Sprinter`) for the hulls that have no abbreviation.
HULL_MUST: list[tuple[str, list[str]]] = [
    (r"cve/cvl", ["CVE", "CVL"]),
    (r"full cve", ["CVE"]),
    (r"cvln", ["Container"]),
    (r"^\s*450 CH\b|^\s*greed CH\b|^\s*CCK CH\b|^\s*missile CH\b|^\s*250 CH\b|^\s*rail CH\b"
     r"|Command Cruiser killer|\(CCK\)", ["CH"]),
    (r"^\s*450 CC\b|^\s*missile CC\b|^\s*S2CC\b|^\s*Rail CC\b|^\s*250 CC\b", ["CC"]),
    (r"^\s*450 BB\b|^\s*TCSG BB\b|^\s*250 BB\b|^\s*Beam BB\b|^\s*rail BB\b", ["BB"]),
    (r"\bln\b", ["LN"]),
    (r"\bCL\b", ["CL"]),
    (r"\bDD\b", ["DD"]),
    (r"\bFF\b", ["FF"]),
    (r"\bMN\b", ["MN"]),
    (r"^rocket shuttle", ["Ferryman"]),
    (r"^missile sprinter", ["Sprinter"]),
    # every class written "(sprinter or shuttle)" means the civilian FFL pair, never
    # the tug: in game the Draugr Clipper still reports FFL, but players treat "tug"
    # as its own class and the tug classes below own it.
    (r"\(sprinter or shuttle\)", ["Sprinter", "Ferryman"]),
    (r"tug", ["Draugr", "Tug"]),
    (r"shuttle", ["Ferryman"]),
    (r"sprinter", ["Sprinter"]),
    (r"\bffl\b", ["Sprinter", "Ferryman", "Draugr"]),
]


def hull_tokens(name: str) -> list[str]:
    for pattern, tokens in HULL_MUST:
        if re.search(pattern, name, re.I):
            return list(tokens)
    return []


def apply_hulls(spec: dict) -> None:
    by_name = {c["name"]: c for c in spec["classes"]}
    for cls in spec["classes"]:
        if cls.get("variant_of"):
            parent = by_name.get(cls["variant_of"])
            cls["hulls"] = list(parent.get("hulls", [])) if parent else hull_tokens(cls["name"])
            cls["hulls_from"] = cls["variant_of"]
        else:
            cls["hulls"] = hull_tokens(cls["name"])
            cls["hulls_from"] = ""
        if cls["name"] in HULL_OVERRIDE:
            cls["hulls"] = list(HULL_OVERRIDE[cls["name"]])
            cls["hulls_from"] = "HULL_OVERRIDE"
    spec["classes"].extend(EXTRA_CLASSES)


#: 名字里没有舰体缩写的舰级，手工绑定到舰体。
#: `CV (ANS)` 是用户为 Worden 这类「航母当战列舰」开的兜底类，只该匹配 CV。
HULL_OVERRIDE: dict[str, list[str]] = {
    "CV (ANS)": ["CV"],
}


#: Classes that are not (yet) in `Ship Builds.txt`, added on the user's instruction.
#: `unarmed` applies to every hull and is defined by the game's own rule: no cannon,
#: no turret, no offensive missile (a 1-point offensive S1 arming missile counts as
#: a weapon), no jammer.  Unarmed ships still contest a point but cannot capture it,
#: and a team with only unarmed ships loses immediately.
EXTRA_CLASSES: list[dict] = [
    {
        "name": "unarmed (any hull)",
        "cost": [0, 12000],
        "any_cost": True,
        "bad": False,
        "recommend": False,
        "recommend": False,
        "variant_of": "",
        "must": ["have no offensive weapons (no cannon, no turret, no offensive missile, no arming missile, no jammer)"],
        "should": [],
        "optional": [],
        "avoid": [],
        "hulls": [],
        "hulls_from": "all hulls",
    },
]


def main() -> int:
    spec = parse()
    apply_hulls(spec)
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(spec, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"baseline must={len(spec['baseline']['must'])} should={len(spec['baseline']['should'])} avoid={len(spec['baseline']['avoid'])}")
    print(f"classes: {len(spec['classes'])}")
    for c in spec["classes"]:
        flag = "bad" if c["bad"] else ("var:" + c["variant_of"] if c["variant_of"] else "")
        print(f"  {c['name'][:38]:40} {c['cost'][0]:>4}-{c['cost'][1]:<4} must={len(c['must']):<2} should={len(c['should']):<2} opt={len(c['optional']):<2} avoid={len(c['avoid']):<2} {flag}")
    print("glossary keys:", list(spec["glossary"]))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

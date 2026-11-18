"""Fail if the hull-socket data and the real saves disagree.

The bug this guards against: the tools believed the Flathead Monitor was a modular
hull and wrote `<HullConfig>` (bow/core/stern segments) for it, even though not one
saved Flathead has a `<HullConfig>`.  The three claims that made it wrong are checked
here, against every `.fleet` we have:

  1. every `<HullSocket><Key>` of a ship exists in `hulls.sockets(HullType)`;
  2. a `<HullConfig>` appears only on the three section hulls (`hulls.SECTIONS`);
  3. every `<SegmentConfiguration><Key>` is a segment GUID of that hull's family.

A fourth check covers the generated KB: every `sockets/….md` link in
`domain/kb/socket_docs` must resolve, and the socket totals in the page headers must
match `hull_sockets.json`.

Usage: python domain/tools/audit_sockets.py [--docs domain/kb/socket_docs] [--quiet]
Exit code 0 = clean, 1 = at least one real finding (warnings do not fail the run).
"""

from __future__ import annotations

import argparse
import json
import pathlib
import re
import sys
import xml.etree.ElementTree as ET
from collections import Counter, defaultdict

ROOT = pathlib.Path(Path(__file__).resolve().parents[2])
sys.path.insert(0, str(ROOT / "domain" / "tools"))
import hulls as hu  # noqa: E402

STEAM_FLEETS = pathlib.Path(
    r"E:\SteamLibrary\steamapps\common\Nebulous\Saves\Fleets")


def fleet_paths() -> list[pathlib.Path]:
    """Every `.fleet` in the repo plus, when present, the game's own save folder."""
    seen: dict[str, pathlib.Path] = {}
    for base in ("sample fleets", "other info", "fleet", "data"):
        root = ROOT / base
        if not root.exists():
            continue
        for path in root.rglob("*.fleet"):
            seen.setdefault(str(path.resolve()).lower(), path)
    kept = ROOT / "domain" / "data" / "fleets_kept.json"
    if kept.exists():
        try:
            for rec in json.loads(kept.read_text(encoding="utf-8")):
                path = pathlib.Path(rec.get("path") or "")
                if path.exists():
                    seen.setdefault(str(path.resolve()).lower(), path)
        except (json.JSONDecodeError, TypeError):
            pass
    if STEAM_FLEETS.exists():
        for path in STEAM_FLEETS.rglob("*.fleet"):
            seen.setdefault(str(path.resolve()).lower(), path)
    return sorted(seen.values(), key=lambda p: str(p).lower())


def audit_fleets(quiet: bool = False) -> tuple[int, list[str], list[str]]:
    errors: list[str] = []
    warnings: list[str] = []
    paths = fleet_paths()
    ships = 0
    per_hull: Counter = Counter()
    missing_keys: dict[str, Counter] = defaultdict(Counter)
    segment_letters: dict[str, Counter] = defaultdict(Counter)
    no_config: Counter = Counter()
    unknown: Counter = Counter()

    for path in paths:
        try:
            root = ET.parse(path).getroot()
        except ET.ParseError as exc:  # a truncated save must not kill the audit
            warnings.append(f"{path.name}: unreadable XML ({exc})")
            continue
        for ship in root.findall("./Ships/Ship"):
            hull = (ship.findtext("HullType") or "").strip()
            if not hull:
                continue
            ships += 1
            per_hull[hull] += 1
            table = hu.sockets(hull)
            keys = {str(k.text).strip() for k in ship.findall("./SocketMap/HullSocket/Key")}
            if not table:
                unknown[hull] += 1
                continue
            known = {e["key"] for e in table}
            for key in keys - known:
                missing_keys[hull][key] += 1

            config = ship.find("HullConfig")
            if config is not None and not hu.is_segmented(hull):
                errors.append(
                    f"{hull}: has <HullConfig> but is not a section hull "
                    f"(ship {ship.findtext('Name')!r} in {path.name})")
            if config is None and hu.is_segmented(hull):
                no_config[hull] += 1
                continue
            if config is None:
                continue
            guids = hu.segment_guids(hull)
            by_part = {part: {guids[letter][part] for letter in guids
                              if (guids.get(letter) or {}).get(part)}
                       for part in hu.PARTS}
            seg = [str(k.text).strip() for k in
                   config.findall("./PrimaryStructure/SegmentConfiguration/Key")]
            if len(seg) != 3:
                errors.append(f"{hull}: {len(seg)} <SegmentConfiguration> (expected 3) in {path.name}")
                continue
            parts = []
            for guid in seg:
                hit = [part for part in hu.PARTS if guid in by_part[part]]
                if not hit:
                    errors.append(
                        f"{hull}: unknown segment GUID {guid} in {path.name}")
                parts.append(hit[0] if hit else "?")
                if hit:
                    letter = next((l for l, g in guids.items() if (g or {}).get(hit[0]) == guid), "?")
                    segment_letters[hull][f"{hit[0]}-{letter}"] += 1
            if parts != list(hu.PARTS):
                errors.append(f"{hull}: segments are {parts} (expected bow/core/stern) in {path.name}")

    for hull, counter in sorted(missing_keys.items()):
        sample = ", ".join(f"{k}×{n}" for k, n in counter.most_common(3))
        errors.append(f"{hull}: {sum(counter.values())} socket keys not in its table ({sample})")
    for hull, n in sorted(unknown.items()):
        # 只有 stock 船体必须被 `hull_sockets.json` 覆盖；mod 船体不在这个仓库的范围内。
        if hull.lower().startswith("stock/"):
            errors.append(f"{hull}: no socket table ({n} ships) — stock hull must be mapped")
        else:
            warnings.append(f"{hull}: no socket table ({n} ships, mod hull — not modelled)")
    for hull, n in sorted(no_config.items()):
        warnings.append(f"{hull}: {n} ships without <HullConfig> (old saves)")
    if not quiet:
        print(f"fleets {len(paths)} | ships {ships} | hull types {len(per_hull)}")
        for hull, n in sorted(per_hull.items(), key=lambda kv: -kv[1]):
            table = hu.sockets(hull)
            tag = "seg" if hu.is_segmented(hull) else ("prefab" if table else "mod")
            letters = ""
            if segment_letters.get(hull):
                letters = "  " + ", ".join(f"{k}×{v}" for k, v in
                                           sorted(segment_letters[hull].items()))
            print(f"  {hull:34} {n:5} ships  {len(table):3} sockets ({tag}){letters}")
    return ships, errors, warnings


def audit_docs(docs: pathlib.Path) -> tuple[int, list[str]]:
    errors: list[str] = []
    if not docs.exists():
        return 0, errors
    data = json.loads((ROOT / "domain" / "data" / "hull_sockets.json").read_text(encoding="utf-8"))
    tables = {name: len(entry.get("sockets") or []) for name, entry in data.items()}
    pages = sorted(docs.glob("*.md"))
    for page in pages:
        text = page.read_text(encoding="utf-8")
        for link in re.findall(r"sockets/([A-Za-z0-9_.-]+\.md)", text):
            if not (docs / link).exists() and not (docs / "sockets" / link).exists():
                errors.append(f"{page.name}: dead link sockets/{link}")
        if text.startswith("# ") and "modular=true" in text.splitlines()[2]:
            # section page: the header claims a total, the merge must agree
            m = re.search(r"total=(\d+)", text.splitlines()[2])
            hull = hu.resolve(re.search(r"hull=([^;]+);", text.splitlines()[2]).group(1))
            got = len(hu.sockets(hull))
            if m and int(m.group(1)) != got:
                errors.append(f"{page.name}: total={m.group(1)} but hulls.sockets()={got}")
    return len(pages), errors


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--docs", default=str(ROOT / "domain" / "kb" / "socket_docs"))
    ap.add_argument("--quiet", action="store_true")
    ap.add_argument("--no-docs", action="store_true")
    args = ap.parse_args(argv)

    _, errors, warnings = audit_fleets(args.quiet)
    pages = 0
    if not args.no_docs:
        pages, doc_errors = audit_docs(pathlib.Path(args.docs))
        errors.extend(doc_errors)
        if not args.quiet:
            print(f"socket docs {pages} | dead links / totals {len(doc_errors)}")
    for warning in warnings:
        print(f"warn: {warning}")
    for error in errors:
        print(f"FAIL: {error}")
    print(f"{'FAILED' if errors else 'ok'} — {len(errors)} findings, {len(warnings)} warnings")
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))

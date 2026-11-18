"""Build ONE fleet that contains every LN bow x core combination, all ships empty.

The user then fits components in game and saves the fleet; because a `.fleet`
stores the socket **key** for every fitted component, reading the saved file
back tells us exactly which socket (and therefore which physical side) each
position is -- no verbal reporting needed.

9 ships = 3 bows x 3 cores (the stern does not add main mounts), so the normal
10-ship fleet cap is not exceeded and the No Ship Limits mod is not required.

    python domain/tools/gen_orientation_all.py
"""

from __future__ import annotations

import pathlib
import re
import sys
import tempfile

sys.path.insert(0, str(pathlib.Path(__file__).parent))

import build_fleet as bf  # noqa: E402

OUT = pathlib.Path(Path(__file__).resolve().parents[2] / "other info" / "LN orientation" / "ORI all.fleet")
LETTERS = ("A", "B", "C")
STERN = "B"


def build_one(bow: str, core: str, tmp: pathlib.Path) -> pathlib.Path:
    name = f"ORI {bow}{core}"
    return bf.build(
        {
            "hull": "Stock/Bulk Hauler",
            "name": name,
            "ship_name": name,
            "callsign": name,
            "faction": "Stock/Protectorate",
            "sections": (bow, core, STERN),
            "fills": {},
            "out": str(tmp / f"{bow}{core}.fleet"),
        }
    )


def ships_block(text: str) -> str:
    m = re.search(r"<Ships\b[^>]*>(.*)</Ships>", text, re.S)
    if not m:
        raise SystemExit("no <Ships> block")
    return m.group(1)


def main() -> int:
    bf.PARTS.update(bf.wiki_parts())
    tmp = pathlib.Path(tempfile.mkdtemp(prefix="ori-all-"))
    files = [build_one(b, c, tmp) for b in LETTERS for c in LETTERS]

    template = files[0].read_text(encoding="utf-8")
    head = template[: template.index("<Ships")]
    tail = template[template.index("</Ships>") + len("</Ships>"):]

    blocks = []
    total = 0.0
    for n, path in enumerate(files, start=1):
        text = path.read_text(encoding="utf-8")
        block = ships_block(text)
        block = re.sub(r"<Number>\d+</Number>", f"<Number>{500 + n}</Number>", block)
        blocks.append(block.strip("\n"))
        m = re.search(r"<Cost>([\d.]+)</Cost>", block)
        if m:
            total += float(m.group(1))

    head = re.sub(r"<Name>[^<]*</Name>", "<Name>ORI all</Name>", head, count=1)
    head = re.sub(r"<TotalPoints>[\d.]+</TotalPoints>", f"<TotalPoints>{total:g}</TotalPoints>", head)
    # a fleet with 9 ships must not carry the mod dependency list of a stock file
    head = re.sub(r"<ModDependencies\s*/>", "<ModDependencies />", head)

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(head + "<Ships>\n" + "\n".join(blocks) + "\n</Ships>" + tail, encoding="utf-8")
    print(f"wrote {OUT}  ships={len(blocks)}  total={total:g} pts")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

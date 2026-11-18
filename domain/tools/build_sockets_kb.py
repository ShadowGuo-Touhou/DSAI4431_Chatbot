"""Render one knowledge-base document per hull describing its socket layout.

Source: `domain/data/hull_sockets.json` (extracted from the game's asset bundles).
Each document lists every socket with its type, grid size, position on the hull
(derived from the socket transform), firing-arc limits and the component the
editor pre-inserts -- the things a player cannot see in one place in game.

Bullets are used instead of a markdown table on purpose: the project chunker
never splits tables, so a 30-row table would become one huge chunk.

    python build_sockets_kb.py            # write docs
    python build_sockets_kb.py --dry-run  # print one document
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from fleet_lib import save_key_name  # noqa: E402
from socket_lib import SocketTables  # noqa: E402

OUT_DIR = Path(__file__).resolve().parents[1] / "kb" / "docs" / "hull" / "sockets"

TYPE_ZH = {"Surface": "挂载", "Compartment": "舱室", "Module": "模块"}

# Hull types as they appear in `.fleet` files (`<Faction>/<Hull>`).
HULL_TYPES = {
    "Ocello Cruiser": "Stock/Ocello Cruiser",
    "Keystone Destroyer": "Stock/Keystone Destroyer",
    "Raines Frigate": "Stock/Raines Frigate",
    "Sprinter Corvette": "Stock/Sprinter Corvette",
    "Vauxhall Light Cruiser": "Stock/Vauxhall Light Cruiser",
    "Axford Heavy Cruiser": "Stock/Axford Heavy Cruiser",
    "Solomon Battleship": "Stock/Solomon Battleship",
    "Levy Escort Carrier": "Stock/Levy Escort Carrier",
    "Worden Fleet Carrier": "Stock/Worden Fleet Carrier",
    "Mercator Oiler": "Stock/Mercator Oiler",
    "Ore Carrier": "Stock/Ore Carrier",
    "Shuttle Clipper": "Stock/Shuttle",
    "Tug Clipper": "Stock/Tugboat",
    "Bulk Clipper": "Stock/Bulk Feeder",
    "Bulk": "Stock/Bulk Hauler",
    "Container": "Stock/Container Hauler",
}

SLUG = re.compile(r"[^a-z0-9]+")


def slug(text: str) -> str:
    return SLUG.sub("-", text.lower()).strip("-")


def band(value: float, low: float, high: float) -> str:
    span = high - low or 1.0
    where = (value - low) / span
    if where < 0.2:
        return "艉部"
    if where < 0.4:
        return "后段"
    if where < 0.6:
        return "中段"
    if where < 0.8:
        return "前段"
    return "艏部"


def side(x: float) -> str:
    if abs(x) < 0.4:
        return "中轴"
    return "右舷" if x > 0 else "左舷"


def deck(y: float, low: float, high: float) -> str:
    span = high - low or 1.0
    where = (y - low) / span
    if where < 0.25:
        return "低甲板"
    if where > 0.75:
        return "高甲板"
    return "中甲板"


def describe_position(socket, xs: list[float], ys: list[float], zs: list[float]) -> str:
    x, y, z = socket.pos
    parts = [band(z, min(zs), max(zs)), side(x)]
    if abs(x) > 0.4:
        parts.append(f"外伸 {abs(x):.2f} 米")
    height = deck(y, min(ys), max(ys))
    if height != "中甲板":
        parts.append(height)
    parts.append(f"坐标 ({x:.2f}, {y:.2f}, {z:.2f})")
    return "，".join(parts)


def describe_arc(socket) -> str:
    trav = socket.traverse
    if not trav:
        return "固定安装，无转向射界"
    left = trav.get("left")
    right = trav.get("right")
    elev = trav.get("elevation") if trav.get("use_elevation") else None
    text = f"射界 左右各 {left:.0f}°"
    if elev is not None:
        text += f"，俯仰 {elev:.0f}°"
    return text


def render(hull_name: str, hull_type: str, sockets) -> str:
    counts: dict[str, int] = {}
    for socket in sockets.values():
        counts[socket.type] = counts.get(socket.type, 0) + 1
    aliases: list[str] = []
    for name in (hull_name, hull_type, save_key_name(hull_type)):
        if name and name not in aliases:
            aliases.append(name)
    xs = [s.pos[0] for s in sockets.values()]
    ys = [s.pos[1] for s in sockets.values()]
    zs = [s.pos[2] for s in sockets.values()]

    lines = [
        f"# {hull_name} › 插槽分布（HullSocket 数据）",
        "",
        f"别名：{' / '.join(aliases)}",
        "",
        f"{hull_name} 共有 {len(sockets)} 个插槽：" + "、".join(
            f"{counts[t]} 个{TYPE_ZH.get(t, t)}" for t in ("Surface", "Compartment", "Module") if t in counts
        ) + "。",
        "",
        "位置按舰体本地坐标给出（+z 指向舰艏，+x 指向右舷，单位米，数值已四舍五入）；"
        "尺寸为 0.25 米网格（例如 6×4×6 = 1.5×1.0×1.5 米）。数据取自游戏资源包里的 "
        "HullSocket 组件，与游戏内装配时使用的是同一套判定。",
        "",
    ]
    for stype in ("Surface", "Compartment", "Module"):
        group = sorted((s for s in sockets.values() if s.type == stype), key=lambda s: s.short)
        if not group:
            continue
        lines.append(f"## {TYPE_ZH.get(stype, stype)}（{len(group)}）")
        lines.append("")
        for socket in group:
            size = "×".join(str(c) for c in socket.cells)
            dims_m = " × ".join(f"{c * 0.25:g}" for c in socket.cells)
            default = f"，默认安装 {save_key_name(socket.default)}" if socket.default else ""
            lines.append(
                f"- {socket.short}：{TYPE_ZH.get(stype, stype)}插槽，{size} 格（{dims_m} 米），"
                f"{describe_position(socket, xs, ys, zs)}，{describe_arc(socket)}{default}"
            )
        lines.append("")
    return "\n".join(lines).rstrip() + "\n"


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dry-run", action="store_true", help="print the first document only")
    parser.add_argument("--out", type=Path, default=OUT_DIR)
    args = parser.parse_args(argv)

    tables = SocketTables()
    if not tables.available:
        print(f"socket table missing: {tables.path}", file=sys.stderr)
        return 2

    written = 0
    skipped: list[str] = []
    for hull_name, hull_type in HULL_TYPES.items():
        hull = tables.hull(hull_type)
        if hull is None or len(hull) < 3:
            skipped.append(hull_name)
            continue
        text = render(hull_name, hull_type, hull.sockets)
        if args.dry_run:
            print(text)
            return 0
        path = args.out / f"{slug(hull_name)}.md"
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8")
        written += 1
        label = str(path.relative_to(args.out.parents[3]))
        print(f"  {label:58s} {len(hull):3d} sockets")

    print(f"{written} document(s) -> {args.out}")
    if skipped:
        print(f"skipped (no socket table): {', '.join(skipped)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

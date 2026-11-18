"""按目标点数自动装满一艘船（贪心 + 背包），用于生成演示舰队。

用法：
    python domain/tools/demo_fleet_3000.py --hull "Stock/Sprinter Corvette" \
        --count 10 --total 3000 --name "Ten Gun Sprinters" --out "ten_gun_sprinters.fleet"

规则：
  - 先用 essentials（CIC / drive / reactor / 弹药库）占掉必要槽位；
  - 剩下的每个空槽用背包（按点数）挑最贵且装得下的部件，直到逼近每艘目标点数；
  - 只用原版（非 $MOD）部件，全部按 wiki 尺寸做逐轴校验。
"""

from __future__ import annotations

import argparse
import itertools
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))

import build_fleet as bf  # noqa: E402

ESSENTIALS = [
    ("Compartment", ["Basic CIC", "Reinforced CIC"]),
    ("Module", ["FR3300 Micro Reactor", "Fr4800 Reactor", "FM200 Drive"]),
    ("Compartment", ["Citadel Magazine", "Reinforced Magazine", "Bulk Magazine"]),
]


KIND_BY_TAG = {"mount": "Surface", "compartment": "Compartment", "module": "Module"}


def candidates() -> list[dict]:
    """所有原版部件，带尺寸与点数（kind 取自知识库文档的 Tags 行）。"""
    bf.PARTS.update(bf.wiki_parts())
    docs = pathlib.Path(__file__).resolve().parents[1] / "kb" / "docs" / "component"
    out = []
    for path in docs.glob("*.md"):
        text = path.read_text(encoding="utf-8", errors="ignore")
        title = ""
        kind = ""
        for line in text.splitlines()[:12]:
            if line.startswith("# "):
                title = line[2:].strip()
            elif line.startswith("Tags:"):
                for chunk in line[5:].split(";"):
                    if "=" in chunk and chunk.split("=")[0].strip() == "kind":
                        kind = chunk.split("=")[1].strip()
        info = bf.part(title) if title else None
        if not info or not info.get("dims") or info.get("cost") is None:
            continue
        slot = KIND_BY_TAG.get(kind)
        if not slot:
            continue
        out.append({"name": info["name"], "kind": slot, "size": info["dims"], "cost": float(info["cost"])})
    return out


def pick(pool: list[dict], sockets: list[dict], target: float, hull_cost: float = 0.0, seed: dict | None = None) -> dict[str, str] | None:
    """返回 {socket 短名: 部件名}。默认件先占位（游戏里空槽会自动装默认件）。"""
    chosen: dict[str, str] = dict(seed or {})
    for s in sockets:
        if s["short"] in chosen:
            continue
        default = (s.get("default_component") or "").split("/")[-1]
        if default and bf.part(default):
            chosen[s["short"]] = bf.part(default)["name"]
    free = [s for s in sockets if s["short"] not in chosen]
    # 1) essentials
    for kind, names in ESSENTIALS:
        for nm in names:
            part = bf.part(nm)
            if not part or not part.get("dims"):
                continue
            for s in free:
                if s["type"] != kind or s["short"] in chosen:
                    continue
                if bf.fits(part["dims"], s["size"]):
                    chosen[s["short"]] = nm
                    break
    # 2) knapsack on the rest
    rest = [s for s in free if s["short"] not in chosen]
    spend = sum(bf.part(n)["cost"] for n in chosen.values() if bf.part(n))
    budget = target - hull_cost - spend
    if budget < 0:
        budget = 0
    options: list[list[tuple[str, float]]] = []
    for s in rest:
        opts = [
            (c["name"], c["cost"])
            for c in pool
            if c["kind"] == s["type"] and c["size"] and bf.fits(c["size"], s["size"])
        ]
        opts.sort(key=lambda x: -x[1])
        options.append(opts[:12])
    dp: dict[int, tuple[list[str], float]] = {0: ([], 0.0)}
    for opts in options:
        nxt: dict[int, tuple[list[str], float]] = {}
        for spent_k, (picked, real) in dp.items():
            for name, cost in opts:
                key = int(spent_k + cost)
                if key > int(budget):
                    continue
                cand = (picked + [name], real + cost)
                if key not in nxt or cand[1] > nxt[key][1]:
                    nxt[key] = cand
        if nxt:
            dp = nxt
    if not dp:
        return chosen or None
    best = max(dp.items(), key=lambda kv: (kv[1][1], kv[0]))[1][0]
    for s, name in zip(rest, best):
        chosen[s["short"]] = name
    return chosen


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--hull", required=True)
    ap.add_argument("--count", type=int, default=1)
    ap.add_argument("--total", type=float, required=True, help="整支舰队目标点数")
    ap.add_argument("--name", default="demo fleet")
    ap.add_argument("--faction", default="Stock/Shelter Alliance")
    ap.add_argument("--sections", default="", help="模块化舰体的三段，如 A,B,B")
    ap.add_argument("--out", required=True)
    ap.add_argument("--must", default="", help="固定装件，如 MT1=Mk68 Cannon,MT2=Mk66 Cannon")
    args = ap.parse_args(argv)

    import hulls as hu

    sections = tuple(args.sections.split(",")) if args.sections else None
    wiki_hull = hu.resolve(args.hull) or args.hull
    sockets = bf.sockets_for(wiki_hull, sections)
    pool = candidates()
    target = args.total / max(1, args.count)
    hull_cost = bf.part(wiki_hull)['cost'] if bf.part(wiki_hull) else 0
    seed = {}
    for pair in [x for x in args.must.split(',') if '=' in x]:
        label, name = pair.split('=', 1)
        if bf.part(name):
            seed[label.strip()] = name.strip()
    chosen = pick(pool, sockets, target, hull_cost, seed) or {}
    fills = dict(sorted(chosen.items()))
    spec = {
        "hull": args.hull,
        "wiki_hull": wiki_hull,
        "name": args.name,
        "count": args.count,
        "faction": args.faction,
        "sections": sections,
        "fills": fills,
        "out": args.out,
    }
    path = bf.build(spec)
    hull_cost = bf.part(wiki_hull)["cost"] if bf.part(wiki_hull) else 0
    per = float(hull_cost) + sum(bf.part(n)["cost"] for n in chosen.values() if bf.part(n))
    print(f"per ship {per:g} pts, total {per * args.count:g} / target {args.total:g}")
    print(f"fills: {len(fills)}")
    print(f"wrote {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))

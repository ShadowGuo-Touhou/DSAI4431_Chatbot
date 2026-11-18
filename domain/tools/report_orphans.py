"""List every ship that has no class in Ship Builds.txt.

"no class" here means: the ship did not satisfy any class's *must* lines within
its price band **and** the `A Cap (Any ship)` fallback had to be applied (or the
fallback did not apply because the ship carries no weapon at all).  For each such
ship the report shows the closest classes and the exact must lines it fails, so
the gaps can be closed by editing `Ship Builds.txt` rather than by guessing.

    python domain/tools/report_orphans.py
"""

from __future__ import annotations

import json
import pathlib
from collections import Counter

ROOT = pathlib.Path(__file__).resolve().parents[2]
DATA = ROOT / "domain" / "data" / "ship_classification.json"
OUT = ROOT / "domain" / "reports" / "no-class-orphans.md"


def load() -> list[dict]:
    d = json.loads(DATA.read_text(encoding="utf-8"))
    return d["rows"]


def is_orphan(row: dict) -> bool:
    if row["verdict"] == "no_class":
        return True
    return str(row["class"]).startswith("A Cap (Any ship)")


def explain(row: dict) -> str:
    near = row.get("near") or []
    if not near:
        return "没有可比舰级"
    parts = []
    for n in near[:2]:
        band = f"{n['cost'][0]:g}-{n['cost'][1]:g}"
        head = f"`{n['class']}`（{band}）"
        if not n["fails"]:
            body = "must 全过，但点数不在区间" if not n["in_band"] else "must 全过"
        else:
            body = "差 " + "；".join(f"「{f}」" for f in n["fails"])
            if n["unknown"]:
                body += f"（另有 {n['unknown']} 条无法判定）"
            if not n["in_band"]:
                body += f"，且点数 {row['cost']:g} 在区间外"
        parts.append(f"{head} {body}")
    return "<br>".join(parts)


def main() -> int:
    rows = load()
    orphans = [r for r in rows if is_orphan(r)]
    by_hull = Counter(r["hull_abbr"] for r in orphans)
    by_fleet = Counter(r["fleet"] for r in orphans)

    lines = [
        "# 没有舰级的船（`A Cap (Any ship)` 之前）",
        "",
        f"语料：{len(rows)} 舰（106 舰队，87 舰因已删除部件跳过）。",
        f"**没有对应舰级：{len(orphans)} 舰** —— 它们在 `Ship Builds.txt` 里不满足任何一类的 must"
        "（含点数区间），只能落进 `A Cap (Any ship)` 这条兜底。",
        "",
        "按舰体：" + "、".join(f"{k} {v}" for k, v in by_hull.most_common()),
        "",
        "按来源舰队：" + "、".join(f"{k} {v}" for k, v in by_fleet.most_common()),
        "",
        "| # | 船名 | 舰体 | 点数 | 舰队 | 最接近的舰级与差距 |",
        "|---|---|---|---|---|---|",
    ]
    for i, r in enumerate(sorted(orphans, key=lambda x: (x["hull_abbr"], x["cost"] or 0)), 1):
        lines.append(
            f"| {i} | {r['ship']} | {r['hull_abbr']} | {r['cost']:g} | {r['fleet']} | {explain(r)} |"
        )

    lines += [
        "",
        "## 怎么读",
        "",
        "- 「差「…」」= 该舰级 must 里被判定为**不满足**的条目，原样引用 `Ship Builds.txt`。",
        "- 「点数在区间外」= must 都过了，只是点数不在这一类标称的区间内。",
        "- 「无法判定」= 条件依赖 .fleet 里没有的信息（例如火炮朝向、某种弹药数量），脚本不下结论。",
        "",
    ]
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text("\n".join(lines), encoding="utf-8")
    print(f"orphans {len(orphans)} / rows {len(rows)} -> {OUT}")
    print("by hull:", dict(by_hull))
    for r in orphans[:12]:
        print(f"  {r['ship'][:30]:<30} {r['hull_abbr']:<3} {r['cost']:>6g}  {explain(r)[:110]}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

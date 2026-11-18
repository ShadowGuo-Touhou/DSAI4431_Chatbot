"""Turn the matched ships of each build class into a reusable template doc.

Input : domain/data/ship_classification.json  (only `match` rows are used)
        the fleets themselves (re-parsed for the component list)
        the Chinese pack readmes (`使用说明*.txt`, `ReadMe.txt`)
Output: domain/data/class_templates.json
        domain/reports/class-templates.md
        domain/kb/builds/<slug>.md           (with --write-kb; copied into the KB
                                              by build_official.py like the zh guides)

Priority for the "sample ships" list: the Chinese starter pack (which ships with
readmes) > the rest of `other info` > the player's own saved fleets.
"""

from __future__ import annotations

import argparse
import json
import re
import statistics
import sys
from collections import Counter, defaultdict
from pathlib import Path

TOOLS = Path(__file__).resolve().parent
sys.path.insert(0, str(TOOLS))

import fleet_lib as fl  # noqa: E402
import build_classes as bc  # noqa: E402
import hulls as hu  # noqa: E402
import sample_ship  # noqa: E402

ROOT = TOOLS.parent.parent
CLS_JSON = ROOT / "domain" / "data" / "ship_classification.json"
SPEC = ROOT / "domain" / "spec" / "ship_builds.json"
OUT_JSON = ROOT / "domain" / "data" / "class_templates.json"
OUT_MD = ROOT / "domain" / "reports" / "class-templates.md"
KB_DIR = ROOT / "domain" / "kb" / "builds"

CN_PACK = "群新手舰队包"
README_PATTERNS = ("使用说明*.txt", "ReadMe.txt", "本新手包对应游戏版本.txt")

# components that are pure filler for a template (they are on every hull)
NOISE = {"berthing"}


def source_rank(path: Path) -> int:
    p = str(path)
    if CN_PACK in p:
        return 0
    if "other info" in p:
        return 1
    return 2


def readme_for(path: Path) -> str:
    """Return the most specific readme block for a fleet file."""
    folder = path.parent
    for pattern in ("使用说明*.txt", "S2 DIR OCELLO.txt"):
        for f in sorted(folder.glob(pattern)):
            try:
                return f.read_text(encoding="utf-8", errors="ignore").strip()
            except OSError:
                continue
    return ""


def class_slug(name: str) -> str:
    s = name.lower()
    s = s.replace("(", "").replace(")", "").replace("/", "-").replace(" ", "-")
    s = re.sub(r"[^a-z0-9\-\u4e00-\u9fff]+", "", s)
    return re.sub(r"-{2,}", "-", s).strip("-")


def load_spec() -> dict:
    spec = json.loads(SPEC.read_text(encoding="utf-8"))
    return {c["name"]: c for c in spec["classes"]}


def component_name(sock, idx, aliases) -> str:
    name = fl.save_key_name(sock.component_name)
    alias = aliases.get(fl.norm(name))
    comp = idx.component(alias or name)
    return comp.name if comp else name


def is_good(quality: dict | None) -> bool:
    """模板只收「good」样本：must 全过、should 全过、价格在区间内（Cost 也是 should）。"""
    if not quality:
        return False
    if quality.get("fails"):
        return False
    if quality.get("should_fails"):
        return False
    if not quality.get("cost_ok", True):
        return False
    total = quality.get("should_total") or 0
    known = quality.get("should_known") or 0
    return total == 0 or known / total >= 0.75


def collect() -> dict:
    rows = json.loads(CLS_JSON.read_text(encoding="utf-8"))["rows"]
    idx = fl.WikiIndex()
    aliases = dict(bc.ALIASES_NORM)
    groups: dict[str, list[dict]] = defaultdict(list)
    for row in rows:
        # (bad) classes only ever land on `bad_class` rows, and they still need a
        # detection-only page ("this is what a 250 CC looks like — do not build it").
        if row["verdict"] not in ("match", "bad_class"):
            continue
        classes = row.get("classes") or [row["class"]]
        quality = row.get("class_quality") or {}
        path = Path(row["fleet_path"])
        try:
            fleet = fl.parse_fleet(str(path))
        except Exception:  # noqa: BLE001
            continue
        ship = next((s for s in fleet.ships if s.name == row["ship"]), None)
        if ship is None:
            continue
        comps = Counter()
        for sock in ship.sockets:
            name = component_name(sock, idx, aliases)
            if fl.norm(name) in NOISE:
                continue
            comps[name] += 1
        rec = {
            "ship": row["ship"],
            "hull": row["hull"],
            "hull_abbr": row["hull_abbr"],
            "cost": row["cost"],
            "draw_kw": row["draw_kw"],
            "supply_kw": row["supply_kw"],
            "missile_pts": row["missile_pts"],
            "fleet": row["fleet"],
            "path": str(path),
            "rank": source_rank(path),
            "readme": readme_for(path),
            "components": dict(comps),
            "calibers": row.get("calibers") or {},
            "launchers": row.get("launchers") or {},
            "good": is_good(quality.get(classes[0])) if len(classes) == 1 else None,
        }
        for cls in classes:
            q = quality.get(cls) or {}
            groups[cls].append(dict(rec, good=is_good(q),
                                    fails=q.get("should_fails") or [],
                                    must_fails=q.get("fails") or []))
    return groups


def summary_block(cls_name: str, spec: dict, ships: list[dict]) -> dict:
    cls = spec.get(cls_name, {})
    good = [s for s in ships if s.get("good")]
    pool = good or []          # 部件统计只来自 good 样本
    comp_counts = Counter()
    hist = Counter()
    for s in pool:
        hist.update({s["hull"]: 1})
        for name, n in s["components"].items():
            comp_counts[name] += 1
    n = len(pool)
    core = sorted([c for c, k in comp_counts.items() if n and k / n >= 0.7])
    common = sorted([c for c, k in comp_counts.items() if n and 0.4 <= k / n < 0.7])
    optional = sorted([c for c, k in comp_counts.items() if n and k / n < 0.4],
                      key=lambda c: (-comp_counts[c], c))[:12]
    costs = sorted(s["cost"] for s in pool) or sorted(s["cost"] for s in ships) or [0.0]
    best = sorted(pool, key=lambda s: (s["rank"], s["cost"]))[:6]
    closest = sorted(ships, key=lambda s: (len(s.get("must_fails") or []) + len(s.get("fails") or []),
                                           s["cost"]))[:4]
    return {
        "class": cls_name,
        "rec": bool(cls.get("recommend", True)),
        "cost_range": cls.get("cost", [0, 0]),
        "ships": len(ships),
        "good_ships": n,
        "requirements": {
            "must": cls.get("must", []),
            "should": cls.get("should", []),
            "optional": cls.get("optional", []),
            "avoid": cls.get("avoid", []),
        },
        "hulls": hist.most_common(),
        "cost_min": costs[0],
        "cost_median": statistics.median(costs),
        "cost_max": costs[-1],
        "draw_median": statistics.median([s["draw_kw"] for s in pool] or [0]),
        "supply_median": statistics.median([s["supply_kw"] for s in pool] or [0]),
        "core": [(c, comp_counts[c]) for c in core],
        "common": [(c, comp_counts[c]) for c in common],
        "optional": [(c, comp_counts[c]) for c in optional],
        "armament": armament_block(pool),
        "samples": best,
        "closest": [
            {"ship": s["ship"], "fleet": s["fleet"], "cost": s["cost"],
             "must_fails": s.get("must_fails") or [], "fails": s.get("fails") or []}
            for s in closest
        ],
    }


def armament_block(ships: list[dict]) -> list[tuple[str, int, float, int, int]]:
    """按口径 / 发射器聚合：[(label, ships_with_it, median, min, max)]。"""
    out: list[tuple[str, int, float, int, int]] = []
    cals: dict[str, list[int]] = {}
    lnch: dict[str, int] = {}
    for s in ships:
        for cal, n in (s.get("calibers") or {}).items():
            cals.setdefault(cal, []).append(int(n))
        for model, n in (s.get("launchers") or {}).items():
            lnch[model] = lnch.get(model, 0) + 1
    for cal in sorted(cals, key=lambda c: -sum(cals[c])):
        vals = cals[cal]
        out.append((f"{cal} mm turret/cannon", len(vals) + 0, statistics.median(vals), min(vals), max(vals)))
    for model, k in sorted(lnch.items(), key=lambda kv: -kv[1]):
        out.append((f"{model} launcher", k, 0, 0, 0))
    return out


def render_requirements(req: dict, *, prefix: str = "") -> list[str]:
    out = ["## 舰级要求（Ship Builds.txt 原文，作为判定依据）", ""]
    for label, key in (("舰级硬性要求（required：缺一条就不算这个舰级）", "must"),
                       ("良好标准（should：缺了算有瑕疵，但仍算这个舰级）", "should"),
                       ("可选加分（optional）", "optional"),
                       ("避免（avoid）", "avoid")):
        items = req.get(key) or []
        if not items:
            continue
        out.append(f"**{label}**")
        out += [f"- {x}" for x in items]
        out.append("")
    if not any(req.get(k) for k in ("must", "should", "optional", "avoid")):
        out.append("（该舰级在 Ship Builds.txt 里没有列出条件）")
        out.append("")
    return out


def render_md(blocks: list[dict]) -> str:
    lines = ["# 舰级模板（模板只由「good」样本归纳，要求引自 Ship Builds.txt）", ""]
    lines.append("**判定来源分两层**："
                 "① 舰级定义（Must / Should / Optional / Avoid）来自 `other info/Ship Builds.txt`，"
                 "回答「这艘船算不算这个舰级 / 合不合格」以它为准；"
                 "② 下面的部件清单只统计 **good 样本**（must 全过 + should 全过，可选项不影响），"
                 "`核心` = ≥70% 的 good 样本装、`常见` = 40–70%、`可选` = <40%。")
    lines.append("样本优先取自带说明的中文新手包（`群新手舰队包 v1.12`），其次是其它示例舰队、最后是玩家自己的存档。")
    lines.append("**参考配置，不是最优解**：频率只表示常见程度；旧版本可能改过数值或名字，模组部件不代表原版可用。")
    lines.append("")
    lines.append("| 舰级 | 造价区间 | 匹配数 | good 数 | 造价中位 | 主流舰体 | 核心部件数 |")
    lines.append("|---|---|---:|---:|---:|---|---:|")
    for b in sorted(blocks, key=lambda x: (x["cost_range"][0], x["class"])):
        hulls = "、".join(f"{h}×{k}" for h, k in b["hulls"][:2])
        mark = "" if b.get("rec", True) else "（仅检测）"
        lines.append(f"| {b['class']}{mark} | {b['cost_range'][0]}–{b['cost_range'][1]} | {b['ships']} | "
                     f"{b['good_ships']} | {b['cost_median']:.0f} | {hulls} | {len(b['core'])} |")
    lines.append("")
    for b in sorted(blocks, key=lambda x: (x["cost_range"][0], x["class"])):
        lines.append(f"## {b['class']}（匹配 {b['ships']} 艘，其中 good {b['good_ships']} 艘）")
        lines.append("")
        lines += render_requirements(b["requirements"])
        if not b.get("rec", True):
            lines.append("**仅用于检测**：这一类（Bad 类或无武装舰）不推荐建造，回答时只按上面的硬性要求识别，"
                         "不要给配置建议。")
            lines.append("")
            continue
        if not b["good_ships"]:
            lines.append("**没有 good 样本**：这一类目前只能按 Ship Builds.txt 的要求回答，给不出实战示例。")
            lines.append("")
            continue
        lines.append(f"- 造价区间：`{b['cost_range'][0]}–{b['cost_range'][1]}`；good 样本 {b['cost_min']:.0f}–{b['cost_max']:.0f}")
        lines.append(f"- 舰体：{'、'.join(f'{h}×{k}' for h, k in b['hulls'])}")
        lines.append(f"- 功率中位：耗 {b['draw_median']:.0f} / 供 {b['supply_median']:.0f} kW")
        if b.get("armament"):
            arms = []
            for label, k, med, lo_n, hi_n in b["armament"]:
                arms.append(f"{label} {med:g}门（{k}/{b['good_ships']} 艘）" if med
                            else f"{label}（{k}/{b['good_ships']} 艘）")
            lines.append(f"- 火力：{'、'.join(arms)}")
        lines.append("")
        lines.append("| 组成部分 | 部件 | 装舰数 |")
        lines.append("|---|---|---:|")
        for label, items in (("核心", b["core"]), ("常见", b["common"]), ("可选", b["optional"])):
            for name, k in items:
                lines.append(f"| {label} | {name} | {k}/{b['good_ships']} |")
        lines.append("")
        if b["samples"]:
            lines.append("| good 样本 | 舰队 | 造价 | 来源 |")
            lines.append("|---|---|---:|---|")
            for s in b["samples"]:
                tag = "中文新手包" if s["rank"] == 0 else ("示例舰队" if s["rank"] == 1 else "玩家存档")
                lines.append(f"| {s['ship']} | {s['fleet']} | {s['cost']:.0f} | {tag} |")
            lines.append("")
    return "\n".join(lines)


def render_sample_page(b: dict, body: str, n: int) -> str:
    """把一段样板船装配包装成独立页面。"""
    cls = b["class"]
    head = body.splitlines()[0].split("：", 1)[-1].strip() if body else cls
    hull = b["hulls"][0][0] if b.get("hulls") else ""
    return "\n".join(
        [
            f"# {cls} 样板船完整装配 {n}：{head}",
            "",
            f"Tags: kind=class assembly; class={cls}; lang=zh",
            f"Keywords: {cls}, 样板船, 完整装配, 整艘照抄, 逐槽, 槽位, 点数, 供电, 弹库, 造舰, 配船, loadout",
            f"Summary: {cls} 的一艘 good 样本船的逐槽完整装配（舰体 {hull}）：照抄这张表就能配出同型船，"
            "点数、供电余量、弹库装载都按存档实测列出。",
            "Section: build templates; per-slot assembly of one real good sample ship",
            "",
            body,
        ]
    ) + "\n"


def render_kb(b: dict) -> str:
    lo, hi = b["cost_range"]
    hulls = "、".join(f"{h}×{k}" for h, k in b["hulls"]) or "—"
    n = b["good_ships"]
    lines = [
        f"# {b['class']}",
        "",
        f"Tags: kind=build template; class={b['class']}; cost={lo}-{hi}; samples={b['ships']}; good={n}",
        "Keywords: build, loadout, template, 配装, 配置, 装配, 模板, 舰级, " + b['class'],
        f"Summary: {b['class']} build; {b['ships']} matched ships, {n} of them are good samples (must and should both pass); "
        f"typical cost {b['cost_median']:.0f} (range {b['cost_min']:.0f}-{b['cost_max']:.0f}); hull {hulls}.",
        "Section: build templates; requirements from other info/Ship Builds.txt; samples from player fleets",
        "",
        "## How to read this",
        "回答「这艘船算不算 / 合不合格」以 Requirements 段为准（must 全过才算这个舰级，should 是良好标准）；"
        "部件清单只统计 good 样本，频率 (k/N) 表示常见程度，不是硬性要求。"
        "所有舰船先要过通用基线（`reference/baseline-requirements.md`），再看本舰级要求。",
        "",
    ]
    lines += render_requirements(b["requirements"])
    if not b.get("rec", True):
        lines += [
            "## Detection only — do not recommend",
            "This class exists for **classification only**. Never propose it as a build to copy: "
            "the ship would be a worse choice than any recommended class at the same price. "
            "Use it only to recognise what an existing ship is.",
            "",
            f"Detection rule: {b['class']} = a ship that matches the hard requirements above. "
            "If the question asks how to identify such a ship, answer with those requirements and stop there.",
            "",
            f"- Matched ships in the corpus: {b['ships']}",
            f"- Price range from the spec: {lo}-{hi}",
            "",
        ]
        return "\n".join(lines) + "\n"
    lines += [
        "## Disclaimer",
        "参考配置，不是最优解。样本是玩家舰队里 must + should 全过的真实配装"
        "（主要取自中文新手包 v1.12，对应游戏 0.6.2.3；其余来自 other info 与本地存档）。"
        "旧版本可能改过数值或改过名字；模组部件不代表原版能照抄。把它当起步模板，不要当配方。",
        "",
        "## Numbers",
        f"- Point cost: {lo}-{hi} (good-sample median {b['cost_median']:.0f}, "
        f"range {b['cost_min']:.0f}-{b['cost_max']:.0f})",
    ]
    if n:
        lines.append(f"- Power: draw {b['draw_median']:.0f} kW / supply {b['supply_median']:.0f} kW (median)")
    lines += [
        f"- Hull: {hulls}",
        "",
    ]
    if not n:
        lines += [
            "## No good sample",
            "语料里没有同时满足 must 与 should 的样本，因此**没有部件清单可用**。"
            "按本类的 Requirements 要求逐条回答（must 是硬性、should 是良好标准），"
            "具体部件用单件资料（component/*.md、catalog/*）确认点数与尺寸，**不要编造一份「标准配置」**。",
            "",
            "## Closest samples (not good)",
            "最接近的样本及它没满足的条件（只作参考，不要照抄）：",
            "",
        ]
        for s in b.get("closest", []):
            miss = (s["must_fails"] or []) + (s["fails"] or [])
            lines.append(f"- {s['ship']} ({s['fleet']}, {s['cost']:.0f} pts) — "
                         f"未满足：{'；'.join(miss) if miss else '（无记录）'}")
        lines.append("")
        return "\n".join(lines) + "\n"
    lines += ["## Armament (good samples)"]
    if b.get("armament"):
        for label, k, med, lo_n, hi_n in b["armament"]:
            if med:
                lines.append(f"- {label}: {k}/{n} ships, median {med:g} (min {lo_n}, max {hi_n})")
            else:
                lines.append(f"- {label}: {k}/{n} ships")
    else:
        lines.append("- (no gun or launcher data)")
    lines += [
        "",
        "## Core parts (fitted on most good samples)",
    ]
    lines += [f"- {name} ({k}/{n})" for name, k in b["core"]] or ["- (no part reaches 70%)"]
    lines += ["", "## Common parts (40-70%)"]
    lines += [f"- {name} ({k}/{n})" for name, k in b["common"]] or ["- -"]
    lines += ["", "## Optional parts"]
    lines += [f"- {name} ({k}/{n})" for name, k in b["optional"]] or ["- -"]
    if b["samples"]:
        lines += ["", "## Sample ships (good)"]
        for s in b["samples"]:
            tag = "Chinese starter pack" if s["rank"] == 0 else ("example fleet" if s["rank"] == 1 else "player save")
            lines.append(f"- {s['ship']} ({s['fleet']}, {s['cost']:.0f} pts, {tag})")
    for block in b.get("assembly") or []:
        lines += ["", block]
    notes = []
    seen = set()
    for s in b["samples"]:
        text = (s.get("readme") or "").strip()
        if not text or text in seen:
            continue
        seen.add(text)
        notes.append((s["fleet"], " / ".join(x.strip() for x in text.splitlines() if x.strip())))
        if len(notes) >= 3:
            break
    if notes:
        lines += ["", "## Author notes (from the fleet's 使用说明.txt)"]
        for fleet, text in notes:
            excerpt = text[:700] + ("…" if len(text) > 700 else "")
            lines.append(f"- {fleet}: {excerpt}")
    return "\n".join(lines) + "\n"


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--write-kb", action="store_true")
    ap.add_argument("--min-samples", type=int, default=1)
    args = ap.parse_args()

    spec = load_spec()
    groups = collect()
    blocks = []
    for cls_name, ships in groups.items():
        if len(ships) < args.min_samples:
            continue
        blocks.append(summary_block(cls_name, spec, ships))    # every non-recommended class gets a page even when no fleet in the corpus uses it:
    # the bot needs to be able to say "that is a <bad class>, do not build it".
    for cls_name, cls in spec.items():
        if cls.get("recommend", True) or any(b["class"] == cls_name for b in blocks):
            continue
        blocks.append(summary_block(cls_name, spec, groups.get(cls_name, [])))

    # 每个可推荐舰级挑 1–2 艘 good 样本，把它们的**完整装配**（槽位→部件→点数→供电）
    # 直接渲染进页面：模型照着「整艘复制」时，一次检索就能拿到成品，
    # 不必再查一遍槽位表和每个部件的尺寸、点数。
    idx = fl.WikiIndex()
    cache: dict[str, fl.Fleet] = {}
    for b in blocks:
        if not b.get("rec", True) or not b.get("samples"):
            continue
        median = b.get("cost_median") or 0.0
        picks = sorted(b["samples"], key=lambda s: (s["rank"], abs(s["cost"] - median)))[:2]
        rendered = []
        for s in picks:
            try:
                fleet = cache.get(s["path"])
                if fleet is None:
                    fleet = fl.parse_fleet(s["path"])
                    cache[s["path"]] = fleet
                text = sample_ship.render(s["path"], s["ship"], idx=idx, fleet=fleet)
            except Exception:  # noqa: BLE001 - 单条样本坏了不该拖垮整次生成
                text = ""
            if text:
                rendered.append(text)
        b["assembly"] = rendered

    OUT_JSON.write_text(json.dumps({"classes": blocks}, ensure_ascii=False, indent=1), encoding="utf-8")
    OUT_MD.write_text(render_md(blocks), encoding="utf-8")
    # `ships` is summed over classes on purpose: a ship that matches two classes is a
    # sample of both, so the sum is memberships, not vessels. Report both numbers so
    # nobody mistakes 927 for the size of the corpus. The vessel count comes from the
    # classifier output (one row per ship), because player-named ships repeat inside a
    # fleet and cannot be counted by name.
    memberships = sum(b["ships"] for b in blocks)
    try:
        vessels = len(json.loads(CLS_JSON.read_text(encoding="utf-8"))["rows"])
    except (OSError, ValueError, KeyError):
        vessels = 0
    print(f"classes={len(blocks)} memberships={memberships} vessels={vessels}")

    if args.write_kb:
        KB_DIR.mkdir(parents=True, exist_ok=True)
        for old in KB_DIR.glob("*.md"):
            old.unlink()
        for b in blocks:
            # one-off ships do not make a template, but a detection-only page is
            # still worth having even with zero samples.
            if b["ships"] < 2 and b.get("rec", True):
                continue
            path = KB_DIR / f"{class_slug(b['class'])}.md"
            path.write_text(render_kb(b), encoding="utf-8")
            # 每艘样板船单独成页：类页里它排在频率表后面，长表格块的相似度拼不过
            # 统计块，模型常常只读到频率表就说「没有逐槽清单」。独立页的标题和
            # Summary 都带「样板船完整装配」，一问造舰就能直接命中。
            for n, text in enumerate(b.get("assembly") or [], start=1):
                slug = class_slug(b["class"])
                (KB_DIR / f"{slug}-sample-{n}.md").write_text(
                    render_sample_page(b, text, n), encoding="utf-8"
                )
        print("wrote", len(list(KB_DIR.glob('*.md'))), "kb docs ->", KB_DIR)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

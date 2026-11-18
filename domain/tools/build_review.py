"""Compose the review document for the build-class library.

Reads domain/data/build_classes.json plus each guide fleet's 使用说明.txt and
writes domain/reports/build-library-review.md.  Nothing is published to the RAG
pool here -- the user reviews the document first.
"""

from __future__ import annotations

import json
import re
import statistics
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "domain" / "data" / "build_classes.json"
OUT = ROOT / "domain" / "reports" / "build-library-review.md"

POSITION = re.compile(r"^\s*\*?\s*舰队定位\s*[:：]\s*(?P<role>.+)$")
DIFFICULTY = re.compile(r"^\s*\*?\s*上手难度\s*[:：]\s*(?P<diff>.+)$")


def read_meat(path: Path) -> dict[str, str]:
    """Pull 定位 / 难度 out of a guide fleet's readme."""
    out: dict[str, str] = {}
    for name in ("使用说明.txt", "readme.txt", "ReadMe.txt", "README.md"):
        f = path / name
        if not f.exists():
            continue
        try:
            text = f.read_text(encoding="utf-8", errors="replace")
        except OSError:
            continue
        lines = [ln.strip() for ln in text.splitlines() if ln.strip()]
        for i, line in enumerate(lines):
            m = POSITION.match(line)
            if m and "role" not in out:
                role = m.group("role").strip()
                if not role and i + 1 < len(lines):
                    role = lines[i + 1]
                role = role.replace("*", "").strip()
                role = re.split(r"[。；;]", role)[0][:40]
                out["role"] = role
            m = DIFFICULTY.match(line)
            if m and "difficulty" not in out:
                out["difficulty"] = re.split(r"[。；;]", m.group("diff"))[0].strip()[:20]
        break
    return out


def fleet_roles() -> dict[str, dict[str, str]]:
    fleet_paths = {s["fleet_path"] for s in json.loads(DATA.read_text(encoding="utf-8"))["ships"]}
    roles: dict[str, dict[str, str]] = {}
    for raw in fleet_paths:
        p = Path(raw)
        roles[p.stem] = read_meat(p.parent)
    return roles


def main() -> int:
    data = json.loads(DATA.read_text(encoding="utf-8"))
    ships = data["ships"]
    roles = fleet_roles()

    by_class: dict[str, list[dict]] = defaultdict(list)
    for s in ships:
        by_class[s["label"]].append(s)

    lines: list[str] = []
    lines.append("# 构建类型库（草案，未入库）")
    lines.append("")
    lines.append(
        f"样本：{len({s['fleet_path'] for s in ships})} 个舰队 / {len(ships)} 艘船 "
        f"（`other info\\fleets` 新手包 + Steam `Saves\\Fleets`）。"
    )
    lines.append("")
    lines.append("> 这份文件只是给你看的草案。**还没有写进 RAG**，等你确认命名和规则之后再入库。")
    lines.append("")

    lines.append("## 1. 识别规则")
    lines.append("")
    lines.append("**类名 = 主武器 + 舰级缩写**，例：`450 CH`、`VLS-2 FFL`、`unarmed CC`（对应你说的 “450 CH”“cap”）。")
    lines.append("")
    lines.append("| 规则 | 取值 |")
    lines.append("|---|---|")
    lines.append("| 火炮主武器 | 口径 450 / 250 / 120 / 100 / 75 / 50 / 30 / 20（按 wiki `Mounts › Projectile weapons` 口径） |")
    lines.append("| 导弹主武器 | 发射器型号：VLS-1-23 / VLS-1-46 / VLS-2 / VLS-3 / MLS-2 / MLS-3 / CLS-3 / SALS-2 / ML-9 … |")
    lines.append("| 纯近防 | `P20 'Bastion' PDT`、`P11 'Pavise' PDT` 这类直接写型号 |")
    lines.append("| 无武器 | `unarmed` |")
    lines.append("| 舰级 | hull_abbr.json（CC/DD/FF/FFL/CH/CL/CVL/CVE/BB/LN/MN…） |")
    lines.append(
        "| 标签 | `line`（有 450mm 舰炮）、`cap`（FFL、≤320 点、无 250mm 以上主炮）、"
        "`scout`、`softkill`、`air-defence`、`carrier`、`support`、`picket` |"
    )
    lines.append("")

    stats = []
    for label, group in sorted(by_class.items(), key=lambda kv: -len(kv[1])):
        costs = sorted(s["declared"] for s in group)
        hulls = sorted((s["hull_cost"] or 0) for s in group)
        mid = statistics.median(costs)
        hull_mid = statistics.median(hulls)
        hulls_counter = Counter(s["hull_abbr"] or s["hull"] for s in group)
        stats.append((label, len(group), costs[0], mid, costs[-1], hull_mid, hull_mid / mid if mid else 0, group, hulls_counter))

    lines.append(f"## 2. 构建类型汇总（共 {len(by_class)} 类）")
    lines.append("")
    lines.append("| 构建 | 船数 | 舰体 | 实际点数 min / 中位 / max | 舰体点数 | 舰体占比 | 标签 |")
    lines.append("|---|---|---|---|---|---|---|")
    for label, n, lo, mid, hi, hull_mid, share, group, hulls_counter in stats:
        tags = Counter(t for s in group for t in s["tags"])
        tag_text = "、".join(t for t, _ in tags.most_common(4)) or "-"
        lines.append(
            f"| {label} | {n} | {'、'.join(f'{k}×{v}' for k, v in hulls_counter.most_common(3))} "
            f"| {lo:.0f} / {mid:.0f} / {hi:.0f} | {hull_mid:.0f} | {share:.0%} | {tag_text} |"
        )
    lines.append("")

    lines.append("## 3. 有说明书的舰队：定位 vs 实际构建")
    lines.append("")
    lines.append("只列 使用说明.txt 的舰队（其余是没有说明的测试/存档舰队）。")
    lines.append("")
    lines.append("| 舰队 | 说明里的定位 | 上手难度 | 构成 |")
    lines.append("|---|---|---|---|")
    for fleet, meta in sorted(roles.items(), key=lambda kv: kv[0].lower()):
        group = [s for s in ships if Path(s["fleet_path"]).stem == fleet]
        if not group or ("role" not in meta and "difficulty" not in meta):
            continue
        classes = Counter(s["label"] for s in group)
        comp = "、".join(f"{k}×{v}" for k, v in classes.most_common(6))
        lines.append(
            f"| {fleet} | {meta.get('role', '-')} | {meta.get('difficulty', '-')} | {comp} |"
        )
    lines.append("")

    lines.append("## 4. 成本模型")
    lines.append("")
    exact = sum(1 for s in ships if abs(s["predicted"] - s["declared"]) < 1)
    diffs = [abs(s["predicted"] - s["declared"]) for s in ships]
    under = sum(1 for s in ships if s["predicted"] < s["declared"] - 1)
    over = sum(1 for s in ships if s["predicted"] > s["declared"] + 1)
    lines.append(
        f"- 逐船预测 = 舰体 + 部件 + 弹药（wiki 单价）：**精确命中 {exact}/{len(ships)}**，"
        f"中位偏差 {statistics.median(diffs):.0f} 点；偏低 {under} 条、偏高 {over} 条。"
    )
    lines.append("- 偏低主因：(a) 游戏内部件单价略高于 wiki 数值，(b) `$MODMIS$` 自制导弹没有模板价格，(c) 自带部件与舱内弹药未计价。")
    lines.append("- 民用船体（Shuttle / Bulk Hauler / Tugboat / Container Hauler / Ore Carrier）wiki 里没有点数列，")
    lines.append("  现在用 `domain\\data\\civilian_hull_prices.json` 的**反推估算值**补上（中位 `declared − 部件 − 弹药`）。")
    lines.append("- 因此类目表里的“实际点数”以舰队文件里的 `Cost` 为准，预测值只当诊断用。")
    lines.append("")

    lines.append("## 5. 已知问题")
    lines.append("")
    unknown = Counter()
    for s in ships:
        for u in s.get("unknown", []):
            unknown[u] += 1
    lines.append("1. 匹配不到的部件：" + "、".join(f"{k}×{v}" for k, v in unknown.most_common()) + "。")
    lines.append("2. 民用舰体价格是估算，不是官方数值。")
    lines.append("3. wiki 的炮弹价是 `1 / N 点`，会出现 25.75 这种小数，游戏里取整规则未验证。")
    lines.append("4. 插件（mod）船没有单独统计；`other info` 里与 Steam 重复的舰队只算一次（按路径去重）。")
    lines.append("")

    lines.append("## 6. 需要你拍板")
    lines.append("")
    lines.append("1. 类名是否就用「主武器 + 舰级」这套（`450 CH` / `VLS-2 FFL` / `unarmed cap`）？要不要把 `cap` 直接写成类名？")
    lines.append("2. 新手包的 28 个舰队要不要留在样本里（它们偏教学，不一定是最优解）？")
    lines.append("3. 标签够不够用？现在会自动打 `line`（450mm）/ `cap` / `scout` / `softkill` / `air-defence` / `carrier` / `support` / `picket`，")
    lines.append("   要不要再加 `logi`（补给）、`sniper`（远程导弹）、`brawler`（近战）这种？")
    lines.append("4. 说明里的“舰队定位”我要不要一起解析成结构化字段（前排 / 中远程 / 软杀 / 眼船…）？")
    lines.append("")

    sample_label = "450 CC"
    sample = [s for s in ships if s["label"] == sample_label]
    if sample:
        costs = sorted(s["declared"] for s in sample)
        lines.append(f"## 7. 如果入库，长这样（以 `{sample_label}` 为例）")
        lines.append("")
        lines.append("```markdown")
        lines.append(f"# {sample_label}（450mm 舰炮 / 指挥巡洋舰）")
        lines.append("Tags: kind=build class; role=line; hull=CC")
        lines.append(
            f"Summary: 主武器 {sample[0]['main'].split('（')[0] or '—'}；"
            f"样本 {len(sample)} 艘；实际点数 {costs[0]:.0f}–{costs[-1]:.0f}（中位 {statistics.median(costs):.0f}）"
        )
        lines.append("## 样本")
        lines.append("| 舰队 | 舰名 | 点数 |")
        lines.append("|---|---|---|")
        for s in sample[:3]:
            lines.append(f"| {s['fleet']} | {s['ship_name']} | {s['declared']:.0f} |")
        lines.append("## 用法")
        lines.append("- 评舰队时：一艘 450 CC 通常吃掉 1300–1650 点预算，占比 4 成是舰体本身。")
        lines.append("- 和 450 CH 的区别：CH 是 Axford 重型巡洋舰（600 点舰体、成品中位 1534），CC 是 Ocello（575 点舰体、1500），槽位更多但点数接近。")
        lines.append("```")
        lines.append("")

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"wrote {OUT} ({len(lines)} lines)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

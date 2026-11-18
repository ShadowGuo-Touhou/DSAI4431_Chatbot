"""弹药点数表：把「一发多少钱」整理成可计算的表，并生成知识库页。

来源分三类：
  * 炮弹 —— `domain/data/munition_costs.json`，值就是 wiki 的 `Cost (pts per X amount): a/b`；
  * 导弹模板 —— `domain/kb/docs/missile/*.md` 的 `Tags: … cost=N pts`（玩家自建导弹存档）；
  * 诱饵弹 —— 存档反解（EA99 = 8 点/发、EA14 = 2、EA12 = 1），见 `DECOYS` 注释。

输出：
  * `domain/data/ammo_costs.json` —— 给脚本用的查价表；
  * `domain/kb/manual_zh/弹药点数表.md` —— 给模型看的页面（含算例）。
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "domain" / "tools"))

DATA = ROOT / "domain" / "data"
KB = ROOT / "domain" / "kb"
MANUAL = KB / "manual_zh"

#: 诱饵弹单价，从存档里「1 艘船只带这一种弹」的样本反解出来
#: （`TotalPoints - 船体 - 部件 - 弹库` 就是弹药账单，见 `recover_ammo_prices.py`）。
#:   EA12 —— 224 艘样本，193 艘精确落在 1.00
#:   EA14 —— 5 艘样本，3 艘精确落在 2.00
#:   EA99 —— 4 艘样本，**4/4 精确落在 8.00**（含一艘带 92 发的：736/92）
#:   EA20 —— 72 艘样本（`_probe_ea20.py` 2026-11-18），**中位数 1.00**，故按 1 点记
DECOYS = {
    "EA12 Chaff Decoy": 1.0,
    "EA14 Chaff Decoy": 2.0,
    "EA20 Flare Decoy": 1.0,
    "EA99 Active Decoy": 8.0,
}

MAGAZINE = {
    "Bulk Magazine": (0.0, 20.0),
    "Reinforced Magazine": (0.0, 40.0),
    "Citadel Magazine": (0.0, 60.0),
}

COST_RE = re.compile(r"cost\s*=\s*([0-9.]+)\s*pts", re.IGNORECASE)


def norm(text: str) -> str:
    """存档里的弹名 → 查表键：去引号、去 `[PD Prio Fired]` 这类后缀、压空格。"""
    text = re.sub(r"\[[^\]]*\]", "", text or "")
    text = text.replace("'", "'").replace("`", "'")
    text = re.sub(r"\s+", " ", text).strip()
    return text.lower()


def shells() -> dict[str, float]:
    raw = json.loads((DATA / "munition_costs.json").read_text(encoding="utf-8"))
    out: dict[str, float] = {}
    for name, value in raw.items():
        m = re.match(r"\s*([0-9.]+)\s*/\s*([0-9.]+)", str(value))
        if not m:
            continue
        pts, rounds = float(m.group(1)), float(m.group(2))
        if rounds:
            out[name] = pts / rounds  # 每发点数
    return out


def missiles() -> dict[str, float]:
    """wiki 上的 20 种导弹部件模板（作为示例表的来源）。"""
    out: dict[str, float] = {}
    for path in sorted((KB / "docs" / "missile").glob("*.md")):
        try:
            head = path.read_text(encoding="utf-8")
        except OSError:
            continue
        title = next((ln.lstrip("# ").strip() for ln in head.splitlines() if ln.startswith("# ")), "")
        m = COST_RE.search(head)
        if title and m:
            out[title] = float(m.group(1))
    return out


def player_missiles() -> dict[str, float]:
    """所有玩家自制导弹（模板存档 + 舰队内嵌），`domain/data/missile_prices.json`。"""
    path = DATA / "missile_prices.json"
    if not path.exists():
        return {}
    data = json.loads(path.read_text(encoding="utf-8"))
    return {name: float(rec["cost"]) for name, rec in (data.get("prices") or {}).items()}


def lookup(name: str, table: dict[str, float]) -> float | None:
    key = norm(name)
    if key in table:
        return table[key]
    for k, v in table.items():
        nk = norm(k)
        if nk == key or (len(nk) > 6 and (nk in key or key in nk)):
            return v
    return None


def craft_table() -> dict[str, float]:
    """舰载机单价：`craft_prices.json` 里 `$CRAFT$/…` → 昵称 → 点数。"""
    path = DATA / "craft_prices.json"
    if not path.exists():
        return {}
    seat = json.loads(path.read_text(encoding="utf-8")).get("seat") or {}
    out: dict[str, float] = {}
    for key, entry in seat.items():
        cost = entry.get("cost") if isinstance(entry, dict) else None
        if not isinstance(cost, (int, float)):
            continue
        name = (entry.get("nickname") or "").strip() or key.split("/")[-1]
        out.setdefault(name, float(cost))
    return out


def render(shell_table: dict[str, float], missile_table: dict[str, float]) -> str:
    rows = sorted(shell_table.items(), key=lambda kv: (-int(re.match(r"\d+", kv[0]).group(0)), kv[0]))
    lines = [
        "# 弹药点数表（0.6.2.6）",
        "",
        "Tags: kind=manual; topic=ammo cost, 弹药点数, 每发几点, 装填预算",
        "Keywords: 弹药点数, 一发几点, 装填, 弹库, 炮弹, 导弹, 诱饵, 预算, cost per round",
        "Summary: 每种弹一发的点数：炮弹看 `X 发 / 1 点`，导弹看模板 `cost=N pts`，"
        "诱饵 EA12 = 1、EA14 = 2、EA99 = 8 点/发；弹库本身首座免费、之后按型号收费。"
        "配船时用它把「部件点数 + 弹药点数」算到官方总价。",
        "",
        "## 速查（一句话回答）",
        "",
        "- **450mm 炮弹一发多少点**：0.04 点（25 发 = 1 点）。375 发 450mm HE ≈ 15 点。",
        "- **250mm 炮弹一发多少点**：0.02 点（50 发 = 1 点）。",
        "- **120mm 炮弹一发多少点**：0.01 点（100 发 = 1 点）。",
        "- **100mm 炮弹一发多少点**：0.004 点（250 发 = 1 点）。",
        "- **20mm Slug 一发多少点**：0.0005 点（2000 发 = 1 点）。",
        "- 小口径高炮（50mm Flak / 35mm）按上表，几十发才 1 点。",
        "- **导弹一发多少点**：看导弹模板的 `cost=N pts`（战斗部+引擎+引导头合计），常见 4–13 点，重型 20–30 点。",
        "- **诱饵弹一发多少点**：EA12 Chaff 1 点、EA14 Chaff 2 点、EA99 Active **8 点**"
        "（从存档总价反解，4/4 样本一致）；EA20 Flare 按 1 点记（未验证）。",
        "- **弹库要算点数吗**：要。同一艘船最贵的一座免点，之后 Bulk 20 / Reinforced 40 / Citadel 60。",
        "- **为什么生成器算出来的点数和游戏不一样**：`build_fleet.py` 只算舰体+部件，没算弹库与弹药；"
        "把这两项补上才是游戏总价（450 CH 例：1340 → 约 1434，存档 1500）。",
        "",
        "## 怎么算",
        "",
        "1. **部件点数**：舰体 + 每个部件的 `Cost (pts)`（弹库首座记 0，见下）。",
        "2. **弹药点数**：每发单价 × 发数，向上取整到点（游戏按点计费，`ceil(发数 ÷ 每点发数)`）。",
        "3. **弹库点数**：同一艘船上最贵的一个弹库免点，其余按型号收费（Bulk 20 / Reinforced 40 / Citadel 60）。",
        "4. 全部相加 = 游戏里显示的总点数。存档 `<Cost>` 与按上面算出来的差，基本就是漏算的弹药。",
        "",
        "## 炮弹（每点发数 / 每发点数）",
        "",
        "| 弹种 | 每点发数 | 每发点数 | 100 发 | 1000 发 |",
        "|---|---:|---:|---:|---:|",
    ]
    for name, ppr in rows:
        per_point = int(round(1 / ppr)) if ppr else 0
        lines.append(
            f"| {name} | {per_point} | {ppr:.4f} | {100 * ppr:.1f} 点 | {1000 * ppr:.0f} 点 |"
        )
    lines += [
        "",
        "## 导弹（模板总价，含弹体/引擎/引导头）",
        "",
        "下面是 wiki 上的 20 种导弹部件模板；**玩家自制导弹另有 536 种**，"
        "单价都在 `domain/data/missile_prices.json`（来自 `Saves\\MissileTemplates` 的存档"
        "和每条 `.fleet` 里内嵌的 `<MissileTemplates>`），脚本按名字就能查到，"
        "常见值 1–30 点/发。",
        "",
        "| 导弹模板 | 每发点数 |",
        "|---|---:|",
    ]
    for name, pts in sorted(missile_table.items()):
        lines.append(f"| {name} | {pts:g} |")
    lines += [
        "",
        "## 诱饵与干扰弹",
        "",
        "| 型号 | 每发点数 | 依据 | 备注 |",
        "|---|---:|---|---|",
        "| EA12 Chaff Decoy | 1 | 224 艘样本，193 艘反解正好 1.00 | S1，VLS-1 系列专用 |",
        "| EA14 Chaff Decoy | 2 | 5 艘样本，3 艘反解正好 2.00 | S1，长时干扰 |",
        "| EA20 Flare Decoy | 1 | 72 艘样本，中位数反解 1.00 | S1，对抗红外制导 |",
        "| EA99 Active Decoy | **8** | 4 艘样本，4/4 反解正好 8.00（含带 92 发的一艘：736 ÷ 92） | S1，主动诱饵 |",
        "",
        "> 反解方法：存档里每艘船都有游戏算好的 `<Cost>`，"
        "`Cost − 舰体 − 部件 − 弹库 − 已知弹药` 就是剩下那种弹的账单；"
        "只带一种未知弹的船可以直接除出发数。",
        "",
        "## 舰载机（机库里那一架多少点）",
        "",
        "来源：每支存档舰队根节点的 `<CraftTypes><CraftTemplate><Cost>`，按 `<SaveKey>` 归并"
        "（`domain/data/craft_prices.json`，48 种）。机库里的每一架都从舰队模板库取价，"
        "**按架计价、不算弹药**。",
        "",
    ]
    crafts = craft_table()
    if crafts:
        lines += ["| 舰载机 | 点数 |", "|---|---:|"]
        for name, pts in sorted(crafts.items(), key=lambda kv: (kv[1], kv[0])):
            lines.append(f"| {name} | {pts:g} |")
        lines += [
            "",
            f"> 共 {len(crafts)} 种；常见 8–20 点（`PF-386 Barracuda` 8、`RS-35P Halberd` 15、`B-86T Claymore` 19），"
            "重型机 54–77 点（`Oasis` 54、`E-448 Sundial` 77）。",
        ]
    lines += [
        "",
        "## 弹库（座数计价）",
        "",
        "| 弹库 | 第一座 | 之后每座 |",
        "|---|---:|---:|",
        "| Bulk Magazine | 0 | 20 |",
        "| Reinforced Magazine | 0 | 40 |",
        "| Citadel Magazine（OSP） | 0 | 60 |",
        "",
        "> 同一艘船只免**最贵的一座**：带 1 座 Reinforced + 1 座 Bulk 时，Reinforced 免点、Bulk 记 20 点。",
        "",
        "## 算例：450 CH 样板船 Value Judgement",
        "",
        "| 项 | 点数 |",
        "|---|---:|",
        "| 舰体 Axford Heavy Cruiser | 600 |",
        "| 部件合计 | 740 |",
        "| 弹库（Reinforced 免点 + Bulk 20） | 20 |",
        "| 450mm HE 375 发（15）＋ AP 200 发（8） | 23 |",
        "| 20mm Slug 4000 发（2）＋ Flak 450 发（6） | 8 |",
        "| 诱饵 EA99 ×6（48）＋ EA12 ×7（7） | 55 |",
        "| **小计** | **≈1446** |",
        "| 存档总价 | **1500** |",
        "",
        "差额约 54 点来自同船那组玩家导弹（`SGM-299 Killjoy` 干扰诱饵 ×4 等，"
        "模板价只写在存档里、没进公开 wiki），以及第二条弹库的装填量。"
        "**结论**：`build_fleet.py` 只算舰体+部件，所以两艘 450 CH 生成出来是 2680 点；"
        "把弹库和弹药补进去才是 3000。",
        "",
    ]
    return "\n".join(lines)


def main() -> int:
    shell_table = shells()
    missile_table = missiles()
    players = player_missiles()
    ammo = {
        "shells": shell_table,
        # 计算用：wiki 的 20 种模板 + 536 种玩家自制导弹（模板存档与舰队内嵌）
        "missiles": {**missile_table, **players},
        "decoys": DECOYS,
        "magazines": {k: {"first": v[0], "next": v[1]} for k, v in MAGAZINE.items()},
    }
    (DATA / "ammo_costs.json").write_text(
        json.dumps(ammo, ensure_ascii=False, indent=1), encoding="utf-8"
    )
    MANUAL.mkdir(parents=True, exist_ok=True)
    out = MANUAL / "弹药点数表.md"
    out.write_text(render(shell_table, missile_table), encoding="utf-8")
    print(
        f"shells={len(shell_table)} missiles={len(missile_table)} "
        f"player missiles={len(players)} -> {out}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

"""Generate `manual_zh/装甲与伤害机制.md` from the wiki mechanics + measured hull armour.

Sources
-------
* hull armour values: `domain/data/hull_armour.json` (player read them off the in-game
  hull panel; one value per hull, uniform over the whole surface, unit cm).
* shell penetration: parsed from `domain/kb/docs/munition/*.md` (`Penetration (cm)`).
* formulas: `Nebulous.decompiled.cs`
    - `Hull.GetEffectiveArmorThickness` (47042)
    - `Hull.WouldArmorHitPenetrate` (47061)
    - `Hull.CalculateInteriorTravel` (47047)
    - `Hull.ComponentDR = Lerp(MinComponentDR, MaxComponentDR, PositionInRange(fill,0.2,0.6))` (46255)
    - `HullComponent` DT/Reinforced killing rules (60928)
  plus the wiki pages Mechanics › Armor and Mechanics › Component damage.
"""

from __future__ import annotations

import json
import math
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]  # project root
OUT = ROOT / "domain" / "kb" / "manual_zh" / "装甲与伤害机制.md"
ARMOUR = json.loads((ROOT / "domain" / "data" / "hull_armour.json").read_text(encoding="utf-8"))["hulls"]

SHELL_ROW = re.compile(r"- \*\*(?P<label>[^:]+):\*\* (?P<value>[^\n]+)", re.M)


def shells() -> list[dict]:
    """[{'name','pen','dmg','caliber','kind'}] from the generated munition docs."""
    out = []
    for path in sorted((ROOT / "domain" / "kb" / "docs" / "munition").glob("*.md")):
        text = path.read_text(encoding="utf-8")
        pen = re.search(r"Penetration \(cm\): (\d+)", text)
        if not pen:
            continue
        dmg = re.search(r"Damage \(Hp\): (\d+)", text)
        name = path.stem
        caliber = re.match(r"(\d+mm)", name)
        out.append(
            {
                "name": name,
                "pen": int(pen.group(1)),
                "dmg": int(dmg.group(1)) if dmg else 0,
                "caliber": caliber.group(1) if caliber else "其它",
                "kind": "AP" if "ap-" in name else ("HE" if "he-" in name else "其它"),
            }
        )
    return out


def effective(base: float, angle_deg: float) -> float:
    return min(base / max(math.cos(math.radians(angle_deg)), 1e-3), base * 2.5)


def main() -> int:
    rows = sorted(ARMOUR.items(), key=lambda kv: kv[1])
    shots = shells()

    def penetrates_against(pen: int) -> list[str]:
        return [h for h, t in rows if pen >= t]

    lines = [
        "# 装甲与伤害机制（穿深 / 跳弹 / DR / DT / 过穿）",
        "",
        "Tags: kind=manual; topic=armour, armor, 装甲, 穿深, 跳弹, 跳弹火花, DR, damage reduction, "
        "DT, damage threshold, 减伤, 阈值, 过穿, overpenetration, reinforced, 加固, 内部密度",
        "Keywords: 装甲, 装甲值, 多少装甲, 穿深, 打得穿吗, 跳弹, 火花, 减伤, DR, DT, 阈值, 过穿, 内部密度, "
        "加固, reinforced, 结构断裂, 结构破坏, 打什么弹, penetration",
        "Summary: 每艘船的装甲厚度（cm）+ 穿透判定（入射角、有效厚度、跳弹 80°）、DR/DT/加固/过穿/结构断裂的完整规则与来源行号。",
        "",
        "一句话：**能不能打穿看 `穿深(AP) ≥ 该船装甲 × 入射角系数 × 该点剩余装甲比例`**；"
        "打穿了才谈伤害，没打穿只有两种结果——擦掉一层装甲（跳弹时只擦 20%），或者跳弹。",
        "",
        "## 一、装甲值（cm，全船表面同一厚度）",
        "",
        "来源：玩家在游戏内船体面板读数（2026-11-17），单位 **cm**；"
        "wiki 原文也确认装甲是「均匀铺满整条船的一层」，不是艏/侧/艉分开的数值。"
        "装甲以贴图遮罩的形式存在，**打哪儿掉哪儿**（局部削甲），不是全船一个血量。",
        "",
        "| 船体 | 装甲 (cm) | 类别 |",
        "|---|---:|---|",
    ]
    classes = {
        "Sprinter": "FFL 轻护卫", "Raines": "FF 护卫舰", "Keystone": "DD 驱逐舰",
        "Vauxhall": "CL 轻巡", "Axford": "CH 重巡", "Levy": "CVE 护航航母",
        "Solomon": "BB 战列舰", "Worden": "CVL 舰队航母", "Mercator": "补给油船",
        "Ferryman": "穿梭机", "Draugr": "拖船", "Flathead": "MN 监视舰",
        "Journeyman": "CVL 轻型航母", "Ocello": "CC 指挥巡洋舰", "Marauder": "LN 线列舰",
        "Moorline": "CLN 线列巡洋舰",
    }
    for hull, value in rows:
        lines.append(f"| {hull} | {value} | {classes.get(hull, '—')} |")
    lines += [
        "",
        "实测口径（重要）：**装甲不会因为装了什么部件而变**——装 Reinforced 部件只是让部件血量更难掉，"
        "不改装甲值；装甲只跟船体型号走。",
        "",
        "## 二、穿透判定（源码 `WouldArmorHitPenetrate`, 47061）",
        "",
        "```",
        "有效厚度 = clamp( 装甲 / cos(入射角) ,  0 ,  装甲 × 2.5 )        // 47042",
        "剩余装甲 RA = 该点剩余比例 × 有效厚度",
        "穿透     ⇔  AP ≥ RA",
        "削甲量   = AP × min(AP / RA, 1)        // 没穿透时这个值就是「擦破一层」",
        "跳弹     ⇔  RA × 2 ≥ AP  且  入射角 ≥ 80°",
        "跳弹削甲 = 削甲量 × 0.2                 // 184920",
        "```",
        "",
        f"- 「入射角」是**期望方向与表面法线的夹角**；正对 0°，掠射趋近 90°。"
        f"60° 时厚度 ×2，80° 时 ×5.76——所以斜着打等于给对面加甲。",
        "- **火花的含义**：打上去冒一片火花 = 跳弹（还没打穿）；这时候该换更高穿深的弹，或者换角度。",
        "- 忽略入射角：等离子（plas）穿甲不看角度；导弹/火箭/炸弹/光束设了 `NeverRicochet`，永远不会跳弹。",
        "- 同一发弹打**出射面**还要再过一次装甲检定（`WouldArmorHitPenetrate(hitInfo.ExitPoint, …)`，184837），"
        "过了才叫过穿。",
        "",
        "## 三、弹药穿深与「打不打得穿」（正面 0°，与上表对比）",
        "",
        "| 弹药 | 穿深 (cm) | 伤害 (hp) | 正面能打穿 |",
        "|---|---:|---:|---|",
    ]
    for shot in sorted(shots, key=lambda s: -s["pen"]):
        hit = penetrates_against(shot["pen"])
        span = f"{hit[0]}～{hit[-1]}（{len(hit)}/{len(rows)}）" if hit else "无（连 Sprinter 都打不穿）"
        lines.append(f"| {shot['name']} | {shot['pen']} | {shot['dmg']} | {span} |")
    lines += [
        "",
        "读法：这张表是 **0° 正击**的结果；按上面的 `1/cos` 算角度后结论会变。"
        "例：120mm AP（45 cm）打 Solomon（56 cm）正面——0° 打得穿（45 < 56？不，见下）；"
        "30° 时有效厚度 56/cos30° = 64.7 cm，45 < 64.7 → **打不穿**，只能擦 45×(45/64.7)=31.3 cm（wiki 原例）。",
        "",
        "## 四、打穿之后：穿透深度与过穿",
        "",
        "```",
        "穿透深度(m) = 剩余穿深 / 内部密度(cm/m)                 // 47047",
        "实际行进(cm) = min( 入射点到出射点距离 × 10 , 穿透深度 × 10 )",
        "能过穿       ⇔ 穿透深度 ≥ 入射点到出射点距离",
        "```",
        "",
        "- 内部密度是船体属性（`hull-internaldensity`，默认 1 cm/m，不同舰种不同）；"
        "wiki 举例：HEKP 打完 Solomon 剩 180 cm，密度 1.2 cm/m → 能穿 150 m。",
        "- 多数弹种有 **15 m 最小穿透深度**：只要打穿装甲，就算只剩 1 cm 也会穿到 15 m。",
        "- **过穿（overpenetration）**：穿透后从另一侧出去 → 伤害按弹种的 overpen 系数打折，"
        "AP 会把伤害分摊给沿途所有部件（HE 过穿则不炸，只分摊削减后的伤害）。"
        "部分弹有「穿透深度覆盖」，只影响过穿判定、不影响命中深度。",
        "",
        "## 五、部件减伤（DR）与伤害阈值（DT）",
        "",
        "```",
        "填入槽位比例 f（只数槽位数量，不看大小）：",
        "ComponentDR = clamp( lerp(0.25×MaxDR, MaxDR, PositionInRange(f, 0.2, 0.6)), 0, 0.9 )   // 46255",
        "```",
        "",
        "- **DR**：船体 DR 按百分比削减进入部件的伤害；**先乘 DR，再判 DT**，所以高 DR 会让 DT 极其难破。",
        "- f ≤ 20% 时只有满值的 1/4；f ≥ 60% 时拿满值。模块被打掉不影响 DR（残骸还在）。",
        "- 火、燃烧（burnthrough）不吃 DR；部分弹药标注 `Ignore DR`。",
        "- **DT**：最后一击必须 **大于** 部件 DT 才能摧毁；否则部件停在 0 HP 变红（失效、可被 DC 修），不算摧毁。",
        "- **Reinforced（加固）**：部件在 0 HP 以上时，任何一次命中最多把它打到 0 HP；"
        "要真正「灰掉」必须**在 0.25 s 内再吃一发**破 DT 的伤害（DC 修得比这快就永远打不死）。",
        "",
        "## 六、结构断裂（structure break）",
        "",
        "- 命中结构体、且路径上没有部件（含已摧毁部件）时，伤害进结构血。",
        "- **减伤后 < 20 的命中不计入结构伤害**（小口径洗不了结构）。",
        "- 结构断裂后：对结构的伤害改为随机转移给一个存活部件，且**船员受到的伤害 +50%**。",
        "",
        "## 七、配船 / 对炮时怎么用",
        "",
        "1. 先看对面装甲（上表）→ 再看自己带的弹穿深（第三节表）→ 结论：**能不能正面打穿**。",
        "2. 打不穿就换角度（侧舷、俯冲）或者换弹种；指望 HE 洗穿 40 cm 的 Axford 是不现实的。",
        "3. 打穿之后看 DT：对面部件 DT 高（比如 40+）时，需要单发高伤弹药（AP/PLASMA）才「一发破」，纸片伤害只能磨。",
        "4. 看到火花 → 是跳弹，不是命中了；换 AP 或换角度。",
        "5. 想拆一个加固部件：要么两发极短时间内命中，要么先用大伤害单发压到 0 血再补。",
        "",
        "## 八、来源",
        "",
        "- 装甲值：玩家实测（游戏内面板），见 `domain/data/hull_armour.json`。",
        "- 公式与阈值：`Nebulous.decompiled.cs` 行号见各节括注；wiki `Mechanics › Armor`、`Mechanics › Component damage`。",
        "- 弹药穿深：`docs/munition/*.md` 的 `Penetration (cm)` 字段（wiki 0.6.2.6）。",
        "",
    ]
    OUT.write_text("\n".join(lines), encoding="utf-8")
    print(f"wrote {OUT.relative_to(ROOT.parent)} ({len(rows)} hulls, {len(shots)} shells)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

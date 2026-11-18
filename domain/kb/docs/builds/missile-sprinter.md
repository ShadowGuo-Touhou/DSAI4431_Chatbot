# missile sprinter

Tags: kind=build template; class=missile sprinter; cost=300-500; samples=60; good=9
Keywords: build, loadout, template, 配装, 配置, 装配, 模板, 舰级, missile sprinter
Summary: missile sprinter build; 60 matched ships, 9 of them are good samples (must and should both pass); typical cost 352 (range 304-480); hull Sprinter Corvette Class×9.
Section: build templates; requirements from other info/Ship Builds.txt; samples from player fleets

## How to read this
回答「这艘船算不算 / 合不合格」以 Requirements 段为准（must 全过才算这个舰级，should 是良好标准）；部件清单只统计 good 样本，频率 (k/N) 表示常见程度，不是硬性要求。所有舰船先要过通用基线（`reference/baseline-requirements.md`），再看本舰级要求。

## 舰级要求（Ship Builds.txt 原文，作为判定依据）

**舰级硬性要求（required：缺一条就不算这个舰级）**
- have 1 large vls-2, vls-3 or cls-3 launcher (mount 1)
- have >30 points of offensive missiles

**良好标准（should：缺了算有瑕疵，但仍算这个舰级）**
- have minimal DC (1 rapid DC Locker)
- have >80 points of offensive missiles
- minimal softkill
- minimal hardkill

**可选加分（optional）**
- have 1 blanket jammer
- have 1 bullseye jammer
- have better DC (at least 1 restore)
- have 1 reinforced CIC
- have 1 floodlight illuminator

## Disclaimer
参考配置，不是最优解。样本是玩家舰队里 must + should 全过的真实配装（主要取自中文新手包 v1.12，对应游戏 0.6.2.3；其余来自 other info 与本地存档）。旧版本可能改过数值或改过名字；模组部件不代表原版能照抄。把它当起步模板，不要当配方。

## Numbers
- Point cost: 300-500 (good-sample median 352, range 304-480)
- Power: draw 2475 kW / supply 2900 kW (median)
- Hull: Sprinter Corvette Class×9

## Armament (good samples)
- 120 mm turret/cannon: 3/9 ships, median 1 (min 1, max 1)
- VLS-1-23 launcher: 9/9 ships
- CLS-3 launcher: 5/9 ships
- VLS-2 launcher: 4/9 ships

## Core parts (fitted on most good samples)
- Basic CIC (9/9)
- FR3300 Micro Reactor (9/9)
- Reinforced Magazine (9/9)
- VLS-1-23 Launcher (9/9)

## Common parts (40-70%)
- CLS-3 Launcher (5/9)
- FM230 'Whiplash' Drive (6/9)
- Missile Programming Bus (4/9)
- Mk20 'Defender' PDT (5/9)
- Mk95 'Sarissa' PDT (4/9)
- RF101 'Bullseye' Radar (4/9)
- RS35 'Frontline' Radar (5/9)
- Rapid DC Locker (5/9)
- Small DC Locker (4/9)
- VLS-2 Launcher (4/9)

## Optional parts
- Auxiliary Steering (3/9)
- FM200 Drive (3/9)
- Mk61 Cannon (3/9)
- E90 'Blanket' Jammer (2/9)
- Plant Control Center (2/9)

## Sample ships (good)
- Blaire B. Lennon (jam CL dad, 304 pts, player save)
- Born Loom (mixed cap, 308 pts, player save)
- Xavier E. Sletten (mixed cap, 308 pts, player save)
- T. Final Light (Mixed FFLs, 352 pts, player save)
- T. Tepid Siren (Mixed FFLs, 352 pts, player save)
- Wang (Shock 12k, 479 pts, player save)

## 样板船完整装配（整艘照抄）：T. Final Light（Mixed FFLs）

**整艘照抄**：舰体 `Sprinter Corvette`（阵营键 `Stock/Shelter Alliance`），存档原值 **352 点**，共 11 个槽位。复制这艘船时连它自带的导弹一起抄，只改船名、呼号和导弹名。

| 槽位 | 部件 | 尺寸 | 点数 | 供电 kW |
|---|---|---|---:|---:|
| MT1 | CLS-3 Launcher | 3x4x3 | 20 | -200 |
| MT2 | E90 'Blanket' Jammer | 2x1x2 | 50 | -1000 |
| MT3 | VLS-1-23 Launcher | 2x2x2 | 5 | -50 |
| MT4 | Mk20 'Defender' PDT | 2x1x2 | 25 | -175 |
| CMP1 | Basic CIC | 4x1x6 | 10 | 0 |
| CMP2 | Rapid DC Locker | 3x1x3 | 10 | 0 |
| CMP3 | Reinforced Magazine | 1x1x1 | 0 → 之后 40/座 | 0 |
| CMP4 | Plant Control Center | 3x1x3 | 25 | 0 |
| MOD1 | FR3300 Micro Reactor | 3x3x3 | 10 | +2250 |
| MOD2 | FM230 'Whiplash' Drive | 5x3x5 | 20 | 0 |
| MOD3 | RS35 'Frontline' Radar | 2x2x2 | 10 | -2000 |

- 合计：部件 185 点 + 舰体 75 点 = **260 点**（不含弹库与弹药，见下）
- 另有弹库 0 点 + 弹药 92 点 ⇒ **全价约 352 点**（估算；游戏里以存档原值 352 为准，单价见 `zh/弹药点数表.md`）
- 供电：发电 2250 kW / 耗电 3425 kW（余量 -1175 kW）
- 弹库装载：MT1 CLS-3 Launcher：EcAKwUE25EuRPL_lZJut7w ×3、SGT-300 主力打击 ×3；MT3 VLS-1-23 Launcher：EA12 Chaff Decoy ×5、mT0rvhr38EiCnWPALx0BLQ ×1；CMP3 Reinforced Magazine：20mm Slug ×4000


## 样板船完整装配（整艘照抄）：T. Tepid Siren（Mixed FFLs）

**整艘照抄**：舰体 `Sprinter Corvette`（阵营键 `Stock/Shelter Alliance`），存档原值 **352 点**，共 11 个槽位。复制这艘船时连它自带的导弹一起抄，只改船名、呼号和导弹名。

| 槽位 | 部件 | 尺寸 | 点数 | 供电 kW |
|---|---|---|---:|---:|
| MT1 | CLS-3 Launcher | 3x4x3 | 20 | -200 |
| MT2 | E90 'Blanket' Jammer | 2x1x2 | 50 | -1000 |
| MT3 | VLS-1-23 Launcher | 2x2x2 | 5 | -50 |
| MT4 | Mk20 'Defender' PDT | 2x1x2 | 25 | -175 |
| CMP1 | Basic CIC | 4x1x6 | 10 | 0 |
| CMP2 | Rapid DC Locker | 3x1x3 | 10 | 0 |
| CMP3 | Reinforced Magazine | 1x1x1 | 0 → 之后 40/座 | 0 |
| CMP4 | Plant Control Center | 3x1x3 | 25 | 0 |
| MOD1 | FR3300 Micro Reactor | 3x3x3 | 10 | +2250 |
| MOD2 | FM230 'Whiplash' Drive | 5x3x5 | 20 | 0 |
| MOD3 | RS35 'Frontline' Radar | 2x2x2 | 10 | -2000 |

- 合计：部件 185 点 + 舰体 75 点 = **260 点**（不含弹库与弹药，见下）
- 另有弹库 0 点 + 弹药 92 点 ⇒ **全价约 352 点**（估算；游戏里以存档原值 352 为准，单价见 `zh/弹药点数表.md`）
- 供电：发电 2250 kW / 耗电 3425 kW（余量 -1175 kW）
- 弹库装载：MT1 CLS-3 Launcher：EcAKwUE25EuRPL_lZJut7w ×3、SGT-300 主力打击 ×3；MT3 VLS-1-23 Launcher：EA12 Chaff Decoy ×5、mT0rvhr38EiCnWPALx0BLQ ×1；CMP3 Reinforced Magazine：20mm Slug ×4000


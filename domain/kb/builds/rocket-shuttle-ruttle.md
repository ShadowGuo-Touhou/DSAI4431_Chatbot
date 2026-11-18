# rocket shuttle (ruttle)

Tags: kind=build template; class=rocket shuttle (ruttle); cost=260-300; samples=7; good=4
Keywords: build, loadout, template, 配装, 配置, 装配, 模板, 舰级, rocket shuttle (ruttle)
Summary: rocket shuttle (ruttle) build; 7 matched ships, 4 of them are good samples (must and should both pass); typical cost 282 (range 277-286); hull Ferryman Clipper Class×4.
Section: build templates; requirements from other info/Ship Builds.txt; samples from player fleets

## How to read this
回答「这艘船算不算 / 合不合格」以 Requirements 段为准（must 全过才算这个舰级，should 是良好标准）；部件清单只统计 good 样本，频率 (k/N) 表示常见程度，不是硬性要求。所有舰船先要过通用基线（`reference/baseline-requirements.md`），再看本舰级要求。

## 舰级要求（Ship Builds.txt 原文，作为判定依据）

**舰级硬性要求（required：缺一条就不算这个舰级）**
- have minimal DC (at least 1 restore)
- have at least 1 RL-18 launcher
- have minimal softkill
- have R2 rockets

**良好标准（should：缺了算有瑕疵，但仍算这个舰级）**
- have the max amount of R2 Rockets it can carry (18 for each launcher it has)

**可选加分（optional）**
- have 2 RL-18 launchers
- have 1 T20 turret
- have pinpoint

## Disclaimer
参考配置，不是最优解。样本是玩家舰队里 must + should 全过的真实配装（主要取自中文新手包 v1.12，对应游戏 0.6.2.3；其余来自 other info 与本地存档）。旧版本可能改过数值或改过名字；模组部件不代表原版能照抄。把它当起步模板，不要当配方。

## Numbers
- Point cost: 260-300 (good-sample median 282, range 277-286)
- Power: draw 1350 kW / supply 2050 kW (median)
- Hull: Ferryman Clipper Class×4

## Armament (good samples)
- RL18 launcher: 4/4 ships
- VLS-1-23 launcher: 4/4 ships

## Core parts (fitted on most good samples)
- Ithaca Bridgemaster (4/4)
- Light Civilian Reactor (4/4)
- RL18 Launcher (4/4)
- Reinforced CIC (4/4)
- Reinforced Magazine (4/4)
- Small DC Locker (4/4)
- Sundrive Racing Pro (4/4)
- VLS-1-23 Launcher (4/4)

## Common parts (40-70%)
- -

## Optional parts
- -

## Sample ships (good)
- Applied Pressure (Azurite Squadron, 286 pts, example fleet)
- Repulsive Force (Azurite Squadron, 286 pts, example fleet)
- Applied Pressure (All 27 sample ships · Protectorate, 277 pts, player save)
- Repulsive Force (All 27 sample ships · Protectorate, 277 pts, player save)

## 样板船完整装配（整艘照抄）：Applied Pressure（Azurite Squadron）

**整艘照抄**：舰体 `Shuttle`（阵营键 `Stock/Outlying Systems Protectorate`），存档原值 **286 点**，共 9 个槽位。复制这艘船时连它自带的导弹一起抄，只改船名、呼号和导弹名。

| 槽位 | 部件 | 尺寸 | 点数 | 供电 kW |
|---|---|---|---:|---:|
| MT1 | RL18 Launcher | 3x1x3 | 30 | -50 |
| MT2 | RL18 Launcher | 3x1x3 | 30 | -50 |
| MT3 | VLS-1-23 Launcher | 2x2x2 | 5 | -50 |
| CMP1 | Reinforced CIC | 4x1x6 | 25 | 0 |
| CMP2 | Reinforced Magazine | 1x1x1 | 0 → 之后 40/座 | 0 |
| CMP3 | Small DC Locker | 3x1x3 | 20 | 0 |
| MOD1 | Light Civilian Reactor | 3x3x3 | 10 | +1850 |
| MOD2 | Sundrive Racing Pro | 5x3x5 | 20 | 0 |
| MOD3 | Ithaca Bridgemaster | 2x2x2 | 10 | -1200 |

- 合计：部件 150 点 + 舰体 50 点 = **200 点**（不含弹库与弹药，见下）
- 另有弹库 0 点 + 弹药 14 点 ⇒ **全价约 214 点**（估算；游戏里以存档原值 286 为准，单价见 `zh/弹药点数表.md`）
- 供电：发电 1850 kW / 耗电 1350 kW（余量 +500 kW）
- 弹库装载：MT1 RL18 Launcher：S1 Rocket ×18；MT2 RL18 Launcher：S1 Rocket ×18；MT3 VLS-1-23 Launcher：EA12 Chaff Decoy ×5、SGM-111 Night Dances ×4、SGM-1 Ceremonial Arming Missile ×1


## 样板船完整装配（整艘照抄）：Repulsive Force（Azurite Squadron）

**整艘照抄**：舰体 `Shuttle`（阵营键 `Stock/Outlying Systems Protectorate`），存档原值 **286 点**，共 9 个槽位。复制这艘船时连它自带的导弹一起抄，只改船名、呼号和导弹名。

| 槽位 | 部件 | 尺寸 | 点数 | 供电 kW |
|---|---|---|---:|---:|
| MT1 | RL18 Launcher | 3x1x3 | 30 | -50 |
| MT2 | RL18 Launcher | 3x1x3 | 30 | -50 |
| MT3 | VLS-1-23 Launcher | 2x2x2 | 5 | -50 |
| CMP1 | Reinforced CIC | 4x1x6 | 25 | 0 |
| CMP2 | Reinforced Magazine | 1x1x1 | 0 → 之后 40/座 | 0 |
| CMP3 | Small DC Locker | 3x1x3 | 20 | 0 |
| MOD1 | Light Civilian Reactor | 3x3x3 | 10 | +1850 |
| MOD2 | Sundrive Racing Pro | 5x3x5 | 20 | 0 |
| MOD3 | Ithaca Bridgemaster | 2x2x2 | 10 | -1200 |

- 合计：部件 150 点 + 舰体 50 点 = **200 点**（不含弹库与弹药，见下）
- 另有弹库 0 点 + 弹药 14 点 ⇒ **全价约 214 点**（估算；游戏里以存档原值 286 为准，单价见 `zh/弹药点数表.md`）
- 供电：发电 1850 kW / 耗电 1350 kW（余量 +500 kW）
- 弹库装载：MT1 RL18 Launcher：S1 Rocket ×18；MT2 RL18 Launcher：S1 Rocket ×18；MT3 VLS-1-23 Launcher：EA12 Chaff Decoy ×5、SGM-111 Night Dances ×4、SGM-1 Ceremonial Arming Missile ×1


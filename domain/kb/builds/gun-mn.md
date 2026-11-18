# gun MN

Tags: kind=build template; class=gun MN; cost=450-650; samples=51; good=7
Keywords: build, loadout, template, 配装, 配置, 装配, 模板, 舰级, gun MN
Summary: gun MN build; 51 matched ships, 7 of them are good samples (must and should both pass); typical cost 594 (range 570-622); hull Flathead Monitor Class×7.
Section: build templates; requirements from other info/Ship Builds.txt; samples from player fleets

## How to read this
回答「这艘船算不算 / 合不合格」以 Requirements 段为准（must 全过才算这个舰级，should 是良好标准）；部件清单只统计 good 样本，频率 (k/N) 表示常见程度，不是硬性要求。所有舰船先要过通用基线（`reference/baseline-requirements.md`），再看本舰级要求。

## 舰级要求（Ship Builds.txt 原文，作为判定依据）

**舰级硬性要求（required：缺一条就不算这个舰级）**
- have turret and/or cannon

**良好标准（should：缺了算有瑕疵，但仍算这个舰级）**
- have a C90 cannon (mount 1)
- have 1 T30 turret
- have 1 T81 turret
- have minimal softkill
- have 1 Damage control Complex (Compartment 5 or 6)
- have 1 Citadel Magazine (Compartment 5 or 6)
- have minimal DC other than the Damage Control Complex (at least 1 restore)
- have 1 reinforced CIC
- have at least 1 ammo elevator

**可选加分（optional）**
- have at least 2 CIC and/or Auxiliary Steering
- have a huntress radar
- have a pinpoint
- have better softkill

**避免（avoid）**
- have anything other than cannon on spinal mount (mount 1)

## Disclaimer
参考配置，不是最优解。样本是玩家舰队里 must + should 全过的真实配装（主要取自中文新手包 v1.12，对应游戏 0.6.2.3；其余来自 other info 与本地存档）。旧版本可能改过数值或改过名字；模组部件不代表原版能照抄。把它当起步模板，不要当配方。

## Numbers
- Point cost: 450-650 (good-sample median 594, range 570-622)
- Power: draw 4470 kW / supply 5200 kW (median)
- Hull: Flathead Monitor Class×7

## Armament (good samples)
- 600 mm turret/cannon: 7/7 ships, median 1 (min 1, max 1)
- 100 mm turret/cannon: 7/7 ships, median 1 (min 1, max 1)
- 400 mm turret/cannon: 7/7 ships, median 1 (min 1, max 1)
- VLS-1-46 launcher: 5/7 ships
- VLS-1-23 launcher: 2/7 ships

## Core parts (fitted on most good samples)
- Ammunition Elevators (7/7)
- Auxiliary Steering (7/7)
- Boosted Reactor (7/7)
- C90 Cannon (7/7)
- Citadel Magazine (7/7)
- Damage Control Complex (7/7)
- Ithaca Bridgemaster (5/7)
- J15 'Bellbird' Jammer (5/7)
- Rapid DC Locker (7/7)
- Reinforced CIC (7/7)
- Sundrive Racing Pro (7/7)
- T30 Cannon (7/7)
- T81 Plasma Cannon (7/7)
- VLS-1-46 Launcher (5/7)

## Common parts (40-70%)
- RF44 'Pinpoint' Radar (4/7)

## Optional parts
- Bulwark Huntress (2/7)
- P20 'Bastion' PDT (2/7)
- VLS-1-23 Launcher (2/7)
- J75 'Warbler' Jammer (1/7)
- L50 'Blackjack' Laser Dazzler (1/7)

## Sample ships (good)
- Serious Callers Only (Garnet Squadron, 570 pts, example fleet)
- Excuse The Interruption (Garnet Squadron, 594 pts, example fleet)
- Open For Business (Garnet Squadron, 594 pts, example fleet)
- Merely Passing Through (Garnet Squadron, 620 pts, example fleet)
- Just The Warm Up (Garnet Squadron, 622 pts, example fleet)
- Excuse The Interruption (All 27 sample ships · Protectorate, 593 pts, player save)

## 样板船完整装配（整艘照抄）：Excuse The Interruption（Garnet Squadron）

**整艘照抄**：舰体 `Bulk Feeder`（阵营键 `Stock/Outlying Systems Protectorate`），存档原值 **594 点**，共 16 个槽位。复制这艘船时连它自带的导弹一起抄，只改船名、呼号和导弹名。

| 槽位 | 部件 | 尺寸 | 点数 | 供电 kW |
|---|---|---|---:|---:|
| MT1 | C90 Cannon | 6x12x6 | 60 | -200 |
| MT2 | T30 Cannon | 6x3x6 | 20 | -120 |
| MT3 | T81 Plasma Cannon | 6x3x6 | 45 | -1500 |
| MT4 | J15 'Bellbird' Jammer | 3x1x3 | 50 | -850 |
| MT5 | VLS-1-46 Launcher | 3x2x3 | 5 | -50 |
| MT6 | RF44 'Pinpoint' Radar | 2x1x2 | 10 | -250 |
| CMP1 | Reinforced CIC | 4x1x6 | 25 | 0 |
| CMP3 | Auxiliary Steering | 3x1x3 | 10 | 0 |
| CMP4 | Rapid DC Locker | 3x1x3 | 10 | 0 |
| CMP5 | Citadel Magazine | 1x3x1 | 0 → 之后 150/座 | 0 |
| CMP6 | Damage Control Complex | 6x3x6 | 55 → 之后 4/座 | 0 |
| MOD1 | Boosted Reactor | 5x5x5 | 10 | +5000 |
| MOD2 | Sundrive Racing Pro | 5x3x5 | 20 | 0 |
| MOD5 | Ammunition Elevators | 2x2x2 | 20 | -150 |
| MOD6 | Ithaca Bridgemaster | 2x2x2 | 10 | -1200 |
| MOD7 | Ammunition Elevators | 2x2x2 | 20 | -150 |

- 合计：部件 370 点 + 舰体 200 点 = **570 点**（不含弹库与弹药，见下）
- 另有弹库 0 点 + 弹药 22 点 ⇒ **全价约 592 点**（估算；游戏里以存档原值 594 为准，单价见 `zh/弹药点数表.md`）
- 供电：发电 5000 kW / 耗电 4470 kW（余量 +530 kW）
- 弹库装载：MT5 VLS-1-46 Launcher：EA12 Chaff Decoy ×6、SGM-1 Ceremonial Arming Missile ×1；CMP5 Citadel Magazine：600mm Bomb Shell ×75、600mm HE Shell ×75、400mm Plasma Ampoule ×125、100mm Grapeshot ×250、100mm AP Shell ×250、100mm HE Shell ×500、100mm HE-HC Shell ×500


## 样板船完整装配（整艘照抄）：Open For Business（Garnet Squadron）

**整艘照抄**：舰体 `Bulk Feeder`（阵营键 `Stock/Outlying Systems Protectorate`），存档原值 **594 点**，共 16 个槽位。复制这艘船时连它自带的导弹一起抄，只改船名、呼号和导弹名。

| 槽位 | 部件 | 尺寸 | 点数 | 供电 kW |
|---|---|---|---:|---:|
| MT1 | C90 Cannon | 6x12x6 | 60 | -200 |
| MT2 | T30 Cannon | 6x3x6 | 20 | -120 |
| MT3 | T81 Plasma Cannon | 6x3x6 | 45 | -1500 |
| MT4 | VLS-1-46 Launcher | 3x2x3 | 5 | -50 |
| MT5 | J15 'Bellbird' Jammer | 3x1x3 | 50 | -850 |
| MT6 | RF44 'Pinpoint' Radar | 2x1x2 | 10 | -250 |
| CMP1 | Reinforced CIC | 4x1x6 | 25 | 0 |
| CMP3 | Auxiliary Steering | 3x1x3 | 10 | 0 |
| CMP4 | Rapid DC Locker | 3x1x3 | 10 | 0 |
| CMP5 | Citadel Magazine | 1x3x1 | 0 → 之后 150/座 | 0 |
| CMP6 | Damage Control Complex | 6x3x6 | 55 → 之后 4/座 | 0 |
| MOD1 | Boosted Reactor | 5x5x5 | 10 | +5000 |
| MOD2 | Sundrive Racing Pro | 5x3x5 | 20 | 0 |
| MOD5 | Ammunition Elevators | 2x2x2 | 20 | -150 |
| MOD6 | Ithaca Bridgemaster | 2x2x2 | 10 | -1200 |
| MOD7 | Ammunition Elevators | 2x2x2 | 20 | -150 |

- 合计：部件 370 点 + 舰体 200 点 = **570 点**（不含弹库与弹药，见下）
- 另有弹库 0 点 + 弹药 22 点 ⇒ **全价约 592 点**（估算；游戏里以存档原值 594 为准，单价见 `zh/弹药点数表.md`）
- 供电：发电 5000 kW / 耗电 4470 kW（余量 +530 kW）
- 弹库装载：MT4 VLS-1-46 Launcher：EA12 Chaff Decoy ×6、SGM-1 Ceremonial Arming Missile ×1；CMP5 Citadel Magazine：600mm Bomb Shell ×75、600mm HE Shell ×75、400mm Plasma Ampoule ×125、100mm Grapeshot ×250、100mm AP Shell ×250、100mm HE Shell ×500、100mm HE-HC Shell ×500


# TCSG BB

Tags: kind=build template; class=TCSG BB; cost=2200-3000; samples=6; good=2
Keywords: build, loadout, template, 配装, 配置, 装配, 模板, 舰级, TCSG BB
Summary: TCSG BB build; 6 matched ships, 2 of them are good samples (must and should both pass); typical cost 2635 (range 2580-2690); hull Solomon Battleship Class×2.
Section: build templates; requirements from other info/Ship Builds.txt; samples from player fleets

## How to read this
回答「这艘船算不算 / 合不合格」以 Requirements 段为准（must 全过才算这个舰级，should 是良好标准）；部件清单只统计 good 样本，频率 (k/N) 表示常见程度，不是硬性要求。所有舰船先要过通用基线（`reference/baseline-requirements.md`），再看本舰级要求。

## 舰级要求（Ship Builds.txt 原文，作为判定依据）

**舰级硬性要求（required：缺一条就不算这个舰级）**
- have at least 3 450 turrets (mount 1,2,4)
- have spyglass radar

**良好标准（should：缺了算有瑕疵，但仍算这个舰级）**
- have at least 3 Track Correlators

## Disclaimer
参考配置，不是最优解。样本是玩家舰队里 must + should 全过的真实配装（主要取自中文新手包 v1.12，对应游戏 0.6.2.3；其余来自 other info 与本地存档）。旧版本可能改过数值或改过名字；模组部件不代表原版能照抄。把它当起步模板，不要当配方。

## Numbers
- Point cost: 2200-3000 (good-sample median 2635, range 2580-2690)
- Power: draw 8625 kW / supply 7700 kW (median)
- Hull: Solomon Battleship Class×2

## Armament (good samples)
- 450 mm turret/cannon: 2/2 ships, median 4 (min 4, max 4)
- VLS-1-46 launcher: 2/2 ships
- VLS-2 launcher: 2/2 ships

## Core parts (fitted on most good samples)
- Adaptive Radar Receiver (2/2)
- Ammunition Elevators (2/2)
- CR70 Antenna (2/2)
- Citadel CIC (2/2)
- Damage Control Central (2/2)
- FM240 'Dragonfly' Drive (2/2)
- FM530 'Whiplash' Drive (2/2)
- FR4800 Reactor (2/2)
- Gun Plotting Center (2/2)
- Intelligence Center (2/2)
- Large DC Locker (2/2)
- Mk20 'Defender' PDT (2/2)
- Mk66 Cannon (2/2)
- Mk68 Cannon (2/2)
- Mount Gyros (2/2)
- RF101 'Bullseye' Radar (2/2)
- RS41 'Spyglass' Radar (2/2)
- Rapid DC Locker (2/2)
- Reinforced CIC (2/2)
- Reinforced DC Locker (2/2)
- Reinforced Magazine (2/2)
- Small Workshop (2/2)
- Track Correlator (2/2)
- VLS-1-46 Launcher (2/2)
- VLS-2 Launcher (2/2)

## Common parts (40-70%)
- -

## Optional parts
- -

## Sample ships (good)
- Glans and Burns (All 34 sample ships · Alliance, 2580 pts, player save)
- Glans and Burns (test, 2690 pts, player save)

## 样板船完整装配（整艘照抄）：Glans and Burns（All 34 sample ships · Alliance）

**整艘照抄**：舰体 `Solomon Battleship`（阵营键 `Stock/Shelter Alliance`），存档原值 **2580 点**，共 45 个槽位。复制这艘船时连它自带的导弹一起抄，只改船名、呼号和导弹名。

| 槽位 | 部件 | 尺寸 | 点数 | 供电 kW |
|---|---|---|---:|---:|
| MT1 | Mk68 Cannon | 8x5x8 | 75 | -225 |
| MT2 | Mk66 Cannon | 6x3x6 | 45 | -200 |
| MT3 | Mk68 Cannon | 8x5x8 | 75 | -225 |
| MT4 | Mk68 Cannon | 8x5x8 | 75 | -225 |
| MT5 | Mk20 'Defender' PDT | 2x1x2 | 25 | -175 |
| MT6 | VLS-2 Launcher | 3x4x3 | 10 | -200 |
| MT7 | VLS-1-46 Launcher | 3x2x3 | 5 | -50 |
| MT8 | Mk20 'Defender' PDT | 2x1x2 | 25 | -175 |
| MT9 | Mk20 'Defender' PDT | 2x1x2 | 25 | -175 |
| MT10 | VLS-1-46 Launcher | 3x2x3 | 5 | -50 |
| MT11 | VLS-2 Launcher | 3x4x3 | 10 | -200 |
| MT12 | Mk20 'Defender' PDT | 2x1x2 | 25 | -175 |
| MT13 | RF101 'Bullseye' Radar | 2x1x2 | 40 | -300 |
| MT14 | CR70 Antenna | 2x1x2 | 15 | -600 |
| CMP1 | Reinforced CIC | 4x1x6 | 25 | 0 |
| CMP2 | Intelligence Center | 6x1x8 | 90 | 0 |
| CMP3 | Small Workshop | 3x1x3 | 20 | -50 |
| CMP4 | Gun Plotting Center | 3x1x3 | 30 | 0 |
| CMP5 | Gun Plotting Center | 3x1x3 | 30 | 0 |
| CMP6 | Large DC Locker | 3x1x6 | 45 | 0 |
| CMP7 | Gun Plotting Center | 3x1x3 | 30 | 0 |
| CMP8 | Large DC Locker | 3x1x6 | 45 | 0 |
| CMP9 | Rapid DC Locker | 3x1x3 | 10 | 0 |
| CMP10 | Damage Control Central | 3x1x3 | 20 | -50 |
| CMP11 | Rapid DC Locker | 3x1x3 | 10 | 0 |
| CMP12 | Reinforced Magazine | 1x1x1 | 0 → 之后 40/座 | 0 |
| CMP13 | Large DC Locker | 3x1x6 | 45 | 0 |
| CMP14 | Reinforced Magazine | 1x1x1 | 0 → 之后 40/座 | 0 |
| CMP15 | Reinforced DC Locker | 3x1x6 | 45 | 0 |
| CMP16 | Citadel CIC | 6x1x8 | 75 | 0 |
| MOD1 | FR4800 Reactor | 5x5x5 | 10 | +4200 |
| MOD2 | FM240 'Dragonfly' Drive | 5x3x5 | 20 | 0 |
| MOD3 | FM530 'Whiplash' Drive | 10x8x10 | 30 | 0 |
| MOD4 | FM530 'Whiplash' Drive | 10x8x10 | 30 | 0 |
| MOD5 | Ammunition Elevators | 2x2x2 | 20 | -150 |
| MOD6 | Ammunition Elevators | 2x2x2 | 20 | -150 |
| MOD7 | Ammunition Elevators | 2x2x2 | 20 | -150 |
| MOD8 | Ammunition Elevators | 2x2x2 | 20 | -150 |
| MOD9 | Track Correlator | 2x2x2 | 25 | -150 |
| MOD10 | Track Correlator | 2x2x2 | 25 | -150 |
| MOD11 | Track Correlator | 2x2x2 | 25 | -150 |
| MOD12 | RS41 'Spyglass' Radar | 2x2x2 | 25 | -4000 |
| MOD13 | Track Correlator | 2x2x2 | 25 | -150 |
| MOD14 | Adaptive Radar Receiver | 2x2x2 | 30 | -200 |
| MOD15 | Mount Gyros | 2x2x2 | 20 | -150 |

- 合计：部件 1320 点 + 舰体 1000 点 = **2320 点**（不含弹库与弹药，见下）
- 另有弹库 40 点 + 弹药 220 点 ⇒ **全价约 2580 点**（估算；游戏里以存档原值 2580 为准，单价见 `zh/弹药点数表.md`）
- 供电：发电 4200 kW / 耗电 8625 kW（余量 -4425 kW）
- 弹库装载：MT6 VLS-2 Launcher：EA99 Active Decoy ×5；MT7 VLS-1-46 Launcher：EA12 Chaff Decoy ×46；MT10 VLS-1-46 Launcher：EA12 Chaff Decoy ×46；MT11 VLS-2 Launcher：EA99 Active Decoy ×5；CMP12 Reinforced Magazine：450mm HE Shell ×400、450mm AP Shell ×150、20mm Slug ×4000；CMP14 Reinforced Magazine：450mm HE Shell ×400、450mm AP Shell ×150、20mm Slug ×4000


## 样板船完整装配（整艘照抄）：Glans and Burns（test）

**整艘照抄**：舰体 `Solomon Battleship`（阵营键 `Stock/Shelter Alliance`），存档原值 **2690 点**，共 45 个槽位。复制这艘船时连它自带的导弹一起抄，只改船名、呼号和导弹名。

| 槽位 | 部件 | 尺寸 | 点数 | 供电 kW |
|---|---|---|---:|---:|
| MT1 | Mk68 Cannon | 8x5x8 | 75 | -225 |
| MT2 | Mk66 Cannon | 6x3x6 | 45 | -200 |
| MT3 | Mk68 Cannon | 8x5x8 | 75 | -225 |
| MT4 | Mk68 Cannon | 8x5x8 | 75 | -225 |
| MT5 | Mk20 'Defender' PDT | 2x1x2 | 25 | -175 |
| MT6 | VLS-2 Launcher | 3x4x3 | 10 | -200 |
| MT7 | VLS-1-46 Launcher | 3x2x3 | 5 | -50 |
| MT8 | Mk20 'Defender' PDT | 2x1x2 | 25 | -175 |
| MT9 | Mk20 'Defender' PDT | 2x1x2 | 25 | -175 |
| MT10 | VLS-1-46 Launcher | 3x2x3 | 5 | -50 |
| MT11 | VLS-2 Launcher | 3x4x3 | 10 | -200 |
| MT12 | Mk20 'Defender' PDT | 2x1x2 | 25 | -175 |
| MT13 | RF101 'Bullseye' Radar | 2x1x2 | 40 | -300 |
| MT14 | CR70 Antenna | 2x1x2 | 15 | -600 |
| CMP1 | Reinforced CIC | 4x1x6 | 25 | 0 |
| CMP2 | Intelligence Center | 6x1x8 | 90 | 0 |
| CMP3 | Small Workshop | 3x1x3 | 20 | -50 |
| CMP4 | Gun Plotting Center | 3x1x3 | 30 | 0 |
| CMP5 | Gun Plotting Center | 3x1x3 | 30 | 0 |
| CMP6 | Large DC Locker | 3x1x6 | 45 | 0 |
| CMP7 | Gun Plotting Center | 3x1x3 | 30 | 0 |
| CMP8 | Large DC Locker | 3x1x6 | 45 | 0 |
| CMP9 | Rapid DC Locker | 3x1x3 | 10 | 0 |
| CMP10 | Damage Control Central | 3x1x3 | 20 | -50 |
| CMP11 | Rapid DC Locker | 3x1x3 | 10 | 0 |
| CMP12 | Reinforced Magazine | 1x1x1 | 0 → 之后 40/座 | 0 |
| CMP13 | Large DC Locker | 3x1x6 | 45 | 0 |
| CMP14 | Reinforced Magazine | 1x1x1 | 0 → 之后 40/座 | 0 |
| CMP15 | Reinforced DC Locker | 3x1x6 | 45 | 0 |
| CMP16 | Citadel CIC | 6x1x8 | 75 | 0 |
| MOD1 | FR4800 Reactor | 5x5x5 | 10 | +4200 |
| MOD2 | FM240 'Dragonfly' Drive | 5x3x5 | 20 | 0 |
| MOD3 | FM530 'Whiplash' Drive | 10x8x10 | 30 | 0 |
| MOD4 | FM530 'Whiplash' Drive | 10x8x10 | 30 | 0 |
| MOD5 | Ammunition Elevators | 2x2x2 | 20 | -150 |
| MOD6 | Ammunition Elevators | 2x2x2 | 20 | -150 |
| MOD7 | Ammunition Elevators | 2x2x2 | 20 | -150 |
| MOD8 | Ammunition Elevators | 2x2x2 | 20 | -150 |
| MOD9 | Track Correlator | 2x2x2 | 25 | -150 |
| MOD10 | Track Correlator | 2x2x2 | 25 | -150 |
| MOD11 | Track Correlator | 2x2x2 | 25 | -150 |
| MOD12 | RS41 'Spyglass' Radar | 2x2x2 | 25 | -4000 |
| MOD13 | Track Correlator | 2x2x2 | 25 | -150 |
| MOD14 | Adaptive Radar Receiver | 2x2x2 | 30 | -200 |
| MOD15 | Mount Gyros | 2x2x2 | 20 | -150 |

- 合计：部件 1320 点 + 舰体 1000 点 = **2320 点**（不含弹库与弹药，见下）
- 另有弹库 40 点 + 弹药 330 点 ⇒ **全价约 2690 点**（估算；游戏里以存档原值 2690 为准，单价见 `zh/弹药点数表.md`）
- 供电：发电 4200 kW / 耗电 8625 kW（余量 -4425 kW）
- 弹库装载：MT6 VLS-2 Launcher：EA99 Active Decoy ×5、SDM-255 Whirlwind ×11；MT7 VLS-1-46 Launcher：EA12 Chaff Decoy ×46；MT10 VLS-1-46 Launcher：EA12 Chaff Decoy ×46；MT11 VLS-2 Launcher：EA99 Active Decoy ×5、SDM-255 Whirlwind ×11；CMP12 Reinforced Magazine：450mm HE Shell ×400、450mm AP Shell ×150、20mm Slug ×4000；CMP14 Reinforced Magazine：450mm HE Shell ×400、450mm AP Shell ×150、20mm Slug ×4000


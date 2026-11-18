# Beam BB

Tags: kind=build template; class=Beam BB; cost=1900-3000; samples=7; good=5
Keywords: build, loadout, template, 配装, 配置, 装配, 模板, 舰级, Beam BB
Summary: Beam BB build; 7 matched ships, 5 of them are good samples (must and should both pass); typical cost 2338 (range 2338-2508); hull Solomon Battleship Class×5.
Section: build templates; requirements from other info/Ship Builds.txt; samples from player fleets

## How to read this
回答「这艘船算不算 / 合不合格」以 Requirements 段为准（must 全过才算这个舰级，should 是良好标准）；部件清单只统计 good 样本，频率 (k/N) 表示常见程度，不是硬性要求。所有舰船先要过通用基线（`reference/baseline-requirements.md`），再看本舰级要求。

## 舰级要求（Ship Builds.txt 原文，作为判定依据）

**舰级硬性要求（required：缺一条就不算这个舰级）**
- have at least 2 beam turrets (mount 1,4)

**良好标准（should：缺了算有瑕疵，但仍算这个舰级）**
- have at least 3 beam turrets (mount 1,3,4)
- have good hardkill or good softkill
- have bullseye
- have good DC (at least 6 restores)
- have at least 2 CIC
- have at least 2 Drives
- have at least 2 Focused Particle Accelerator

**可选加分（optional）**
- have 1 parallax radar
- have 1 ES32 Missile ID
- have full softkill
- have a 250 turret (mount 2 only)
- have a large vls or cls(mount 2,4)
- have offensive direct missiles
- have defensive direct missiles
- have extra antenna

**避免（avoid）**
- have rail turret
- have 450 turret
- have 120 turret
- have a craft launch pad

## Disclaimer
参考配置，不是最优解。样本是玩家舰队里 must + should 全过的真实配装（主要取自中文新手包 v1.12，对应游戏 0.6.2.3；其余来自 other info 与本地存档）。旧版本可能改过数值或改过名字；模组部件不代表原版能照抄。把它当起步模板，不要当配方。

## Numbers
- Point cost: 1900-3000 (good-sample median 2338, range 2338-2508)
- Power: draw 17740 kW / supply 16700 kW (median)
- Hull: Solomon Battleship Class×5

## Armament (good samples)
- 250 mm turret/cannon: 4/5 ships, median 1 (min 1, max 1)
- VLS-1-46 launcher: 1/5 ships
- VLS-3 launcher: 1/5 ships

## Core parts (fitted on most good samples)
- CR70 Antenna (5/5)
- Damage Control Central (5/5)
- FM240 'Dragonfly' Drive (4/5)
- FM530 'Whiplash' Drive (5/5)
- FR3300 Micro Reactor (5/5)
- FR4800 Reactor (5/5)
- Focused Particle Accelerator (5/5)
- Large DC Locker (5/5)
- Mk20 'Defender' PDT (5/5)
- Mk29 'Stonewall' PDT (4/5)
- Mk610 Beam Turret (5/5)
- Mk65 Cannon (4/5)
- Mount Gyros (4/5)
- Plant Control Center (4/5)
- RF101 'Bullseye' Radar (5/5)
- RM50 'Parallax' Radar (5/5)
- Rapid DC Locker (5/5)
- Reinforced CIC (5/5)
- Reinforced DC Locker (5/5)
- Reinforced Magazine (5/5)
- Small Energy Regulator (5/5)
- Small Workshop (5/5)

## Common parts (40-70%)
- -

## Optional parts
- Auxiliary Steering (1/5)
- Bulk Magazine (1/5)
- Citadel CIC (1/5)
- E70 'Interruption' Jammer (1/5)
- ES32 'Scryer' Missile ID System (1/5)
- FM540 'Dragonfly' Drive (1/5)
- Missile Programming Bus (1/5)
- Small DC Locker (1/5)
- VLS-1-46 Launcher (1/5)
- VLS-3 Launcher (1/5)

## Sample ships (good)
- Strong the roots Dick (beme, 2338 pts, player save)
- Strong the roots Whilly (beme, 2338 pts, player save)
- Strong the roots Dick (All 34 sample ships · Alliance, 2338 pts, player save)
- Strong the roots Whilly (All 34 sample ships · Alliance, 2338 pts, player save)
- Pretty Lights (New Beam BB, 2508 pts, player save)

## 样板船完整装配（整艘照抄）：Strong the roots Dick（beme）

**整艘照抄**：舰体 `Solomon Battleship`（阵营键 `Stock/Shelter Alliance`），存档原值 **2338 点**，共 45 个槽位。复制这艘船时连它自带的导弹一起抄，只改船名、呼号和导弹名。

| 槽位 | 部件 | 尺寸 | 点数 | 供电 kW |
|---|---|---|---:|---:|
| MT1 | Mk610 Beam Turret | 8x5x8 | 80 | -3000 |
| MT2 | Mk65 Cannon | 6x3x6 | 40 | -180 |
| MT3 | Mk610 Beam Turret | 8x5x8 | 80 | -3000 |
| MT4 | Mk610 Beam Turret | 8x5x8 | 80 | -3000 |
| MT5 | Mk20 'Defender' PDT | 2x1x2 | 25 | -175 |
| MT6 | Mk29 'Stonewall' PDT | 3x1x3 | 30 | -40 |
| MT7 | Mk29 'Stonewall' PDT | 3x1x3 | 30 | -40 |
| MT8 | Mk20 'Defender' PDT | 2x1x2 | 25 | -175 |
| MT9 | Mk20 'Defender' PDT | 2x1x2 | 25 | -175 |
| MT10 | Mk29 'Stonewall' PDT | 3x1x3 | 30 | -40 |
| MT11 | Mk29 'Stonewall' PDT | 3x1x3 | 30 | -40 |
| MT12 | Mk20 'Defender' PDT | 2x1x2 | 25 | -175 |
| MT13 | RF101 'Bullseye' Radar | 2x1x2 | 40 | -300 |
| MT14 | CR70 Antenna | 2x1x2 | 15 | -600 |
| CMP1 | Reinforced CIC | 4x1x6 | 25 | 0 |
| CMP2 | Damage Control Central | 3x1x3 | 20 | -50 |
| CMP3 | Small Workshop | 3x1x3 | 20 | -50 |
| CMP4 | Plant Control Center | 3x1x3 | 25 | 0 |
| CMP5 | Large DC Locker | 3x1x6 | 45 | 0 |
| CMP6 | Large DC Locker | 3x1x6 | 45 | 0 |
| CMP7 | Large DC Locker | 3x1x6 | 45 | 0 |
| CMP8 | Plant Control Center | 3x1x3 | 25 | 0 |
| CMP9 | Rapid DC Locker | 3x1x3 | 10 | 0 |
| CMP10 | Rapid DC Locker | 3x1x3 | 10 | 0 |
| CMP11 | Rapid DC Locker | 3x1x3 | 10 | 0 |
| CMP12 | Reinforced Magazine | 1x1x1 | 0 → 之后 40/座 | 0 |
| CMP13 | Large DC Locker | 3x1x6 | 45 | 0 |
| CMP14 | Reinforced Magazine | 1x1x1 | 0 → 之后 40/座 | 0 |
| CMP15 | Reinforced CIC | 4x1x6 | 25 | 0 |
| CMP16 | Reinforced DC Locker | 3x1x6 | 45 | 0 |
| MOD1 | FR4800 Reactor | 5x5x5 | 10 | +4200 |
| MOD2 | FM240 'Dragonfly' Drive | 5x3x5 | 20 | 0 |
| MOD3 | FM530 'Whiplash' Drive | 10x8x10 | 30 | 0 |
| MOD4 | FM530 'Whiplash' Drive | 10x8x10 | 30 | 0 |
| MOD5 | FR3300 Micro Reactor | 3x3x3 | 10 | +2250 |
| MOD6 | FR3300 Micro Reactor | 3x3x3 | 10 | +2250 |
| MOD7 | FR3300 Micro Reactor | 3x3x3 | 10 | +2250 |
| MOD8 | FR3300 Micro Reactor | 3x3x3 | 10 | +2250 |
| MOD9 | Focused Particle Accelerator | 3x3x3 | 25 | -800 |
| MOD10 | Focused Particle Accelerator | 3x3x3 | 25 | -800 |
| MOD11 | Focused Particle Accelerator | 3x3x3 | 25 | -800 |
| MOD12 | RM50 'Parallax' Radar | 2x2x2 | 45 | -3600 |
| MOD13 | Mount Gyros | 2x2x2 | 20 | -150 |
| MOD14 | Small Energy Regulator | 2x2x2 | 20 | -400 |
| MOD15 | Mount Gyros | 2x2x2 | 20 | -150 |

- 合计：部件 1260 点 + 舰体 1000 点 = **2260 点**（不含弹库与弹药，见下）
- 另有弹库 40 点 + 弹药 33 点 ⇒ **全价约 2333 点**（估算；游戏里以存档原值 2338 为准，单价见 `zh/弹药点数表.md`）
- 供电：发电 13200 kW / 耗电 17740 kW（余量 -4540 kW）
- 弹库装载：CMP12 Reinforced Magazine：20mm Slug ×12000、250mm AP Shell ×50、250mm HE-RPF Shell ×50、250mm HE Shell ×50、Flak Round ×750；CMP14 Reinforced Magazine：20mm Slug ×12000、250mm AP Shell ×50、250mm HE-RPF Shell ×50、250mm HE Shell ×50、Flak Round ×750


## 样板船完整装配（整艘照抄）：Strong the roots Whilly（beme）

**整艘照抄**：舰体 `Solomon Battleship`（阵营键 `Stock/Shelter Alliance`），存档原值 **2338 点**，共 45 个槽位。复制这艘船时连它自带的导弹一起抄，只改船名、呼号和导弹名。

| 槽位 | 部件 | 尺寸 | 点数 | 供电 kW |
|---|---|---|---:|---:|
| MT1 | Mk610 Beam Turret | 8x5x8 | 80 | -3000 |
| MT2 | Mk65 Cannon | 6x3x6 | 40 | -180 |
| MT3 | Mk610 Beam Turret | 8x5x8 | 80 | -3000 |
| MT4 | Mk610 Beam Turret | 8x5x8 | 80 | -3000 |
| MT5 | Mk20 'Defender' PDT | 2x1x2 | 25 | -175 |
| MT6 | Mk29 'Stonewall' PDT | 3x1x3 | 30 | -40 |
| MT7 | Mk29 'Stonewall' PDT | 3x1x3 | 30 | -40 |
| MT8 | Mk20 'Defender' PDT | 2x1x2 | 25 | -175 |
| MT9 | Mk20 'Defender' PDT | 2x1x2 | 25 | -175 |
| MT10 | Mk29 'Stonewall' PDT | 3x1x3 | 30 | -40 |
| MT11 | Mk29 'Stonewall' PDT | 3x1x3 | 30 | -40 |
| MT12 | Mk20 'Defender' PDT | 2x1x2 | 25 | -175 |
| MT13 | RF101 'Bullseye' Radar | 2x1x2 | 40 | -300 |
| MT14 | CR70 Antenna | 2x1x2 | 15 | -600 |
| CMP1 | Reinforced CIC | 4x1x6 | 25 | 0 |
| CMP2 | Damage Control Central | 3x1x3 | 20 | -50 |
| CMP3 | Small Workshop | 3x1x3 | 20 | -50 |
| CMP4 | Plant Control Center | 3x1x3 | 25 | 0 |
| CMP5 | Large DC Locker | 3x1x6 | 45 | 0 |
| CMP6 | Large DC Locker | 3x1x6 | 45 | 0 |
| CMP7 | Large DC Locker | 3x1x6 | 45 | 0 |
| CMP8 | Plant Control Center | 3x1x3 | 25 | 0 |
| CMP9 | Rapid DC Locker | 3x1x3 | 10 | 0 |
| CMP10 | Rapid DC Locker | 3x1x3 | 10 | 0 |
| CMP11 | Rapid DC Locker | 3x1x3 | 10 | 0 |
| CMP12 | Reinforced Magazine | 1x1x1 | 0 → 之后 40/座 | 0 |
| CMP13 | Large DC Locker | 3x1x6 | 45 | 0 |
| CMP14 | Reinforced Magazine | 1x1x1 | 0 → 之后 40/座 | 0 |
| CMP15 | Reinforced CIC | 4x1x6 | 25 | 0 |
| CMP16 | Reinforced DC Locker | 3x1x6 | 45 | 0 |
| MOD1 | FR4800 Reactor | 5x5x5 | 10 | +4200 |
| MOD2 | FM240 'Dragonfly' Drive | 5x3x5 | 20 | 0 |
| MOD3 | FM530 'Whiplash' Drive | 10x8x10 | 30 | 0 |
| MOD4 | FM530 'Whiplash' Drive | 10x8x10 | 30 | 0 |
| MOD5 | FR3300 Micro Reactor | 3x3x3 | 10 | +2250 |
| MOD6 | FR3300 Micro Reactor | 3x3x3 | 10 | +2250 |
| MOD7 | FR3300 Micro Reactor | 3x3x3 | 10 | +2250 |
| MOD8 | FR3300 Micro Reactor | 3x3x3 | 10 | +2250 |
| MOD9 | Focused Particle Accelerator | 3x3x3 | 25 | -800 |
| MOD10 | Focused Particle Accelerator | 3x3x3 | 25 | -800 |
| MOD11 | Focused Particle Accelerator | 3x3x3 | 25 | -800 |
| MOD12 | RM50 'Parallax' Radar | 2x2x2 | 45 | -3600 |
| MOD13 | Mount Gyros | 2x2x2 | 20 | -150 |
| MOD14 | Small Energy Regulator | 2x2x2 | 20 | -400 |
| MOD15 | Mount Gyros | 2x2x2 | 20 | -150 |

- 合计：部件 1260 点 + 舰体 1000 点 = **2260 点**（不含弹库与弹药，见下）
- 另有弹库 40 点 + 弹药 33 点 ⇒ **全价约 2333 点**（估算；游戏里以存档原值 2338 为准，单价见 `zh/弹药点数表.md`）
- 供电：发电 13200 kW / 耗电 17740 kW（余量 -4540 kW）
- 弹库装载：CMP12 Reinforced Magazine：20mm Slug ×12000、250mm AP Shell ×50、250mm HE-RPF Shell ×50、250mm HE Shell ×50、Flak Round ×750；CMP14 Reinforced Magazine：20mm Slug ×12000、250mm AP Shell ×50、250mm HE-RPF Shell ×50、250mm HE Shell ×50、Flak Round ×750


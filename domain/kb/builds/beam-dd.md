# Beam DD

Tags: kind=build template; class=Beam DD; cost=400-800; samples=93; good=43
Keywords: build, loadout, template, 配装, 配置, 装配, 模板, 舰级, Beam DD
Summary: Beam DD build; 93 matched ships, 43 of them are good samples (must and should both pass); typical cost 735 (range 635-796); hull Keystone Destroyer Class×43.
Section: build templates; requirements from other info/Ship Builds.txt; samples from player fleets

## How to read this
回答「这艘船算不算 / 合不合格」以 Requirements 段为准（must 全过才算这个舰级，should 是良好标准）；部件清单只统计 good 样本，频率 (k/N) 表示常见程度，不是硬性要求。所有舰船先要过通用基线（`reference/baseline-requirements.md`），再看本舰级要求。

## 舰级要求（Ship Builds.txt 原文，作为判定依据）

**舰级硬性要求（required：缺一条就不算这个舰级）**
- have 1 Mk600 beam as spinal weapon (mount 7)

**良好标准（should：缺了算有瑕疵，但仍算这个舰级）**
- have bullseye
- have minimal DC (at least 2 restores)
- have at least 1 Focused Particle Accelerator
- have minimal softkill
- have minimal hardkill

**可选加分（optional）**
- have better DC (at least 3 restores)
- have at least 2 Focused Particle Accelerators
- have at least 1 Aurora PDT
- have 1  vls-3 or cls-3 launchers
- ^have offensive S3 missiles
- have 1 blanket jammer

## Disclaimer
参考配置，不是最优解。样本是玩家舰队里 must + should 全过的真实配装（主要取自中文新手包 v1.12，对应游戏 0.6.2.3；其余来自 other info 与本地存档）。旧版本可能改过数值或改过名字；模组部件不代表原版能照抄。把它当起步模板，不要当配方。

## Numbers
- Point cost: 400-800 (good-sample median 735, range 635-796)
- Power: draw 8650 kW / supply 6950 kW (median)
- Hull: Keystone Destroyer Class×43

## Armament (good samples)
- 120 mm turret/cannon: 16/43 ships, median 1 (min 1, max 2)
- VLS-1-23 launcher: 36/43 ships
- VLS-1-46 launcher: 7/43 ships

## Core parts (fitted on most good samples)
- E90 'Blanket' Jammer (31/43)
- FM240 'Dragonfly' Drive (33/43)
- FR3300 Micro Reactor (42/43)
- FR4800 Reactor (36/43)
- Focused Particle Accelerator (42/43)
- Mk20 'Defender' PDT (38/43)
- Mk600 Beam Cannon (42/43)
- RF101 'Bullseye' Radar (43/43)
- RS35 'Frontline' Radar (40/43)
- Rapid DC Locker (42/43)
- Reinforced CIC (36/43)
- Reinforced Magazine (43/43)
- VLS-1-23 Launcher (35/43)

## Common parts (40-70%)
- ES32 'Scryer' Missile ID System (30/43)
- Large DC Locker (29/43)
- Reinforced DC Locker (29/43)

## Optional parts
- Mk62 Cannon (16/43)
- Small DC Locker (14/43)
- Auxiliary Steering (9/43)
- FM230 'Whiplash' Drive (9/43)
- Basic CIC (7/43)
- FM280 'Raider' Drive (7/43)
- VLS-1-46 Launcher (7/43)
- Mk90 'Aurora' PDT (5/43)
- Mount Gyros (2/43)
- RM50 'Parallax' Radar (2/43)
- Ammunition Elevators (1/43)
- CR70 Antenna (1/43)

## Sample ships (good)
- Beyond Conventional (TF Willow, 675 pts, example fleet)
- Word Cadence (TF Willow, 675 pts, example fleet)
- Basal Reflex (TF Willow, 675 pts, example fleet)
- Crash (All Craft Are Bastards, 635 pts, player save)
- Bad Teens (mixed cap, 635 pts, player save)
- D-1080 (Assult Group Sigma, 640 pts, player save)

## 样板船完整装配（整艘照抄）：Beyond Conventional（TF Willow）

**整艘照抄**：舰体 `Keystone Destroyer`（阵营键 `Stock/Shelter Alliance`），存档原值 **675 点**，共 19 个槽位。复制这艘船时连它自带的导弹一起抄，只改船名、呼号和导弹名。

| 槽位 | 部件 | 尺寸 | 点数 | 供电 kW |
|---|---|---|---:|---:|
| MT1 | VLS-1-46 Launcher | 3x2x3 | 5 | -50 |
| MT3 | Mk90 'Aurora' PDT | 2x1x2 | 55 | -1250 |
| MT4 | Mk90 'Aurora' PDT | 2x1x2 | 55 | -1250 |
| MT5 | RF101 'Bullseye' Radar | 2x1x2 | 40 | -300 |
| MT6 | E90 'Blanket' Jammer | 2x1x2 | 50 | -1000 |
| MT7 | Mk600 Beam Cannon | — | 75 | -3000 |
| CMP1 | Rapid DC Locker | 3x1x3 | 10 | 0 |
| CMP2 | Basic CIC | 4x1x6 | 10 | 0 |
| CMP3 | Small DC Locker | 3x1x3 | 20 | 0 |
| CMP4 | Small DC Locker | 3x1x3 | 20 | 0 |
| CMP5 | Rapid DC Locker | 3x1x3 | 10 | 0 |
| CMP6 | Reinforced Magazine | 1x1x1 | 0 → 之后 40/座 | 0 |
| CMP7 | Basic CIC | 4x1x6 | 10 | 0 |
| MOD1 | FR4800 Reactor | 5x5x5 | 10 | +4200 |
| MOD2 | FM280 'Raider' Drive | 5x3x5 | 20 | 0 |
| MOD3 | FR3300 Micro Reactor | 3x3x3 | 10 | +2250 |
| MOD4 | Focused Particle Accelerator | 3x3x3 | 25 | -800 |
| MOD6 | RS35 'Frontline' Radar | 2x2x2 | 10 | -2000 |
| MOD7 | Focused Particle Accelerator | 3x3x3 | 25 | -800 |

- 合计：部件 460 点 + 舰体 200 点 = **660 点**（不含弹库与弹药，见下）
- 另有弹库 0 点 + 弹药 15 点 ⇒ **全价约 675 点**（估算；游戏里以存档原值 675 为准，单价见 `zh/弹药点数表.md`）
- 供电：发电 6450 kW / 耗电 10450 kW（余量 -4000 kW）
- 弹库装载：MT1 VLS-1-46 Launcher：EA12 Chaff Decoy ×11、EA20 Flare Decoy ×3、SGM-1 Ceremonial Arming Missile ×1


## 样板船完整装配（整艘照抄）：Word Cadence（TF Willow）

**整艘照抄**：舰体 `Keystone Destroyer`（阵营键 `Stock/Shelter Alliance`），存档原值 **675 点**，共 19 个槽位。复制这艘船时连它自带的导弹一起抄，只改船名、呼号和导弹名。

| 槽位 | 部件 | 尺寸 | 点数 | 供电 kW |
|---|---|---|---:|---:|
| MT1 | VLS-1-46 Launcher | 3x2x3 | 5 | -50 |
| MT3 | Mk90 'Aurora' PDT | 2x1x2 | 55 | -1250 |
| MT4 | Mk90 'Aurora' PDT | 2x1x2 | 55 | -1250 |
| MT5 | RF101 'Bullseye' Radar | 2x1x2 | 40 | -300 |
| MT6 | E90 'Blanket' Jammer | 2x1x2 | 50 | -1000 |
| MT7 | Mk600 Beam Cannon | — | 75 | -3000 |
| CMP1 | Rapid DC Locker | 3x1x3 | 10 | 0 |
| CMP2 | Basic CIC | 4x1x6 | 10 | 0 |
| CMP3 | Small DC Locker | 3x1x3 | 20 | 0 |
| CMP4 | Small DC Locker | 3x1x3 | 20 | 0 |
| CMP5 | Rapid DC Locker | 3x1x3 | 10 | 0 |
| CMP6 | Reinforced Magazine | 1x1x1 | 0 → 之后 40/座 | 0 |
| CMP7 | Basic CIC | 4x1x6 | 10 | 0 |
| MOD1 | FR4800 Reactor | 5x5x5 | 10 | +4200 |
| MOD2 | FM280 'Raider' Drive | 5x3x5 | 20 | 0 |
| MOD3 | FR3300 Micro Reactor | 3x3x3 | 10 | +2250 |
| MOD4 | Focused Particle Accelerator | 3x3x3 | 25 | -800 |
| MOD6 | RS35 'Frontline' Radar | 2x2x2 | 10 | -2000 |
| MOD7 | Focused Particle Accelerator | 3x3x3 | 25 | -800 |

- 合计：部件 460 点 + 舰体 200 点 = **660 点**（不含弹库与弹药，见下）
- 另有弹库 0 点 + 弹药 15 点 ⇒ **全价约 675 点**（估算；游戏里以存档原值 675 为准，单价见 `zh/弹药点数表.md`）
- 供电：发电 6450 kW / 耗电 10450 kW（余量 -4000 kW）
- 弹库装载：MT1 VLS-1-46 Launcher：EA12 Chaff Decoy ×11、EA20 Flare Decoy ×3、SGM-1 Ceremonial Arming Missile ×1


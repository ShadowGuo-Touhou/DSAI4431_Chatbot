# support tug

Tags: kind=build template; class=support tug; cost=250-400; samples=12; good=11
Keywords: build, loadout, template, 配装, 配置, 装配, 模板, 舰级, support tug
Summary: support tug build; 12 matched ships, 11 of them are good samples (must and should both pass); typical cost 386 (range 365-400); hull Draugr Clipper Class×11.
Section: build templates; requirements from other info/Ship Builds.txt; samples from player fleets

## How to read this
回答「这艘船算不算 / 合不合格」以 Requirements 段为准（must 全过才算这个舰级，should 是良好标准）；部件清单只统计 good 样本，频率 (k/N) 表示常见程度，不是硬性要求。所有舰船先要过通用基线（`reference/baseline-requirements.md`），再看本舰级要求。

## 舰级要求（Ship Builds.txt 原文，作为判定依据）

**舰级硬性要求（required：缺一条就不算这个舰级）**
- have at least 1 jammer and/or illuminator

**良好标准（should：缺了算有瑕疵，但仍算这个舰级）**
- have minimal DC (at least 1 rapid DC)
- have minimal softkill

**可选加分（optional）**
- have at least 2 jammer and/or illuminator
- have minimal hardkill
- have good softkill

## Disclaimer
参考配置，不是最优解。样本是玩家舰队里 must + should 全过的真实配装（主要取自中文新手包 v1.12，对应游戏 0.6.2.3；其余来自 other info 与本地存档）。旧版本可能改过数值或改过名字；模组部件不代表原版能照抄。把它当起步模板，不要当配方。

## Numbers
- Point cost: 250-400 (good-sample median 386, range 365-400)
- Power: draw 3700 kW / supply 3950 kW (median)
- Hull: Draugr Clipper Class×11

## Armament (good samples)
- 250 mm turret/cannon: 3/11 ships, median 1 (min 1, max 1)
- 100 mm turret/cannon: 2/11 ships, median 1 (min 1, max 1)
- VLS-1-23 launcher: 3/11 ships
- MLS launcher: 2/11 ships

## Core parts (fitted on most good samples)
- Basic CIC (8/11)
- Civilian Reactor (10/11)
- Rapid DC Locker (11/11)

## Common parts (40-70%)
- Actively Cooled Amplifiers (5/11)
- Auxiliary Steering (5/11)
- BW800 Drive (5/11)
- BW800-R Drive (5/11)
- E20 'Lighthouse' Illuminator (5/11)
- J15 'Bellbird' Jammer (7/11)
- J75 'Warbler' Jammer (5/11)
- L50 'Blackjack' Laser Dazzler (6/11)
- RF44 'Pinpoint' Radar (5/11)
- Reinforced Magazine (6/11)
- Small DC Locker (5/11)
- Small Workshop (5/11)

## Optional parts
- Ammunition Elevators (3/11)
- C53 Cannon (3/11)
- Reinforced CIC (3/11)
- T20 Cannon (3/11)
- Adaptive Radar Receiver (2/11)
- Bulwark Huntress (2/11)
- C30 Cannon (2/11)
- MLS-3 Launcher (2/11)
- VLS-1-23 Launcher (2/11)
- Boosted Reactor (1/11)
- CHI-777 Yard Drive (1/11)
- Large DC Locker (1/11)

## Sample ships (good)
- TBD (tug blob, 373 pts, example fleet)
- TBD (tug blob, 373 pts, example fleet)
- TBD (tug blob, 374 pts, example fleet)
- 不冲击 (大冲击, 395 pts, example fleet)
- 不冲击 (大冲击, 395 pts, example fleet)
- 不冲击 (大冲击, 400 pts, example fleet)

## 样板船完整装配（整艘照抄）：不冲击（大冲击）

**整艘照抄**：舰体 `Tugboat`（阵营键 `Stock/Outlying Systems Protectorate`），存档原值 **400 点**，共 14 个槽位。复制这艘船时连它自带的导弹一起抄，只改船名、呼号和导弹名。

| 槽位 | 部件 | 尺寸 | 点数 | 供电 kW |
|---|---|---|---:|---:|
| MT1 | L50 'Blackjack' Laser Dazzler | 2x1x2 | 40 | -750 |
| MT2 | J75 'Warbler' Jammer | 3x1x3 | 50 | -500 |
| MT3 | J15 'Bellbird' Jammer | 3x1x3 | 50 | -850 |
| MT4 | E20 'Lighthouse' Illuminator | 2x1x2 | 15 | -600 |
| MT5 | E20 'Lighthouse' Illuminator | 2x1x2 | 15 | -600 |
| CMP1 | Basic CIC | 4x1x6 | 10 | 0 |
| CMP2 | Rapid DC Locker | 3x1x3 | 10 | 0 |
| CMP3 | Rapid DC Locker | 3x1x3 | 10 | 0 |
| CMP4 | Small Workshop | 3x1x3 | 20 | -50 |
| CMP5 | Rapid DC Locker | 3x1x3 | 10 | 0 |
| MOD1 | BW800 Drive | 5x3x5 | 10 | 0 |
| MOD2 | Civilian Reactor ⚠ 槽只有 8×3×6 | 5x5x5 | 10 | +3650 |
| MOD3 | Actively Cooled Amplifiers | 2x2x2 | 25 | -175 |
| MOD4 | Actively Cooled Amplifiers | 2x2x2 | 25 | -175 |

- 合计：部件 300 点 + 舰体 100 点 = **400 点**（不含弹库与弹药，见下）
- 供电：发电 3650 kW / 耗电 3700 kW（余量 -50 kW）
- ⚠ 存档里这几个槽装的东西比槽位大（旧版本留下的，当前版本装不进去）：MOD2 Civilian Reactor（5x5x5）塞不进 8×3×6。照抄时换小一号的部件，或改用同功能的小件。


## 样板船完整装配（整艘照抄）：不冲击（大冲击）

**整艘照抄**：舰体 `Tugboat`（阵营键 `Stock/Outlying Systems Protectorate`），存档原值 **400 点**，共 14 个槽位。复制这艘船时连它自带的导弹一起抄，只改船名、呼号和导弹名。

| 槽位 | 部件 | 尺寸 | 点数 | 供电 kW |
|---|---|---|---:|---:|
| MT1 | L50 'Blackjack' Laser Dazzler | 2x1x2 | 40 | -750 |
| MT2 | J75 'Warbler' Jammer | 3x1x3 | 50 | -500 |
| MT3 | J15 'Bellbird' Jammer | 3x1x3 | 50 | -850 |
| MT4 | E20 'Lighthouse' Illuminator | 2x1x2 | 15 | -600 |
| MT5 | E20 'Lighthouse' Illuminator | 2x1x2 | 15 | -600 |
| CMP1 | Basic CIC | 4x1x6 | 10 | 0 |
| CMP2 | Rapid DC Locker | 3x1x3 | 10 | 0 |
| CMP3 | Rapid DC Locker | 3x1x3 | 10 | 0 |
| CMP4 | Small Workshop | 3x1x3 | 20 | -50 |
| CMP5 | Rapid DC Locker | 3x1x3 | 10 | 0 |
| MOD1 | BW800 Drive | 5x3x5 | 10 | 0 |
| MOD2 | Civilian Reactor ⚠ 槽只有 8×3×6 | 5x5x5 | 10 | +3650 |
| MOD3 | Actively Cooled Amplifiers | 2x2x2 | 25 | -175 |
| MOD4 | Actively Cooled Amplifiers | 2x2x2 | 25 | -175 |

- 合计：部件 300 点 + 舰体 100 点 = **400 点**（不含弹库与弹药，见下）
- 供电：发电 3650 kW / 耗电 3700 kW（余量 -50 kW）
- ⚠ 存档里这几个槽装的东西比槽位大（旧版本留下的，当前版本装不进去）：MOD2 Civilian Reactor（5x5x5）塞不进 8×3×6。照抄时换小一号的部件，或改用同功能的小件。


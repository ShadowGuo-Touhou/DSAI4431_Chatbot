# Rail CC

Tags: kind=build template; class=Rail CC; cost=1200-1600; samples=6; good=2
Keywords: build, loadout, template, 配装, 配置, 装配, 模板, 舰级, Rail CC
Summary: Rail CC build; 6 matched ships, 2 of them are good samples (must and should both pass); typical cost 1554 (range 1529-1579); hull Ocello Command Cruiser Class×2.
Section: build templates; requirements from other info/Ship Builds.txt; samples from player fleets

## How to read this
回答「这艘船算不算 / 合不合格」以 Requirements 段为准（must 全过才算这个舰级，should 是良好标准）；部件清单只统计 good 样本，频率 (k/N) 表示常见程度，不是硬性要求。所有舰船先要过通用基线（`reference/baseline-requirements.md`），再看本舰级要求。

## 舰级要求（Ship Builds.txt 原文，作为判定依据）

**舰级硬性要求（required：缺一条就不算这个舰级）**
- have at least 2 rail turrets (mount 1-3)

**良好标准（should：缺了算有瑕疵，但仍算这个舰级）**
- have 3rail turrets
- have good hardkill or good softkill
- have bullseye
- have minimal DC (at least 2 restores)
- have at least 3 energy regulators or small energy regulators

**可选加分（optional）**
- have 1 parallax radar or spyglass radar
- have Track Correlator if using spyglass radar
- have 1 ES32 Missile ID
- have at least 2 CIC
- have good softkill
- have 2 Sarissa PDT
- have 2 aurora PDT
- have at least 2 Drives
- have 1 floodlight illuminator

**避免（avoid）**
- have a craft launch pad
- have non-rail turret
- have OSP equipment when better ANS alternative is available

## Disclaimer
参考配置，不是最优解。样本是玩家舰队里 must + should 全过的真实配装（主要取自中文新手包 v1.12，对应游戏 0.6.2.3；其余来自 other info 与本地存档）。旧版本可能改过数值或改过名字；模组部件不代表原版能照抄。把它当起步模板，不要当配方。

## Numbers
- Point cost: 1200-1600 (good-sample median 1554, range 1529-1579)
- Power: draw 19100 kW / supply 14400 kW (median)
- Hull: Ocello Command Cruiser Class×2

## Armament (good samples)
- 300 mm turret/cannon: 2/2 ships, median 3 (min 3, max 3)
- VLS-1-46 launcher: 2/2 ships

## Core parts (fitted on most good samples)
- E90 'Blanket' Jammer (2/2)
- ES32 'Scryer' Missile ID System (2/2)
- Energy Regulator (2/2)
- FM530 'Whiplash' Drive (2/2)
- FR3300 Micro Reactor (2/2)
- FR4800 Reactor (2/2)
- Gun Plotting Center (2/2)
- Large DC Locker (2/2)
- Mk81 Railgun (2/2)
- Mk90 'Aurora' PDT (2/2)
- Mk95 'Sarissa' PDT (2/2)
- Plant Control Center (2/2)
- R550 Early Warning Radar (2/2)
- RF101 'Bullseye' Radar (2/2)
- RS35 'Frontline' Radar (2/2)
- Rapid DC Locker (2/2)
- Reinforced CIC (2/2)
- Reinforced Magazine (2/2)
- Small DC Locker (2/2)
- Small Energy Regulator (2/2)
- VLS-1-46 Launcher (2/2)

## Common parts (40-70%)
- -

## Optional parts
- -

## Sample ships (good)
- Hoshimachi (Comet Squadron, 1529 pts, player save)
- Hoshimachi (All 27 sample ships · Protectorate, 1579 pts, player save)

## 样板船完整装配（整艘照抄）：Hoshimachi（Comet Squadron）

**整艘照抄**：舰体 `Ocello Cruiser`（阵营键 `Stock/Outlying Systems Protectorate`），存档原值 **1529 点**，共 30 个槽位。复制这艘船时连它自带的导弹一起抄，只改船名、呼号和导弹名。

| 槽位 | 部件 | 尺寸 | 点数 | 供电 kW |
|---|---|---|---:|---:|
| MT1 | Mk81 Railgun | 6x3x6 | 75 | -1500 |
| MT2 | Mk81 Railgun | 6x3x6 | 75 | -1500 |
| MT3 | Mk81 Railgun | 6x3x6 | 75 | -1500 |
| MT4 | Mk95 'Sarissa' PDT | 3x1x3 | 65 | -1250 |
| MT5 | Mk95 'Sarissa' PDT | 3x1x3 | 65 | -1250 |
| MT6 | VLS-1-46 Launcher | 3x2x3 | 5 | -50 |
| MT7 | R550 Early Warning Radar | 3x1x3 | 40 | -4500 |
| MT8 | E90 'Blanket' Jammer | 2x1x2 | 50 | -1000 |
| MT9 | RF101 'Bullseye' Radar | 2x1x2 | 40 | -300 |
| MT10 | Mk90 'Aurora' PDT | 2x1x2 | 55 | -1250 |
| MT11 | Mk90 'Aurora' PDT | 2x1x2 | 55 | -1250 |
| CMP1 | Large DC Locker | 3x1x6 | 45 | 0 |
| CMP2 | Reinforced CIC | 4x1x6 | 25 | 0 |
| CMP3 | Rapid DC Locker | 3x1x3 | 10 | 0 |
| CMP4 | Gun Plotting Center | 3x1x3 | 30 | 0 |
| CMP5 | Gun Plotting Center | 3x1x3 | 30 | 0 |
| CMP6 | Small DC Locker | 3x1x3 | 20 | 0 |
| CMP7 | Reinforced Magazine | 1x1x1 | 0 → 之后 40/座 | 0 |
| CMP8 | Plant Control Center | 3x1x3 | 25 | 0 |
| CMP9 | Gun Plotting Center | 3x1x3 | 30 | 0 |
| MOD1 | FR4800 Reactor | 5x5x5 | 10 | +4200 |
| MOD2 | FR4800 Reactor | 5x5x5 | 10 | +4200 |
| MOD3 | FM530 'Whiplash' Drive | 10x8x10 | 30 | 0 |
| MOD4 | FR3300 Micro Reactor | 3x3x3 | 10 | +2250 |
| MOD5 | FR3300 Micro Reactor | 3x3x3 | 10 | +2250 |
| MOD6 | Energy Regulator | 3x3x3 | 30 | -650 |
| MOD7 | RS35 'Frontline' Radar | 2x2x2 | 10 | -2000 |
| MOD8 | ES32 'Scryer' Missile ID System | 2x2x2 | 10 | -300 |
| MOD9 | Small Energy Regulator | 2x2x2 | 20 | -400 |
| MOD10 | Small Energy Regulator | 2x2x2 | 20 | -400 |

- 合计：部件 975 点 + 舰体 575 点 = **1550 点**（不含弹库与弹药，见下）
- 另有弹库 0 点 + 弹药 29 点 ⇒ **全价约 1579 点**（估算；游戏里以存档原值 1529 为准，单价见 `zh/弹药点数表.md`）
- 供电：发电 12900 kW / 耗电 19100 kW（余量 -6200 kW）
- 弹库装载：MT6 VLS-1-46 Launcher：EA12 Chaff Decoy ×10；CMP7 Reinforced Magazine：300mm AP Rail Sabot ×400、15mm Sandshot ×150


## 样板船完整装配（整艘照抄）：Hoshimachi（All 27 sample ships · Protectorate）

**整艘照抄**：舰体 `Ocello Cruiser`（阵营键 `Stock/Outlying Systems Protectorate`），存档原值 **1579 点**，共 30 个槽位。复制这艘船时连它自带的导弹一起抄，只改船名、呼号和导弹名。

| 槽位 | 部件 | 尺寸 | 点数 | 供电 kW |
|---|---|---|---:|---:|
| MT1 | Mk81 Railgun | 6x3x6 | 75 | -1500 |
| MT2 | Mk81 Railgun | 6x3x6 | 75 | -1500 |
| MT3 | Mk81 Railgun | 6x3x6 | 75 | -1500 |
| MT4 | Mk95 'Sarissa' PDT | 3x1x3 | 65 | -1250 |
| MT5 | Mk95 'Sarissa' PDT | 3x1x3 | 65 | -1250 |
| MT6 | VLS-1-46 Launcher | 3x2x3 | 5 | -50 |
| MT7 | R550 Early Warning Radar | 3x1x3 | 40 | -4500 |
| MT8 | E90 'Blanket' Jammer | 2x1x2 | 50 | -1000 |
| MT9 | RF101 'Bullseye' Radar | 2x1x2 | 40 | -300 |
| MT10 | Mk90 'Aurora' PDT | 2x1x2 | 55 | -1250 |
| MT11 | Mk90 'Aurora' PDT | 2x1x2 | 55 | -1250 |
| CMP1 | Large DC Locker | 3x1x6 | 45 | 0 |
| CMP2 | Reinforced CIC | 4x1x6 | 25 | 0 |
| CMP3 | Rapid DC Locker | 3x1x3 | 10 | 0 |
| CMP4 | Gun Plotting Center | 3x1x3 | 30 | 0 |
| CMP5 | Gun Plotting Center | 3x1x3 | 30 | 0 |
| CMP6 | Small DC Locker | 3x1x3 | 20 | 0 |
| CMP7 | Reinforced Magazine | 1x1x1 | 0 → 之后 40/座 | 0 |
| CMP8 | Plant Control Center | 3x1x3 | 25 | 0 |
| CMP9 | Gun Plotting Center | 3x1x3 | 30 | 0 |
| MOD1 | FR4800 Reactor | 5x5x5 | 10 | +4200 |
| MOD2 | FR4800 Reactor | 5x5x5 | 10 | +4200 |
| MOD3 | FM530 'Whiplash' Drive | 10x8x10 | 30 | 0 |
| MOD4 | FR3300 Micro Reactor | 3x3x3 | 10 | +2250 |
| MOD5 | FR3300 Micro Reactor | 3x3x3 | 10 | +2250 |
| MOD6 | Energy Regulator | 3x3x3 | 30 | -650 |
| MOD7 | RS35 'Frontline' Radar | 2x2x2 | 10 | -2000 |
| MOD8 | ES32 'Scryer' Missile ID System | 2x2x2 | 10 | -300 |
| MOD9 | Small Energy Regulator | 2x2x2 | 20 | -400 |
| MOD10 | Small Energy Regulator | 2x2x2 | 20 | -400 |

- 合计：部件 975 点 + 舰体 575 点 = **1550 点**（不含弹库与弹药，见下）
- 另有弹库 0 点 + 弹药 29 点 ⇒ **全价约 1579 点**（估算；游戏里以存档原值 1579 为准，单价见 `zh/弹药点数表.md`）
- 供电：发电 12900 kW / 耗电 19100 kW（余量 -6200 kW）
- 弹库装载：MT6 VLS-1-46 Launcher：EA12 Chaff Decoy ×10；CMP7 Reinforced Magazine：300mm AP Rail Sabot ×400、15mm Sandshot ×150


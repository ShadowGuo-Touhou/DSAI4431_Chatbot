# missle FF

Tags: kind=build template; class=missle FF; cost=750-1000; samples=5; good=3
Keywords: build, loadout, template, 配装, 配置, 装配, 模板, 舰级, missle FF
Summary: missle FF build; 5 matched ships, 3 of them are good samples (must and should both pass); typical cost 1000 (range 1000-1000); hull Raines Frigate Class×3.
Section: build templates; requirements from other info/Ship Builds.txt; samples from player fleets

## How to read this
回答「这艘船算不算 / 合不合格」以 Requirements 段为准（must 全过才算这个舰级，should 是良好标准）；部件清单只统计 good 样本，频率 (k/N) 表示常见程度，不是硬性要求。所有舰船先要过通用基线（`reference/baseline-requirements.md`），再看本舰级要求。

## 舰级要求（Ship Builds.txt 原文，作为判定依据）

**舰级硬性要求（required：缺一条就不算这个舰级）**
- have at least 2 vls-2, vls-3 or cls-3 launchers
- have >400 points of offensive missiles

**良好标准（should：缺了算有瑕疵，但仍算这个舰级）**
- have >700 points of offensive missiles
- have minimal DC (1 rapid DC Locker)
- have minimal softkill
- have at least 1 Missile Programming Bus/ Missile Programming Bus Array

**可选加分（optional）**
- have better DC (at least 1 restore)
- have 1 reinforced CIC
- have at least 2 Missile Programming Bus/ Missile Programming Bus Array
- have 1 spyglass radar

## Disclaimer
参考配置，不是最优解。样本是玩家舰队里 must + should 全过的真实配装（主要取自中文新手包 v1.12，对应游戏 0.6.2.3；其余来自 other info 与本地存档）。旧版本可能改过数值或改过名字；模组部件不代表原版能照抄。把它当起步模板，不要当配方。

## Numbers
- Point cost: 750-1000 (good-sample median 1000, range 1000-1000)
- Power: draw 3000 kW / supply 4700 kW (median)
- Hull: Raines Frigate Class×3

## Armament (good samples)
- VLS-1-46 launcher: 3/3 ships
- VLS-2 launcher: 3/3 ships

## Core parts (fitted on most good samples)
- Basic CIC (3/3)
- FM200 Drive (3/3)
- FR4800 Reactor (3/3)
- Missile Programming Bus Array (3/3)
- RS35 'Frontline' Radar (3/3)
- Rapid DC Locker (3/3)
- Reinforced Magazine (3/3)
- VLS-1-46 Launcher (3/3)
- VLS-2 Launcher (3/3)

## Common parts (40-70%)
- -

## Optional parts
- -

## Sample ships (good)
- Read (zpzd 导弹FF, 1000 pts, player save)
- Toady (zpzd 导弹FF, 1000 pts, player save)
- Bling (zpzd 导弹FF, 1000 pts, player save)

## 样板船完整装配（整艘照抄）：Read（zpzd 导弹FF）

**整艘照抄**：舰体 `Raines Frigate`（阵营键 `Stock/Shelter Alliance`），存档原值 **1000 点**，共 11 个槽位。复制这艘船时连它自带的导弹一起抄，只改船名、呼号和导弹名。

| 槽位 | 部件 | 尺寸 | 点数 | 供电 kW |
|---|---|---|---:|---:|
| MT1 | VLS-1-46 Launcher | 3x2x3 | 5 | -50 |
| MT2 | VLS-2 Launcher | 3x4x3 | 10 | -200 |
| MT3 | VLS-2 Launcher | 3x4x3 | 10 | -200 |
| MT4 | VLS-2 Launcher | 3x4x3 | 10 | -200 |
| CMP1 | Basic CIC | 4x1x6 | 10 | 0 |
| CMP2 | Reinforced Magazine | 1x1x1 | 0 → 之后 40/座 | 0 |
| CMP4 | Rapid DC Locker | 3x1x3 | 10 | 0 |
| MOD1 | FR4800 Reactor | 5x5x5 | 10 | +4200 |
| MOD2 | FM200 Drive | 5x3x5 | 10 | 0 |
| MOD3 | RS35 'Frontline' Radar | 2x2x2 | 10 | -2000 |
| MOD5 | Missile Programming Bus Array | 3x3x3 | 50 | -350 |

- 合计：部件 135 点 + 舰体 125 点 = **260 点**（不含弹库与弹药，见下）
- 另有弹库 0 点 + 弹药 740 点 ⇒ **全价约 1000 点**（估算；游戏里以存档原值 1000 为准，单价见 `zh/弹药点数表.md`）
- 供电：发电 4200 kW / 耗电 3000 kW（余量 +1200 kW）
- 弹库装载：MT1 VLS-1-46 Launcher：SGM-100 占点 ×1、EA12 Chaff Decoy ×11、SGM-100 AMM ×26；MT2 VLS-2 Launcher：SGM-200 补刀 ×12、SGM-200 反小v1 ×4；MT3 VLS-2 Launcher：SGM-H-200 zpzd002 雷达 ×12、SGM-H-200 zpzd002 尾焰 ×12；MT4 VLS-2 Launcher：SGM-H-200 zpzd002 尾焰 ×24


## 样板船完整装配（整艘照抄）：Toady（zpzd 导弹FF）

**整艘照抄**：舰体 `Raines Frigate`（阵营键 `Stock/Shelter Alliance`），存档原值 **1000 点**，共 11 个槽位。复制这艘船时连它自带的导弹一起抄，只改船名、呼号和导弹名。

| 槽位 | 部件 | 尺寸 | 点数 | 供电 kW |
|---|---|---|---:|---:|
| MT1 | VLS-1-46 Launcher | 3x2x3 | 5 | -50 |
| MT2 | VLS-2 Launcher | 3x4x3 | 10 | -200 |
| MT3 | VLS-2 Launcher | 3x4x3 | 10 | -200 |
| MT4 | VLS-2 Launcher | 3x4x3 | 10 | -200 |
| CMP1 | Basic CIC | 4x1x6 | 10 | 0 |
| CMP2 | Reinforced Magazine | 1x1x1 | 0 → 之后 40/座 | 0 |
| CMP4 | Rapid DC Locker | 3x1x3 | 10 | 0 |
| MOD1 | FR4800 Reactor | 5x5x5 | 10 | +4200 |
| MOD2 | FM200 Drive | 5x3x5 | 10 | 0 |
| MOD3 | RS35 'Frontline' Radar | 2x2x2 | 10 | -2000 |
| MOD5 | Missile Programming Bus Array | 3x3x3 | 50 | -350 |

- 合计：部件 135 点 + 舰体 125 点 = **260 点**（不含弹库与弹药，见下）
- 另有弹库 0 点 + 弹药 740 点 ⇒ **全价约 1000 点**（估算；游戏里以存档原值 1000 为准，单价见 `zh/弹药点数表.md`）
- 供电：发电 4200 kW / 耗电 3000 kW（余量 +1200 kW）
- 弹库装载：MT1 VLS-1-46 Launcher：SGM-100 占点 ×1、EA12 Chaff Decoy ×11、SGM-100 AMM ×26；MT2 VLS-2 Launcher：SGM-200 补刀 ×12、SGM-200 反小v1 ×4；MT3 VLS-2 Launcher：SGM-H-200 zpzd002 雷达 ×12、SGM-H-200 zpzd002 尾焰 ×12；MT4 VLS-2 Launcher：SGM-H-200 zpzd002 尾焰 ×24


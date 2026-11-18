# multi mission tug (mmt)

Tags: kind=build template; class=multi mission tug (mmt); cost=400-500; samples=6; good=6
Keywords: build, loadout, template, 配装, 配置, 装配, 模板, 舰级, multi mission tug (mmt)
Summary: multi mission tug (mmt) build; 6 matched ships, 6 of them are good samples (must and should both pass); typical cost 452 (range 432-453); hull Draugr Clipper Class×6.
Section: build templates; requirements from other info/Ship Builds.txt; samples from player fleets

## How to read this
回答「这艘船算不算 / 合不合格」以 Requirements 段为准（must 全过才算这个舰级，should 是良好标准）；部件清单只统计 good 样本，频率 (k/N) 表示常见程度，不是硬性要求。所有舰船先要过通用基线（`reference/baseline-requirements.md`），再看本舰级要求。

## 舰级要求（Ship Builds.txt 原文，作为判定依据）

**舰级硬性要求（required：缺一条就不算这个舰级）**
- have 1 mls launcher
- have >20 points of direct offensive missiles

**良好标准（should：缺了算有瑕疵，但仍算这个舰级）**
- have >50 points of direct offensive missiles

## Disclaimer
参考配置，不是最优解。样本是玩家舰队里 must + should 全过的真实配装（主要取自中文新手包 v1.12，对应游戏 0.6.2.3；其余来自 other info 与本地存档）。旧版本可能改过数值或改过名字；模组部件不代表原版能照抄。把它当起步模板，不要当配方。

## Numbers
- Point cost: 400-500 (good-sample median 452, range 432-453)
- Power: draw 3400 kW / supply 3950 kW (median)
- Hull: Draugr Clipper Class×6

## Armament (good samples)
- 100 mm turret/cannon: 6/6 ships, median 1 (min 1, max 1)
- 250 mm turret/cannon: 2/6 ships, median 1 (min 1, max 1)
- MLS launcher: 6/6 ships
- VLS-1-23 launcher: 4/6 ships

## Core parts (fitted on most good samples)
- BW800-R Drive (6/6)
- Reinforced Magazine (5/6)
- Small DC Locker (6/6)

## Common parts (40-70%)
- Adaptive Radar Receiver (3/6)
- Auxiliary Steering (4/6)
- Basic CIC (3/6)
- Bulk Magazine (3/6)
- Bulwark Huntress (4/6)
- C30 Cannon (4/6)
- Civilian Reactor (4/6)
- J15 'Bellbird' Jammer (4/6)
- MLS-2 Launcher (3/6)
- MLS-3 Launcher (3/6)
- RF44 'Pinpoint' Radar (4/6)
- Rapid DC Locker (3/6)
- Reinforced CIC (3/6)
- VLS-1-23 Launcher (4/6)

## Optional parts
- Ammunition Elevators (2/6)
- Boosted Reactor (2/6)
- C53 Cannon (2/6)
- Ithaca Bridgemaster (2/6)
- P20 'Bastion' PDT (2/6)
- P60 'Grazer' PDT (2/6)
- T20 Cannon (2/6)

## Sample ships (good)
- 大冲击二型 (大冲击, 432 pts, example fleet)
- 大冲击二型 (大冲击, 436 pts, example fleet)
- Ranger (Tantalum Squadron, 452 pts, example fleet)
- Bailiff (Tantalum Squadron, 452 pts, example fleet)
- Custodian (Tantalum Squadron, 452 pts, example fleet)
- Amphorateuthis (Heteroteuthinae, 453 pts, player save)

## 样板船完整装配（整艘照抄）：Ranger（Tantalum Squadron）

**整艘照抄**：舰体 `Tugboat`（阵营键 `Stock/Outlying Systems Protectorate`），存档原值 **452 点**，共 14 个槽位。复制这艘船时连它自带的导弹一起抄，只改船名、呼号和导弹名。

| 槽位 | 部件 | 尺寸 | 点数 | 供电 kW |
|---|---|---|---:|---:|
| MT1 | C30 Cannon | 2x5x2 | 20 | -100 |
| MT2 | MLS-3 Launcher | 2x2x5 | 15 | -50 |
| MT3 | J15 'Bellbird' Jammer | 3x1x3 | 50 | -850 |
| MT4 | VLS-1-23 Launcher | 2x2x2 | 5 | -50 |
| MT5 | RF44 'Pinpoint' Radar | 2x1x2 | 10 | -250 |
| CMP1 | Reinforced CIC | 4x1x6 | 25 | 0 |
| CMP2 | Reinforced Magazine | 1x1x1 | 0 → 之后 40/座 | 0 |
| CMP3 | Auxiliary Steering | 3x1x3 | 10 | 0 |
| CMP4 | Small DC Locker | 3x1x3 | 20 | 0 |
| CMP5 | Rapid DC Locker | 3x1x3 | 10 | 0 |
| MOD1 | BW800-R Drive | 5x3x5 | 20 | 0 |
| MOD2 | Civilian Reactor ⚠ 槽只有 8×3×6 | 5x5x5 | 10 | +3650 |
| MOD3 | Bulwark Huntress | 2x2x2 | 30 | -2000 |
| MOD4 | Adaptive Radar Receiver | 2x2x2 | 30 | -200 |

- 合计：部件 255 点 + 舰体 100 点 = **355 点**（不含弹库与弹药，见下）
- 另有弹库 0 点 + 弹药 97 点 ⇒ **全价约 452 点**（估算；游戏里以存档原值 452 为准，单价见 `zh/弹药点数表.md`）
- 供电：发电 3650 kW / 耗电 3500 kW（余量 +150 kW）
- 弹库装载：MT4 VLS-1-23 Launcher：EA12 Chaff Decoy ×7、SGM-126 Counter-Time ×1、SGM-102 Reprise ×7；CMP2 Reinforced Magazine：100mm Grapeshot ×250、100mm AP Shell ×250、100mm HE Shell ×250、QUoBzVIvJUWTBgd_xJznwQ ×4、YF_tfrjLd0O64Rmftg9hOg ×2
- ⚠ 存档里这几个槽装的东西比槽位大（旧版本留下的，当前版本装不进去）：MOD2 Civilian Reactor（5x5x5）塞不进 8×3×6。照抄时换小一号的部件，或改用同功能的小件。


## 样板船完整装配（整艘照抄）：Bailiff（Tantalum Squadron）

**整艘照抄**：舰体 `Tugboat`（阵营键 `Stock/Outlying Systems Protectorate`），存档原值 **452 点**，共 14 个槽位。复制这艘船时连它自带的导弹一起抄，只改船名、呼号和导弹名。

| 槽位 | 部件 | 尺寸 | 点数 | 供电 kW |
|---|---|---|---:|---:|
| MT1 | C30 Cannon | 2x5x2 | 20 | -100 |
| MT2 | MLS-3 Launcher | 2x2x5 | 15 | -50 |
| MT3 | J15 'Bellbird' Jammer | 3x1x3 | 50 | -850 |
| MT4 | VLS-1-23 Launcher | 2x2x2 | 5 | -50 |
| MT5 | RF44 'Pinpoint' Radar | 2x1x2 | 10 | -250 |
| CMP1 | Reinforced CIC | 4x1x6 | 25 | 0 |
| CMP2 | Reinforced Magazine | 1x1x1 | 0 → 之后 40/座 | 0 |
| CMP3 | Auxiliary Steering | 3x1x3 | 10 | 0 |
| CMP4 | Small DC Locker | 3x1x3 | 20 | 0 |
| CMP5 | Rapid DC Locker | 3x1x3 | 10 | 0 |
| MOD1 | BW800-R Drive | 5x3x5 | 20 | 0 |
| MOD2 | Civilian Reactor ⚠ 槽只有 8×3×6 | 5x5x5 | 10 | +3650 |
| MOD3 | Bulwark Huntress | 2x2x2 | 30 | -2000 |
| MOD4 | Adaptive Radar Receiver | 2x2x2 | 30 | -200 |

- 合计：部件 255 点 + 舰体 100 点 = **355 点**（不含弹库与弹药，见下）
- 另有弹库 0 点 + 弹药 97 点 ⇒ **全价约 452 点**（估算；游戏里以存档原值 452 为准，单价见 `zh/弹药点数表.md`）
- 供电：发电 3650 kW / 耗电 3500 kW（余量 +150 kW）
- 弹库装载：MT4 VLS-1-23 Launcher：EA12 Chaff Decoy ×7、SGM-126 Counter-Time ×1、SGM-102 Reprise ×7；CMP2 Reinforced Magazine：100mm Grapeshot ×250、100mm AP Shell ×250、100mm HE Shell ×250、QUoBzVIvJUWTBgd_xJznwQ ×4、YF_tfrjLd0O64Rmftg9hOg ×2
- ⚠ 存档里这几个槽装的东西比槽位大（旧版本留下的，当前版本装不进去）：MOD2 Civilian Reactor（5x5x5）塞不进 8×3×6。照抄时换小一号的部件，或改用同功能的小件。


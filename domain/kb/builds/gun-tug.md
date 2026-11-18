# gun tug

Tags: kind=build template; class=gun tug; cost=250-400; samples=23; good=6
Keywords: build, loadout, template, 配装, 配置, 装配, 模板, 舰级, gun tug
Summary: gun tug build; 23 matched ships, 6 of them are good samples (must and should both pass); typical cost 369 (range 320-374); hull Draugr Clipper Class×6.
Section: build templates; requirements from other info/Ship Builds.txt; samples from player fleets

## How to read this
回答「这艘船算不算 / 合不合格」以 Requirements 段为准（must 全过才算这个舰级，should 是良好标准）；部件清单只统计 good 样本，频率 (k/N) 表示常见程度，不是硬性要求。所有舰船先要过通用基线（`reference/baseline-requirements.md`），再看本舰级要求。

## 舰级要求（Ship Builds.txt 原文，作为判定依据）

**舰级硬性要求（required：缺一条就不算这个舰级）**
- have at least 1 cannon or turret

**良好标准（should：缺了算有瑕疵，但仍算这个舰级）**
- have minimal softkill
- have a reinforced CIC
- have a reinforced Magazine
- have minimal DC (at least 1 restore)
- have 2 CIC and/or Auxiliary Steering

**可选加分（optional）**
- have pinpoint
- have a bellbird jammer
- have huntress radar
- have adaptive radar receiver

## Disclaimer
参考配置，不是最优解。样本是玩家舰队里 must + should 全过的真实配装（主要取自中文新手包 v1.12，对应游戏 0.6.2.3；其余来自 other info 与本地存档）。旧版本可能改过数值或改过名字；模组部件不代表原版能照抄。把它当起步模板，不要当配方。

## Numbers
- Point cost: 250-400 (good-sample median 369, range 320-374)
- Power: draw 3488 kW / supply 3950 kW (median)
- Hull: Draugr Clipper Class×6

## Armament (good samples)
- 250 mm turret/cannon: 4/6 ships, median 1 (min 1, max 1)
- 100 mm turret/cannon: 2/6 ships, median 1 (min 1, max 1)
- VLS-1-23 launcher: 4/6 ships
- MLS launcher: 3/6 ships

## Core parts (fitted on most good samples)
- Auxiliary Steering (6/6)
- BW800-R Drive (5/6)
- Civilian Reactor (6/6)
- RF44 'Pinpoint' Radar (6/6)
- Rapid DC Locker (5/6)
- Reinforced Magazine (6/6)
- Small DC Locker (6/6)

## Common parts (40-70%)
- Ammunition Elevators (3/6)
- Basic CIC (3/6)
- Bulwark Huntress (3/6)
- C53 Cannon (4/6)
- MLS-3 Launcher (3/6)
- Reinforced CIC (3/6)
- T20 Cannon (3/6)
- VLS-1-23 Launcher (3/6)

## Optional parts
- Adaptive Radar Receiver (2/6)
- C30 Cannon (2/6)
- J15 'Bellbird' Jammer (2/6)
- ES32 'Scryer' Missile ID System (1/6)
- P11 'Pavise' PDT (1/6)
- Reinforced DC Locker (1/6)
- Sundrive Racing Pro (1/6)

## Sample ships (good)
- TBD (tug blob, 373 pts, example fleet)
- TBD (tug blob, 373 pts, example fleet)
- TBD (tug blob, 374 pts, example fleet)
- Maker (tesdt, 320 pts, player save)
- Bailiff (All 27 sample ships · Protectorate, 365 pts, player save)
- Ranger (All 27 sample ships · Protectorate, 365 pts, player save)

## 样板船完整装配（整艘照抄）：TBD（tug blob）

**整艘照抄**：舰体 `Tugboat`（阵营键 `Stock/Outlying Systems Protectorate`），存档原值 **280 点**，共 13 个槽位。复制这艘船时连它自带的导弹一起抄，只改船名、呼号和导弹名。

| 槽位 | 部件 | 尺寸 | 点数 | 供电 kW |
|---|---|---|---:|---:|
| MT1 | C53 Cannon | 2x4x2 | 10 | -100 |
| MT2 | T20 Cannon | 3x1x3 | 15 | -30 |
| MT3 | T20 Cannon | 3x1x3 | 15 | -30 |
| MT4 | RF44 'Pinpoint' Radar | 2x1x2 | 10 | -250 |
| CMP1 | Auxiliary Steering | 3x1x3 | 10 | 0 |
| CMP2 | Basic CIC | 4x1x6 | 10 | 0 |
| CMP3 | Rapid DC Locker | 3x1x3 | 10 | 0 |
| CMP4 | Small DC Locker | 3x1x3 | 20 | 0 |
| CMP5 | Reinforced Magazine | 1x1x1 | 0 → 之后 40/座 | 0 |
| MOD1 | BW800-R Drive | 5x3x5 | 20 | 0 |
| MOD2 | Civilian Reactor ⚠ 槽只有 8×3×6 | 5x5x5 | 10 | +3650 |
| MOD3 | Ammunition Elevators | 2x2x2 | 20 | -150 |
| MOD4 | Ammunition Elevators | 2x2x2 | 20 | -150 |

- 合计：部件 170 点 + 舰体 100 点 = **270 点**（不含弹库与弹药，见下）
- 另有弹库 0 点 + 弹药 10 点 ⇒ **全价约 280 点**（估算；游戏里以存档原值 280 为准，单价见 `zh/弹药点数表.md`）
- 供电：发电 3650 kW / 耗电 710 kW（余量 +2940 kW）
- 弹库装载：CMP5 Reinforced Magazine：250mm HE Shell ×100、250mm Bomb Shell ×100、250mm AP Shell ×100、100mm Grapeshot ×500、100mm HE Shell ×250、100mm AP Shell ×250
- ⚠ 存档里这几个槽装的东西比槽位大（旧版本留下的，当前版本装不进去）：MOD2 Civilian Reactor（5x5x5）塞不进 8×3×6。照抄时换小一号的部件，或改用同功能的小件。


## 样板船完整装配（整艘照抄）：TBD（tug blob）

**整艘照抄**：舰体 `Tugboat`（阵营键 `Stock/Outlying Systems Protectorate`），存档原值 **280 点**，共 13 个槽位。复制这艘船时连它自带的导弹一起抄，只改船名、呼号和导弹名。

| 槽位 | 部件 | 尺寸 | 点数 | 供电 kW |
|---|---|---|---:|---:|
| MT1 | C53 Cannon | 2x4x2 | 10 | -100 |
| MT2 | T20 Cannon | 3x1x3 | 15 | -30 |
| MT3 | T20 Cannon | 3x1x3 | 15 | -30 |
| MT4 | RF44 'Pinpoint' Radar | 2x1x2 | 10 | -250 |
| CMP1 | Auxiliary Steering | 3x1x3 | 10 | 0 |
| CMP2 | Basic CIC | 4x1x6 | 10 | 0 |
| CMP3 | Rapid DC Locker | 3x1x3 | 10 | 0 |
| CMP4 | Small DC Locker | 3x1x3 | 20 | 0 |
| CMP5 | Reinforced Magazine | 1x1x1 | 0 → 之后 40/座 | 0 |
| MOD1 | BW800-R Drive | 5x3x5 | 20 | 0 |
| MOD2 | Civilian Reactor ⚠ 槽只有 8×3×6 | 5x5x5 | 10 | +3650 |
| MOD3 | Ammunition Elevators | 2x2x2 | 20 | -150 |
| MOD4 | Ammunition Elevators | 2x2x2 | 20 | -150 |

- 合计：部件 170 点 + 舰体 100 点 = **270 点**（不含弹库与弹药，见下）
- 另有弹库 0 点 + 弹药 10 点 ⇒ **全价约 280 点**（估算；游戏里以存档原值 280 为准，单价见 `zh/弹药点数表.md`）
- 供电：发电 3650 kW / 耗电 710 kW（余量 +2940 kW）
- 弹库装载：CMP5 Reinforced Magazine：250mm HE Shell ×100、250mm Bomb Shell ×100、250mm AP Shell ×100、100mm Grapeshot ×500、100mm HE Shell ×250、100mm AP Shell ×250
- ⚠ 存档里这几个槽装的东西比槽位大（旧版本留下的，当前版本装不进去）：MOD2 Civilian Reactor（5x5x5）塞不进 8×3×6。照抄时换小一号的部件，或改用同功能的小件。


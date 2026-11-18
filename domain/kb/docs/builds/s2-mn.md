# S2 MN

Tags: kind=build template; class=S2 MN; cost=800-1500; samples=2; good=1
Keywords: build, loadout, template, 配装, 配置, 装配, 模板, 舰级, S2 MN
Summary: S2 MN build; 2 matched ships, 1 of them are good samples (must and should both pass); typical cost 969 (range 969-969); hull Flathead Monitor Class×1.
Section: build templates; requirements from other info/Ship Builds.txt; samples from player fleets

## How to read this
回答「这艘船算不算 / 合不合格」以 Requirements 段为准（must 全过才算这个舰级，should 是良好标准）；部件清单只统计 good 样本，频率 (k/N) 表示常见程度，不是硬性要求。所有舰船先要过通用基线（`reference/baseline-requirements.md`），再看本舰级要求。

## 舰级要求（Ship Builds.txt 原文，作为判定依据）

**舰级硬性要求（required：缺一条就不算这个舰级）**
- have at least 2 mls launchers
- have >500 points of offensive missiles

**良好标准（should：缺了算有瑕疵，但仍算这个舰级）**
- have at least 4 mls launchers
- all mls launchers are of the same type
- all offensive missiles should be cruise guidance
- have minimal DC (at least 1 restore)
- have minimal softkill

**可选加分（optional）**
- have 5 mls
- have better DC (at least 2 restores)
- have ammo elevators
- have 2 ammo storage

## Disclaimer
参考配置，不是最优解。样本是玩家舰队里 must + should 全过的真实配装（主要取自中文新手包 v1.12，对应游戏 0.6.2.3；其余来自 other info 与本地存档）。旧版本可能改过数值或改过名字；模组部件不代表原版能照抄。把它当起步模板，不要当配方。

## Numbers
- Point cost: 800-1500 (good-sample median 969, range 969-969)
- Power: draw 1500 kW / supply 3850 kW (median)
- Hull: Flathead Monitor Class×1

## Armament (good samples)
- MLS launcher: 1/1 ships
- VLS-1-23 launcher: 1/1 ships

## Core parts (fitted on most good samples)
- Basic CIC (1/1)
- Bulk Magazine (1/1)
- Civilian Reactor (1/1)
- Ithaca Bridgemaster (1/1)
- MLS-2 Launcher (1/1)
- Rapid DC Locker (1/1)
- Small DC Locker (1/1)
- Sundrive Racing Pro (1/1)
- VLS-1-23 Launcher (1/1)

## Common parts (40-70%)
- -

## Optional parts
- -

## Sample ships (good)
- Time Dilation (Tantalum Squadron, 969 pts, example fleet)

## 样板船完整装配（整艘照抄）：Time Dilation（Tantalum Squadron）

**整艘照抄**：舰体 `Bulk Feeder`（阵营键 `Stock/Outlying Systems Protectorate`），存档原值 **969 点**，共 13 个槽位。复制这艘船时连它自带的导弹一起抄，只改船名、呼号和导弹名。

| 槽位 | 部件 | 尺寸 | 点数 | 供电 kW |
|---|---|---|---:|---:|
| MT1 | MLS-2 Launcher | 2x2x5 | 15 | -50 |
| MT2 | MLS-2 Launcher | 2x2x5 | 15 | -50 |
| MT3 | MLS-2 Launcher | 2x2x5 | 15 | -50 |
| MT4 | MLS-2 Launcher | 2x2x5 | 15 | -50 |
| MT5 | MLS-2 Launcher | 2x2x5 | 15 | -50 |
| MT6 | VLS-1-23 Launcher | 2x2x2 | 5 | -50 |
| CMP1 | Basic CIC | 4x1x6 | 10 | 0 |
| CMP2 | Bulk Magazine | 1x1x1 | 0 → 之后 20/座 | 0 |
| CMP3 | Rapid DC Locker | 3x1x3 | 10 | 0 |
| CMP4 | Small DC Locker | 3x1x3 | 20 | 0 |
| MOD1 | Sundrive Racing Pro | 5x3x5 | 20 | 0 |
| MOD2 | Civilian Reactor | 5x5x5 | 10 | +3650 |
| MOD3 | Ithaca Bridgemaster | 2x2x2 | 10 | -1200 |

- 合计：部件 160 点 + 舰体 200 点 = **360 点**（不含弹库与弹药，见下）
- 另有弹库 0 点 + 弹药 609 点 ⇒ **全价约 969 点**（估算；游戏里以存档原值 969 为准，单价见 `zh/弹药点数表.md`）
- 供电：发电 3650 kW / 耗电 1500 kW（余量 +2150 kW）
- 弹库装载：MT6 VLS-1-23 Launcher：EA12 Chaff Decoy ×8、SGM-126 Counter-Time ×1；CMP2 Bulk Magazine：SGM-220 Fleche ×100


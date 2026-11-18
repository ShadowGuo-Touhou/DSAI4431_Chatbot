# missle ln

Tags: kind=build template; class=missle ln; cost=1400-3000; samples=14; good=3
Keywords: build, loadout, template, 配装, 配置, 装配, 模板, 舰级, missle ln
Summary: missle ln build; 14 matched ships, 3 of them are good samples (must and should both pass); typical cost 3000 (range 3000-3000); hull Marauder Line Ship Class×3.
Section: build templates; requirements from other info/Ship Builds.txt; samples from player fleets

## How to read this
回答「这艘船算不算 / 合不合格」以 Requirements 段为准（must 全过才算这个舰级，should 是良好标准）；部件清单只统计 good 样本，频率 (k/N) 表示常见程度，不是硬性要求。所有舰船先要过通用基线（`reference/baseline-requirements.md`），再看本舰级要求。

## 舰级要求（Ship Builds.txt 原文，作为判定依据）

**舰级硬性要求（required：缺一条就不算这个舰级）**
- have at least 4 mls launchers in main mounts (mount 1-8)
- have >400 points of offensive missiles

**良好标准（should：缺了算有瑕疵，但仍算这个舰级）**
- have exactly 8 mls launchers in main mounts (mount 1-8)
- all mls launchers are of the same type
- have >1300 points of offensive missiles
- have minimal DC (at least 2 restores)
- have minimal softkill

**可选加分（optional）**
- have >1800 points of offensive missiles
- have at least 2 ammo elevators
- have good softkill
- have T20 cannon
- have at least 2 CIC

**避免（avoid）**
- have different type of mls
- have anything other than mls in main mounts (mount 1-8)

## Disclaimer
参考配置，不是最优解。样本是玩家舰队里 must + should 全过的真实配装（主要取自中文新手包 v1.12，对应游戏 0.6.2.3；其余来自 other info 与本地存档）。旧版本可能改过数值或改过名字；模组部件不代表原版能照抄。把它当起步模板，不要当配方。

## Numbers
- Point cost: 1400-3000 (good-sample median 3000, range 3000-3000)
- Power: draw 2460 kW / supply 3950 kW (median)
- Hull: Marauder Line Ship Class×3

## Armament (good samples)
- 100 mm turret/cannon: 2/3 ships, median 3 (min 2, max 4)
- MLS launcher: 3/3 ships
- VLS-1-46 launcher: 2/3 ships
- VLS-1-23 launcher: 1/3 ships

## Core parts (fitted on most good samples)
- Bulk Magazine (3/3)
- Civilian Reactor (3/3)
- Ithaca Bridgemaster (3/3)
- MLS-2 Launcher (3/3)
- Reinforced CIC (3/3)

## Common parts (40-70%)
- Basic CIC (2/3)
- CHI-9100 Long Haul Drive (2/3)
- Large DC Storage (2/3)
- P11 'Pavise' PDT (2/3)
- Reinforced DC Locker (2/3)
- T20 Cannon (2/3)
- VLS-1-46 Launcher (2/3)

## Optional parts
- Ammunition Elevators (1/3)
- BW1500 Drive (1/3)
- Damage Control Complex (1/3)
- L50 'Blackjack' Laser Dazzler (1/3)
- VLS-1-23 Launcher (1/3)

## Sample ships (good)
- Life Goes On (Life Goes On LNG, 3000 pts, player save)
- Blot Out The Sun With Our Arrows (cmd test2, 3000 pts, player save)
- Blot Out The Sun With Our Arrows (S2LN NEO, 3000 pts, player save)

## 样板船完整装配（整艘照抄）：Life Goes On（Life Goes On LNG）

**整艘照抄**：舰体 `Bulk Hauler`（阵营键 `Stock/Outlying Systems Protectorate`），存档原值 **3000 点**，共 24 个槽位。复制这艘船时连它自带的导弹一起抄，只改船名、呼号和导弹名。

| 槽位 | 部件 | 尺寸 | 点数 | 供电 kW |
|---|---|---|---:|---:|
| Bow·MT1 | MLS-2 Launcher | 2x2x5 | 15 | -50 |
| Bow·MT2 | MLS-2 Launcher | 2x2x5 | 15 | -50 |
| Bow·MT3 | MLS-2 Launcher | 2x2x5 | 15 | -50 |
| Bow·MT4 | MLS-2 Launcher | 2x2x5 | 15 | -50 |
| Core·MT5 | MLS-2 Launcher | 2x2x5 | 15 | -50 |
| Core·MT6 | MLS-2 Launcher | 2x2x5 | 15 | -50 |
| Core·MT7 | MLS-2 Launcher | 2x2x5 | 15 | -50 |
| Core·MT8 | MLS-2 Launcher | 2x2x5 | 15 | -50 |
| Bow·MT9 | T20 Cannon | 3x1x3 | 15 | -30 |
| Bow·MT10 | L50 'Blackjack' Laser Dazzler | 2x1x2 | 40 | -750 |
| Core·MT11 | T20 Cannon | 3x1x3 | 15 | -30 |
| Core·MT12 | VLS-1-46 Launcher | 3x2x3 | 5 | -50 |
| Stern·MT14 | T20 Cannon | 3x1x3 | 15 | -30 |
| Stern·MT15 | T20 Cannon | 3x1x3 | 15 | -30 |
| Bow·MT16 | P11 'Pavise' PDT | 2x1x2 | 20 | -150 |
| Bow·MT17 | P11 'Pavise' PDT | 2x1x2 | 20 | -150 |
| Bow·CMP2 | Bulk Magazine | 1x1x1 | 0 → 之后 20/座 | 0 |
| Core·CMP2 | Reinforced CIC | 4x1x6 | 25 | 0 |
| Core·CMP4 | Damage Control Complex | 6x3x6 | 55 → 之后 4/座 | 0 |
| Core·CMP5 | Bulk Magazine | 1x1x1 | 0 → 之后 20/座 | 0 |
| Core·CMP6 | Bulk Magazine | 1x1x1 | 0 → 之后 20/座 | 0 |
| Stern·MOD1 | Civilian Reactor | 5x5x5 | 10 | +3650 |
| Stern·MOD2 | BW1500 Drive | 12x12x12 | 10 | 0 |
| Bow·MOD3 | Ithaca Bridgemaster | 2x2x2 | 10 | -1200 |

- 合计：部件 375 点 + 舰体 375 点 = **750 点**（不含弹库与弹药，见下）
- 另有弹库 40 点 + 弹药 2210 点 ⇒ **全价约 3000 点**（估算；游戏里以存档原值 3000 为准，单价见 `zh/弹药点数表.md`）
- 供电：发电 3650 kW / 耗电 2820 kW（余量 +830 kW）
- 弹库装载：Core·MT12 VLS-1-46 Launcher：EA12 Chaff Decoy ×13、-c3RhRHJCUO3HnO0aoQS8A ×1；Bow·CMP2 Bulk Magazine：K-VS6QY7D0yGvnDzmnckTw ×68、ULjvAhVu5ke0ip-8ISpGiA ×32、oJsNOtEhIUWDtMx2PzqVZg ×32、100mm HE Shell ×250、100mm Grapeshot ×250、20mm Slug ×8000；Core·CMP5 Bulk Magazine：K-VS6QY7D0yGvnDzmnckTw ×68、ULjvAhVu5ke0ip-8ISpGiA ×32、oJsNOtEhIUWDtMx2PzqVZg ×32、100mm HE Shell ×250、100mm Grapeshot ×250、20mm Slug ×8000；Core·CMP6 Bulk Magazine：K-VS6QY7D0yGvnDzmnckTw ×24、ULjvAhVu5ke0ip-8ISpGiA ×8、oJsNOtEhIUWDtMx2PzqVZg ×8


## 样板船完整装配（整艘照抄）：Blot Out The Sun With Our Arrows（cmd test2）

**整艘照抄**：舰体 `Bulk Hauler`（阵营键 `Stock/Outlying Systems Protectorate`），存档原值 **3000 点**，共 18 个槽位。复制这艘船时连它自带的导弹一起抄，只改船名、呼号和导弹名。

| 槽位 | 部件 | 尺寸 | 点数 | 供电 kW |
|---|---|---|---:|---:|
| Bow·MT1 | MLS-2 Launcher | 2x2x5 | 15 | -50 |
| Bow·MT2 | MLS-2 Launcher | 2x2x5 | 15 | -50 |
| Bow·MT3 | MLS-2 Launcher | 2x2x5 | 15 | -50 |
| Bow·MT4 | MLS-2 Launcher | 2x2x5 | 15 | -50 |
| Core·MT5 | MLS-2 Launcher | 2x2x5 | 15 | -50 |
| Core·MT6 | MLS-2 Launcher | 2x2x5 | 15 | -50 |
| Core·MT7 | MLS-2 Launcher | 2x2x5 | 15 | -50 |
| Core·MT8 | MLS-2 Launcher | 2x2x5 | 15 | -50 |
| Bow·MT9 | VLS-1-23 Launcher | 2x2x2 | 5 | -50 |
| Bow·CMP1 | Basic CIC | 4x1x6 | 10 | 0 |
| Bow·CMP2 | Large DC Storage | 6x3x6 | 45 | 0 |
| Core·CMP2 | Reinforced DC Locker | 3x1x6 | 45 | 0 |
| Core·CMP4 | Bulk Magazine | 1x1x1 | 0 → 之后 20/座 | 0 |
| Core·CMP5 | Bulk Magazine | 1x1x1 | 0 → 之后 20/座 | 0 |
| Core·CMP6 | Reinforced CIC | 4x1x6 | 25 | 0 |
| Stern·MOD1 | Civilian Reactor | 5x5x5 | 10 | +3650 |
| Stern·MOD2 | CHI-9100 Long Haul Drive | 12x12x12 | 20 | 0 |
| Bow·MOD3 | Ithaca Bridgemaster | 2x2x2 | 10 | -1200 |

- 合计：部件 290 点 + 舰体 375 点 = **665 点**（不含弹库与弹药，见下）
- 另有弹库 20 点 + 弹药 2315 点 ⇒ **全价约 3000 点**（估算；游戏里以存档原值 3000 为准，单价见 `zh/弹药点数表.md`）
- 供电：发电 3650 kW / 耗电 1650 kW（余量 +2000 kW）
- 弹库装载：Bow·MT9 VLS-1-23 Launcher：EA12 Chaff Decoy ×3；Core·CMP4 Bulk Magazine：SGM-206 Musket ×70、-ImowmjgyEK7oJ6sMnnIOw ×54、P0TZ9BO9ZkyYKljJaYKzvg ×18；Core·CMP5 Bulk Magazine：SGM-206 Musket ×70、-ImowmjgyEK7oJ6sMnnIOw ×54、P0TZ9BO9ZkyYKljJaYKzvg ×18


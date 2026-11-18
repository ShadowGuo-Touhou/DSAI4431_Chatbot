# A Cap ffl (sprinter or shuttle)

Tags: kind=build template; class=A Cap ffl (sprinter or shuttle); cost=100-200; samples=239; good=33
Keywords: build, loadout, template, 配装, 配置, 装配, 模板, 舰级, A Cap ffl (sprinter or shuttle)
Summary: A Cap ffl (sprinter or shuttle) build; 239 matched ships, 33 of them are good samples (must and should both pass); typical cost 176 (range 115-189); hull Ferryman Clipper Class×20、Sprinter Corvette Class×13.
Section: build templates; requirements from other info/Ship Builds.txt; samples from player fleets

## How to read this
回答「这艘船算不算 / 合不合格」以 Requirements 段为准（must 全过才算这个舰级，should 是良好标准）；部件清单只统计 good 样本，频率 (k/N) 表示常见程度，不是硬性要求。所有舰船先要过通用基线（`reference/baseline-requirements.md`），再看本舰级要求。

## 舰级要求（Ship Builds.txt 原文，作为判定依据）

**舰级硬性要求（required：缺一条就不算这个舰级）**
- have no turrets
- does not satisfy any other class

**良好标准（should：缺了算有瑕疵，但仍算这个舰级）**
- have 1 arming missile (offensive S1 that cost 1 point)
- have a fast drive (FM230 whiplash or sundrive)

**可选加分（optional）**
- have a Radar
- have minimal DC (1 rapid DC Locker)
- have 1 reinforced CIC
- have minimal softkill

## Disclaimer
参考配置，不是最优解。样本是玩家舰队里 must + should 全过的真实配装（主要取自中文新手包 v1.12，对应游戏 0.6.2.3；其余来自 other info 与本地存档）。旧版本可能改过数值或改过名字；模组部件不代表原版能照抄。把它当起步模板，不要当配方。

## Numbers
- Point cost: 100-200 (good-sample median 176, range 115-189)
- Power: draw 1500 kW / supply 2050 kW (median)
- Hull: Ferryman Clipper Class×20、Sprinter Corvette Class×13

## Armament (good samples)
- VLS-1-23 launcher: 17/33 ships
- RL18 launcher: 17/33 ships
- VLS-1-46 launcher: 6/33 ships
- ML-9 Mine Launcher launcher: 2/33 ships

## Core parts (fitted on most good samples)
- Basic CIC (32/33)

## Common parts (40-70%)
- Ithaca Bridgemaster (20/33)
- Light Civilian Reactor (20/33)
- RF44 'Pinpoint' Radar (14/33)
- RL18 Launcher (17/33)
- Rapid DC Locker (14/33)
- Reinforced Magazine (20/33)
- Sundrive Racing Pro (17/33)
- VLS-1-23 Launcher (17/33)

## Optional parts
- FM200 Drive (7/33)
- Auxiliary Steering (6/33)
- FM230 'Whiplash' Drive (6/33)
- VLS-1-46 Launcher (6/33)
- FR3300 Micro Reactor (5/33)
- RS35 'Frontline' Radar (5/33)
- BW800 Drive (3/33)
- E15 'Masquerade' Signature Booster (2/33)
- ML-9 'Mine' Launcher (2/33)
- Mk25 'Rebound' PDT (1/33)
- Reinforced CIC (1/33)

## Sample ships (good)
- Hustler (Tantalum Squadron, 183 pts, example fleet)
- A Point (1-bb less but effective baofan, 115 pts, player save)
- The Ample Goofy (You Can't Make Me Bring Hardkill, 121 pts, player save)
- Spasm (CL cap fleet 2, 122 pts, player save)
- The Deft Pasta (CL cap fleet 2, 122 pts, player save)
- The Toned Wound (All Craft Are Bastards, 123 pts, player save)

## 样板船完整装配（整艘照抄）：Hustler（Tantalum Squadron）

**整艘照抄**：舰体 `Shuttle`（阵营键 `Stock/Outlying Systems Protectorate`），存档原值 **183 点**，共 8 个槽位。复制这艘船时连它自带的导弹一起抄，只改船名、呼号和导弹名。

| 槽位 | 部件 | 尺寸 | 点数 | 供电 kW |
|---|---|---|---:|---:|
| MT1 | ML-9 'Mine' Launcher | 3x2x3 | 10 | -100 |
| MT3 | VLS-1-23 Launcher | 2x2x2 | 5 | -50 |
| CMP1 | Basic CIC | 4x1x6 | 10 | 0 |
| CMP2 | Rapid DC Locker | 3x1x3 | 10 | 0 |
| CMP3 | Reinforced Magazine | 1x1x1 | 0 → 之后 40/座 | 0 |
| MOD1 | Light Civilian Reactor | 3x3x3 | 10 | +1850 |
| MOD2 | BW800 Drive | 5x3x5 | 10 | 0 |
| MOD3 | Ithaca Bridgemaster | 2x2x2 | 10 | -1200 |

- 合计：部件 65 点 + 舰体 50 点 = **115 点**（不含弹库与弹药，见下）
- 另有弹库 0 点 + 弹药 18 点 ⇒ **全价约 133 点**（估算；游戏里以存档原值 183 为准，单价见 `zh/弹药点数表.md`）
- 供电：发电 1850 kW / 耗电 1350 kW（余量 +500 kW）
- 弹库装载：MT1 ML-9 'Mine' Launcher：S3 Sprint Mine ×5；MT3 VLS-1-23 Launcher：EA12 Chaff Decoy ×5、SGM-126 Counter-Time ×1、SGM-102 Reprise ×6


## 样板船完整装配（整艘照抄）：The Toned Wound（All Craft Are Bastards）

**整艘照抄**：舰体 `Sprinter Corvette`（阵营键 `Stock/Shelter Alliance`），存档原值 **123 点**，共 6 个槽位。复制这艘船时连它自带的导弹一起抄，只改船名、呼号和导弹名。

| 槽位 | 部件 | 尺寸 | 点数 | 供电 kW |
|---|---|---|---:|---:|
| MT4 | VLS-1-23 Launcher | 2x2x2 | 5 | -50 |
| CMP1 | Rapid DC Locker | 3x1x3 | 10 | 0 |
| CMP2 | Basic CIC | 4x1x6 | 10 | 0 |
| CMP3 | Reinforced Magazine | 1x1x1 | 0 → 之后 40/座 | 0 |
| CMP4 | Auxiliary Steering | 3x1x3 | 10 | 0 |
| MOD2 | FM200 Drive | 5x3x5 | 10 | 0 |

- 合计：部件 45 点 + 舰体 75 点 = **120 点**（不含弹库与弹药，见下）
- 另有弹库 0 点 + 弹药 3 点 ⇒ **全价约 123 点**（估算；游戏里以存档原值 123 为准，单价见 `zh/弹药点数表.md`）
- 供电：发电 0 kW / 耗电 50 kW（余量 -50 kW）
- 弹库装载：MT4 VLS-1-23 Launcher：SGM-123 Ghost Bird ×1、EA12 Chaff Decoy ×2


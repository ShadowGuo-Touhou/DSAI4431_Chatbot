# S2CC

Tags: kind=build template; class=S2CC; cost=2500-3000; samples=10; good=10
Keywords: build, loadout, template, 配装, 配置, 装配, 模板, 舰级, S2CC
Summary: S2CC build; 10 matched ships, 10 of them are good samples (must and should both pass); typical cost 3000 (range 2543-3000); hull Ocello Command Cruiser Class×10.
Section: build templates; requirements from other info/Ship Builds.txt; samples from player fleets

## How to read this
回答「这艘船算不算 / 合不合格」以 Requirements 段为准（must 全过才算这个舰级，should 是良好标准）；部件清单只统计 good 样本，频率 (k/N) 表示常见程度，不是硬性要求。所有舰船先要过通用基线（`reference/baseline-requirements.md`），再看本舰级要求。

## 舰级要求（Ship Builds.txt 原文，作为判定依据）

**舰级硬性要求（required：缺一条就不算这个舰级）**
- have >1000 points of S2 direct straightrunner offensive missiles

**良好标准（should：缺了算有瑕疵，但仍算这个舰级）**
- have at least 2 blanket jammers

## Disclaimer
参考配置，不是最优解。样本是玩家舰队里 must + should 全过的真实配装（主要取自中文新手包 v1.12，对应游戏 0.6.2.3；其余来自 other info 与本地存档）。旧版本可能改过数值或改过名字；模组部件不代表原版能照抄。把它当起步模板，不要当配方。

## Numbers
- Point cost: 2500-3000 (good-sample median 3000, range 2543-3000)
- Power: draw 11900 kW / supply 11500 kW (median)
- Hull: Ocello Command Cruiser Class×10

## Armament (good samples)
- VLS-2 launcher: 10/10 ships
- VLS-1-46 launcher: 6/10 ships
- CLS-3 launcher: 1/10 ships

## Core parts (fitted on most good samples)
- Boosted Reactor (9/10)
- E70 'Interruption' Jammer (7/10)
- E90 'Blanket' Jammer (10/10)
- ES32 'Scryer' Missile ID System (9/10)
- FM530 'Whiplash' Drive (8/10)
- Intelligence Center (9/10)
- L50 'Blackjack' Laser Dazzler (10/10)
- Missile Parallel Interface (10/10)
- Missile Programming Bus Array (10/10)
- Mk90 'Aurora' PDT (10/10)
- RF101 'Bullseye' Radar (10/10)
- RM50 'Parallax' Radar (10/10)
- Reinforced CIC (10/10)
- Reinforced DC Locker (10/10)
- Strike Planning Center (9/10)
- VLS-2 Launcher (10/10)

## Common parts (40-70%)
- Rapid DC Locker (4/10)
- Reinforced Magazine (5/10)
- Small DC Locker (4/10)
- VLS-1-46 Launcher (6/10)

## Optional parts
- Auxiliary Steering (2/10)
- FM540 'Dragonfly' Drive (2/10)
- J75 'Warbler' Jammer (2/10)
- CLS-3 Launcher (1/10)
- E55 'Spotlight' Illuminator (1/10)
- FR3300 Micro Reactor (1/10)
- FR4800 Reactor (1/10)
- Missile Programming Bus (1/10)
- Plant Control Center (1/10)
- Sundrive Racing Pro (1/10)

## Sample ships (good)
- Nuclear Summer (S2 DIR OCELLO, 3000 pts, Chinese starter pack)
- Command Cruiser Must Command (S2 DIR OCELLO, 3000 pts, Chinese starter pack)
- Grand Basal (tesdt, 2543 pts, player save)
- Nuclear Spring (Helplessness, 3000 pts, player save)
- Nuclear Autumn (Helplessness, 3000 pts, player save)
- Dark (4 S2CC, 3000 pts, player save)

## 样板船完整装配（整艘照抄）：Nuclear Summer（S2 DIR OCELLO）

**整艘照抄**：舰体 `Ocello Cruiser`（阵营键 `Stock/Outlying Systems Protectorate`），存档原值 **3000 点**，共 28 个槽位。复制这艘船时连它自带的导弹一起抄，只改船名、呼号和导弹名。

| 槽位 | 部件 | 尺寸 | 点数 | 供电 kW |
|---|---|---|---:|---:|
| MT1 | VLS-2 Launcher | 3x4x3 | 10 | -200 |
| MT2 | VLS-2 Launcher | 3x4x3 | 10 | -200 |
| MT3 | VLS-2 Launcher | 3x4x3 | 10 | -200 |
| MT4 | Mk90 'Aurora' PDT | 2x1x2 | 55 | -1250 |
| MT5 | Mk90 'Aurora' PDT | 2x1x2 | 55 | -1250 |
| MT6 | J75 'Warbler' Jammer | 3x1x3 | 50 | -500 |
| MT7 | VLS-1-46 Launcher | 3x2x3 | 5 | -50 |
| MT8 | L50 'Blackjack' Laser Dazzler | 2x1x2 | 40 | -750 |
| MT9 | RF101 'Bullseye' Radar | 2x1x2 | 40 | -300 |
| MT10 | E90 'Blanket' Jammer | 2x1x2 | 50 | -1000 |
| MT11 | E90 'Blanket' Jammer | 2x1x2 | 50 | -1000 |
| CMP1 | Strike Planning Center | 6x1x8 | 70 | 0 |
| CMP2 | Intelligence Center | 6x1x8 | 90 | 0 |
| CMP3 | Small DC Locker | 3x1x3 | 20 | 0 |
| CMP4 | Reinforced CIC | 4x1x6 | 25 | 0 |
| CMP5 | Reinforced DC Locker | 3x1x6 | 45 | 0 |
| CMP6 | Reinforced Magazine | 1x1x1 | 0 → 之后 40/座 | 0 |
| CMP7 | Auxiliary Steering | 3x1x3 | 10 | 0 |
| CMP8 | Small DC Locker | 3x1x3 | 20 | 0 |
| MOD1 | Boosted Reactor | 5x5x5 | 10 | +5000 |
| MOD2 | Boosted Reactor | 5x5x5 | 10 | +5000 |
| MOD3 | FM530 'Whiplash' Drive | 10x8x10 | 30 | 0 |
| MOD4 | Missile Programming Bus Array | 3x3x3 | 50 | -350 |
| MOD5 | Missile Programming Bus Array | 3x3x3 | 50 | -350 |
| MOD6 | Missile Programming Bus Array | 3x3x3 | 50 | -350 |
| MOD7 | RM50 'Parallax' Radar | 2x2x2 | 45 | -3600 |
| MOD8 | Missile Parallel Interface | 2x2x2 | 40 | -150 |
| MOD9 | ES32 'Scryer' Missile ID System | 2x2x2 | 10 | -300 |

- 合计：部件 950 点 + 舰体 575 点 = **1525 点**（不含弹库与弹药，见下）
- 另有弹库 0 点 + 弹药 1479 点 ⇒ **全价约 3004 点**（估算；游戏里以存档原值 3000 为准，单价见 `zh/弹药点数表.md`）
- 供电：发电 10000 kW / 耗电 11800 kW（余量 -1800 kW）
- 弹库装载：MT1 VLS-2 Launcher：SGM-291 DO NOT SCARE ME ×10、SGM-291 I WILL USE CHAFF ×42、SGM-29 EA29 Killjoy ×1、D6HAL97ob02E3ok_6EVdrg ×6；MT2 VLS-2 Launcher：SGM-291 DO NOT SCARE ME ×10、SGM-291 I WILL USE CHAFF ×42、SGM-29 EA29 Killjoy ×2、D6HAL97ob02E3ok_6EVdrg ×5；MT3 VLS-2 Launcher：SGM-291 DO NOT SCARE ME ×10、SGM-291 I WILL USE CHAFF ×42、SGM-29 EA29 Killjoy ×1、D6HAL97ob02E3ok_6EVdrg ×5；MT7 VLS-1-46 Launcher：EA12 Chaff Decoy ×17、EA20 Flare Decoy ×5、_RrCeP-3aEaZ6ecS3aXiww ×1


## 样板船完整装配（整艘照抄）：Command Cruiser Must Command（S2 DIR OCELLO）

**整艘照抄**：舰体 `Ocello Cruiser`（阵营键 `Stock/Outlying Systems Protectorate`），存档原值 **3000 点**，共 29 个槽位。复制这艘船时连它自带的导弹一起抄，只改船名、呼号和导弹名。

| 槽位 | 部件 | 尺寸 | 点数 | 供电 kW |
|---|---|---|---:|---:|
| MT1 | VLS-2 Launcher | 3x4x3 | 10 | -200 |
| MT2 | VLS-2 Launcher | 3x4x3 | 10 | -200 |
| MT3 | VLS-2 Launcher | 3x4x3 | 10 | -200 |
| MT4 | Mk90 'Aurora' PDT | 2x1x2 | 55 | -1250 |
| MT5 | Mk90 'Aurora' PDT | 2x1x2 | 55 | -1250 |
| MT6 | E70 'Interruption' Jammer | 3x1x3 | 55 | -600 |
| MT7 | VLS-1-46 Launcher | 3x2x3 | 5 | -50 |
| MT8 | L50 'Blackjack' Laser Dazzler | 2x1x2 | 40 | -750 |
| MT9 | RF101 'Bullseye' Radar | 2x1x2 | 40 | -300 |
| MT10 | E90 'Blanket' Jammer | 2x1x2 | 50 | -1000 |
| MT11 | E90 'Blanket' Jammer | 2x1x2 | 50 | -1000 |
| CMP1 | Strike Planning Center | 6x1x8 | 70 | 0 |
| CMP2 | Reinforced CIC | 4x1x6 | 25 | 0 |
| CMP3 | Intelligence Center | 6x1x8 | 90 | 0 |
| CMP4 | Small DC Locker | 3x1x3 | 20 | 0 |
| CMP5 | Reinforced DC Locker | 3x1x6 | 45 | 0 |
| CMP6 | Reinforced Magazine | 1x1x1 | 0 → 之后 40/座 | 0 |
| CMP7 | Rapid DC Locker | 3x1x3 | 10 | 0 |
| CMP8 | Rapid DC Locker | 3x1x3 | 10 | 0 |
| CMP9 | Rapid DC Locker | 3x1x3 | 10 | 0 |
| MOD1 | Boosted Reactor | 5x5x5 | 10 | +5000 |
| MOD2 | Boosted Reactor | 5x5x5 | 10 | +5000 |
| MOD3 | FM530 'Whiplash' Drive | 10x8x10 | 30 | 0 |
| MOD4 | Missile Programming Bus Array | 3x3x3 | 50 | -350 |
| MOD5 | Missile Programming Bus Array | 3x3x3 | 50 | -350 |
| MOD6 | Missile Programming Bus Array | 3x3x3 | 50 | -350 |
| MOD7 | RM50 'Parallax' Radar | 2x2x2 | 45 | -3600 |
| MOD8 | Missile Parallel Interface | 2x2x2 | 40 | -150 |
| MOD9 | ES32 'Scryer' Missile ID System | 2x2x2 | 10 | -300 |

- 合计：部件 955 点 + 舰体 575 点 = **1530 点**（不含弹库与弹药，见下）
- 另有弹库 0 点 + 弹药 1470 点 ⇒ **全价约 3000 点**（估算；游戏里以存档原值 3000 为准，单价见 `zh/弹药点数表.md`）
- 供电：发电 10000 kW / 耗电 11900 kW（余量 -1900 kW）
- 弹库装载：MT1 VLS-2 Launcher：SGM-291 DO NOT SCARE ME ×11、SGM-291 I WILL USE CHAFF ×44、SGM-29 EA29 Killjoy ×1；MT2 VLS-2 Launcher：SGM-291 DO NOT SCARE ME ×11、SGM-291 I WILL USE CHAFF ×45、SGM-29 EA29 Killjoy ×2；MT3 VLS-2 Launcher：SGM-291 DO NOT SCARE ME ×10、SGM-291 I WILL USE CHAFF ×46、SGM-29 EA29 Killjoy ×1；MT7 VLS-1-46 Launcher：EA12 Chaff Decoy ×12、EA20 Flare Decoy ×5


## Author notes (from the fleet's 使用说明.txt)
- S2 DIR OCELLO: *舰队定位* / 前排，中远程直射火力，电子战辅助 / *上手难度* / 高，难于所有OSP直射火力舰队，建议掌握基本机制与对炮技术后开始尝试 / *武装说明* / 该战舰使用两款SGM-291导弹作为攻击武器。导弹速度约290mps，伤害高，突防能力较强。代价是数量较少，总伤害池较低，如果大量射失、被拦截或攻击尸体会严重降低输出能力。 / 防御武器主要为S2防空导弹Bread Stick III、SGM-29土制反辐射诱饵弹和两门近防激光组成。Bread Stick专门用来攻击敌方轰炸机，推荐使用时将点防导弹战法选择改为手动，按*默认为Z键*后单击敌轰炸机。缺点是备弹少，仅能应对两轮轰炸机攻击，所以使用时以保护自身安全为优先。SGM-29的弹载干扰机可以发出雷达干扰信号，近距离可以诱骗对方反辐射武器，但是有一些编程时间且需要手动指定路径，酌情使用。此外还有箔条和热焰弹作为无源干扰设备。 / 电子战设备配套齐全，主要为两台定向雷达干扰机，用以掩护导弹突防，并保护自己不被对方发现。在常规的7-8km交战距离上可以有效地反制对方探测或火控锁定。舰桥的激光压制设备可以干扰对方高价值的光电制导导弹，注意使用时最好手动指向目标。尾部的全向通讯干扰机用以干扰来袭的指令引导导弹，较有效应对小型平台，如驱护舰、轰炸机等使用的指令引导武器，使用时仍需与其他干扰设备配合以有效反制来袭导弹。 / *优点* / 导弹攻击灵活多样，可以攻击抢点小船或者前线主力舰，命中伤害可观，快速达成目标。 / 军用雷达，强力天线，配备情报中心，有效辅助全队索敌和引导自身导弹攻击。 / 防御手段齐全，有一定辅助能力。 …
- S2 DIR OCELLO: *舰队定位* / 前排，中远程直射火力，电子战辅助 / *上手难度* / 高，难于所有OSP直射火力舰队，建议掌握基本机制与对炮技术后开始尝试 / *武装说明* / 该战舰使用两款SGM-291导弹作为攻击武器。导弹速度约290mps，伤害高，突防能力较强。代价是数量较少，总伤害池较低，如果大量射失、被拦截或攻击尸体会严重降低输出能力。 / 防御武器主要为SGM-29土制反辐射诱饵弹和两门近防激光组成。SGM-29的弹载干扰机可以发出雷达干扰信号，近距离可以诱骗对方反辐射武器，但是有一些编程时间且需要手动指定路径，酌情使用。此外还有箔条和热焰弹作为无源干扰设备。 / 电子战设备配套齐全，主要为两台定向雷达干扰机，用以掩护导弹突防，并保护自己不被对方发现。在常规的7-8km交战距离上可以有效地反制对方探测或火控锁定。舰桥的激光压制设备可以干扰对方高价值的光电制导导弹，注意使用时最好手动指向目标。尾部的全向通讯干扰机用以干扰来袭的指令引导导弹，较有效应对小型平台，如驱护舰、轰炸机等使用的指令引导武器，使用时仍需与其他干扰设备配合以有效反制来袭导弹。 / *优点* / 导弹攻击灵活多样，可以攻击抢点小船或者前线主力舰，命中伤害可观，快速达成目标。 / 军用雷达，强力天线，配备情报中心，有效辅助全队索敌和引导自身导弹攻击。 / 防御手段齐全，有一定辅助能力。 / 航速较快，便于抢占攻击阵位。 / *缺点* / 正如你所见这条船自身就3000分，他本身就是一个高价值目标，可以拉到相当大的仇恨-而抗损能力远远比不上同样为前排单位的战列舰。使用时请务必小心规划走位，防止长时间暴露位置后遭遇各…

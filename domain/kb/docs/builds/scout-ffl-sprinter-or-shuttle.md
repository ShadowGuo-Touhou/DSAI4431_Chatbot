# scout ffl (sprinter or shuttle)

Tags: kind=build template; class=scout ffl (sprinter or shuttle); cost=110-250; samples=111; good=111
Keywords: build, loadout, template, 配装, 配置, 装配, 模板, 舰级, scout ffl (sprinter or shuttle)
Summary: scout ffl (sprinter or shuttle) build; 111 matched ships, 111 of them are good samples (must and should both pass); typical cost 155 (range 110-248); hull Ferryman Clipper Class×68、Sprinter Corvette Class×43.
Section: build templates; requirements from other info/Ship Builds.txt; samples from player fleets

## How to read this
回答「这艘船算不算 / 合不合格」以 Requirements 段为准（must 全过才算这个舰级，should 是良好标准）；部件清单只统计 good 样本，频率 (k/N) 表示常见程度，不是硬性要求。所有舰船先要过通用基线（`reference/baseline-requirements.md`），再看本舰级要求。

## 舰级要求（Ship Builds.txt 原文，作为判定依据）

**舰级硬性要求（required：缺一条就不算这个舰级）**
- have a long range radar (huntress or spyglass)

**可选加分（optional）**
- have minimal softkill
- have minimal hardkill
- have minimal DC (1 rapid DC Locker)

## Disclaimer
参考配置，不是最优解。样本是玩家舰队里 must + should 全过的真实配装（主要取自中文新手包 v1.12，对应游戏 0.6.2.3；其余来自 other info 与本地存档）。旧版本可能改过数值或改过名字；模组部件不代表原版能照抄。把它当起步模板，不要当配方。

## Numbers
- Point cost: 110-250 (good-sample median 155, range 110-248)
- Power: draw 2000 kW / supply 2150 kW (median)
- Hull: Ferryman Clipper Class×68、Sprinter Corvette Class×43

## Armament (good samples)
- 100 mm turret/cannon: 7/111 ships, median 1 (min 1, max 2)
- VLS-1-46 launcher: 26/111 ships
- VLS-1-23 launcher: 18/111 ships
- ML-9 Mine Launcher launcher: 2/111 ships

## Core parts (fitted on most good samples)
- Basic CIC (78/111)

## Common parts (40-70%)
- BW800 Drive (51/111)
- Bulwark Huntress (67/111)
- Light Civilian Reactor (67/111)
- Rapid DC Locker (50/111)
- Reinforced Magazine (67/111)

## Optional parts
- FR3300 Micro Reactor (43/111)
- Plant Control Center (43/111)
- RS41 'Spyglass' Radar (43/111)
- FM230 'Whiplash' Drive (39/111)
- Reinforced CIC (33/111)
- VLS-1-46 Launcher (26/111)
- Small DC Locker (19/111)
- VLS-1-23 Launcher (18/111)
- Sundrive Racing Pro (16/111)
- T20 Cannon (7/111)
- Small Reactor Booster (6/111)
- FM200 Drive (4/111)

## Sample ships (good)
- Hourglass (BB test 55 Newbie, 222 pts, Chinese starter pack)
- Hourglass (CC LN test 4 450, 232 pts, Chinese starter pack)
- Hourglass (CC LN test 4 450, 232 pts, Chinese starter pack)
- Pawn (dum shi, 110 pts, player save)
- Pawn (dum shi, 110 pts, player save)
- Pawn (dum shi, 110 pts, player save)

## 样板船完整装配（整艘照抄）：Hourglass（BB test 55 Newbie）

**整艘照抄**：舰体 `Sprinter Corvette`（阵营键 `Stock/Shelter Alliance`），存档原值 **222 点**，共 9 个槽位。复制这艘船时连它自带的导弹一起抄，只改船名、呼号和导弹名。

| 槽位 | 部件 | 尺寸 | 点数 | 供电 kW |
|---|---|---|---:|---:|
| MT4 | VLS-1-23 Launcher | 2x2x2 | 5 | -50 |
| CMP1 | Basic CIC | 4x1x6 | 10 | 0 |
| CMP2 | Plant Control Center | 3x1x3 | 25 | 0 |
| CMP3 | Rapid DC Locker | 3x1x3 | 10 | 0 |
| CMP4 | Plant Control Center | 3x1x3 | 25 | 0 |
| MOD1 | FR3300 Micro Reactor | 3x3x3 | 10 | +2250 |
| MOD2 | FM230 'Whiplash' Drive | 5x3x5 | 20 | 0 |
| MOD3 | RS41 'Spyglass' Radar | 2x2x2 | 25 | -4000 |
| MOD4 | Small Reactor Booster | 2x2x2 | 10 | 0 |

- 合计：部件 140 点 + 舰体 75 点 = **215 点**（不含弹库与弹药，见下）
- 另有弹库 0 点 + 弹药 7 点 ⇒ **全价约 222 点**（估算；游戏里以存档原值 222 为准，单价见 `zh/弹药点数表.md`）
- 供电：发电 2250 kW / 耗电 4050 kW（余量 -1800 kW）
- 弹库装载：MT4 VLS-1-23 Launcher：SGM-100 Balestra ×1、EA12 Chaff Decoy ×6


## 样板船完整装配（整艘照抄）：Hourglass（CC LN test 4 450）

**整艘照抄**：舰体 `Shuttle`（阵营键 `Stock/Outlying Systems Protectorate`），存档原值 **232 点**，共 9 个槽位。复制这艘船时连它自带的导弹一起抄，只改船名、呼号和导弹名。

| 槽位 | 部件 | 尺寸 | 点数 | 供电 kW |
|---|---|---|---:|---:|
| MT1 | J15 'Bellbird' Jammer | 3x1x3 | 50 | -850 |
| MT2 | VLS-1-46 Launcher | 3x2x3 | 5 | -50 |
| MT3 | L50 'Blackjack' Laser Dazzler | 2x1x2 | 40 | -750 |
| CMP1 | Basic CIC | 4x1x6 | 10 | 0 |
| CMP2 | Reinforced Magazine | 1x1x1 | 0 → 之后 40/座 | 0 |
| CMP3 | Small DC Locker | 3x1x3 | 20 | 0 |
| MOD1 | Light Civilian Reactor | 3x3x3 | 10 | +1850 |
| MOD2 | BW800 Drive | 5x3x5 | 10 | 0 |
| MOD3 | Bulwark Huntress | 2x2x2 | 30 | -2000 |

- 合计：部件 175 点 + 舰体 50 点 = **225 点**（不含弹库与弹药，见下）
- 另有弹库 0 点 + 弹药 7 点 ⇒ **全价约 232 点**（估算；游戏里以存档原值 232 为准，单价见 `zh/弹药点数表.md`）
- 供电：发电 1850 kW / 耗电 3650 kW（余量 -1800 kW）
- 弹库装载：MT2 VLS-1-46 Launcher：SGM-101 OA ×1、EA12 Chaff Decoy ×6


## Author notes (from the fleet's 使用说明.txt)
- CC LN test 4 450: *舰队定位：前排/中远程火炮输出 / *上手难度：高（比战列舰容易，但是有限） / *武装说明 / --指挥巡洋舰（CC）有6管450mm火炮，垂发中的S1导弹为防空导弹。装备泛光灯对抗雷达干扰。 / --二号线列舰（LN）主武器450mm弹夹炮。另有100mm副炮，EO干扰器，和各种诱饵。 / --三号穿梭机装备范围10KM的雷达。另有雷达干扰和EO干扰。 / --舰队装备类全软杀，例外还是Eact[CMD]拒绝。 / *优点： / --OSP的六边形战士 / --CC能打能扛还能提供ECCM / --CC在9km外能通过环绕指令有效回避450mm炮弹 / --LN的弹夹炮高爆发，副炮能打小船 / --LN可以依靠CC的火控数据躲在敌方Bulls Eye锁定范围外输出 / --穿梭机可以前出开视野，也可以利用干扰器干扰一下敌方锁定 / *缺点： / -未装备真.全软杀 / --穿梭机启动电子战时需要关掉雷达，否则电不够 / --点防御搞不定大批量导弹，需要软杀 / 使用注意事项： / 1.CC虽然能躲炮弹，但是距离太近或者被敌方打交叉火力就不行了 / 2.CC需要时刻将船艏指向来袭火力的大致方向。侧面挨打很伤。 / 3.CC航速一般，撤退需要及时。不要离掩体太远。 / 4.S1防空导弹数量少，一定要手动发射； / 5.LN身上的集装箱导弹是SSJ诱饵，请设置成手动发射然后对有Hoj引导头的导弹按Z发射； / LN背后还有两发诱饵集装箱，看见arad或[arad]时手动发射 / 6.LN需要手动提前转向，把有炮的侧面对准敌方可能出现的位置，然后依靠CC或者其他友军的火控数据射击…
- CC LN test 4 450: *舰队定位：前排/中远程火炮输出 / *上手难度：高（比战列舰容易，但是有限） / *武装说明 / --指挥巡洋舰（CC）有6管450mm火炮，垂发中的S1导弹为防空导弹。装备泛光灯对抗雷达干扰。 / --二号线列舰（LN）主武器450mm弹夹炮。另有100mm副炮，EO干扰器，和各种诱饵。 / --三号穿梭机装备范围10KM的雷达。另有雷达干扰和EO干扰。 / --舰队装备全软杀，理论上所以引导头组合都能软杀。 / *优点： / --OSP的六边形战士 / --CC能打能扛还能提供ECCM / --CC在9km外能通过环绕指令有效回避450mm炮弹 / --LN的弹夹炮高爆发，副炮能打小船 / --LN可以依靠CC的火控数据躲在敌方Bulls Eye锁定范围外输出 / --穿梭机可以前出开视野，也可以利用干扰器干扰一下敌方锁定 / *缺点： / --非常怕被打交叉火力 / --穿梭机启动电子战时需要关掉雷达，否则电不够 / --点防御搞不定大批量导弹，需要软杀 / 使用注意事项： / 1.CC虽然能躲炮弹，但是距离太近或者被敌方打交叉火力就不行了 / 2.CC需要时刻将船艏指向来袭火力的大致方向。侧面挨打很伤。 / 3.CC航速一般，撤退需要及时。不要离掩体太远。 / 4.S1防空导弹数量少，一定要手动发射； / 5.LN身上的集装箱导弹是SSJ诱饵，请设置成手动发射然后对有Hoj引导头的导弹按Z发射； / LN背后还有两发诱饵集装箱，看见arad或[arad]时手动发射 / 6.LN需要手动提前转向，把有炮的侧面对准敌方可能出现的位置，然后依靠CC或者其他友军的火控数据射击…

# support ffl (sprinter or shuttle)

Tags: kind=build template; class=support ffl (sprinter or shuttle); cost=150-400; samples=69; good=55
Keywords: build, loadout, template, 配装, 配置, 装配, 模板, 舰级, support ffl (sprinter or shuttle)
Summary: support ffl (sprinter or shuttle) build; 69 matched ships, 55 of them are good samples (must and should both pass); typical cost 293 (range 186-391); hull Sprinter Corvette Class×40、Ferryman Clipper Class×15.
Section: build templates; requirements from other info/Ship Builds.txt; samples from player fleets

## How to read this
回答「这艘船算不算 / 合不合格」以 Requirements 段为准（must 全过才算这个舰级，should 是良好标准）；部件清单只统计 good 样本，频率 (k/N) 表示常见程度，不是硬性要求。所有舰船先要过通用基线（`reference/baseline-requirements.md`），再看本舰级要求。

## 舰级要求（Ship Builds.txt 原文，作为判定依据）

**舰级硬性要求（required：缺一条就不算这个舰级）**
- have at least 1 jammer and/or illuminator

**良好标准（should：缺了算有瑕疵，但仍算这个舰级）**
- have minimal DC (1 Rapid DC Locker)
- have minimal softkill

**可选加分（optional）**
- have minimal hardkill
- have at least 2 jammer and/or illuminator
- have better DC (at least 1 restore)
- have 1 reinforced CIC

## Disclaimer
参考配置，不是最优解。样本是玩家舰队里 must + should 全过的真实配装（主要取自中文新手包 v1.12，对应游戏 0.6.2.3；其余来自 other info 与本地存档）。旧版本可能改过数值或改过名字；模组部件不代表原版能照抄。把它当起步模板，不要当配方。

## Numbers
- Point cost: 150-400 (good-sample median 293, range 186-391)
- Power: draw 2495 kW / supply 2900 kW (median)
- Hull: Sprinter Corvette Class×40、Ferryman Clipper Class×15

## Armament (good samples)
- 250 mm turret/cannon: 22/55 ships, median 1 (min 1, max 1)
- 120 mm turret/cannon: 16/55 ships, median 1 (min 1, max 1)
- 100 mm turret/cannon: 4/55 ships, median 1 (min 1, max 1)
- VLS-1-23 launcher: 20/55 ships
- VLS-1-46 launcher: 5/55 ships
- CLS-3 launcher: 5/55 ships
- VLS-2 launcher: 1/55 ships

## Core parts (fitted on most good samples)
- Basic CIC (42/55)
- Reinforced Magazine (43/55)

## Common parts (40-70%)
- E90 'Blanket' Jammer (26/55)
- FM230 'Whiplash' Drive (35/55)
- FR3300 Micro Reactor (38/55)
- Mk64 Cannon (22/55)
- Rapid DC Locker (36/55)
- Small DC Locker (23/55)

## Optional parts
- VLS-1-23 Launcher (21/55)
- Ammunition Elevators (17/55)
- Mk62 Cannon (17/55)
- Light Civilian Reactor (15/55)
- E71 'Hangup' Jammer (13/55)
- Reinforced CIC (13/55)
- E55 'Floodlight' Illuminator (12/55)
- Ithaca Bridgemaster (12/55)
- Actively Cooled Amplifiers (11/55)
- Bulk Magazine (11/55)
- Plant Control Center (11/55)
- Mk20 'Defender' PDT (10/55)

## Sample ships (good)
- Zippy Taxis (BB test 55 Newbie, 220 pts, Chinese starter pack)
- Hourglass (CC LN test 4 450, 232 pts, Chinese starter pack)
- Hourglass (CC LN test 4 450, 232 pts, Chinese starter pack)
- The Alike Even (HC Gun Missile test 8, 385 pts, Chinese starter pack)
- 无名氏 (大冲击, 235 pts, example fleet)
- ̢̧͔̹͇̀̆̄A̴N̅́̏O̰̽Ṁ̸͈͠A̶L̸͇̗͕Y (ANOMALY-120FFMAXX, 319 pts, example fleet)

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
- BB test 55 Newbie: *舰队定位：前排/中远程火炮输出 / *上手难度：高 / （该舰队本不应出现在新手包里面。但是我知道新手肯定会试着去搓战列舰舰队所以干脆放在这里给你们当参考） / *武装说明 / 1.主武器为8管450mm火炮 / 2.战列舰背后的S3H导弹都是防空导弹。使用时将防御导弹发射控制设置成"手动"，然后锁定敌方飞机后按Z发射 / 3.战列舰侧面的S2垂发中，S2导弹为SSJ诱饵导弹，使用方法同上，目标为敌方有hoj引导头的导弹 / 4.二号轻护上面有泛光灯和锁定雷达。可以在战列舰前面，目标8.5公里左右处锁定目标，给战列舰提供火控数据。战列舰根据火控数据能发挥450mm火炮的最大射程。 / 5.三号舰为点防御护卫舰，战列舰本体也装备有适量点防御。 / 6.本舰队装备类全软杀，除"Eact[cmd]拒绝"引导头外，别的引导头都能软杀。 / *优点： / --战列舰船体拥有56厘米装甲和大量损管，比较耐打。 / --拥有9.5公里以上精确火控能力，在该9.5公里外交火能压制OSP的线列舰 / --有类全软杀和足够多的防空导弹 / *缺点： / --反小船火力只有二号舰上面一门120mm炮，约等于没有。 / --未装备 真.全软杀 / --未装备视差雷达 / --大量软杀/电子战设备集中在战列舰本体上，容易被打坏 / --反电子战能力一般，遇到敌方重干扰如果泛光灯搞不定请找队友支援 / --机动性较差，回避效果一般，撤退缓慢 / 使用注意事项： / 1.战列舰虽然耐打但并不无敌，不要和过多（大于3000分）的敌方同时交手 / 2.战列舰需要时刻将船艏指向来袭火力的大致方向。侧面挨打很伤。…
- CC LN test 4 450: *舰队定位：前排/中远程火炮输出 / *上手难度：高（比战列舰容易，但是有限） / *武装说明 / --指挥巡洋舰（CC）有6管450mm火炮，垂发中的S1导弹为防空导弹。装备泛光灯对抗雷达干扰。 / --二号线列舰（LN）主武器450mm弹夹炮。另有100mm副炮，EO干扰器，和各种诱饵。 / --三号穿梭机装备范围10KM的雷达。另有雷达干扰和EO干扰。 / --舰队装备类全软杀，例外还是Eact[CMD]拒绝。 / *优点： / --OSP的六边形战士 / --CC能打能扛还能提供ECCM / --CC在9km外能通过环绕指令有效回避450mm炮弹 / --LN的弹夹炮高爆发，副炮能打小船 / --LN可以依靠CC的火控数据躲在敌方Bulls Eye锁定范围外输出 / --穿梭机可以前出开视野，也可以利用干扰器干扰一下敌方锁定 / *缺点： / -未装备真.全软杀 / --穿梭机启动电子战时需要关掉雷达，否则电不够 / --点防御搞不定大批量导弹，需要软杀 / 使用注意事项： / 1.CC虽然能躲炮弹，但是距离太近或者被敌方打交叉火力就不行了 / 2.CC需要时刻将船艏指向来袭火力的大致方向。侧面挨打很伤。 / 3.CC航速一般，撤退需要及时。不要离掩体太远。 / 4.S1防空导弹数量少，一定要手动发射； / 5.LN身上的集装箱导弹是SSJ诱饵，请设置成手动发射然后对有Hoj引导头的导弹按Z发射； / LN背后还有两发诱饵集装箱，看见arad或[arad]时手动发射 / 6.LN需要手动提前转向，把有炮的侧面对准敌方可能出现的位置，然后依靠CC或者其他友军的火控数据射击…
- CC LN test 4 450: *舰队定位：前排/中远程火炮输出 / *上手难度：高（比战列舰容易，但是有限） / *武装说明 / --指挥巡洋舰（CC）有6管450mm火炮，垂发中的S1导弹为防空导弹。装备泛光灯对抗雷达干扰。 / --二号线列舰（LN）主武器450mm弹夹炮。另有100mm副炮，EO干扰器，和各种诱饵。 / --三号穿梭机装备范围10KM的雷达。另有雷达干扰和EO干扰。 / --舰队装备全软杀，理论上所以引导头组合都能软杀。 / *优点： / --OSP的六边形战士 / --CC能打能扛还能提供ECCM / --CC在9km外能通过环绕指令有效回避450mm炮弹 / --LN的弹夹炮高爆发，副炮能打小船 / --LN可以依靠CC的火控数据躲在敌方Bulls Eye锁定范围外输出 / --穿梭机可以前出开视野，也可以利用干扰器干扰一下敌方锁定 / *缺点： / --非常怕被打交叉火力 / --穿梭机启动电子战时需要关掉雷达，否则电不够 / --点防御搞不定大批量导弹，需要软杀 / 使用注意事项： / 1.CC虽然能躲炮弹，但是距离太近或者被敌方打交叉火力就不行了 / 2.CC需要时刻将船艏指向来袭火力的大致方向。侧面挨打很伤。 / 3.CC航速一般，撤退需要及时。不要离掩体太远。 / 4.S1防空导弹数量少，一定要手动发射； / 5.LN身上的集装箱导弹是SSJ诱饵，请设置成手动发射然后对有Hoj引导头的导弹按Z发射； / LN背后还有两发诱饵集装箱，看见arad或[arad]时手动发射 / 6.LN需要手动提前转向，把有炮的侧面对准敌方可能出现的位置，然后依靠CC或者其他友军的火控数据射击…

# EWR/LRT tug

Tags: kind=build template; class=EWR/LRT tug; cost=170-300; samples=39; good=8
Keywords: build, loadout, template, 配装, 配置, 装配, 模板, 舰级, EWR/LRT tug
Summary: EWR/LRT tug build; 39 matched ships, 8 of them are good samples (must and should both pass); typical cost 257 (range 217-258); hull Draugr Clipper Class×8.
Section: build templates; requirements from other info/Ship Builds.txt; samples from player fleets

## How to read this
回答「这艘船算不算 / 合不合格」以 Requirements 段为准（must 全过才算这个舰级，should 是良好标准）；部件清单只统计 good 样本，频率 (k/N) 表示常见程度，不是硬性要求。所有舰船先要过通用基线（`reference/baseline-requirements.md`），再看本舰级要求。

## 舰级要求（Ship Builds.txt 原文，作为判定依据）

**舰级硬性要求（required：缺一条就不算这个舰级）**
- have a LRT radar or Early Warning Radar (EWR)

**良好标准（should：缺了算有瑕疵，但仍算这个舰级）**
- have at least 1 Track Correlator
- have minimal DC (at least 1 rapid DC)
- have minimal softkill

**可选加分（optional）**
- have at least 2 Track Correlators
- have both LRT and EWR (this overrides power requirement, in this case power is only required to support both radar individually)
- have minimal hardkill
- have jammers

## Disclaimer
参考配置，不是最优解。样本是玩家舰队里 must + should 全过的真实配装（主要取自中文新手包 v1.12，对应游戏 0.6.2.3；其余来自 other info 与本地存档）。旧版本可能改过数值或改过名字；模组部件不代表原版能照抄。把它当起步模板，不要当配方。

## Numbers
- Point cost: 170-300 (good-sample median 257, range 217-258)
- Power: draw 7850 kW / supply 5300 kW (median)
- Hull: Draugr Clipper Class×8

## Armament (good samples)
- 100 mm turret/cannon: 1/8 ships, median 1 (min 1, max 1)
- VLS-1-23 launcher: 7/8 ships
- VLS-1-46 launcher: 1/8 ships

## Core parts (fitted on most good samples)
- BW800 Drive (8/8)
- Basic CIC (8/8)
- Boosted Reactor (7/8)
- R400 Radar (8/8)
- Rapid DC Locker (7/8)
- Reinforced Magazine (8/8)
- Track Correlator (8/8)
- VLS-1-23 Launcher (7/8)

## Common parts (40-70%)
- R550 Early Warning Radar (5/8)

## Optional parts
- Auxiliary Steering (1/8)
- Civilian Reactor (1/8)
- Small DC Locker (1/8)
- T20 Cannon (1/8)
- VLS-1-46 Launcher (1/8)

## Sample ships (good)
- Eager Mover (TF Purple Joy 2, 217 pts, Chinese starter pack)
- Eager Mover (TF Purple Joy 2, 258 pts, Chinese starter pack)
- Mired Act (CC LN test 1, 258 pts, Chinese starter pack)
- Ink Spirit (CC LN test 1, 258 pts, Chinese starter pack)
- Until The End (Kyanite Squadron, 252 pts, example fleet)
- Comet (Comet Squadron, 249 pts, player save)

## 样板船完整装配（整艘照抄）：Eager Mover（TF Purple Joy 2）

**整艘照抄**：舰体 `Tugboat`（阵营键 `Stock/Outlying Systems Protectorate`），存档原值 **258 点**，共 10 个槽位。复制这艘船时连它自带的导弹一起抄，只改船名、呼号和导弹名。

| 槽位 | 部件 | 尺寸 | 点数 | 供电 kW |
|---|---|---|---:|---:|
| MT1 | R400 'Bloodhound' LRT Radar | 2x5x2 | 15 | -3000 |
| MT3 | R550 Early Warning Radar | 3x1x3 | 40 | -4500 |
| MT5 | VLS-1-23 Launcher | 2x2x2 | 5 | -50 |
| CMP2 | Reinforced Magazine | 1x1x1 | 0 → 之后 40/座 | 0 |
| CMP4 | Rapid DC Locker | 3x1x3 | 10 | 0 |
| CMP5 | Basic CIC | 4x1x6 | 10 | 0 |
| MOD1 | Boosted Reactor | 5x5x5 | 10 | +5000 |
| MOD2 | BW800 Drive | 5x3x5 | 10 | 0 |
| MOD3 | Track Correlator | 2x2x2 | 25 | -150 |
| MOD4 | Track Correlator | 2x2x2 | 25 | -150 |

- 合计：部件 150 点 + 舰体 100 点 = **250 点**（不含弹库与弹药，见下）
- 另有弹库 0 点 + 弹药 8 点 ⇒ **全价约 258 点**（估算；游戏里以存档原值 258 为准，单价见 `zh/弹药点数表.md`）
- 供电：发电 5000 kW / 耗电 7850 kW（余量 -2850 kW）
- 弹库装载：MT5 VLS-1-23 Launcher：SGM-103 Balestra Block II ×1、EA12 Chaff Decoy ×7


## 样板船完整装配（整艘照抄）：Mired Act（CC LN test 1）

**整艘照抄**：舰体 `Tugboat`（阵营键 `Stock/Outlying Systems Protectorate`），存档原值 **258 点**，共 10 个槽位。复制这艘船时连它自带的导弹一起抄，只改船名、呼号和导弹名。

| 槽位 | 部件 | 尺寸 | 点数 | 供电 kW |
|---|---|---|---:|---:|
| MT1 | R400 'Bloodhound' LRT Radar | 2x5x2 | 15 | -3000 |
| MT3 | R550 Early Warning Radar | 3x1x3 | 40 | -4500 |
| MT5 | VLS-1-23 Launcher | 2x2x2 | 5 | -50 |
| CMP1 | Basic CIC | 4x1x6 | 10 | 0 |
| CMP2 | Reinforced Magazine | 1x1x1 | 0 → 之后 40/座 | 0 |
| CMP5 | Rapid DC Locker | 3x1x3 | 10 | 0 |
| MOD1 | Boosted Reactor | 5x5x5 | 10 | +5000 |
| MOD2 | BW800 Drive | 5x3x5 | 10 | 0 |
| MOD3 | Track Correlator | 2x2x2 | 25 | -150 |
| MOD4 | Track Correlator | 2x2x2 | 25 | -150 |

- 合计：部件 150 点 + 舰体 100 点 = **250 点**（不含弹库与弹药，见下）
- 另有弹库 0 点 + 弹药 8 点 ⇒ **全价约 258 点**（估算；游戏里以存档原值 258 为准，单价见 `zh/弹药点数表.md`）
- 供电：发电 5000 kW / 耗电 7850 kW（余量 -2850 kW）
- 弹库装载：MT5 VLS-1-23 Launcher：SGM-101 OA ×1、EA12 Chaff Decoy ×7


## Author notes (from the fleet's 使用说明.txt)
- TF Purple Joy 2: *舰队定位：前排/中近距离输出 / *上手难度：中 / *舰船说明 / --1，2号两条线列舰主武器是离子炮+100mm炮组合。离子炮烧毁目标装甲后用100mm炮的高输出快速击沉。船上装备S1防空导弹，使用时手动发射或者将点防御控制器设置成point。 / --3号拖船辅助舰，有EO干扰，10公里视野的雷达和防空导弹。防空导弹通过TALS-2能自动一轮发射两发，MLS-2不能自动发射但是能一轮打四发。总共一轮六发。 / --4号拖船是LRT锁定船，在后方提供火控数据 / *优点： / --中近距离（100mm炮射程内）对敌方所有舰艇输出极高，理论上比任意450mm火炮舰队高 / --能软杀巡航导弹；面对战机有防空导弹和100mm的多用途炮 / --线列舰备件数量很多，机动性不错。 / *缺点： / --未装备CMD干扰（新人如果搞不定软杀装了也没用。所以请自行安装） / --射程比250mm火炮还近，离光束最大射程不远 / --反电子战设备只有pinpoint和后方的LRT雷达 / --点防御火力只有防空导弹且数量不多 / 使用注意事项： / 1.线列舰（LN）的耐打建立在能时不时缩回掩体里面修。尽量不要离掩体太远。也不要被太多敌方舰艇集火。 / 2.本舰队线列舰两弦的火炮可以同时朝上，下方射击。所以尽量手动用天花板对准目标。如果觉得手动对准很累，天花板上面还有一门250mm炮。用250mm炮攻击目标会自动让LN的天花板对准。 / 3.本舰队LN航速一般，撤退需要及时。但是加速很快。 / 4.轻巡舰队可以在6.5公里外回避很多离子炮，且装甲能顶住100mm炮。不要和轻巡队硬拼。…
- TF Purple Joy 2: *舰队定位：前排/中近距离输出 / *上手难度：中 / *舰船说明 / --1，2号两条线列舰主武器是离子炮+100mm炮组合。离子炮烧毁目标装甲后用100mm炮的高输出快速击沉。船上装备S1防空导弹，使用时手动发射或者将点防御控制器设置成point并关掉发射导弹帮助队友的选项。 / --3号拖船辅助舰，有EO干扰，10公里视野的雷达和防空导弹。防空导弹通过TALS-2能自动一轮发射两发，MLS-2不能自动发射但是能一轮打四发。总共一轮六发。 / --4号拖船是EWR+LRT锁定船，在后方提供火控数据和早期警戒。拖船没有足够的电同时运行EWR和LRT所以只能2选1。 / *优点： / --中近距离（100mm炮射程内）对敌方所有舰艇输出极高，理论上比任意450mm火炮舰队高 / --能软杀巡航导弹；面对战机有防空导弹和100mm的多用途炮 / --线列舰备件数量很多，机动性不错。 / *缺点： / --未装备CMD干扰（新人如果搞不定软杀装了也没用。如有需求请自行安装） / --射程比250mm火炮还近，离光束最大射程（6km）不远 / --反电子战设备只有pinpoint和后方的LRT雷达 / --点防御火力只有防空导弹且数量不多(每条船23发） / 使用注意事项： / 1.线列舰（LN）的耐打建立在能时不时缩回掩体里面修。尽量不要离掩体太远。也不要被太多敌方舰艇集火。 / 2.本舰队线列舰两弦的火炮可以同时朝上，下方射击。所以尽量手动用天花板对准目标。如果觉得手动对准很累，天花板上面还有一门250mm炮。用250mm炮攻击目标会自动让LN的天花板对准。 / 3.本舰队LN航…
- CC LN test 1: *舰队定位：前排/中远程火炮输出 / *上手难度：高（比战列舰容易，但是有限） / *武装说明 / --指挥巡洋舰（CC）有6管450mm火炮，垂发中的S1导弹为防空导弹。装备泛光灯对抗雷达干扰。 / --二号线列舰（LN）主武器450mm弹夹炮。另有100mm副炮，EO干扰器，和各种诱饵。装备的KJ导弹是SSJ诱饵。设成手动按Z发射。 / --三号拖船装备EWR+LRT雷达。因为电量限制，两个雷达不能同时工作。 / --舰队装备全软杀，理论上所以引导头组合都能软杀。 / *优点： / --OSP的六边形战士 / --CC能打能扛还能提供ECCM / --CC在9km外能通过环绕指令有效回避450mm炮弹 / --LN的450mm弹夹炮高爆发；100mm副炮能打小船 / --LN可以依靠CC的火控数据躲在敌方Bulls Eye锁定范围外输出 / --拖船既可以提供18KM的早期预警，也可以提供14km的长程火控。 / *缺点： / --非常怕被打交叉火力 / --点防御搞不定大批量导弹，需要软杀 / 使用注意事项： / 1.CC虽然能躲炮弹，但是距离太近或者被敌方打交叉火力就不行了 / 2.CC需要时刻将船艏指向来袭火力的大致方向。侧面挨打很伤。 / 3.CC航速一般，撤退需要及时。不要离掩体太远。 / 4.S1防空导弹数量少，一定要手动发射； / 5.LN身上的集装箱导弹是SSJ诱饵，请设置成手动发射然后对有Hoj引导头的导弹按Z发射； / LN背后还有两发诱饵集装箱，看见arad或[arad]时手动发射 / 6.LN需要手动提前转向，把有炮的侧面对准敌方可能出现的位置，然后…

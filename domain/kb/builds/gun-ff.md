# gun FF

Tags: kind=build template; class=gun FF; cost=250-400; samples=16; good=7
Keywords: build, loadout, template, 配装, 配置, 装配, 模板, 舰级, gun FF
Summary: gun FF build; 16 matched ships, 7 of them are good samples (must and should both pass); typical cost 371 (range 330-397); hull Raines Frigate Class×7.
Section: build templates; requirements from other info/Ship Builds.txt; samples from player fleets

## How to read this
回答「这艘船算不算 / 合不合格」以 Requirements 段为准（must 全过才算这个舰级，should 是良好标准）；部件清单只统计 good 样本，频率 (k/N) 表示常见程度，不是硬性要求。所有舰船先要过通用基线（`reference/baseline-requirements.md`），再看本舰级要求。

## 舰级要求（Ship Builds.txt 原文，作为判定依据）

**舰级硬性要求（required：缺一条就不算这个舰级）**
- have at least 2 120 turrets

**良好标准（should：缺了算有瑕疵，但仍算这个舰级）**
- have at least 3 gun turrets
- have minimal DC (have at least 1 restore)

**可选加分（optional）**
- have at least 1 250 turret
- have 1 parallax radar or spyglass radar
- have Track Correlator if spyglass radar
- have minimal softkill
- have 1 jammer of any type

## Disclaimer
参考配置，不是最优解。样本是玩家舰队里 must + should 全过的真实配装（主要取自中文新手包 v1.12，对应游戏 0.6.2.3；其余来自 other info 与本地存档）。旧版本可能改过数值或改过名字；模组部件不代表原版能照抄。把它当起步模板，不要当配方。

## Numbers
- Point cost: 250-400 (good-sample median 371, range 330-397)
- Power: draw 2650 kW / supply 4850 kW (median)
- Hull: Raines Frigate Class×7

## Armament (good samples)
- 120 mm turret/cannon: 7/7 ships, median 2 (min 2, max 2)
- 250 mm turret/cannon: 6/7 ships, median 2 (min 1, max 2)
- VLS-1-46 launcher: 1/7 ships

## Core parts (fitted on most good samples)
- Ammunition Elevators (6/7)
- Basic CIC (7/7)
- FM230 'Whiplash' Drive (5/7)
- FR4800 Reactor (7/7)
- Mk62 Cannon (7/7)
- Mk64 Cannon (6/7)
- RS35 'Frontline' Radar (5/7)
- Reinforced Magazine (7/7)
- Small DC Locker (7/7)

## Common parts (40-70%)
- Auxiliary Steering (4/7)

## Optional parts
- ES32 'Scryer' Missile ID System (2/7)
- FM200 Drive (2/7)
- RM50 'Parallax' Radar (2/7)
- Rapid DC Locker (2/7)
- E90 'Blanket' Jammer (1/7)
- RF101 'Bullseye' Radar (1/7)
- VLS-1-46 Launcher (1/7)

## Sample ships (good)
- Peel of Agnesse (HC Gun Missile test 8, 397 pts, Chinese starter pack)
- Pizza? (Another 6k, 330 pts, player save)
- Brew (masqford, 371 pts, player save)
- Irony (masqford, 371 pts, player save)
- Brew (All 34 sample ships · Alliance, 371 pts, player save)
- Maxim and Money (masqford, 388 pts, player save)

## 样板船完整装配（整艘照抄）：Peel of Agnesse（HC Gun Missile test 8）

**整艘照抄**：舰体 `Raines Frigate`（阵营键 `Stock/Shelter Alliance`），存档原值 **397 点**，共 14 个槽位。复制这艘船时连它自带的导弹一起抄，只改船名、呼号和导弹名。

| 槽位 | 部件 | 尺寸 | 点数 | 供电 kW |
|---|---|---|---:|---:|
| MT1 | Mk62 Cannon | 3x1x3 | 20 | -50 |
| MT2 | Mk62 Cannon | 3x1x3 | 20 | -50 |
| MT3 | Mk64 Cannon | 3x1x5 | 30 | -125 |
| MT4 | Mk64 Cannon | 3x1x5 | 30 | -125 |
| CMP1 | Basic CIC | 4x1x6 | 10 | 0 |
| CMP2 | Reinforced Magazine | 1x1x1 | 0 → 之后 40/座 | 0 |
| CMP3 | Small DC Locker | 3x1x3 | 20 | 0 |
| CMP4 | Rapid DC Locker | 3x1x3 | 10 | 0 |
| CMP5 | Rapid DC Locker | 3x1x3 | 10 | 0 |
| MOD1 | FR4800 Reactor | 5x5x5 | 10 | +4200 |
| MOD2 | FM200 Drive | 5x3x5 | 10 | 0 |
| MOD3 | ES32 'Scryer' Missile ID System | 2x2x2 | 10 | -300 |
| MOD4 | Ammunition Elevators | 2x2x2 | 20 | -150 |
| MOD5 | RM50 'Parallax' Radar | 2x2x2 | 45 | -3600 |

- 合计：部件 245 点 + 舰体 125 点 = **370 点**（不含弹库与弹药，见下）
- 另有弹库 0 点 + 弹药 27 点 ⇒ **全价约 397 点**（估算；游戏里以存档原值 397 为准，单价见 `zh/弹药点数表.md`）
- 供电：发电 4200 kW / 耗电 4400 kW（余量 -200 kW）
- 弹库装载：CMP2 Reinforced Magazine：250mm HE Shell ×200、250mm HE-RPF Shell ×200、250mm AP Shell ×200、120mm HE Shell ×500、120mm HE-RPF Shell ×500、120mm AP Shell ×500


## 样板船完整装配（整艘照抄）：Brew（masqford）

**整艘照抄**：舰体 `Raines Frigate`（阵营键 `Stock/Shelter Alliance`），存档原值 **371 点**，共 13 个槽位。复制这艘船时连它自带的导弹一起抄，只改船名、呼号和导弹名。

| 槽位 | 部件 | 尺寸 | 点数 | 供电 kW |
|---|---|---|---:|---:|
| MT1 | Mk62 Cannon | 3x1x3 | 20 | -50 |
| MT2 | Mk62 Cannon | 3x1x3 | 20 | -50 |
| MT3 | Mk64 Cannon | 3x1x5 | 30 | -125 |
| MT4 | Mk64 Cannon | 3x1x5 | 30 | -125 |
| CMP1 | Reinforced Magazine | 1x1x1 | 0 → 之后 40/座 | 0 |
| CMP2 | Basic CIC | 4x1x6 | 10 | 0 |
| CMP3 | Small DC Locker | 3x1x3 | 20 | 0 |
| CMP5 | Auxiliary Steering | 3x1x3 | 10 | 0 |
| MOD1 | FR4800 Reactor | 5x5x5 | 10 | +4200 |
| MOD2 | FM230 'Whiplash' Drive | 5x3x5 | 20 | 0 |
| MOD3 | RS35 'Frontline' Radar | 2x2x2 | 10 | -2000 |
| MOD4 | Ammunition Elevators | 2x2x2 | 20 | -150 |
| MOD5 | Ammunition Elevators | 2x2x2 | 20 | -150 |

- 合计：部件 220 点 + 舰体 125 点 = **345 点**（不含弹库与弹药，见下）
- 另有弹库 0 点 + 弹药 26 点 ⇒ **全价约 371 点**（估算；游戏里以存档原值 371 为准，单价见 `zh/弹药点数表.md`）
- 供电：发电 4200 kW / 耗电 2650 kW（余量 +1550 kW）
- 弹库装载：CMP1 Reinforced Magazine：250mm HE-RPF Shell ×200、250mm AP Shell ×200、250mm HE Shell ×200、120mm HE-RPF Shell ×400、120mm AP Shell ×500、120mm HE Shell ×500


## Author notes (from the fleet's 使用说明.txt)
- HC Gun Missile test 8: *舰队定位：半前排/中远程火炮输出+导弹收割 / *上手难度：高 / （该舰队本不应出现在新手包里面。但我知道新手肯定会试着去搓火炮+二级导弹的混合舰队所以干脆放在这里给你们当参考） / *武装说明 / 1.重巡有5管450mm火炮。 / 2.重巡带的Bread Stick导弹为防空导弹。使用时将建议将防空导弹发射控制设置成"手动"模式以免乱打。 / 3.重巡携带的SGM-H-301 Atlatl系列导弹有五个子型号。分别在后面加了数字1,2,3,4,5。设计的全弹发射有4波，每波5发。分别为两波次，5发SGM-H-301 Atlatl 1的单种类导弹打击波;和两波次SGM-H-301 Atlatl 1,2,3,4,5各一发的混合导弹打击波。所有导弹打击波都建议用来收割受伤的大型目标（线列舰，航母和指挥巡洋舰）目标为给货船（MN）时适当缩小打击波，例如一个目标打三发导弹。发射导弹时请启动干扰护卫舰舰上的雷达干扰和重巡上的泛光灯。 / 4.二号舰是干扰轻护卫舰。建议和重巡一起编队。 / 5.三号舰火炮护卫舰。建议开局和重巡一起走。优先打对面小船。 / 6.本舰队装备全软杀。 / *优点： / --拥有一定的扛线和炮击能力 / --拥有二级导弹，能快速收割受伤目标，或打伤点防御差的目标 / --有全软杀和 / --有适量电子战 / --在9.5km外能通过环绕指令有效回避450mm炮弹 / *缺点： / --主力只有一条重巡，死了就没了 / --大量软杀/电子战设备集中在轻护卫舰上面，被打坏就没了 / --航速一般 / --点防御火力只有俩防卫者 / --S3H导弹第一级速度很慢，…

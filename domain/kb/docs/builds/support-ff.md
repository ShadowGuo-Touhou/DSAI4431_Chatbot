# support FF

Tags: kind=build template; class=support FF; cost=300-700; samples=36; good=20
Keywords: build, loadout, template, 配装, 配置, 装配, 模板, 舰级, support FF
Summary: support FF build; 36 matched ships, 20 of them are good samples (must and should both pass); typical cost 460 (range 330-571); hull Raines Frigate Class×20.
Section: build templates; requirements from other info/Ship Builds.txt; samples from player fleets

## How to read this
回答「这艘船算不算 / 合不合格」以 Requirements 段为准（must 全过才算这个舰级，should 是良好标准）；部件清单只统计 good 样本，频率 (k/N) 表示常见程度，不是硬性要求。所有舰船先要过通用基线（`reference/baseline-requirements.md`），再看本舰级要求。

## 舰级要求（Ship Builds.txt 原文，作为判定依据）

**舰级硬性要求（required：缺一条就不算这个舰级）**
- have no turrets

**良好标准（should：缺了算有瑕疵，但仍算这个舰级）**
- have minimal DC (at least 1 restore)
- have minimal softkill

**可选加分（optional）**
- have at least 1 Sarissa PDT
- have 1 vls-2 launcher
- ^have defensive missiles
- have jammer of any type
- have better softkill

## Disclaimer
参考配置，不是最优解。样本是玩家舰队里 must + should 全过的真实配装（主要取自中文新手包 v1.12，对应游戏 0.6.2.3；其余来自 other info 与本地存档）。旧版本可能改过数值或改过名字；模组部件不代表原版能照抄。把它当起步模板，不要当配方。

## Numbers
- Point cost: 300-700 (good-sample median 460, range 330-571)
- Power: draw 5850 kW / supply 5900 kW (median)
- Hull: Raines Frigate Class×20

## Armament (good samples)
- VLS-2 launcher: 5/20 ships
- VLS-1-46 launcher: 5/20 ships
- VLS-1-23 launcher: 5/20 ships
- VLS-3 launcher: 3/20 ships

## Core parts (fitted on most good samples)
- E90 'Blanket' Jammer (17/20)
- FM230 'Whiplash' Drive (14/20)
- FR4800 Reactor (20/20)
- Rapid DC Locker (14/20)
- Reinforced Magazine (20/20)

## Common parts (40-70%)
- Actively Cooled Amplifiers (9/20)
- Auxiliary Steering (8/20)
- Basic CIC (9/20)
- E71 'Hangup' Jammer (8/20)
- FR3300 Micro Reactor (10/20)
- RS35 'Frontline' Radar (10/20)
- RS41 'Spyglass' Radar (8/20)
- Reinforced CIC (11/20)
- Reinforced DC Locker (8/20)
- Small DC Locker (12/20)

## Optional parts
- Plant Control Center (7/20)
- E70 'Interruption' Jammer (6/20)
- FM200 Drive (6/20)
- VLS-1-23 Launcher (6/20)
- VLS-1-46 Launcher (5/20)
- ES32 'Scryer' Missile ID System (4/20)
- Mk90 'Aurora' PDT (4/20)
- VLS-2 Launcher (4/20)
- RF101 'Bullseye' Radar (3/20)
- VLS-3 Launcher (3/20)
- E55 'Floodlight' Illuminator (2/20)
- Large DC Locker (2/20)

## Sample ships (good)
- Beige of Cleland (hc gun dd test 11, 461 pts, Chinese starter pack)
- Sale (hc gun dd test 11, 485 pts, Chinese starter pack)
- Pizza? (Another 6k (3), 330 pts, player save)
- Sale (All 34 sample ships · Alliance, 344 pts, player save)
- Beige of Cleland (All 34 sample ships · Alliance, 370 pts, player save)
- Rowland B. Hauger (All Craft Are Bastards, 411 pts, player save)

## 样板船完整装配（整艘照抄）：Beige of Cleland（hc gun dd test 11）

**整艘照抄**：舰体 `Raines Frigate`（阵营键 `Stock/Shelter Alliance`），存档原值 **461 点**，共 12 个槽位。复制这艘船时连它自带的导弹一起抄，只改船名、呼号和导弹名。

| 槽位 | 部件 | 尺寸 | 点数 | 供电 kW |
|---|---|---|---:|---:|
| MT1 | VLS-1-23 Launcher | 2x2x2 | 5 | -50 |
| MT2 | E70 'Interruption' Jammer | 3x1x3 | 55 | -600 |
| MT3 | VLS-3 Launcher | 3x4x3 | 20 | -200 |
| MT4 | E90 'Blanket' Jammer | 2x1x2 | 50 | -1000 |
| CMP1 | Basic CIC | 4x1x6 | 10 | 0 |
| CMP3 | Small DC Locker | 3x1x3 | 20 | 0 |
| CMP4 | Auxiliary Steering | 3x1x3 | 10 | 0 |
| CMP5 | Reinforced Magazine | 1x1x1 | 0 → 之后 40/座 | 0 |
| MOD1 | FR4800 Reactor | 5x5x5 | 10 | +4200 |
| MOD2 | FM200 Drive | 5x3x5 | 10 | 0 |
| MOD3 | RS41 'Spyglass' Radar | 2x2x2 | 25 | -4000 |
| MOD5 | FR3300 Micro Reactor | 3x3x3 | 10 | +2250 |

- 合计：部件 225 点 + 舰体 125 点 = **350 点**（不含弹库与弹药，见下）
- 另有弹库 0 点 + 弹药 111 点 ⇒ **全价约 461 点**（估算；游戏里以存档原值 461 为准，单价见 `zh/弹药点数表.md`）
- 供电：发电 6450 kW / 耗电 5850 kW（余量 +600 kW）
- 弹库装载：MT1 VLS-1-23 Launcher：SGM-100 Balestra ×1、EA12 Chaff Decoy ×13、EA20 Flare Decoy ×7；MT3 VLS-3 Launcher：SGM-H-310 BFR ×6


## 样板船完整装配（整艘照抄）：Sale（hc gun dd test 11）

**整艘照抄**：舰体 `Raines Frigate`（阵营键 `Stock/Shelter Alliance`），存档原值 **485 点**，共 11 个槽位。复制这艘船时连它自带的导弹一起抄，只改船名、呼号和导弹名。

| 槽位 | 部件 | 尺寸 | 点数 | 供电 kW |
|---|---|---|---:|---:|
| MT1 | E70 'Interruption' Jammer | 3x1x3 | 55 | -600 |
| MT2 | E90 'Blanket' Jammer | 2x1x2 | 50 | -1000 |
| MT3 | VLS-2 Launcher | 3x4x3 | 10 | -200 |
| MT4 | VLS-1-23 Launcher | 2x2x2 | 5 | -50 |
| CMP1 | Basic CIC | 4x1x6 | 10 | 0 |
| CMP3 | Small DC Locker | 3x1x3 | 20 | 0 |
| CMP5 | Reinforced Magazine | 1x1x1 | 0 → 之后 40/座 | 0 |
| MOD1 | FR4800 Reactor | 5x5x5 | 10 | +4200 |
| MOD2 | FM200 Drive | 5x3x5 | 10 | 0 |
| MOD3 | RS41 'Spyglass' Radar | 2x2x2 | 25 | -4000 |
| MOD5 | FR3300 Micro Reactor | 3x3x3 | 10 | +2250 |

- 合计：部件 205 点 + 舰体 125 点 = **330 点**（不含弹库与弹药，见下）
- 另有弹库 0 点 + 弹药 155 点 ⇒ **全价约 485 点**（估算；游戏里以存档原值 485 为准，单价见 `zh/弹药点数表.md`）
- 供电：发电 6450 kW / 耗电 5850 kW（余量 +600 kW）
- 弹库装载：MT3 VLS-2 Launcher：-491APZt5UelPA5ml2kF9w ×14；MT4 VLS-1-23 Launcher：SGM-100 Balestra ×1、EA12 Chaff Decoy ×7、EA20 Flare Decoy ×7


## Author notes (from the fleet's 使用说明.txt)
- hc gun dd test 11: *舰队定位：半前排/中远程火炮输出+导弹收割 / *上手难度：高 / （该舰队本不应出现在新手包里面。但我知道新手肯定会试着去搓火炮+二级导弹的混合舰队所以干脆放在这里给你们当参考） / *武装说明 / 1.重巡有5管450mm火炮和两台120mm火炮。450打大船120打小船。 / 2.重巡和轻护带的SGM-H-310 BFR导弹为防空导弹。使用时将防御导弹发射控制设置成"手动"，然后重巡锁定敌方飞机后按Z发射 / 3.重巡携带的SGM-H-301 Atlatl系列导弹有五个子型号。分别在后面加了数字1,2,3,4,5。设计的全弹发射有3波，每波5发。分别为一波次，5发SGM-H-301 Atlatl 1的单种类导弹打击波;和两波次SGM-H-301 Atlatl 1,2,3,4,5各一发的混合导弹打击波。所有导弹打击波都建议用来收割受伤的大型目标（线列舰，航母和指挥巡洋舰）目标为给货船（MN）时适当缩小打击波，例如一个目标打三发导弹。发射导弹时请启动三号舰上的雷达干扰和重巡上的泛光灯。 / 4.二号舰是船棍磁轨炮驱逐，建议挂在大后方射击帮助重巡。 / 5.三号舰为辅助护卫舰，上有防空导弹，软杀设备和雷达干扰。 / 6.本舰队装备类全软杀，除"Eact[cmd]拒绝"引导头外，别的引导头都能软杀。 / *优点： / --拥有一定的扛线和炮击能力 / --拥有二级导弹，能快速收割受伤目标，或打伤点防御差的目标 / --有类全软杀和足够多的防空导弹 / --有一台雷达干扰稍微干扰一下 / --在9.5km外能通过环绕指令有效回避450mm炮弹 / *缺点： / --未装备 真.全…

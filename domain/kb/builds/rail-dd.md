# Rail DD

Tags: kind=build template; class=Rail DD; cost=400-800; samples=20; good=7
Keywords: build, loadout, template, 配装, 配置, 装配, 模板, 舰级, Rail DD
Summary: Rail DD build; 20 matched ships, 7 of them are good samples (must and should both pass); typical cost 465 (range 452-768); hull Keystone Destroyer Class×7.
Section: build templates; requirements from other info/Ship Builds.txt; samples from player fleets

## How to read this
回答「这艘船算不算 / 合不合格」以 Requirements 段为准（must 全过才算这个舰级，should 是良好标准）；部件清单只统计 good 样本，频率 (k/N) 表示常见程度，不是硬性要求。所有舰船先要过通用基线（`reference/baseline-requirements.md`），再看本舰级要求。

## 舰级要求（Ship Builds.txt 原文，作为判定依据）

**舰级硬性要求（required：缺一条就不算这个舰级）**
- have 1 Mk550 railgun as spinal weapon (mount 7)

**良好标准（should：缺了算有瑕疵，但仍算这个舰级）**
- have minimal DC (1 rapid DC Locker)
- have at least 1 Energy Regulator
- have minimal softkill

**可选加分（optional）**
- have minimal hardkill
- have better DC (at least 1 restores)
- have at least 2 Energy Regulator

## Disclaimer
参考配置，不是最优解。样本是玩家舰队里 must + should 全过的真实配装（主要取自中文新手包 v1.12，对应游戏 0.6.2.3；其余来自 other info 与本地存档）。旧版本可能改过数值或改过名字；模组部件不代表原版能照抄。把它当起步模板，不要当配方。

## Numbers
- Point cost: 400-800 (good-sample median 465, range 452-768)
- Power: draw 4000 kW / supply 4700 kW (median)
- Hull: Keystone Destroyer Class×7

## Armament (good samples)
- 120 mm turret/cannon: 1/7 ships, median 1 (min 1, max 1)
- VLS-1-23 launcher: 5/7 ships
- VLS-1-46 launcher: 2/7 ships

## Core parts (fitted on most good samples)
- Basic CIC (6/7)
- Energy Regulator (7/7)
- FM240 'Dragonfly' Drive (5/7)
- FR4800 Reactor (7/7)
- Mk550 Railgun (7/7)
- Rapid DC Locker (5/7)
- Reinforced Magazine (7/7)
- Small DC Locker (5/7)
- VLS-1-23 Launcher (5/7)

## Common parts (40-70%)
- Auxiliary Steering (4/7)

## Optional parts
- FM200 Drive (2/7)
- FR3300 Micro Reactor (2/7)
- Mk20 'Defender' PDT (2/7)
- Small Energy Regulator (2/7)
- VLS-1-46 Launcher (2/7)
- ES22 'Pinard' Electronic Support Module (1/7)
- Intelligence Center (1/7)
- Mk62 Cannon (1/7)
- Mk95 'Sarissa' PDT (1/7)
- RS35 'Frontline' Radar (1/7)
- Reinforced CIC (1/7)

## Sample ships (good)
- BFG (hc gun dd test 11, 453 pts, Chinese starter pack)
- BFR (hc gun dd test 11, 466 pts, Chinese starter pack)
- Singing Mantle (TF Redwood, 465 pts, example fleet)
- Rime of Solitas (TF Redwood, 490 pts, example fleet)
- BFG (All 34 sample ships · Alliance, 452 pts, player save)
- BFR (All 34 sample ships · Alliance, 465 pts, player save)

## 样板船完整装配（整艘照抄）：BFR（hc gun dd test 11）

**整艘照抄**：舰体 `Keystone Destroyer`（阵营键 `Stock/Shelter Alliance`），存档原值 **466 点**，共 12 个槽位。复制这艘船时连它自带的导弹一起抄，只改船名、呼号和导弹名。

| 槽位 | 部件 | 尺寸 | 点数 | 供电 kW |
|---|---|---|---:|---:|
| MT5 | VLS-1-23 Launcher | 2x2x2 | 5 | -50 |
| MT7 | Mk550 Mass Driver | — | — | 0 |
| CMP3 | Basic CIC | 4x1x6 | 10 | 0 |
| CMP4 | Small DC Locker | 3x1x3 | 20 | 0 |
| CMP5 | Reinforced Magazine | 1x1x1 | 0 → 之后 40/座 | 0 |
| CMP6 | Auxiliary Steering | 3x1x3 | 10 | 0 |
| CMP7 | Rapid DC Locker | 3x1x3 | 10 | 0 |
| MOD1 | FR4800 Reactor | 5x5x5 | 10 | +4200 |
| MOD2 | FM240 'Dragonfly' Drive | 5x3x5 | 20 | 0 |
| MOD3 | Energy Regulator | 3x3x3 | 30 | -650 |
| MOD4 | Energy Regulator | 3x3x3 | 30 | -650 |
| MOD7 | Energy Regulator | 3x3x3 | 30 | -650 |

- 合计：部件 175 点 + 舰体 200 点 = **375 点**（不含弹库与弹药，见下）
- 另有弹库 0 点 + 弹药 16 点 ⇒ **全价约 391 点**（估算；游戏里以存档原值 466 为准，单价见 `zh/弹药点数表.md`）
- 供电：发电 4200 kW / 耗电 2000 kW（余量 +2200 kW）
- 弹库装载：MT5 VLS-1-23 Launcher：EA12 Chaff Decoy ×6、SGM-100 Balestra ×1；CMP5 Reinforced Magazine：300mm AP Rail Sabot ×225


## 样板船完整装配（整艘照抄）：BFG（hc gun dd test 11）

**整艘照抄**：舰体 `Keystone Destroyer`（阵营键 `Stock/Shelter Alliance`），存档原值 **453 点**，共 11 个槽位。复制这艘船时连它自带的导弹一起抄，只改船名、呼号和导弹名。

| 槽位 | 部件 | 尺寸 | 点数 | 供电 kW |
|---|---|---|---:|---:|
| MT5 | VLS-1-23 Launcher | 2x2x2 | 5 | -50 |
| MT7 | Mk550 Mass Driver | — | — | 0 |
| CMP3 | Basic CIC | 4x1x6 | 10 | 0 |
| CMP4 | Small DC Locker | 3x1x3 | 20 | 0 |
| CMP5 | Reinforced Magazine | 1x1x1 | 0 → 之后 40/座 | 0 |
| CMP6 | Auxiliary Steering | 3x1x3 | 10 | 0 |
| MOD1 | FR4800 Reactor | 5x5x5 | 10 | +4200 |
| MOD2 | FM240 'Dragonfly' Drive | 5x3x5 | 20 | 0 |
| MOD3 | Energy Regulator | 3x3x3 | 30 | -650 |
| MOD4 | Energy Regulator | 3x3x3 | 30 | -650 |
| MOD7 | Energy Regulator | 3x3x3 | 30 | -650 |

- 合计：部件 165 点 + 舰体 200 点 = **365 点**（不含弹库与弹药，见下）
- 另有弹库 0 点 + 弹药 13 点 ⇒ **全价约 378 点**（估算；游戏里以存档原值 453 为准，单价见 `zh/弹药点数表.md`）
- 供电：发电 4200 kW / 耗电 2000 kW（余量 +2200 kW）
- 弹库装载：MT5 VLS-1-23 Launcher：EA12 Chaff Decoy ×6、SGM-100 Balestra ×1；CMP5 Reinforced Magazine：300mm AP Rail Sabot ×150


## Author notes (from the fleet's 使用说明.txt)
- hc gun dd test 11: *舰队定位：半前排/中远程火炮输出+导弹收割 / *上手难度：高 / （该舰队本不应出现在新手包里面。但我知道新手肯定会试着去搓火炮+二级导弹的混合舰队所以干脆放在这里给你们当参考） / *武装说明 / 1.重巡有5管450mm火炮和两台120mm火炮。450打大船120打小船。 / 2.重巡和轻护带的SGM-H-310 BFR导弹为防空导弹。使用时将防御导弹发射控制设置成"手动"，然后重巡锁定敌方飞机后按Z发射 / 3.重巡携带的SGM-H-301 Atlatl系列导弹有五个子型号。分别在后面加了数字1,2,3,4,5。设计的全弹发射有3波，每波5发。分别为一波次，5发SGM-H-301 Atlatl 1的单种类导弹打击波;和两波次SGM-H-301 Atlatl 1,2,3,4,5各一发的混合导弹打击波。所有导弹打击波都建议用来收割受伤的大型目标（线列舰，航母和指挥巡洋舰）目标为给货船（MN）时适当缩小打击波，例如一个目标打三发导弹。发射导弹时请启动三号舰上的雷达干扰和重巡上的泛光灯。 / 4.二号舰是船棍磁轨炮驱逐，建议挂在大后方射击帮助重巡。 / 5.三号舰为辅助护卫舰，上有防空导弹，软杀设备和雷达干扰。 / 6.本舰队装备类全软杀，除"Eact[cmd]拒绝"引导头外，别的引导头都能软杀。 / *优点： / --拥有一定的扛线和炮击能力 / --拥有二级导弹，能快速收割受伤目标，或打伤点防御差的目标 / --有类全软杀和足够多的防空导弹 / --有一台雷达干扰稍微干扰一下 / --在9.5km外能通过环绕指令有效回避450mm炮弹 / *缺点： / --未装备 真.全…

# 250 gun CL

Tags: kind=build template; class=250 gun CL; cost=800-1200; samples=38; good=22
Keywords: build, loadout, template, 配装, 配置, 装配, 模板, 舰级, 250 gun CL
Summary: 250 gun CL build; 38 matched ships, 22 of them are good samples (must and should both pass); typical cost 1002 (range 932-1191); hull Vauxhall Light Cruiser Class×22.
Section: build templates; requirements from other info/Ship Builds.txt; samples from player fleets

## How to read this
回答「这艘船算不算 / 合不合格」以 Requirements 段为准（must 全过才算这个舰级，should 是良好标准）；部件清单只统计 good 样本，频率 (k/N) 表示常见程度，不是硬性要求。所有舰船先要过通用基线（`reference/baseline-requirements.md`），再看本舰级要求。

## 舰级要求（Ship Builds.txt 原文，作为判定依据）

**舰级硬性要求（required：缺一条就不算这个舰级）**
- have at least 1 250mm turret (mount 1-4, 6)

**良好标准（should：缺了算有瑕疵，但仍算这个舰级）**
- have at least 4 250 turret (mount 1-4, 6)
- have minimal DC (at least 2 restores)
- have minimal softkill
- have minimal hardkill
- have at least 2 CIC and/or Auxiliary Steering
- have 1 FM230/FM530 whiplash drive

**可选加分（optional）**
- have better DC (at least 3 restores)
- have 1 blanket jammer
- have good softkill
- have 1 parallax radar or spyglass radar
- ^have Track Correlator if spyglass radar
- have 1 ES32 Missile ID

**避免（avoid）**
- have 120mm turret

## Disclaimer
参考配置，不是最优解。样本是玩家舰队里 must + should 全过的真实配装（主要取自中文新手包 v1.12，对应游戏 0.6.2.3；其余来自 other info 与本地存档）。旧版本可能改过数值或改过名字；模组部件不代表原版能照抄。把它当起步模板，不要当配方。

## Numbers
- Point cost: 800-1200 (good-sample median 1002, range 932-1191)
- Power: draw 5425 kW / supply 5650 kW (median)
- Hull: Vauxhall Light Cruiser Class×22

## Armament (good samples)
- 250 mm turret/cannon: 22/22 ships, median 5 (min 4, max 5)
- VLS-1-23 launcher: 8/22 ships
- VLS-1-46 launcher: 7/22 ships
- VLS-2 launcher: 6/22 ships

## Core parts (fitted on most good samples)
- Ammunition Elevators (22/22)
- Auxiliary Steering (22/22)
- FM230 'Whiplash' Drive (18/22)
- FM580 'Raider' Drive (22/22)
- FR3300 Micro Reactor (19/22)
- Mk20 'Defender' PDT (19/22)
- Mk64 Cannon (22/22)
- Rapid DC Locker (22/22)
- Reinforced CIC (21/22)
- Reinforced Magazine (22/22)
- Small DC Locker (21/22)

## Common parts (40-70%)
- E90 'Blanket' Jammer (11/22)
- RM50 'Parallax' Radar (10/22)
- RS35 'Frontline' Radar (9/22)

## Optional parts
- ES32 'Scryer' Missile ID System (8/22)
- VLS-1-23 Launcher (8/22)
- E70 'Interruption' Jammer (7/22)
- VLS-1-46 Launcher (7/22)
- VLS-2 Launcher (6/22)
- Damage Control Central (5/22)
- FR4800 Reactor (4/22)
- RF101 'Bullseye' Radar (4/22)
- Mk25 'Rebound' PDT (3/22)
- Plant Control Center (3/22)
- RS41 'Spyglass' Radar (3/22)
- Rapid-Cycle Cradle (3/22)

## Sample ships (good)
- Impact (1101 CL, 976 pts, Chinese starter pack)
- Despair (1101 CL, 976 pts, Chinese starter pack)
- Impede (1101 CL, 1002 pts, Chinese starter pack)
- Suffering (1101 CL, 1002 pts, Chinese starter pack)
- Implode (1101 CL, 1022 pts, Chinese starter pack)
- Remorse (1101 CL, 1022 pts, Chinese starter pack)

## 样板船完整装配（整艘照抄）：Impede（1101 CL）

**整艘照抄**：舰体 `Vauxhall Light Cruiser`（阵营键 `Stock/Shelter Alliance`），存档原值 **1002 点**，共 28 个槽位。复制这艘船时连它自带的导弹一起抄，只改船名、呼号和导弹名。

| 槽位 | 部件 | 尺寸 | 点数 | 供电 kW |
|---|---|---|---:|---:|
| MT1 | Mk64 Cannon | 3x1x5 | 30 | -125 |
| MT2 | Mk64 Cannon | 3x1x5 | 30 | -125 |
| MT3 | Mk64 Cannon | 3x1x5 | 30 | -125 |
| MT4 | Mk64 Cannon | 3x1x5 | 30 | -125 |
| MT5 | E70 'Interruption' Jammer | 3x1x3 | 55 | -600 |
| MT6 | Mk64 Cannon | 3x1x5 | 30 | -125 |
| MT7 | VLS-1-23 Launcher | 2x2x2 | 5 | -50 |
| MT8 | Mk20 'Defender' PDT | 2x1x2 | 25 | -175 |
| MT9 | E90 'Blanket' Jammer | 2x1x2 | 50 | -1000 |
| MT10 | Mk20 'Defender' PDT | 2x1x2 | 25 | -175 |
| CMP1 | Small DC Locker | 3x1x3 | 20 | 0 |
| CMP2 | Small DC Locker | 3x1x3 | 20 | 0 |
| CMP3 | Rapid DC Locker | 3x1x3 | 10 | 0 |
| CMP4 | Rapid DC Locker | 3x1x3 | 10 | 0 |
| CMP5 | Small DC Locker | 3x1x3 | 20 | 0 |
| CMP6 | Auxiliary Steering | 3x1x3 | 10 | 0 |
| CMP7 | Auxiliary Steering | 3x1x3 | 10 | 0 |
| CMP8 | Reinforced CIC | 4x1x6 | 25 | 0 |
| CMP9 | Reinforced Magazine | 1x1x1 | 0 → 之后 40/座 | 0 |
| MOD1 | FM230 'Whiplash' Drive | 5x3x5 | 20 | 0 |
| MOD2 | FR3300 Micro Reactor | 3x3x3 | 10 | +2250 |
| MOD3 | FM580 'Raider' Drive | 10x8x10 | 30 | 0 |
| MOD4 | FR3300 Micro Reactor | 3x3x3 | 10 | +2250 |
| MOD5 | ES32 'Scryer' Missile ID System | 2x2x2 | 10 | -300 |
| MOD6 | Ammunition Elevators | 2x2x2 | 20 | -150 |
| MOD7 | Ammunition Elevators | 2x2x2 | 20 | -150 |
| MOD8 | RS35 'Frontline' Radar | 2x2x2 | 10 | -2000 |
| MOD9 | Ammunition Elevators | 2x2x2 | 20 | -150 |

- 合计：部件 585 点 + 舰体 350 点 = **935 点**（不含弹库与弹药，见下）
- 另有弹库 0 点 + 弹药 67 点 ⇒ **全价约 1002 点**（估算；游戏里以存档原值 1002 为准，单价见 `zh/弹药点数表.md`）
- 供电：发电 4500 kW / 耗电 5375 kW（余量 -875 kW）
- 弹库装载：MT7 VLS-1-23 Launcher：EA12 Chaff Decoy ×11；CMP9 Reinforced Magazine：250mm HE Shell ×850、250mm AP Shell ×800、250mm HE-RPF Shell ×950、20mm Slug ×8000


## 样板船完整装配（整艘照抄）：Suffering（1101 CL）

**整艘照抄**：舰体 `Vauxhall Light Cruiser`（阵营键 `Stock/Shelter Alliance`），存档原值 **1002 点**，共 28 个槽位。复制这艘船时连它自带的导弹一起抄，只改船名、呼号和导弹名。

| 槽位 | 部件 | 尺寸 | 点数 | 供电 kW |
|---|---|---|---:|---:|
| MT1 | Mk64 Cannon | 3x1x5 | 30 | -125 |
| MT2 | Mk64 Cannon | 3x1x5 | 30 | -125 |
| MT3 | Mk64 Cannon | 3x1x5 | 30 | -125 |
| MT4 | Mk64 Cannon | 3x1x5 | 30 | -125 |
| MT5 | E70 'Interruption' Jammer | 3x1x3 | 55 | -600 |
| MT6 | Mk64 Cannon | 3x1x5 | 30 | -125 |
| MT7 | VLS-1-23 Launcher | 2x2x2 | 5 | -50 |
| MT8 | Mk20 'Defender' PDT | 2x1x2 | 25 | -175 |
| MT9 | E90 'Blanket' Jammer | 2x1x2 | 50 | -1000 |
| MT10 | Mk20 'Defender' PDT | 2x1x2 | 25 | -175 |
| CMP1 | Small DC Locker | 3x1x3 | 20 | 0 |
| CMP2 | Small DC Locker | 3x1x3 | 20 | 0 |
| CMP3 | Rapid DC Locker | 3x1x3 | 10 | 0 |
| CMP4 | Rapid DC Locker | 3x1x3 | 10 | 0 |
| CMP5 | Small DC Locker | 3x1x3 | 20 | 0 |
| CMP6 | Auxiliary Steering | 3x1x3 | 10 | 0 |
| CMP7 | Auxiliary Steering | 3x1x3 | 10 | 0 |
| CMP8 | Reinforced CIC | 4x1x6 | 25 | 0 |
| CMP9 | Reinforced Magazine | 1x1x1 | 0 → 之后 40/座 | 0 |
| MOD1 | FM230 'Whiplash' Drive | 5x3x5 | 20 | 0 |
| MOD2 | FR3300 Micro Reactor | 3x3x3 | 10 | +2250 |
| MOD3 | FM580 'Raider' Drive | 10x8x10 | 30 | 0 |
| MOD4 | FR3300 Micro Reactor | 3x3x3 | 10 | +2250 |
| MOD5 | ES32 'Scryer' Missile ID System | 2x2x2 | 10 | -300 |
| MOD6 | Ammunition Elevators | 2x2x2 | 20 | -150 |
| MOD7 | Ammunition Elevators | 2x2x2 | 20 | -150 |
| MOD8 | RS35 'Frontline' Radar | 2x2x2 | 10 | -2000 |
| MOD9 | Ammunition Elevators | 2x2x2 | 20 | -150 |

- 合计：部件 585 点 + 舰体 350 点 = **935 点**（不含弹库与弹药，见下）
- 另有弹库 0 点 + 弹药 67 点 ⇒ **全价约 1002 点**（估算；游戏里以存档原值 1002 为准，单价见 `zh/弹药点数表.md`）
- 供电：发电 4500 kW / 耗电 5375 kW（余量 -875 kW）
- 弹库装载：MT7 VLS-1-23 Launcher：EA12 Chaff Decoy ×11；CMP9 Reinforced Magazine：250mm HE Shell ×850、250mm AP Shell ×800、250mm HE-RPF Shell ×950、20mm Slug ×8000


## Author notes (from the fleet's 使用说明.txt)
- 1101 CL: *舰队定位：前排/中程火炮输出 / *上手难度：中 / （比战列舰略简单） / *武装说明 / 没啥特殊的，主武器250mm两用火炮，点防御炮全是防卫者20mm；两条船上有雷达干扰。二号舰有11.5km雷达探测范围。 / 舰队装备类全软杀，CMD/hoj需要在干扰后靠机动躲一下。 / *优点： / --航速快，且在8km外可以靠环绕机动躲掉大部分450炮弹 / --有Bullseye火控和视差雷达 / --250两用炮可以对付OSP所有战斗单位 / --大量防卫者点防炮和250mm两用炮组成的点防御网 / --在大部分ANS舰队要买防空导弹的时候，三轻巡的250mm he-ref炮弹勉强满足了驱逐敌方舰载机的需求 / --有俩雷达干扰可以欺负电子战不好的OSP / *缺点： / --装甲被450mm高爆弹乱穿 / --未装备 真.全软杀 / --船体没有一个地方是安全的，所有部件都会被快速打坏 / --250mm炮射程8km，但在8km内需要分别手操每一条轻巡才能较好地回避450mm（操作不来就自动 / --250mm炮需要一定时间才能打出足够的伤害 / --250mm炮杀伤给货船（MN）和指挥巡洋舰（CC）的速度很慢 / 使用注意事项： / 1.躲炮弹不是无敌的，需要时刻小心被打交叉火力导致躲不掉 / 2.轻巡开局Rush和绕侧都是常见战术，但是一定要注意控制和地方的距离 / 3.轻巡的点防炮都是20mm，对带突防机动的S2导弹效率不高，得用250mm的he ref炮弹对付 / 4.需要注意诱饵数量 / 5.17号推进器是轻巡鼻子上那个最大的推进器。这个推进器提供了轻巡很多倒…

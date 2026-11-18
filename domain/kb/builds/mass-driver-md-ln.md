# mass driver (md) ln

Tags: kind=build template; class=mass driver (md) ln; cost=1000-1300; samples=27; good=7
Keywords: build, loadout, template, 配装, 配置, 装配, 模板, 舰级, mass driver (md) ln
Summary: mass driver (md) ln build; 27 matched ships, 7 of them are good samples (must and should both pass); typical cost 1052 (range 1048-1222); hull Marauder Line Ship Class×7.
Section: build templates; requirements from other info/Ship Builds.txt; samples from player fleets

## How to read this
回答「这艘船算不算 / 合不合格」以 Requirements 段为准（must 全过才算这个舰级，should 是良好标准）；部件清单只统计 good 样本，频率 (k/N) 表示常见程度，不是硬性要求。所有舰船先要过通用基线（`reference/baseline-requirements.md`），再看本舰级要求。

## 舰级要求（Ship Builds.txt 原文，作为判定依据）

**舰级硬性要求（required：缺一条就不算这个舰级）**
- have at least 1 mass drivers

**良好标准（should：缺了算有瑕疵，但仍算这个舰级）**
- all mass drivers face the same direction
- have 3 - 4 mass drivers total
- have minimal DC (at least 2 restores)
- have at least 1 Reinforced CIC
- have minimal softkill
- have at least 2 Energy Regulators

**可选加分（optional）**
- have exactly 3 mass drivers total
- have at least 2 CIC and/or Auxiliary Steering
- have good DC (more than 2 restores)
- have hardkill
- have good softkill
- have T20 turrets
- have extra antenna

**避免（avoid）**
- having more or less mass drivers than 3
- have 250 cannons
- have C30 cannons
- have 450 cannons
- have plasma cannons
- have mls launchers
- have turret on main mount  (mount 1-8)
- have LRT radar
- have >16000kW power required

## Disclaimer
参考配置，不是最优解。样本是玩家舰队里 must + should 全过的真实配装（主要取自中文新手包 v1.12，对应游戏 0.6.2.3；其余来自 other info 与本地存档）。旧版本可能改过数值或改过名字；模组部件不代表原版能照抄。把它当起步模板，不要当配方。

## Numbers
- Point cost: 1000-1300 (good-sample median 1052, range 1048-1222)
- Power: draw 14750 kW / supply 10850 kW (median)
- Hull: Marauder Line Ship Class×7

## Armament (good samples)
- 100 mm turret/cannon: 2/7 ships, median 1 (min 1, max 1)
- VLS-1-46 launcher: 7/7 ships

## Core parts (fitted on most good samples)
- Boosted Reactor (7/7)
- Citadel Magazine (6/7)
- Energy Regulator (7/7)
- Gun Plotting Center (5/7)
- Large DC Storage (6/7)
- Light Civilian Reactor (7/7)
- Plant Control Center (7/7)
- TE45 Mass Driver (7/7)
- VLS-1-46 Launcher (7/7)

## Common parts (40-70%)
- BW2000 Drive (3/7)
- Basic CIC (3/7)
- CHI-7700 Drive (4/7)
- Reinforced CIC (4/7)
- Small DC Locker (4/7)

## Optional parts
- Damage Control Central (2/7)
- Damage Control Complex (2/7)
- Rapid DC Locker (2/7)
- T20 Cannon (2/7)
- L50 'Blackjack' Laser Dazzler (1/7)
- Large DC Locker (1/7)
- P20 'Bastion' PDT (1/7)
- Reinforced Magazine (1/7)

## Sample ships (good)
- Wired Daily (CC ln test 6, 1049 pts, Chinese starter pack)
- Wired Daily (CC ln test 6, 1052 pts, Chinese starter pack)
- Wired Daily (All 27 sample ships · Protectorate, 1048 pts, player save)
- Wired Daily (All 27 sample ships · Protectorate, 1051 pts, player save)
- Eversimp (Dual rail bulk, 1200 pts, player save)
- Evercringe (Dual rail bulk, 1200 pts, player save)

## 样板船完整装配（整艘照抄）：Wired Daily（CC ln test 6）

**整艘照抄**：舰体 `Bulk Hauler`（阵营键 `Stock/Outlying Systems Protectorate`），存档原值 **1052 点**，共 21 个槽位。复制这艘船时连它自带的导弹一起抄，只改船名、呼号和导弹名。

| 槽位 | 部件 | 尺寸 | 点数 | 供电 kW |
|---|---|---|---:|---:|
| Bow·MT1 | TE45 Mass Driver | — | 100 | -4250 |
| Bow·MT3 | TE45 Mass Driver | — | 100 | -4250 |
| Core·MT6 | TE45 Mass Driver | — | 100 | -4250 |
| Stern·MT14 | VLS-1-46 Launcher | 3x2x3 | 5 | -50 |
| Bow·CMP1 | Basic CIC | 4x1x6 | 10 | 0 |
| Core·CMP1 | Gun Plotting Center | 3x1x3 | 30 | 0 |
| Bow·CMP2 | Plant Control Center | 3x1x3 | 25 | 0 |
| Core·CMP2 | Gun Plotting Center | 3x1x3 | 30 | 0 |
| Bow·CMP3 | Small DC Locker | 3x1x3 | 20 | 0 |
| Core·CMP3 | Plant Control Center | 3x1x3 | 25 | 0 |
| Core·CMP4 | Citadel Magazine | 1x3x1 | 0 → 之后 150/座 | 0 |
| Core·CMP5 | Large DC Storage | 6x3x6 | 45 | 0 |
| Core·CMP6 | Basic CIC | 4x1x6 | 10 | 0 |
| Stern·MOD1 | Boosted Reactor | 5x5x5 | 10 | +5000 |
| Bow·MOD1 | Light Civilian Reactor | 3x3x3 | 10 | +1850 |
| Core·MOD1 | Energy Regulator | 3x3x3 | 30 | -650 |
| Stern·MOD2 | CHI-7700 Drive | 12x12x12 | 20 | 0 |
| Bow·MOD2 | Energy Regulator | 3x3x3 | 30 | -650 |
| Core·MOD2 | Energy Regulator | 3x3x3 | 30 | -650 |
| Bow·MOD3 | Light Civilian Reactor | 3x3x3 | 10 | +1850 |
| Core·MOD3 | Light Civilian Reactor | 3x3x3 | 10 | +1850 |

- 合计：部件 650 点 + 舰体 375 点 = **1025 点**（不含弹库与弹药，见下）
- 另有弹库 0 点 + 弹药 27 点 ⇒ **全价约 1052 点**（估算；游戏里以存档原值 1052 为准，单价见 `zh/弹药点数表.md`）
- 供电：发电 10550 kW / 耗电 14750 kW（余量 -4200 kW）
- 弹库装载：Stern·MT14 VLS-1-46 Launcher：SGM-101 OA ×1、EA14 Chaff Decoy ×6；Core·CMP4 Citadel Magazine：500mm Fracturing Block ×350


## 样板船完整装配（整艘照抄）：Wired Daily（CC ln test 6）

**整艘照抄**：舰体 `Bulk Hauler`（阵营键 `Stock/Outlying Systems Protectorate`），存档原值 **1049 点**，共 20 个槽位。复制这艘船时连它自带的导弹一起抄，只改船名、呼号和导弹名。

| 槽位 | 部件 | 尺寸 | 点数 | 供电 kW |
|---|---|---|---:|---:|
| Bow·MT1 | TE45 Mass Driver | — | 100 | -4250 |
| Bow·MT3 | TE45 Mass Driver | — | 100 | -4250 |
| Core·MT6 | TE45 Mass Driver | — | 100 | -4250 |
| Stern·MT14 | VLS-1-46 Launcher | 3x2x3 | 5 | -50 |
| Bow·CMP1 | Reinforced CIC | 4x1x6 | 25 | 0 |
| Core·CMP1 | Small DC Locker | 3x1x3 | 20 | 0 |
| Bow·CMP2 | Plant Control Center | 3x1x3 | 25 | 0 |
| Core·CMP2 | Gun Plotting Center | 3x1x3 | 30 | 0 |
| Bow·CMP3 | Small DC Locker | 3x1x3 | 20 | 0 |
| Core·CMP4 | Citadel Magazine | 1x3x1 | 0 → 之后 150/座 | 0 |
| Core·CMP5 | Large DC Storage | 6x3x6 | 45 | 0 |
| Core·CMP6 | Plant Control Center | 3x1x3 | 25 | 0 |
| Stern·MOD1 | Boosted Reactor | 5x5x5 | 10 | +5000 |
| Bow·MOD1 | Light Civilian Reactor | 3x3x3 | 10 | +1850 |
| Core·MOD1 | Energy Regulator | 3x3x3 | 30 | -650 |
| Stern·MOD2 | CHI-7700 Drive | 12x12x12 | 20 | 0 |
| Bow·MOD2 | Energy Regulator | 3x3x3 | 30 | -650 |
| Core·MOD2 | Energy Regulator | 3x3x3 | 30 | -650 |
| Bow·MOD3 | Light Civilian Reactor | 3x3x3 | 10 | +1850 |
| Core·MOD3 | Light Civilian Reactor | 3x3x3 | 10 | +1850 |

- 合计：部件 645 点 + 舰体 375 点 = **1020 点**（不含弹库与弹药，见下）
- 另有弹库 0 点 + 弹药 29 点 ⇒ **全价约 1049 点**（估算；游戏里以存档原值 1049 为准，单价见 `zh/弹药点数表.md`）
- 供电：发电 10550 kW / 耗电 14750 kW（余量 -4200 kW）
- 弹库装载：Stern·MT14 VLS-1-46 Launcher：SGM-101 OA ×1、EA14 Chaff Decoy ×7；Core·CMP4 Citadel Magazine：500mm Fracturing Block ×350


## Author notes (from the fleet's 使用说明.txt)
- CC ln test 6: *舰队定位：半前排/中远程火炮输出+半后排火力支援 / *上手难度：中 / *武装说明 / --指挥巡洋舰（CC）有6管450mm火炮，垂发中的S1导弹为防空导弹。装备泛光灯对抗雷达干扰。 / --二号线列舰（LN）是船棍质量投射器远程支援船 / --三号拖船装备EWR，SSJ软杀导弹和光电干扰器 / *优点： / --CC能扛线，LN也有远程火力支援 / --拖船的EWR能提供非常远的视野 / --有全软杀，面对元气弹有CMD S1导弹 / --CC在9.5km外能通过环绕指令有效回避450mm炮弹 / *缺点： / --CMD干扰只有一个interruption。敌方在近距离靠CR75天线引导CMD导弹，有概率不能及时干扰掉。 / --点防御搞不定大批量导弹，需要软杀 / --前线只有一条CC，死了就没了 / --所有主力舰航速一般 / --后方的LN是脆弱的船棍 / 使用注意事项： / 1.CC虽然能躲炮弹，但是距离太近或者被敌方打交叉火力就不行了 / 2.CC需要时刻将船艏指向来袭火力的大致方向。侧面挨打很伤。 / 3.CC航速一般，撤退需要及时。不要离掩体太远。 / 4.S1防空导弹数量少，一定要手动发射 / 5.LN需要手动提前转向，把有炮的侧面对准敌方可能出现的位置，然后依靠CC或者其他友军的火控数据射击 / 6.拖船不要离CC太近，也不要太远，具体距离根据地图判断 / 7.SSJ导弹的原理是用导弹搭载雷达干扰模快来吸引对面的HOJ引导头或者干扰对面的ACT和SAH引导头。必须手动对目标发射。 / --作者：Jordenxue
- CC ln test 6: *舰队定位：半前排/中远程火炮输出+半后排火力支援 / *上手难度：中 / *武装说明 / --指挥巡洋舰（CC）有6管450mm火炮，垂发中的S1导弹为防空导弹。装备泛光灯对抗雷达干扰。 / --二号线列舰（LN）是船棍质量投射器远程支援船 / --三号拖船装备EWR，反飞机防空导弹和EO干扰器 / --CC和拖船装备类全软杀，例外还是Eeact[CMD]拒绝 / *优点： / --CC能扛线，LN也有远程火力支援 / --拖船的EWR能提供非常远的视野 / --有类全软杀，面对元气弹有CMD S1导弹 / --CC在9.5km外能通过环绕指令有效回避450mm炮弹 / --CC装备4台极光点防炮，对二级导弹效果不错 / *缺点： / --未装备 真.全软杀 / --点防御搞不定大批量导弹，需要软杀 / --前线只有一条CC，死了就没了 / --反飞机防空导弹一轮只能打两发。 / --航速一般 / --后方的LN是脆弱的船棍 / 使用注意事项： / 1.CC虽然能躲炮弹，但是距离太近或者被敌方打交叉火力就不行了 / 2.CC需要时刻将船艏指向来袭火力的大致方向。侧面挨打很伤。 / 3.CC航速一般，撤退需要及时。不要离掩体太远。 / 4.S1防空导弹数量少，一定要手动发射 / 5.LN需要手动提前转向，把有炮的侧面对准敌方可能出现的位置，然后依靠CC或者其他友军的火控数据射击 / 6.拖船不要离CC太近，也不要太远，具体距离根据地图判断 / --作者：J某

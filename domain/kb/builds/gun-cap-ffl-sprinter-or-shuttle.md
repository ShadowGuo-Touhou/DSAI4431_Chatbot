# gun/cap ffl  (sprinter or shuttle)

Tags: kind=build template; class=gun/cap ffl  (sprinter or shuttle); cost=150-300; samples=141; good=106
Keywords: build, loadout, template, 配装, 配置, 装配, 模板, 舰级, gun/cap ffl  (sprinter or shuttle)
Summary: gun/cap ffl  (sprinter or shuttle) build; 141 matched ships, 106 of them are good samples (must and should both pass); typical cost 215 (range 152-293); hull Sprinter Corvette Class×71、Ferryman Clipper Class×35.
Section: build templates; requirements from other info/Ship Builds.txt; samples from player fleets

## How to read this
回答「这艘船算不算 / 合不合格」以 Requirements 段为准（must 全过才算这个舰级，should 是良好标准）；部件清单只统计 good 样本，频率 (k/N) 表示常见程度，不是硬性要求。所有舰船先要过通用基线（`reference/baseline-requirements.md`），再看本舰级要求。

## 舰级要求（Ship Builds.txt 原文，作为判定依据）

**舰级硬性要求（required：缺一条就不算这个舰级）**
- have at least 1 turret (T20 or Mk61,Mk62,Mk64)

**良好标准（should：缺了算有瑕疵，但仍算这个舰级）**
- have minimal DC (1 rapid DC Locker)

**可选加分（optional）**
- have minimal softkill
- have minimal hardkill
- have Mk64 (for sprinter mount 1)
- have 1 reinforced CIC
- have better DC (1 restore)

## Disclaimer
参考配置，不是最优解。样本是玩家舰队里 must + should 全过的真实配装（主要取自中文新手包 v1.12，对应游戏 0.6.2.3；其余来自 other info 与本地存档）。旧版本可能改过数值或改过名字；模组部件不代表原版能照抄。把它当起步模板，不要当配方。

## Numbers
- Point cost: 150-300 (good-sample median 215, range 152-293)
- Power: draw 2228 kW / supply 2750 kW (median)
- Hull: Sprinter Corvette Class×71、Ferryman Clipper Class×35

## Armament (good samples)
- 120 mm turret/cannon: 65/106 ships, median 1 (min 1, max 2)
- 100 mm turret/cannon: 35/106 ships, median 1 (min 1, max 2)
- 250 mm turret/cannon: 30/106 ships, median 1 (min 1, max 1)
- VLS-1-23 launcher: 58/106 ships
- VLS-1-46 launcher: 23/106 ships
- RL18 launcher: 2/106 ships
- ML-9 Mine Launcher launcher: 2/106 ships

## Core parts (fitted on most good samples)
- Reinforced Magazine (98/106)

## Common parts (40-70%)
- Basic CIC (66/106)
- FR3300 Micro Reactor (67/106)
- RS35 'Frontline' Radar (46/106)
- Rapid DC Locker (70/106)
- VLS-1-23 Launcher (58/106)

## Optional parts
- Mk62 Cannon (40/106)
- Reinforced CIC (40/106)
- Small DC Locker (40/106)
- Mk20 'Defender' PDT (36/106)
- FM230 'Whiplash' Drive (35/106)
- Light Civilian Reactor (35/106)
- T20 Cannon (35/106)
- Mk64 Cannon (30/106)
- Ithaca Bridgemaster (28/106)
- Ammunition Elevators (25/106)
- Mk61 Cannon (24/106)
- FM200 Drive (22/106)

## Sample ships (good)
- Zippy Taxis (BB test 55 Newbie, 220 pts, Chinese starter pack)
- Scoundrel (Tantalum Squadron, 164 pts, example fleet)
- Charlatan (Tantalum Squadron, 164 pts, example fleet)
- Swindler (Tantalum Squadron, 164 pts, example fleet)
- In Your Walls (Wulfenite Squadron, 165 pts, example fleet)
- It's Free Real Estate (Wulfenite Squadron, 165 pts, example fleet)

## 样板船完整装配（整艘照抄）：Zippy Taxis（BB test 55 Newbie）

**整艘照抄**：舰体 `Sprinter Corvette`（阵营键 `Stock/Shelter Alliance`），存档原值 **220 点**，共 9 个槽位。复制这艘船时连它自带的导弹一起抄，只改船名、呼号和导弹名。

| 槽位 | 部件 | 尺寸 | 点数 | 供电 kW |
|---|---|---|---:|---:|
| MT1 | Mk61 Cannon | 3x1x3 | 10 | -50 |
| MT2 | RF101 'Bullseye' Radar | 2x1x2 | 40 | -300 |
| MT3 | VLS-1-23 Launcher | 2x2x2 | 5 | -50 |
| MT4 | E57 'Floodlight' Illuminator | — | — | 0 |
| CMP1 | Basic CIC | 4x1x6 | 10 | 0 |
| CMP3 | Reinforced Magazine | 1x1x1 | 0 → 之后 40/座 | 0 |
| CMP4 | Small DC Locker | 3x1x3 | 20 | 0 |
| MOD1 | FR3300 Micro Reactor | 3x3x3 | 10 | +2250 |
| MOD2 | FM30X 'Prowler' Drive | 5x3x5 | 25 | 0 |

- 合计：部件 120 点 + 舰体 75 点 = **195 点**（不含弹库与弹药，见下）
- 另有弹库 0 点 + 弹药 10 点 ⇒ **全价约 205 点**（估算；游戏里以存档原值 220 为准，单价见 `zh/弹药点数表.md`）
- 供电：发电 2250 kW / 耗电 400 kW（余量 +1850 kW）
- 弹库装载：MT3 VLS-1-23 Launcher：SGM-100 Balestra ×1、EA12 Chaff Decoy ×5；CMP3 Reinforced Magazine：120mm HE Shell ×200、120mm HE-RPF Shell ×200


## 样板船完整装配（整艘照抄）：In Your Walls（Wulfenite Squadron）

**整艘照抄**：舰体 `Shuttle`（阵营键 `Stock/Outlying Systems Protectorate`），存档原值 **165 点**，共 9 个槽位。复制这艘船时连它自带的导弹一起抄，只改船名、呼号和导弹名。

| 槽位 | 部件 | 尺寸 | 点数 | 供电 kW |
|---|---|---|---:|---:|
| MT1 | T20 Cannon | 3x1x3 | 15 | -30 |
| MT2 | T20 Cannon | 3x1x3 | 15 | -30 |
| MT3 | VLS-1-23 Launcher | 2x2x2 | 5 | -50 |
| CMP1 | Basic CIC | 4x1x6 | 10 | 0 |
| CMP2 | Small DC Locker | 3x1x3 | 20 | 0 |
| CMP3 | Reinforced Magazine | 1x1x1 | 0 → 之后 40/座 | 0 |
| MOD1 | Light Civilian Reactor | 3x3x3 | 10 | +1850 |
| MOD2 | BW800 Drive | 5x3x5 | 10 | 0 |
| MOD3 | Ithaca Bridgemaster | 2x2x2 | 10 | -1200 |

- 合计：部件 95 点 + 舰体 50 点 = **145 点**（不含弹库与弹药，见下）
- 另有弹库 0 点 + 弹药 20 点 ⇒ **全价约 165 点**（估算；游戏里以存档原值 165 为准，单价见 `zh/弹药点数表.md`）
- 供电：发电 1850 kW / 耗电 1310 kW（余量 +540 kW）
- 弹库装载：MT3 VLS-1-23 Launcher：EA12 Chaff Decoy ×5、SGM-1 Ceremonial Arming Missile ×1、SGM-1 Scorch ×3；CMP3 Reinforced Magazine：100mm Grapeshot ×250、100mm HE Shell ×250


## Author notes (from the fleet's 使用说明.txt)
- BB test 55 Newbie: *舰队定位：前排/中远程火炮输出 / *上手难度：高 / （该舰队本不应出现在新手包里面。但是我知道新手肯定会试着去搓战列舰舰队所以干脆放在这里给你们当参考） / *武装说明 / 1.主武器为8管450mm火炮 / 2.战列舰背后的S3H导弹都是防空导弹。使用时将防御导弹发射控制设置成"手动"，然后锁定敌方飞机后按Z发射 / 3.战列舰侧面的S2垂发中，S2导弹为SSJ诱饵导弹，使用方法同上，目标为敌方有hoj引导头的导弹 / 4.二号轻护上面有泛光灯和锁定雷达。可以在战列舰前面，目标8.5公里左右处锁定目标，给战列舰提供火控数据。战列舰根据火控数据能发挥450mm火炮的最大射程。 / 5.三号舰为点防御护卫舰，战列舰本体也装备有适量点防御。 / 6.本舰队装备类全软杀，除"Eact[cmd]拒绝"引导头外，别的引导头都能软杀。 / *优点： / --战列舰船体拥有56厘米装甲和大量损管，比较耐打。 / --拥有9.5公里以上精确火控能力，在该9.5公里外交火能压制OSP的线列舰 / --有类全软杀和足够多的防空导弹 / *缺点： / --反小船火力只有二号舰上面一门120mm炮，约等于没有。 / --未装备 真.全软杀 / --未装备视差雷达 / --大量软杀/电子战设备集中在战列舰本体上，容易被打坏 / --反电子战能力一般，遇到敌方重干扰如果泛光灯搞不定请找队友支援 / --机动性较差，回避效果一般，撤退缓慢 / 使用注意事项： / 1.战列舰虽然耐打但并不无敌，不要和过多（大于3000分）的敌方同时交手 / 2.战列舰需要时刻将船艏指向来袭火力的大致方向。侧面挨打很伤。…

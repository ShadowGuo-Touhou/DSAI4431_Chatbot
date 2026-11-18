# missile CH

Tags: kind=build template; class=missile CH; cost=2000-3000; samples=6; good=2
Keywords: build, loadout, template, 配装, 配置, 装配, 模板, 舰级, missile CH
Summary: missile CH build; 6 matched ships, 2 of them are good samples (must and should both pass); typical cost 2912 (range 2825-3000); hull Axford Heavy Cruiser Class×2.
Section: build templates; requirements from other info/Ship Builds.txt; samples from player fleets

## How to read this
回答「这艘船算不算 / 合不合格」以 Requirements 段为准（must 全过才算这个舰级，should 是良好标准）；部件清单只统计 good 样本，频率 (k/N) 表示常见程度，不是硬性要求。所有舰船先要过通用基线（`reference/baseline-requirements.md`），再看本舰级要求。

## 舰级要求（Ship Builds.txt 原文，作为判定依据）

**舰级硬性要求（required：缺一条就不算这个舰级）**
- have at least 2 large vls or cls (mount 1-3)
- have >1000 points of offensive missiles

**良好标准（should：缺了算有瑕疵，但仍算这个舰级）**
- have full softkill
- have bullseye
- have minimal DC (at least 2 restores)
- have at least 2 CIC and/or Auxillary Steering
- have at least 2  Missile Programming Bus / Missile Programming Bus Array

**可选加分（optional）**
- have a beam turret
- have minimal hardkill
- have good DC (at least 4 restores)
- have 1 parallax radar or spyglass radar
- have Track Correlator if using spyglass radar
- have 1 ES32 Missile ID
- have extra antenna

**避免（avoid）**
- have a craft launch pad
- have rail turret
- have 250 turret
- have 120 turret

## Disclaimer
参考配置，不是最优解。样本是玩家舰队里 must + should 全过的真实配装（主要取自中文新手包 v1.12，对应游戏 0.6.2.3；其余来自 other info 与本地存档）。旧版本可能改过数值或改过名字；模组部件不代表原版能照抄。把它当起步模板，不要当配方。

## Numbers
- Point cost: 2000-3000 (good-sample median 2912, range 2825-3000)
- Power: draw 9250 kW / supply 8975 kW (median)
- Hull: Axford Heavy Cruiser Class×2

## Armament (good samples)
- VLS-1-23 launcher: 2/2 ships
- VLS-2 launcher: 2/2 ships
- VLS-3 launcher: 2/2 ships

## Core parts (fitted on most good samples)
- Auxiliary Steering (2/2)
- CR70 Antenna (2/2)
- ES32 'Scryer' Missile ID System (2/2)
- FR3300 Micro Reactor (2/2)
- Large DC Locker (2/2)
- Missile Programming Bus (2/2)
- Missile Programming Bus Array (2/2)
- Mk20 'Defender' PDT (2/2)
- RF101 'Bullseye' Radar (2/2)
- Reinforced CIC (2/2)
- Reinforced DC Locker (2/2)
- Reinforced Magazine (2/2)
- Small DC Locker (2/2)
- VLS-1-23 Launcher (2/2)
- VLS-2 Launcher (2/2)
- VLS-3 Launcher (2/2)

## Common parts (40-70%)
- E15 'Masquerade' Signature Booster (1/2)
- E55 'Floodlight' Illuminator (1/2)
- E70 'Interruption' Jammer (1/2)
- FM230 'Whiplash' Drive (1/2)
- FM540 'Dragonfly' Drive (1/2)
- FM580 'Raider' Drive (1/2)
- FR4800 Reactor (1/2)
- Focused Particle Accelerator (1/2)
- Mk610 Beam Turret (1/2)
- Plant Control Center (1/2)
- RM50 'Parallax' Radar (1/2)
- RS35 'Frontline' Radar (1/2)

## Optional parts
- -

## Sample ships (good)
- LOADER 4 (HC Missile test 7, 3000 pts, Chinese starter pack)
- LOADER 4 (Shock CH test, 2825 pts, player save)

## 样板船完整装配（整艘照抄）：LOADER 4（HC Missile test 7）

**整艘照抄**：舰体 `Axford Heavy Cruiser`（阵营键 `Stock/Shelter Alliance`），存档原值 **3000 点**，共 31 个槽位。复制这艘船时连它自带的导弹一起抄，只改船名、呼号和导弹名。

| 槽位 | 部件 | 尺寸 | 点数 | 供电 kW |
|---|---|---|---:|---:|
| MT1 | VLS-2 Launcher | 3x4x3 | 10 | -200 |
| MT2 | VLS-3 Launcher | 3x4x3 | 20 | -200 |
| MT3 | Mk610 Beam Turret | 8x5x8 | 80 | -3000 |
| MT4 | VLS-2 Launcher | 3x4x3 | 10 | -200 |
| MT5 | Mk20 'Defender' PDT | 2x1x2 | 25 | -175 |
| MT6 | E70 'Interruption' Jammer | 3x1x3 | 55 | -600 |
| MT7 | Mk20 'Defender' PDT | 2x1x2 | 25 | -175 |
| MT8 | E57 'Floodlight' Illuminator | — | — | 0 |
| MT9 | RF101 'Bullseye' Radar | 2x1x2 | 40 | -300 |
| MT10 | VLS-1-23 Launcher | 2x2x2 | 5 | -50 |
| MT11 | CR70 Antenna | 2x1x2 | 15 | -600 |
| CMP1 | Small DC Locker | 3x1x3 | 20 | 0 |
| CMP2 | Small DC Locker | 3x1x3 | 20 | 0 |
| CMP3 | Small DC Locker | 3x1x3 | 20 | 0 |
| CMP4 | Reinforced CIC | 4x1x6 | 25 | 0 |
| CMP5 | Reinforced DC Locker | 3x1x6 | 45 | 0 |
| CMP6 | Large DC Locker | 3x1x6 | 45 | 0 |
| CMP7 | Plant Control Center | 3x1x3 | 25 | 0 |
| CMP8 | Auxiliary Steering | 3x1x3 | 10 | 0 |
| CMP9 | Reinforced Magazine | 1x1x1 | 0 → 之后 40/座 | 0 |
| CMP10 | Auxiliary Steering | 3x1x3 | 10 | 0 |
| MOD1 | FR4800 Reactor | 5x5x5 | 10 | +4200 |
| MOD2 | FR4800 Reactor | 5x5x5 | 10 | +4200 |
| MOD3 | FM580 'Raider' Drive | 10x8x10 | 30 | 0 |
| MOD4 | FR3300 Micro Reactor | 3x3x3 | 10 | +2250 |
| MOD5 | Missile Programming Bus Array | 3x3x3 | 50 | -350 |
| MOD6 | Missile Programming Bus Array | 3x3x3 | 50 | -350 |
| MOD7 | Focused Particle Accelerator | 3x3x3 | 25 | -800 |
| MOD9 | ES32 'Scryer' Missile ID System | 2x2x2 | 10 | -300 |
| MOD11 | Missile Programming Bus | 2x2x2 | 30 | -200 |
| MOD12 | RM50 'Parallax' Radar | 2x2x2 | 45 | -3600 |

- 合计：部件 775 点 + 舰体 600 点 = **1375 点**（不含弹库与弹药，见下）
- 另有弹库 0 点 + 弹药 1610 点 ⇒ **全价约 2985 点**（估算；游戏里以存档原值 3000 为准，单价见 `zh/弹药点数表.md`）
- 供电：发电 10650 kW / 耗电 11100 kW（余量 -450 kW）
- 弹库装载：MT1 VLS-2 Launcher：SGM-H-201 HASM-201 ×27、SGM-H-202 HASM-201 II ×27、EA99 Active Decoy ×3、SGM-201 SSJ ×3、FN-rqVU7_02Nt_UhdXSfPg ×4；MT2 VLS-3 Launcher：SGM-H-301 Atlatl I ×8、SGM-H-302 Atlatl II ×4、SGM-H-303 Atlatl III ×4；MT4 VLS-2 Launcher：FN-rqVU7_02Nt_UhdXSfPg ×16；MT10 VLS-1-23 Launcher：EA12 Chaff Decoy ×15、SGM-100 Balestra ×1、EA20 Flare Decoy ×7；CMP9 Reinforced Magazine：20mm Slug ×6000


## 样板船完整装配（整艘照抄）：LOADER 4（Shock CH test）

**整艘照抄**：舰体 `Axford Heavy Cruiser`（阵营键 `Stock/Shelter Alliance`），存档原值 **2825 点**，共 29 个槽位。复制这艘船时连它自带的导弹一起抄，只改船名、呼号和导弹名。

| 槽位 | 部件 | 尺寸 | 点数 | 供电 kW |
|---|---|---|---:|---:|
| MT1 | VLS-2 Launcher | 3x4x3 | 10 | -200 |
| MT2 | VLS-3 Launcher | 3x4x3 | 20 | -200 |
| MT3 | VLS-2 Launcher | 3x4x3 | 10 | -200 |
| MT4 | VLS-2 Launcher | 3x4x3 | 10 | -200 |
| MT5 | Mk20 'Defender' PDT | 2x1x2 | 25 | -175 |
| MT6 | E15 'Masquerade' Signature Booster | 3x1x3 | 20 | -600 |
| MT7 | Mk20 'Defender' PDT | 2x1x2 | 25 | -175 |
| MT9 | RF101 'Bullseye' Radar | 2x1x2 | 40 | -300 |
| MT10 | VLS-1-23 Launcher | 2x2x2 | 5 | -50 |
| MT11 | CR70 Antenna | 2x1x2 | 15 | -600 |
| CMP1 | Small DC Locker | 3x1x3 | 20 | 0 |
| CMP2 | Small DC Locker | 3x1x3 | 20 | 0 |
| CMP3 | Small DC Locker | 3x1x3 | 20 | 0 |
| CMP4 | Reinforced CIC | 4x1x6 | 25 | 0 |
| CMP5 | Reinforced DC Locker | 3x1x6 | 45 | 0 |
| CMP6 | Large DC Locker | 3x1x6 | 45 | 0 |
| CMP8 | Auxiliary Steering | 3x1x3 | 10 | 0 |
| CMP9 | Reinforced Magazine | 1x1x1 | 0 → 之后 40/座 | 0 |
| CMP10 | Auxiliary Steering | 3x1x3 | 10 | 0 |
| MOD1 | FM230 'Whiplash' Drive | 5x3x5 | 20 | 0 |
| MOD2 | FM230 'Whiplash' Drive | 5x3x5 | 20 | 0 |
| MOD3 | FM540 'Dragonfly' Drive | 10x8x10 | 30 | 0 |
| MOD4 | FR3300 Micro Reactor | 3x3x3 | 10 | +2250 |
| MOD5 | Missile Programming Bus Array | 3x3x3 | 50 | -350 |
| MOD6 | FR3300 Micro Reactor | 3x3x3 | 10 | +2250 |
| MOD7 | Missile Programming Bus Array | 3x3x3 | 50 | -350 |
| MOD9 | ES32 'Scryer' Missile ID System | 2x2x2 | 10 | -300 |
| MOD11 | Missile Programming Bus | 2x2x2 | 30 | -200 |
| MOD12 | RS35 'Frontline' Radar | 2x2x2 | 10 | -2000 |

- 合计：部件 615 点 + 舰体 600 点 = **1215 点**（不含弹库与弹药，见下）
- 另有弹库 0 点 + 弹药 1610 点 ⇒ **全价约 2825 点**（估算；游戏里以存档原值 2825 为准，单价见 `zh/弹药点数表.md`）
- 供电：发电 4500 kW / 耗电 5900 kW（余量 -1400 kW）
- 弹库装载：MT1 VLS-2 Launcher：SGM-H-201 HASM-201 ×27、SGM-H-202 HASM-201 II ×27、EA99 Active Decoy ×3、SGM-201 SSJ ×3、FN-rqVU7_02Nt_UhdXSfPg ×4；MT2 VLS-3 Launcher：SGM-H-301 Atlatl I ×8、SGM-H-302 Atlatl II ×4、SGM-H-303 Atlatl III ×4；MT4 VLS-2 Launcher：FN-rqVU7_02Nt_UhdXSfPg ×16；MT10 VLS-1-23 Launcher：EA12 Chaff Decoy ×15、SGM-100 Balestra ×1、EA20 Flare Decoy ×7；CMP9 Reinforced Magazine：20mm Slug ×6000


## Author notes (from the fleet's 使用说明.txt)
- HC Missile test 7: *舰队定位：后排/巡航导弹 / *上手难度：中 / （原版舰队降低使用难度和弹药量的产物） / *武装说明 / 1.主要武器有S2H巡航导弹，S3H巡航导弹，和一个光束炮塔 / 2.叫ADASHs的S2H导弹都是多用途导弹。使用时将防御导弹发射控制设置成"手动"，然后锁定敌方飞机后按Z发射。多用途导弹也可以锁定目标后攻击对面舰艇。 / 3.S2H导弹用法为EO/Wake和Arad/act一比一混合发射。主要目标是敌方小船。建议反小一次性发射6发。 / 4.S3H导弹为CMD系列攻坚导弹。比例为4发301，2发302，2发303混合，然后通过TRP或直接对目标发射。 / 5.重巡有泛光灯和锁定雷达。遇到重干扰目标可以烧穿->照射泛光灯->锁定 / 6.本舰队装备类全软杀。SGM-201导弹为SSJ诱饵导弹，看见有hoj引导头的导弹，或者act[cmd]按Z发射 / *优点： / --重巡在后排打巡航导弹比较安全 / --两轮8通道高质量S3H杀伤巨大，突防能力很强 / --导弹打完了还有一门光束炮收拾残局 / *缺点： / --点防御火力只有俩防卫者 / --导弹数量较少 / 使用注意事项： / 1.S3H一定要通过TRP或者直接选中目标发射，这样CMD才有用 / 发射时一定要锁定目标。 / S3H第一级速度很慢，对面可以通过躲进掩体让S3H撞石头，需要格外小心。 / 2.S2H注意最大射程 / 3.多用途导弹不多而且突防能力一般，对舰艇和战斗机省着点打。 / --作者：Jordenxue

# CLN (OSP)

Tags: kind=build template; class=CLN (OSP); cost=2000-3000; samples=31; good=27
Keywords: build, loadout, template, 配装, 配置, 装配, 模板, 舰级, CLN (OSP)
Summary: CLN (OSP) build; 31 matched ships, 27 of them are good samples (must and should both pass); typical cost 3000 (range 2184-3000); hull Container Hauler Refit×25、Moorline Line Ship Class×2.
Section: build templates; requirements from other info/Ship Builds.txt; samples from player fleets

## How to read this
回答「这艘船算不算 / 合不合格」以 Requirements 段为准（must 全过才算这个舰级，should 是良好标准）；部件清单只统计 good 样本，频率 (k/N) 表示常见程度，不是硬性要求。所有舰船先要过通用基线（`reference/baseline-requirements.md`），再看本舰级要求。

## 舰级要求（Ship Builds.txt 原文，作为判定依据）

**舰级硬性要求（required：缺一条就不算这个舰级）**
- have at least 1 Container Bank Launcher

## Disclaimer
参考配置，不是最优解。样本是玩家舰队里 must + should 全过的真实配装（主要取自中文新手包 v1.12，对应游戏 0.6.2.3；其余来自 other info 与本地存档）。旧版本可能改过数值或改过名字；模组部件不代表原版能照抄。把它当起步模板，不要当配方。

## Numbers
- Point cost: 2000-3000 (good-sample median 3000, range 2184-3000)
- Power: draw 1606 kW / supply 3950 kW (median)
- Hull: Container Hauler Refit×25、Moorline Line Ship Class×2

## Armament (good samples)
- 100 mm turret/cannon: 1/27 ships, median 1 (min 1, max 1)
- VLS-1-46 launcher: 7/27 ships
- Container Bank Launcher launcher: 4/27 ships

## Core parts (fitted on most good samples)
- Basic CIC (23/27)
- Civilian Reactor (20/27)
- Container Bank Hangar (23/27)
- Deck Gear Locker (23/27)
- Flight Deck Traversal System (23/27)

## Common parts (40-70%)
- BW1500 Drive (11/27)
- Bulk Magazine (17/27)
- Ithaca Bridgemaster (15/27)
- Medium Mounted Hangar (17/27)

## Optional parts
- Large DC Storage (8/27)
- Rapid DC Locker (8/27)
- Reinforced Magazine (8/27)
- Small DC Locker (8/27)
- BW2000 Drive (7/27)
- CHI-7700 Drive (7/27)
- VLS-1-46 Launcher (7/27)
- Spacecraft Repair Station (6/27)
- Intelligence Center (5/27)
- Container Bank Launcher (4/27)
- Reinforced CIC (4/27)
- Bulk Internal Hangar (3/27)

## Sample ships (good)
- Ever Lovely (CVLN test 5 Newbie, 3000 pts, Chinese starter pack)
- All Reaching All Taking (Amethyst Squadron, 3000 pts, example fleet)
- Shanna F. Rosene (cmd test, 2184 pts, player save)
- Huffy Think (Meteror Rain Project, 2340 pts, player save)
- Bus Vocal (Hellbomb, 2602 pts, player save)
- Evergreen Ceres (CV 6k duo, 2965 pts, player save)

## 样板船完整装配（整艘照抄）：Ever Lovely（CVLN test 5 Newbie）

**整艘照抄**：舰体 `Container Hauler Refit`（阵营键 `Stock/Outlying Systems Protectorate`），存档原值 **3000 点**，共 20 个槽位。复制这艘船时连它自带的导弹一起抄，只改船名、呼号和导弹名。

| 槽位 | 部件 | 尺寸 | 点数 | 供电 kW |
|---|---|---|---:|---:|
| Core·MT1 | Container Bank Hangar | 20x5x20 | 100 | -1 |
| Core·MT2 | Container Bank Hangar | 20x5x20 | 100 | -1 |
| Bow·MT3 | Container Bank Hangar | 20x5x20 | 100 | -1 |
| Bow·MT4 | Container Bank Hangar | 20x5x20 | 100 | -1 |
| Stern·MT10 | VLS-1-46 Launcher | 3x2x3 | 5 | -50 |
| Bow·CMP1 | Small DC Locker | 3x1x3 | 20 | 0 |
| Core·CMP1 | Bulk Internal Hangar | 6x3x6 | 10 | 0 |
| Core·CMP2 | Bulk Magazine | 1x1x1 | 0 → 之后 20/座 | 0 |
| Bow·CMP2 | Basic CIC | 4x1x6 | 10 | 0 |
| Bow·CMP3 | Deck Gear Locker | 3x1x6 | 30 | 0 |
| Core·CMP3 | Deck Gear Locker | 3x1x6 | 30 | 0 |
| Core·CMP4 | Small DC Locker | 3x1x3 | 20 | 0 |
| Core·CMP5 | Deck Gear Locker | 3x1x6 | 30 | 0 |
| Core·CMP6 | Deck Gear Locker | 3x1x6 | 30 | 0 |
| Stern·MOD1 | BW1500 Drive | 12x12x12 | 10 | 0 |
| Bow·MOD1 | Flight Deck Traversal System | 3x3x3 | 20 | -200 |
| Core·MOD1 | Ithaca Bridgemaster | 2x2x2 | 10 | -1200 |
| Stern·MOD2 | Civilian Reactor | 5x5x5 | 10 | +3650 |
| Bow·MOD2 | Flight Deck Traversal System | 3x3x3 | 20 | -200 |
| Core·MOD2 | Flight Deck Traversal System | 3x3x3 | 20 | -200 |

- 合计：部件 675 点 + 舰体 600 点 = **1275 点**（不含弹库与弹药，见下）
- 另有弹库 0 点 + 弹药 781 点 + 舰载机 59 架 839 点 ⇒ **全价约 2895 点**（估算；游戏里以存档原值 3000 为准，单价见 `zh/弹药点数表.md`）
- 供电：发电 3650 kW / 耗电 1854 kW（余量 +1796 kW）
- 弹库装载：Stern·MT10 VLS-1-46 Launcher：SGM-100 ARM ×1、EA14 Chaff Decoy ×6；Core·CMP2 Bulk Magazine：100mm HE Shell ×500、20mm Slug ×38000、SDM-201 Sticker ×40、SGM-102 AAM ×16、SGM-103 Wake ×16、SGM-210 SEPD ×4、SGT-300 Pilum ×18、S2 Glide Bomb ×24、S1 Rocket ×30、S3 Rocket ×40、SGT-300 Pilum Block III ×18、50mm Slug ×1000


## 样板船完整装配（整艘照抄）：All Reaching All Taking（Amethyst Squadron）

**整艘照抄**：舰体 `Container Hauler Refit`（阵营键 `Stock/Outlying Systems Protectorate`），存档原值 **3000 点**，共 18 个槽位。复制这艘船时连它自带的导弹一起抄，只改船名、呼号和导弹名。

| 槽位 | 部件 | 尺寸 | 点数 | 供电 kW |
|---|---|---|---:|---:|
| Core·MT1 | Container Bank Hangar | 20x5x20 | 100 | -1 |
| Core·MT2 | Container Bank Hangar | 20x5x20 | 100 | -1 |
| Bow·MT3 | Container Bank Hangar | 20x5x20 | 100 | -1 |
| Bow·MT4 | Container Bank Hangar | 20x5x20 | 100 | -1 |
| Core·MT8 | T30 Cannon ⚠ 槽只有 3×4×3 | 6x3x6 | 20 | -120 |
| Stern·MT11 | VLS-1-46 Launcher | 3x2x3 | 5 | -50 |
| Bow·CMP1 | Damage Control Complex | 6x3x6 | 55 → 之后 4/座 | 0 |
| Core·CMP1 | Large DC Storage | 6x3x6 | 45 | 0 |
| Core·CMP2 | Reinforced Magazine | 1x1x1 | 0 → 之后 40/座 | 0 |
| Bow·CMP2 | Reinforced CIC | 4x1x6 | 25 | 0 |
| Bow·CMP3 | Deck Gear Locker | 3x1x6 | 30 | 0 |
| Core·CMP3 | Auxiliary Steering | 3x1x3 | 10 | 0 |
| Core·CMP4 | Deck Gear Locker | 3x1x6 | 30 | 0 |
| Core·CMP5 | Deck Gear Locker | 3x1x6 | 30 | 0 |
| Stern·MOD1 | CHI-9100 Long Haul Drive | 12x12x12 | 20 | 0 |
| Bow·MOD1 | Flight Deck Traversal System | 3x3x3 | 20 | -200 |
| Core·MOD1 | Ithaca Bridgemaster | 2x2x2 | 10 | -1200 |
| Stern·MOD2 | Civilian Reactor | 5x5x5 | 10 | +3650 |

- 合计：部件 710 点 + 舰体 600 点 = **1310 点**（不含弹库与弹药，见下）
- 另有弹库 0 点 + 弹药 631 点 + 舰载机 54 架 820 点 ⇒ **全价约 2761 点**（估算；游戏里以存档原值 3000 为准，单价见 `zh/弹药点数表.md`）
- 供电：发电 3650 kW / 耗电 1574 kW（余量 +2076 kW）
- 弹库装载：Stern·MT11 VLS-1-46 Launcher：EA14 Chaff Decoy ×5、SGM-1 Scorch ×12、SGM-1 Ceremonial Arming Missile ×1；Core·CMP2 Reinforced Magazine：Mk0sQMiAdkKWQa-16rbg-w ×32、S3 Rocket ×8、S1 Rocket ×80、S3 Cluster Bomb ×8、S2 Glide Bomb ×8、SDM-122 Spamraam ×120、100mm Grapeshot ×250、100mm HE Shell ×500、35mm Flechette ×10000
- ⚠ 存档里这几个槽装的东西比槽位大（旧版本留下的，当前版本装不进去）：Core·MT8 T30 Cannon（6x3x6）塞不进 3×4×3。照抄时换小一号的部件，或改用同功能的小件。


## Author notes (from the fleet's 使用说明.txt)
- CVLN test 5 Newbie: *舰队定位：后排 / *上手难度：极高 / （舰队航母本不应出现在新手包里面。但玩你游不玩航母约等于没玩过，所以我干脆放在新手包里面当参考） / *设备说明 / --船棍航母，携带战斗机，轰炸机,轻型侦察机和一架雷达直升机 / --侦察机既可以格斗，也可以脸探草丛做侦察 / --战斗机主制空，也能挂两发R2火箭反小 / --轰炸机是主力输出，鱼雷引导头 CMD/hoj和CMD/Sah，容易被高玩软杀但是便宜 / --雷达直升机用于辅助轰炸机发现目标 / *优点： / --好玩 / --能有效反制敌方航母和没带防空导弹的目标 / --弹药比较难软杀，也有无法软杀的R3火箭弹 / --轰炸机能扔打穿所以锁血DT的KBU22炸弹 / *缺点： / --航母本体脆弱，死了就没了 / --飞机只有挂弹起飞后才有用，需要玩家小心计划 / --侦察完全依赖Pike侦察机脸探草丛 / --当前版本ANS能装备大量防空导弹，所有OSP航母都很难混 / --对ANS的10炮艇舰队没辙 / 使用注意事项： / 1.侦察机Pike一般开局就要挂油箱出去侦察了 / 2.战斗机用“2X SD 2”挂载打BVR空战，“Fuel Jam 2X AAM”挂载格斗，“Fuel Jam”只有油箱和干扰，适合当肉盾。“2X R2”挂两发R2火箭弹，5机以上一组抓对面小船。 / 战斗机尽量打BVR，尽量躲在石头后面待命而不是停在空中。 / 护航队友需要提前计划。 / 3.轰炸机“Gun 100 HE”是100mm火炮吊舱，用来杀ANS的便宜占点船； / 反舰主力挂载为一波3机“S3 + KBU 22”和1机“S3 + …

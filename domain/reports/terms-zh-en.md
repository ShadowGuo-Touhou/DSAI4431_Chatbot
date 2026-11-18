# 中英术语总表

数据来源：`en-US/en_assets.json` + `zh-CN/cn_assets.json`（同一 key 对照，游戏 0.6.2.6 自带）、`raw_official/*`（尺寸 / 点数 / 供电 / 穿深 / 弹舱值）、`domain/data/`（单发体积、每点发数、装甲、存档键）、352 份存档（实测某部件被哪家实际使用）、`query_terms.py` 与 `manual_zh/`（玩家口语）。

**列说明**

- `类别` 取自 wiki 页面（挂载 / 舱室 / 模块）。
- `阵营`：wiki 有阵营图标写「SA 专属 / OSP 专属」，**没有图标 = 通用**（游戏里双方都能装）。
- `实测（存档）` = 352 份真实存档里这个部件被 SA / OSP 各装了多少次；`⚠` 表示 wiki 说专属、但另一家也在用。

## 译名优先级（冲突时按顺序采纳）

1. **`other info` 里的玩家表格**（`Neb英文缩写.jpg`、`NEB简明指挥术语v0.1.png`，已转成 `domain/kb/manual_zh/缩写与术语表.md`、`指挥术语.md`）——最高，玩家实际在用。
2. **中文舰队包 readme**（`群新手舰队包 v1.12` 的 `使用说明.txt`）——高，作者行文用语。
3. **游戏官方中文本地化**（`zh-CN/cn_*.json`）——**最低**：机翻痕迹明显（点防炮/战情室/损管机柜），简体包里还混着繁体字（石牆、修復、彈艙）。术语表里所有「中文」列都来自这一层，仅作参考。

## 已知译名冲突（按上表取舍）

| 概念 | 官方本地化（低） | 玩家表 / readme（优先） |
|---|---|---|
| PDT | 点防炮 | 点防御炮、近防炮、PDT |
| CIC | 战情室、强化型战情室 | CIC、指挥舱 |
| DC Locker | 损管机柜 | 损管舱、损管柜 |
| Chaff | 无「箔条」一词，统一译「诱饵」 | 箔条（EA12 chaff） |
| Soft-kill / Hard-kill | 软杀 / 硬杀（仅教程与 UI 零星出现） | 软杀 / 硬杀（口语高频） |
| 舰船级别 CC/DD/CH… | 无 | CC/DD/CH/BB/FF/FFL/LN/MN/CV/CVL/CVE（玩家约定，见 `舰船级别对照.md`） |
| 导弹口语 S3 / S3F | 无 | S3=SGT-3、S3F=SGM-3 |
| 繁简混用 | 石牆 / 修復 / 彈艙 | 石墙 / 修复 / 弹舱 |
| 炸弹 | 250mm Bomb Shell 译「250mm 炸弹外壳」 | 直接叫「250 航弹」，和 250 RPF 一样用来打小艇 |

## 玩家用词习惯（很重要）

- 这款游戏中文社区长期没有可用本地化，**绝大多数中文玩家直接用英文原名与缩写**（Ocello、VLS-2、PDT、softkill）。
- 所以知识库与人设要**同时支持两种输入**：英文名照常检索；中文名按本表映射后再检索。
- **回答跟随提问语言**：用户用中文问就用中文答，但凡是中文译名（尤其是舰级/舰名）要提醒一句「中文译名不一定准确，以英文名为准」。
- 舰船名优先用英文原名，需要时补官方中文；官方中文目前只有零星几条（见下）。

## 舰船总表（16 艘，阵营 / 装甲 / 结构 / 价格 / 存档键）

装甲与 DR 取自玩家在游戏面板实测（`domain/data/hull_armour.json`）并与 wiki 记录一致；价格取 wiki 舰体页；存档键来自 `domain/data/game_names.json`。

| English | 阵营 | 装甲 (cm) | 部件 DR | 结构值 | 雷达信号 | 价格 (pts) | 槽位 | 存档键 |
|---|---|---|---|---|---|---|---|---|
| Axford Heavy Cruiser | SA 专属 | 40 | 40 | 6500 | 14332 | 600 | 11 Mounts 11 Compartments 12 Modules | Stock/Axford Heavy Cruiser |
| Draugr Clipper | OSP 专属 | 5 | 0 | 1000 | 4685 | 100 | 5 Mounts 5 Compartments 4 Modules | Stock/Tugboat |
| Ferryman Clipper | OSP 专属 | 5 | 0 | 1000 | 2890 | 50 | 3 Mounts 3 Compartments 4 Modules | Stock/Shuttle |
| Flathead Monitor | OSP 专属 | 48 | 20 | 1000 | 9869 | 200 | 6 Mounts 6 Compartments 7 Modules | Stock/Bulk Feeder |
| Journeyman Light Carrier | OSP 专属 | 12 | 20 | 1000 | 14182 | 300 | 3 Mounts 8 Compartments 6 Modules | Stock/Ore Carrier |
| Keystone Destroyer | SA 专属 | 22 | 10 | 4000 | 6282 | 200 | 7 Mounts 7 Compartments 7 Modules | Stock/Keystone Destroyer |
| Levy Escort Carrier | SA 专属 | 15 | 25 | 6500 | 16516 | 500 | 4 Mounts 10 Compartments 8 Modules | Stock/Levy Escort Carrier |
| Marauder Line Ship | OSP 专属 | 20 | 35 | 4000 | 31,045–47,400 m² | 375 | 17 Mounts 9 Compartments 8 Modules | Stock/Bulk Hauler |
| Mercator Replenishment Oiler | SA 专属 | 15 | 5 | 3000 | 3783 | 3000 | 3 Mounts 8 Compartments 4 Modules | Stock/Mercator Oiler |
| Moorline Line Ship | OSP 专属 | 20 | 20 | 3000 | 33,781–50,424 m² | 600 | 10 Mounts 9 Compartments 6 Modules | Stock/Container Hauler |
| Ocello Command Cruiser | OSP 专属 | 30 | 40 | 6500 | 15745 | 575 | 11 Mounts 9 Compartments 10 Modules | Stock/Ocello Cruiser |
| Raines Frigate | SA 专属 | 15 | 5 | 3000 | 3783 | 125 | 4 Mounts 5 Compartments 5 Modules | Stock/Raines Frigate |
| Solomon Battleship | SA 专属 | 56 | 40 | 8000 | 27876 | 1000 | 14 Mounts 16 Compartments 15 Modules | Stock/Solomon Battleship |
| Sprinter Corvette | SA 专属 | 8 | 0 | 1000 | 2890 | 75 | 4 Mounts 4 Compartments 4 Modules | Stock/Sprinter Corvette |
| Vauxhall Light Cruiser | SA 专属 | 26 | 20 | 5500 | 11727 | 350 | 10 Mounts 9 Compartments 9 Modules | Stock/Vauxhall Light Cruiser |
| Worden Fleet Carrier | SA 专属 | 30 | 30 | 5000 | 34357 | 3000 | 13 Mounts 20 Compartments 14 Modules | Stock/Worden Fleet Carrier |

> 15 艘主力舰都在上表；`Shuttle` / `Tugboat` 之类的民船没有装甲数据（5 cm 左右）。舰级缩写（FFL/DD/CH/LN/CV…）见 `舰船级别对照.md`，本表不重复。

## 舰级名称（官方 `HULLCLASSIFICATION_*`，在 `cn_ui.json` 里）

| English | 官方中文 | 建议用法 |
|---|---|---|
| Corvette | 轻型护卫舰 | 口语 FFL |
| Frigate | 护卫舰 | 口语 FF |
| Destroyer | 驱逐舰 | 口语 DD |
| Light Cruiser | 轻型巡洋舰 | 口语 CL |
| Heavy Cruiser | 重型巡洋舰 | 口语 CH |
| Command Cruiser | 指挥巡洋舰 | 口语 CC |
| **Line Ship** | **战列舰** | ⚠️ 官方误译，正确是**线列舰**；口语 LN |
| **Battleship** | **战舰** | ⚠️ 官方误译，正确是**战列舰**；口语 BB |
| Monitor | 炮舰 | 口语 MN |
| Clipper | 飞剪舰 | Ferryman / Draugr |
| Escort Carrier | 护卫航母 | 口语 CVE |
| Light Carrier | 轻型航母 | 口语 CVL |
| Fleet Carrier | 舰队航母 | 口语 CV（Worden） |
| Replenishment Oiler | 补给舰 | Mercator，无缩写 |

> 官方把 Line Ship 译成「战列舰」、Battleship 译成「战舰」，**两个是反的**。中文里说「线列舰 / 战列舰」区分，英文优先 `line ship` / `battleship`。

## 舰段与阵营键（存档相关）

- **线列舰 / 航母的 A/B/C 只是外观**：`Bulk - A - Bow` 与 `B`、`C` 的 14 个槽位**键、尺寸、类型完全一致**（已用 `hull_sockets.json` 逐键比对），所以配装表对三种舰段通用。
- 存档里的 `<FactionKey>` 只有两个值：`Stock/Alliance`（SA）、`Stock/Protectorate`（OSP）。部件键是 `Stock/<部件名>`，**不带阵营前缀**；写了不存在的阵营键会让整船槽位清空。
- 舰体键 `Stock/<HullName>`（例如 `Stock/Axford Heavy Cruiser`，去掉「Class」）。

> 中文列填“待补”的就是缺译名的；改完告诉我，我重新生成知识库。

## 部件 / 挂载（143 条）

| English | 中文 | 尺寸(格) | 点数 | 供电 | 关键数值 | 阵营（wiki） | 存档实测 | 建议 |
|---|---|---|---|---|---|---|---|---|
| Actively Cooled Amplifiers | 主动式冷却放大器 | 2x2x2 | 25 | 175 kW | - | 通用 | SA 56 / OSP 14 | 通用（实测） |
| Adaptive Radar Receiver | 自适应雷达接收机 | 2x2x2 | 30 | 200 kW | - | 通用 | SA 48 / OSP 26 | 通用（实测） |
| Ammunition Elevators | 弹药升降机 | 2x2x2 | 20 | 150 kW | - | 通用 | SA 521 / OSP 264 | 通用（实测） |
| Analysis Annex | 分析舱 | 3x1x3 | 20 | - | - | 通用 | SA 10 / OSP 1 | 通用（实测） |
| Auxiliary Steering | 辅助舵轮舱 | 3x1x3 | 10（1x 叠加价） | - | - | 通用 | SA 166 / OSP 147 | 通用（实测） |
| Basic CIC | 基础战情室 | 4x1x6 | 10（1x 叠加价） | - | - | 通用 | SA 295 / OSP 194 | 通用（实测） |
| Boosted Reactor | 强化反应堆 | 5x5x5 | 10 | 5000 kW | - | OSP 专属 | SA 0 / OSP 157 | OSP 专属（实测） |
| Bulk Internal Hangar | 大型内部机库 | 6x3x6 | 10 | 0 kW | - | 通用 | SA 70 / OSP 15 | 通用（实测） |
| Bulk Magazine | 大型弹舱 | 1x1x1 | 20（0x 叠加价） | - | +15 m³/格 | 通用 | SA 92 / OSP 114 | 通用（实测） |
| Bulwark Huntress | 要塞女猎手 | 2x2x2 | 30 | 2000 kW | 射程 10 | OSP 专属 | SA 0 / OSP 50 | OSP 专属（实测） |
| BW1500 Drive | BW1500 驱动系统 | 12x12x12 | 10 | +300 kW | - | OSP 专属 | SA 0 / OSP 74 | OSP 专属（实测） |
| BW1500-R Drive | BW1500-R 驱动系统 | 12x12x12 | 20 | +300 kW | - | OSP 专属 | SA 0 / OSP 5 | OSP 专属（实测） |
| BW2000 Drive | BW2000 驱动系统 | 12x12x12 | 15 | +2000 kW | - | OSP 专属 | SA 0 / OSP 13 | OSP 专属（实测） |
| BW800 Drive | BW800 驱动系统 | 5x3x5 | 10 | +300 kW | - | OSP 专属 | SA 0 / OSP 75 | OSP 专属（实测） |
| BW800-R Drive | BW800-R 驱动系统 | 5x3x5 | 20 | +300 kW | - | OSP 专属 | SA 0 / OSP 47 | OSP 专属（实测） |
| C30 Cannon | C30 火炮 | 2x5x2 | 20 | 100 kW | 24 发/30s · 48.0 发/分 | OSP 专属 | SA 0 / OSP 10 | OSP 专属（实测） |
| C53 Cannon | C53 火炮 | 2x4x2 | 10 | 100 kW | 8 发/50s · 9.6 发/分 | OSP 专属 | SA 0 / OSP 75 | OSP 专属（实测） |
| C56 Cannon | C56 火炮 | 4x6x4 | 20 | 100 kW | 15 发/70s · 12.9 发/分 | OSP 专属 | 未见样本 | OSP 专属 |
| C65 Cannon | C65 火炮 | 6x10x6 | 40 | 300 kW | 8 发/90s · 5.3 发/分 | OSP 专属 | SA 0 / OSP 100 | OSP 专属（实测） |
| C81 Plasma Cannon | C81 电浆炮 | 4x6x4 | 30 | 1200 kW | - | OSP 专属 | SA 0 / OSP 26 | OSP 专属（实测） |
| C90 Cannon | C90 火炮 | 6x12x6 | 60 | 200 kW | 1 发/18s · 3.3 发/分 | OSP 专属 | SA 0 / OSP 10 | OSP 专属（实测） |
| CHI-7700 Drive | CHI-7700 驱动系统 | 12x12x12 | 20 | +300 kW | - | OSP 专属 | SA 0 / OSP 28 | OSP 专属（实测） |
| CHI-777 Yard Drive | CHI-777 船厂驱动系统 | 5x3x5 | 20 | +300 kW | - | OSP 专属 | SA 0 / OSP 25 | OSP 专属（实测） |
| CHI-9100 Long Haul Drive | CHI-9100 长征驱动系统 | 12x12x12 | 20 | +300 kW | - | OSP 专属 | SA 0 / OSP 8 | OSP 专属（实测） |
| Citadel CIC | 堡垒战情室 | 6x1x8 | 75（1x 叠加价） | - | - | 通用 | SA 74 / OSP 22 | 通用（实测） |
| Citadel Magazine | 堡垒弹舱 | 1x3x1 | 150（0x 叠加价） | - | - | OSP 专属 | SA 0 / OSP 96 | OSP 专属（实测） |
| Civilian Reactor | 民用反应堆 | 5x5x5 | 10 | 3650 kW | - | OSP 专属 | SA 0 / OSP 130 | OSP 专属（实测） |
| CLS-3 Launcher | CLS-3 发射器 | 3x4x3 | 20 | 200 kW | ≤4 发 × S3 | SA 专属 | SA 167 / OSP 17（含 CC 跨阵营） | SA 专属（CC 例外） |
| Container Bank Hangar | 货柜舱机库 | 20x5x20 | 100 | 1 kW | - | OSP 专属 | SA 0 / OSP 84 | OSP 专属（实测） |
| Container Bank Launcher | 货柜舱发射器 | 20x5x10 | 25 | 200 kW | ≤48 发 × S4 | OSP 专属 | SA 0 / OSP 70 | OSP 专属（实测） |
| Container Datalink Array | 货柜资料链阵列 | 6x3x6 | 200 | - | - | OSP 专属 | SA 0 / OSP 12 | OSP 专属（实测） |
| Container Stack Launcher | 货柜堆发射器 | 6x1x6 | 5 | 50 kW | ≤2 发 × S4 | OSP 专属 | SA 0 / OSP 49 | OSP 专属（实测） |
| CR10 Antenna | CR10 天线 | 2x1x2 | 5 | 250 kW | - | SA 专属 | SA 13 / OSP 25（含 CC 跨阵营） | SA 专属（CC 例外） |
| CR70 Antenna | CR70 天线 | 2x1x2 | 15 | 600 kW | - | SA 专属 | SA 68 / OSP 0 | SA 专属（实测） |
| CR75 Antenna | CR75 天线 | - | - | - |  | 通用 | 未见样本 | 通用 |
| Damage Control Central | 损害管制中枢 | 3x1x3 | 20 | 50 kW | - | 通用 | SA 104 / OSP 14 | 通用（实测） |
| Damage Control Complex | 损害管制区 | 6x3x6 | 55（4x 叠加价） | 0 kW | - | OSP 专属 | SA 0 / OSP 65 | OSP 专属（实测） |
| Deck Gear Locker | 甲板工具柜 | 3x1x6 | 30 | 0 kW | - | 通用 | SA 52 / OSP 76 | 通用（实测） |
| E15 'Masquerade' Deception Module | E15「化装舞会」欺骗模块 | - | - | - |  | 通用 | 未见样本 | 通用 |
| E20 'Lighthouse' Illuminator | E20「灯塔」照明雷达 | 2x1x2 | 15 | 600 kW | - | OSP 专属 | SA 0 / OSP 17 | OSP 专属（实测） |
| E55 'Spotlight' Illuminator | E55「探照灯」照明雷达 | 2x1x2 | 15 | 750 kW | - | SA 专属 | SA 15 / OSP 3（含 CC 跨阵营） | SA 专属（CC 例外） |
| E57 'Floodlight' Illuminator | E57「泛光灯」照明雷达 | - | - | - |  | 通用 | SA 41 / OSP 31 | 通用（实测） |
| E70 'Interruption' Jammer | E70「中断」干扰器 | 3x1x3 | 55 | 600 kW | - | SA 专属 | SA 101 / OSP 27（含 CC 跨阵营） | SA 专属（CC 例外） |
| E71 'Hangup' Jammer | E71「挂断」干扰器 | 2x1x2 | 45 | 500 kW | - | SA 专属 | SA 52 / OSP 0 | SA 专属（实测） |
| E90 'Blanket' Jammer | E90「地毯」干扰器 | 2x1x2 | 50 | 1000 kW | - | SA 专属 | SA 171 / OSP 34（含 CC 跨阵营） | SA 专属（CC 例外） |
| Energy Regulator | 能量调节器 | 3x3x3 | 30 | 650 kW | - | 通用 | SA 52 / OSP 39 | 通用（实测） |
| ES22 'Pinard' Electronic Support Module | ES22「皮纳德」电子支援模块 | 3x1x3 | 30 | 200 kW | - | SA 专属 | SA 46 / OSP 0 | SA 专属（实测） |
| ES32 'Scryer' Missile ID System | ES32「预言者」导弹辨识系统 | 2x2x2 | 10 | 300 kW | - | 通用 | SA 162 / OSP 59 | 通用（实测） |
| Fire Suppression System | 灭火系统 | 2x2x2 | 20 | 100 kW | - | 通用 | SA 2 / OSP 5 | 通用（实测） |
| Flight Deck Traversal System | 飞行甲板通行系统 | 3x3x3 | 20 | 200 kW | - | 通用 | SA 71 / OSP 57 | 通用（实测） |
| FM200 Drive | FM200 驱动系统 | 5x3x5 | 10 | +500 kW | - | SA 专属 | SA 108 / OSP 0 | SA 专属（实测） |
| FM200R Drive | FM200R 驱动系统 | 5x3x5 | 20 | +500 kW | - | SA 专属 | SA 4 / OSP 0 | SA 专属（实测） |
| FM230 'Whiplash' Drive | FM230「甩鞭」驱动系统 | 5x3x5 | 20 | +650 kW | - | SA 专属 | SA 337 / OSP 5（含 CC 跨阵营） | SA 专属（CC 例外） |
| FM240 'Dragonfly' Drive | FM240「蜻蜓」驱动系统 | 5x3x5 | 20 | +500 kW | - | SA 专属 | SA 123 / OSP 1（含 CC 跨阵营） | SA 专属（CC 例外） |
| FM280 'Raider' Drive | FM280「掠夺者」驱动系统 | 5x3x5 | 20 | +0 kW | - | SA 专属 | SA 17 / OSP 0 | SA 专属（实测） |
| FM30X 'Prowler' Drive | FM30X「徘徊者」驱动系统 | 5x3x5 | 25 | +350 kW | - | SA 专属 | SA 21 / OSP 0 | SA 专属（实测） |
| FM500 Drive | FM500 驱动系统 | 10x8x10 | 15 | +1000 kW | - | SA 专属 | SA 35 / OSP 9（含 CC 跨阵营） | SA 专属（CC 例外） |
| FM500R Drive | FM500R 驱动系统 | 10x8x10 | 30 | +1000 kW | - | SA 专属 | SA 2 / OSP 0 | SA 专属（实测） |
| FM530 'Whiplash' Drive | FM530「甩鞭」驱动系统 | 10x8x10 | 30 | +1500 kW | - | SA 专属 | SA 93 / OSP 29（含 CC 跨阵营） | SA 专属（CC 例外） |
| FM540 'Dragonfly' Drive | FM540「蜻蜓」驱动系统 | 10x8x10 | 30 | +1000 kW | - | SA 专属 | SA 59 / OSP 5（含 CC 跨阵营） | SA 专属（CC 例外） |
| FM580 'Raider' Drive | FM580「掠夺者」驱动系统 | 10x8x10 | 30 | +500 kW | - | SA 专属 | SA 53 / OSP 15（含 CC 跨阵营） | SA 专属（CC 例外） |
| Focused Particle Accelerator | 聚焦式粒子加速器 | 3x3x3 | 25 | 800 kW | - | SA 专属 | SA 146 / OSP 0 | SA 专属（实测） |
| FR3300 Micro Reactor | FR3300 微型反应堆 | 3x3x3 | 10 | 2250 kW | - | SA 专属 | SA 602 / OSP 48（含 CC 跨阵营） | SA 专属（CC 例外） |
| FR4800 Reactor | FR4800 反应堆 | 5x5x5 | 10 | 4200 kW | - | SA 专属 | SA 365 / OSP 50（含 CC 跨阵营） | SA 专属（CC 例外） |
| Gun Plotting Center | 火炮测绘室 | 3x1x3 | 30 | - | - | 通用 | SA 127 / OSP 69 | 通用（实测） |
| Intelligence Center | 情报室 | 6x1x8 | 90 | - | - | 通用 | SA 53 / OSP 60 | 通用（实测） |
| Ithaca Bridgemaster | 伊萨卡渡桥者 | 2x2x2 | 10 | 1200 kW | 射程 8.5 | OSP 专属 | SA 0 / OSP 227 | OSP 专属（实测） |
| J15 'Bellbird' Jammer | J15「伞鸟」干扰器 | 3x1x3 | 50 | 850 kW | - | OSP 专属 | 未见样本 | OSP 专属 |
| J360 'Lyrebird' Jammer | J360「琴鸟」干扰器 | 3x1x3 | 75 | 500 kW | - | OSP 专属 | 未见样本 | OSP 专属 |
| J75 'Warbler' Jammer | J75「林莺」干扰器 | 3x1x3 | 50 | 500 kW | - | OSP 专属 | 未见样本 | OSP 专属 |
| Jury-Rigged Reactor | 应急反应堆 | 6x3x6 | 20 | - | - | OSP 专属 | SA 0 / OSP 5 | OSP 专属（实测） |
| L50 'Blackjack' Laser Dazzler | L50「二十一点」激光眩目器 | 2x1x2 | 40 | 750 kW | - | OSP 专属 | 未见样本 | OSP 专属 |
| Large DC Locker | 大型损管机柜 | 3x1x6 | 45 | 0 kW | - | 通用 | SA 322 / OSP 83 | 通用（实测） |
| Large DC Storage | 大型损管仓储 | 6x3x6 | 45 | 0 kW | - | OSP 专属 | SA 0 / OSP 41 | OSP 专属（实测） |
| Large Mounted Hangar | 大型基座式机库 | 8x7x8 | 10 | 1 kW | - | SA 专属 | 未见样本 | SA 专属 |
| Light Civilian Reactor | 轻型民用反应堆 | 3x3x3 | 10 | 1850 kW | - | OSP 专属 | SA 0 / OSP 164 | OSP 专属（实测） |
| Medium Mounted Hangar | 中型基座式机库 | 6x4x6 | 10 | 1 kW | - | SA 专属 | 未见样本 | SA 专属 |
| Missile Parallel Interface | 导弹平行介面 | 2x2x2 | 40 | 150 kW | - | 通用 | SA 59 / OSP 44 | 通用（实测） |
| Missile Programming Bus | 导弹编程汇流排 | 2x2x2 | 30 | 200 kW | - | SA 专属 | SA 97 / OSP 5（含 CC 跨阵营） | SA 专属（CC 例外） |
| Missile Programming Bus Array | 导弹编程汇流排阵列 | 3x3x3 | 50 | 350 kW | - | SA 专属 | SA 157 / OSP 46（含 CC 跨阵营） | SA 专属（CC 例外） |
| Mk20 'Defender' PDT | Mk20「防御者」点防炮 | 2x1x2 | 25 | 175 kW | - | SA 专属 | SA 694 / OSP 16（含 CC 跨阵营） | SA 专属（CC 例外） |
| Mk25 'Rebound' PDT | Mk25「反弹」点防炮 | 2x1x2 | 15 | 20 kW | - | SA 专属 | SA 77 / OSP 0 | SA 专属（实测） |
| Mk29 'Stonewall' PDT | Mk29「石牆」点防炮 | 3x1x3 | 30 | 40 kW | - | SA 专属 | SA 155 / OSP 5（含 CC 跨阵营） | SA 专属（CC 例外） |
| Mk550 Railgun | Mk550 磁轨炮 | - | 75 | 2000 kW | - | SA 专属 | 未见样本 | SA 专属 |
| Mk600 Beam Cannon | Mk600 光束炮 | - | 75 | 3000 kW | - | SA 专属 | SA 91 / OSP 0 | SA 专属（实测） |
| Mk61 Cannon | Mk61 火炮 | 3x1x3 | 10 | 50 kW | 1 发/5.5s · 10.9 发/分 | SA 专属 | SA 51 / OSP 0 | SA 专属（实测） |
| Mk610 Beam Turret | Mk610 光束炮塔 | 8x5x8 | 80 | 3000 kW | - | SA 专属 | SA 24 / OSP 0 | SA 专属（实测） |
| Mk62 Cannon | Mk62 火炮 | 3x1x3 | 20 | 50 kW | 1 发/4s · 15.0 发/分 | SA 专属 | SA 179 / OSP 0 | SA 专属（实测） |
| Mk64 Cannon | Mk64 火炮 | 3x1x5 | 30 | 125 kW | 1 发/10s · 6.0 发/分 | SA 专属 | SA 180 / OSP 0 | SA 专属（实测） |
| Mk65 Cannon | Mk65 火炮 | 6x3x6 | 40 | 180 kW | 3 发/13s · 13.8 发/分 | SA 专属 | SA 9 / OSP 4（含 CC 跨阵营） | SA 专属（CC 例外） |
| Mk66 Cannon | Mk66 火炮 | 6x3x6 | 45 | 200 kW | 2 发/20s · 6.0 发/分 | SA 专属 | SA 87 / OSP 105（含 CC 跨阵营） | SA 专属（CC 例外） |
| Mk68 Cannon | Mk68 火炮 | 8x5x8 | 75 | 225 kW | 3 发/20s · 9.0 发/分 | SA 专属 | SA 132 / OSP 0 | SA 专属（实测） |
| Mk81 Railgun | Mk81 磁轨炮 | 6x3x6 | 75 | 1500 kW | 3 发/100s · 1.8 发/分 | SA 专属 | SA 6 / OSP 6（含 CC 跨阵营） | SA 专属（CC 例外） |
| Mk90 'Aurora' PDT | Mk90「极光」点防炮 | 2x1x2 | 55 | 1250 kW | - | SA 专属 | SA 136 / OSP 147（含 CC 跨阵营） | SA 专属（CC 例外） |
| Mk95 'Sarissa' PDT | Mk95「萨里沙」点防炮 | 3x1x3 | 65 | 1250 kW | - | SA 专属 | SA 76 / OSP 30（含 CC 跨阵营） | SA 专属（CC 例外） |
| ML-9 Mine Launcher | ML-9 空雷发射器 | - | - | - |  | 通用 | SA 0 / OSP 91 | OSP 专属（实测） |
| MLS-2 Launcher | MLS-2 发射器 | 2x2x5 | 15 | 50 kW | ≤4 发 × S2 | OSP 专属 | SA 0 / OSP 57 | OSP 专属（实测） |
| MLS-3 Launcher | MLS-3 发射器 | 2x2x5 | 15 | 50 kW | ≤2 发 × S3 | OSP 专属 | SA 0 / OSP 55 | OSP 专属（实测） |
| Mount Gyros | 陀螺仪基座 | 2x2x2 | 20 | 150 kW | - | 通用 | SA 140 / OSP 23 | 通用（实测） |
| P11 'Pavise' PDT | P11「大盾」点防炮 | 2x1x2 | 20 | 150 kW | - | OSP 专属 | 未见样本 | OSP 专属 |
| P20 'Bastion' PDT | P20「棱堡」点防炮 | 2x1x2 | 15 | 40 kW | - | OSP 专属 | 未见样本 | OSP 专属 |
| P60 'Grazer' PDT | P60「飞掠者」点防炮 | 2x1x2 | 35 | 1500 kW | - | OSP 专属 | 未见样本 | OSP 专属 |
| Plant Control Center | 厂房控制室 | 3x1x3 | 25 | - | - | 通用 | SA 266 / OSP 69 | 通用（实测） |
| R400 'Bloodhound' LRT Radar | R400「寻血犬」长程雷达 | 2x5x2 | 15 | 3000 kW | - | OSP 专属 | 未见样本 | OSP 专属 |
| R550 Early Warning Radar | R550 早期预警雷达 | 3x1x3 | 40 | 4500 kW | - | OSP 专属 | SA 0 / OSP 32 | OSP 专属（实测） |
| Rapid DC Locker | 快速损管机柜 | 3x1x3 | 10 | 0 kW | - | 通用 | SA 579 / OSP 249 | 通用（实测） |
| Rapid-Cycle Cradle | 快速装填吊架 | 3x3x3 | 20 | 150 kW | - | 通用 | SA 26 / OSP 96 | 通用（实测） |
| Redundant Reactor Failsafes | 冗馀反应堆保险 | 2x2x2 | 10 | 100 kW | - | 通用 | SA 1 / OSP 5 | 通用（实测） |
| Reinforced CIC | 强化型战情室 | 4x1x6 | 25（1x 叠加价） | - | - | 通用 | SA 384 / OSP 246 | 通用（实测） |
| Reinforced DC Locker | 强化型损管机柜 | 3x1x6 | 45 | 0 kW | - | 通用 | SA 254 / OSP 136 | 通用（实测） |
| Reinforced Magazine | 强化型弹舱 | 1x1x1 | 40（0x 叠加价） | - | +10 m³/格 | 通用 | SA 504 / OSP 195 | 通用（实测） |
| Reinforced Thruster Nozzles | 强化型推进喷嘴 | 2x2x2 | 10 | 0 kW | - | 通用 | SA 0 / OSP 17 | OSP 专属（实测） |
| RF101 'Bullseye' Radar | RF101「靶心」雷达 | 2x1x2 | 40 | 300 kW | - | SA 专属 | SA 204 / OSP 52（含 CC 跨阵营） | SA 专属（CC 例外） |
| RF44 'Pinpoint' Radar | RF44「标明」雷达 | 2x1x2 | 10 | 250 kW | - | OSP 专属 | SA 0 / OSP 118 | OSP 专属（实测） |
| RL18 Launcher | RL18 发射器 | 3x1x3 | 30 | 50 kW | ≤18 发 × S2 | OSP 专属 | SA 0 / OSP 65 | OSP 专属（实测） |
| RL36 Launcher | RL36 发射器 | 6x3x6 | 30 | 75 kW | ≤36 发 × S2 | OSP 专属 | SA 0 / OSP 8 | OSP 专属（实测） |
| RM50 'Parallax' Radar | RM50「视差」雷达 | 2x2x2 | 45 | 3600 kW | 射程 9.5 | SA 专属 | SA 108 / OSP 44（含 CC 跨阵营） | SA 专属（CC 例外） |
| RS35 'Frontline' Radar | RS35「前线」雷达 | 2x2x2 | 10 | 2000 kW | 射程 8 | SA 专属 | SA 267 / OSP 3（含 CC 跨阵营） | SA 专属（CC 例外） |
| RS41 'Spyglass' Radar | RS41「小望远镜」雷达 | 2x2x2 | 25 | 4000 kW | 射程 11.5 | SA 专属 | SA 143 / OSP 9（含 CC 跨阵营） | SA 专属（CC 例外） |
| SALS-2 'Ward' Launcher | SALS-2「牢房」发射器 | 3x4x3 | 5 | 50 kW | ≤1 发 × S2 | OSP 专属 | 未见样本 | OSP 专属 |
| Signature Scrambler | 讯迹扰码器 | 2x2x2 | 35 | 450 kW | - | 通用 | SA 4 / OSP 1 | 通用（实测） |
| Small DC Locker | 小型损管机柜 | 3x1x3 | 20 | 0 kW | - | 通用 | SA 261 / OSP 163 | 通用（实测） |
| Small Energy Regulator | 小型能量调节器 | 2x2x2 | 20 | 400 kW | - | 通用 | SA 12 / OSP 7 | 通用（实测） |
| Small Mounted Hangar | 小型基座式机库 | 6x4x6 | 10 | 1 kW | - | OSP 专属 | 未见样本 | OSP 专属 |
| Small Reactor Booster | 小型反应堆强化件 | 2x2x2 | 10 | 0 kW | - | 通用 | SA 31 / OSP 7 | 通用（实测） |
| Small Workshop | 小型工坊 | 3x1x3 | 20 | 50 kW | - | 通用 | SA 56 / OSP 14 | 通用（实测） |
| Spacecraft Repair Station | 战机维修站 | 3x1x6 | 15 | 0 kW | - | 通用 | SA 7 / OSP 5 | 通用（实测） |
| Spacecraft Strikedown Station | 战机整备站 | 3x1x6 | 75 | 0 kW | - | 通用 | SA 12 / OSP 6 | 通用（实测） |
| Strike Planning Center | 导弹计画室 | 6x1x8 | 70 | - | - | 通用 | SA 130 / OSP 27 | 通用（实测） |
| Strobe Correlator | 闪烁相关器 | 2x2x2 | 15 | 150 kW | - | 通用 | 未见样本 | 通用 |
| Sundrive Racing Pro | 日驰 Racing Pro | 5x3x5 | 20 | +200 kW | - | OSP 专属 | SA 0 / OSP 100 | OSP 专属（实测） |
| Supplementary Radio Amplifiers | 辅助无线电放大器 | 2x2x2 | 20 | 100 kW | - | 通用 | SA 5 / OSP 4 | 通用（实测） |
| T20 Cannon | T20 火炮 | 3x1x3 | 15 | 30 kW | 4 发/15s · 16.0 发/分 | OSP 专属 | SA 0 / OSP 136 | OSP 专属（实测） |
| T30 Cannon | T30 火炮 | 6x3x6 | 20 | 120 kW | 16 发/30s · 32.0 发/分 | OSP 专属 | SA 0 / OSP 88 | OSP 专属（实测） |
| T81 Plasma Cannon | T81 电浆炮 | 6x3x6 | 45 | 1500 kW | - | OSP 专属 | SA 0 / OSP 71 | OSP 专属（实测） |
| TALS-2 'Talisman' Launcher | TALS-2 「护符」发射器 | 3x4x5 | 10 | 50 kW | ≤2 发 × S2 | OSP 专属 | 未见样本 | OSP 专属 |
| TE45 Mass Driver | TE45 质量加速器 | - | 100 | 4250 kW | - | OSP 专属 | SA 0 / OSP 26 | OSP 专属（实测） |
| TLS-3 Launcher | TLS-3 发射器 | 3x1x5 | 20 | 250 kW | ≤6 发 × S3 | SA 专属 | 未见样本 | SA 专属 |
| Track Correlator | 跟踪相关器 | 2x2x2 | 25 | 150 kW | - | 通用 | SA 18 / OSP 34 | 通用（实测） |
| VLS-1-23 Launcher | VLS-1-23 发射器 | 2x2x2 | 5 | 50 kW | ≤23 发 × S1 | SA 专属 | SA 304 / OSP 85（含 CC 跨阵营） | SA 专属（CC 例外） |
| VLS-1-46 Launcher | VLS-1-46 发射器 | 3x2x3 | 5 | 50 kW | ≤46 发 × S1 | SA 专属 | SA 170 / OSP 121（含 CC 跨阵营） | SA 专属（CC 例外） |
| VLS-2 Launcher | VLS-2 发射器 | 3x4x3 | 10 | 200 kW | ≤16 发 × S2 | SA 专属 | SA 144 / OSP 46（含 CC 跨阵营） | SA 专属（CC 例外） |
| VLS-3 Launcher | VLS-3 发射器 | 3x4x3 | 20 | 200 kW | ≤4 发 × S3 | SA 专属 | SA 115 / OSP 0 | SA 专属（实测） |

## 舰体自带部件（113 条）

| English | 中文 | 短名 | 短名中文 | 类别 | 阵营 |
|---|---|---|---|---|---|
| BBL Radar Panel | 左后下雷达面板 | - | - | 雷达 | 随舰体 |
| BBR Radar Panel | 右后下雷达面板 | - | - | 雷达 | 随舰体 |
| BL Radar Panel | 左下雷达面板 | - | - | 雷达 | 随舰体 |
| Bottom Radar | 下方雷达 | - | - | 雷达 | 随舰体 |
| BR Radar Panel | 右下雷达面板 | - | - | 雷达 | 随舰体 |
| Braking B01 | 制动 B01 | - | - | 制动引擎 | 随舰体 |
| Braking B02 | 制动 B02 | - | - | 制动引擎 | 随舰体 |
| Braking B03 | 制动 B03 | - | - | 制动引擎 | 随舰体 |
| Braking B04 | 制动 B04 | - | - | 制动引擎 | 随舰体 |
| Braking B05 | 制动 B05 | - | - | 制动引擎 | 随舰体 |
| Braking B06 | 制动 B06 | - | - | 制动引擎 | 随舰体 |
| Braking B07 | 制动 B07 | - | - | 制动引擎 | 随舰体 |
| Braking B08 | 制动 B08 | - | - | 制动引擎 | 随舰体 |
| Braking B09 | 制动 B09 | - | - | 制动引擎 | 随舰体 |
| Braking B10 | 制动 B10 | - | - | 制动引擎 | 随舰体 |
| Braking S01 | 制动 S01 | - | - | 制动引擎 | 随舰体 |
| Braking S02 | 制动 S02 | - | - | 制动引擎 | 随舰体 |
| Braking S03 | 制动 S03 | - | - | 制动引擎 | 随舰体 |
| Braking S04 | 制动 S04 | - | - | 制动引擎 | 随舰体 |
| Braking S05 | 制动 S05 | - | - | 制动引擎 | 随舰体 |
| Braking S06 | 制动 S06 | - | - | 制动引擎 | 随舰体 |
| Braking S07 | 制动 S07 | - | - | 制动引擎 | 随舰体 |
| Braking S08 | 制动 S08 | - | - | 制动引擎 | 随舰体 |
| Braking S09 | 制动 S09 | - | - | 制动引擎 | 随舰体 |
| Braking S10 | 制动 S10 | - | - | 制动引擎 | 随舰体 |
| BTL Radar Panel | 左后上雷达面板 | - | - | 雷达 | 随舰体 |
| BTR Radar Panel | 右后上雷达面板 | - | - | 雷达 | 随舰体 |
| CR10 Ant | CR10 天线 | - | - | 舰体 | 随舰体 |
| CR75 Ant | CR75 天线 | - | - | 舰体 | 随舰体 |
| FBL Radar Panel | 左前后雷达面板 | - | - | 雷达 | 随舰体 |
| FBR Radar Panel | 右前后雷达面板 | - | - | 雷达 | 随舰体 |
| FTL Radar Panel | 左前上雷达面板 | - | - | 雷达 | 随舰体 |
| FTR Radar Panel | 左前下雷达面板 | - | - | 雷达 | 随舰体 |
| Large Pad 01 | 大平台 01 | - | - | 停机坪 | 随舰体 |
| Large Pad 02 | 大平台 02 | - | - | 停机坪 | 随舰体 |
| Large Pad 03 | 大平台 03 | - | - | 停机坪 | 随舰体 |
| Large Pad 04 | 大平台 04 | - | - | 停机坪 | 随舰体 |
| Large Pad 05 | 大平台 05 | - | - | 停机坪 | 随舰体 |
| Large Pad 06 | 大平台 06 | - | - | 停机坪 | 随舰体 |
| Large Pad 07 | 大平台 07 | - | - | 停机坪 | 随舰体 |
| Large Pad 08 | 大平台 08 | - | - | 停机坪 | 随舰体 |
| Large Pad 09 | 大平台 09 | - | - | 停机坪 | 随舰体 |
| Large Pad 10 | 大平台 10 | - | - | 停机坪 | 随舰体 |
| Main 01 | 主 01 | - | - | 主引擎 | 随舰体 |
| Main 02 | 主 02 | - | - | 主引擎 | 随舰体 |
| Main 03 | 主 03 | - | - | 主引擎 | 随舰体 |
| Main 04 | 主 04 | - | - | 主引擎 | 随舰体 |
| Main 05 | 主 05 | - | - | 主引擎 | 随舰体 |
| Main 06 | 主 06 | - | - | 主引擎 | 随舰体 |
| Main 07 | 主 07 | - | - | 主引擎 | 随舰体 |
| Main 08 | 主 08 | - | - | 主引擎 | 随舰体 |
| Main 09 | 主 09 | - | - | 主引擎 | 随舰体 |
| Main 10 | 主 10 | - | - | 主引擎 | 随舰体 |
| Radar (Bottom) | 雷达（下） | - | - | 雷达 | 随舰体 |
| Radar (Top) | 雷达（上） | - | - | 雷达 | 随舰体 |
| Small Pad 01 | 小平台 01 | - | - | 停机坪 | 随舰体 |
| Small Pad 02 | 小平台 02 | - | - | 停机坪 | 随舰体 |
| Small Pad 03 | 小平台 03 | - | - | 停机坪 | 随舰体 |
| Small Pad 04 | 小平台 04 | - | - | 停机坪 | 随舰体 |
| Small Pad 05 | 小平台 05 | - | - | 停机坪 | 随舰体 |
| Small Pad 06 | 小平台 06 | - | - | 停机坪 | 随舰体 |
| Small Pad 07 | 小平台 07 | - | - | 停机坪 | 随舰体 |
| Small Pad 08 | 小平台 08 | - | - | 停机坪 | 随舰体 |
| Small Pad 09 | 小平台 09 | - | - | 停机坪 | 随舰体 |
| Small Pad 10 | 小平台 10 | - | - | 停机坪 | 随舰体 |
| Small Pad 11 | 小平台 11 | - | - | 停机坪 | 随舰体 |
| Small Pad 12 | 小平台 12 | - | - | 停机坪 | 随舰体 |
| Small Pad 13 | 小平台 13 | - | - | 停机坪 | 随舰体 |
| Small Pad 14 | 小平台 14 | - | - | 停机坪 | 随舰体 |
| Small Pad 15 | 小平台 15 | - | - | 停机坪 | 随舰体 |
| Thruster 01 | 推进器 01 | - | - | 姿控/侧推 | 随舰体 |
| Thruster 02 | 推进器 02 | - | - | 姿控/侧推 | 随舰体 |
| Thruster 03 | 推进器 03 | - | - | 姿控/侧推 | 随舰体 |
| Thruster 04 | 推进器 04 | - | - | 姿控/侧推 | 随舰体 |
| Thruster 05 | 推进器 05 | - | - | 姿控/侧推 | 随舰体 |
| Thruster 06 | 推进器 06 | - | - | 姿控/侧推 | 随舰体 |
| Thruster 07 | 推进器 07 | - | - | 姿控/侧推 | 随舰体 |
| Thruster 08 | 推进器 08 | - | - | 姿控/侧推 | 随舰体 |
| Thruster 09 | 推进器 09 | - | - | 姿控/侧推 | 随舰体 |
| Thruster 10 | 推进器 10 | - | - | 姿控/侧推 | 随舰体 |
| Thruster 11 | 推进器 11 | - | - | 姿控/侧推 | 随舰体 |
| Thruster 12 | 推进器 12 | - | - | 姿控/侧推 | 随舰体 |
| Thruster 13 | 推进器 13 | - | - | 姿控/侧推 | 随舰体 |
| Thruster 14 | 推进器 14 | - | - | 姿控/侧推 | 随舰体 |
| Thruster 15 | 推进器 15 | - | - | 姿控/侧推 | 随舰体 |
| Thruster 16 | 推进器 16 | - | - | 姿控/侧推 | 随舰体 |
| Thruster 17 | 推进器 17 | - | - | 姿控/侧推 | 随舰体 |
| Thruster 18 | 推进器 18 | - | - | 姿控/侧推 | 随舰体 |
| Thruster 19 | 推进器 19 | - | - | 姿控/侧推 | 随舰体 |
| Thruster 20 | 推进器 20 | - | - | 姿控/侧推 | 随舰体 |
| Thruster B01 | 推进器 B01 | - | - | 姿控/侧推 | 随舰体 |
| Thruster B02 | 推进器 B02 | - | - | 姿控/侧推 | 随舰体 |
| Thruster B03 | 推进器 B03 | - | - | 姿控/侧推 | 随舰体 |
| Thruster B04 | 推进器 B04 | - | - | 姿控/侧推 | 随舰体 |
| Thruster B05 | 推进器 B05 | - | - | 姿控/侧推 | 随舰体 |
| Thruster B06 | 推进器 B06 | - | - | 姿控/侧推 | 随舰体 |
| Thruster B07 | 推进器 B07 | - | - | 姿控/侧推 | 随舰体 |
| Thruster B08 | 推进器 B08 | - | - | 姿控/侧推 | 随舰体 |
| Thruster B09 | 推进器 B09 | - | - | 姿控/侧推 | 随舰体 |
| Thruster B10 | 推进器 B10 | - | - | 姿控/侧推 | 随舰体 |
| Thruster S01 | 推进器 S01 | - | - | 姿控/侧推 | 随舰体 |
| Thruster S02 | 推进器 S02 | - | - | 姿控/侧推 | 随舰体 |
| Thruster S03 | 推进器 S03 | - | - | 姿控/侧推 | 随舰体 |
| Thruster S04 | 推进器 S04 | - | - | 姿控/侧推 | 随舰体 |
| Thruster S05 | 推进器 S05 | - | - | 姿控/侧推 | 随舰体 |
| Thruster S06 | 推进器 S06 | - | - | 姿控/侧推 | 随舰体 |
| Thruster S07 | 推进器 S07 | - | - | 姿控/侧推 | 随舰体 |
| Thruster S08 | 推进器 S08 | - | - | 姿控/侧推 | 随舰体 |
| Thruster S09 | 推进器 S09 | - | - | 姿控/侧推 | 随舰体 |
| Thruster S10 | 推进器 S10 | - | - | 姿控/侧推 | 随舰体 |
| TL Radar Panel | 左上雷达面板 | - | - | 雷达 | 随舰体 |
| Top Radar | 上方雷达 | - | - | 雷达 | 随舰体 |
| TR Radar Panel | 右上雷达面板 | - | - | 雷达 | 随舰体 |

## 舰载机部件（42 条）

| English | 中文 | 短名 | 短名中文 | 类别 | 阵营 |
|---|---|---|---|---|---|
| 100mm Gun Pods | 100mm 机炮荚舱 | - | - | 荚舱 | 通用（未单列） |
| 15mm Coilgun | 15mm 磁轨炮 | - | - | 磁轨炮 | 通用（未单列） |
| 20mm Gun | 20mm 机炮 | - | - | 机炮 | 通用（未单列） |
| 35mm Gun | 35mm 机炮 | - | - | 机炮 | 通用（未单列） |
| 35mm Gun Pods | 35mm 机炮荚舱 | - | - | 荚舱 | 通用（未单列） |
| Ablative Foam | 烧蚀泡沫 | - | - | 舰载机 | 通用（未单列） |
| Articulated Nozzles | 铰接式喷嘴 | - | - | 舰载机 | 通用（未单列） |
| Braced Frame | 支撑型骨架 | - | - | 舰载机 | 通用（未单列） |
| Centerline Fuel Tank | 中线油箱 | - | - | 舰载机 | 通用（未单列） |
| Ceramic Tiling | 陶瓷装甲板 | - | - | 舰载机 | 通用（未单列） |
| Dome Radar | 穹顶雷达 | - | - | 舰载机 | 通用（未单列） |
| ELINT Sensor | 电子情报传感器 | - | - | 舰载机 | 通用（未单列） |
| EO Targeting Ball | 光电标定球 | - | - | 舰载机 | 通用（未单列） |
| Ferryman Masquerade | 小艇欺骗模块（伪装成渡船 / 官方机翻「船夫化装舞会」） | - | - | 舰载机 | 通用（未单列） |
| Fuel Tanks | 油箱 | - | - | 舰载机 | 通用（未单列） |
| Helmet-Mounted Display | 头盔显示器 | - | - | 舰载机 | 通用（未单列） |
| High-Capacity CM Launcher | 高容量反制发射器 | - | - | 舰载机 | 通用（未单列） |
| High-Coherence CM Launcher | 高连贯反制发射器 | - | - | 舰载机 | 通用（未单列） |
| Illuminator Pods | 照明荚舱 | - | - | 荚舱 | 通用（未单列） |
| Jamming Pods | 干扰荚舱 | - | - | 荚舱 | 通用（未单列） |
| Missile Control Computer | 导弹控制电脑 | - | - | 导弹 | 通用（未单列） |
| Missile Decoy Projector | 导弹诱饵发射器 | - | - | 导弹 | 通用（未单列） |
| Nose Illuminator | 机鼻照明雷达 | - | - | 舰载机 | 通用（未单列） |
| Nose Radar | 机鼻雷达 | - | - | 舰载机 | 通用（未单列） |
| Puck Radar (Advanced) | 圆盘雷达（进阶） | - | - | 舰载机 | 通用（未单列） |
| Puck Radar (Basic) | 圆盘雷达（基础） | - | - | 舰载机 | 通用（未单列） |
| R-1 Rocket Pods | R-1 火箭荚舱 | - | - | 荚舱 | 通用（未单列） |
| S1 Missile Bays | S1 导弹舱 | - | - | 导弹 | 通用（未单列） |
| S1 Outboard Pylons | S1 外侧挂架 | - | - | 舰载机 | 通用（未单列） |
| S1 Overwing Pylons | S1 翼上挂架 | - | - | 舰载机 | 通用（未单列） |
| S1 Underwing Pylons | S1 翼下挂架 | - | - | 舰载机 | 通用（未单列） |
| S2 Missile Bay | S2 导弹舱 | - | - | 导弹 | 通用（未单列） |
| S2 Missile Pylons | S2 导弹挂架 | - | - | 导弹 | 通用（未单列） |
| S2 Overwing Pylons | S2 翼上挂架 | - | - | 舰载机 | 通用（未单列） |
| S2 Underwing Pylons | S2 翼下挂架 | - | - | 舰载机 | 通用（未单列） |
| S3 Missile Bay | S3 导弹舱 | - | - | 导弹 | 通用（未单列） |
| S3 Missile Pylons | S3 导弹挂架 | - | - | 导弹 | 通用（未单列） |
| Shrouded Exhaust | 遮蔽式排气口 | - | - | 舰载机 | 通用（未单列） |
| Sprinter Masquerade | 冲刺化装舞会 | - | - | 舰载机 | 通用（未单列） |
| Standard CM Launcher | 标准反制发射器 | - | - | 舰载机 | 通用（未单列） |
| Stealth Coating | 隐形涂层 | - | - | 舰载机 | 通用（未单列） |
| Wake Sensor | 尾流传感器 | - | - | 舰载机 | 通用（未单列） |

## 弹药（41 条：口径 / 伤害 / 穿深 / 每点发数 / 单发体积 / 阵营）

每点发数 = 官方 `Cost (pts per X amount)=1/N` 里的 N；单发体积取自游戏资源（`munition_storage.json`），装弹上限用 `弹库容量(m³) ÷ 单发体积` 算。

| English | 中文 | 口径 | 伤害 | 穿深 (cm) | 每点发数 | 单发体积 | 阵营 |
|---|---|---|---|---|---|---|---|
| 100mm AP Shell | 100mm 穿甲弹 | 100mm | 25 | 45 | 250 发/点 | 0.05 m³ | OSP |
| 100mm Grape | 100mm 葡萄弹 | 100mm | 25 | 16 | 250 发/点 | 0.05 m³ | OSP |
| 100mm HE Shell | 100mm 高爆弹 | 100mm | 45 | 30 | 250 发/点 | 0.05 m³ | OSP |
| 100mm HE-HC Shell | 100mm 高爆高能弹 | 100mm | 70 | 8 | 250 发/点 | 0.05 m³ | OSP |
| 120mm AP Shell | 120mm 穿甲弹 | 120mm | 30 | 45 | 100 发/点 | 0.05 m³ | 通用 |
| 120mm HE Shell | 120mm 高爆弹 | 120mm | 50 | 30 | 100 发/点 | 0.05 m³ | 通用 |
| 120mm HE-RPF Shell | 120mm 高爆近炸弹 | 120mm | 64/8 | 10 | 100 发/点 | 0.05 m³ | SA |
| 15mm Sandshot | 15mm 沙弹 | 15mm | 75 | 0.275 | 50 发/点 | 0.0025 m³ | 通用 |
| 20mm Slug | 20mm 独头弹 | 20mm | 15 | 0.3 | 2000 发/点 | 0.0025 m³ | 通用 |
| 250mm AP Shell | 250mm 穿甲弹 | 250mm | 70 | 60 | 50 发/点 | 0.15 m³ | 通用 |
| 250mm Bomb Shell | 250mm 炸药弹 | - | - | - | - | 0.15 m³ | OSP |
| 250mm Flak Shell | 250mm 高射炮弹 | - | - | - | - | 0.15 m³ | OSP |
| 250mm HE Shell | 250mm 高爆弹 | 250mm | 80 | 40 | 50 发/点 | 0.15 m³ | 通用 |
| 250mm HE-RPF Shell | 250mm 高爆近炸弹 | 250mm | 128/8 | 20 | 50 发/点 | 0.15 m³ | SA |
| 300mm AP Rail Sabot | 300mm 磁轨穿甲弹 | 300mm | 80 | 200 | 25 发/点 | 0.75 m³ | 通用 |
| 35mm Flechette | 35mm 飞镖弹 | 35mm | 15 | 0.1 | 250 发/点 | 0.005 m³ | OSP |
| 35mm Slug | 35mm 独头弹 | 35mm | 15 | 4 | 1000 发/点 | 0.005 m³ | 通用 |
| 400mm Plasma Ampoule | 400mm 电浆安瓶 | 400mm | 60 | 60 | 25 发/点 | 0.8 m³ | OSP |
| 450mm AP Shell | 450mm 穿甲弹 | 450mm | 100 | 120 | 25 发/点 | 0.8 m³ | 通用 |
| 450mm HE Shell | 450mm 高爆弹 | 450mm | 150 | 65 | 25 发/点 | 0.8 m³ | 通用 |
| 500mm Fracturing Block | 500mm 碎片块 | 500mm | 300/20 | 120 | 25 发/点 | 0.75 m³ | OSP |
| 500mm Fragmentation Block | 500mm 破片块 | - | - | - | - | 0.75 m³ | OSP |
| 50mm Flak Shell | 50mm 高射炮弹 | 50mm | 15 | 0.176 | 75 发/点 | 0.01 m³ | 通用 |
| 600mm Bomb Shell | 600mm 炸药弹 | 600mm | 480 per target/12 | 40 | 25 发/点 | 0.8 m³ | OSP |
| 600mm HE-SH Shell | 600mm 黏着弹 | 600mm | 420/7 | 85 | 25 发/点 | 0.8 m³ | OSP |
| CBU-40 Cluster Bomb | CBU-40 集束炸弹 | - | - | - | - | - | 通用 |
| CM-4D1 Decoy Container (Clipper) | CM-4D1 诱饵容器（飞剪舰） | - | - | - | - | - | 通用 |
| CM-4D2 Decoy Container (Line Ship) | CM-4D2 诱饵容器（战列舰） | - | - | - | - | - | 通用 |
| EA12 Chaff Decoy | EA12 干扰丝诱饵 | - | - | - | - | - | 通用 |
| EA14 Chaff Decoy | EA14 干扰丝诱饵 | - | - | - | - | - | 通用 |
| EA20 Flare Decoy | EA20 热焰弹诱饵 | - | - | - | - | - | 通用 |
| EA99 'Conure' Active Decoy | EA99「太阳鹦鹉」主动式诱饵 | - | - | - | - | - | 通用 |
| FBU-15 Fragmentation Bomb | FBU-15 破片炸弹 | - | - | - | - | - | 通用 |
| KBU-15 Bomb | KBU-15 炸弹 | - | - | - | - | - | 通用 |
| KBU-22 Bomb | KBU-22 炸弹 | - | - | - | - | - | 通用 |
| M-30 'Mattock' Mine | M-30「锄头」空雷 | - | - | - | - | - | 通用 |
| M-30-N 'Mattock' Cooperative Mine | M-30-N「锄头」联合空雷 | - | - | - | - | - | 通用 |
| M-50 'Auger' Sprint Mine | M-50「螺旋钻」冲刺水雷 | - | - | - | - | - | 通用 |
| R-1 'Perch' Rocket | R-1「鲈鱼」火箭 | - | - | - | - | - | 通用 |
| R-2 'Piranha' Rocket | R-2「食人鱼」火箭 | - | - | - | - | - | 通用 |
| R-3 'Spearfish' Rocket | R-3 「旗鱼」火箭 | - | - | - | - | - | 通用 |

## 导弹部件（37 条）

| English | 中文 | 短名 | 短名中文 | 类别 | 阵营 |
|---|---|---|---|---|---|
| Blast Fragmentation | 爆炸破片 | - | - | 战斗部 | 通用 |
| Blast Fragmentation EL | 爆炸破片 EL | - | - | 战斗部 | 通用 |
| Boosted Self-Screening Jammer | 强化型自卫干扰器 | - | - | 辅助 | 通用 |
| Cluster Decoy Launcher | 诱饵群发射器 | - | - | 辅助 | 通用 |
| CM-4 Engine | CM-4 引擎 | - | - | 引擎 | 通用 |
| Cold Gas Bottle | 冷空气罐 | - | - | 辅助 | 通用 |
| Command Receiver | 指令接收机 | - | - | 航电 | 通用 |
| Cruise Guidance | 巡航导引 | - | - | 引擎 | 通用 |
| Decoy Launcher | 诱饵发射器 | - | - | 辅助 | 通用 |
| Direct Guidance | 直接导引 | - | - | 航电 | 通用 |
| Electro-Optical Seeker | 光电寻标器 | - | - | 引导头 | SA 专属 |
| Fast Startup Module | 快速启动模块 | - | - | 辅助 | 通用 |
| Fixed Active Radar Seeker | 固定式主动雷达寻标器 | - | - | 引导头 | 通用 |
| Fixed Anti-Radiation Seeker | 固定式反辐射寻标器 | - | - | 引导头 | 通用 |
| Fixed Semi-Active Radar Seeker | 固定式半主动雷达寻标器 | - | - | 引导头 | 通用 |
| Hardened Skin | 硬化表面 | - | - | 辅助 | 通用 |
| HE Impact | 高爆撞击 | - | - | 战斗部 | 通用 |
| HE Kinetic Penetrator | 高爆动能穿透 | - | - | 战斗部 | SA 专属 |
| Kinetic Kill Mass | 动能击杀块 | - | - | 战斗部 | 通用 |
| Radar Absorbent Coating | 雷达吸波涂层 | - | - | 辅助 | 通用 |
| SDM-1 Booster Engine | SDM-1 加力引擎 | - | - | 引擎 | 通用 |
| SDM-1 Main Engine | SDM-1 主引擎 | - | - | 引擎 | 通用 |
| SDM-2 Booster Engine | SDM-2 加力引擎 | - | - | 引擎 | 通用 |
| SDM-2 Main Engine | SDM-2 主引擎 | - | - | 引擎 | 通用 |
| Self-Screening Jammer | 自卫干扰器 | - | - | 辅助 | 通用 |
| SGM-1 Engine | SGM-1 引擎 | - | - | 引擎 | 通用 |
| SGM-2 Engine | SGM-2 引擎 | - | - | 引擎 | 通用 |
| SGM-H-2 Cruise Engine | SGM-H-2 巡航引擎 | - | - | 引擎 | 通用 |
| SGM-H-2 Sprint Engine | SGM-H-2 冲刺引擎 | - | - | 引擎 | 通用 |
| SGM-H-3 Cruise Engine | SGM-H-3 巡航引擎 | - | - | 引擎 | 通用 |
| SGM-H-3 Sprint Engine | SGM-H-3 冲刺引擎 | - | - | 引擎 | 通用 |
| SGT-3 Engine | SGT-3 引擎 | - | - | 引擎 | 通用 |
| Steerable Active Radar Seeker | 可转向主动雷达寻标器 | - | - | 引导头 | 通用 |
| Steerable Extended Active Radar Seeker | 可转向增程主动雷达寻标器 | - | - | 引导头 | 通用 |
| Submunition Dispenser | 次弹药发射器 | - | - | 战斗部 | 通用 |
| Wake-Homing Seeker | 尾流归向寻标器 | - | - | 引导头 | 通用 |
| Wake-Thermal Seeker | 尾流热源寻标器 | - | - | 引导头 | 通用 |

## 其它（导弹型号 / 舰载机 / 减益 / 阵营名称，34 条）

`_DESC` 结尾的说明文字已过滤（太长，不适合当术语；它们本来就在知识库里）。

| English | 中文 | key |
|---|---|---|
| Ammunition Loader Jammed | 装弹机卡死 | DEBUFFNAME_AMMUNITION_LOADER_JAMMED |
| Antenna Bent | 天线弯曲 | DEBUFFNAME_ANTENNA_BENT |
| Atmosphere Leak | 空气泄漏 | DEBUFFNAME_ATMOSPHERE_LEAK |
| Bearing Surface Bent | 承载面弯曲 | DEBUFFNAME_BEARING_SURFACE_BENT |
| Cell Cookoff | 单元过热引爆 | DEBUFFNAME_CELL_COOKOFF |
| Container Bank Cookoff | 货柜舱过热引爆 | DEBUFFNAME_CONTAINER_BANK_COOKOFF |
| FC Waveguide Bent | 火控波导弯曲 | DEBUFFNAME_FC_WAVEGUIDE_BENT |
| Fire | 火灾（船体着火减益） | DEBUFFNAME_FIRE |
| Focusing Element Misaligned | 聚焦元件未校正 | DEBUFFNAME_FOCUSING_ELEMENT_MISALIGNED |
| Fuel Line Fire | 燃料管线火灾 | DEBUFFNAME_FUEL_LINE_FIRE |
| Gyroscope Drift | 陀螺仪偏离 | DEBUFFNAME_GYROSCOPE_DRIFT |
| Heatsink Ruptured | 散热器破裂 | DEBUFFNAME_HEATSINK_RUPTURED |
| Magazine Cookoff | 弹舱过热引爆 | DEBUFFNAME_MAGAZINE_COOKOFF |
| Main Bus Short | 主汇流排短路 | DEBUFFNAME_MAIN_BUS_SHORT |
| Reactor Overload | 反应堆超载 | DEBUFFNAME_REACTOR_OVERLOAD |
| Civilian Ships | 平民船舰 | FACTIONNAME_CIVILIAN_SHIPS |
| Outlying Systems Protectorate | 致远星系保护领 | FACTIONNAME_OUTLYING_SYSTEMS_PROTECTORATE |
| Shelter Alliance | 庇护同盟 | FACTIONNAME_SHELTER_ALLIANCE |
| Container Torpedo | 货柜鱼雷 | MISSILE_CLASS_CONTAINER_TORPEDO |
| Size 1 Hybrid Missile | 尺寸 1 混合导弹 | MISSILE_CLASS_SIZE_1_HYBRID_MISSILE |
| Size 1 Missile | 尺寸 1 导弹 | MISSILE_CLASS_SIZE_1_MISSILE |
| Size 2 Hybrid Missile | 尺寸 2 混合导弹 | MISSILE_CLASS_SIZE_2_HYBRID_MISSILE |
| Size 2 Missile | 尺寸 2 导弹 | MISSILE_CLASS_SIZE_2_MISSILE |
| Size 3 Hybrid Missile | 尺寸 3 混合导弹 | MISSILE_CLASS_SIZE_3_HYBRID_MISSILE |
| Size 3 Missile | 尺寸 3 导弹 | MISSILE_CLASS_SIZE_3_MISSILE |
| Size 3 Torpedo | 尺寸 3 鱼雷（官方误作“导弹”） | MISSILE_CLASS_SIZE_3_TORPEDO |
| nimble general-purpose missile | 灵敏型通用导弹 | MISSILE_FUNCDEC_BALESTRA |
| heavy anti-ship torpedo | 重型反舰鱼雷 | MISSILE_FUNCDESC_CONTAINER |
| heavy support torpedo | 重型支援鱼雷 | MISSILE_FUNCDESC_CONTAINERSUP |
| flexible defensive missile with a booster | 灵活型防御导弹（搭载加力段） | MISSILE_FUNCDESC_LUNGE |
| heavy anti-ship torpedo | 重型反舰鱼雷 | MISSILE_FUNCDESC_PILUM |
| nimble space-superiority missile | 灵敏型空优导弹 | MISSILE_FUNCDESC_REMISE |
| flexible mainstay anti-ship missile | 灵活型主力反舰导弹（搭载加力段） | MISSILE_FUNCDESC_TEMPEST |
| flexible defensive missile with a booster | 灵活型防御导弹（搭载加力段） | MISSILE_FUNCDESC_TYPHOON |

## 装甲与伤害术语

| 术语 | 中文 | 含义 / 公式 |
|---|---|---|
| Armour / Armor Thickness | 装甲厚度 | 整船一个值（cm），不分艏侧艉；来源 `hull_armour.json` |
| Effective Armor | 等效装甲 | `Clamp(装甲 / cos(入射角), 0, 装甲×2.5)`，角度越大越厚 |
| Ricochet | 跳弹 | `等效装甲×2 ≥ 伤害 且 入射角 ≥ 80°`，只造成 20% 伤害 |
| Penetration | 穿深 | 弹药字段（cm），`伤害 ≥ 等效装甲×剩余结构比例` 才击穿 |
| Over-penetration | 过穿 | 穿深用完前穿出船体，内部伤害按剩余穿深折算 |
| Interior travel / Density | 内部行程 / 内部密度 | `剩余穿深 = 剩余穿深 / 内部密度`，每 cm 消耗对应穿深 |
| DR (Damage Reduction) | 减伤 | 部件减伤，槽位填充率 20%–60% 之间线性变化，最高 90% |
| DT (Damage Threshold) | 伤害阈值 | 单发伤害 ≤ DT 打不掉这个部件 |
| Reinforced | 加固 | DR 下限 ×0.25 与 Catastrophic 概率相关，具体见 wiki |
| Structure break | 结构断裂 | 命中 < 20 伤害的炮击不计入结构损伤 |

## 弹库与装载术语

| 术语 | 中文 | 含义 |
|---|---|---|
| Magazine | 弹库 | 按**体积**存炮弹：`容量(m³) = 每格容量 × 格数`；Reinforced 10 / Bulk 15 / Citadel 3.33 |
| Citadel Magazine | 要塞弹库 | OSP 专属，占 1x3x1×N 格，**槽位至少 6x3x8**，10 m³/格 |
| VLS / CLS | 垂发 / 冷发射 | 按**格数**存导弹：每个 cell 一发，尺寸受发射器限制 |
| MLS / SALS | 导弹弹库 / 软发射 | 导弹也按体积存在弹库里，由 Launcher 装填 |
| Arming missile | 武装弹 | 1 点 1 发的 S1 进攻导弹（SGM-114 Wuffer 是现成模板） |
| Storage Volume | 单发体积 | 炮弹 0.0025–0.8 m³；导弹 S1 4 / S2 20 / S3 30 m³ |
| Rounds per point | 每点发数 | 官方 `1/N`：450mm AP 1/25 = 25 发/点 |

## 编成与配合术语

| 术语 | 中文 | 含义 |
|---|---|---|
| Remote track | 遥测航迹 | 靠友军传感器共享的航迹，自己看不到也能打 |
| Lock / Fire control | 锁定 / 火控 | 一艘船同时锁定的目标数受 CIC 限制 |
| Comms jamming | 通信干扰 | 让共享航迹断链：`d ≈ d_A·√(K/P_A·G_A)`，CR75 能把距离压到一半 |
| Hard kill / Soft kill | 硬杀 / 软杀 | 打掉船体 vs 打掉导弹/传感器/航迹 |
| Tank / Anchor | 抗线 / 锚点 | 前排吃伤害的船 |
| Flank / Pincer | 绕侧 / 夹击 | 从侧翼或两面包夹 |

## 玩家口语 → 官方英文（376 条，来自 `query_terms.py`）

这一列是**检索用的映射**，不是官方译名：左边是玩家会说/会打的中文，右边是知识库文档里实际用的英文词。

| 中文口语 | 映射到的英文 |
|---|---|
| 贪 | greed underpriced |
| 贪婪 | greed underpriced |
| 乞丐 | greed underpriced |
| 贪污 | greed underpriced |
| 省钱 | greed underpriced cheap |
| 廉价 | greed underpriced cheap |
| 堆料 | overpriced over-equipped |
| 装备过剩 | overpriced over-equipped |
| 超配 | overpriced over-equipped |
| 价格 | cost point cost band |
| 点数 | cost point cost |
| greed | greed underpriced |
| shell | shell greed underpriced |
| 口径 | caliber caliber mm |
| 12k | 12000 points large fleet mod No Ship Limits |
| 6k | 6000 points large fleet mod |
| 供电不足 | power budget deficit n-1 shutdown |
| 电力不够 | power deficit |
| 超载 | overload power |
| 关掉雷达 | shutdown radar power budget |
| 供电超了 | power deficit |
| 火炮 | cannon gun |
| 炮 | cannon |
| 型号 | model |
| 有哪几种 | which types models |
| 有几种 | types models |
| 毫米炮 | mm cannon |
| 挂载位 | socket mount socket map |
| 挂载点 | socket mount |
| 槽位 | socket mount |
| 插槽 | socket |
| 几号位 | mount index |
| 几号槽 | mount index |
| 号挂载位 | mount |
| 舱室 | compartment |
| 指挥舱 | command compartment |
| 损管舱 | damage control compartment |
| 机库 | hangar |
| 模块 | module |
| 挂载 | mount |
| 武器位 | mount |
| 内置部件 | integrated component |
| 导弹发射器 | missile launcher |
| 发射器 | launcher |
| 垂直发射 | vertical launch |
| 鱼雷发射器 | cls-3 launcher torpedo |
| cls | cls launcher |
| cls3 | cls-3 launcher |
| tls | tls launcher |
| 禁用 | avoid banned |
| 被禁 | avoid banned |
| 近防 | point defense |
| 点防御 | point defense |
| 轴炮 | spinal weapon |
| 脊髓炮 | spinal mount Spinal weapons railgun |
| 主轴炮 | spinal mount Spinal weapons |
| 雷达 | radar |
| 传感器 | sensor |
| 电子战 | electronic warfare |
| 干扰 | jamming |
| 干扰器 | jammer required power |
| 开干扰 | jammer active power |
| 短接 | battleshort |
| 战斗短接 | battleshort BSHRT |
| 耗电 | required power |
| 诱饵 | decoy |
| 反应堆 | reactor |
| 动力装置 | powerplant |
| 发动机 | drive |
| 推进器 | propulsion |
| 装甲 | armor |
| 穿深 | penetration |
| 穿透 | penetration |
| 船体 | hull |
| 巡洋舰 | cruiser |
| 驱逐舰 | destroyer |
| 护卫舰 | frigate |
| 战列舰 | battleship |
| 航母 | carrier |
| 航空母舰 | carrier |
| 补给舰 | logistics ship |
| 布雷舰 | minelayer |
| 舰载机 | spacecraft craft |
| 战机 | craft fighter |
| 无人机 | drone |
| 弹药 | munition ammunition |
| 导弹 | missile |
| 炮弹 | shell |
| 穿甲弹 | AP shell |
| 高爆弹 | HE shell |
| 破片 | flechette |
| 引信 | fuze |
| 导引头 | seeker |
| 战斗部 | payload |
| 弹体 | missile body |
| 水雷 | mine |
| 炸弹 | bomb |
| 火箭 | rocket |
| 点防炮塔 | point defense turret |
| 炮塔 | turret |
| 磁轨 | mass driver |
| 粒子束 | particle beam |
| 等离子 | plasma |
| 箔条 | chaff |
| 热焰弹 | flare |
| 编程通道 | programming channel |
| 扬弹机 | ammunition elevator elevator |
| 炮术指挥中心 | gun plot center |
| 情报中心 | intel compartment |
| 战斗情报中心 | combat information center |
| 雷达接收机 | radar receiver |
| 粒子加速器 | particle accelerator |
| 软杀 | soft kill |
| 满套软杀 | 满套软杀 成对互补 greedford 双舰 干扰 箔条 照明弹 |
| 软杀组合 | 软杀组合 成对互补 两艘船分工 满套软杀 |
| 互补 | 成对互补 两艘船分工 |
| 成对 | 成对互补 两艘船分工 |
| 造舰技巧 | 造舰技巧 分步流程 自检清单 softkill pair |
| 分步流程 | 分步流程 造舰技巧 步骤 检查点 |
| 造舰流程 | 造舰流程 步骤 检查点 自检清单 |
| 硬杀 | hard kill |
| 主引导头 | primary seeker |
| 副引导头 | secondary seeker |
| 验证头 | verification seeker |
| 烧穿 | burnthrough sweep |
| 航迹 | track |
| 锁定 | lock on |
| 交战距离 | engagement range |
| 集火 | focus fire |
| 抢点 | capture point |
| 据点 | capture point unarmed |
| 占点 | capture point unarmed contested |
| 无武装舰 | unarmed capture point |
| 无武装船 | unarmed capture point |
| 无武装 | unarmed |
| 无人舰 | unarmed weaponless ship |
| 舰段 | hull section segment |
| 挂载限制 | socket size limit mount fit |
| 装不下 | does not fit socket size |
| 能不能装 | can it fit socket size faction |
| 尺寸 | dimensions size socket |
| 阵营限制 | faction restriction exclusive |
| 混装 | mixed faction components |
| 跨阵营 | cross faction components both sides |
| 对面阵营 | opposite faction parts |
| 两家部件 | both factions components |
| CC特权 | CC Ocello mixed faction privilege |
| 特权 | privilege exception perk |
| 杂交 | hybrid hull section combination |
| LN杂交 | LN hybrid hull section |
| 舰桥 | bridge secondary structure |
| 朝向 | facing mount direction |
| 炮塔朝向 | turret facing mount direction |
| 拆舰桥 | remove bridge |
| 无人船 | unarmed weaponless ship |
| 争夺 | contested capture |
| 判负 | lose unarmed |
| 绕侧 | flank |
| 抗线 | hold the line |
| 拖船 | tugboat |
| 箱船 | container liner |
| 集装箱船 | container liner |
| 长船 | line ship |
| 指挥巡洋舰 | command cruiser |
| 导弹船 | missile line ship |
| 缩写 | abbreviation glossary |
| MMT | multi mission tug |
| 拦截机 | interceptor craft |
| 轰炸机 | bomber craft |
| 轴炮 | spinal weapon spinal mount |
| 地图 | map maps |
| 这张图 | map |
| 多大 | map size |
| 几发 | capacity cells minimum |
| 弹位 | capacity cells minimum |
| 装几发 | capacity cells minimum |
| 载弹 | capacity cells minimum |
| 弹药基数 | capacity cells minimum |
| 发射器 | launcher |
| 垂发 | VLS vertical launch system |
| 名字 | naming differences wiki in-game name |
| 名称 | naming differences wiki in-game name |
| 叫法 | naming differences in-game name |
| 改名 | renamed naming differences |
| 对不上 | naming differences |
| 不一致 | naming differences |
| 冲突 | naming differences |
| 差异 | naming differences |
| 换过名 | renamed |
| 部件 | part |
| 组件 | part |
| 阵营 | faction |
| 势力 | faction |
| 哪边 | faction |
| 专属 | exclusive only |
| 特有 | exclusive only |
| 独有 | exclusive only |
| 只有 | exclusive only |
| 通用 | both factions unrestricted |
| 共用 | both factions unrestricted |
| 民用 | civilian |
| 军用 | military |
| 雷达模块 | radar module |
| 动力模块 | powerplant module |
| 推进模块 | propulsion module |
| 武器支援模块 | weapon support module |
| 发动机模块 | propulsion drive module |
| 损管模块 | damage control module |
| 导弹发射器 | missile launcher vertical launch system |
| 有哪几种 | list of all entries |
| 有哪些 | list of all entries |
| 点数 | point cost cost |
| 质量 | mass tonnes |
| 结构值 | hitpoints |
| 伤害阈值 | damage threshold |
| 射程 | range |
| 射速 | rate of fire |
| 供电 | power |
| 功率 | power kW |
| 信号 | radar signature |
| 信号半径 | signature radius |
| 乘员 | crew |
| 损管 | damage control |
| 维修 | repair |
| 维修上限 | max repair |
| 载弹 | magazine capacity |
| 弹舱 | magazine |
| 有哪些船 | hull class |
| 哪些船 | hull class |
| 船体 | hull |
| 舰体 | hull |
| 造舰 | ship building SOP procedure |
| 配船 | ship building SOP loadout |
| 铁律 | SOP rule priority copy paste |
| 三条铁律 | SOP rule priority copy paste |
| 优先级 | priority rule copy paste edit from scratch |
| 先抄 | copy paste template first |
| 从零 | from scratch build |
| 默认点数 | default 3000 points budget |
| 点数默认 | default 3000 points budget |
| 没有点数 | no point limit default 3000 |
| 怎么造 | how to build procedure |
| 流程 | SOP procedure steps |
| 插槽 | hull socket mounting size |
| 槽位 | hull socket mounting size |
| 挂载点 | mounting socket |
| 射界 | traversal firing arc |
| 固定安装 | fixed mount no traverse |
| 朝哪 | firing arc direction |
| 装得下 | socket fit size |
| 能不能装 | socket fit size |
| 装多大 | socket fit size |
| 哪个槽 | which socket |
| 哪艘 | which hull |
| 艘 | hull |
| 最贵 | most expensive point cost |
| 最便宜 | cheapest point cost |
| 便宜 | cheap point cost |
| 贵 | expensive point cost |
| 排序 | sorted by |
| 导弹模板 | missile template |
| 弹药模板 | missile template |
| 模板 | template |
| 配船 | build order copy template |
| 怎么配 | build order copy template |
| 配一艘 | build one ship template |
| 配一支 | build a fleet template |
| 怎么做 | how to build |
| 从零 | build from scratch |
| 抄模板 | copy template rename |
| 复制 | copy template |
| 改名 | rename |
| 导弹配置 | missile template loadout |
| S3F | SGM-3 body size 3 |
| S3 | SGT-3 body size 3 |
| 导引头 | seeker |
| 验证头 | validator seeker |
| 制导包 | avionics guidance package |
| 载荷 | payload warhead |
| 弹体 | missile body |
| 发动机 | engine |
| 基线 | baseline all ships |
| 通用要求 | baseline all ships |
| 通用基线 | baseline all ships |
| 硬性要求 | baseline must |
| 必须满足 | baseline must |
| 合格 | baseline legal build |
| 不合规 | baseline legal build |
| 线列舰 | line ship |
| 线列 | line ship |
| 战列舰 | battleship |
| 炮舰 | monitor |
| 飞剪舰 | clipper |
| 轻型护卫舰 | corvette |
| 护卫航母 | escort carrier |
| 舰队航母 | fleet carrier |
| 轻型航母 | light carrier |
| 补给舰 | replenishment oiler |
| 闪退 | fleet file structure validation |
| 崩溃 | fleet file structure validation |
| 打不开 | fleet file structure validation |
| 加载不了 | fleet file structure validation |
| 读档 | fleet file structure validation |
| 校验 | validation |
| 合法性 | valid fleet |
| 合法 | valid fleet |
| 坏档 | fleet file structure validation |
| 结构 | structure |
| 舰体配置 | hull configuration |
| 舰段 | hull section |
| 舰桥 | bridge superstructure |
| 从零 | from scratch build fleet file |
| 造一支 | build fleet file |
| 造一个 | build fleet file |
| 建一支 | build fleet file |
| 组一支 | build fleet file |
| 新建舰队 | build fleet file |
| 生成舰队 | generate fleet file |
| 炮艇 | gunboat corvette |
| 十艘 | count ships fleet |
| 太大 | component too large socket fit |
| 装不下 | component too large socket fit |
| 尺寸不符 | socket size fit |
| 类型不符 | socket type mismatch |
| 少了部件 | socket component silently dropped |
| 留空 | socket left empty |
| 静默 | silently dropped socket |
| 装多少发 | storage capacity magazine quantity |
| 能装几发 | storage capacity magazine quantity |
| 装几发 | storage capacity magazine quantity |
| 载弹量 | storage capacity magazine |
| 弹药量 | storage capacity magazine |
| 弹库容量 | magazine storage capacity |
| 怎么装弹 | how to load ammunition magazine |
| 装填 | load ammunition |
| 空弹 | empty ammunition load |
| 弹药点数 | ammo point cost per round |
| 弹库点数 | magazine point cost first free |
| 每发 | cost per round ammo points |
| 一发 | cost per round ammo points |
| 装填成本 | ammo points loading cost |
| 弹药成本 | ammo point cost per round |
| 组队 | fleet composition role |
| 编队 | fleet composition role |
| 编成 | fleet composition role |
| 搭配 | composition synergy role mix |
| 协同 | fleet synergy coordination |
| 阵容 | fleet composition |
| 舰队怎么组 | how to compose a fleet |
| 火控共享 | shared tracks fire control |
| 视野共享 | shared tracks vision |
| 通信干扰 | communication jamming data link |
| 克制 | counter pick |
| 槽位 | socket layout common part |
| 挂载位 | socket layout common part |
| 常见配置 | common layout sample build |
| 常用部件 | most used part socket |
| 配对槽位 | mirrored socket pair |
| 左右对称 | mirrored socket pair |
| 照抄 | copy sample build |
| 这块装什么 | what fits this socket |
| 射速 | rate of fire rounds per minute |
| 每分钟 | rounds per minute |
| rpm | rounds per minute |
| 炮管数 | barrels per turret |
| 装填时间 | reload time |
| 弹药升降机 | ammunition elevator reload buff |
| 升降机 | ammunition elevator reload buff |
| 武装弹 | arming missile one point |
| 诱饵弹 | decoy chaff flare |
| 干扰弹 | decoy chaff flare |
| 箔条 | chaff decoy |
| 弹种 | shell type choice |
| 穿甲 | AP shell |
| 高爆 | HE shell |
| 用什么弹 | which shell to use |

## 阵营特例：CC 的特权（29 条）

下面这些部件 wiki 标了「专属」，但真实存档里另一家也在用。**wiki 是对的**：`CC`（Ocello Cruiser）的特权是**可以装两家的部件**，所以 OSP 存档里出现 SA 专属件只会发生在 CC 身上，换到非 CC 船体就是非法配装。
配装时按「wiki 声明」执行；只有在配 `CC` 时才允许跨阵营，别把这条特权抄到其它船体上。

| 部件 | wiki 声明 | 存档实测 | 配装规则 |
|---|---|---|---|
| CLS-3 Launcher | SA 专属 | SA 167 / OSP 17（含 CC 跨阵营） | SA 专属（CC 例外） |
| CR10 Antenna | SA 专属 | SA 13 / OSP 25（含 CC 跨阵营） | SA 专属（CC 例外） |
| E55 'Spotlight' Illuminator | SA 专属 | SA 15 / OSP 3（含 CC 跨阵营） | SA 专属（CC 例外） |
| E70 'Interruption' Jammer | SA 专属 | SA 101 / OSP 27（含 CC 跨阵营） | SA 专属（CC 例外） |
| E90 'Blanket' Jammer | SA 专属 | SA 171 / OSP 34（含 CC 跨阵营） | SA 专属（CC 例外） |
| FM230 'Whiplash' Drive | SA 专属 | SA 337 / OSP 5（含 CC 跨阵营） | SA 专属（CC 例外） |
| FM240 'Dragonfly' Drive | SA 专属 | SA 123 / OSP 1（含 CC 跨阵营） | SA 专属（CC 例外） |
| FM500 Drive | SA 专属 | SA 35 / OSP 9（含 CC 跨阵营） | SA 专属（CC 例外） |
| FM530 'Whiplash' Drive | SA 专属 | SA 93 / OSP 29（含 CC 跨阵营） | SA 专属（CC 例外） |
| FM540 'Dragonfly' Drive | SA 专属 | SA 59 / OSP 5（含 CC 跨阵营） | SA 专属（CC 例外） |
| FM580 'Raider' Drive | SA 专属 | SA 53 / OSP 15（含 CC 跨阵营） | SA 专属（CC 例外） |
| FR3300 Micro Reactor | SA 专属 | SA 602 / OSP 48（含 CC 跨阵营） | SA 专属（CC 例外） |
| FR4800 Reactor | SA 专属 | SA 365 / OSP 50（含 CC 跨阵营） | SA 专属（CC 例外） |
| Missile Programming Bus | SA 专属 | SA 97 / OSP 5（含 CC 跨阵营） | SA 专属（CC 例外） |
| Missile Programming Bus Array | SA 专属 | SA 157 / OSP 46（含 CC 跨阵营） | SA 专属（CC 例外） |
| Mk20 'Defender' PDT | SA 专属 | SA 694 / OSP 16（含 CC 跨阵营） | SA 专属（CC 例外） |
| Mk29 'Stonewall' PDT | SA 专属 | SA 155 / OSP 5（含 CC 跨阵营） | SA 专属（CC 例外） |
| Mk65 Cannon | SA 专属 | SA 9 / OSP 4（含 CC 跨阵营） | SA 专属（CC 例外） |
| Mk66 Cannon | SA 专属 | SA 87 / OSP 105（含 CC 跨阵营） | SA 专属（CC 例外） |
| Mk81 Railgun | SA 专属 | SA 6 / OSP 6（含 CC 跨阵营） | SA 专属（CC 例外） |
| Mk90 'Aurora' PDT | SA 专属 | SA 136 / OSP 147（含 CC 跨阵营） | SA 专属（CC 例外） |
| Mk95 'Sarissa' PDT | SA 专属 | SA 76 / OSP 30（含 CC 跨阵营） | SA 专属（CC 例外） |
| RF101 'Bullseye' Radar | SA 专属 | SA 204 / OSP 52（含 CC 跨阵营） | SA 专属（CC 例外） |
| RM50 'Parallax' Radar | SA 专属 | SA 108 / OSP 44（含 CC 跨阵营） | SA 专属（CC 例外） |
| RS35 'Frontline' Radar | SA 专属 | SA 267 / OSP 3（含 CC 跨阵营） | SA 专属（CC 例外） |
| RS41 'Spyglass' Radar | SA 专属 | SA 143 / OSP 9（含 CC 跨阵营） | SA 专属（CC 例外） |
| VLS-1-23 Launcher | SA 专属 | SA 304 / OSP 85（含 CC 跨阵营） | SA 专属（CC 例外） |
| VLS-1-46 Launcher | SA 专属 | SA 170 / OSP 121（含 CC 跨阵营） | SA 专属（CC 例外） |
| VLS-2 Launcher | SA 专属 | SA 144 / OSP 46（含 CC 跨阵营） | SA 专属（CC 例外） |

## 已知缺口

1. **舰船名没有官方中文名**：本地化里只有 `HULL_*_DESC` 长描述，没有 `HULL_*_NAME`，所以舰名只有英文（本表已给出存档键与数据）。
2. `HULLCOMPSHORTNAME` 只有 108 条，比 145 个部件少，缺的那批在“短名”列会显示 `-`。
3. 界面文案 3669 条已单独导出到 `domain/data/ui_terms_zh_en.csv`，没混进这张表。
4. 舰体自带部件（`Main 01`、`Thruster S 03` 之类）是实例名，没有尺寸/点数数据，只能按舰体查。
5. 部件表 143 条（本地化有 145 条）：`CR10 Antenna` / `CR70 Antenna` 各有长短两个名字，已合并成一行。
6. 「建议」列只是存档统计：通用部件也可能只被一家用过（样本偏差），专属部件被另一家用过则优先怀疑 wiki 图标口径。


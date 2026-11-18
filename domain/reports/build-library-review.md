# 构建类型库（草案，未入库）

样本：99 个舰队 / 324 艘船 （`other info\fleets` 新手包 + Steam `Saves\Fleets`）。

> 这份文件只是给你看的草案。**还没有写进 RAG**，等你确认命名和规则之后再入库。

## 1. 识别规则

**类名 = 主武器 + 舰级缩写**，例：`450 CH`、`VLS-2 FFL`、`unarmed CC`（对应你说的 “450 CH”“cap”）。

| 规则 | 取值 |
|---|---|
| 火炮主武器 | 口径 450 / 250 / 120 / 100 / 75 / 50 / 30 / 20（按 wiki `Mounts › Projectile weapons` 口径） |
| 导弹主武器 | 发射器型号：VLS-1-23 / VLS-1-46 / VLS-2 / VLS-3 / MLS-2 / MLS-3 / CLS-3 / SALS-2 / ML-9 … |
| 纯近防 | `P20 'Bastion' PDT`、`P11 'Pavise' PDT` 这类直接写型号 |
| 无武器 | `unarmed` |
| 舰级 | hull_abbr.json（CC/DD/FF/FFL/CH/CL/CVL/CVE/BB/LN/MN…） |
| 标签 | `line`（有 450mm 舰炮）、`cap`（FFL、≤320 点、无 250mm 以上主炮）、`scout`、`softkill`、`air-defence`、`carrier`、`support`、`picket` |

## 2. 构建类型汇总（共 56 类）

| 构建 | 船数 | 舰体 | 实际点数 min / 中位 / max | 舰体点数 | 舰体占比 | 标签 |
|---|---|---|---|---|---|---|
| RL18 Shuttle | 20 | Shuttle×20 | 174 / 189 / 320 | 82 | 43% | - |
| 100 Shuttle | 19 | Shuttle×19 | 146 / 165 / 187 | 82 | 50% | - |
| 100 Bulk | 19 | Bulk Feeder×14、Bulk Hauler×5 | 425 / 435 / 3000 | 206 | 47% | air-defence |
| VLS-2 FFL | 18 | FFL×18 | 391 / 508 / 800 | 75 | 15% | scout、softkill、support |
| 450 CC | 17 | CC×17 | 1299 / 1500 / 1649 | 575 | 38% | air-defence、line、softkill、support |
| 250 FFL | 17 | FFL×17 | 218 / 289 / 350 | 75 | 26% | softkill、scout |
| 120 FFL | 15 | FFL×15 | 185 / 195 / 254 | 75 | 38% | scout、cap、air-defence |
| 600 Bulk | 11 | Bulk Feeder×11 | 570 / 594 / 1097 | 206 | 35% | line、softkill |
| 450 CH | 10 | CH×10 | 1433 / 1534 / 2218 | 600 | 39% | air-defence、line、support、softkill |
| VLS-2 FF | 9 | FF×9 | 536 / 571 / 1050 | 125 | 22% | scout、air-defence |
| unarmed Container | 9 | Container Hauler Refit×9 | 2602 / 3000 / 3000 | 2238 | 75% | carrier |
| CLS-3 DD | 8 | DD×8 | 852 / 855 / 887 | 200 | 23% | air-defence、support |
| 250 CL | 8 | CL×8 | 976 / 1302 / 1387 | 350 | 27% | air-defence、softkill |
| VLS-1-23 Tugboat | 8 | Tugboat×8 | 250 / 255 / 302 | 132 | 52% | - |
| 100 Tugboat | 8 | Tugboat×8 | 249 / 452 / 453 | 132 | 29% | - |
| CLS-3 CL | 8 | CL×8 | 2961 / 3829 / 3829 | 350 | 9% | support |
| VLS-1-46 CVE | 7 | CVE×7 | 1888 / 3000 / 3000 | 500 | 17% | carrier、air-defence |
| 450 Bulk | 7 | Bulk Hauler×7 | 1142 / 1364 / 1384 | 532 | 39% | line、carrier、air-defence、softkill |
| unarmed FFL | 6 | FFL×6 | 215 / 314 / 425 | 75 | 24% | scout、support、softkill、cap |
| VLS-1-46 DD | 6 | DD×6 | 675 / 675 / 675 | 200 | 30% | air-defence |
| VLS-2 CC | 6 | CC×6 | 3000 / 3000 / 3142 | 575 | 19% | air-defence、softkill |
| 450 BB | 6 | BB×6 | 2606 / 2782 / 3000 | 1000 | 36% | air-defence、support、line、softkill |
| VLS-1-46 FFL | 5 | FFL×5 | 144 / 202 / 225 | 75 | 37% | scout、cap |
| 120 DD | 5 | DD×5 | 700 / 727 / 727 | 200 | 28% | support、softkill |
| P20 'Bastion' Bulk | 5 | Bulk Hauler×5 | 600 / 600 / 600 | 532 | 89% | air-defence |
| 300 DD | 4 | DD×4 | 465 / 478 / 490 | 200 | 42% | air-defence |
| VLS-1-23 FFL | 4 | FFL×4 | 201 / 220 / 234 | 75 | 34% | scout、cap |
| 100 Ore | 4 | Ore Carrier×4 | 1252 / 1252 / 1252 | 1065 | 85% | carrier |
| VLS-1-46 Container | 4 | Container Hauler Refit×4 | 3000 / 3000 / 3000 | 2238 | 75% | carrier |
| 120 CH | 4 | CH×4 | 1440 / 1531 / 1600 | 600 | 39% | softkill、line |
| CLS-3 FFL | 4 | FFL×4 | 540 / 574 / 632 | 75 | 13% | support、scout |
| MLS-2 Bulk | 3 | Bulk Feeder×2、Bulk Hauler×1 | 969 / 969 / 2713 | 206 | 21% | - |
| ML-9 'Mine' Shuttle | 3 | Shuttle×3 | 183 / 183 / 216 | 82 | 45% | - |
| 500 Bulk | 3 | Bulk Hauler×3 | 979 / 1049 / 1222 | 532 | 51% | line、air-defence |
| MLS-3 Bulk | 3 | Bulk Hauler×3 | 1499 / 1501 / 3121 | 532 | 35% | air-defence |
| VLS-1-23 Shuttle | 3 | Shuttle×3 | 92 / 136 / 150 | 82 | 60% | - |
| VLS-3 CH | 2 | CH×2 | 3000 / 3000 / 3000 | 600 | 20% | air-defence、softkill |
| 100 Container | 2 | Container Hauler Refit×2 | 3000 / 3000 / 3000 | 2238 | 75% | carrier |
| 400 Bulk | 2 | Bulk Hauler×2 | 1197 / 1197 / 1197 | 532 | 44% | - |
| VLS-1-23 DD | 2 | DD×2 | 704 / 762 / 819 | 200 | 26% | softkill、support、air-defence |
| 300 CC | 2 | CC×2 | 1065 / 1297 / 1529 | 575 | 44% | air-defence |
| Container Bank Container | 2 | Container Hauler×1、Container Hauler Refit×1 | 3000 / 3715 / 4430 | 2819 | 76% | carrier |
| unarmed FF | 2 | FF×2 | 415 / 415 / 415 | 125 | 30% | softkill、scout、support |
| VLS-1-46 Ore | 2 | Ore Carrier×2 | 1493 / 1500 / 1507 | 1065 | 71% | carrier |
| VLS-2 DD | 1 | DD×1 | 835 / 835 / 835 | 200 | 24% | air-defence |
| CLS-3 CC | 1 | CC×1 | 2170 / 2170 / 2170 | 575 | 26% | air-defence、softkill |
| VLS-1-46 Tugboat | 1 | Tugboat×1 | 258 / 258 / 258 | 132 | 51% | - |
| MLS-2 Tugboat | 1 | Tugboat×1 | 348 / 348 / 348 | 132 | 38% | - |
| 250 FF | 1 | FF×1 | 397 / 397 / 397 | 125 | 31% | scout |
| unarmed CVE | 1 | CVE×1 | 1513 / 1513 / 1513 | 500 | 33% | carrier |
| VLS-1-46 Bulk | 1 | Bulk Feeder×1 | 503 / 503 / 503 | 206 | 41% | - |
| P11 'Pavise' Container | 1 | Container Hauler Refit×1 | 3000 / 3000 / 3000 | 2238 | 75% | carrier、air-defence |
| 250 Tugboat | 1 | Tugboat×1 | 344 / 344 / 344 | 132 | 38% | air-defence |
| VLS-2 CH | 1 | CH×1 | 3000 / 3000 / 3000 | 600 | 20% | softkill |
| VLS-1-46 Shuttle | 1 | Shuttle×1 | 232 / 232 / 232 | 82 | 35% | softkill |
| VLS-2 CL | 1 | CL×1 | 2454 / 2454 / 2454 | 350 | 14% | softkill、support |

## 3. 有说明书的舰队：定位 vs 实际构建

只列 使用说明.txt 的舰队（其余是没有说明的测试/存档舰队）。

| 舰队 | 说明里的定位 | 上手难度 | 构成 |
|---|---|---|---|
| 1101 CL | 前排/中程火炮输出 | 中 | 250 CL×3 |
| BB test 52 no ic | 前排/中远程火炮输出 | 高 | 450 BB×1、VLS-1-23 FFL×1 |
| CC 450 Test 4 Newbie | 前排/中远程火炮输出 | 中 | 450 CC×2 |
| CC LN test 1 | 前排/中远程火炮输出 | 高（比战列舰容易，但是有限） | 450 CC×2、450 Bulk×2、VLS-1-23 Tugboat×2 |
| CC LN test 4 450 | 前排/中远程火炮输出 | 高（比战列舰容易，但是有限） | 450 CC×1、450 Bulk×1、VLS-1-46 Shuttle×1 |
| CC ln test 6 | 半前排/中远程火炮输出+半后排火力支援 | 中 | 450 CC×1、500 Bulk×1、VLS-1-23 Tugboat×1 |
| HC Gun Missile test 8 | 半前排/中远程火炮输出+导弹收割 | 高 | 450 CH×1、250 FF×1、unarmed FFL×1 |
| HC Gun test 4 | 前排/中远程火炮输出 | 中 | 450 CH×2 |
| HC Missile test 7 | 后排/巡航导弹 | 中 | VLS-3 CH×1 |
| TF Purple Joy 2 | 前排/中近距离输出 | 中 | 400 Bulk×2、MLS-2 Tugboat×1、VLS-1-23 Tugboat×1 |

## 4. 成本模型

- 逐船预测 = 舰体 + 部件 + 弹药（wiki 单价）：**精确命中 20/324**，中位偏差 30 点；偏低 236 条、偏高 61 条。
- 偏低主因：(a) 游戏内部件单价略高于 wiki 数值，(b) `$MODMIS$` 自制导弹没有模板价格，(c) 自带部件与舱内弹药未计价。
- 民用船体（Shuttle / Bulk Hauler / Tugboat / Container Hauler / Ore Carrier）wiki 里没有点数列，
  现在用 `domain\data\civilian_hull_prices.json` 的**反推估算值**补上（中位 `declared − 部件 − 弹药`）。
- 因此类目表里的“实际点数”以舰队文件里的 `Cost` 为准，预测值只当诊断用。

## 5. 已知问题

1. 匹配不到的部件：Berthing×42、C54 Cannon×20、S2 Bandit Launcher×11、S2 Twin Bandit Launcher×5、Torpedo Turret×1。
2. 民用舰体价格是估算，不是官方数值。
3. wiki 的炮弹价是 `1 / N 点`，会出现 25.75 这种小数，游戏里取整规则未验证。
4. 插件（mod）船没有单独统计；`other info` 里与 Steam 重复的舰队只算一次（按路径去重）。

## 6. 需要你拍板

1. 类名是否就用「主武器 + 舰级」这套（`450 CH` / `VLS-2 FFL` / `unarmed cap`）？要不要把 `cap` 直接写成类名？
2. 新手包的 28 个舰队要不要留在样本里（它们偏教学，不一定是最优解）？
3. 标签够不够用？现在会自动打 `line`（450mm）/ `cap` / `scout` / `softkill` / `air-defence` / `carrier` / `support` / `picket`，
   要不要再加 `logi`（补给）、`sniper`（远程导弹）、`brawler`（近战）这种？
4. 说明里的“舰队定位”我要不要一起解析成结构化字段（前排 / 中远程 / 软杀 / 眼船…）？

## 7. 如果入库，长这样（以 `450 CC` 为例）

```markdown
# 450 CC（450mm 舰炮 / 指挥巡洋舰）
Tags: kind=build class; role=line; hull=CC
Summary: 主武器 450mm ×3；样本 17 艘；实际点数 1299–1649（中位 1500）
## 样本
| 舰队 | 舰名 | 点数 |
|---|---|---|
| Cobalt Squadron | Tungsten Crescendo | 1500 |
| Cobalt Squadron | Titanium Overture | 1500 |
| CC 450 Test 4 Newbie | Aster Crown | 1515 |
## 用法
- 评舰队时：一艘 450 CC 通常吃掉 1300–1650 点预算，占比 4 成是舰体本身。
- 和 450 CH 的区别：CH 是 Axford 重型巡洋舰（600 点舰体、成品中位 1534），CC 是 Ocello（575 点舰体、1500），槽位更多但点数接近。
```


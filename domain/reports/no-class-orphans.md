# 没有舰级的船（`A Cap (Any ship)` 之前）

语料：826 舰（106 舰队，87 舰因已删除部件跳过）。
**没有对应舰级：3 舰** —— 它们在 `Ship Builds.txt` 里不满足任何一类的 must（含点数区间），只能落进 `A Cap (Any ship)` 这条兜底。

按舰体：CC 3

按来源舰队：CC maxxing 3

| # | 船名 | 舰体 | 点数 | 舰队 | 最接近的舰级与差距 |
|---|---|---|---|---|---|
| 1 | Hello | CC | 1201 | CC maxxing | `450 CC`（1400-1600） 差 「have at least 2 450 turrets (mount 1-3)」，且点数 1201 在区间外<br>`S2CC`（2500-3000） 差 「have >1000 points of direct straightrunner offensive missiles」，且点数 1201 在区间外 |
| 2 | Grit and Ark | CC | 1201 | CC maxxing | `450 CC`（1400-1600） 差 「have at least 2 450 turrets (mount 1-3)」，且点数 1201 在区间外<br>`S2CC`（2500-3000） 差 「have >1000 points of direct straightrunner offensive missiles」，且点数 1201 在区间外 |
| 3 | Sharai E. Naamann | CC | 1291 | CC maxxing | `450 CC`（1400-1600） 差 「have at least 2 450 turrets (mount 1-3)」，且点数 1291 在区间外<br>`S2CC`（2500-3000） 差 「have >1000 points of direct straightrunner offensive missiles」，且点数 1291 在区间外 |

## 怎么读

- 「差「…」」= 该舰级 must 里被判定为**不满足**的条目，原样引用 `Ship Builds.txt`。
- 「点数在区间外」= must 都过了，只是点数不在这一类标称的区间内。
- 「无法判定」= 条件依赖 .fleet 里没有的信息（例如火炮朝向、某种弹药数量），脚本不下结论。

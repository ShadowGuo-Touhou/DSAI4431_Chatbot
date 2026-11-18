# 配装用语：greed / shell / 贪污（偏低）与堆料（偏高）

Keywords: greed, shell, 贪污, 贪, 乞丐, 省钱, 廉价, underpriced, overpriced, 堆料, 装备过剩, 超配, cost band

Summary: Ship Builds.txt 的价格区间只是「应该」（should），不是硬门槛。低于下沿叫 greed / shell / 贪污（underpriced，省掉了该带的东西），高于上沿叫堆料 / 装备过剩（overpriced）。greedford 这个词来自把原本装硬杀的挂载位拆掉、换成更多 120mm 炮的 Axford。

## 结论

| 情况 | 英文 | 玩家口语 | 点评时的意思 |
|---|---|---|---|
| 点数 < 区间下沿 | underpriced | **greed / shell / 贪污 / 贪** | 把该带的东西省掉了，通常省的是硬杀、雷达、DC、弹药深度 |
| 点数在区间内 | in band | — | 正常 |
| 点数 > 区间上沿 | overpriced | 堆料 / 装备过剩 / 超配 | 多出来的多半是非必要部件，或者为了一个极限数值牺牲了别的 |

## greed 的几个变体

- **greed**（贪婪）：为了进攻/某一项数值，把防御性部件砍掉。最常见的是砍硬杀 PDT、砍雷达、砍 DC。
- **shell**（空壳）：船壳 + 武器，几乎不带支撑系统（没雷达、没 DC、没弹药深度），打起来一碰就废。
- **贪污**：中文社区对同一件事的说法，意思是"钱被贪掉了"——点数花在炮上，防御全空。
- **greedford**：Axford 的 greed 版特指——**把原本装硬杀的挂载位拆掉，换成更多 120mm 炮**。这个词是"greed" + "Axford" 的拼合，`Ship Builds.txt` 里的 `greed CH` 就是这一类（它有自己的 must：≥2 门 450 + ≥3 门 120）。

## 点评时怎么用

1. 先判断 **must 是否全过**（决定它是不是这个舰级），再看 **should**（决定它好不好）。
2. 价格偏离方向单独说，不要混进 must/should：
   - 偏低 → 「这艘是 greed 配置：省掉了 X、Y」，并列出省掉的具体部件（硬杀数量、雷达、DC restores）。
   - 偏高 → 「这艘堆料：多花了 N 点，在 A、B 上超出了这个舰级需要」。
3. 不要因为 greed 就判它"不是这个舰级"：`greed CH` 本身就是合法舰级；greed 是一种取舍，不是错误。
4. 但也别推荐 greed 配置给新手——先给区间内的标准配置，再说明哪里可以省。

## 与分类器的对应

- 分类器给每艘船一个 `cost_band`：`in` / `under`（偏低）/ `over`（偏高）。
- 模板只把**区间内 + must 全过 + should 全过**的船当 good 样本，所以 greed 配置不会污染"标准配置"的统计。

# 阵营限制与 CC 特权

来源：官方 wiki 的部件页阵营图标（`Faction (wiki logo)`）+ 352 份真实存档的实测对照。

## 1. 部件阵营怎么读

每个部件页右上角有个圆标，表示「哪个阵营的页面收录了它」：

| 标注 | 含义 | 游戏内 |
|---|---|---|
| **Shelter Alliance (SA)** | 庇护联盟专属 | 只有 SA 船体能装 |
| **Outlying Systems Protectorate (OSP)** | 外围星系保护国专属 | 只有 OSP 船体能装 |
| **没有圆标** | 通用件 | 两家都能装 |

部件 JSON 里没有 `Faction (wiki logo)` 字段，就是**通用**——不是「未知」，也不是「只能某一家」。
201 个部件里 98 个是通用件（例如 Citadel CIC、Ammunition Elevators、Reinforced DC Locker）。

## 2. 装船规则

1. 船体的阵营由 `FactionKey` 决定：`Stock/Alliance`（SA）或 `Stock/Protectorate`（OSP）。
2. 槽位里放的部件必须**同阵营或通用**，否则游戏里装不上（存档里会变成非法配装）。
3. 判断顺序：先看船体阵营 → 再看部件圆标 → 通用件永远合法。

## 3. CC 特权（唯一的例外）

**`CC`（Ocello Cruiser）可以装两家的部件。** 这是舰级特权，不是错误配装。

后果：在存档里统计「OSP 舰队用了哪些 SA 专属件」时，会出现一批跨阵营的使用——
它们**全部来自 CC**。所以下面这类统计（wiki 说 SA 专属，OSP 也有使用）**不推翻 wiki**，
只是 CC 在用：

| 部件 | wiki | 存档实测 |
|---|---|---|
| Mk66 Cannon | SA 专属 | SA 87 / OSP 105（含 CC） |
| Mk90 'Aurora' PDT | SA 专属 | SA 136 / OSP 147（含 CC） |
| VLS-1-23 Launcher | SA 专属 | SA 304 / OSP 85（含 CC） |
| VLS-2 Launcher | SA 专属 | SA 144 / OSP 46（含 CC） |
| FR3300 / FR4800 反应堆 | SA 专属 | SA 602 / 365，OSP 48 / 50（含 CC） |
| RM50 'Parallax' Radar | SA 专属 | SA 144 / OSP 44（含 CC） |
| RF101 'Bullseye' Radar | SA 专属 | SA 204 / OSP 52（含 CC） |
| RS35 'Longshot' Radar | SA 专属 | SA 267 / OSP 3（含 CC） |
| E90 'Blanket' Jammer | SA 专属 | SA 171 / OSP 34（含 CC） |

完整 29 条见 `domain/reports/terms-zh-en.md` 的「阵营特例：CC 的特权」一节与
`domain/data/faction_conflicts.csv`。

## 4. 配船时的正确说法

- 给别人推荐配装：**按 wiki 阵营执行**，别把 CC 能装的件推荐给普通船。
- 检索引擎会把 OSP 存档里出现的 SA 件统计成「也用过」——回答时要说明「那是 CC」。
- 只有 `CC` 这一级允许混装；`CS`/`CL`/`CH` 等都不行。

## 5. 相关文档

- `zh/缩写与术语表.md`：SA / OSP / CC 等缩写
- `zh/槽位配置总表.md`：每个船体每个槽位常见装什么（已按阵营过滤掉非法件）
- `hull/ocello-cruiser-class.md`：CC 的舰体数据

# 线列舰（LN）舰段、舰桥与炮塔朝向

Keywords: LN, 线列舰, Bulk Hauler, Marauder, 杂交, hybrid, 舰段, hull section, bow, core, stern, 舰桥, bridge, 炮塔朝向, mount direction, 朝向, 45度

Summary: LN（Bulk Hauler / Marauder Line Ship）是可拆成 3 段拼装的舰体，3 段 × 3 种 = 27 种组合，每段自带不同的挂载位数量与炮塔朝向；舰桥可拆但不可加，炮塔朝向必须靠实测，不能从存档推出。

## 1. 它是什么

线列舰（LN）的 `HullType` 在存档里写作 `Stock/Bulk Hauler`（旧名），现在叫 **Marauder Line Ship**。它的舰体不是一整块，而是 **`RandomHullConfiguration`**：由「船头 / 船身 / 船尾」三段拼起来，每段有三种款式，所以同一艘 LN 可以有 3 × 3 × 3 = **27 种外形组合**。玩家口语叫「杂交 LN」。

存档里的写法（`<Ship>` 内、`<HullType>` 之后）：

```
<HullConfig xsi:type="RandomHullConfiguration">
  <PrimaryStructure>
    <SegmentConfiguration><Key>{船头}</Key><Dressing>…</Dressing></SegmentConfiguration>
    <SegmentConfiguration><Key>{船身}</Key><Dressing>…</Dressing></SegmentConfiguration>
    <SegmentConfiguration><Key>{船尾}</Key><Dressing>…</Dressing></SegmentConfiguration>
  </PrimaryStructure>
  <HullTint><r>…</r><g>…</g><b>…</b><a>1</a></HullTint>
  <TextureVariation><x>0</x><y>0</y><z>0</z></TextureVariation>
</HullConfig>
```

三段顺序固定：**第 1 段船头、第 2 段船身、第 3 段船尾**。

## 2. 三段对应的 GUID

| 位置 | 款式 | GUID | 外形特征（来自《LN杂交技术》） |
| --- | --- | --- | --- |
| 船头 | 1 | `38e7a28f-1b06-4b73-98ee-f03d1d8a81fe` | 上下有凸起，上面一组 PD 槽位略带倾角 |
| 船头 | 2 | `29eb9c63-6c47-40f2-8f46-4ed4da8d3386` | 下侧内凹 |
| 船头 | 3 | `c534a876-3f8a-4315-a194-5dda0f84c2b3` | 整体平坦，PD 槽位更靠后 |
| 船身 | 1 | `d4c9a66d-81e6-49ee-9b33-82d7a1522bbf` | 下方有凸起，核心区居中 |
| 船身 | 2 | `e2c11e02-b770-495e-a3c2-3dc998eac5a6` | 下侧内凹，核心区靠后 |
| 船身 | 3 | `429f178e-e369-4f51-8054-2e01dd0abea1` | 更宽，核心区在内部，PD 布局不合理 |
| 船尾 | 1 | `2f2b451c-4776-405c-9914-cad4764f1072` | PD 槽位在上下，3 主 + 2 小引擎 |
| 船尾 | 2 | `a8bf77b9-b7e3-4498-bf91-d3e777a7f688` | PD 槽位在上下，4 主引擎 |
| 船尾 | 3 | `78d72a9a-893c-41c6-bddd-f198dfcf77ee` | PD 槽位在左右，2 主 + 4 小引擎 |

## 3. Dressing（外观装饰）不能乱改

每段还有 `<Dressing>`，控制吊车、油罐、集装箱等装饰。**不同舰段的取值范围不同**，填错可能导致存档直接读不出来（游戏里表现为这支舰队打不开）。杂交时正确做法是：**整段 `<SegmentConfiguration>` 原样复制**，不要手写 `<Dressing>`；改之前先备份 `.fleet`。

## 4. 每段有多少挂载位、多大

| 舰段 | 挂载位（Surface） | 隔舱 | 模块 | 合计槽位 |
| --- | --- | --- | --- | --- |
| 船头 | 8 | 4 | 2 | 14 |
| 船身 | 7 | 5 | 4 | 16 |
| 船尾 | 2 | 1 | 1 | 4 |
| **合计** | **17** | 10 | 7 | 34 |

挂载位的**尺寸**（三种舰段都一样）：

| 槽位尺寸（格） | 数量 | 能装什么（举例） |
| --- | --- | --- |
| 6×10×6 | 8（船头 4 + 船身 4） | C65 Cannon（450mm，正好 6×10×6） |
| 3×4×3 | 7（船头 2 + 船身 3 + 船尾 2） | RL18 Launcher（3×1×3）、VLS-1-46（3×2×3）、P20 PDT（2×1×2） |
| 2×2×2 | 2（船头 2） | VLS-1-23（2×2×2）、P20 'Bastion' PDT（2×1×2） |

隔舱槽位是 8×1×8 / 8×3×8，模块槽位是 3×3×3（船头/船身）与 6×6×6、12×12×12（船尾）。

**重要**：不能把大炮塞进小挂载位。LN 的 17 个挂载位里只有 8 个装得下 450mm 火炮，剩下 9 个最大只能装 3×4×3 的东西（见《挂载限制（尺寸与阵营）》）。

挂载位的短标签只有 **MT1 / MT5 / MT6** 三种，而且**会重复**（比如 A 型船头有 4 个 MT1、1 个 MT5、3 个 MT6）。所以存档里的槽位顺序号（1–17）只代表「按舰体层级遍历的顺序」，不等于「第几个炮位朝哪边」。`Ship Builds.txt` 里说的 "mount 1-8" 指的是**实际炮位编号**，与存档顺序不是一回事。

## 5. 炮塔朝向目前只能实测

存档里每个槽位只有：短标签、类型、尺寸、世界坐标、`traverse` / `forward`（这两个是**射界挡块**，不是朝向向量）。因此「1 号挂载位朝前还是朝后」无法从 `.fleet` 或拆包数据直接推出。当前结论：**朝向需要进游戏实测**。

实测用舰队已生成，在 `other info\LN test fleets\`：

| 文件 | 船头 | 船身 | 船尾 | 用途 |
| --- | --- | --- | --- | --- |
| `LN ABB.fleet` | 1 | 2 | 2 | 船头对比 |
| `LN BBB.fleet` | 2 | 2 | 2 | 基准 |
| `LN CBB.fleet` | 3 | 2 | 2 | 船头对比 |
| `LN BAB.fleet` | 2 | 1 | 2 | 船身对比 |
| `LN BCB.fleet` | 2 | 3 | 2 | 船身对比 |
| `LN BBA.fleet` | 2 | 2 | 1 | 船尾对比 |
| `LN BBC.fleet` | 2 | 2 | 3 | 船尾对比 |

每艘船 **17 个挂载位全部装满**，但按尺寸和阵营配的是合法件（LN 是 OSP 船，全部用 OSP 件）：

| 挂载位尺寸 | 装的东西 | 数量 |
| --- | --- | --- |
| 6×10×6 | C65 Cannon（450mm，OSP） | 8 |
| 3×4×3 | RL18 Launcher（OSP） | 7 |
| 2×2×2 | P20 'Bastion' PDT（OSP） | 2 |

另配 1 个 Basic CIC（隔舱）、4 个 Light Civilian Reactor（3×3×3 模块）、1 个 Boosted Reactor、1 个 BW1500 Drive（12×12×12 模块），总点数约 655。用 `domain\tools\validate_fleet.py` 自检过：**尺寸/阵营 0 违规**。

## 6. 舰桥

舰桥属于 `SecondaryStructure`，写法：

```
<SecondaryStructure>
  <SecondaryStructureConfig>
    <Key>{舰桥 GUID}</Key>
    <Segment>2</Segment>
    <SnapPoint>0</SnapPoint>
  </SecondaryStructureConfig>
</SecondaryStructure>
```

规则（玩家实测）：

- 可以**拆掉**舰桥。拆掉会一并失去它自带的 1 个内部雷达和 1 个 CR10 天线。
- 没有舰桥的 LN 在编辑界面会掉图形，但**不影响对战**。
- **超过 1 个舰桥是非法配置**，会让游戏崩。
- 舰桥的摆放方式与舰段类似（`Segment` 指挂在哪一截、`SnapPoint` 指锚点），具体可选项还没整理完。

## 7. 什么时候要用到这些

- 用户问「LN 杂交怎么配」「这艘 LN 是几号船头」。
- 评审一支 LN：先看三段组合，再核对 `Ship Builds.txt` 里「所有火炮朝向一致」这类要求 —— 因为不同舰段的炮位朝向不同，杂交后必须实测确认。
- CI 目前**不会**自动判断朝向，遇到相关问题要明确说明「朝向需要实测」，不要猜。

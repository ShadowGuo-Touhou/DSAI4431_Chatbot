# .fleet 文件结构与校验规则（0.6.2.6，源码依据）

> 目的：说明一份 `.fleet` 为什么能加载、为什么会卡死/闪退。
> 依据：`other info/Nebulous.decompiled.cs`（行号为该文件行号）+ 现网存档实测。

## 0. 一句话结论

**崩溃不是来自"部件装错"，而是来自反序列化后为 null 的数组。**
最典型的是省略 `<SecondaryStructure />`：读档时 `RandomHullConfiguration.SecondaryStructure`
为 null，`BuildSecondaryStructure()` 第一行就取 `config.Length` → 空引用 → 读档协程中断 →
游戏卡在加载画面（看起来像闪退）。实机上所有无舰桥的 LN 都写了空的 `<SecondaryStructure />`。

## 1. 文件骨架

```xml
<Fleet xmlns:xsi="…" xmlns:xsd="…">
  <Name>舰队名</Name>
  <Version>3</Version>
  <TotalPoints>3000</TotalPoints>
  <FactionKey>Stock/Protectorate</FactionKey>
  <Description />            <!-- 可选 -->
  <SortOverrideOrder />      <!-- 可选 -->
  <ModDependencies />        <!-- 必须存在，空也要写 -->
  <Ships> … </Ships>
  <MissileTypes />           <!-- 必须存在 -->
  <CraftTypes />             <!-- 必须存在 -->
</Fleet>
```

数组/列表字段缺失时反序列化为 `null`，代码里只有部分字段做了 `?? new List<>()` 兜底
（`SocketMap` / `WeaponGroups` / `TemplateMissileTypes` / `TemplateSpacecraftTypes` 有兜底，见
79068–79072），`ModDependencies` **没有兜底**，所以空元素也要写出来。

## 2. 舰船字段（`SerializedShip`，79006–79036）

| 字段 | 类型 | 说明 |
| --- | --- | --- |
| `Key` | Guid | 舰船实例 ID；空 Guid 会保留旧值（72813） |
| `Name` | string | 截断到 40 字符（72081） |
| `Cost` | int | 显示用点数，编辑器按各部件重算 |
| `Callsign` / `Number` / `SymbolOption` | string/int | 呼号、舷号、徽标序号 |
| `HullType` | string | 必须能被 `BundleManager.GetHull` 找到，否则 `KeyNotFoundException("No hull with name …")`（71645） |
| `HullConfig` | `HullConfiguration`（多态，`xsi:type`） | 见 §3；**随机舰体必须给**，给了别的类型会走随机生成 |
| `ModDependencies` | ulong[] | 空也要写 |
| `SocketMap` | HullSocket[] | 见 §4 |
| `WeaponGroups` | WepGroup[] | 空也要写；指向不存在的槽位只是被忽略（72867） |
| `InitialFormation` | — | 可选 |
| `TemplateMissileTypes` / `TemplateSpacecraftTypes` | 内嵌模板 | 自建导弹/舰载机时使用 |

## 3. `HullConfig`（随机舰体 LN / CLN）

```xml
<HullConfig xsi:type="RandomHullConfiguration">
  <PrimaryStructure>
    <SegmentConfiguration><Key>船首GUID</Key><Dressing><int>23</int><int>35</int></Dressing></SegmentConfiguration>
    <SegmentConfiguration><Key>船体GUID</Key><Dressing /></SegmentConfiguration>
    <SegmentConfiguration><Key>船尾GUID</Key><Dressing /></SegmentConfiguration>
  </PrimaryStructure>
  <SecondaryStructure />   <!-- 必须存在！空 = 无舰桥 -->
  <HullTint><r>0.62</r><g>0.62</g><b>0.62</b><a>1</a></HullTint>
  <TextureVariation><x>0</x><y>0</y><z>0</z></TextureVariation>
</HullConfig>
```

- **顺序固定**：第 1 段 = 船首，第 2 段 = 船体，第 3 段 = 船尾（69392–69396 `_bowIndex/_coreIndex/_sternIndex`，69547–69553）。
- **段数必须 3**：`BuildPrimaryStructure` 直接下标 `config[0..2]`（69525–69539），少于 3 段会越界。
- **GUID 不认识时不会崩**：找不到就随机换一个同位置舰段（69528–69539）。
- **`<SecondaryStructure />` 缺失 → 崩**（69582 `config.Length`）。空元素 = 不装舰桥。
- 舰桥元素写法：`<SecondaryStructureConfig><Key>舰桥GUID</Key><Segment>0..2</Segment><SnapPoint>0..n</SnapPoint></SecondaryStructureConfig>`（69383–69390）。`SnapPoint` 必须落在该段的 `SuperstructurePoints` 范围内（69587），越界同样崩。
- **最多一个舰桥**：实测装两个会直接坏档（玩家结论）。
- `Dressing`：`int[]`，长度对应舰段的装饰点数量；多余/不足按 `Mathf.Min` 截断（65600–65603），建议原样复制整段。
- LN 三段 GUID（`NLHC catalog.json` 与实测一致）：

| | A | B | C |
| --- | --- | --- | --- |
| 船首 | `38e7a28f-1b06-4b73-98ee-f03d1d8a81fe` | `29eb9c63-6c47-40f2-8f46-4ed4da8d3386` | `c534a876-3f8a-4315-a194-5dda0f84c2b3` |
| 船体 | `d4c9a66d-81e6-49ee-9b33-82d7a1522bbf` | `e2c11e02-b770-495e-a3c2-3dc998eac5a6` | `429f178e-e369-4f51-8054-2e01dd0abea1` |
| 船尾 | `78d72a9a-893c-41c6-bddd-f198dfcf77ee` | `2f2b451c-4776-405c-9914-cad4764f1072` | `a8bf77b9-b7e3-4498-bf91-d3e777a7f688` |

舰桥 GUID：`42d07c1a-156b-4057-aaca-7a2024751423`、`59344a67-9e7b-43df-9f7c-505ad9a0ab87`、
`9ebcea74-e9c9-45b3-b616-e12e3f491024`、`c9d04445-3558-46b4-b6fc-7dca8617d438`。

## 4. `SocketMap`

```xml
<HullSocket><Key>槽位Key</Key><ComponentName>Stock/C65 Cannon</ComponentName></HullSocket>
```

- `Key` 必须是**拼装完成后那艘船**的槽位键；找不到只打 warning 并跳过（72828–72833），不会崩 —— 但会静默丢部件，是"船看起来被清空"的最常见原因。
- `ComponentName` 为空串 = 空槽（72834–72837）。
- 部件找不到、或不被本舰队阵营允许 → warning + 空槽（72840–72853）。阵营判定用的是**读档时舰队的阵营**（`overrideBuildoutOwner.PlayerFleet.Faction`，72841），不是文件里的 `FactionKey`。
- **尺寸与类型确实会校验，只是发生在更下一层**：`SetSocketComponent`（46868）→ `HullSocket.InstallComponent`（约 62250–62280）：
  - `componentPrefab.Type != Type` → `LogWarning("Component and Socket type mismatch.  Component is X and Socket is Y")`，返回 null；
  - `!componentPrefab.TestSocketFit(Size)` → `Debug.Log("Component too large for this socket")`，返回 null。
  两种情况都**不崩**，只是那个槽位静默留空 —— 这是"打开舰队发现少了几个部件"的真正原因。
- 装配合法性规则 `TestSocketFit`（59973–59985）按部件的 `RotateToFit` 分三种（`enum RotateAxis { None, UpOnly, AnyAxis }`，58604；`_rotateToFit` 默认 `None`，58883）：
  - `None`（默认）：三轴各自 ≤ 槽位（不旋转）；
  - `UpOnly`：Y 轴固定，X/Z 可互换；
  - `AnyAxis`：只比**对角线平方和**（`x²+y²+z² ≤ X²+Y²+Z²`），所以 10×8×10 的驱动器能进 8×12×10 的槽。
  实测存档里 `FM530 'Whiplash' Drive`、`Large DC Locker`、`Reinforced CIC` 都出现过"逐轴不过、对角线过"，说明它们的资产设成了 `AnyAxis`；工具对这种情形只给提示，不算错误。
- `ComponentData` 里放弹药/导弹装载；自建导弹用内嵌 `<MissileTemplate>`，指向 `$MODMIS$/…`。

## 5. 造成崩溃/坏档的清单

1. 缺 `<SecondaryStructure />` → 卡加载（本次元凶）。
2. `<PrimaryStructure>` 段数 ≠ 3，或 `SnapPoint`/`Segment` 越界。
3. 装 ≥2 个舰桥。
4. 手工拼 `HullConfig` 时 `Dressing` 用了该段不存在的装饰编号（可能读不到装饰再崩）。
5. `HullType` 不存在（如拼错 `Stock/Bulk Hauler`）→ 抛异常。
6. `ModDependencies` 缺失 + 游戏内 mod 状态不一致 → 载入时 mod 校验失败。

**安全做法：拿一份游戏自己写出的同名舰队做模板，只改 `<ComponentName>` 与 `<Cost>`。**
`domain/tools/gen_ln_donor.py` 就是这么做的。

## 6. 校验工具

- `domain/tools/validate_fleet.py <file|dir>`：体积/阵营/槽位/结构检查（3 段、`SecondaryStructure` 存在、槽位键已知）。
- `domain/tools/gen_ln_donor.py`：从真实 LN 舰队克隆 → 换部件 → 输出到 `other info/LN test fleets/`。
- `domain/tools/build_fleet.py`：**从零生成**一份 `.fleet`（固定舰体与随机舰体都支持）。
  - `--list` 先看槽位：`build_fleet.py --hull "Stock/Bulk Hauler" --sections B,B,B --list`
  - 填充语法 `--fill <槽位>=<部件>`，槽位可写 `MT1`（同名的全填）或 `Compartment:3` / `Module:8`（按类型序号）。
  - 费用自动算：`hull 点数 + Σ 部件点数`；超体积会直接报错并中止。
  - 例：`build_fleet.py --hull "Stock/Sprinter Corvette" --count 10 --faction "Stock/Shelter Alliance" --name "Ten Gun Sprinters" --out "out.fleet" --fill "MT1=Stock/Mk64 Cannon" --fill "MOD2=Stock/FM200 Drive" --fill "MOD1=Stock/FR3300 Micro Reactor" --fill "CMP1=Stock/Basic CIC"`
  - 例（随机舰体）：`build_fleet.py --hull "Stock/Bulk Hauler" --sections B,B,B --faction Stock/Protectorate --out ln.fleet --fill "MT1=Stock/C65 Cannon" --fill "MT6=Stock/P20 'Bastion' PDT" --fill "Compartment:1=Stock/Basic CIC" --fill "Module:8=Stock/BW1500 Drive"`

### 6.1 建造顺序（人格里的同一规则）

1. **首选**：整艘复制现成舰队（连导弹一起，只改名）——最不容易崩，也最符合游戏实际。
2. **次选**：在现成舰队上小改（换部件、换弹药），`gen_ln_donor.py` 就是这条路。
3. **兜底**：`build_fleet.py` 从零生成。用户明确要从零建（例如"造 10 艘炮艇"）时用它，
   即使这个配置在战术上很糟：**先给一句风险提示，再照做**——用户要的是能进游戏的合法文件。

## 7. 待确认

- 尺寸超限时游戏是"卡住不装"还是"自动缩小"，需在游戏里实测一次。
- 舰桥 `SnapPoint` 的合法上限随舰段而定（`SuperstructurePoints` 数量），目前按实测舰队反推。
- 真实存档 `S2LN NEO.fleet` 省略了 `<ModDependencies />` 与 `<CraftTypes />` 仍能加载，
  说明这两个空元素并非必需；`validate_fleet.py` 只把它当提示，不再算错误。

## 舰体键与阵营键：必须写游戏认的值

这一条是最容易「舰队能载入、但部件/阵营全错」的原因。<HullType> 和 <FactionKey> 不是 wiki 名字，
而是存档里的键；<ComponentName> 也必须带 Stock/ 前缀。

合法 <FactionKey>（只有两个）：

| 键 | 说明 |
|---|---|
| Stock/Alliance | Shelter Alliance（ANS） |
| Stock/Protectorate | Outlying Systems Protectorate（OSP） |

合法 <HullType>（17 个，取自真实存档）：

| 键 | 显示名 |
|---|---|
| Stock/Axford Heavy Cruiser | Axford Heavy Cruiser |
| Stock/Bulk Feeder | Bulk Feeder |
| Stock/Bulk Hauler | Bulk Hauler |
| Stock/Container Hauler | Container Hauler |
| Stock/Container Hauler Refit | Container Hauler Refit |
| Stock/Keystone Destroyer | Keystone Destroyer |
| Stock/Levy Escort Carrier | Levy Escort Carrier |
| Stock/Mercator Oiler | Mercator Oiler |
| Stock/Ocello Cruiser | Ocello Cruiser |
| Stock/Ore Carrier | Ore Carrier |
| Stock/Raines Frigate | Raines Frigate |
| Stock/Shuttle | Shuttle |
| Stock/Solomon Battleship | Solomon Battleship |
| Stock/Sprinter Corvette | Sprinter Corvette |
| Stock/Tugboat | Tugboat |
| Stock/Vauxhall Light Cruiser | Vauxhall Light Cruiser |
| Stock/Worden Fleet Carrier | Worden Fleet Carrier |

常见错误（都会导致「载入后部件全空 / 阵营未知」）：

- 写 Stock/Axford Heavy Cruiser Class（多一个  Class）⇒ 游戏找不到船体，整艘船作废。
- 写 Stock/Shelter Alliance ⇒ 阵营键无效，所有部件因阵营不匹配被静默丢弃。
- 写 Mk64 Cannon（缺 Stock/）⇒ 部件名无效，槽位留空。

生成器 domain/tools/build_fleet.py 现在会把 wiki 名自动映射成这三个键；校验器 alidate_fleet.py 会直接报「舰体键无效 / 阵营键无效」。

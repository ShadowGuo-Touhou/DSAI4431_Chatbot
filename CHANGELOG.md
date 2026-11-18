# CHANGELOG — `Nab-branch`

Everything below is **what this branch adds on top of `main` (`4e3d6c2`)**. `main` itself is untouched: the
framework only gained three small hooks (检索轮数、术语表、人设), and the rest is a new `domain/` tree plus
`sample fleets/` that can be ignored if you only care about the GUI.

Rebuild everything from scratch with:

```
python domain/tools/import_official.py      # wiki → domain/kb/raw_official
python domain/tools/build_spec.py           # other info/Ship Builds.txt → 53 classes
python domain/tools/classify_ships.py       # saves + 新手包 → 分类结果
python domain/tools/build_layouts.py        # 槽位拟合、部件阵营
python domain/tools/build_templates.py --write-kb
python domain/tools/build_official.py       # → domain/kb/docs（910 篇）
python domain/tools/index_kb.py             # → repo/asset/RAG 并建索引（2 567 块）
```

`other info/`（131 MB 的 PDF、反编译源码、存档副本）**不进仓库**：脚本按 `仓库/other info` 读，工作区里
以目录联接指向仓库外的那份，`.gitignore` 已排除。

---

## 1. 框架侧的三处改动（`src/`、`data/personality/`）

| 文件 | 改动 | 原因 |
| --- | --- | --- |
| `core/gui/tool_router.py` | `MAX_ROUNDS 3 → 6`；`TOOL_SPEC` 描述改成「怎么写检索词、查几次、怎么接续」 | 造舰请求要连查「舰级要求 → 槽位表 → 部件尺寸/点数」三跳，3 轮永远停在「还没查到槽位表」；模型原来只会把整句问题丢进检索 |
| `core/gui/chat_config.py` | `DEFAULT_RAG_PROMPT` 从一句「你有知识库、先调用」扩成四句检索机制（分目录、关键词、英文名、文件名当下一跳、缺数就继续查），旧文案自动迁移 | 提示词只说了「存在」，没说「怎么查」；旧版本写死的两版文案通过 `_LEGACY_RAG_PROMPTS` 自动替换，用户自己改过的不动 |
| `core/rag/query_terms.py` | 376 条中↔英术语映射（原 328） | 中文提问要能命中英文 wiki；新增阵营/CC 特权、脊髓炮、满套软杀、造舰技巧等 |
| `data/personality/Nebulous/SKILLS.md` | 技能 3.3 坏舰级清单、3.4 价格偏离、3.5 造舰 SOP、「回答形态（硬性）」、「不要为凑参数而反问」；新增**技能 0.5 检索路由**（13 类问题 → 第一条查询 → 补查 → 目标目录） | 模型会拿「请给我四个参数」代替交付物；也常常查一条就下结论 |
| `data/personality/Nebulous/CHECKLIST.md` | 「最多 2 次检索」改成「缺会改变答案的数就继续查，上限 6 次」；补「按类型选目录」与真实的 `sockets/<船名>.md` 路径 | 文档自我限制到 2 轮，和 `MAX_ROUNDS=6` 矛盾，模型按文档收手 |

## 2. 新增的知识库（`domain/kb/`，910 篇 / 1.31 M 字符）

来源只有三个：官方 wiki（游戏 0.6.2.6）、`other info/Ship Builds.txt`、玩家存档与中文资料。

| 目录 | 篇数 | 内容 |
| --- | --- | --- |
| `component/` | 226 | 每个部件的尺寸/点数/供电/血量/冷却/弹药 |
| `munition/` | 122 | 每种弹药的伤害、穿深、单价（b 发 / a 点） |
| `mechanics/` | 119 | 装甲、损伤、雷达、电子战、DC、船员、移动 |
| `builds/` | 120 | 53 个舰级的 Must/Should/Optional/Avoid + 65 篇**逐槽样板船** |
| `guide/` `map/` `craft/` `hull/` | 98 / 43 / 33 / 22 | 官方指南、地图、舰载机、船体面板 |
| `sockets/` | 47 | 每艘船的槽位表（尺寸、段、挂载号、常用部件与填充率） |
| `zh/` | 31 | 中文手册：SOP、术语、装甲、弹库、编成、CC 特权、造舰技巧… |
| `catalog/` `missile/` `faction/` `reference/` | 20 / 21 / 4 / 4 | 按口径/舰级/阵营的速查表 |

新增的两类「数据页」是这个分支最有用的部分：

- **`sockets/*.md` + `zh/槽位配置总表.md`**：直接回答「这个槽位一般装什么」，带填充率、备选、配对槽。
  例：`Keystone MT7 → Mk600 Beam Cannon ×29 / Mk550 Railgun ×6`。
- **`builds/<class>-sample-N.md`**：整艘船的逐槽装配（31 个槽位、点数、供电、弹库、弹药、舰载机），
  可以照着抄。

## 3. 新增的数据与工具（`domain/data/` 27 个 JSON，`domain/tools/` 68 个脚本）

- **舰级分类**：`ship_builds.json`（53 类，含 must/should/optional/avoid/价格区间）、`ship_classification.json`
  （**1 375 艘**：1 330 match、45 bad_class）。
- **槽位**：`hull_sockets.json`、`hull_layouts.json`、`socket_fit.json`、`layout_corrections.json`。
- **价格**：`missile_prices.json`（**536** 枚导弹/发）、`craft_prices.json`（**48** 型舰载机）、
  `ammo_costs.json`（炮弹/诱饵/弹库）、`munition_storage.json`（单发体积，用来算弹库能装几发）。
- **装甲**：`hull_armour.json`（16 艘船体面板读数 + DR 上限），`build_armour_doc.py` 生成
  `zh/装甲与伤害机制.md`（含 30 弹 × 16 船穿深表）。
- **术语**：`terms_zh_en.json`、`ui_terms_zh_en.csv`（3 669 对）、`faction_conflicts.csv`（29 条 CC 跨阵营）。

## 4. 61 个可直接载入的样板舰队（`sample fleets/`）

每个舰级取 2 艘「match 且价格居中」的真实存档船，原样导出成单舰 `.fleet`，**不改任何部件**：

- 63 个文件（61 艘 + 2 个全量合并：Alliance 34 艘 / Protectorate 27 艘），全部 `validate_fleet.py` 0 issue；
- 修正了两个会让船「打不出导弹、起飞不了飞机」的坑（见第 6 节）；
- 文件名 = `<舰级> - <船名>.fleet`，清单在 `domain/reports/sample-ships.md` 与 `zh/样板船清单.md`。

## 5. 三份新的中文手册

- `zh/造舰技巧与分步流程.md`：满套软杀判定（2 干扰吊舱/2 箔条/≥1 照明弹/2 PDT/2 雷达）、四条配队规则、
  greedford 双舰实战例子、10 步建造流程与检查表。
- `zh/阵营限制与CC特权.md`：`Faction (wiki logo)` 圆标怎么读、只有 CC 能混装、9 个最常跨阵营的部件。
- `zh/弹药点数表.md`：23 种炮弹 + 20 种导弹 + 诱饵 + 舰载机的单价，以及弹库「第一个免费、其余翻倍」的计费规则。

---

## 6. 三个例子（为什么值得 merge）

### 例 1：一艘船的费用能反解出弹药单价

游戏不给诱饵/照明弹的单价，但存档里每艘船的 `TotalPoints` 是真实的。于是对同一艘船列方程：

```
ship.cost = Σ 船体 + Σ 部件 + Σ 弹库 + Σ(弹药发数 × 单价) + Σ(导弹发数 × 导弹单价)
```

EA20 在 72 艘船上出现，且这些船上其它弹药都已有单价 ⇒ 解出 `1.00 点/发`（残差中位数 1.00，
「只有 EA20 未知」的起步舰队残差 **0.00**）。同样的方法解出 **EA99 = 8 点/发**（不是 1 点），
并整理了 536 枚玩家导弹的每发价格。

### 例 2：合并舰队后导弹与飞机全部消失

症状：载入合并后的 `.fleet`，日志刷 `Fleet is missing guide with GUID 071dc387-…  The ship … will start independently`，
且所有发射器、机库都是空的。两个独立的原因：

1. `<InitialFormation><GuideKey>` 指向旧 UUID —— 复制船时给每艘船重新生成了 `<Key>`，编队引导键还指着老 UUID；
2. `.fleet` 根节点的 `<MissileTypes>` / `<CraftTypes>` 模板库没被复制 —— 发射器里写的是
   `$MODMIS$/SGM-100 ARM`、机库里写的是 `$CRAFT$/B-45 Sturgeon`，库里没有这两条就整条丢掉。

修法：`domain/tools/fleet_templates.py` 负责收集/去重/写回模板库；导出的单舰用自己的 `<Key>` 当引导键；
合并时按新旧键表重映射。结果：63/63 文件解析通过、0 个悬空引导键、Alliance 携带 56 导弹 + 8 舰载机模板。

### 例 3：`MT1` 到底是哪个槽

同一艘船的 A/B/C 三个外观变体有**完全相同的槽位键**，但文件里的顺序不同，所以「第几个槽」按文件顺序数
在三个变体之间对不上。最终用游戏自己的挂载号（prefab 里的 `i`，`(mount 1)` 条件引用的就是它）：

- 挂载槽：**全船连续编号**（Marauder `MT1…MT17`，6×10×6 的大家伙是 `MT1–MT8`）；
- 舱室/模块：每段从 1 开始（`CMP1`、`MOD1`），因为 `(compartment N)` 是按段算的。

于是 `B | MT1 … MT4`、`C | MT5 … MT8` 这种写法在三个变体之间稳定，机器人也能引用「艏段 MT3」而不歧义。

---

## 7. 已知缺口

- `validate_fleet.py` 对模块化船体（Flathead/Marauder/Moorline）会打 `槽位未知`：它按 wiki 船体名查表，
  而存档里写的是 `Stock/Bulk Feeder` 之类的键 —— 数据齐全，只是校验器的名字映射没接上。
- 少数样板船的来源存档本身带「装不进的部件」（例如 `All Reaching All Taking` 的 `T30 Cannon` 6×3×6
  塞进 3×4×3），导出时原样保留，没有改船。
- 弹库装载量依赖存档里的实例数据；游戏重新计算点数时，弹库会被重算，所以样板船的「全价」是估算值
  （页面底部给出与存档原值的差）。

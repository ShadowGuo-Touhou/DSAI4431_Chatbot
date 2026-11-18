# NEBULOUS: Fleet Command 领域助手 —— 实施计划 v1

> 目标：把当前"通用聊天机器人"改造成"星舰舰队参谋"——能查规格、讲战术、读 `.fleet` 文件并评分/给改进建议。
> 本文件是讨论稿，编号 [D1]–[D6] 是待你拍板的决定，见第 12 节。

---

## 0. 一句话结论

数据是够的，而且比预想的干净：**Wikidot 粉丝 wiki 可以整站抓**（~300 页，含每个组件的完整数值 + `Save Key`），
`Save Key` 正好等于 `.fleet` 文件里的 `ComponentName`，**天然能 join**。
原先唯一的真缺口——**舰体插槽的位置/尺寸在任何可读文件里都没有**（wiki 也没有）——**已经解决**：
用 UnityPy 直接读游戏的 `Assets\AssetBundles\stock-f1|f2`，把每个舰体的 `HullSocket` 序列化字段全部导出
（44 个舰体 / 580 个插槽：类型、格子尺寸、3D 位置、射界），并用 346 份真实舰队的组件-插槽装配反证，**0 例尺寸/类型冲突**。
详见 6.3。

---

## 1. 已确认的硬约束（读代码得到，不是猜的）

| 位置 | 限制 | 对方案的影响 |
|---|---|---|
| `core/rag/paths.py` | 知识库只收 `.md` / `.txt`，单文件 ≤ 2 MB，总块数 ≤ 2000 | 全部清洗成 markdown；控制文档粒度 |
| `core/rag/chunker.py:20-25` | 目标块 480 字，overlap 64，硬上限 700 | 一个实体一份文档，天然对齐 |
| `core/rag/chunker.py:214-219` | **表格整块不切**（超长也不切） | 禁止"整张 wiki 大表"直接入 KB，必须按行/按实体拆 |
| `core/rag/chunker.py:336-339` | 块前缀 `资料：<标题>（来源：<文件> Lx-Ly）` | 标题层级=实体名，检索命中率直接受它影响 |
| `core/gui/tool_router.py:13` | 只有 **1 个**工具 `search_knowledge` | 加"舰队分析"工具要改代码（约 80 行） |
| `core/gui/tool_router.py:15-18` | 单轮最多 3 次工具调用；命中分 < 0.5 直接判"没资料" | 多跳问题要设计成一次检索能答 |
| `data/settings.ini` 默认 | `rag_top_k=4`、`rag_inject_chars=3000` | 只够 4–6 段，文档必须"自包含" |
| `core/gui/personas.py:49` | 人格提示词 **20000 字符**封顶 | 人格只放"角色+答题规范+校对清单"，知识进 KB |
| `core/gui/personas.py:156-174` | 人格=`<data>/personality/<id>.json` + 同目录 `.md` | 新建领域人格不动默认的 FatWhale |
| `core/gui/attachments.py:33-39` | 收 `.xml` 但**不收 `.fleet`**；文本 ≤ 200 KB | 舰队文件要改名 `.xml`，或改一行后缀表 |
| 同上 | 图片只支持 `deepseek-flash`，且只在 user 消息里；超过 10 轮自动降级为文字 | 截图问答必须用 flash 模型 |
| `.gitignore:72` | `asset/RAG/` 被忽略 | 交作业打包要 `git add -f`，或交"生成脚本+源数据" |

---

## 2. 能力分级：先保底，再炫技

| 级别 | 能力 | 依赖 | 评分价值 |
|---|---|---|---|
| **L1 查询** | "VLS-2 装填多快""Ocello 多贵""Aurora PDT 打多远" | wiki 数值库 | 基本分（3/10） |
| **L2 解释** | 术语（PDT/LOBs/burn-through）、机制（雷达/EW/装甲）、战术 SOP | 机制页 + 你的教程 | 加分（7/10 的门槛） |
| **L3 读舰队** | 贴一个 `.fleet` → 逐舰报表 + 点数/功率/导弹位核对 + 组成点评 | 解析脚本 + 数值库 + [D1] | 技术复杂度主力 |
| **L4 生成舰队** | 给需求（"3000 点、Protectorate、防空流"）→ 可加载的 `.fleet` | 插槽地图（第 6.3 节） | 天花板，风险高，放最后 |

**建议：L1+L2 做扎实，L3 做成"亮点"，L4 只演示"改一艘船"（模板改写，见 6.4）。**

---

## 3. 数据源盘点

| 源 | 可达性 | 内容 | 用途 |
|---|---|---|---|
| `https://nebfltcom.wikidot.com/` | **HTTP 200，可整站爬** | ~300 页：`/component:*`（~200）、`/munition:*`（~60）、`/hull:*`（~18）、`/mechanics:*`（~15）、`/modding:savekeys`、`/glossary`、`/buildtips:*`、`/external:tools`、`/unittest:pdt` | **数值主库** |
| 官方 wiki `wiki.hoodedhorse.com` | **Cloudflare 403**（`api.php` 也 403） | 同上数值，另有 Armor/Crew/ECM 等理论页 | 仅用于交叉校验；走 Wayback（`web.archive.org/web/20250803231357/.../Components`，rev 581，游戏版本 0.5.2.2） |
| 游戏本地化 `Nebulous_Data\StreamingAssets\Localization\en_US\en_assets.json` | 本体自带，129.9 KB | 所有舰体/组件/弹药/导弹的**名字 + 一句话描述 + 风味文本**，**无数字** | 官方措辞、别名、中文名（`cn_assets.json`） |
| `en_tut.json`(743) / `en_ui.json`(3672) | 同上 | 教程字幕、全部界面文案 | 教程语料；截图识别的"菜单词表" |
| 你的教程/攻略/截图表格 | 你提供 | 战术、SOP、黑话、图片表格 | L2 主力 |
| 你的 344 份 `.fleet` | 本地 `Saves\Fleets` | 真实配装样本 | 好舰队案例（精选 10–20）+ **反推插槽容量**（6.3） |
| 游戏本体数值（bundle / `Nebulous.dll`） | 需 UnityPy/ILSpy，工作量大 | 插槽定义、隐藏参数 | **不做**（除非卡住） |

**Join 键**：wiki 每页都有 `Save Key`，形如 `Stock/VLS-2 Launcher`；`.fleet` 里 `<ComponentName>` 就是它；本地化 key 由它推导（`HULLCOMPNAME_VLS_2_LAUNCHER`）。三方可以直接合并。

---

## 4. 知识库结构（生成到 `repo\asset\RAG\`）

```
asset/RAG/
  _index.md                    总览：KB 里有什么、命名法、引用规范（模型检索"目录"用）
  factions/protectorate.md  alliance.md  ...
  hulls/ocello.md  axford.md  ...           18 份
  components/mounts/vls-2-launcher.md       武器/雷达/EW（Surface/Mount）
  components/compartments/reinforced-cic.md
  components/modules/fm530-whiplash-drive.md
  munitions/ea12-chaff-decoy.md             60 份
  craft/halberd.md                          舰载机
  mechanics/radar.md  armor.md  ewar.md  point-defense.md  missiles.md
            damage-control.md  crew.md  intelligence.md  movement.md  fleet-building.md
  tactics/screening.md  missile-defense.md  alpha-strike.md  positioning.md  ...
  jargon/glossary.md                        黑话中英对照
  fleets/design-rules.md  critique-rubric.md
  fleets/examples/<name>.md                 精选好船（报表+点评）
  fleets/file-format.md                     .fleet 格式说明（教模型读 XML）
```

### 单实体模板（关键：一段一实体，480 字内）

```markdown
# VLS-2 Launcher（VLS-2 导弹发射器）

别名：VLS-2、VLS2、垂直发射-2 ｜ 存档键：`Stock/VLS-2 Launcher` ｜ 阵营：Alliance ｜ 类别：武器-导弹

| 项 | 值 |
|---|---|
| 点数 | 10 |
| 尺寸 | 3x4x3（不可平铺） |
| 质量 | 5 t ｜ 功率 -200 kW |
| 结构 | 200 hp ｜ 阈值 15 hp ｜ 功能阈值 10% |
| 发射 | 0.50 s/发（120 RPM）｜ 导弹尺寸 2 ｜ 单元格 4 |
| 灾害概率 | 5%（cell launcher） |

**干什么用**：最泛用的尺寸 2 导弹平台，混装 SGM-2 系列；**一次性**——打完无法补给。
**搭配**：Missile Programming Bus 提编程通道；Magazine 供弹。
**代价/取舍**：功率重（-200 kW）、质量小，但占 3x4x3 大槽。
```

要点：
1. **标题 = 唯一实体名**（chunker 会把它写进块前缀，检索靠这个）。
2. **双语别名行**必须写（`bge-base-zh` 中英混检，中文提问也能命中）。
3. 一张小表 + 三段话，总长 ≤ 480 字；数值来自 wiki，措辞来自本地化。
4. 大表（如全组件对比）**不进 KB**，只作为开发者参考。

---

## 5. 构建流水线（`domain/tools/`，Python 3.12，只用标准库 + 项目自带依赖）

```
① fetch_wikidot.py   抓 /system:list-all-pages 的 21 页 → 按 Category 过滤出
                      component:/munition:/hull:/mechanics:/glossary/... 的 URL
                     → 逐页 GET（1 s 间隔）→ 解析"两列 spec 卡" + In-game Description
                     → domain/kb/raw/<category>/<slug>.json
② join_localization.py  读 en_assets.json / cn_assets.json / en_ui.json / en_tut.json
                     → 给每个实体补：官方英文名、中文名、一句话描述、UI 词表
③ build_kb.py        合并 ① ② → domain/kb/db.json（唯一事实源）
                     → 渲染 markdown（第 4 节模板）→ repo/asset/RAG/
                     → 调 dsai4431_chatbot.core.rag.chunker 自检：
                        块数、单块是否超 700、前缀是否正确、有没有"一大坨表"
④ mine_sockets.py    扫 344 份 .fleet → (hull, socket_key) 上观察到的组件集合
                     → domain/kb/sockets.json（反推的插槽容量表）
⑤ fleet_report.py    .fleet / .ship → 报表 markdown（点数/功率/质量/防空/导弹位/警告）
⑥ index_and_test.py  触发重建索引（app 启动或手动按钮）+ 跑 20 条检索自测
                     （期望命中的文档 / 分数）
⑦ img2md.py          截图表格 → deepseek-flash 视觉 → markdown 草稿（人工校对）
```

命令形态（`repo\.venv\Scripts\python.exe`）：
`.\domain\tools\fetch_wikidot.py --all` → `--build` → `--mine-sockets` → `--rebuild-index`

自检是重点：**在写 300 篇文档之前**，先拿 3 页跑通链路，用项目的 chunker 验证块数与长度。

---

## 6. `.fleet` 能力（技术复杂度主要在这里）

### 6.1 文件里到底有什么（已解析 `S2 DIR OCELLO.fleet`）

```xml
<Fleet><Name>S2 DIR OCELLO</Name><Version>3</Version><TotalPoints>3000</TotalPoints>
  <FactionKey>Stock/Protectorate</FactionKey>
  <Ships><Ship>
    <Key>…GUID</Key><Name>Command Cruiser Must Command</Name><Cost>3000</Cost>
    <HullType>Stock/Ocello Cruiser</HullType>
    <SocketMap>
      <HullSocket><Key>iJzzxinSN0uJIjrt9M3aGA</Key>
        <ComponentName>Stock/VLS-2 Launcher</ComponentName>
        <ComponentData p2:type="ResizableCellLauncherData">
          <MissileLoad><MagSaveData><MagazineKey>…</MagazineKey>
            <MunitionKey>$MODMIS$/SGM-291 DO NOT SCARE ME</MunitionKey><Quantity>11</Quantity>
```

**有**：舰队名/点数上限/阵营、每舰 hull + 点数 + 呼号 + 舷号、29 个插槽上的组件、导弹装载清单（含模组弹）。
**没有**：插槽的**尺寸/类型/位置**；单个组件的点数（只有整舰 `Cost`）。

### 6.2 能做的校验（不需要插槽数据）

- 点数：舱单 vs `<TotalPoints>`（也该等于各舰 `Cost` 之和）
- 阵营：`<FactionKey>` ↔ 各组件阵营（wiki 的 Faction 字段）
- 用电：Σ `Power`（wiki）↔ 反应堆/驱动提供的功率 → 余量给建议
- 质量/加速度：Σ 质量 → 用 hull 的 `Linear Thrust` 算加速度（hull 页有）
- 导弹：发射器 cell 数 × 尺寸 ↔ `MissileLoad` 实际装填（超载/空仓/弹药不匹配）
- 防空/EW/传感：按功能分类统计（PDT 数量与覆盖率、jammer 类型、雷达质量）
- 灾害：5%/10%/15% 类组件的数量与堆叠风险
- 依赖：`$MODMIS$` 等模组键 → 标"来自模组，数值未知"

### 6.3 位置问题（你担心的那条）——**已解决：从游戏资源里直接读**

**事实**：`.fleet` 只有不透明 GUID；`hull:*` wiki 页没有插槽表。但 `other info` 里的反编译源码给出了完整结构：
`HullSocket : MonoBehaviour`（第 62035 行）序列化了 `_key / _size(Vector3Int，单位 0.25 m) / _type(_Surface|Compartment|Module) / _attachPoint / _traverseLimits / _forwardLimits / _interiorOverhangSpace / _defaultComponent`，
所以**只要读出这批组件实例的字段，插槽表就是游戏真值**，不是反推。

做法（`domain\tools\`）：

1. `repo\.venv-tools`（UnityPy 1.25.4，独立于 app 的 `.venv`）读 `Assets\AssetBundles\stock-f1|f2`；
2. 按二进制布局定位脚本：`int32 fileID | int64 GameObject | u8 enabled+pad | int32 scriptFileID | **int64 scriptPathID** | string m_Name | 字段…`（脚本 pathID 在偏移 20，不在 16）；
3. 用 `Transform.m_Father` 回溯到舰体根节点（`Keystone Destroyer` 之类），把插槽位置换算成舰体本地米制坐标；
4. 两个 `TraversalLimits` 结构**无条件**序列化（各 20 字节），`_hasTraverseLimits` 只表示"是否生效"——按这个读，880 个插槽 **0 字节残留**。

产物与校验：

- `domain\data\hull_sockets.json`：**44 个舰体 / 580 个插槽**（Ocello 30 = 11 挂载 + 9 舱室 + 10 模块，与 wiki 的 "11 mounts / 9 compartments / 10 modules" 完全对上，互为交叉验证）。
- `domain\tools\audit_fit.py`：拿全部 **346 份真实舰队 / 1776 艘船 / 25911 个装配**去过一遍，规则是"组件类别 = 插槽类型"且"wiki 尺寸能塞进插槽格子"（游戏建模时会强制这两条）：
  `fit_ok=25081, type_mismatch=0, key_unknown=0, too_large=27`。
  27 例里 26 例是同一处——`Stock/Tugboat` 的 `MOD2`（8×3×6）装了 wiki 标 `5x5x5` 的反应堆，属于 **wiki 尺寸与游戏不一致**，已单列，不是提取错误；剩下 1 例同理（`Container Hauler Refit` 的 `MT6` + `T30 Cannon`）。
- `domain\tools\socket_lib.py` + `fleet_report.py`：报表里现在会打印 `| socket | type | size | fitted | check |`，并对每个装配给 `ok` / 类型不符 / 装不下。`S2 DIR OCELLO.fleet` 的 29 个装配全部 `ok`。
- `domain\tools\build_sockets_kb.py` → `kb\docs\hull\sockets\*.md`（16 份，含中文方位词 `艏部/中段/艉部`、`左舷/右舷/中轴`、`射界 左右各 N°`），已进索引：问「Ocello 的 MT7 挂载点在哪」→ 0.896，问「Keystone 有几个模块插槽」→ 0.894。

**所以 [D2] 的 A/B 方案不再需要**：不用反推、也不用手工录。留下的两个小尾巴：
① 多段舰（Bulk/Container 的 A/B/C × Bow/Core/Stern）按"同键合并"处理，已合并成一条舰体；② 模组舰体（KUIPER/Falcata 等 95 艘）没有插槽表，报表里标"模组舰体，未知"。

### 6.4 生成舰队：模板改写而不是从零画

从零生成必须精确知道 29 个槽的 GUID → 不现实。
可行：**取一份现成同型船的 `.ship`/`.fleet` 作模板**，只换 `<ComponentName>`（槽位不动）→ 合法性天然成立，
点数由我们算。这就是"给这艘 Ocello 的导弹换成一波流"这类请求的正确解法。
L4 演示口径：*"改一艘船"*，不是"造一整支舰队"。

---

## 7. 人格（`data/personality/Nebulous/` + `Nebulous.json`）

```json
{"id": "Nebulous", "label": "舰队参谋", "dir": "Nebulous",
 "files": ["IDENTITY.md", "SOUL.md", "USER.md", "CHECKLIST.md"], "order": 0}
```

- `IDENTITY.md`：NEBULOUS 舰队参谋（staff officer），口吻=作战简报；中英混用（术语保英文）。
- `SOUL.md`：先给结论再给依据；数值必带单位与来源；**没查到就说没查到**（禁止编数值）；版本不同先问。
- `USER.md`：服务对象=舰队指挥官；偏好直接、要数字、要取舍理由。
- `CHECKLIST.md`：点评舰队的固定顺序（预算→角色→防空→EW/传感→损管→弹药→动力→余量），≤ 1500 字。

> 20k 上限足够；来源在 `domain/persona/`，用 `tools/install_persona.py` 复制进 `data/`（可随仓库走）。

---

## 8. 图像能力

1. **图片表格 → markdown**（必做，正是你说的"只在图里的表"）：`img2md.py` 调 `deepseek-flash` 转写 → 人工校对 → 进 KB。批量 20–50 张没问题。
2. **截图识别**（加分项）：
   - KB 加 `ui/screens.md`（菜单词表来自 `en_ui.json`）+ `craft/*`、`components/*` 的视觉特征描述；
   - 用固定提示词让模型做"先描述、再归类、给置信度与依据"，而不是直接猜；
   - 可靠范围：**认界面/读 tooltip/认舰种轮廓**；"某舰正在用某武器开火"不可靠，演示时如实说局限。
3. 训练分类器（CLIP/微调）**不做**——投入产出比差，且答辩时讲不清。

---

## 9. 评估与演示（10 分里的"技术贡献"和"演示"都靠这个）

- **测试集 30 条**：15 条事实（组件/舰体/弹药数值）、8 条机制/术语、4 条舰队点评、3 条"KB 里没有"（考察是否承认不知道）。
- 指标：命中率、数值正确率、幻觉率（编造数值/文档）、平均延迟、检索分分布。
- **7 分钟演示脚本**：① 问我"VLS-2 能不能打 SGM-2"→ 引用来源；② 术语"burn-through 是什么"；③ 贴 `S2 DIR OCELLO.fleet` → 报表 + 3 条改进；④ 换一艘船加双 PDT → 说明为什么；⑤ 贴截图 → 认出是舰队编辑器；⑥ 讲数据管线（爬取→实体化→索引）+ 评估数字 + 局限。

---

## 10. 分工与排期

| 阶段 | 内容 | 谁 | 估时 |
|---|---|---|---|
| P0 | 脚手架 + 3 页跑通链路 + chunker 自检 | 我 | 1–2 h |
| P1 | 全站抓取 + 本地化 join + 人工抽检（10 组件对游戏内） | 我 | 3–4 h |
| P2 | 文档渲染 + 建索引 + 20 条检索自测调参（top_k、阈值） | 我 | 2–3 h |
| P3 | 人格四件套 + 问答调优（数值/术语/拒答） | 我 | 2–3 h |
| P4 | 舰队解析/报表/校验 + 插槽反推 + 精选案例 | 我 | 3–5 h |
| P5 | 图片表格转录 + 截图识别 + 评估 | 我 | 2–4 h |
| P6 | 测试集、README、提交打包、PPT 素材 | 我+你 | 2 h |
| 你的部分 | 教程/攻略文本、图片表格、精选 10–20 份好舰队、3–5 条演示船的插槽截图、20 张识别测试截图、拍板 [D1]–[D6] | 你 | 2–3 h |

合计约 15–21 h 我的工作，可拆成 3–4 个交付节点（每个节点都保持"可运行+可演示"）。

---

## 11. 风险

| 风险 | 影响 | 对策 |
|---|---|---|
| wiki 数据与游戏版本不符（0.5.2.2 / 2025-01） | 数值错 | 每篇带 `game version` 与抓取日期；抽检 10 个组件进游戏对比；KB 里注明 |
| 官方 wiki 被 Cloudflare | 少一个源 | 用 Wikidot + Wayback，足够 |
| 表格块过大撑爆注入预算 | 检索质量差 | 按实体拆文档；build_kb 自检单块长度 |
| 中文提问＋英文文档召回差 | 答非所问 | 每篇双别名；必要时把 `cn_assets.json` 中文名并入正文；调 `rag_min_score` |
| 模型对 29 个组件做心算 | 点数/功率算错 | **一律走脚本**，模型只负责解释与建议 |
| 模组弹（`$MODMIS$`）无数据 | 报表缺项 | 标"模组内容，未知"，不猜 |
| 插槽位置/尺寸 | **已解决** | 6.3：从游戏 bundle 直读 `HullSocket`；wiki 的反应堆尺寸有一处不一致（26 例），标成已知差异 |
| `asset/RAG` 被 gitignore | 提交缺 KB | `git add -f` 或提交"源+脚本+一键构建" |

---

## 12. 需要你拍板的 6 个决定

- **[D1] 舰队能力形态**：(a) 仓库外脚本，聊天里贴报表（零改动，1 天）；(b) 加 `analyze_fleet` 工具（改 `tool_router.py`+`main_window.py` 约 80 行，演示最顺）。(建议 b，先 a 兜底)
- **[D2] 插槽位置**：~~A 反推 / B 手工表 / C 跳过~~ → **已由 6.3 的 bundle 直读解决**（A/B 都不需要了）。
- **[D3] 阵营范围**：两阵营全做，还是先 Protectorate（样例舰队是 P 系）。（建议全做，KB 里分文件）
- **[D4] 语言**：KB 英文原文 + 中文问答，还是全中文化？黑话表要不要中英双列？（建议英文原文+双别名+中文黑话表）
- **[D5] 改动仓库的尺度**：只动 `asset/RAG` + `data/`，还是允许改 `src/`（工具、`.fleet` 后缀）？要不要开分支/走 PR 让队友 review？
- **[D6] 交付优先级**：时间不够时先砍哪个？（我的排序：L1/L2 完整性 > L3 读舰队 > 图片识别 > L4 生成）

---

## 附：已完成的验证（本次调研）

- Wikidot 三页实测可达：`/component:list`、`/component:vls-2-launcher`、`/hull:ocello`、`/system:list-all-pages`（21 页索引）。
- 官方 wiki `Components` 两页 403；Wayback 快照完整可读。
- `.fleet` 已解析：1 舰 / 3000 点 / 29 槽 / 含模组弹。
- 本地化 JSON 结构已确认（`HULLCOMPNAME_*` 等键族 + 中文包）。
- 项目侧限制已逐条核对（第 1 节表格，含行号）。

---

## 13. 实装进度（持续更新）

| 阶段 | 状态 | 产物 |
|---|---|---|
| P0 爬虫 + 链路 | ✅ | `domain/tools/fetch_wikidot.py`，3 页索引 / 259 条目录 |
| P1 全站抓取 | ✅ | `domain/kb/raw/` 255 页（0 失败，component 154 / munition 55 / hull 20 / mechanics 15 / glossary 2 / 其他 9） |
| P2 实体化 + 索引 | ✅ | `domain/tools/build_kb.py` → 270 篇 / 13.2 万字；`index_kb.py` → 593 块 / 32.8 s；`check_chunks.py` 自检 |
| P3 人格 + 问答 | ✅ | `domain/persona/Nebulous/`（4 文件）+ `install_persona.py`；system prompt 3593 字；带 `search_knowledge` 的真机问答已通 |
| P4 读舰队 | ✅ 主体完成 | `fleet_report.py`（点数/功率/质量/数量/分工 + **插槽级校验**）＋ `socket_lib.py`／`audit_fit.py`（346 舰队 0 类型冲突）＋ `build_sockets_kb.py`（16 份插槽文档入 KB）；`analyze_fleet` 工具仍待接线 |
| P5 图片 | ⬜ 未开始 | `img2md.py` + `ui/screens.md` |
| P6 评估/提交 | ⬜ 未开始 | 30 条测试集、README、打包 |

**已实测的检索质量**（`index_kb.py --probe-only`，热态 12–36 ms/次）：

| 问题 | Top1 | 分数 |
|---|---|---|
| VLS-2 能装多大的导弹 | `component/vls-2-launcher.md` | 0.692 |
| Ocello 多少点、装甲多厚 | `hull/ocello.md` | 0.703 |
| 近防 PDT 能拦什么 | `component/mk20-defender-pdt.md` | 0.666 |
| Keystone 信号半径 | `hull/keystone.md` | 0.670 |
| 导弹制导方式 | `mechanics/missiles--launching-missiles.md` | 0.519 |
| 「什么是 MMT」 | ✗ 命中 munition，非术语表 | 0.395 |

> 已知待修：① 缩写类问题（MMT/EWar/AOO）召回差 → 需要一篇扁平「术语速查」文档；② 冷启动 2–3 s 会顶到超时 → `rag_timeout_ms` 已从 3000 改到 8000，首次提问前可先点一次「重建索引」预热。

**改动清单（给队友 review）**：

1. `src/dsai4431_chatbot/core/rag/query_terms.py`（+约 40 行，纯增量）：补了插槽类问法（`插槽/槽位/挂载点/射界/朝哪/装得下/装多大/哪个槽`）和编目类问法（`有哪些船/最贵/最便宜/导弹模板`）的中英词表。不改任何已有条目。
2. `data/personality/Nebulous/`（5 个 .md）+ `Nebulous.json`：新增人格，**不动**默认 `FatWhale`。
3. 未改：`tool_router.py`、`chunker.py`、`personas.py`、`attachments.py`、GUI 任何文件。`asset/RAG/` 是运行时 KB（`.gitignore` 已忽略），不进版本库。
4. 如需回滚：`git checkout -- src/dsai4431_chatbot/core/rag/query_terms.py` + 删掉 `data/personality/Nebulous*`。

# gun tug 样板船完整装配 1：TBD（tug blob）

Tags: kind=class assembly; class=gun tug; lang=zh
Keywords: gun tug, 样板船, 完整装配, 整艘照抄, 逐槽, 槽位, 点数, 供电, 弹库, 造舰, 配船, loadout
Summary: gun tug 的一艘 good 样本船的逐槽完整装配（舰体 Draugr Clipper Class）：照抄这张表就能配出同型船，点数、供电余量、弹库装载都按存档实测列出。
Section: build templates; per-slot assembly of one real good sample ship

## 样板船完整装配（整艘照抄）：TBD（tug blob）

**整艘照抄**：舰体 `Tugboat`（阵营键 `Stock/Outlying Systems Protectorate`），存档原值 **280 点**，共 13 个槽位。复制这艘船时连它自带的导弹一起抄，只改船名、呼号和导弹名。

| 槽位 | 部件 | 尺寸 | 点数 | 供电 kW |
|---|---|---|---:|---:|
| MT1 | C53 Cannon | 2x4x2 | 10 | -100 |
| MT2 | T20 Cannon | 3x1x3 | 15 | -30 |
| MT3 | T20 Cannon | 3x1x3 | 15 | -30 |
| MT4 | RF44 'Pinpoint' Radar | 2x1x2 | 10 | -250 |
| CMP1 | Auxiliary Steering | 3x1x3 | 10 | 0 |
| CMP2 | Basic CIC | 4x1x6 | 10 | 0 |
| CMP3 | Rapid DC Locker | 3x1x3 | 10 | 0 |
| CMP4 | Small DC Locker | 3x1x3 | 20 | 0 |
| CMP5 | Reinforced Magazine | 1x1x1 | 0 → 之后 40/座 | 0 |
| MOD1 | BW800-R Drive | 5x3x5 | 20 | 0 |
| MOD2 | Civilian Reactor ⚠ 槽只有 8×3×6 | 5x5x5 | 10 | +3650 |
| MOD3 | Ammunition Elevators | 2x2x2 | 20 | -150 |
| MOD4 | Ammunition Elevators | 2x2x2 | 20 | -150 |

- 合计：部件 170 点 + 舰体 100 点 = **270 点**（不含弹库与弹药，见下）
- 另有弹库 0 点 + 弹药 10 点 ⇒ **全价约 280 点**（估算；游戏里以存档原值 280 为准，单价见 `zh/弹药点数表.md`）
- 供电：发电 3650 kW / 耗电 710 kW（余量 +2940 kW）
- 弹库装载：CMP5 Reinforced Magazine：250mm HE Shell ×100、250mm Bomb Shell ×100、250mm AP Shell ×100、100mm Grapeshot ×500、100mm HE Shell ×250、100mm AP Shell ×250
- ⚠ 存档里这几个槽装的东西比槽位大（旧版本留下的，当前版本装不进去）：MOD2 Civilian Reactor（5x5x5）塞不进 8×3×6。照抄时换小一号的部件，或改用同功能的小件。


# missle FF 样板船完整装配 1：Read（zpzd 导弹FF）

Tags: kind=class assembly; class=missle FF; lang=zh
Keywords: missle FF, 样板船, 完整装配, 整艘照抄, 逐槽, 槽位, 点数, 供电, 弹库, 造舰, 配船, loadout
Summary: missle FF 的一艘 good 样本船的逐槽完整装配（舰体 Raines Frigate Class）：照抄这张表就能配出同型船，点数、供电余量、弹库装载都按存档实测列出。
Section: build templates; per-slot assembly of one real good sample ship

## 样板船完整装配（整艘照抄）：Read（zpzd 导弹FF）

**整艘照抄**：舰体 `Raines Frigate`（阵营键 `Stock/Shelter Alliance`），存档原值 **1000 点**，共 11 个槽位。复制这艘船时连它自带的导弹一起抄，只改船名、呼号和导弹名。

| 槽位 | 部件 | 尺寸 | 点数 | 供电 kW |
|---|---|---|---:|---:|
| MT1 | VLS-1-46 Launcher | 3x2x3 | 5 | -50 |
| MT2 | VLS-2 Launcher | 3x4x3 | 10 | -200 |
| MT3 | VLS-2 Launcher | 3x4x3 | 10 | -200 |
| MT4 | VLS-2 Launcher | 3x4x3 | 10 | -200 |
| CMP1 | Basic CIC | 4x1x6 | 10 | 0 |
| CMP2 | Reinforced Magazine | 1x1x1 | 0 → 之后 40/座 | 0 |
| CMP4 | Rapid DC Locker | 3x1x3 | 10 | 0 |
| MOD1 | FR4800 Reactor | 5x5x5 | 10 | +4200 |
| MOD2 | FM200 Drive | 5x3x5 | 10 | 0 |
| MOD3 | RS35 'Frontline' Radar | 2x2x2 | 10 | -2000 |
| MOD5 | Missile Programming Bus Array | 3x3x3 | 50 | -350 |

- 合计：部件 135 点 + 舰体 125 点 = **260 点**（不含弹库与弹药，见下）
- 另有弹库 0 点 + 弹药 740 点 ⇒ **全价约 1000 点**（估算；游戏里以存档原值 1000 为准，单价见 `zh/弹药点数表.md`）
- 供电：发电 4200 kW / 耗电 3000 kW（余量 +1200 kW）
- 弹库装载：MT1 VLS-1-46 Launcher：SGM-100 占点 ×1、EA12 Chaff Decoy ×11、SGM-100 AMM ×26；MT2 VLS-2 Launcher：SGM-200 补刀 ×12、SGM-200 反小v1 ×4；MT3 VLS-2 Launcher：SGM-H-200 zpzd002 雷达 ×12、SGM-H-200 zpzd002 尾焰 ×12；MT4 VLS-2 Launcher：SGM-H-200 zpzd002 尾焰 ×24


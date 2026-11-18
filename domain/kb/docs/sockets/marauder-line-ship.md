# Marauder Line Ship — section hull (LN)

Tags: kind=hull sockets; hull=Marauder Line Ship; modular=true; sections=3; abbr=LN; save_key=Stock/Bulk Hauler; total=34
Keywords: socket, sockets, mount, mounts, slot, 槽位, 挂载位, 分段, 船段, bow, core, stern, random hull, HullConfig, SegmentConfiguration, 分段组装, Marauder Line Ship, Stock/Bulk Hauler
Summary: Marauder Line Ship (save key `Stock/Bulk Hauler`) is assembled from one bow + one core + one stern: 3 variants per part, 27 combinations, all variants of a part carry the same sockets. Any complete set gives 34 sockets = 17 mount / 9 compartment / 8 module; the `#` of a mount is ship-wide (continuous over the three parts), compartments and modules restart at 1 in each part.
Section: hull sockets;source=game prefab hierarchy + NLHC catalog (segment GUIDs)

## Parts
| Part | # | Letter | Segment GUID | Sockets | Socket table |
|---|---:|---|---|---|---|
| Bow | 1 | `A` | `38e7a28f-1b06-4b73-98ee-f03d1d8a81fe` | 8 / 3 / 3 | sockets/bulk---a---bow.md |
| Bow | 2 | `B` | `29eb9c63-6c47-40f2-8f46-4ed4da8d3386` | 8 / 3 / 3 | sockets/bulk---a---bow.md |
| Bow | 3 | `C` | `c534a876-3f8a-4315-a194-5dda0f84c2b3` | 8 / 3 / 3 | sockets/bulk---a---bow.md |
| Core | 1 | `A` | `d4c9a66d-81e6-49ee-9b33-82d7a1522bbf` | 7 / 6 / 3 | sockets/bulk---a---core.md |
| Core | 2 | `B` | `e2c11e02-b770-495e-a3c2-3dc998eac5a6` | 7 / 6 / 3 | sockets/bulk---a---core.md |
| Core | 3 | `C` | `429f178e-e369-4f51-8054-2e01dd0abea1` | 7 / 6 / 3 | sockets/bulk---a---core.md |
| Stern | 1 | `A` | `78d72a9a-893c-41c6-bddd-f198dfcf77ee` | 2 / 0 / 2 | sockets/bulk---a---stern.md |
| Stern | 2 | `B` | `2f2b451c-4776-405c-9914-cad4764f1072` | 2 / 0 / 2 | sockets/bulk---a---stern.md |
| Stern | 3 | `C` | `a8bf77b9-b7e3-4498-bf91-d3e777a7f688` | 2 / 0 / 2 | sockets/bulk---a---stern.md |

资产树里这些分段 piece 的名字是 `CivBulk - <letter> - <part>`，槽位表在 `hull_sockets.json` 里按 `Bulk - <letter> - <part>` 存 —— 两套名字指的是同一批 prefab。

## Rules (from `zh/fleet文件结构与校验.md`)
- `<HullConfig xsi:type="RandomHullConfiguration">` 里 `<PrimaryStructure>` 必须正好 3 个 `<SegmentConfiguration>`：bow、core、stern。
- `<SecondaryStructure />` 必须存在（哪怕没有舰桥），否则读档崩溃。
- 舰桥最多一个；没有舰桥的船体只会让编辑器图形出问题。
- 左右/上下分段由游戏自动镜像，同一份存档在两边都能读。

## Counting
- 挂载号（`#`）在这条船上是**全船连续**的：三段合起来的 surface 槽位按游戏顺序编号，`Ship Builds.txt` 的 `(mount 1-3)` 用的就是这个号；分段页的 `#` 列已经是全船号，不要按段重数。
- 舱室与模块每段从 1 重新数，所以 `CMP1` 在 bow 和 core 各有一个。

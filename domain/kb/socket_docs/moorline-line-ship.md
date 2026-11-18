# Moorline Line Ship — section hull (CLN)

Tags: kind=hull sockets; hull=Moorline Line Ship; modular=true; sections=3; abbr=CLN; save_key=Stock/Container Hauler; total=26
Keywords: socket, sockets, mount, mounts, slot, 槽位, 挂载位, 分段, 船段, bow, core, stern, random hull, HullConfig, SegmentConfiguration, 分段组装, Moorline Line Ship, Stock/Container Hauler
Summary: Moorline Line Ship (save key `Stock/Container Hauler`) is assembled from one bow + one core + one stern: 3 variants per part, 27 combinations, all variants of a part carry the same sockets. Any complete set gives 26 sockets = 11 mount / 9 compartment / 6 module; the `#` of a mount is ship-wide (continuous over the three parts), compartments and modules restart at 1 in each part.
Section: hull sockets;source=game prefab hierarchy + NLHC catalog (segment GUIDs)

## Parts
| Part | # | Letter | Segment GUID | Sockets | Socket table |
|---|---:|---|---|---|---|
| Bow | 1 | `A` | `2d7c228c-cbd6-425e-9590-a2f8ae8d5915` | 4 / 3 / 2 | sockets/container---a---bow.md |
| Bow | 2 | `B` | `541cf476-4952-4234-a35a-5f1aa9089316` | 4 / 3 / 2 | sockets/container---a---bow.md |
| Bow | 3 | `C` | `bb034299-84c2-456f-b271-c91249cd4375` | 4 / 3 / 2 | sockets/container---a---bow.md |
| Core | 1 | `A` | `18a6bc15-58b0-479c-82c3-1722768f033d` | 5 / 6 / 2 | sockets/container---a---core.md |
| Core | 2 | `B` | `09354e51-953c-451a-b415-3e3361812650` | 5 / 6 / 2 | sockets/container---a---core.md |
| Core | 3 | `C` | `2c68a462-a143-4c89-aea0-df09d4786e92` | 5 / 6 / 2 | sockets/container---a---core.md |
| Stern | 1 | `A` | `674e0528-3e0c-48e4-8e5e-d3a559869104` | 2 / 0 / 2 | sockets/container---a---stern.md |
| Stern | 2 | `B` | `2dbd82fe-d365-4367-aef5-9bb2d3528528` | 2 / 0 / 2 | sockets/container---a---stern.md |
| Stern | 3 | `C` | `aff1eba2-048e-4477-956b-574f4d468f1d` | 2 / 0 / 2 | sockets/container---a---stern.md |

分段 piece 与槽位表同名：`Container - <letter> - <part>`。

## Rules (from `zh/fleet文件结构与校验.md`)
- `<HullConfig xsi:type="RandomHullConfiguration">` 里 `<PrimaryStructure>` 必须正好 3 个 `<SegmentConfiguration>`：bow、core、stern。
- `<SecondaryStructure />` 必须存在（哪怕没有舰桥），否则读档崩溃。
- 舰桥最多一个；没有舰桥的船体只会让编辑器图形出问题。
- 左右/上下分段由游戏自动镜像，同一份存档在两边都能读。

## Counting
- 挂载号（`#`）在这条船上是**全船连续**的：三段合起来的 surface 槽位按游戏顺序编号，`Ship Builds.txt` 的 `(mount 1-3)` 用的就是这个号；分段页的 `#` 列已经是全船号，不要按段重数。
- 舱室与模块每段从 1 重新数，所以 `CMP1` 在 bow 和 core 各有一个。

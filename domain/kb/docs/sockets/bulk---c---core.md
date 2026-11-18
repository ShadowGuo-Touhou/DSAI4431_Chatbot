# Bulk - C - Core — socket map

Tags: kind=hull sockets; hull=Bulk - C - Core; sockets=16; mounts=7; compartments=6; modules=3
Keywords: socket, sockets, mount, mounts, slot, 槽位, 挂载位, 挂载点, 尺寸, 多大, 能装什么, 装得下, Bulk - C - Core
Summary: 16 sockets = 7 mount / 6 compartment / 3 module. The mount / compartment / module number is the one the game counts in (mount 1)/(mount 1-3) conditions — mounts are numbered 1..N across the whole ship, compartments and modules restart at 1 per section (this page is one section, so the mount numbers are ship-wide).
Section: hull sockets;source=game prefab hierarchy (Nebulous stock/stock-f1/stock-f2 bundles)

## How to read this
- `Mount` = a surface mount for a weapon or a sensor.
- `Compartment` = the hull cut-outs that take CIC, damage control, magazines, crew spaces.
- `Module` = internal bays for reactors, drives, radar, jammers, hangars.
- Size is given both in 0.25 m cells and in metres; the volume is the cell product.

## Mounts (7)

| # | Short | Size (cells) | Size (m) | Volume (cells) | Position (m) | Default part |
|---:|---|---|---|---:|---|---|
| 5 | MT5 | 6×10×6 | 1.5×2.5×1.5 m | 360 | 4.29 / 8.65 / -52.186 | - |
| 6 | MT6 | 6×10×6 | 1.5×2.5×1.5 m | 360 | -4.29 / 8.65 / -52.186 | - |
| 7 | MT7 | 6×10×6 | 1.5×2.5×1.5 m | 360 | 4.29 / 8.65 / -46.088 | - |
| 8 | MT8 | 6×10×6 | 1.5×2.5×1.5 m | 360 | -4.29 / 8.65 / -46.088 | - |
| 11 | MT11 | 3×4×3 | 0.75×1×0.75 m | 36 | 0 / 3.16 / -46.44 | - |
| 12 | MT12 | 3×4×3 | 0.75×1×0.75 m | 36 | 4.21 / 10.015 / -49.03 | - |
| 13 | MT13 | 3×4×3 | 0.75×1×0.75 m | 36 | -4.21 / 10.015 / -49.03 | - |

## Compartments (6)

| # | Short | Size (cells) | Size (m) | Volume (cells) | Position (m) | Default part |
|---:|---|---|---|---:|---|---|
| 1 | - | 8×3×8 | 2×0.75×2 m | 192 | 0 / 10.06 / -46.75 | Stock/Basic CIC |
| 2 | - | 8×3×8 | 2×0.75×2 m | 192 | 0 / 10.06 / -51.6 | - |
| 3 | - | 8×1×8 | 2×0.25×2 m | 64 | 0 / 7.57 / -46.75 | - |
| 4 | - | 8×1×8 | 2×0.25×2 m | 64 | 0 / 7.57 / -51.6 | - |
| 5 | - | 8×1×8 | 2×0.25×2 m | 64 | 0 / 7.04 / -46.75 | - |
| 6 | - | 8×1×8 | 2×0.25×2 m | 64 | 0 / 7.04 / -51.6 | - |

## Modules (3)

| # | Short | Size (cells) | Size (m) | Volume (cells) | Position (m) | Default part |
|---:|---|---|---|---:|---|---|
| 1 | - | 3×3×3 | 0.75×0.75×0.75 m | 27 | 0 / 8.77 / -49.47 | Stock/Ithaca Bridgemaster |
| 2 | - | 3×3×3 | 0.75×0.75×0.75 m | 27 | 0 / 7.1 / -49.47 | - |
| 3 | - | 3×3×3 | 0.75×0.75×0.75 m | 27 | 0 / 4.62 / -48.22 | - |

# Ore Carrier — socket map

Tags: kind=hull sockets; hull=Ore Carrier; sockets=17; mounts=3; compartments=8; modules=6
Keywords: socket, sockets, mount, mounts, slot, 槽位, 挂载位, 挂载点, 尺寸, 多大, 能装什么, 装得下, Ore Carrier
Summary: 17 sockets = 3 mount / 8 compartment / 6 module. The mount / compartment / module number is the one the game counts in (mount 1)/(mount 1-3) conditions — mounts are numbered 1..N across the whole ship, compartments and modules restart at 1 per hull.
Section: hull sockets;source=game prefab hierarchy (Nebulous stock/stock-f1/stock-f2 bundles)

## How to read this
- `Mount` = a surface mount for a weapon or a sensor.
- `Compartment` = the hull cut-outs that take CIC, damage control, magazines, crew spaces.
- `Module` = internal bays for reactors, drives, radar, jammers, hangars.
- Size is given both in 0.25 m cells and in metres; the volume is the cell product.

## Mounts (3)

| # | Short | Size (cells) | Size (m) | Volume (cells) | Position (m) | Default part |
|---:|---|---|---|---:|---|---|
| 1 | MT1 | 6×4×6 | 1.5×1×1.5 m | 144 | -0.943 / 1.335 / 0 | - |
| 2 | MT2 | 3×4×5 | 0.75×1×1.25 m | 60 | 0 / 1.72 / -4.517 | - |
| 3 | MT3 | 3×4×5 | 0.75×1×1.25 m | 60 | 0 / -2.34 / -4.517 | - |

## Compartments (8)

| # | Short | Size (cells) | Size (m) | Volume (cells) | Position (m) | Default part |
|---:|---|---|---|---:|---|---|
| 1 | CMP1 | 4×1×6 | 1×0.25×1.5 m | 24 | 0.94 / 2.16 / 0.22 | Stock/Basic CIC |
| 2 | CMP2 | 4×1×6 | 1×0.25×1.5 m | 24 | 0.94 / 1.72 / 0.22 | - |
| 3 | CMP3 | 6×1×8 | 1.5×0.25×2 m | 48 | 1.28 / 1.11 / 0.05 | - |
| 4 | CMP4 | 6×1×8 | 1.5×0.25×2 m | 48 | 1.28 / 0.59 / 0.05 | - |
| 5 | CMP5 | 6×1×8 | 1.5×0.25×2 m | 48 | 1.28 / 0.07 / 0.05 | - |
| 6 | CMP6 | 6×3×8 | 1.5×0.75×2 m | 144 | 1.28 / -0.79 / 0.05 | - |
| 7 | CMP7 | 12×3×12 | 3×0.75×3 m | 432 | 0 / -1.37 / 4.45 | Stock/Bulk Internal Hangar |
| 8 | CMP8 | 12×3×12 | 3×0.75×3 m | 432 | 0 / -1.37 / 8.74 | Stock/Bulk Internal Hangar |

## Modules (6)

| # | Short | Size (cells) | Size (m) | Volume (cells) | Position (m) | Default part |
|---:|---|---|---|---:|---|---|
| 1 | MOD1 | 6×6×6 | 1.5×1.5×1.5 m | 216 | 0 / -0.05 / -2.43 | Stock/Civilian Reactor |
| 2 | MOD2 | 5×10×8 | 1.25×2.5×2 m | 400 | 0 / -0.25 / -4.59 | Stock/BW800 Drive |
| 3 | MOD3 | 3×3×3 | 0.75×0.75×0.75 m | 27 | 0 / 1.38 / -2.52 | - |
| 4 | MOD4 | 3×3×3 | 0.75×0.75×0.75 m | 27 | 0 / -1.66 / -2.52 | - |
| 5 | MOD5 | 2×2×2 | 0.5×0.5×0.5 m | 8 | 0 / 1.49 / -3.48 | Stock/Ithaca Bridgemaster |
| 6 | MOD6 | 2×2×2 | 0.5×0.5×0.5 m | 8 | 0 / -2.05 / -3.48 | - |

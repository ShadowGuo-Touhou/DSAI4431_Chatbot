# Bulk Clipper (today: Flathead Monitor) — socket map

Alias: Bulk Clipper — in-game save key `Stock/Bulk Feeder`; the hull is the modern Flathead Monitor, one prefab, not a segment hull.

Tags: kind=hull sockets; hull=Bulk Clipper; sockets=19; mounts=6; compartments=6; modules=7
Keywords: socket, sockets, mount, mounts, slot, 槽位, 挂载位, 挂载点, 尺寸, 多大, 能装什么, 装得下, Bulk Clipper
Summary: 19 sockets = 6 mount / 6 compartment / 7 module. The mount / compartment / module number is the one the game counts in (mount 1)/(mount 1-3) conditions — mounts are numbered 1..N across the whole ship, compartments and modules restart at 1 per hull.
Section: hull sockets;source=game prefab hierarchy (Nebulous stock/stock-f1/stock-f2 bundles)

## How to read this
- `Mount` = a surface mount for a weapon or a sensor.
- `Compartment` = the hull cut-outs that take CIC, damage control, magazines, crew spaces.
- `Module` = internal bays for reactors, drives, radar, jammers, hangars.
- Size is given both in 0.25 m cells and in metres; the volume is the cell product.

## Mounts (6)

| # | Short | Size (cells) | Size (m) | Volume (cells) | Position (m) | Default part |
|---:|---|---|---|---:|---|---|
| 1 | MT1 | 6×12×6 | 1.5×3×1.5 m | 432 | 0 / 0.036 / 4.702 | - |
| 2 | MT2 | 6×4×6 | 1.5×1×1.5 m | 144 | 0.004 / 1.355 / 2.21 | - |
| 3 | MT3 | 6×4×6 | 1.5×1×1.5 m | 144 | 0.004 / -1.557 / 2.211 | - |
| 4 | MT4 | 3×4×5 | 0.75×1×1.25 m | 60 | 2.346 / 0.006 / 0.295 | - |
| 5 | MT5 | 3×4×5 | 0.75×1×1.25 m | 60 | -2.346 / 0.006 / 0.295 | - |
| 6 | MT6 | 2×2×2 | 0.5×0.5×0.5 m | 8 | 0.727 / 1.62 / -3.393 | - |

## Compartments (6)

| # | Short | Size (cells) | Size (m) | Volume (cells) | Position (m) | Default part |
|---:|---|---|---|---:|---|---|
| 1 | CMP1 | 6×1×8 | 1.5×0.25×2 m | 48 | 0 / 1.04 / -1.92 | Stock/Basic CIC |
| 2 | CMP2 | 6×3×8 | 1.5×0.75×2 m | 144 | 0 / 0.75 / 0.39 | - |
| 3 | CMP3 | 6×1×3 | 1.5×0.25×0.75 m | 18 | 0 / -0.147 / 1.78 | - |
| 4 | CMP4 | 6×1×3 | 1.5×0.25×0.75 m | 18 | 0 / -0.147 / 0.45 | - |
| 5 | CMP5 | 6×3×8 | 1.5×0.75×2 m | 144 | 0 / -1.01 / 0.39 | - |
| 6 | CMP6 | 6×3×8 | 1.5×0.75×2 m | 144 | 0 / -1.39 / -1.92 | - |

## Modules (7)

| # | Short | Size (cells) | Size (m) | Volume (cells) | Position (m) | Default part |
|---:|---|---|---|---:|---|---|
| 1 | MOD1 | 6×6×6 | 1.5×1.5×1.5 m | 216 | 0 / -0.05 / -1.58 | Stock/Civilian Reactor |
| 2 | MOD2 | 10×5×8 | 2.5×1.25×2 m | 400 | 0 / 0 / -4.13 | Stock/BW800 Drive |
| 3 | MOD3 | 3×3×3 | 0.75×0.75×0.75 m | 27 | 1.25 / -0.618 / 2.649 | - |
| 4 | MOD4 | 3×3×3 | 0.75×0.75×0.75 m | 27 | -1.25 / -0.618 / 2.649 | - |
| 5 | MOD5 | 3×3×3 | 0.75×0.75×0.75 m | 27 | 0 / 0.387 / 2.649 | - |
| 6 | MOD6 | 2×2×2 | 0.5×0.5×0.5 m | 8 | 0 / 1.15 / -3.35 | Stock/Ithaca Bridgemaster |
| 7 | MOD7 | 2×2×2 | 0.5×0.5×0.5 m | 8 | 0 / -1.07 / -3.35 | - |

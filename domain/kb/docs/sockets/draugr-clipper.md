# Tug Clipper (today: Draugr Clipper) — socket map

Alias: Tug Clipper — in-game save key `Stock/Tugboat`; the hull is the modern Draugr Clipper, one prefab, not a segment hull.

Tags: kind=hull sockets; hull=Tug Clipper; sockets=14; mounts=5; compartments=5; modules=4
Keywords: socket, sockets, mount, mounts, slot, 槽位, 挂载位, 挂载点, 尺寸, 多大, 能装什么, 装得下, Tug Clipper
Summary: 14 sockets = 5 mount / 5 compartment / 4 module. The mount / compartment / module number is the one the game counts in (mount 1)/(mount 1-3) conditions — mounts are numbered 1..N across the whole ship, compartments and modules restart at 1 per hull.
Section: hull sockets;source=game prefab hierarchy (Nebulous stock/stock-f1/stock-f2 bundles)

## How to read this
- `Mount` = a surface mount for a weapon or a sensor.
- `Compartment` = the hull cut-outs that take CIC, damage control, magazines, crew spaces.
- `Module` = internal bays for reactors, drives, radar, jammers, hangars.
- Size is given both in 0.25 m cells and in metres; the volume is the cell product.

## Mounts (5)

| # | Short | Size (cells) | Size (m) | Volume (cells) | Position (m) | Default part |
|---:|---|---|---|---:|---|---|
| 1 | MT1 | 2×5×2 | 0.5×1.25×0.5 m | 20 | 0 / 0.162 / 3.961 | - |
| 2 | MT2 | 3×4×5 | 0.75×1×1.25 m | 60 | -0.299 / 1.095 / 2.34 | - |
| 3 | MT3 | 3×2×5 | 0.75×0.5×1.25 m | 30 | 0 / -1.162 / 1.145 | - |
| 4 | MT4 | 2×2×2 | 0.5×0.5×0.5 m | 8 | 2.438 / 0.269 / -0.733 | - |
| 5 | MT5 | 2×2×2 | 0.5×0.5×0.5 m | 8 | -2.438 / 0.269 / -0.733 | - |

## Compartments (5)

| # | Short | Size (cells) | Size (m) | Volume (cells) | Position (m) | Default part |
|---:|---|---|---|---:|---|---|
| 1 | CMP1 | 4×1×6 | 1×0.25×1.5 m | 24 | 0 / 0.297 / 1.143 | Stock/Basic CIC |
| 2 | CMP2 | 4×1×6 | 1×0.25×1.5 m | 24 | 0 / -0.147 / 1.143 | - |
| 3 | CMP3 | 3×1×3 | 0.75×0.25×0.75 m | 9 | 0 / 1.431 / -0.24 | - |
| 4 | CMP4 | 3×1×3 | 0.75×0.25×0.75 m | 9 | 0 / 1.431 / -1.082 | - |
| 5 | CMP5 | 4×1×6 | 1×0.25×1.5 m | 24 | 0 / -0.584 / 1.143 | - |

## Modules (4)

| # | Short | Size (cells) | Size (m) | Volume (cells) | Position (m) | Default part |
|---:|---|---|---|---:|---|---|
| 1 | MOD1 | 6×6×6 | 1.5×1.5×1.5 m | 216 | 0 / -0.36 / -0.882 | Stock/Civilian Reactor |
| 2 | MOD2 | 8×3×6 | 2×0.75×1.5 m | 144 | 0 / 0.26 / -2.511 | Stock/BW800 Drive |
| 3 | MOD3 | 2×2×2 | 0.5×0.5×0.5 m | 8 | 0.5 / 0.83 / 0.42 | Stock/Ithaca Bridgemaster |
| 4 | MOD4 | 2×2×2 | 0.5×0.5×0.5 m | 8 | -0.5 / 0.83 / 0.42 | - |

# Shuttle Clipper (today: Ferryman Clipper) — socket map

Alias: Shuttle Clipper — in-game save key `Stock/Shuttle`; the hull is the modern Ferryman Clipper, one prefab, not a segment hull.

Tags: kind=hull sockets; hull=Shuttle Clipper; sockets=10; mounts=3; compartments=3; modules=4
Keywords: socket, sockets, mount, mounts, slot, 槽位, 挂载位, 挂载点, 尺寸, 多大, 能装什么, 装得下, Shuttle Clipper
Summary: 10 sockets = 3 mount / 3 compartment / 4 module. The mount / compartment / module number is the one the game counts in (mount 1)/(mount 1-3) conditions — mounts are numbered 1..N across the whole ship, compartments and modules restart at 1 per hull.
Section: hull sockets;source=game prefab hierarchy (Nebulous stock/stock-f1/stock-f2 bundles)

## How to read this
- `Mount` = a surface mount for a weapon or a sensor.
- `Compartment` = the hull cut-outs that take CIC, damage control, magazines, crew spaces.
- `Module` = internal bays for reactors, drives, radar, jammers, hangars.
- Size is given both in 0.25 m cells and in metres; the volume is the cell product.

## Mounts (3)

| # | Short | Size (cells) | Size (m) | Volume (cells) | Position (m) | Default part |
|---:|---|---|---|---:|---|---|
| 1 | MT1 | 3×2×3 | 0.75×0.5×0.75 m | 18 | 0 / 0.499 / 0.832 | - |
| 2 | MT2 | 3×2×3 | 0.75×0.5×0.75 m | 18 | 0 / -0.687 / 0.313 | - |
| 3 | MT3 | 2×2×2 | 0.5×0.5×0.5 m | 8 | -0.398 / 0.948 / -0.698 | - |

## Compartments (3)

| # | Short | Size (cells) | Size (m) | Volume (cells) | Position (m) | Default part |
|---:|---|---|---|---:|---|---|
| 1 | CMP1 | 4×1×6 | 1×0.25×1.5 m | 24 | 0 / -0.27 / 1.143 | Stock/Basic CIC |
| 2 | CMP2 | 3×1×3 | 0.75×0.25×0.75 m | 9 | 0 / 0.101 / 1.577 | - |
| 3 | CMP3 | 3×1×3 | 0.75×0.25×0.75 m | 9 | 0 / 0.101 / 0.735 | - |

## Modules (4)

| # | Short | Size (cells) | Size (m) | Volume (cells) | Position (m) | Default part |
|---:|---|---|---|---:|---|---|
| 1 | MOD1 | 3×3×3 | 0.75×0.75×0.75 m | 27 | 0 / -0.002 / -0.235 | Stock/Light Civilian Reactor |
| 2 | MOD2 | 8×3×6 | 2×0.75×1.5 m | 144 | 0 / 0.043 / -1.434 | Stock/BW800 Drive |
| 3 | MOD3 | 2×2×2 | 0.5×0.5×0.5 m | 8 | 0.5 / 0.011 / 2.44 | Stock/Ithaca Bridgemaster |
| 4 | MOD4 | 2×2×2 | 0.5×0.5×0.5 m | 8 | -0.5 / 0.011 / 2.44 | - |

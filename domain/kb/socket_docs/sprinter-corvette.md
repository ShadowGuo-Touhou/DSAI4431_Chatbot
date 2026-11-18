# Sprinter Corvette — socket map

Tags: kind=hull sockets; hull=Sprinter Corvette; sockets=12; mounts=4; compartments=4; modules=4
Keywords: socket, sockets, mount, mounts, slot, 槽位, 挂载位, 挂载点, 尺寸, 多大, 能装什么, 装得下, Sprinter Corvette
Summary: 12 sockets = 4 mount / 4 compartment / 4 module. The mount / compartment / module number is the one the game counts in (mount 1)/(mount 1-3) conditions — mounts are numbered 1..N across the whole ship, compartments and modules restart at 1 per hull.
Section: hull sockets;source=game prefab hierarchy (Nebulous stock/stock-f1/stock-f2 bundles)

## How to read this
- `Mount` = a surface mount for a weapon or a sensor.
- `Compartment` = the hull cut-outs that take CIC, damage control, magazines, crew spaces.
- `Module` = internal bays for reactors, drives, radar, jammers, hangars.
- Size is given both in 0.25 m cells and in metres; the volume is the cell product.

## Mounts (4)

| # | Short | Size (cells) | Size (m) | Volume (cells) | Position (m) | Default part |
|---:|---|---|---|---:|---|---|
| 1 | MT1 | 3×4×5 | 0.75×1×1.25 m | 60 | 0 / -0.9 / -0.361 | - |
| 2 | MT2 | 3×2×3 | 0.75×0.5×0.75 m | 18 | 0 / -0.547 / 3.204 | - |
| 3 | MT3 | 2×2×2 | 0.5×0.5×0.5 m | 8 | 1.642 / -0.139 / -0.294 | - |
| 4 | MT4 | 2×2×2 | 0.5×0.5×0.5 m | 8 | -1.636 / -0.139 / -0.294 | - |

## Compartments (4)

| # | Short | Size (cells) | Size (m) | Volume (cells) | Position (m) | Default part |
|---:|---|---|---|---:|---|---|
| 1 | CMP1 | 4×1×6 | 1×0.25×1.5 m | 24 | 0 / -0.453 / 1.628 | Stock/Basic CIC |
| 2 | CMP2 | 4×1×6 | 1×0.25×1.5 m | 24 | 0 / -0.083 / 1.628 | - |
| 3 | CMP3 | 3×1×3 | 0.75×0.25×0.75 m | 9 | 0 / 0.29 / 2.062 | - |
| 4 | CMP4 | 3×1×3 | 0.75×0.25×0.75 m | 9 | 0 / 0.29 / 1.22 | - |

## Modules (4)

| # | Short | Size (cells) | Size (m) | Volume (cells) | Position (m) | Default part |
|---:|---|---|---|---:|---|---|
| 1 | MOD1 | 3×3×3 | 0.75×0.75×0.75 m | 27 | 0 / 0.084 / -0.979 | Stock/FR3300 Micro Reactor |
| 2 | MOD2 | 8×3×6 | 2×0.75×1.5 m | 144 | 0 / -0.07 / -2.452 | Stock/FM200 Drive |
| 3 | MOD3 | 2×2×2 | 0.5×0.5×0.5 m | 8 | 0.44 / 0.011 / 0.389 | Stock/RS35 'Frontline' Radar |
| 4 | MOD4 | 2×2×2 | 0.5×0.5×0.5 m | 8 | -0.44 / 0.011 / 0.389 | - |

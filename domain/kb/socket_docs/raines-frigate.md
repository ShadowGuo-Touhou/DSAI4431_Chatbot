# Raines Frigate — socket map

Tags: kind=hull sockets; hull=Raines Frigate; sockets=14; mounts=4; compartments=5; modules=5
Keywords: socket, sockets, mount, mounts, slot, 槽位, 挂载位, 挂载点, 尺寸, 多大, 能装什么, 装得下, Raines Frigate
Summary: 14 sockets = 4 mount / 5 compartment / 5 module. The mount / compartment / module number is the one the game counts in (mount 1)/(mount 1-3) conditions — mounts are numbered 1..N across the whole ship, compartments and modules restart at 1 per hull.
Section: hull sockets;source=game prefab hierarchy (Nebulous stock/stock-f1/stock-f2 bundles)

## How to read this
- `Mount` = a surface mount for a weapon or a sensor.
- `Compartment` = the hull cut-outs that take CIC, damage control, magazines, crew spaces.
- `Module` = internal bays for reactors, drives, radar, jammers, hangars.
- Size is given both in 0.25 m cells and in metres; the volume is the cell product.

## Mounts (4)

| # | Short | Size (cells) | Size (m) | Volume (cells) | Position (m) | Default part |
|---:|---|---|---|---:|---|---|
| 1 | MT1 | 3×4×3 | 0.75×1×0.75 m | 36 | 0 / 1.6 / -0.967 | - |
| 2 | MT2 | 3×4×3 | 0.75×1×0.75 m | 36 | 0 / -1.48 / -0.967 | - |
| 3 | MT3 | 3×4×5 | 0.75×1×1.25 m | 60 | 0 / 1.39 / 1.207 | - |
| 4 | MT4 | 3×4×5 | 0.75×1×1.25 m | 60 | 0 / -1.37 / 1.207 | - |

## Compartments (5)

| # | Short | Size (cells) | Size (m) | Volume (cells) | Position (m) | Default part |
|---:|---|---|---|---:|---|---|
| 1 | CMP1 | 4×1×6 | 1×0.25×1.5 m | 24 | 0 / -0.36 / 1.06 | Stock/Basic CIC |
| 2 | CMP2 | 4×1×6 | 1×0.25×1.5 m | 24 | 0 / 0 / 1.06 | - |
| 3 | CMP3 | 3×1×3 | 0.75×0.25×0.75 m | 9 | 0 / 0.39 / 0.72 | - |
| 4 | CMP4 | 3×1×3 | 0.75×0.25×0.75 m | 9 | 0 / 0.59 / 3.2 | - |
| 5 | CMP5 | 4×1×6 | 1×0.25×1.5 m | 24 | 0 / 0.26 / 3.2 | - |

## Modules (5)

| # | Short | Size (cells) | Size (m) | Volume (cells) | Position (m) | Default part |
|---:|---|---|---|---:|---|---|
| 1 | MOD1 | 6×6×6 | 1.5×1.5×1.5 m | 216 | 0 / 0 / -0.71 | Stock/FR4800 Reactor |
| 2 | MOD2 | 8×3×6 | 2×0.75×1.5 m | 144 | 0 / 0 / -2.35 | Stock/FM200 Drive |
| 3 | MOD3 | 2×2×2 | 0.5×0.5×0.5 m | 8 | 0 / 1.21 / 0.18 | Stock/RS35 'Frontline' Radar |
| 4 | MOD4 | 2×2×2 | 0.5×0.5×0.5 m | 8 | 0 / -1.21 / 0.18 | - |
| 5 | MOD5 | 3×3×3 | 0.75×0.75×0.75 m | 27 | 0 / -0.61 / 3.25 | - |

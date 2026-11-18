# Mercator Oiler — socket map

Tags: kind=hull sockets; hull=Mercator Oiler; sockets=15; mounts=3; compartments=8; modules=4
Keywords: socket, sockets, mount, mounts, slot, 槽位, 挂载位, 挂载点, 尺寸, 多大, 能装什么, 装得下, Mercator Oiler
Summary: 15 sockets = 3 mount / 8 compartment / 4 module. The mount / compartment / module number is the one the game counts in (mount 1)/(mount 1-3) conditions — mounts are numbered 1..N across the whole ship, compartments and modules restart at 1 per hull.
Section: hull sockets;source=game prefab hierarchy (Nebulous stock/stock-f1/stock-f2 bundles)

## How to read this
- `Mount` = a surface mount for a weapon or a sensor.
- `Compartment` = the hull cut-outs that take CIC, damage control, magazines, crew spaces.
- `Module` = internal bays for reactors, drives, radar, jammers, hangars.
- Size is given both in 0.25 m cells and in metres; the volume is the cell product.

## Mounts (3)

| # | Short | Size (cells) | Size (m) | Volume (cells) | Position (m) | Default part |
|---:|---|---|---|---:|---|---|
| 1 | MT1 | 2×2×2 | 0.5×0.5×0.5 m | 8 | -0.893 / 5.575 / -1.175 | - |
| 2 | MT2 | 2×2×2 | 0.5×0.5×0.5 m | 8 | 0 / -3.062 / 9.156 | - |
| 3 | MT3 | 3×4×3 | 0.75×1×0.75 m | 36 | -0.003 / -3.732 / -4.55 | - |

## Compartments (8)

| # | Short | Size (cells) | Size (m) | Volume (cells) | Position (m) | Default part |
|---:|---|---|---|---:|---|---|
| 1 | CMP1 | 6×1×8 | 1.5×0.25×2 m | 48 | 0 / 3.56 / 10.5 | Stock/Basic CIC |
| 2 | CMP2 | 6×1×8 | 1.5×0.25×2 m | 48 | 0 / 2.96 / 10.5 | - |
| 3 | CMP3 | 6×1×8 | 1.5×0.25×2 m | 48 | 0 / 4.35 / -2.38 | - |
| 4 | CMP4 | 6×1×8 | 1.5×0.25×2 m | 48 | 0 / 3.65 / -2.38 | - |
| 5 | CMP5 | 8×3×15 | 2×0.75×3.75 m | 360 | 0 / 0.54 / 5.11 | Stock/Reinforced Magazine |
| 6 | CMP6 | 8×3×15 | 2×0.75×3.75 m | 360 | 0 / -1.39 / 5.11 | Stock/Reinforced Magazine |
| 7 | CMP7 | 8×3×15 | 2×0.75×3.75 m | 360 | 0 / 0.54 / -0.64 | Stock/Reinforced Magazine |
| 8 | CMP8 | 8×3×15 | 2×0.75×3.75 m | 360 | 0 / -1.39 / -0.64 | Stock/Reinforced Magazine |

## Modules (4)

| # | Short | Size (cells) | Size (m) | Volume (cells) | Position (m) | Default part |
|---:|---|---|---|---:|---|---|
| 1 | MOD1 | 8×8×8 | 2×2×2 m | 512 | 0 / -0.25 / -6.19 | Stock/FR4800 Reactor |
| 2 | MOD2 | 12×8×10 | 3×2×2.5 m | 960 | 0 / -0.25 / -9.13 | Stock/FM500 Drive |
| 3 | MOD3 | 3×3×3 | 0.75×0.75×0.75 m | 27 | 0 / 0.26 / 9.67 | Stock/RS35 'Frontline' Radar |
| 4 | MOD4 | 3×3×3 | 0.75×0.75×0.75 m | 27 | 0 / -1.21 / 9.67 | - |

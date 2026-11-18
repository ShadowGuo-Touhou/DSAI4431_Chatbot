# Keystone Destroyer — socket map

Tags: kind=hull sockets; hull=Keystone Destroyer; sockets=21; mounts=7; compartments=7; modules=7
Keywords: socket, sockets, mount, mounts, slot, 槽位, 挂载位, 挂载点, 尺寸, 多大, 能装什么, 装得下, Keystone Destroyer
Summary: 21 sockets = 7 mount / 7 compartment / 7 module. The mount / compartment / module number is the one the game counts in (mount 1)/(mount 1-3) conditions — mounts are numbered 1..N across the whole ship, compartments and modules restart at 1 per hull.
Section: hull sockets;source=game prefab hierarchy (Nebulous stock/stock-f1/stock-f2 bundles)

## How to read this
- `Mount` = a surface mount for a weapon or a sensor.
- `Compartment` = the hull cut-outs that take CIC, damage control, magazines, crew spaces.
- `Module` = internal bays for reactors, drives, radar, jammers, hangars.
- Size is given both in 0.25 m cells and in metres; the volume is the cell product.

## Mounts (7)

| # | Short | Size (cells) | Size (m) | Volume (cells) | Position (m) | Default part |
|---:|---|---|---|---:|---|---|
| 1 | MT1 | 3×4×5 | 0.75×1×1.25 m | 60 | 0 / 1.82 / 0.12 | - |
| 2 | MT2 | 3×4×5 | 0.75×1×1.25 m | 60 | 0 / -1.82 / 0.12 | - |
| 3 | MT3 | 3×4×3 | 0.75×1×0.75 m | 36 | -2.07 / -0.197 / -2.235 | - |
| 4 | MT4 | 3×4×3 | 0.75×1×0.75 m | 36 | 2.07 / -0.197 / -2.235 | - |
| 5 | MT5 | 2×2×2 | 0.5×0.5×0.5 m | 8 | 0 / 1.763 / -4.394 | - |
| 6 | MT6 | 2×2×2 | 0.5×0.5×0.5 m | 8 | 0 / -1.756 / 2.623 | - |
| 7 | MT7 | 4×12×4 | 1×3×1 m | 192 | 0 / 0 / 5.47 | - |

## Compartments (7)

| # | Short | Size (cells) | Size (m) | Volume (cells) | Position (m) | Default part |
|---:|---|---|---|---:|---|---|
| 1 | CMP1 | 6×1×8 | 1.5×0.25×2 m | 48 | 0 / -0.36 / 1.26 | Stock/Basic CIC |
| 2 | CMP2 | 6×1×8 | 1.5×0.25×2 m | 48 | 0 / 0.24 / 1.26 | - |
| 3 | CMP3 | 6×1×4 | 1.5×0.25×1 m | 24 | 0 / 0.83 / 0.42 | - |
| 4 | CMP4 | 6×1×4 | 1.5×0.25×1 m | 24 | 0 / 0.83 / 1.72 | - |
| 5 | CMP5 | 6×1×4 | 1.5×0.25×1 m | 24 | 0 / 0.83 / 3.04 | - |
| 6 | CMP6 | 6×1×4 | 1.5×0.25×1 m | 24 | 0 / 0.83 / 4.32 | - |
| 7 | CMP7 | 6×1×4 | 1.5×0.25×1 m | 24 | 0 / -0.99 / 3.06 | - |

## Modules (7)

| # | Short | Size (cells) | Size (m) | Volume (cells) | Position (m) | Default part |
|---:|---|---|---|---:|---|---|
| 1 | MOD1 | 6×6×6 | 1.5×1.5×1.5 m | 216 | 0 / -0.01 / -1.06 | Stock/FR4800 Reactor |
| 2 | MOD2 | 8×8×6 | 2×2×1.5 m | 384 | 0 / 0 / -4.28 | Stock/FM200 Drive |
| 3 | MOD3 | 3×3×3 | 0.75×0.75×0.75 m | 27 | 0 / 0.89 / -2.66 | - |
| 4 | MOD4 | 3×3×3 | 0.75×0.75×0.75 m | 27 | 0 / -0.99 / -2.66 | - |
| 5 | MOD5 | 2×2×2 | 0.5×0.5×0.5 m | 8 | 0 / -1.25 / 1.15 | Stock/RS35 'Frontline' Radar |
| 6 | MOD6 | 2×2×2 | 0.5×0.5×0.5 m | 8 | 0 / -1.25 / 1.82 | - |
| 7 | MOD7 | 3×3×3 | 0.75×0.75×0.75 m | 27 | 0 / 1.46 / -1.37 | - |

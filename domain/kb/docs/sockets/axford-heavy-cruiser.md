# Axford Heavy Cruiser — socket map

Tags: kind=hull sockets; hull=Axford Heavy Cruiser; sockets=34; mounts=11; compartments=11; modules=12
Keywords: socket, sockets, mount, mounts, slot, 槽位, 挂载位, 挂载点, 尺寸, 多大, 能装什么, 装得下, Axford Heavy Cruiser
Summary: 34 sockets = 11 mount / 11 compartment / 12 module. The mount / compartment / module number is the one the game counts in (mount 1)/(mount 1-3) conditions — mounts are numbered 1..N across the whole ship, compartments and modules restart at 1 per hull.
Section: hull sockets;source=game prefab hierarchy (Nebulous stock/stock-f1/stock-f2 bundles)

## How to read this
- `Mount` = a surface mount for a weapon or a sensor.
- `Compartment` = the hull cut-outs that take CIC, damage control, magazines, crew spaces.
- `Module` = internal bays for reactors, drives, radar, jammers, hangars.
- Size is given both in 0.25 m cells and in metres; the volume is the cell product.

## Mounts (11)

| # | Short | Size (cells) | Size (m) | Volume (cells) | Position (m) | Default part |
|---:|---|---|---|---:|---|---|
| 1 | MT1 | 6×4×6 | 1.5×1×1.5 m | 144 | 0 / 1.949 / 2.71 | - |
| 2 | MT2 | 6×4×6 | 1.5×1×1.5 m | 144 | 0 / 1.742 / -4.93 | - |
| 3 | MT3 | 8×7×8 | 2×1.75×2 m | 448 | 0 / -2.494 / 2.14 | - |
| 4 | MT4 | 3×4×3 | 0.75×1×0.75 m | 36 | -1.735 / -0.081 / 2.376 | - |
| 5 | MT5 | 3×4×3 | 0.75×1×0.75 m | 36 | -3.047 / -0.08 / -1.703 | - |
| 6 | MT6 | 3×4×3 | 0.75×1×0.75 m | 36 | 1.735 / -0.081 / 2.376 | - |
| 7 | MT7 | 3×4×3 | 0.75×1×0.75 m | 36 | 3.047 / -0.08 / -1.703 | - |
| 8 | MT8 | 2×2×2 | 0.5×0.5×0.5 m | 8 | 0 / 1.61 / 7.86 | - |
| 9 | MT9 | 2×2×2 | 0.5×0.5×0.5 m | 8 | 0 / -2.459 / -3.162 | - |
| 10 | MT10 | 2×2×2 | 0.5×0.5×0.5 m | 8 | -1.554 / 1.61 / -1.67 | - |
| 11 | MT11 | 2×2×2 | 0.5×0.5×0.5 m | 8 | 1.554 / 1.61 / -1.67 | - |

## Compartments (11)

| # | Short | Size (cells) | Size (m) | Volume (cells) | Position (m) | Default part |
|---:|---|---|---|---:|---|---|
| 1 | CMP1 | 6×1×8 | 1.5×0.25×2 m | 48 | 0 / -0.36 / 0.77 | Stock/Basic CIC |
| 2 | CMP2 | 6×1×8 | 1.5×0.25×2 m | 48 | 0 / 0.26 / 0.77 | - |
| 3 | CMP3 | 6×1×8 | 1.5×0.25×2 m | 48 | 0 / 0.77 / 0.77 | - |
| 4 | CMP4 | 6×1×8 | 1.5×0.25×2 m | 48 | 0 / -1.41 / -0.8 | - |
| 5 | CMP5 | 6×1×4 | 1.5×0.25×1 m | 24 | 0 / -1.95 / -1.46 | - |
| 6 | CMP6 | 6×1×4 | 1.5×0.25×1 m | 24 | 0 / -1.95 / -0.12 | - |
| 7 | CMP7 | 4×1×6 | 1×0.25×1.5 m | 24 | 0 / 1.31 / 0.02 | - |
| 8 | CMP8 | 6×1×6 | 1.5×0.25×1.5 m | 36 | 0 / 1.31 / 4.51 | - |
| 9 | CMP9 | 6×1×6 | 1.5×0.25×1.5 m | 36 | 0 / 0.81 / 4.51 | - |
| 10 | CMP10 | 6×1×8 | 1.5×0.25×2 m | 48 | 0 / 0.23 / 4.76 | - |
| 11 | CMP11 | 4×1×6 | 1×0.25×1.5 m | 24 | 0 / 3.25 / -0.85 | - |

## Modules (12)

| # | Short | Size (cells) | Size (m) | Volume (cells) | Position (m) | Default part |
|---:|---|---|---|---:|---|---|
| 1 | MOD1 | 6×6×6 | 1.5×1.5×1.5 m | 216 | 0 / 0.92 / -3.17 | Stock/FR4800 Reactor |
| 2 | MOD2 | 6×6×6 | 1.5×1.5×1.5 m | 216 | 0 / -0.99 / -3.17 | - |
| 3 | MOD3 | 12×8×10 | 3×2×2.5 m | 960 | 0 / 0 / -6.37 | Stock/FM500 Drive |
| 4 | MOD4 | 3×3×3 | 0.75×0.75×0.75 m | 27 | 1.9 / -0.06 / -2.54 | - |
| 5 | MOD5 | 3×3×3 | 0.75×0.75×0.75 m | 27 | 1.9 / -0.06 / -0.78 | - |
| 6 | MOD6 | 3×3×3 | 0.75×0.75×0.75 m | 27 | -1.9 / -0.06 / -2.54 | - |
| 7 | MOD7 | 3×3×3 | 0.75×0.75×0.75 m | 27 | -1.9 / -0.06 / -0.78 | - |
| 8 | MOD8 | 2×2×2 | 0.5×0.5×0.5 m | 8 | 0 / -0.81 / 3.75 | - |
| 9 | MOD9 | 2×2×2 | 0.5×0.5×0.5 m | 8 | 0 / -0.81 / 4.8 | - |
| 10 | MOD10 | 2×2×2 | 0.5×0.5×0.5 m | 8 | 0 / -0.81 / 5.89 | - |
| 11 | MOD11 | 2×2×2 | 0.5×0.5×0.5 m | 8 | 0 / 2.58 / -1.69 | Stock/RS35 'Frontline' Radar |
| 12 | MOD12 | 2×2×2 | 0.5×0.5×0.5 m | 8 | 0 / 2.58 / -0.64 | - |

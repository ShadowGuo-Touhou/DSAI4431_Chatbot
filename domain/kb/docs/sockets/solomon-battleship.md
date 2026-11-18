# Solomon Battleship — socket map

Tags: kind=hull sockets; hull=Solomon Battleship; sockets=45; mounts=14; compartments=16; modules=15
Keywords: socket, sockets, mount, mounts, slot, 槽位, 挂载位, 挂载点, 尺寸, 多大, 能装什么, 装得下, Solomon Battleship
Summary: 45 sockets = 14 mount / 16 compartment / 15 module. The mount / compartment / module number is the one the game counts in (mount 1)/(mount 1-3) conditions — mounts are numbered 1..N across the whole ship, compartments and modules restart at 1 per hull.
Section: hull sockets;source=game prefab hierarchy (Nebulous stock/stock-f1/stock-f2 bundles)

## How to read this
- `Mount` = a surface mount for a weapon or a sensor.
- `Compartment` = the hull cut-outs that take CIC, damage control, magazines, crew spaces.
- `Module` = internal bays for reactors, drives, radar, jammers, hangars.
- Size is given both in 0.25 m cells and in metres; the volume is the cell product.

## Mounts (14)

| # | Short | Size (cells) | Size (m) | Volume (cells) | Position (m) | Default part |
|---:|---|---|---|---:|---|---|
| 1 | MT1 | 8×7×8 | 2×1.75×2 m | 448 | 0 / 0.956 / 6.434 | - |
| 2 | MT2 | 6×4×6 | 1.5×1×1.5 m | 144 | 0 / 1.943 / 3.37 | - |
| 3 | MT3 | 8×7×8 | 2×1.75×2 m | 448 | 0 / 1.825 / -6.642 | - |
| 4 | MT4 | 8×7×8 | 2×1.75×2 m | 448 | 0 / -4.44 / -0.312 | - |
| 5 | MT5 | 3×4×3 | 0.75×1×0.75 m | 36 | -1.79 / -1.149 / 5.272 | - |
| 6 | MT6 | 3×4×3 | 0.75×1×0.75 m | 36 | -2.24 / -0.433 / -0.426 | - |
| 7 | MT7 | 3×4×3 | 0.75×1×0.75 m | 36 | -2.284 / -1.841 / -0.426 | - |
| 8 | MT8 | 2×2×2 | 0.5×0.5×0.5 m | 8 | -3.826 / -1.091 / -10.118 | - |
| 9 | MT9 | 3×4×3 | 0.75×1×0.75 m | 36 | 1.79 / -1.149 / 5.272 | - |
| 10 | MT10 | 3×4×3 | 0.75×1×0.75 m | 36 | 2.24 / -0.433 / -0.426 | - |
| 11 | MT11 | 3×4×3 | 0.75×1×0.75 m | 36 | 2.284 / -1.841 / -0.426 | - |
| 12 | MT12 | 2×2×2 | 0.5×0.5×0.5 m | 8 | 3.826 / -1.091 / -10.118 | - |
| 13 | MT13 | 2×2×2 | 0.5×0.5×0.5 m | 8 | -0.024 / 0.955 / 10.011 | - |
| 14 | MT14 | 2×2×2 | 0.5×0.5×0.5 m | 8 | -0.024 / -4.424 / 3.674 | - |

## Compartments (16)

| # | Short | Size (cells) | Size (m) | Volume (cells) | Position (m) | Default part |
|---:|---|---|---|---:|---|---|
| 1 | CMP1 | 6×1×8 | 1.5×0.25×2 m | 48 | 0 / -0.98 / -0.36 | Stock/Basic CIC |
| 2 | CMP2 | 6×1×8 | 1.5×0.25×2 m | 48 | 0 / 0.76 / -0.36 | - |
| 3 | CMP3 | 6×1×8 | 1.5×0.25×2 m | 48 | 0 / 1.52 / -0.36 | - |
| 4 | CMP4 | 6×1×4 | 1.5×0.25×1 m | 24 | 0 / -1.76 / -2.64 | - |
| 5 | CMP5 | 6×1×4 | 1.5×0.25×1 m | 24 | 0 / -1.76 / -0.36 | - |
| 6 | CMP6 | 6×1×4 | 1.5×0.25×1 m | 24 | 0 / -1.76 / 1.61 | - |
| 7 | CMP7 | 6×1×4 | 1.5×0.25×1 m | 24 | 0 / -0.91 / -2.64 | - |
| 8 | CMP8 | 6×1×4 | 1.5×0.25×1 m | 24 | 0 / -0.91 / 1.61 | - |
| 9 | CMP9 | 6×1×8 | 1.5×0.25×2 m | 48 | 0 / 3.24 / 0.35 | - |
| 10 | CMP10 | 6×1×4 | 1.5×0.25×1 m | 24 | 0 / 2.5 / -0.29 | - |
| 11 | CMP11 | 6×1×4 | 1.5×0.25×1 m | 24 | 0 / 2.5 / 1.05 | - |
| 12 | CMP12 | 6×1×8 | 1.5×0.25×2 m | 48 | 0 / 0.59 / 2.8 | - |
| 13 | CMP13 | 6×1×8 | 1.5×0.25×2 m | 48 | 0 / -1.16 / 3.85 | - |
| 14 | CMP14 | 6×1×8 | 1.5×0.25×2 m | 48 | 0 / -2.72 / 2.74 | - |
| 15 | CMP15 | 6×1×8 | 1.5×0.25×2 m | 48 | 0 / -0.27 / 7.34 | - |
| 16 | CMP16 | 6×1×8 | 1.5×0.25×2 m | 48 | 0 / -0.89 / 7.34 | - |

## Modules (15)

| # | Short | Size (cells) | Size (m) | Volume (cells) | Position (m) | Default part |
|---:|---|---|---|---:|---|---|
| 1 | MOD1 | 8×8×8 | 2×2×2 m | 512 | 0 / -0.43 / -5.82 | Stock/FR4800 Reactor |
| 2 | MOD2 | 8×8×8 | 2×2×2 m | 512 | 0 / -2.63 / -5.82 | - |
| 3 | MOD3 | 16×8×10 | 4×2×2.5 m | 1280 | 0 / -0.66 / -8.67 | Stock/FM500 Drive |
| 4 | MOD4 | 12×8×10 | 3×2×2.5 m | 960 | 0 / -2.84 / -8.67 | Stock/FM500 Drive |
| 5 | MOD5 | 3×3×3 | 0.75×0.75×0.75 m | 27 | -1.57 / -1.19 / -3.33 | - |
| 6 | MOD6 | 3×3×3 | 0.75×0.75×0.75 m | 27 | -1.57 / -1.19 / 2.58 | - |
| 7 | MOD7 | 3×3×3 | 0.75×0.75×0.75 m | 27 | 1.57 / -1.19 / -3.33 | - |
| 8 | MOD8 | 3×3×3 | 0.75×0.75×0.75 m | 27 | 1.57 / -1.19 / 2.58 | - |
| 9 | MOD9 | 3×3×3 | 0.75×0.75×0.75 m | 27 | 0 / -1.83 / 6.43 | - |
| 10 | MOD10 | 3×3×3 | 0.75×0.75×0.75 m | 27 | 0 / -1.83 / 7.69 | - |
| 11 | MOD11 | 3×3×3 | 0.75×0.75×0.75 m | 27 | 0 / -1.83 / 8.95 | - |
| 12 | MOD12 | 2×2×2 | 0.5×0.5×0.5 m | 8 | 0 / 2.33 / -2.12 | Stock/RS35 'Frontline' Radar |
| 13 | MOD13 | 2×2×2 | 0.5×0.5×0.5 m | 8 | 0 / 3.35 / -2.12 | - |
| 14 | MOD14 | 2×2×2 | 0.5×0.5×0.5 m | 8 | 0 / -3.92 / 1.4 | - |
| 15 | MOD15 | 2×2×2 | 0.5×0.5×0.5 m | 8 | 0 / -3.92 / -2.1 | - |

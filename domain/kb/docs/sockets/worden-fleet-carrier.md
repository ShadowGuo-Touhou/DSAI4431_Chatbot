# Worden Fleet Carrier — socket map

Tags: kind=hull sockets; hull=Worden Fleet Carrier; sockets=47; mounts=13; compartments=20; modules=14
Keywords: socket, sockets, mount, mounts, slot, 槽位, 挂载位, 挂载点, 尺寸, 多大, 能装什么, 装得下, Worden Fleet Carrier
Summary: 47 sockets = 13 mount / 20 compartment / 14 module. The mount / compartment / module number is the one the game counts in (mount 1)/(mount 1-3) conditions — mounts are numbered 1..N across the whole ship, compartments and modules restart at 1 per hull.
Section: hull sockets;source=game prefab hierarchy (Nebulous stock/stock-f1/stock-f2 bundles)

## How to read this
- `Mount` = a surface mount for a weapon or a sensor.
- `Compartment` = the hull cut-outs that take CIC, damage control, magazines, crew spaces.
- `Module` = internal bays for reactors, drives, radar, jammers, hangars.
- Size is given both in 0.25 m cells and in metres; the volume is the cell product.

## Mounts (13)

| # | Short | Size (cells) | Size (m) | Volume (cells) | Position (m) | Default part |
|---:|---|---|---|---:|---|---|
| 1 | MT1 | 10×7×10 | 2.5×1.75×2.5 m | 700 | 21.171 / 2.415 / 5.823 | - |
| 2 | MT2 | 10×7×10 | 2.5×1.75×2.5 m | 700 | 21.171 / 2.415 / 2.75 | - |
| 3 | MT3 | 3×4×3 | 0.75×1×0.75 m | 36 | 22.057 / 1.817 / 0.161 | - |
| 4 | MT4 | 3×4×3 | 0.75×1×0.75 m | 36 | 22.355 / -2.514 / 0.549 | - |
| 5 | MT5 | 3×4×3 | 0.75×1×0.75 m | 36 | 17.674 / 1.616 / 2.129 | - |
| 6 | MT6 | 3×4×3 | 0.75×1×0.75 m | 36 | 16.605 / -2.514 / 0.549 | - |
| 7 | MT7 | 3×4×3 | 0.75×1×0.75 m | 36 | 24.355 / -0.327 / -11.683 | - |
| 8 | MT8 | 3×4×3 | 0.75×1×0.75 m | 36 | 14.605 / -0.327 / -11.683 | - |
| 9 | MT9 | 2×2×2 | 0.5×0.5×0.5 m | 8 | 18.365 / 2.745 / 10.469 | - |
| 10 | MT10 | 2×2×2 | 0.5×0.5×0.5 m | 8 | 20.619 / 2.745 / 10.469 | - |
| 11 | MT11 | 2×2×2 | 0.5×0.5×0.5 m | 8 | 14.92 / 2.85 / -2.431 | - |
| 12 | MT12 | 2×2×2 | 0.5×0.5×0.5 m | 8 | 22.063 / 4.172 / -1.593 | - |
| 13 | MT13 | 2×2×2 | 0.5×0.5×0.5 m | 8 | 19.48 / -3.04 / 12.638 | - |

## Compartments (20)

| # | Short | Size (cells) | Size (m) | Volume (cells) | Position (m) | Default part |
|---:|---|---|---|---:|---|---|
| 1 | CMP1 | 6×1×8 | 1.5×0.25×2 m | 48 | 19.48 / 4.39 / 7.75 | Stock/Basic CIC |
| 2 | CMP2 | 6×1×8 | 1.5×0.25×2 m | 48 | 19.48 / 4.39 / 3.74 | - |
| 3 | CMP3 | 6×1×8 | 1.5×0.25×2 m | 48 | 19.48 / 5.06 / 3.74 | - |
| 4 | CMP4 | 6×1×4 | 1.5×0.25×1 m | 24 | 19.48 / 4.39 / 1.71 | - |
| 5 | CMP5 | 6×1×4 | 1.5×0.25×1 m | 24 | 19.48 / 5.06 / 1.71 | - |
| 6 | CMP6 | 6×1×8 | 1.5×0.25×2 m | 48 | 19.48 / 5.38 / 7.75 | - |
| 7 | CMP7 | 6×1×8 | 1.5×0.25×2 m | 48 | 19.48 / 6.05 / 7.75 | - |
| 8 | CMP8 | 6×1×8 | 1.5×0.25×2 m | 48 | 19.48 / 1.39 / 9.66 | - |
| 9 | CMP9 | 6×1×8 | 1.5×0.25×2 m | 48 | 19.48 / 0.64 / 9.66 | - |
| 10 | CMP10 | 6×1×4 | 1.5×0.25×1 m | 24 | 19.48 / -0.36 / 8.91 | - |
| 11 | CMP11 | 6×1×4 | 1.5×0.25×1 m | 24 | 19.48 / -1.11 / 8.91 | - |
| 12 | CMP12 | 6×1×4 | 1.5×0.25×1 m | 24 | 19.48 / -0.36 / 10.41 | - |
| 13 | CMP13 | 6×1×4 | 1.5×0.25×1 m | 24 | 19.48 / -1.11 / 10.41 | - |
| 14 | CMP14 | 16×3×8 | 4×0.75×2 m | 384 | 19.48 / -1.73 / 3.18 | - |
| 15 | CMP15 | 16×3×8 | 4×0.75×2 m | 384 | 19.48 / -2.73 / -3.32 | - |
| 16 | HGR1 | 12×3×18 | 3×0.75×4.5 m | 648 | 19.48 / 1.12 / 4.47 | Stock/Bulk Internal Hangar |
| 17 | HGR2 | 12×3×18 | 3×0.75×4.5 m | 648 | 19.48 / -0.19 / 4.47 | Stock/Bulk Internal Hangar |
| 18 | HGR3 | 12×3×18 | 3×0.75×4.5 m | 648 | 19.48 / 1.12 / -3.35 | Stock/Bulk Internal Hangar |
| 19 | HGR4 | 12×3×18 | 3×0.75×4.5 m | 648 | 19.48 / -0.19 / -3.35 | Stock/Bulk Internal Hangar |
| 20 | HGR5 | 12×3×18 | 3×0.75×4.5 m | 648 | 19.48 / -1.44 / -3.35 | Stock/Bulk Internal Hangar |

## Modules (14)

| # | Short | Size (cells) | Size (m) | Volume (cells) | Position (m) | Default part |
|---:|---|---|---|---:|---|---|
| 1 | MOD1 | 8×8×8 | 2×2×2 m | 512 | 19.48 / 0.7 / -7 | Stock/FR4800 Reactor |
| 2 | MOD2 | 8×8×8 | 2×2×2 m | 512 | 19.48 / -1.5 / -7 | - |
| 3 | MOD3 | 16×8×10 | 4×2×2.5 m | 1280 | 19.48 / 0.33 / -9.74 | Stock/FM500 Drive |
| 4 | MOD4 | 16×8×10 | 4×2×2.5 m | 1280 | 19.48 / -1.85 / -9.74 | Stock/FM500 Drive |
| 5 | MOD5 | 3×3×3 | 0.75×0.75×0.75 m | 27 | 17.91 / -2.43 / -5.29 | - |
| 6 | MOD6 | 3×3×3 | 0.75×0.75×0.75 m | 27 | 17.91 / -2.43 / -1.45 | - |
| 7 | MOD7 | 3×3×3 | 0.75×0.75×0.75 m | 27 | 21.05 / -2.43 / -5.29 | - |
| 8 | MOD8 | 3×3×3 | 0.75×0.75×0.75 m | 27 | 21.05 / -2.43 / -1.45 | - |
| 9 | MOD9 | 2×2×2 | 0.5×0.5×0.5 m | 8 | 19.48 / 1.26 / 7.7 | - |
| 10 | MOD10 | 2×2×2 | 0.5×0.5×0.5 m | 8 | 19.48 / 0.26 / 7.7 | - |
| 11 | MOD11 | 2×2×2 | 0.5×0.5×0.5 m | 8 | 19.48 / -0.74 / 7.7 | - |
| 12 | MOD12 | 2×2×2 | 0.5×0.5×0.5 m | 8 | 19.48 / 3.29 / 5.86 | Stock/RS35 'Frontline' Radar |
| 13 | MOD13 | 2×2×2 | 0.5×0.5×0.5 m | 8 | 19.48 / 4.31 / 5.86 | - |
| 14 | MOD14 | 2×2×2 | 0.5×0.5×0.5 m | 8 | 19.48 / 3.29 / 7.7 | - |

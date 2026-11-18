# Levy Escort Carrier — socket map

Tags: kind=hull sockets; hull=Levy Escort Carrier; sockets=22; mounts=4; compartments=10; modules=8
Keywords: socket, sockets, mount, mounts, slot, 槽位, 挂载位, 挂载点, 尺寸, 多大, 能装什么, 装得下, Levy Escort Carrier
Summary: 22 sockets = 4 mount / 10 compartment / 8 module. The mount / compartment / module number is the one the game counts in (mount 1)/(mount 1-3) conditions — mounts are numbered 1..N across the whole ship, compartments and modules restart at 1 per hull.
Section: hull sockets;source=game prefab hierarchy (Nebulous stock/stock-f1/stock-f2 bundles)

## How to read this
- `Mount` = a surface mount for a weapon or a sensor.
- `Compartment` = the hull cut-outs that take CIC, damage control, magazines, crew spaces.
- `Module` = internal bays for reactors, drives, radar, jammers, hangars.
- Size is given both in 0.25 m cells and in metres; the volume is the cell product.

## Mounts (4)

| # | Short | Size (cells) | Size (m) | Volume (cells) | Position (m) | Default part |
|---:|---|---|---|---:|---|---|
| 1 | MT1 | 3×4×3 | 0.75×1×0.75 m | 36 | 167.342 / -109.129 / 6.462 | - |
| 2 | MT2 | 3×4×3 | 0.75×1×0.75 m | 36 | 165.233 / -112.082 / -3.953 | - |
| 3 | MT3 | 3×4×3 | 0.75×1×0.75 m | 36 | 168.463 / -110.35 / -0.387 | - |
| 4 | MT4 | 3×4×3 | 0.75×1×0.75 m | 36 | 160.96 / -110.35 / -0.387 | - |

## Compartments (10)

| # | Short | Size (cells) | Size (m) | Volume (cells) | Position (m) | Default part |
|---:|---|---|---|---:|---|---|
| 1 | CMP1 | 4×1×6 | 1×0.25×1.5 m | 24 | 167.362 / -107.586 / 4.84 | Stock/Basic CIC |
| 2 | CMP2 | 4×1×6 | 1×0.25×1.5 m | 24 | 167.362 / -108.116 / 4.84 | - |
| 3 | CMP3 | 4×1×6 | 1×0.25×1.5 m | 24 | 167.362 / -108.116 / 2.5 | - |
| 4 | CMP4 | 4×1×6 | 1×0.25×1.5 m | 24 | 167.362 / -108.646 / 2.5 | - |
| 5 | CMP5 | 6×1×8 | 1.5×0.25×2 m | 48 | 167.743 / -109.476 / 3.845 | - |
| 6 | CMP6 | 6×1×8 | 1.5×0.25×2 m | 48 | 167.743 / -110.099 / 3.845 | - |
| 7 | CMP7 | 12×3×12 | 3×0.75×3 m | 432 | 165.232 / -111.046 / 6.11 | Stock/Bulk Internal Hangar |
| 8 | CMP8 | 12×3×18 | 3×0.75×4.5 m | 648 | 165.232 / -111.046 / 2 | Stock/Bulk Internal Hangar |
| 9 | CMP9 | 12×3×12 | 3×0.75×3 m | 432 | 165.232 / -111.046 / -2.11 | Stock/Bulk Internal Hangar |
| 10 | CMP10 | 6×3×16 | 1.5×0.75×4 m | 288 | 162.322 / -111.046 / -0.17 | - |

## Modules (8)

| # | Short | Size (cells) | Size (m) | Volume (cells) | Position (m) | Default part |
|---:|---|---|---|---:|---|---|
| 1 | MOD1 | 6×6×6 | 1.5×1.5×1.5 m | 216 | 165.232 / -110.496 / -4.95 | Stock/FR4800 Reactor |
| 2 | MOD2 | 12×8×10 | 3×2×2.5 m | 960 | 165.232 / -110.506 / -7.05 | Stock/FM500 Drive |
| 3 | MOD3 | 3×3×3 | 0.75×0.75×0.75 m | 27 | 167.722 / -110.356 / -2.51 | - |
| 4 | MOD4 | 3×3×3 | 0.75×0.75×0.75 m | 27 | 167.722 / -110.356 / -1.42 | - |
| 5 | MOD5 | 3×3×3 | 0.75×0.75×0.75 m | 27 | 167.722 / -110.356 / 0.78 | - |
| 6 | MOD6 | 3×3×3 | 0.75×0.75×0.75 m | 27 | 167.722 / -110.356 / 1.87 | - |
| 7 | MOD7 | 2×2×2 | 0.5×0.5×0.5 m | 8 | 167.362 / -108.786 / 0.86 | - |
| 8 | MOD8 | 2×2×2 | 0.5×0.5×0.5 m | 8 | 167.362 / -108.786 / 4.26 | Stock/RS35 'Frontline' Radar |

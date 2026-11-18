# Ocello Cruiser — socket map

Tags: kind=hull sockets; hull=Ocello Cruiser; sockets=30; mounts=11; compartments=9; modules=10
Keywords: socket, sockets, mount, mounts, slot, 槽位, 挂载位, 挂载点, 尺寸, 多大, 能装什么, 装得下, Ocello Cruiser
Summary: 30 sockets = 11 mount / 9 compartment / 10 module. The mount / compartment / module number is the one the game counts in (mount 1)/(mount 1-3) conditions — mounts are numbered 1..N across the whole ship, compartments and modules restart at 1 per hull.
Section: hull sockets;source=game prefab hierarchy (Nebulous stock/stock-f1/stock-f2 bundles)

## How to read this
- `Mount` = a surface mount for a weapon or a sensor.
- `Compartment` = the hull cut-outs that take CIC, damage control, magazines, crew spaces.
- `Module` = internal bays for reactors, drives, radar, jammers, hangars.
- Size is given both in 0.25 m cells and in metres; the volume is the cell product.

## Mounts (11)

| # | Short | Size (cells) | Size (m) | Volume (cells) | Position (m) | Default part |
|---:|---|---|---|---:|---|---|
| 1 | MT1 | 6×4×6 | 1.5×1×1.5 m | 144 | 0 / 1.63 / 4.61 | - |
| 2 | MT2 | 6×4×6 | 1.5×1×1.5 m | 144 | 0 / 2.189 / 1.479 | - |
| 3 | MT3 | 6×4×6 | 1.5×1×1.5 m | 144 | 0 / -2.259 / -0.971 | - |
| 4 | MT4 | 3×4×3 | 0.75×1×0.75 m | 36 | -2.118 / -0.042 / -1.055 | - |
| 5 | MT5 | 3×4×3 | 0.75×1×0.75 m | 36 | 2.118 / -0.042 / -1.055 | - |
| 6 | MT6 | 3×4×3 | 0.75×1×0.75 m | 36 | 0 / 2.283 / -6.399 | - |
| 7 | MT7 | 3×4×3 | 0.75×1×0.75 m | 36 | 0 / -2.33 / -5.777 | - |
| 8 | MT8 | 2×2×2 | 0.5×0.5×0.5 m | 8 | 0 / 4.588 / -1.454 | - |
| 9 | MT9 | 2×2×2 | 0.5×0.5×0.5 m | 8 | 0 / -1.834 / 7.315 | - |
| 10 | MT10 | 2×2×2 | 0.5×0.5×0.5 m | 8 | -1.9 / 0.252 / 2.036 | - |
| 11 | MT11 | 2×2×2 | 0.5×0.5×0.5 m | 8 | 1.9 / 0.252 / 2.036 | - |

## Compartments (9)

| # | Short | Size (cells) | Size (m) | Volume (cells) | Position (m) | Default part |
|---:|---|---|---|---:|---|---|
| 1 | CMP1 | 6×1×8 | 1.5×0.25×2 m | 48 | 0 / 1 / 0.59 | Stock/Basic CIC |
| 2 | CMP2 | 6×1×8 | 1.5×0.25×2 m | 48 | 0 / 0.37 / 0.59 | - |
| 3 | CMP3 | 6×1×8 | 1.5×0.25×2 m | 48 | 0 / -0.34 / 0.59 | - |
| 4 | CMP4 | 6×1×8 | 1.5×0.25×2 m | 48 | 0 / -1.04 / -0.8 | - |
| 5 | CMP5 | 4×1×6 | 1×0.25×1.5 m | 24 | 0 / 3.64 / -1.5 | - |
| 6 | CMP6 | 6×1×6 | 1.5×0.25×1.5 m | 36 | 0 / 0.51 / 8 | - |
| 7 | CMP7 | 6×1×6 | 1.5×0.25×1.5 m | 36 | 0 / 0.01 / 8 | - |
| 8 | CMP8 | 6×1×6 | 1.5×0.25×1.5 m | 36 | 0 / 0.51 / 6.12 | - |
| 9 | CMP9 | 6×1×6 | 1.5×0.25×1.5 m | 36 | 0 / 0.01 / 6.12 | - |

## Modules (10)

| # | Short | Size (cells) | Size (m) | Volume (cells) | Position (m) | Default part |
|---:|---|---|---|---:|---|---|
| 1 | MOD1 | 6×6×6 | 1.5×1.5×1.5 m | 216 | 0 / 1.2 / -3.34 | Stock/FR4800 Reactor |
| 2 | MOD2 | 6×6×6 | 1.5×1.5×1.5 m | 216 | 0 / -0.71 / -3.34 | - |
| 3 | MOD3 | 8×12×10 | 2×3×2.5 m | 960 | 0 / 0 / -5.65 | Stock/FM500 Drive |
| 4 | MOD4 | 3×3×3 | 0.75×0.75×0.75 m | 27 | 0 / -1.11 / 1.99 | - |
| 5 | MOD5 | 3×3×3 | 0.75×0.75×0.75 m | 27 | 0 / 1.44 / 2.77 | - |
| 6 | MOD6 | 3×3×3 | 0.75×0.75×0.75 m | 27 | 0 / 0.21 / 4.58 | - |
| 7 | MOD7 | 2×2×2 | 0.5×0.5×0.5 m | 8 | 0 / 3.03 / -3.69 | Stock/RS35 'Frontline' Radar |
| 8 | MOD8 | 2×2×2 | 0.5×0.5×0.5 m | 8 | 0 / -1.16 / 4.08 | - |
| 9 | MOD9 | 2×2×2 | 0.5×0.5×0.5 m | 8 | 0 / -1.16 / 5.13 | - |
| 10 | MOD10 | 2×2×2 | 0.5×0.5×0.5 m | 8 | 0 / -1.16 / 6.22 | - |

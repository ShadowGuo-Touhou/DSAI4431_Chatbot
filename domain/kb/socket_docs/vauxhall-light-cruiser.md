# Vauxhall Light Cruiser — socket map

Tags: kind=hull sockets; hull=Vauxhall Light Cruiser; sockets=28; mounts=10; compartments=9; modules=9
Keywords: socket, sockets, mount, mounts, slot, 槽位, 挂载位, 挂载点, 尺寸, 多大, 能装什么, 装得下, Vauxhall Light Cruiser
Summary: 28 sockets = 10 mount / 9 compartment / 9 module. The mount / compartment / module number is the one the game counts in (mount 1)/(mount 1-3) conditions — mounts are numbered 1..N across the whole ship, compartments and modules restart at 1 per hull.
Section: hull sockets;source=game prefab hierarchy (Nebulous stock/stock-f1/stock-f2 bundles)

## How to read this
- `Mount` = a surface mount for a weapon or a sensor.
- `Compartment` = the hull cut-outs that take CIC, damage control, magazines, crew spaces.
- `Module` = internal bays for reactors, drives, radar, jammers, hangars.
- Size is given both in 0.25 m cells and in metres; the volume is the cell product.

## Mounts (10)

| # | Short | Size (cells) | Size (m) | Volume (cells) | Position (m) | Default part |
|---:|---|---|---|---:|---|---|
| 1 | MT1 | 3×4×5 | 0.75×1×1.25 m | 60 | 0 / 2.246 / -0.986 | - |
| 2 | MT2 | 3×4×5 | 0.75×1×1.25 m | 60 | 0 / -2.107 / -1.018 | - |
| 3 | MT3 | 3×4×5 | 0.75×1×1.25 m | 60 | 0 / 1.206 / 2.714 | - |
| 4 | MT4 | 3×4×5 | 0.75×1×1.25 m | 60 | 0 / 0.59 / 5.071 | - |
| 5 | MT5 | 3×4×5 | 0.75×1×1.25 m | 60 | 0 / 1.634 / -4.585 | - |
| 6 | MT6 | 3×4×5 | 0.75×1×1.25 m | 60 | 0 / -1.391 / 1.551 | - |
| 7 | MT7 | 2×2×2 | 0.5×0.5×0.5 m | 8 | 2.095 / 0.85 / -0.068 | - |
| 8 | MT8 | 2×2×2 | 0.5×0.5×0.5 m | 8 | -2.095 / 0.85 / -0.068 | - |
| 9 | MT9 | 2×2×2 | 0.5×0.5×0.5 m | 8 | 2.313 / -0.118 / -1.432 | - |
| 10 | MT10 | 2×2×2 | 0.5×0.5×0.5 m | 8 | -2.313 / -0.118 / -1.432 | - |

## Compartments (9)

| # | Short | Size (cells) | Size (m) | Volume (cells) | Position (m) | Default part |
|---:|---|---|---|---:|---|---|
| 1 | CMP1 | 6×1×8 | 1.5×0.25×2 m | 48 | 0 / -0.64 / 0.77 | Stock/Basic CIC |
| 2 | CMP2 | 6×1×8 | 1.5×0.25×2 m | 48 | 0 / -0.15 / 0.77 | - |
| 3 | CMP3 | 6×1×8 | 1.5×0.25×2 m | 48 | 0 / 0.33 / 0.77 | - |
| 4 | CMP4 | 6×1×8 | 1.5×0.25×2 m | 48 | 0 / 1.56 / 0.18 | - |
| 5 | CMP5 | 6×1×4 | 1.5×0.25×1 m | 24 | 0 / -0.69 / 4.05 | - |
| 6 | CMP6 | 6×1×4 | 1.5×0.25×1 m | 24 | 0 / -0.69 / 5.39 | - |
| 7 | CMP7 | 4×1×8 | 1×0.25×2 m | 32 | 0 / -0.204 / 4.655 | - |
| 8 | CMP8 | 6×1×4 | 1.5×0.25×1 m | 24 | 0 / 0.95 / -2.14 | - |
| 9 | CMP9 | 6×1×8 | 1.5×0.25×2 m | 48 | 0 / 0.95 / -3.81 | - |

## Modules (9)

| # | Short | Size (cells) | Size (m) | Volume (cells) | Position (m) | Default part |
|---:|---|---|---|---:|---|---|
| 1 | MOD1 | 6×6×6 | 1.5×1.5×1.5 m | 216 | 0 / -0.48 / -5.02 | Stock/FR4800 Reactor |
| 2 | MOD2 | 3×3×3 | 0.75×0.75×0.75 m | 27 | 0 / -0.65 / -3.41 | - |
| 3 | MOD3 | 8×12×10 | 2×3×2.5 m | 960 | 0 / -0.4 / -7.72 | Stock/FM500 Drive |
| 4 | MOD4 | 3×3×3 | 0.75×0.75×0.75 m | 27 | 1.9 / 0.35 / -2.3 | - |
| 5 | MOD5 | 2×2×2 | 0.5×0.5×0.5 m | 8 | 1.06 / 0.35 / 2.23 | - |
| 6 | MOD6 | 3×3×3 | 0.75×0.75×0.75 m | 27 | -1.9 / 0.35 / -2.3 | - |
| 7 | MOD7 | 2×2×2 | 0.5×0.5×0.5 m | 8 | -1.06 / 0.35 / 2.23 | - |
| 8 | MOD8 | 2×2×2 | 0.5×0.5×0.5 m | 8 | 0.64 / 2.1 / -2.57 | Stock/RS35 'Frontline' Radar |
| 9 | MOD9 | 2×2×2 | 0.5×0.5×0.5 m | 8 | -0.64 / 2.1 / -2.57 | - |

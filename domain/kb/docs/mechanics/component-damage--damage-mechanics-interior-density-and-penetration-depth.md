# Component Damage › Damage Mechanics › Interior Density and Penetration Depth

Source: Official wiki (wiki.hoodedhorse.com), game 0.6.2.6:260903-1430

## Body
Just like real life ships, all ships in Nebulous also have internal structural bulkheads to provide redundancy against threats in space. In game, internal hull structure is generalized as a homogeneous interior density (Interior Armor Density Equivalent) measured in cm of armor per meter, with different hull classes having different densities. Some damage types use internal density to determine pendepth (see damage type section below). For example, if HEKP hits a Solomon and has 180cm of pen left over after penetrating armor, the Solomon's 1.2cm/m density means the penetrator can go up to 150 meters into the hull.

| ANS Hull | Interior Density (cm/m) | Size (Length/Width/Height) | Total Armor Equivalent (Front/Side/Top) | Internal Armor Equivalent (F/S/T) |
|---|---|---|---|---|
| Sprinter | 0.5 | 80/37/28m | 56/35/30cm | 40/19/14cm |
| Raines | 0.5 | 96/35/40m | 78/48/50cm | 48/18/20cm |
| Keystone | 0.5 | 130/50/45m | 109/69/67cm | 65/25/23cm |
| Vauxhall | 1.00 | 215/62/60m | 267/114/112cm | 215/62/60cm |
| Axford | 1.20 | 195/70/75m | 314/164/170cm | 234/84/90cm |
| Solomon | 1.20 | 285/80/105m | 454/208/238cm | 342/96/126cm |
| OSP Hull | Interior Density (cm/m) | Size (L/W/H) | Total Armor Equivalent (F/S/T) | Internal Armor Equivalent (F/S/T) |
| Ferryman | 0.5 | 68/36/23m | 44/28/22cm | 34/18/12cm |
| Draugr | 0.5 | 87/53/40m | 54/37/30cm | 44/27/20cm |
| Flathead | 0.75 | 128/56/52m | 192/138/135cm | 96/42/39cm |
| Ocello | 1.2 | 210/50/75m | 312/120/150cm | 252/60/90cm |
| Marauder | 0.25 | 309/90/115m[1] | 118/63/69cm[1] | 78/23/29cm[1] |
| Moorline | 0.25 | 345/100/110m[1] | 127/65/68cm[1] | 87/25/28cm[1] |

Most damage types have a minimum pendepth of 15m. Even if the leftover penetration is 1cm, as long as it penetrates armor it will penetrate to 15m deep

Some damage types have conditions that can stop the attack early or limit penetration depth, even if it would normally penetrate deeper.

Some shells[2] have a "Penetration Depth Override"[3]; These shells only use pendepth for calculating overpen, and if the shell does not overpen, the shell's pendepth is guarenteed to reach the override distance. This override is not usually limited by anything, and is applied after the overpen check which means the override cannot cause an overpen on its own.

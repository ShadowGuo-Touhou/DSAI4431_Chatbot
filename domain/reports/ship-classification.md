# 舰船分类结果（依据 `Ship Builds.txt`）

舰队 230 支 · 舰船 1375 艘 · 解析失败 0 艘

判定口径：**must 全部满足 + 价格落在区间 + 非 bad 类** = `match`；价格区间只是参考（Ship Builds.txt 明说不是硬门槛，Cost 按 should 处理）：must 全过的就是该舰级，价格出区间标 `偏高`（overpriced，堆料）或 `偏低`（underpriced，玩家口语 greed / shell / 贪污）。整艘船没有任何 must 全过的 class = `bad_class`（A Cap 兜底）。一艘船可以同时属于多个舰级（例如 Sprinter 同时是 `A Cap ffl` 与 `gun/cap ffl`），满足的会全部并列列出。
`mount N` 类条件按 **Unity 预制体层级顺序**核对（序号取自游戏资源，已用 52 艘样本验证单调递增）。模块化民船（Bulk / Container 系列）没有顺序数据，相关条目按未知处理。

| 舰级 | 价格区间 | 艘数 | match | 偏高 | 偏低 |
|---|---|---:|---:|---:|---:|
| A Cap ffl (sprinter or shuttle) | 100-200 | 239 | 239 | 17 | 189 |
| A Cap (Any ship) | 0-0 | 35 | 0 | 0 | 0 |
| gun/cap ffl  (sprinter or shuttle) | 150-300 | 141 | 141 | 0 | 11 |
| scout ffl (sprinter or shuttle) | 110-250 | 111 | 111 | 0 | 0 |
| support ffl (sprinter or shuttle) | 150-400 | 69 | 69 | 9 | 0 |
| rocket shuttle (ruttle) | 260-300 | 7 | 7 | 0 | 3 |
| missile sprinter | 300-500 | 60 | 60 | 9 | 8 |
| gun tug | 250-400 | 23 | 23 | 0 | 0 |
| multi mission tug (mmt) | 400-500 | 6 | 6 | 0 | 0 |
| EWR/LRT tug | 170-300 | 39 | 39 | 0 | 0 |
| support tug | 250-400 | 12 | 12 | 1 | 0 |
| gun FF | 250-400 | 16 | 16 | 3 | 0 |
| missle FF | 750-1000 | 5 | 5 | 1 | 0 |
| support FF | 300-700 | 36 | 36 | 1 | 1 |
| Beam DD | 400-800 | 93 | 93 | 10 | 0 |
| Rail DD | 400-800 | 20 | 20 | 1 | 0 |
| 250 gun CL | 800-1200 | 38 | 38 | 14 | 0 |
| 120 gun CL | 0-0 | 1 | 0 | 0 | 0 |
| missile CL | 0-0 | 2 | 0 | 0 | 0 |
| gun MN | 450-650 | 51 | 51 | 5 | 15 |
| S2 MN | 800-1500 | 2 | 2 | 1 | 0 |
| EWR MN | 0-0 | 1 | 0 | 0 | 0 |
| 450 CH | 1400-1600 | 54 | 54 | 6 | 3 |
| greed CH | 1400-1600 | 6 | 6 | 0 | 0 |
| 250 CH | 0-0 | 1 | 0 | 0 | 0 |
| Command Cruiser killer (CCK) CH | 1600-3000 | 6 | 6 | 0 | 0 |
| missile CH | 2000-3000 | 6 | 6 | 2 | 0 |
| S2CH | 2500-3000 | 1 | 1 | 0 | 0 |
| 450 CC | 1400-1600 | 48 | 48 | 3 | 5 |
| 250 CC | 0-0 | 3 | 0 | 0 | 0 |
| missile CC | 2000-3000 | 12 | 12 | 1 | 0 |
| S2CC | 2000-3000 | 10 | 10 | 0 | 0 |
| Rail CC | 1200-1600 | 6 | 6 | 0 | 1 |
| 450 BB | 2000-3000 | 34 | 34 | 0 | 0 |
| TCSG BB | 2000-3000 | 6 | 6 | 0 | 0 |
| Beam BB | 1900-3000 | 7 | 7 | 0 | 0 |
| rail BB | 0-0 | 1 | 0 | 0 | 0 |
| 450 ln | 1100-1300 | 25 | 25 | 0 | 17 |
| 250 ln | 900-1100 | 9 | 9 | 4 | 5 |
| missle ln | 1400-3000 | 14 | 14 | 3 | 0 |
| mass driver (md) ln | 1000-1300 | 27 | 27 | 0 | 1 |
| half cve/cvl | 1300-1700 | 23 | 23 | 5 | 8 |
| full cve (ANS) | 2000-3000 | 5 | 5 | 0 | 0 |
| CLN (OSP) | 2500-3000 | 31 | 31 | 2 | 2 |
| CVLN (OSP) | 2500-3000 | 32 | 32 | 6 | 2 |
| CV (ANS) | 3000-12000 | 1 | 0 | 0 | 0 |
| unarmed (any hull) | 0-12000 | 183 | 183 | 0 | 0 |

## A Cap ffl (sprinter or shuttle)（100-200，共 239 艘）

| 舰队 | 舰名 | 舰体 | 点数 | 判定 | 本类 must | 通用 must | 耗电/供电 (kW) | (n-1) 判定 |
|---|---|---|---:|---|---|---|---|---|
| click to win | Glade of Mildrid | Ferryman Clipper Class | 76.0 | match 偏低 | 2/2 | 4/6 | 50/300 | OK |
| click to win | Raw and Rodeo | Ferryman Clipper Class | 76.0 | match 偏低 | 2/2 | 4/6 | 50/300 | OK |
| click to win | Brake | Ferryman Clipper Class | 76.0 | match 偏低 | 2/2 | 4/6 | 50/300 | OK |
| click to win | Doralia Y. Dollie | Ferryman Clipper Class | 76.0 | match 偏低 | 2/2 | 4/6 | 50/300 | OK |
| click to win | Gild | Ferryman Clipper Class | 76.0 | match 偏低 | 2/2 | 4/6 | 50/300 | OK |
| click to win | Slow Sneak | Ferryman Clipper Class | 76.0 | match 偏低 | 2/2 | 4/6 | 50/300 | OK |
| click to win | Bath Oaken | Ferryman Clipper Class | 76.0 | match 偏低 | 2/2 | 4/6 | 50/300 | OK |
| click to win | The Gusty Use | Ferryman Clipper Class | 76.0 | match 偏低 | 2/2 | 4/6 | 50/300 | OK |
| click to win | Mule Star | Ferryman Clipper Class | 76.0 | match 偏低 | 2/2 | 4/6 | 50/300 | OK |
| click to win | Steel of Levin | Ferryman Clipper Class | 76.0 | match 偏低 | 2/2 | 4/6 | 50/300 | OK |
| click to win | The Edged Wing | Ferryman Clipper Class | 76.0 | match 偏低 | 2/2 | 4/6 | 50/300 | OK |
| click to win | Medal | Ferryman Clipper Class | 76.0 | match 偏低 | 2/2 | 4/6 | 50/300 | OK |
| click to win | The Mini Poser | Ferryman Clipper Class | 76.0 | match 偏低 | 2/2 | 4/6 | 50/300 | OK |
| click to win | Email Small | Ferryman Clipper Class | 76.0 | match 偏低 | 2/2 | 4/6 | 50/300 | OK |
| 等 | 共 225 艘 | | | | | | |

## A Cap (Any ship)（0-0，共 35 艘）

| 舰队 | 舰名 | 舰体 | 点数 | 判定 | 本类 must | 通用 must | 耗电/供电 (kW) | (n-1) 判定 |
|---|---|---|---:|---|---|---|---|---|
| Raines | Booty | Raines Frigate Class | 176.0 | bad_class | 1/1 | 5/6 | 2050/4700 | OK |
| Raines | Flyer | Raines Frigate Class | 176.0 | bad_class | 1/1 | 5/6 | 2050/4700 | OK |
| Raines | Reset | Raines Frigate Class | 176.0 | bad_class | 1/1 | 5/6 | 2050/4700 | OK |
| Raines | Shirt | Raines Frigate Class | 176.0 | bad_class | 1/1 | 5/6 | 2050/4700 | OK |
| Raines | Eager | Raines Frigate Class | 176.0 | bad_class | 1/1 | 5/6 | 2050/4700 | OK |
| Raines | Ailey | Raines Frigate Class | 176.0 | bad_class | 1/1 | 5/6 | 2050/4700 | OK |
| Raines | Well | Raines Frigate Class | 176.0 | bad_class | 1/1 | 5/6 | 2050/4700 | OK |
| Raines | Bidet | Raines Frigate Class | 176.0 | bad_class | 1/1 | 5/6 | 2050/4700 | OK |
| Raines | Meal | Raines Frigate Class | 176.0 | bad_class | 1/1 | 5/6 | 2050/4700 | OK |
| Raines | Brag | Raines Frigate Class | 176.0 | bad_class | 1/1 | 5/6 | 2050/4700 | OK |
| FF GUN test 2 | Lilac Dual | Raines Frigate Class | 387.0 | bad_class | 1/1 | 6/6 | 3575/4850 | OK |
| FF GUN test 2 | Rummy | Raines Frigate Class | 400.0 | bad_class | 1/1 | 6/6 | 4775/4850 | OK |
| FF GUN test 2 | Godfrey W. Alard | Raines Frigate Class | 403.0 | bad_class | 1/1 | 6/6 | 3850/4850 | OK |
| FF GUN test 2 | The Lay Felt | Raines Frigate Class | 407.0 | bad_class | 1/1 | 6/6 | 3725/4850 | OK |
| 等 | 共 21 艘 | | | | | | |

## gun/cap ffl  (sprinter or shuttle)（150-300，共 141 艘）

| 舰队 | 舰名 | 舰体 | 点数 | 判定 | 本类 must | 通用 must | 耗电/供电 (kW) | (n-1) 判定 |
|---|---|---|---:|---|---|---|---|---|
| TF-6k | Cash | Ferryman Clipper Class | 122.0 | match 偏低 | 1/1 | 5/6 | 30/200 | OK |
| TF-6k | Binni A. Marice | Ferryman Clipper Class | 122.0 | match 偏低 | 1/1 | 5/6 | 30/200 | OK |
| TF-C | Cash | Ferryman Clipper Class | 123.0 | match 偏低 | 1/1 | 5/6 | 30/200 | OK |
| TF-C | Binni A. Marice | Ferryman Clipper Class | 123.0 | match 偏低 | 1/1 | 5/6 | 30/200 | OK |
| CV 12k | Gram | Sprinter Corvette Class | 127.0 | match 偏低 | 1/1 | 5/6 | 2050/2750 | OK |
| CV 12k | Input Game | Sprinter Corvette Class | 127.0 | match 偏低 | 1/1 | 5/6 | 2050/2750 | OK |
| CV 12k | Fixer of Deanna | Sprinter Corvette Class | 127.0 | match 偏低 | 1/1 | 5/6 | 2050/2750 | OK |
| CV 12k | Tours and Grits | Sprinter Corvette Class | 127.0 | match 偏低 | 1/1 | 5/6 | 2050/2750 | OK |
| 1- cc and shuttles | Wound Know | Ferryman Clipper Class | 144.0 | match 偏低 | 1/1 | 5/6 | 1510/2150 | OK |
| 1- cc and shuttles | Gipsy Done | Ferryman Clipper Class | 144.0 | match 偏低 | 1/1 | 5/6 | 1510/2150 | OK |
| LIGHT 2.0 | CM-4D1 Decoy Container | Ferryman Clipper Class | 145.0 | match 偏低 | 1/1 | 5/6 | 1530/2150 | OK |
| Mothballed ships | Forty | Sprinter Corvette Class | 151.0 | match | 1/1 | 5/6 | 2050/2750 | OK |
| All 27 sample ships · Protectorate | In Your Walls | Ferryman Clipper Class | 152.0 | match | 1/1 | 5/6 | 1310/2150 | OK |
| TF-6k | Mabelle R. Margy | Ferryman Clipper Class | 159.0 | match | 1/1 | 5/6 | 1530/2050 | OK |
| 等 | 共 127 艘 | | | | | | |

## scout ffl (sprinter or shuttle)（110-250，共 111 艘）

| 舰队 | 舰名 | 舰体 | 点数 | 判定 | 本类 must | 通用 must | 耗电/供电 (kW) | (n-1) 判定 |
|---|---|---|---:|---|---|---|---|---|
| dum shi | Pawn | Ferryman Clipper Class | 110.0 | match [scout ffl (sprinter or shuttle) / unarmed (any hull)] | 1/1 | 3/6 | 2000/2150 | OK |
| dum shi | Pawn | Ferryman Clipper Class | 110.0 | match [scout ffl (sprinter or shuttle) / unarmed (any hull)] | 1/1 | 3/6 | 2000/2150 | OK |
| dum shi | Pawn | Ferryman Clipper Class | 110.0 | match [scout ffl (sprinter or shuttle) / unarmed (any hull)] | 1/1 | 3/6 | 2000/2150 | OK |
| dum shi | Pawn | Ferryman Clipper Class | 110.0 | match [scout ffl (sprinter or shuttle) / unarmed (any hull)] | 1/1 | 3/6 | 2000/2150 | OK |
| dum shi | Pawn | Ferryman Clipper Class | 110.0 | match [scout ffl (sprinter or shuttle) / unarmed (any hull)] | 1/1 | 3/6 | 2000/2150 | OK |
| dum shi | Pawn | Ferryman Clipper Class | 110.0 | match [scout ffl (sprinter or shuttle) / unarmed (any hull)] | 1/1 | 3/6 | 2000/2150 | OK |
| dum shi | Pawn | Ferryman Clipper Class | 110.0 | match [scout ffl (sprinter or shuttle) / unarmed (any hull)] | 1/1 | 3/6 | 2000/2150 | OK |
| dum shi | Pawn | Ferryman Clipper Class | 110.0 | match [scout ffl (sprinter or shuttle) / unarmed (any hull)] | 1/1 | 3/6 | 2000/2150 | OK |
| Linear inf | BULWARK | Ferryman Clipper Class | 110.0 | match [scout ffl (sprinter or shuttle) / unarmed (any hull)] | 1/1 | 3/6 | 2000/2150 | OK |
| cmd test | Brandice J. Rachel | Ferryman Clipper Class | 110.0 | match [scout ffl (sprinter or shuttle) / unarmed (any hull)] | 1/1 | 3/6 | 2000/2150 | OK |
| cmd test | Hoop Antic | Ferryman Clipper Class | 110.0 | match [scout ffl (sprinter or shuttle) / unarmed (any hull)] | 1/1 | 3/6 | 2000/2150 | OK |
| cmd test | Brit of Charmane | Ferryman Clipper Class | 110.0 | match [scout ffl (sprinter or shuttle) / unarmed (any hull)] | 1/1 | 3/6 | 2000/2150 | OK |
| cmd test | Jeer | Ferryman Clipper Class | 110.0 | match [scout ffl (sprinter or shuttle) / unarmed (any hull)] | 1/1 | 3/6 | 2000/2150 | OK |
| cmd test | Oates | Ferryman Clipper Class | 110.0 | match [scout ffl (sprinter or shuttle) / unarmed (any hull)] | 1/1 | 3/6 | 2000/2150 | OK |
| 等 | 共 97 艘 | | | | | | |

## support ffl (sprinter or shuttle)（150-400，共 69 艘）

| 舰队 | 舰名 | 舰体 | 点数 | 判定 | 本类 must | 通用 must | 耗电/供电 (kW) | (n-1) 判定 |
|---|---|---|---:|---|---|---|---|---|
| 大冲击 | 无名氏 | Ferryman Clipper Class | 168.0 | match | 1/1 | 3/6 | 2100/2150 | OK |
| 1- cc and shuttles | Lobby | Ferryman Clipper Class | 186.0 | match [gun/cap ffl  (sprinter or shuttle) / support ffl (sprinter or shuttle)] | 1/1 | 6/6 | 2120/2150 | OK |
| 1- cc and shuttles | Croak | Ferryman Clipper Class | 186.0 | match [gun/cap ffl  (sprinter or shuttle) / support ffl (sprinter or shuttle)] | 1/1 | 6/6 | 2120/2150 | OK |
| TF-6k | Mist Zonal | Ferryman Clipper Class | 189.0 | match [gun/cap ffl  (sprinter or shuttle) / support ffl (sprinter or shuttle)] | 1/1 | 5/6 | 2130/2150 | OK |
| Advent Squadran MKIII | Misty Slate | Ferryman Clipper Class | 189.0 | match [support ffl (sprinter or shuttle) / unarmed (any hull)] | 1/1 | 5/6 | 2000/2050 | OK |
| TF-C | Mist Zonal | Ferryman Clipper Class | 190.0 | match [gun/cap ffl  (sprinter or shuttle) / support ffl (sprinter or shuttle)] | 1/1 | 5/6 | 2130/2150 | OK |
| Advent Squadran MKIII | Fluffy Tails | Ferryman Clipper Class | 190.0 | match [support ffl (sprinter or shuttle) / unarmed (any hull)] | 1/1 | 5/6 | 2000/2050 | OK |
| Advent Squadran MKIII | Fuzzy Ears | Ferryman Clipper Class | 190.0 | match [support ffl (sprinter or shuttle) / unarmed (any hull)] | 1/1 | 5/6 | 2000/2050 | OK |
| Advent Squadran MKIII | Thick Raven | Ferryman Clipper Class | 190.0 | match [support ffl (sprinter or shuttle) / unarmed (any hull)] | 1/1 | 5/6 | 2000/2050 | OK |
| Advent Squadran MKIII | Failed Repair | Ferryman Clipper Class | 190.0 | match [support ffl (sprinter or shuttle) / unarmed (any hull)] | 1/1 | 5/6 | 2000/2050 | OK |
| Advent Squadran MKIII | Chief Wells | Ferryman Clipper Class | 190.0 | match [support ffl (sprinter or shuttle) / unarmed (any hull)] | 1/1 | 5/6 | 2000/2050 | OK |
| Advent Squadran MKIII | Gone Roads | Ferryman Clipper Class | 190.0 | match [support ffl (sprinter or shuttle) / unarmed (any hull)] | 1/1 | 5/6 | 2000/2050 | OK |
| All 34 sample ships · Alliance | Zippy Taxis | Sprinter Corvette Class | 219.0 | match [gun/cap ffl  (sprinter or shuttle) / support ffl (sprinter or shuttle)] | 1/1 | 5/6 | 1900/2600 | OK |
| BB test 55 Newbie | Zippy Taxis | Sprinter Corvette Class | 220.0 | match [gun/cap ffl  (sprinter or shuttle) / support ffl (sprinter or shuttle)] | 1/1 | 5/6 | 1900/2600 | OK |
| 等 | 共 55 艘 | | | | | | |

## rocket shuttle (ruttle)（260-300，共 7 艘）

| 舰队 | 舰名 | 舰体 | 点数 | 判定 | 本类 must | 通用 must | 耗电/供电 (kW) | (n-1) 判定 |
|---|---|---|---:|---|---|---|---|---|
| Meteror Rain Project | Pecan Slav | Ferryman Clipper Class | 221.0 | match 偏低 | 4/4 | 4/6 | 1550/2050 | OK |
| Meteror Rain Project | Clock | Ferryman Clipper Class | 221.0 | match 偏低 | 4/4 | 4/6 | 1550/2050 | OK |
| md maxxing | Pecan Slav | Ferryman Clipper Class | 221.0 | match 偏低 | 4/4 | 4/6 | 1550/2050 | OK |
| All 27 sample ships · Protectorate | Applied Pressure | Ferryman Clipper Class | 277.0 | match | 4/4 | 4/6 | 1350/2050 | OK |
| All 27 sample ships · Protectorate | Repulsive Force | Ferryman Clipper Class | 277.0 | match | 4/4 | 4/6 | 1350/2050 | OK |
| Azurite Squadron | Applied Pressure | Ferryman Clipper Class | 286.0 | match | 4/4 | 4/6 | 1350/2050 | OK |
| Azurite Squadron | Repulsive Force | Ferryman Clipper Class | 286.0 | match | 4/4 | 4/6 | 1350/2050 | OK |

## missile sprinter（300-500，共 60 艘）

| 舰队 | 舰名 | 舰体 | 点数 | 判定 | 本类 must | 通用 must | 耗电/供电 (kW) | (n-1) 判定 |
|---|---|---|---:|---|---|---|---|---|
| TF Connect | Eternal Star | Sprinter Corvette Class | 266.0 | match 偏低 | 2/2 | 3/6 | 2200/2900 | OK |
| TF Connect | Timekeeper | Sprinter Corvette Class | 266.0 | match 偏低 | 2/2 | 3/6 | 2200/2900 | OK |
| TF Connect | Reverse Chaos | Sprinter Corvette Class | 266.0 | match 偏低 | 2/2 | 3/6 | 2200/2900 | OK |
| TF Connect | Deer of Nature | Sprinter Corvette Class | 266.0 | match 偏低 | 2/2 | 3/6 | 2200/2900 | OK |
| TF Connect | Reaper Rapper | Sprinter Corvette Class | 281.0 | match 偏低 | 2/2 | 3/6 | 2200/2900 | OK |
| TF Connect | Tanticle Cultist | Sprinter Corvette Class | 281.0 | match 偏低 | 2/2 | 3/6 | 2200/2900 | OK |
| TF Connect | Bird of Flame | Sprinter Corvette Class | 281.0 | match 偏低 | 2/2 | 3/6 | 2200/2900 | OK |
| TF Connect | Civilization | Sprinter Corvette Class | 281.0 | match 偏低 | 2/2 | 3/6 | 2200/2900 | OK |
| jam CL dad | Blaire B. Lennon | Sprinter Corvette Class | 304.0 | match | 2/2 | 6/6 | 2475/2750 | OK |
| mixed cap | Born Loom | Sprinter Corvette Class | 308.0 | match | 2/2 | 6/6 | 2475/2750 | OK |
| mixed cap | Xavier E. Sletten | Sprinter Corvette Class | 308.0 | match | 2/2 | 6/6 | 2475/2750 | OK |
| Assult Group Sigma | Mama I'm a Criminal | Sprinter Corvette Class | 322.0 | match [support ffl (sprinter or shuttle) / missile sprinter] | 1/1 | 5/6 | 3425/2900 | OK |
| Mixed FFLs | T. Final Light | Sprinter Corvette Class | 352.0 | match [missile sprinter / support ffl (sprinter or shuttle)] | 2/2 | 5/6 | 3425/2900 | OK |
| Mixed FFLs | T. Tepid Siren | Sprinter Corvette Class | 352.0 | match [missile sprinter / support ffl (sprinter or shuttle)] | 2/2 | 5/6 | 3425/2900 | OK |
| 等 | 共 46 艘 | | | | | | |

## gun tug（250-400，共 23 艘）

| 舰队 | 舰名 | 舰体 | 点数 | 判定 | 本类 must | 通用 must | 耗电/供电 (kW) | (n-1) 判定 |
|---|---|---|---:|---|---|---|---|---|
| tug blob | TBD | Draugr Clipper Class | 260.0 | match | 1/1 | 5/6 | 460/3950 | OK |
| tug blob | TBD | Draugr Clipper Class | 260.0 | match | 1/1 | 5/6 | 460/3950 | OK |
| tug blob | TBD | Draugr Clipper Class | 270.0 | match | 1/1 | 5/6 | 460/3950 | OK |
| tug blob | TBD | Draugr Clipper Class | 270.0 | match | 1/1 | 5/6 | 460/3950 | OK |
| tug blob | TBD | Draugr Clipper Class | 270.0 | match | 1/1 | 5/6 | 460/3950 | OK |
| tug blob | TBD | Draugr Clipper Class | 270.0 | match | 1/1 | 5/6 | 460/3950 | OK |
| tug blob | TBD | Draugr Clipper Class | 280.0 | match | 1/1 | 5/6 | 710/3950 | OK |
| All 27 sample ships · Protectorate | TBD | Draugr Clipper Class | 280.0 | match | 1/1 | 5/6 | 710/3950 | OK |
| 大冲击 | 大冲击 | Draugr Clipper Class | 284.0 | match | 1/1 | 6/6 | 1590/5300 | OK |
| 大冲击 | 大冲击 | Draugr Clipper Class | 284.0 | match | 1/1 | 6/6 | 1590/5300 | OK |
| 大冲击 | 大冲击 | Draugr Clipper Class | 284.0 | match | 1/1 | 6/6 | 1590/5300 | OK |
| 大冲击 | 大冲击 | Draugr Clipper Class | 311.0 | match | 1/1 | 6/6 | 3050/5300 | OK |
| tesdt | Maker | Draugr Clipper Class | 320.0 | match | 1/1 | 6/6 | 2900/3850 | OK |
| 大冲击 | 大冲击 | Draugr Clipper Class | 321.0 | match | 1/1 | 6/6 | 2000/5300 | OK |
| 等 | 共 9 艘 | | | | | | |

## multi mission tug (mmt)（400-500，共 6 艘）

| 舰队 | 舰名 | 舰体 | 点数 | 判定 | 本类 must | 通用 must | 耗电/供电 (kW) | (n-1) 判定 |
|---|---|---|---:|---|---|---|---|---|
| 大冲击 | 大冲击二型 | Draugr Clipper Class | 432.0 | match | 2/2 | 6/6 | 3070/5300 | OK |
| 大冲击 | 大冲击二型 | Draugr Clipper Class | 436.0 | match | 2/2 | 6/6 | 3070/5300 | OK |
| Tantalum Squadron | Ranger | Draugr Clipper Class | 452.0 | match | 2/2 | 5/6 | 3500/3950 | OK |
| Tantalum Squadron | Bailiff | Draugr Clipper Class | 452.0 | match | 2/2 | 5/6 | 3500/3950 | OK |
| Tantalum Squadron | Custodian | Draugr Clipper Class | 452.0 | match | 2/2 | 5/6 | 3500/3950 | OK |
| Heteroteuthinae | Amphorateuthis | Draugr Clipper Class | 453.0 | match | 2/2 | 5/6 | 3300/3950 | OK |

## EWR/LRT tug（170-300，共 39 艘）

| 舰队 | 舰名 | 舰体 | 点数 | 判定 | 本类 must | 通用 must | 耗电/供电 (kW) | (n-1) 判定 |
|---|---|---|---:|---|---|---|---|---|
| plasma 100 | Nosed Brow | Draugr Clipper Class | 170.0 | match [unarmed (any hull) / EWR/LRT tug] | 1/1 | 3/6 | 4500/5300 | OK |
| plasma 100 | Molar Juke | Draugr Clipper Class | 170.0 | match [unarmed (any hull) / EWR/LRT tug] | 1/1 | 3/6 | 4500/5300 | OK |
| plasma 100 | Slimy Grain | Draugr Clipper Class | 170.0 | match [unarmed (any hull) / EWR/LRT tug] | 1/1 | 3/6 | 4500/5300 | OK |
| LIGHT 2.0 | CM-4D1 Decoy Container | Draugr Clipper Class | 170.0 | match [unarmed (any hull) / EWR/LRT tug] | 1/1 | 4/6 | 4500/5300 | OK |
| LIGHT MAX | TallyTwoTimes | Draugr Clipper Class | 170.0 | match [unarmed (any hull) / EWR/LRT tug] | 1/1 | 3/6 | 4500/5300 | OK |
| LIGHT MAX | Admiralyolo | Draugr Clipper Class | 170.0 | match [unarmed (any hull) / EWR/LRT tug] | 1/1 | 3/6 | 4500/5300 | OK |
| LIGHT MAX | TwoNiner | Draugr Clipper Class | 170.0 | match [unarmed (any hull) / EWR/LRT tug] | 1/1 | 3/6 | 4500/5300 | OK |
| 大冲击 | 高耸灯一号 | Draugr Clipper Class | 185.0 | match [unarmed (any hull) / EWR/LRT tug] | 1/1 | 3/6 | 5100/5300 | OK |
| 大冲击 | 高耸灯二号 | Draugr Clipper Class | 185.0 | match [unarmed (any hull) / EWR/LRT tug] | 1/1 | 3/6 | 5100/5300 | OK |
| Linear inf | BULWARK | Draugr Clipper Class | 187.0 | match | 1/1 | 5/6 | 4530/5300 | OK |
| Linear inf | BULWARK | Draugr Clipper Class | 187.0 | match | 1/1 | 5/6 | 4530/5300 | OK |
| TF-6k | Fade and Hinge | Draugr Clipper Class | 187.0 | match [unarmed (any hull) / EWR/LRT tug] | 1/1 | 4/6 | 4550/5300 | OK |
| TF-6k | Swell of Hatty | Draugr Clipper Class | 187.0 | match [unarmed (any hull) / EWR/LRT tug] | 1/1 | 4/6 | 4550/5300 | OK |
| TF-C | Fade and Hinge | Draugr Clipper Class | 187.0 | match [unarmed (any hull) / EWR/LRT tug] | 1/1 | 4/6 | 4550/5300 | OK |
| 等 | 共 25 艘 | | | | | | |

## support tug（250-400，共 12 艘）

| 舰队 | 舰名 | 舰体 | 点数 | 判定 | 本类 must | 通用 must | 耗电/供电 (kW) | (n-1) 判定 |
|---|---|---|---:|---|---|---|---|---|
| All 27 sample ships · Protectorate | Bailiff | Draugr Clipper Class | 365.0 | match [gun tug / support tug] | 1/1 | 5/6 | 3500/3950 | OK |
| All 27 sample ships · Protectorate | Ranger | Draugr Clipper Class | 365.0 | match [gun tug / support tug] | 1/1 | 5/6 | 3500/3950 | OK |
| tug blob | TBD | Draugr Clipper Class | 373.0 | match [gun tug / support tug] | 1/1 | 6/6 | 3475/3950 | OK |
| tug blob | TBD | Draugr Clipper Class | 373.0 | match [gun tug / support tug] | 1/1 | 6/6 | 3475/3950 | OK |
| tug blob | TBD | Draugr Clipper Class | 374.0 | match [gun tug / support tug] | 1/1 | 5/6 | 3850/5300 | OK |
| bulk WIP | Jkerjter | Draugr Clipper Class | 386.0 | match | 1/1 | 5/6 | 4350/5300 | OK |
| 大冲击 | 不冲击 | Draugr Clipper Class | 395.0 | match | 1/1 | 3/6 | 3700/3950 | OK |
| 大冲击 | 不冲击 | Draugr Clipper Class | 395.0 | match | 1/1 | 3/6 | 3700/3950 | OK |
| 大冲击 | 不冲击 | Draugr Clipper Class | 400.0 | match | 1/1 | 3/6 | 3700/3950 | OK |
| 大冲击 | 不冲击 | Draugr Clipper Class | 400.0 | match | 1/1 | 3/6 | 3700/5300 | OK |
| All 27 sample ships · Protectorate | 不冲击 | Draugr Clipper Class | 400.0 | match | 1/1 | 3/6 | 3700/3950 | OK |
| 2 OSP Support New | The Wily Fact | Draugr Clipper Class | 442.0 | match 偏高 | 1/1 | 3/6 | 9350/5200 | OK |

## gun FF（250-400，共 16 艘）

| 舰队 | 舰名 | 舰体 | 点数 | 判定 | 本类 must | 通用 must | 耗电/供电 (kW) | (n-1) 判定 |
|---|---|---|---:|---|---|---|---|---|
| Another 6k | Pizza? | Raines Frigate Class | 330.0 | match | 1/1 | 5/6 | 3400/4850 | OK |
| ANOMALY-120FFMAXX | ̢̧͔̹͇̀̆̄A̴N̅́̏O̰̽Ṁ̸͈͠A̶L̸͇̗͕Y | Raines Frigate Class | 333.0 | match | 1/1 | 5/6 | 500/4850 | OK |
| ANOMALY-120FFMAXX | ̢̧͔̹͇̀̆̄A̴N̅́̏O̰̽Ṁ̸͈͠A̶L̸͇̗͕Y | Raines Frigate Class | 343.0 | match | 1/1 | 5/6 | 2500/4850 | OK |
| ANOMALY-120FFMAXX | ̢̧͔̹͇̀̆̄A̴N̅́̏O̰̽Ṁ̸͈͠A̶L̸͇̗͕Y | Raines Frigate Class | 343.0 | match | 1/1 | 5/6 | 2500/4850 | OK |
| ANOMALY-120FFMAXX | ̢̧͔̹͇̀̆̄A̴N̅́̏O̰̽Ṁ̸͈͠A̶L̸͇̗͕Y | Raines Frigate Class | 343.0 | match | 1/1 | 5/6 | 2500/4850 | OK |
| masqford | Brew | Raines Frigate Class | 371.0 | match | 1/1 | 5/6 | 2650/4850 | OK |
| masqford | Irony | Raines Frigate Class | 371.0 | match | 1/1 | 5/6 | 2650/4850 | OK |
| All 34 sample ships · Alliance | Brew | Raines Frigate Class | 371.0 | match | 1/1 | 5/6 | 2650/4850 | OK |
| ANOMALY-120FFMAXX | ̢̧͔̹͇̀̆̄A̴N̅́̏O̰̽Ṁ̸͈͠A̶L̸͇̗͕Y | Raines Frigate Class | 380.0 | match | 1/1 | 5/6 | 4250/4850 | OK |
| ANOMALY-120FFMAXX | ̢̧͔̹͇̀̆̄A̴N̅́̏O̰̽Ṁ̸͈͠A̶L̸͇̗͕Y | Raines Frigate Class | 383.0 | match | 1/1 | 5/6 | 4800/4850 | OK |
| masqford | Maxim and Money | Raines Frigate Class | 388.0 | match | 1/1 | 5/6 | 2575/4850 | OK |
| HC Gun Missile test 8 | Peel of Agnesse | Raines Frigate Class | 397.0 | match | 1/1 | 5/6 | 4400/4700 | OK |
| All 34 sample ships · Alliance | Peel of Agnesse | Raines Frigate Class | 397.0 | match | 1/1 | 5/6 | 4400/4700 | OK |
| All Craft Are Bastards | Blind Silly | Raines Frigate Class | 417.0 | match 偏高 | 1/1 | 5/6 | 4250/4850 | OK |
| 等 | 共 2 艘 | | | | | | |

## missle FF（750-1000，共 5 艘）

| 舰队 | 舰名 | 舰体 | 点数 | 判定 | 本类 must | 通用 must | 耗电/供电 (kW) | (n-1) 判定 |
|---|---|---|---:|---|---|---|---|---|
| concept | |||||||| | Raines Frigate Class | 927.0 | match | 2/2 | 4/6 | 1000/4700 | OK |
| zpzd 导弹FF | Read | Raines Frigate Class | 1000.0 | match | 2/2 | 4/6 | 3000/4700 | OK |
| zpzd 导弹FF | Toady | Raines Frigate Class | 1000.0 | match | 2/2 | 4/6 | 3000/4700 | OK |
| zpzd 导弹FF | Bling | Raines Frigate Class | 1000.0 | match | 2/2 | 4/6 | 3000/4700 | OK |
| Test Group Alpha | Inlet West | Raines Frigate Class | 1195.0 | match 偏高 | 2/2 | 5/6 | 3650/4850 | OK |

## support FF（300-700，共 36 艘）

| 舰队 | 舰名 | 舰体 | 点数 | 判定 | 本类 must | 通用 must | 耗电/供电 (kW) | (n-1) 判定 |
|---|---|---|---:|---|---|---|---|---|
| mixed cap | Josiah U. Garik | Raines Frigate Class | 276.0 | match 偏低 | 1/1 | 4/6 | 4450/4700 | OK |
| Another 6k (3) | Pizza? | Raines Frigate Class | 330.0 | match | 1/1 | 4/6 | 4550/4850 | OK |
| All 34 sample ships · Alliance | Sale | Raines Frigate Class | 344.0 | match | 1/1 | 4/6 | 5850/6950 | OK |
| jam CL dad | Burn Ahead | Raines Frigate Class | 349.0 | match | 1/1 | 5/6 | 5700/6950 | OK |
| jam CL dad | Hate and Vial | Raines Frigate Class | 349.0 | match | 1/1 | 5/6 | 5700/6950 | OK |
| All 34 sample ships · Alliance | Beige of Cleland | Raines Frigate Class | 370.0 | match | 1/1 | 4/6 | 5850/6950 | OK |
| CV test | Starlit Skies | Raines Frigate Class | 407.0 | match | 1/1 | 5/6 | 4490/7100 | OK |
| All Craft Are Bastards | Rowland B. Hauger | Raines Frigate Class | 411.0 | match | 1/1 | 5/6 | 5850/7100 | OK |
| All Craft Are Bastards | Pawn Roast | Raines Frigate Class | 411.0 | match | 1/1 | 5/6 | 5850/7100 | OK |
| mixed cap | Ring Down | Raines Frigate Class | 411.0 | match | 1/1 | 5/6 | 5850/7100 | OK |
| Presidential Escort | Charlotte | Raines Frigate Class | 415.0 | match | 1/1 | 4/6 | 9175/6950 | (n-1) 可关 |
| Another 6k (2) | Pizza? | Raines Frigate Class | 429.0 | match | 1/1 | 4/6 | 4750/4850 | OK |
| masqford | Drain of Cathie | Raines Frigate Class | 440.0 | match | 1/1 | 4/6 | 3850/4850 | OK |
| hc gun dd test 11 | Sale | Raines Frigate Class | 459.0 | match | 1/1 | 4/6 | 5850/6950 | OK |
| 等 | 共 22 艘 | | | | | | |

## Beam DD（400-800，共 93 艘）

| 舰队 | 舰名 | 舰体 | 点数 | 判定 | 本类 must | 通用 must | 耗电/供电 (kW) | (n-1) 判定 |
|---|---|---|---:|---|---|---|---|---|
| Another 6k (2) | Tam Tember | Keystone Destroyer Class | 445.0 | match | 1/1 | 4/6 | 3850/3400 | OK |
| Another 6k (2) | Ten Dender | Keystone Destroyer Class | 445.0 | match | 1/1 | 4/6 | 3850/3400 | OK |
| Another 6k (2) | Tan Dander | Keystone Destroyer Class | 445.0 | match | 1/1 | 4/6 | 3850/3400 | OK |
| Another 6k (2) | Tam Gender | Keystone Destroyer Class | 445.0 | match | 1/1 | 4/6 | 3850/3400 | OK |
| Another 6k (2) | Pam Tender | Keystone Destroyer Class | 445.0 | match | 1/1 | 4/6 | 3850/3400 | OK |
| Another 6k (2) | Chicken Tender | Keystone Destroyer Class | 445.0 | match | 1/1 | 4/6 | 3850/3400 | OK |
| Another 6k (3) | Tam Tember | Keystone Destroyer Class | 445.0 | match | 1/1 | 4/6 | 3850/3400 | OK |
| Another 6k (3) | Ten Dender | Keystone Destroyer Class | 445.0 | match | 1/1 | 4/6 | 3850/3400 | OK |
| Another 6k (3) | Tan Dander | Keystone Destroyer Class | 445.0 | match | 1/1 | 4/6 | 3850/3400 | OK |
| Another 6k (3) | Tam Gender | Keystone Destroyer Class | 445.0 | match | 1/1 | 4/6 | 3850/3400 | OK |
| Another 6k (3) | Pam Tender | Keystone Destroyer Class | 445.0 | match | 1/1 | 4/6 | 3850/3400 | OK |
| Another 6k (3) | Chicken Tender | Keystone Destroyer Class | 445.0 | match | 1/1 | 4/6 | 3850/3400 | OK |
| Another 6k | Tam Tember | Keystone Destroyer Class | 445.0 | match | 1/1 | 4/6 | 3850/3400 | OK |
| Another 6k | Ten Dender | Keystone Destroyer Class | 445.0 | match | 1/1 | 4/6 | 3850/3400 | OK |
| 等 | 共 79 艘 | | | | | | |

## Rail DD（400-800，共 20 艘）

| 舰队 | 舰名 | 舰体 | 点数 | 判定 | 本类 must | 通用 must | 耗电/供电 (kW) | (n-1) 判定 |
|---|---|---|---:|---|---|---|---|---|
| All 34 sample ships · Alliance | BFG | Keystone Destroyer Class | 452.0 | match | 1/1 | 4/6 | 4000/4700 | OK |
| hc gun dd test 11 | BFG | Keystone Destroyer Class | 453.0 | match | 1/1 | 4/6 | 4000/4700 | OK |
| TF Redwood | Singing Mantle | Keystone Destroyer Class | 465.0 | match | 1/1 | 4/6 | 4800/4700 | OK |
| All 34 sample ships · Alliance | BFR | Keystone Destroyer Class | 465.0 | match | 1/1 | 4/6 | 4000/4700 | OK |
| hc gun dd test 11 | BFR | Keystone Destroyer Class | 466.0 | match | 1/1 | 4/6 | 4000/4700 | OK |
| TF Redwood | Rime of Solitas | Keystone Destroyer Class | 490.0 | match | 1/1 | 5/6 | 6100/6950 | OK |
| Concept 5 | Concept | Keystone Destroyer Class | 498.0 | match | 1/1 | 4/6 | 4200/4700 | OK |
| Concept 5 | Concept | Keystone Destroyer Class | 498.0 | match | 1/1 | 4/6 | 4200/4700 | OK |
| Atonement squadran | Alloy | Keystone Destroyer Class | 557.0 | match | 1/1 | 4/6 | 4350/4700 | OK |
| Atonement squadran | Anger | Keystone Destroyer Class | 557.0 | match | 1/1 | 4/6 | 4350/4700 | OK |
| Atonement squadran | Art | Keystone Destroyer Class | 557.0 | match | 1/1 | 4/6 | 4350/4700 | OK |
| Atonement squadran | Arson | Keystone Destroyer Class | 557.0 | match | 1/1 | 4/6 | 4350/4700 | OK |
| Concept 5 | Concept | Keystone Destroyer Class | 655.0 | match | 1/1 | 6/6 | 6275/6950 | OK |
| Concept 5 | Concept | Keystone Destroyer Class | 655.0 | match | 1/1 | 6/6 | 6275/6950 | OK |
| 等 | 共 6 艘 | | | | | | |

## 250 gun CL（800-1200，共 38 艘）

| 舰队 | 舰名 | 舰体 | 点数 | 判定 | 本类 must | 通用 must | 耗电/供电 (kW) | (n-1) 判定 |
|---|---|---|---:|---|---|---|---|---|
| 比赛CL | The Rosy Boy | Vauxhall Light Cruiser Class | 800.0 | match | 1/1 | 5/6 | 3800/5700 | OK |
| TF Ponthera | Cringetino | Vauxhall Light Cruiser Class | 866.0 | match | 1/1 | 6/6 | 5750/7450 | OK |
| Guards Division 12k | CL-279 | Vauxhall Light Cruiser Class | 932.0 | match | 1/1 | 6/6 | 4125/5650 | OK |
| Guards Division 12k | CL-280 | Vauxhall Light Cruiser Class | 932.0 | match | 1/1 | 6/6 | 4125/5650 | OK |
| Guards Division 12k | CL-282 | Vauxhall Light Cruiser Class | 939.0 | match | 1/1 | 6/6 | 4700/5650 | OK |
| Guards Division 12k | CL-283 | Vauxhall Light Cruiser Class | 939.0 | match | 1/1 | 6/6 | 4700/5650 | OK |
| The Night Dances new | Cold Folds of Ego | Vauxhall Light Cruiser Class | 968.0 | match | 1/1 | 6/6 | 5305/4700 | OK |
| 1101 CL | Impact | Vauxhall Light Cruiser Class | 976.0 | match | 1/1 | 6/6 | 5425/5650 | OK |
| 1101 CL | Despair | Vauxhall Light Cruiser Class | 976.0 | match | 1/1 | 6/6 | 5425/5650 | OK |
| jam CL dad | Drier of Marilu | Vauxhall Light Cruiser Class | 984.0 | match | 1/1 | 6/6 | 5355/4700 | OK |
| The Night Dances new | A Spread of Hot Petals | Vauxhall Light Cruiser Class | 995.0 | match | 1/1 | 6/6 | 5455/4700 | OK |
| 1101 CL | Impede | Vauxhall Light Cruiser Class | 1002.0 | match | 1/1 | 6/6 | 5375/5650 | OK |
| 1101 CL | Suffering | Vauxhall Light Cruiser Class | 1002.0 | match | 1/1 | 6/6 | 5375/5650 | OK |
| All 34 sample ships · Alliance | Impede | Vauxhall Light Cruiser Class | 1002.0 | match | 1/1 | 6/6 | 5375/5650 | OK |
| 等 | 共 24 艘 | | | | | | |

## 120 gun CL（0-0，共 1 艘）

| 舰队 | 舰名 | 舰体 | 点数 | 判定 | 本类 must | 通用 must | 耗电/供电 (kW) | (n-1) 判定 |
|---|---|---|---:|---|---|---|---|---|
| Mothballed ships | Shin | Vauxhall Light Cruiser Class | 406.0 | bad_class | 1/1 | 5/6 | 2050/5200 | OK |

## missile CL（0-0，共 2 艘）

| 舰队 | 舰名 | 舰体 | 点数 | 判定 | 本类 must | 通用 must | 耗电/供电 (kW) | (n-1) 判定 |
|---|---|---|---:|---|---|---|---|---|
| 'We can fix her' (3) | Novel Bookmark | Vauxhall Light Cruiser Class | 2961.0 | bad_class | 1/1 | 4/6 | 8450/5700 | (n-1) 可关 |
| Testbulous | Novel Bookmark | Vauxhall Light Cruiser Class | 3000.0 | bad_class | 1/1 | 4/6 | 8300/5700 | (n-1) 可关 |

## gun MN（450-650，共 51 艘）

| 舰队 | 舰名 | 舰体 | 点数 | 判定 | 本类 must | 通用 must | 耗电/供电 (kW) | (n-1) 判定 |
|---|---|---|---:|---|---|---|---|---|
| Literal shit | Shit 6 | Flathead Monitor Class | 425.0 | match 偏低 | 1/1 | 5/6 | 3840/3950 | OK |
| Literal shit | Shit 7 | Flathead Monitor Class | 425.0 | match 偏低 | 1/1 | 5/6 | 3840/3950 | OK |
| Literal shit | Shit 2 | Flathead Monitor Class | 426.0 | match 偏低 | 1/1 | 5/6 | 3840/3950 | OK |
| Literal shit | Shit 3 | Flathead Monitor Class | 426.0 | match 偏低 | 1/1 | 5/6 | 3840/3950 | OK |
| Literal shit | Shit 4 | Flathead Monitor Class | 426.0 | match 偏低 | 1/1 | 5/6 | 3840/3950 | OK |
| Literal shit | Shit 5 | Flathead Monitor Class | 426.0 | match 偏低 | 1/1 | 5/6 | 3840/3950 | OK |
| emmmmmmmm | Jkterjter | Flathead Monitor Class | 435.0 | match 偏低 | 1/1 | 5/6 | 3890/5800 | OK |
| emmmmmmmm | Jkterjter | Flathead Monitor Class | 435.0 | match 偏低 | 1/1 | 5/6 | 3890/5800 | OK |
| emmmmmmmm | Jkterjter | Flathead Monitor Class | 435.0 | match 偏低 | 1/1 | 5/6 | 3890/5800 | OK |
| emmmmmmmm | Jkterjter | Flathead Monitor Class | 435.0 | match 偏低 | 1/1 | 5/6 | 3890/5800 | OK |
| emmmmmmmm | Jkterjter | Flathead Monitor Class | 435.0 | match 偏低 | 1/1 | 5/6 | 3890/5800 | OK |
| emmmmmmmm | Folly | Flathead Monitor Class | 435.0 | match 偏低 | 1/1 | 5/6 | 3890/5800 | OK |
| emmmmmmmm | Wrong | Flathead Monitor Class | 435.0 | match 偏低 | 1/1 | 5/6 | 3890/5800 | OK |
| Literal shit | Shit 1 | Flathead Monitor Class | 446.0 | match 偏低 | 1/1 | 5/6 | 4340/5300 | OK |
| 等 | 共 37 艘 | | | | | | |

## S2 MN（800-1500，共 2 艘）

| 舰队 | 舰名 | 舰体 | 点数 | 判定 | 本类 must | 通用 must | 耗电/供电 (kW) | (n-1) 判定 |
|---|---|---|---:|---|---|---|---|---|
| Tantalum Squadron | Time Dilation | Flathead Monitor Class | 969.0 | match | 2/2 | 4/6 | 1500/3850 | OK |
| 💩 | Box 36 | Flathead Monitor Class | 1785.0 | match 偏高 | 2/2 | 4/6 | 1100/2250 | OK |

## EWR MN（0-0，共 1 艘）

| 舰队 | 舰名 | 舰体 | 点数 | 判定 | 本类 must | 通用 must | 耗电/供电 (kW) | (n-1) 判定 |
|---|---|---|---:|---|---|---|---|---|
| Heteroteuthinae | Iridoteuthis | Flathead Monitor Class | 503.0 | bad_class | 1/1 | 3/6 | 8200/7150 | (n-1) 可关 |

## 450 CH（1400-1600，共 54 艘）

| 舰队 | 舰名 | 舰体 | 点数 | 判定 | 本类 must | 通用 must | 耗电/供电 (kW) | (n-1) 判定 |
|---|---|---|---:|---|---|---|---|---|
| Two 450 CH (v2) | Two 450 CH (v2) 1 | Axford Heavy Cruiser Class | 1170.0 | match 偏低 | 1/1 | 5/6 | 5155/11850 | OK |
| Two 450 CH (v2) | Two 450 CH (v2) 2 | Axford Heavy Cruiser Class | 1170.0 | match 偏低 | 1/1 | 5/6 | 5155/11850 | OK |
| 450 CH (KB-only build) | 450 CH (KB-only build) 1 | Axford Heavy Cruiser Class | 1340.0 | match 偏低 | 1/1 | 6/6 | 5915/7600 | OK |
| TF Pilgrim | Dragonfall | Axford Heavy Cruiser Class | 1411.0 | match | 1/1 | 6/6 | 5855/6200 | OK |
| HC Gun test 4 | Equility-On-Sea | Axford Heavy Cruiser Class | 1433.0 | match | 1/1 | 6/6 | 8380/8900 | OK |
| greedford | York Supreme | Axford Heavy Cruiser Class | 1440.0 | match [greed CH / 450 CH] | 2/2 | 6/6 | 7500/7600 | OK |
| All 34 sample ships · Alliance | Equility-On-Sea | Axford Heavy Cruiser Class | 1442.0 | match [greed CH / 450 CH] | 2/2 | 6/6 | 8350/9850 | OK |
| Tactical Fish Division 5.0 | Flamewhisker | Axford Heavy Cruiser Class | 1454.0 | match | 1/1 | 6/6 | 7155/6200 | (n-1) 可关 |
| 2- bb and 3dd ish 1 | Waowa Ponthera | Axford Heavy Cruiser Class | 1460.0 | match | 1/1 | 6/6 | 7240/9900 | OK |
| rail test | Food of Nelsen | Axford Heavy Cruiser Class | 1463.0 | match | 1/1 | 6/6 | 6805/6200 | OK |
| rail test | Caper | Axford Heavy Cruiser Class | 1463.0 | match | 1/1 | 6/6 | 6805/6200 | OK |
| rail test | Gavel and Graze | Axford Heavy Cruiser Class | 1463.0 | match | 1/1 | 6/6 | 6805/6200 | OK |
| 新手舰队2CH | 先驱 | Axford Heavy Cruiser Class | 1468.0 | match | 1/1 | 6/6 | 8435/9400 | OK |
| 新手舰队2CH | 先驱 | Axford Heavy Cruiser Class | 1468.0 | match | 1/1 | 6/6 | 8435/9400 | OK |
| 等 | 共 40 艘 | | | | | | |

## greed CH（1400-1600，共 6 艘）

| 舰队 | 舰名 | 舰体 | 点数 | 判定 | 本类 must | 通用 must | 耗电/供电 (kW) | (n-1) 判定 |
|---|---|---|---:|---|---|---|---|---|
| greedford | York Supreme | Axford Heavy Cruiser Class | 1440.0 | match [greed CH / 450 CH] | 2/2 | 6/6 | 7500/7600 | OK |
| All 34 sample ships · Alliance | Equility-On-Sea | Axford Heavy Cruiser Class | 1442.0 | match [greed CH / 450 CH] | 2/2 | 6/6 | 8350/9850 | OK |
| All 34 sample ships · Alliance | |||||||| | Axford Heavy Cruiser Class | 1501.0 | match [greed CH / 450 CH] | 2/2 | 6/6 | 8875/12100 | OK |
| concept | |||||||| | Axford Heavy Cruiser Class | 1502.0 | match [greed CH / 450 CH] | 2/2 | 6/6 | 8875/12100 | OK |
| greedford | Equility-On-Sea | Axford Heavy Cruiser Class | 1560.0 | match [greed CH / 450 CH] | 2/2 | 6/6 | 8350/9850 | OK |
| White Fox and her doggos | Fubuki | Axford Heavy Cruiser Class | 1600.0 | match [greed CH / 450 CH] | 2/2 | 6/6 | 8100/9850 | OK |

## 250 CH（0-0，共 1 艘）

| 舰队 | 舰名 | 舰体 | 点数 | 判定 | 本类 must | 通用 must | 耗电/供电 (kW) | (n-1) 判定 |
|---|---|---|---:|---|---|---|---|---|
| masqford | The Wacky Joy | Axford Heavy Cruiser Class | 1430.0 | bad_class | 1/1 | 6/6 | 6485/8550 | OK |

## Command Cruiser killer (CCK) CH（1600-3000，共 6 艘）

| 舰队 | 舰名 | 舰体 | 点数 | 判定 | 本类 must | 通用 must | 耗电/供电 (kW) | (n-1) 判定 |
|---|---|---|---:|---|---|---|---|---|
| Meh 6k | Sakana | Axford Heavy Cruiser Class | 1733.0 | match | 2/2 | 6/6 | 6705/6200 | OK |
| TF Redwood | Star of Atlas | Axford Heavy Cruiser Class | 1825.0 | match | 2/2 | 6/6 | 9850/8900 | OK |
| hc gun dd test 11 | LOADER 4 | Axford Heavy Cruiser Class | 2062.0 | match | 2/2 | 6/6 | 8725/8900 | OK |
| hc gun dd test 11 | LOADER 4 | Axford Heavy Cruiser Class | 2064.0 | match | 2/2 | 6/6 | 8675/8900 | OK |
| hc gun dd test 11 | LOADER 4 | Axford Heavy Cruiser Class | 2073.0 | match | 2/2 | 6/6 | 8675/8900 | OK |
| HC Gun Missile test 8 | LOADER 4 | Axford Heavy Cruiser Class | 2218.0 | match | 2/2 | 6/6 | 9175/9900 | OK |

## missile CH（2000-3000，共 6 艘）

| 舰队 | 舰名 | 舰体 | 点数 | 判定 | 本类 must | 通用 must | 耗电/供电 (kW) | (n-1) 判定 |
|---|---|---|---:|---|---|---|---|---|
| Shock CH test | LOADER 4 | Axford Heavy Cruiser Class | 2825.0 | match | 2/2 | 5/6 | 5900/6800 | OK |
| TF Hemlock | Totem | Axford Heavy Cruiser Class | 3000.0 | match | 2/2 | 6/6 | 9425/9850 | OK |
| HC Missile test 7 | LOADER 4 | Axford Heavy Cruiser Class | 3000.0 | match | 2/2 | 6/6 | 12600/11150 | OK |
| S2CH | Diesal Summer | Axford Heavy Cruiser Class | 3000.0 | match [S2CH / missile CH] | 1/1 | 4/6 | 8900/6800 | OK |
| Shock 12k | The Nameless Gambit | Axford Heavy Cruiser Class | 3091.0 | match 偏高 | 2/2 | 5/6 | 5900/6800 | OK |
| Blindness | Diesal Summer | Axford Heavy Cruiser Class | 3414.0 | match 偏高 | 2/2 | 5/6 | 8530/6800 | OK |

## S2CH（2500-3000，共 1 艘）

| 舰队 | 舰名 | 舰体 | 点数 | 判定 | 本类 must | 通用 must | 耗电/供电 (kW) | (n-1) 判定 |
|---|---|---|---:|---|---|---|---|---|
| S2CH | Diesal Summer | Axford Heavy Cruiser Class | 3000.0 | match [S2CH / missile CH] | 1/1 | 4/6 | 8900/6800 | OK |

## 450 CC（1400-1600，共 48 艘）

| 舰队 | 舰名 | 舰体 | 点数 | 判定 | 本类 must | 通用 must | 耗电/供电 (kW) | (n-1) 判定 |
|---|---|---|---:|---|---|---|---|---|
| CC maxxing | Hawk | Ocello Command Cruiser Class | 1248.0 | match 偏低 | 1/1 | 6/6 | 6850/9400 | OK |
| CC maxxing | Wall and Song | Ocello Command Cruiser Class | 1248.0 | match 偏低 | 1/1 | 6/6 | 6850/9400 | OK |
| CC maxxing | Noble | Ocello Command Cruiser Class | 1248.0 | match 偏低 | 1/1 | 6/6 | 6850/9400 | OK |
| Rush B | CC Gun 3 | Ocello Command Cruiser Class | 1394.0 | match 偏低 | 1/1 | 6/6 | 10380/9900 | OK |
| Rush B | CC Gun 9 | Ocello Command Cruiser Class | 1394.0 | match 偏低 | 1/1 | 6/6 | 10380/9900 | OK |
| All 27 sample ships · Protectorate | Above Chunk | Ocello Command Cruiser Class | 1456.0 | match | 1/1 | 6/6 | 10500/10350 | OK |
| All 27 sample ships · Protectorate | Delta of Maddy | Ocello Command Cruiser Class | 1456.0 | match | 1/1 | 6/6 | 10500/10350 | OK |
| CC maxxing | Delta of Maddy | Ocello Command Cruiser Class | 1457.0 | match | 1/1 | 6/6 | 10500/10350 | OK |
| CC maxxing | Above Chunk | Ocello Command Cruiser Class | 1457.0 | match | 1/1 | 6/6 | 10500/10350 | OK |
| CC maxxing | Mauve Flag | Ocello Command Cruiser Class | 1457.0 | match | 1/1 | 6/6 | 10500/10350 | OK |
| CCCC | Ill Sixty | Ocello Command Cruiser Class | 1461.0 | match | 1/1 | 6/6 | 11450/13250 | OK |
| 新手舰队2CC | 先驱-E | Ocello Command Cruiser Class | 1462.0 | match | 1/1 | 6/6 | 11975/9400 | (n-1) 可关 |
| Rush B | CC Gun 2 | Ocello Command Cruiser Class | 1464.0 | match | 1/1 | 6/6 | 10480/9900 | OK |
| Rush B | CC Gun 8 | Ocello Command Cruiser Class | 1464.0 | match | 1/1 | 6/6 | 10480/9900 | OK |
| 等 | 共 34 艘 | | | | | | |

## 250 CC（0-0，共 3 艘）

| 舰队 | 舰名 | 舰体 | 点数 | 判定 | 本类 must | 通用 must | 耗电/供电 (kW) | (n-1) 判定 |
|---|---|---|---:|---|---|---|---|---|
| CC maxxing | Hello | Ocello Command Cruiser Class | 1201.0 | bad_class | 1/1 | 6/6 | 5040/5900 | OK |
| CC maxxing | Grit and Ark | Ocello Command Cruiser Class | 1201.0 | bad_class | 1/1 | 6/6 | 5040/5900 | OK |
| CC maxxing | Sharai E. Naamann | Ocello Command Cruiser Class | 1291.0 | bad_class | 1/1 | 6/6 | 5040/5900 | OK |

## missile CC（2000-3000，共 12 艘）

| 舰队 | 舰名 | 舰体 | 点数 | 判定 | 本类 must | 通用 must | 耗电/供电 (kW) | (n-1) 判定 |
|---|---|---|---:|---|---|---|---|---|
| Azurite Squadron | Abject Terror | Ocello Command Cruiser Class | 2170.0 | match | 2/2 | 5/6 | 9150/9850 | OK |
| tesdt | Grand Basal | Ocello Command Cruiser Class | 2543.0 | match [S2CC / missile CC] | 1/1 | 5/6 | 11750/7650 | OK |
| S2 DIR OCELLO | Nuclear Summer | Ocello Command Cruiser Class | 3000.0 | match [missile CC / S2CC] | 2/2 | 5/6 | 11800/11500 | OK |
| Helplessness | Nuclear Spring | Ocello Command Cruiser Class | 3000.0 | match [S2CC / missile CC] | 1/1 | 5/6 | 11900/11500 | OK |
| Helplessness | Nuclear Autumn | Ocello Command Cruiser Class | 3000.0 | match [S2CC / missile CC] | 1/1 | 5/6 | 11900/11500 | OK |
| S2 DIR OCELLO | Command Cruiser Must Command | Ocello Command Cruiser Class | 3000.0 | match [S2CC / missile CC] | 1/1 | 5/6 | 11900/11500 | OK |
| 4 S2CC | Dark | Ocello Command Cruiser Class | 3000.0 | match [S2CC / missile CC] | 1/1 | 4/6 | 12050/11500 | OK |
| 4 S2CC | Batch and Gland | Ocello Command Cruiser Class | 3000.0 | match [S2CC / missile CC] | 1/1 | 4/6 | 12050/11500 | OK |
| 4 S2CC | Medic | Ocello Command Cruiser Class | 3000.0 | match [S2CC / missile CC] | 1/1 | 4/6 | 12050/11500 | OK |
| 4 S2CC | Jug Four | Ocello Command Cruiser Class | 3000.0 | match [S2CC / missile CC] | 1/1 | 4/6 | 12050/11500 | OK |
| S2CC MkII | HATSUNE | Ocello Command Cruiser Class | 3000.0 | match [S2CC / missile CC] | 1/1 | 4/6 | 11800/11000 | OK |
| Linear inf | BULWARK | Ocello Command Cruiser Class | 3400.0 | match 偏高 | 2/2 | 5/6 | 11650/11500 | OK |

## S2CC（2000-3000，共 10 艘）

| 舰队 | 舰名 | 舰体 | 点数 | 判定 | 本类 must | 通用 must | 耗电/供电 (kW) | (n-1) 判定 |
|---|---|---|---:|---|---|---|---|---|
| tesdt | Grand Basal | Ocello Command Cruiser Class | 2543.0 | match [S2CC / missile CC] | 1/1 | 5/6 | 11750/7650 | OK |
| S2 DIR OCELLO | Nuclear Summer | Ocello Command Cruiser Class | 3000.0 | match [missile CC / S2CC] | 2/2 | 5/6 | 11800/11500 | OK |
| Helplessness | Nuclear Spring | Ocello Command Cruiser Class | 3000.0 | match [S2CC / missile CC] | 1/1 | 5/6 | 11900/11500 | OK |
| Helplessness | Nuclear Autumn | Ocello Command Cruiser Class | 3000.0 | match [S2CC / missile CC] | 1/1 | 5/6 | 11900/11500 | OK |
| S2 DIR OCELLO | Command Cruiser Must Command | Ocello Command Cruiser Class | 3000.0 | match [S2CC / missile CC] | 1/1 | 5/6 | 11900/11500 | OK |
| 4 S2CC | Dark | Ocello Command Cruiser Class | 3000.0 | match [S2CC / missile CC] | 1/1 | 4/6 | 12050/11500 | OK |
| 4 S2CC | Batch and Gland | Ocello Command Cruiser Class | 3000.0 | match [S2CC / missile CC] | 1/1 | 4/6 | 12050/11500 | OK |
| 4 S2CC | Medic | Ocello Command Cruiser Class | 3000.0 | match [S2CC / missile CC] | 1/1 | 4/6 | 12050/11500 | OK |
| 4 S2CC | Jug Four | Ocello Command Cruiser Class | 3000.0 | match [S2CC / missile CC] | 1/1 | 4/6 | 12050/11500 | OK |
| S2CC MkII | HATSUNE | Ocello Command Cruiser Class | 3000.0 | match [S2CC / missile CC] | 1/1 | 4/6 | 11800/11000 | OK |

## Rail CC（1200-1600，共 6 艘）

| 舰队 | 舰名 | 舰体 | 点数 | 判定 | 本类 must | 通用 must | 耗电/供电 (kW) | (n-1) 判定 |
|---|---|---|---:|---|---|---|---|---|
| Heteroteuthinae | Nectoteuthis | Ocello Command Cruiser Class | 1065.0 | match 偏低 | 1/1 | 5/6 | 8350/6500 | OK |
| Meteror Rain Project | Aware Rule | Ocello Command Cruiser Class | 1431.0 | match | 1/1 | 6/6 | 17150/13750 | OK |
| md maxxing | Aware Rule | Ocello Command Cruiser Class | 1506.0 | match | 1/1 | 6/6 | 17150/13750 | OK |
| md maxxing | Curl Dim | Ocello Command Cruiser Class | 1506.0 | match | 1/1 | 6/6 | 17150/13750 | OK |
| Comet Squadron | Hoshimachi | Ocello Command Cruiser Class | 1529.0 | match | 1/1 | 6/6 | 19100/14400 | OK |
| All 27 sample ships · Protectorate | Hoshimachi | Ocello Command Cruiser Class | 1579.0 | match | 1/1 | 6/6 | 19100/14400 | OK |

## 450 BB（2000-3000，共 34 艘）

| 舰队 | 舰名 | 舰体 | 点数 | 判定 | 本类 must | 通用 must | 耗电/供电 (kW) | (n-1) 判定 |
|---|---|---|---:|---|---|---|---|---|
| 1-bb more baofan 2 | Miner Arch | Solomon Battleship Class | 2039.0 | match | 1/1 | 6/6 | 8950/10900 | OK |
| TF Ponthera | Waowa Ponthera | Solomon Battleship Class | 2134.0 | match | 1/1 | 6/6 | 6460/6700 | OK |
| 1-bb less but effective baofan | Miner Arch | Solomon Battleship Class | 2193.0 | match | 1/1 | 6/6 | 9630/10900 | OK |
| Meh 6k | Waowa Ponthera | Solomon Battleship Class | 2264.0 | match | 1/1 | 6/6 | 9100/9550 | OK |
| Funni 6k | Waowa Ponthera | Solomon Battleship Class | 2264.0 | match | 1/1 | 6/6 | 9100/9550 | OK |
| TF Ponthera (3) | Waowa Ponthera | Solomon Battleship Class | 2264.0 | match | 1/1 | 6/6 | 9100/9550 | OK |
| TF Ponthera (2) | Waowa Ponthera | Solomon Battleship Class | 2269.0 | match | 1/1 | 6/6 | 12550/11200 | OK |
| All 34 sample ships · Alliance | Billion Lightyear | Solomon Battleship Class | 2319.0 | match [450 BB / TCSG BB] | 1/1 | 6/6 | 8620/8600 | OK |
| Meh 6k duo | Waowa Ponthera | Solomon Battleship Class | 2325.0 | match | 1/1 | 6/6 | 9100/9550 | OK |
| BB 12k | Merak | Solomon Battleship Class | 2362.0 | match | 1/1 | 6/6 | 8440/7300 | (n-1) 可关 |
| BB 12k | Megrez | Solomon Battleship Class | 2362.0 | match | 1/1 | 6/6 | 8440/7300 | (n-1) 可关 |
| Concept 5 | Concept | Solomon Battleship Class | 2362.0 | match | 1/1 | 6/6 | 8440/7300 | (n-1) 可关 |
| BB 12k | Dubhe | Solomon Battleship Class | 2382.0 | match | 1/1 | 6/6 | 8040/7300 | OK |
| BB 12k | Phecda | Solomon Battleship Class | 2382.0 | match | 1/1 | 6/6 | 8040/7300 | OK |
| 等 | 共 20 艘 | | | | | | |

## TCSG BB（2000-3000，共 6 艘）

| 舰队 | 舰名 | 舰体 | 点数 | 判定 | 本类 must | 通用 must | 耗电/供电 (kW) | (n-1) 判定 |
|---|---|---|---:|---|---|---|---|---|
| All 34 sample ships · Alliance | Billion Lightyear | Solomon Battleship Class | 2319.0 | match [450 BB / TCSG BB] | 1/1 | 6/6 | 8620/8600 | OK |
| BB test 55 Newbie | Billion Lightyear | Solomon Battleship Class | 2527.0 | match [450 BB / TCSG BB] | 1/1 | 6/6 | 8620/8600 | OK |
| All 34 sample ships · Alliance | Glans and Burns | Solomon Battleship Class | 2580.0 | match [TCSG BB / 450 BB] | 2/2 | 6/6 | 8625/7700 | (n-1) 可关 |
| test | Glans and Burns | Solomon Battleship Class | 2690.0 | match [TCSG BB / 450 BB] | 2/2 | 6/6 | 8625/7700 | (n-1) 可关 |
| Funni 6k | Fairy of AKIBerse | Solomon Battleship Class | 3000.0 | match [450 BB / TCSG BB] | 1/1 | 6/6 | 12350/11800 | OK |
| TF Fairy (2) | Fairy of AKIBerse | Solomon Battleship Class | 3000.0 | match [450 BB / TCSG BB] | 1/1 | 6/6 | 12350/11800 | OK |

## Beam BB（1900-3000，共 7 艘）

| 舰队 | 舰名 | 舰体 | 点数 | 判定 | 本类 must | 通用 must | 耗电/供电 (kW) | (n-1) 判定 |
|---|---|---|---:|---|---|---|---|---|
| please don't play this | Ibuprofen | Solomon Battleship Class | 2060.0 | match | 1/1 | 6/6 | 17076/17150 | OK |
| beme | Strong the roots Dick | Solomon Battleship Class | 2338.0 | match | 1/1 | 6/6 | 17740/16700 | OK |
| beme | Strong the roots Whilly | Solomon Battleship Class | 2338.0 | match | 1/1 | 6/6 | 17740/16700 | OK |
| All 34 sample ships · Alliance | Strong the roots Dick | Solomon Battleship Class | 2338.0 | match | 1/1 | 6/6 | 17740/16700 | OK |
| All 34 sample ships · Alliance | Strong the roots Whilly | Solomon Battleship Class | 2338.0 | match | 1/1 | 6/6 | 17740/16700 | OK |
| Blindness | Solar Summer | Solomon Battleship Class | 2385.0 | match | 1/1 | 5/6 | 11740/8300 | 超载 |
| New Beam BB | Pretty Lights | Solomon Battleship Class | 2508.0 | match | 1/1 | 6/6 | 19100/19900 | OK |

## rail BB（0-0，共 1 艘）

| 舰队 | 舰名 | 舰体 | 点数 | 判定 | 本类 must | 通用 must | 耗电/供电 (kW) | (n-1) 判定 |
|---|---|---|---:|---|---|---|---|---|
| TF Libra | Dooby Nights | Solomon Battleship Class | 2612.0 | bad_class | 1/1 | 6/6 | 18600/15700 | (n-1) 可关 |

## 450 ln（1100-1300，共 25 艘）

| 舰队 | 舰名 | 舰体 | 点数 | 判定 | 本类 must | 通用 must | 耗电/供电 (kW) | (n-1) 判定 |
|---|---|---|---:|---|---|---|---|---|
| Nice balance fuck u testulous | Damp of Penelopa | Marauder Line Ship Class | 750.0 | match 偏低 | 1/1 | 5/6 | 2221/3950 | OK |
| Nice balance fuck u testulous | Genoa Micro | Marauder Line Ship Class | 750.0 | match 偏低 | 1/1 | 5/6 | 2221/3950 | OK |
| Nice balance fuck u testulous | Arrow of Mala | Marauder Line Ship Class | 750.0 | match 偏低 | 1/1 | 5/6 | 2221/3950 | OK |
| Nice balance fuck u testulous | Axial Roast | Marauder Line Ship Class | 750.0 | match 偏低 | 1/1 | 5/6 | 2221/3950 | OK |
| TF-6k | CM-4D2 Decoy Container | Marauder Line Ship Class | 780.0 | match 偏低 | 1/1 | 5/6 | 2100/3950 | OK |
| TF-6k | CM-4D2 Decoy Container | Marauder Line Ship Class | 780.0 | match 偏低 | 1/1 | 5/6 | 2100/3950 | OK |
| TF-6k | CM-4D2 Decoy Container | Marauder Line Ship Class | 780.0 | match 偏低 | 1/1 | 5/6 | 2100/3950 | OK |
| TF-6k | CM-4D2 Decoy Container | Marauder Line Ship Class | 780.0 | match 偏低 | 1/1 | 5/6 | 2100/3950 | OK |
| TF-M | CM-4D2 Decoy Container | Marauder Line Ship Class | 780.0 | match 偏低 | 1/1 | 5/6 | 2100/3950 | OK |
| TF-M | CM-4D2 Decoy Container | Marauder Line Ship Class | 780.0 | match 偏低 | 1/1 | 5/6 | 2100/3950 | OK |
| TF-M | CM-4D2 Decoy Container | Marauder Line Ship Class | 780.0 | match 偏低 | 1/1 | 5/6 | 2100/3950 | OK |
| TF-M | CM-4D2 Decoy Container | Marauder Line Ship Class | 780.0 | match 偏低 | 1/1 | 5/6 | 2100/3950 | OK |
| Linear inf | BULWARK | Marauder Line Ship Class | 840.0 | match 偏低 | 1/1 | 5/6 | 3490/3950 | OK |
| Linear inf | BULWARK | Marauder Line Ship Class | 840.0 | match 偏低 | 1/1 | 5/6 | 3490/3950 | OK |
| 等 | 共 11 艘 | | | | | | |

## 250 ln（900-1100，共 9 艘）

| 舰队 | 舰名 | 舰体 | 点数 | 判定 | 本类 must | 通用 must | 耗电/供电 (kW) | (n-1) 判定 |
|---|---|---|---:|---|---|---|---|---|
| lights test | CM-4D2 Decoy Container | Marauder Line Ship Class | 681.0 | match 偏低 | 1/1 | 5/6 | 350/600 | OK |
| LIGHT 2.0 | CM-4D2 Decoy Container | Marauder Line Ship Class | 681.0 | match 偏低 | 1/1 | 5/6 | 350/600 | OK |
| LIGHT 2.0 | CM-4D2 Decoy Container | Marauder Line Ship Class | 681.0 | match 偏低 | 1/1 | 5/6 | 350/600 | OK |
| LIGHT 2.0 | CM-4D2 Decoy Container | Marauder Line Ship Class | 681.0 | match 偏低 | 1/1 | 5/6 | 350/600 | OK |
| LIGHT 2.0 | CM-4D2 Decoy Container | Marauder Line Ship Class | 681.0 | match 偏低 | 1/1 | 5/6 | 350/600 | OK |
| TF Purple Joy 2 | Lazy Count | Marauder Line Ship Class | 1192.0 | match 偏高 | 1/1 | 5/6 | 8780/9000 | OK |
| TF Purple Joy 2 | Bush Magic | Marauder Line Ship Class | 1192.0 | match 偏高 | 1/1 | 5/6 | 8780/9000 | OK |
| TF Purple Joy 2 | Lazy Count | Marauder Line Ship Class | 1197.0 | match 偏高 | 1/1 | 5/6 | 8780/9000 | OK |
| TF Purple Joy 2 | Overt Lefty | Marauder Line Ship Class | 1197.0 | match 偏高 | 1/1 | 5/6 | 8780/9000 | OK |

## missle ln（1400-3000，共 14 艘）

| 舰队 | 舰名 | 舰体 | 点数 | 判定 | 本类 must | 通用 must | 耗电/供电 (kW) | (n-1) 判定 |
|---|---|---|---:|---|---|---|---|---|
| Rocket Shuttles but bigger | Ever Lovely | Marauder Line Ship Class | 1499.0 | match | 2/2 | 4/6 | 2850/400 | 超载 |
| Rocket Shuttles but bigger | The Lousy Puppy | Marauder Line Ship Class | 1501.0 | match | 2/2 | 4/6 | 2850/400 | 超载 |
| dum shi | Nuclear Summer | Marauder Line Ship Class | 2378.0 | match | 2/2 | 4/6 | 1600/3950 | OK |
| dat shi | Bishop L | Marauder Line Ship Class | 2481.0 | match | 2/2 | 4/6 | 1600/3950 | OK |
| dat shi | Bishop D | Marauder Line Ship Class | 2481.0 | match | 2/2 | 4/6 | 1600/3950 | OK |
| msl ln test | Corps of Kalil | Marauder Line Ship Class | 2713.0 | match | 2/2 | 4/6 | 1600/3950 | OK |
| dum shi | Bishop W | Marauder Line Ship Class | 2829.0 | match | 2/2 | 4/6 | 1600/3950 | OK |
| dum shi | Bishop B | Marauder Line Ship Class | 2829.0 | match | 2/2 | 4/6 | 1600/3950 | OK |
| Life Goes On LNG | Life Goes On | Marauder Line Ship Class | 3000.0 | match | 2/2 | 6/6 | 2820/3950 | OK |
| cmd test2 | Blot Out The Sun With Our Arrows | Marauder Line Ship Class | 3000.0 | match | 2/2 | 4/6 | 1650/3950 | OK |
| S2LN NEO | Blot Out The Sun With Our Arrows | Marauder Line Ship Class | 3000.0 | match | 2/2 | 6/6 | 2460/3950 | OK |
| cmd test | Carrie X. Madelene | Marauder Line Ship Class | 3004.0 | match 偏高 | 2/2 | 4/6 | 1600/3950 | OK |
| cmd test | Rachele F. Lach | Marauder Line Ship Class | 3004.0 | match 偏高 | 2/2 | 4/6 | 1600/3950 | OK |
| msl ln test | Value of Edita | Marauder Line Ship Class | 3121.0 | match 偏高 | 2/2 | 4/6 | 1600/3950 | OK |

## mass driver (md) ln（1000-1300，共 27 艘）

| 舰队 | 舰名 | 舰体 | 点数 | 判定 | 本类 must | 通用 must | 耗电/供电 (kW) | (n-1) 判定 |
|---|---|---|---:|---|---|---|---|---|
| Heteroteuthinae | Stoloteuthis | Marauder Line Ship Class | 979.0 | match 偏低 | 1/1 | 4/6 | 14850/10850 | OK |
| Meteror Rain Project | CM-4D2 Decoy Container | Marauder Line Ship Class | 1000.0 | match | 1/1 | 3/6 | 18950/12550 | 超载 |
| Meteror Rain Project | CM-4D2 Decoy Container | Marauder Line Ship Class | 1000.0 | match | 1/1 | 3/6 | 18950/12550 | 超载 |
| Meteror Rain Project | CM-4D2 Decoy Container | Marauder Line Ship Class | 1000.0 | match | 1/1 | 3/6 | 18950/12550 | 超载 |
| Meteror Rain Project | CM-4D2 Decoy Container | Marauder Line Ship Class | 1000.0 | match | 1/1 | 3/6 | 18950/12550 | 超载 |
| Meteror Rain Project | CM-4D2 Decoy Container | Marauder Line Ship Class | 1000.0 | match | 1/1 | 3/6 | 18950/12550 | 超载 |
| Meteror Rain Project | CM-4D2 Decoy Container | Marauder Line Ship Class | 1000.0 | match | 1/1 | 3/6 | 18950/12550 | 超载 |
| Meteror Rain Project | CM-4D2 Decoy Container | Marauder Line Ship Class | 1000.0 | match | 1/1 | 3/6 | 18950/12550 | 超载 |
| Meteror Rain Project | CM-4D2 Decoy Container | Marauder Line Ship Class | 1000.0 | match | 1/1 | 3/6 | 18950/12550 | 超载 |
| md maxxing | CM-4D2 Decoy Container | Marauder Line Ship Class | 1025.0 | match | 1/1 | 3/6 | 18950/12550 | 超载 |
| md maxxing | CM-4D2 Decoy Container | Marauder Line Ship Class | 1025.0 | match | 1/1 | 3/6 | 18950/12550 | 超载 |
| md maxxing | CM-4D2 Decoy Container | Marauder Line Ship Class | 1025.0 | match | 1/1 | 3/6 | 18950/12550 | 超载 |
| md maxxing | CM-4D2 Decoy Container | Marauder Line Ship Class | 1025.0 | match | 1/1 | 3/6 | 18950/12550 | 超载 |
| md maxxing | CM-4D2 Decoy Container | Marauder Line Ship Class | 1025.0 | match | 1/1 | 3/6 | 18950/12550 | 超载 |
| 等 | 共 13 艘 | | | | | | |

## half cve/cvl（1300-1700，共 23 艘）

| 舰队 | 舰名 | 舰体 | 点数 | 判定 | 本类 must | 通用 must | 耗电/供电 (kW) | (n-1) 判定 |
|---|---|---|---:|---|---|---|---|---|
| All 34 sample ships · Alliance | For Whutever | Levy Escort Carrier Class | 706.0 | match 偏低 | 0/0 | 4/6 | 600/1000 | OK |
| All 34 sample ships · Alliance | Whutever loves this | Levy Escort Carrier Class | 706.0 | match 偏低 | 0/0 | 4/6 | 600/1000 | OK |
| meat CV | Russell T. Hannon | Levy Escort Carrier Class | 799.0 | match 偏低 | 0/0 | 4/6 | 200/2150 | OK |
| All 34 sample ships · Alliance | Democratic Space Station | Levy Escort Carrier Class | 899.0 | match 偏低 | 0/0 | 4/6 | 4650/4700 | OK |
| All 34 sample ships · Alliance | Democratic Space Station | Levy Escort Carrier Class | 899.0 | match 偏低 | 0/0 | 5/6 | 4825/5200 | OK |
| please don't play this | Excedrin Migraine | Levy Escort Carrier Class | 940.0 | match 偏低 | 0/0 | 4/6 | 50/1000 | OK |
| Wulfenite Squadron | The Bar Is In Hell | Journeyman Light Carrier Class | 1252.0 | match 偏低 | 0/0 | 5/6 | 1281/3950 | OK |
| Wulfenite Squadron | More Is Never Less | Journeyman Light Carrier Class | 1252.0 | match 偏低 | 0/0 | 5/6 | 1281/3950 | OK |
| 2cvl  s3 6km | Tidal May | Journeyman Light Carrier Class | 1493.0 | match | 0/0 | 4/6 | 451/3950 | OK |
| CVE | For Whutever | Levy Escort Carrier Class | 1500.0 | match | 0/0 | 4/6 | 600/1000 | OK |
| CVE | Whutever loves this | Levy Escort Carrier Class | 1500.0 | match | 0/0 | 4/6 | 600/1000 | OK |
| AACV | Last Cup of Coffee | Levy Escort Carrier Class | 1500.0 | match | 0/0 | 5/6 | 3400/4700 | OK |
| AACV | Soak of Kerri | Levy Escort Carrier Class | 1500.0 | match | 0/0 | 5/6 | 3400/4700 | OK |
| 2cvl  s3 6km | Judge Rural | Journeyman Light Carrier Class | 1507.0 | match | 0/0 | 4/6 | 1651/3950 | OK |
| 等 | 共 9 艘 | | | | | | |

## full cve (ANS)（2000-3000，共 5 艘）

| 舰队 | 舰名 | 舰体 | 点数 | 判定 | 本类 must | 通用 must | 耗电/供电 (kW) | (n-1) 判定 |
|---|---|---|---:|---|---|---|---|---|
| CV test | Of Martial Build | Levy Escort Carrier Class | 2310.0 | match | 0/0 | 5/6 | 5200/5200 | OK |
| CVE test 33 SS2 | Democratic Space Station | Levy Escort Carrier Class | 3000.0 | match | 0/0 | 4/6 | 4650/4700 | OK |
| CVE test 34 S2 | Democratic Space Station | Levy Escort Carrier Class | 3000.0 | match | 0/0 | 5/6 | 4825/5200 | OK |
| CVE test 33 SS2 | Democratic Space Station | Levy Escort Carrier Class | 3000.0 | match | 0/0 | 5/6 | 4825/5200 | OK |
| TF Hope | Eternal Hope | Levy Escort Carrier Class | 3000.0 | match | 0/0 | 5/6 | 5400/7450 | OK |

## CLN (OSP)（2500-3000，共 31 艘）

| 舰队 | 舰名 | 舰体 | 点数 | 判定 | 本类 must | 通用 must | 耗电/供电 (kW) | (n-1) 判定 |
|---|---|---|---:|---|---|---|---|---|
| CLN x2 test | Ligma | Container Hauler Refit | 1500.0 | match 偏低 | 1/1 | 3/6 | 800/3950 | OK |
| CLN x2 test | Suckma | Container Hauler Refit | 1500.0 | match 偏低 | 1/1 | 3/6 | 800/3950 | OK |
| cmd test | Shanna F. Rosene | Container Hauler Refit | 2184.0 | match | 1/1 | 3/6 | 2000/3950 | OK |
| Meteror Rain Project | Huffy Think | Moorline Line Ship Class | 2340.0 | match | 1/1 | 3/6 | 800/3950 | OK |
| Hellbomb | Bus Vocal | Container Hauler Refit | 2602.0 | match [CVLN (OSP) / CLN (OSP)] | 1/1 | 4/6 | 1604/3950 | OK |
| CV 6k duo | Evergreen Ceres | Container Hauler Refit | 2965.0 | match [CVLN (OSP) / CLN (OSP)] | 1/1 | 4/6 | 606/3950 | OK |
| CV 6k duo | Mini Nightmare | Container Hauler Refit | 2965.0 | match [CVLN (OSP) / CLN (OSP)] | 1/1 | 4/6 | 606/3950 | OK |
| Cope Squadran 6k | Evergreen Ceres | Container Hauler Refit | 2965.0 | match [CVLN (OSP) / CLN (OSP)] | 1/1 | 4/6 | 1606/2000 | OK |
| Cope Squadran 6k | Mini Nightmare | Container Hauler Refit | 2965.0 | match [CVLN (OSP) / CLN (OSP)] | 1/1 | 4/6 | 1606/2000 | OK |
| Cope Squadran | Evergreen Ceres | Container Hauler Refit | 2965.0 | match [CVLN (OSP) / CLN (OSP)] | 1/1 | 4/6 | 1606/2000 | OK |
| Cope Squadran | Mini Nightmare | Container Hauler Refit | 2965.0 | match [CVLN (OSP) / CLN (OSP)] | 1/1 | 4/6 | 1606/2000 | OK |
| shi shi | Queen | Container Hauler Refit | 2970.0 | match [CVLN (OSP) / CLN (OSP)] | 1/1 | 4/6 | 1806/3950 | OK |
| Amethyst Squadron | All Reaching All Taking | Container Hauler Refit | 3000.0 | match [CVLN (OSP) / CLN (OSP)] | 1/1 | 5/6 | 1574/3950 | OK |
| CV 6k | Evergreen Ceres | Container Hauler Refit | 3000.0 | match [CVLN (OSP) / CLN (OSP)] | 1/1 | 4/6 | 606/3950 | OK |
| 等 | 共 17 艘 | | | | | | |

## CVLN (OSP)（2500-3000，共 32 艘）

| 舰队 | 舰名 | 舰体 | 点数 | 判定 | 本类 must | 通用 must | 耗电/供电 (kW) | (n-1) 判定 |
|---|---|---|---:|---|---|---|---|---|
| All 27 sample ships · Protectorate | Ever Lovely | Container Hauler Refit | 1537.0 | match 偏低 | 1/1 | 4/6 | 1854/3950 | OK |
| All 27 sample ships · Protectorate | All Reaching All Taking | Container Hauler Refit | 1603.0 | match 偏低 | 1/1 | 5/6 | 1574/3950 | OK |
| Hellbomb | Bus Vocal | Container Hauler Refit | 2602.0 | match [CVLN (OSP) / CLN (OSP)] | 1/1 | 4/6 | 1604/3950 | OK |
| CV 6k duo | Evergreen Ceres | Container Hauler Refit | 2965.0 | match [CVLN (OSP) / CLN (OSP)] | 1/1 | 4/6 | 606/3950 | OK |
| CV 6k duo | Mini Nightmare | Container Hauler Refit | 2965.0 | match [CVLN (OSP) / CLN (OSP)] | 1/1 | 4/6 | 606/3950 | OK |
| Cope Squadran 6k | Evergreen Ceres | Container Hauler Refit | 2965.0 | match [CVLN (OSP) / CLN (OSP)] | 1/1 | 4/6 | 1606/2000 | OK |
| Cope Squadran 6k | Mini Nightmare | Container Hauler Refit | 2965.0 | match [CVLN (OSP) / CLN (OSP)] | 1/1 | 4/6 | 1606/2000 | OK |
| Cope Squadran | Evergreen Ceres | Container Hauler Refit | 2965.0 | match [CVLN (OSP) / CLN (OSP)] | 1/1 | 4/6 | 1606/2000 | OK |
| Cope Squadran | Mini Nightmare | Container Hauler Refit | 2965.0 | match [CVLN (OSP) / CLN (OSP)] | 1/1 | 4/6 | 1606/2000 | OK |
| shi shi | Queen | Container Hauler Refit | 2970.0 | match [CVLN (OSP) / CLN (OSP)] | 1/1 | 4/6 | 1806/3950 | OK |
| Amethyst Squadron | All Reaching All Taking | Container Hauler Refit | 3000.0 | match [CVLN (OSP) / CLN (OSP)] | 1/1 | 5/6 | 1574/3950 | OK |
| CV 6k | Evergreen Ceres | Container Hauler Refit | 3000.0 | match [CVLN (OSP) / CLN (OSP)] | 1/1 | 4/6 | 606/3950 | OK |
| CV 6k | Mini Nightmare | Container Hauler Refit | 3000.0 | match [CVLN (OSP) / CLN (OSP)] | 1/1 | 4/6 | 606/3950 | OK |
| 3_OSP_Carrier_ASW++ | All Reaching All Taking | Container Hauler Refit | 3000.0 | match [CVLN (OSP) / CLN (OSP)] | 1/1 | 5/6 | 2906/3950 | OK |
| 等 | 共 18 艘 | | | | | | |

## CV (ANS)（3000-12000，共 1 艘）

| 舰队 | 舰名 | 舰体 | 点数 | 判定 | 本类 must | 通用 must | 耗电/供电 (kW) | (n-1) 判定 |
|---|---|---|---:|---|---|---|---|---|
| CV 12k | Math and Ruse | Worden Fleet Carrier Class | 10352.0 | bad_class | 0/0 | 5/6 | 6987/8600 | OK |

## unarmed (any hull)（0-12000，共 183 艘）

| 舰队 | 舰名 | 舰体 | 点数 | 判定 | 本类 must | 通用 must | 耗电/供电 (kW) | (n-1) 判定 |
|---|---|---|---:|---|---|---|---|---|
| surrender | Jewel and Pale | Ferryman Clipper Class | 50.0 | match | 1/1 | 0/5 | 0/0 | 无反应堆 |
| 大冲击 | CM-4D1 | Ferryman Clipper Class | 70.0 | match | 1/1 | 3/6 | 0/300 | OK |
| 大冲击 | CM-4D1 | Ferryman Clipper Class | 70.0 | match | 1/1 | 3/6 | 0/300 | OK |
| 大冲击 | CM-4D1 | Ferryman Clipper Class | 70.0 | match | 1/1 | 3/6 | 0/300 | OK |
| 大冲击 | CM-4D1 | Ferryman Clipper Class | 70.0 | match | 1/1 | 3/6 | 0/300 | OK |
| 大冲击 | CM-4D1 | Ferryman Clipper Class | 70.0 | match | 1/1 | 3/6 | 0/300 | OK |
| Cope Squadran | Command Shuttle | Ferryman Clipper Class | 70.0 | match | 1/1 | 3/6 | 0/300 | OK |
| Meteror Rain Project | Cleft Gleam | Ferryman Clipper Class | 70.0 | match | 1/1 | 3/6 | 0/300 | OK |
| Meteror Rain Project | Gross Famed | Ferryman Clipper Class | 70.0 | match | 1/1 | 3/6 | 0/300 | OK |
| Meteror Rain Project | Awe of Anthea | Ferryman Clipper Class | 70.0 | match | 1/1 | 3/6 | 0/300 | OK |
| Meteror Rain Project | Shut Coney | Ferryman Clipper Class | 70.0 | match | 1/1 | 3/6 | 0/300 | OK |
| Meteror Rain Project | Mixed Award | Ferryman Clipper Class | 70.0 | match | 1/1 | 3/6 | 0/300 | OK |
| Meteror Rain Project | Drew | Ferryman Clipper Class | 70.0 | match | 1/1 | 3/6 | 0/300 | OK |
| Meteror Rain Project | Tired Boa | Ferryman Clipper Class | 70.0 | match | 1/1 | 3/6 | 0/300 | OK |
| 等 | 共 169 艘 | | | | | | |

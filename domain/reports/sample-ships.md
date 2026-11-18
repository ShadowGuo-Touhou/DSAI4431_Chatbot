# 样板船清单（每艘一个 `.fleet`）

共 **61** 艘，文件在 `sample fleets/`（与 `domain/kb/builds/<舰级>-sample-N.md` 一一对应：同一艘船的表格页和 `.fleet` 是同一份数据）。

用法：把 `.fleet` 拖进 `E:\SteamLibrary\steamapps\common\Nebulous\Saves\Fleets`，游戏里「舰队 → 载入」即可；也可以用 `repo\.venv\Scripts\python.exe domain\tools\validate_fleet.py "<文件>"` 先校验。

> `.fleet` 直接搬运原存档的 `<Ship>` 节点，弹药装载（`<ComponentData>`）、武器组、导弹模板都原样保留；只有舰队名、点数、描述被改成这艘船自己的。

| 舰级 | 船名 | 舰体 | 点数 | 来源舰队 | 文件 |
|---|---|---|---:|---|---|
| gun FF | Peel of Agnesse | Raines Frigate Class | 397 | HC Gun Missile test 8 | `gun FF - Peel of Agnesse.fleet` |
| gun FF | Brew | Raines Frigate Class | 371 | masqford | `gun FF - Brew.fleet` |
| support ffl (sprinter or shuttle) | Hourglass | Ferryman Clipper Class | 232 | CC LN test 4 450 | `support ffl (sprinter or shuttle) - Hourglass.fleet` |
| Beam DD | Beyond Conventional | Keystone Destroyer Class | 675 | TF Willow | `Beam DD - Beyond Conventional.fleet` |
| Beam DD | Word Cadence | Keystone Destroyer Class | 675 | TF Willow | `Beam DD - Word Cadence.fleet` |
| 250 gun CL | Impede | Vauxhall Light Cruiser Class | 1002 | 1101 CL | `250 gun CL - Impede.fleet` |
| 250 gun CL | Suffering | Vauxhall Light Cruiser Class | 1002 | 1101 CL | `250 gun CL - Suffering.fleet` |
| missile CH | LOADER 4 | Axford Heavy Cruiser Class | 3000 | HC Missile test 7 | `missile CH - LOADER 4.fleet` |
| missile CH | LOADER 4 | Axford Heavy Cruiser Class | 2825 | Shock CH test | `missile CH - LOADER 4（Shock CH test）.fleet` |
| half cve/cvl | For Whutever | Levy Escort Carrier Class | 1500 | CVE | `half cve-cvl - For Whutever.fleet` |
| half cve/cvl | Whutever loves this | Levy Escort Carrier Class | 1500 | CVE | `half cve-cvl - Whutever loves this.fleet` |
| support FF | Beige of Cleland | Raines Frigate Class | 461 | hc gun dd test 11 | `support FF - Beige of Cleland.fleet` |
| support FF | Sale | Raines Frigate Class | 485 | hc gun dd test 11 | `support FF - Sale.fleet` |
| 450 CH | Value Judgement | Axford Heavy Cruiser Class | 1500 | TF Oak | `450 CH - Value Judgement.fleet` |
| 450 CH | Moral Failing | Axford Heavy Cruiser Class | 1500 | TF Oak | `450 CH - Moral Failing.fleet` |
| Command Cruiser killer (CCK) CH | Sakana | Axford Heavy Cruiser Class | 1733 | Meh 6k | `Command Cruiser killer (CCK) CH - Sakana.fleet` |
| Rail DD | BFR | Keystone Destroyer Class | 466 | hc gun dd test 11 | `Rail DD - BFR.fleet` |
| Rail DD | BFG | Keystone Destroyer Class | 453 | hc gun dd test 11 | `Rail DD - BFG.fleet` |
| A Cap ffl (sprinter or shuttle) | Hustler | Ferryman Clipper Class | 183 | Tantalum Squadron | `A Cap ffl (sprinter or shuttle) - Hustler.fleet` |
| A Cap ffl (sprinter or shuttle) | The Toned Wound | Sprinter Corvette Class | 123 | All Craft Are Bastards | `A Cap ffl (sprinter or shuttle) - The Toned Wound.fleet` |
| missile sprinter | T. Final Light | Sprinter Corvette Class | 352 | Mixed FFLs | `missile sprinter - T. Final Light.fleet` |
| missile sprinter | T. Tepid Siren | Sprinter Corvette Class | 352 | Mixed FFLs | `missile sprinter - T. Tepid Siren.fleet` |
| gun/cap ffl  (sprinter or shuttle) | Zippy Taxis | Sprinter Corvette Class | 220 | BB test 55 Newbie | `gun-cap ffl (sprinter or shuttle) - Zippy Taxis.fleet` |
| gun/cap ffl  (sprinter or shuttle) | In Your Walls | Ferryman Clipper Class | 165 | Wulfenite Squadron | `gun-cap ffl (sprinter or shuttle) - In Your Walls.fleet` |
| CLN (OSP) | Ever Lovely | Moorline Line Ship Class | 3000 | CVLN test 5 Newbie | `CLN (OSP) - Ever Lovely.fleet` |
| CLN (OSP) | All Reaching All Taking | Moorline Line Ship Class | 3000 | Amethyst Squadron | `CLN (OSP) - All Reaching All Taking.fleet` |
| missile CC | Nuclear Summer | Ocello Command Cruiser Class | 3000 | S2 DIR OCELLO | `missile CC - Nuclear Summer.fleet` |
| EWR/LRT tug | Eager Mover | Draugr Clipper Class | 258 | TF Purple Joy 2 | `EWR-LRT tug - Eager Mover.fleet` |
| EWR/LRT tug | Mired Act | Draugr Clipper Class | 258 | CC LN test 1 | `EWR-LRT tug - Mired Act.fleet` |
| rocket shuttle (ruttle) | Applied Pressure | Ferryman Clipper Class | 286 | Azurite Squadron | `rocket shuttle (ruttle) - Applied Pressure.fleet` |
| rocket shuttle (ruttle) | Repulsive Force | Ferryman Clipper Class | 286 | Azurite Squadron | `rocket shuttle (ruttle) - Repulsive Force.fleet` |
| 450 CC | Delta of Maddy | Ocello Command Cruiser Class | 1457 | CC maxxing | `450 CC - Delta of Maddy.fleet` |
| 450 CC | Above Chunk | Ocello Command Cruiser Class | 1457 | CC maxxing | `450 CC - Above Chunk.fleet` |
| gun MN | Excuse The Interruption | Flathead Monitor Class | 594 | Garnet Squadron | `gun MN - Excuse The Interruption.fleet` |
| gun MN | Open For Business | Flathead Monitor Class | 594 | Garnet Squadron | `gun MN - Open For Business.fleet` |
| S2 MN | Time Dilation | Flathead Monitor Class | 969 | Tantalum Squadron | `S2 MN - Time Dilation.fleet` |
| multi mission tug (mmt) | Ranger | Draugr Clipper Class | 452 | Tantalum Squadron | `multi mission tug (mmt) - Ranger.fleet` |
| multi mission tug (mmt) | Bailiff | Draugr Clipper Class | 452 | Tantalum Squadron | `multi mission tug (mmt) - Bailiff.fleet` |
| gun tug | TBD | Draugr Clipper Class | 373 | tug blob | `gun tug - TBD.fleet` |
| support tug | 不冲击 | Draugr Clipper Class | 395 | 大冲击 | `support tug - 不冲击.fleet` |
| S2CC | Command Cruiser Must Command | Ocello Command Cruiser Class | 3000 | S2 DIR OCELLO | `S2CC - Command Cruiser Must Command.fleet` |
| 450 ln | Umber Ox | Marauder Line Ship Class | 1142 | CC LN test 1 | `450 ln - Umber Ox.fleet` |
| 450 ln | Where All Things Bloom Between Mountains | Marauder Line Ship Class | 1142 | CC LN test 1 | `450 ln - Where All Things Bloom Between Mountains.fleet` |
| mass driver (md) ln | Wired Daily | Marauder Line Ship Class | 1052 | CC ln test 6 | `mass driver (md) ln - Wired Daily.fleet` |
| mass driver (md) ln | Wired Daily | Marauder Line Ship Class | 1049 | CC ln test 6 | `mass driver (md) ln - Wired Daily（CC ln test 6）.fleet` |
| 450 BB | Billion Lightyear | Solomon Battleship Class | 2766 | BB test 52 no ic | `450 BB - Billion Lightyear.fleet` |
| 450 BB | Billion Lightyear | Solomon Battleship Class | 2527 | BB test 55 Newbie | `450 BB - Billion Lightyear（BB test 55 Newbie）.fleet` |
| full cve (ANS) | Democratic Space Station | Levy Escort Carrier Class | 3000 | CVE test 33 SS2 | `full cve (ANS) - Democratic Space Station.fleet` |
| full cve (ANS) | Democratic Space Station | Levy Escort Carrier Class | 3000 | CVE test 34 S2 | `full cve (ANS) - Democratic Space Station（CVE test 34 S2）.fleet` |
| scout ffl (sprinter or shuttle) | Hourglass | Sprinter Corvette Class | 222 | BB test 55 Newbie | `scout ffl (sprinter or shuttle) - Hourglass.fleet` |
| missle ln | Life Goes On | Marauder Line Ship Class | 3000 | Life Goes On LNG | `missle ln - Life Goes On.fleet` |
| missle ln | Blot Out The Sun With Our Arrows | Marauder Line Ship Class | 3000 | cmd test2 | `missle ln - Blot Out The Sun With Our Arrows.fleet` |
| Rail CC | Hoshimachi | Ocello Command Cruiser Class | 1529 | Comet Squadron | `Rail CC - Hoshimachi.fleet` |
| S2CH | Diesal Summer | Axford Heavy Cruiser Class | 3000 | S2CH | `S2CH - Diesal Summer.fleet` |
| greed CH | ｜｜｜｜｜｜｜｜ | Axford Heavy Cruiser Class | 1502 | concept | `greed CH - --------.fleet` |
| greed CH | Equility-On-Sea | Axford Heavy Cruiser Class | 1560 | greedford | `greed CH - Equility-On-Sea.fleet` |
| missle FF | Read | Raines Frigate Class | 1000 | zpzd 导弹FF | `missle FF - Read.fleet` |
| missle FF | Toady | Raines Frigate Class | 1000 | zpzd 导弹FF | `missle FF - Toady.fleet` |
| Beam BB | Strong the roots Dick | Solomon Battleship Class | 2338 | beme | `Beam BB - Strong the roots Dick.fleet` |
| Beam BB | Strong the roots Whilly | Solomon Battleship Class | 2338 | beme | `Beam BB - Strong the roots Whilly.fleet` |
| TCSG BB | Glans and Burns | Solomon Battleship Class | 2690 | test | `TCSG BB - Glans and Burns.fleet` |

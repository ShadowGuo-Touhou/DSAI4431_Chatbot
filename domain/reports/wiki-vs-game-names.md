# Wiki (0.6.2.6) vs installed game strings

Source A: the saved official wiki pages (game 0.6.2.6:260903-1430).
Source B: `Nebulous_Data/StreamingAssets/Localization/en-US/en_assets.json`,
i.e. the string table of the installed build itself.

## Counts

| Group | wiki entries | game strings | matched | spelling | wiki-only | game-only |
|---|---|---|---|---|---|---|
| Parts (mounts / compartments / modules / built-in hull parts) | 201 | 258 | 140 | 1 | 60 | 115 |
| Munitions (shells, missiles, seekers, mines, bombs) | 71 | 94 | 55 | 2 | 14 | 37 |

The player's own `.fleet` files are **not** used: most are older-version or modded.

## Parts (mounts / compartments / modules / built-in hull parts)

### Spelling conflicts (1)
- **E55 'Floodlight' Illuminator** → game: `E57 'Floodlight' Illuminator` — game key `HULLCOMPNAME_E57_FLOODLIGHT_ILLUMINATOR` — wiki page `Components`

### In the wiki, absent from the installed game's strings (60)
- **E15 'Masquerade' Signature Booster** → game: `` — wiki page `Components`
- **CR10** → game: `` — wiki page `Components`
- **CR75** → game: `` — wiki page `Components`
- **Radar Panel** → game: `` — wiki page `Components`
- **Radar Array** → game: `` — wiki page `Components`
- **Sprinter Main** → game: `` — wiki page `Components`
- **Sprinter Angular** → game: `` — wiki page `Components`
- **Sprinter Braking** → game: `` — wiki page `Components`
- **Raines Main** → game: `` — wiki page `Components`
- **Raines Angular** → game: `` — wiki page `Components`
- **Raines Braking** → game: `` — wiki page `Components`
- **Keystone Main** → game: `` — wiki page `Components`
- **Keystone Angular** → game: `` — wiki page `Components`
- **Keystone Braking** → game: `` — wiki page `Components`
- **Vauxhall Main** → game: `` — wiki page `Components`
- **Vauxhall Angular** → game: `` — wiki page `Components`
- **Vauxhall Braking** → game: `` — wiki page `Components`
- **Axford Main** → game: `` — wiki page `Components`
- **Axford Angular** → game: `` — wiki page `Components`
- **Axford Braking** → game: `` — wiki page `Components`
- **Levy Main** → game: `` — wiki page `Components`
- **Levy Angular** → game: `` — wiki page `Components`
- **Levy Braking** → game: `` — wiki page `Components`
- **Solomon Main** → game: `` — wiki page `Components`
- **Solomon Angular** → game: `` — wiki page `Components`
- **Solomon Braking** → game: `` — wiki page `Components`
- **Worden Main** → game: `` — wiki page `Components`
- **Worden Angular** → game: `` — wiki page `Components`
- **Worden Braking** → game: `` — wiki page `Components`
- **Mercator Main** → game: `` — wiki page `Components`
- **Mercator Angular** → game: `` — wiki page `Components`
- **Mercator Braking** → game: `` — wiki page `Components`
- **Ferryman Main** → game: `` — wiki page `Components`
- **Ferryman Angular** → game: `` — wiki page `Components`
- **Ferryman Braking** → game: `` — wiki page `Components`
- **Draugr Main** → game: `` — wiki page `Components`
- **Draugr Angular** → game: `` — wiki page `Components`
- **Draugr Braking** → game: `` — wiki page `Components`
- **Flathead Main** → game: `` — wiki page `Components`
- **Flathead Angular** → game: `` — wiki page `Components`
- **Flathead Braking** → game: `` — wiki page `Components`
- **Journeyman Main** → game: `` — wiki page `Components`
- **Journeyman Angular** → game: `` — wiki page `Components`
- **Journeyman Braking** → game: `` — wiki page `Components`
- **Ocello Main** → game: `` — wiki page `Components`
- **Ocello Angular** → game: `` — wiki page `Components`
- **Ocello Braking** → game: `` — wiki page `Components`
- **Marauder Main** → game: `` — wiki page `Components`
- **Marauder Angular** → game: `` — wiki page `Components`
- **Marauder Braking** → game: `` — wiki page `Components`
- **Moorline Main** → game: `` — wiki page `Components`
- **Moorline Angular** → game: `` — wiki page `Components`
- **Moorline Braking** → game: `` — wiki page `Components`
- **Levy Large Pad** → game: `` — wiki page `Components`
- **Levy Small Pad** → game: `` — wiki page `Components`
- **Worden Large Pad** → game: `` — wiki page `Components`
- **Worden Small Pad** → game: `` — wiki page `Components`
- **Journeyman Large Pad** → game: `` — wiki page `Components`
- **Journeyman Small Pad** → game: `` — wiki page `Components`
- **Resupply** → game: `` — wiki page `Components`

### In the installed game, absent from the wiki (115)
- **E15 'Masquerade' Deception Module** → game: `E15 'Masquerade' Deception Module` — game key `HULLCOMPNAME_E15_MASQUERADE_DECEPTION_MODULE`
- **BL Radar Panel** → game: `BL Radar Panel` — game key `HULLPARTNAME_BL_RADAR_PANEL`
- **BR Radar Panel** → game: `BR Radar Panel` — game key `HULLPARTNAME_BR_RADAR_PANEL`
- **TL Radar Panel** → game: `TL Radar Panel` — game key `HULLPARTNAME_TL_RADAR_PANEL`
- **TR Radar Panel** → game: `TR Radar Panel` — game key `HULLPARTNAME_TR_RADAR_PANEL`
- **BBL Radar Panel** → game: `BBL Radar Panel` — game key `HULLPARTNAME_BBL_RADAR_PANEL`
- **BBR Radar Panel** → game: `BBR Radar Panel` — game key `HULLPARTNAME_BBR_RADAR_PANEL`
- **BTL Radar Panel** → game: `BTL Radar Panel` — game key `HULLPARTNAME_BTL_RADAR_PANEL`
- **BTR Radar Panel** → game: `BTR Radar Panel` — game key `HULLPARTNAME_BTR_RADAR_PANEL`
- **FBL Radar Panel** → game: `FBL Radar Panel` — game key `HULLPARTNAME_FBL_RADAR_PANEL`
- **FBR Radar Panel** → game: `FBR Radar Panel` — game key `HULLPARTNAME_FBR_RADAR_PANEL`
- **FTL Radar Panel** → game: `FTL Radar Panel` — game key `HULLPARTNAME_FTL_RADAR_PANEL`
- **FTR Radar Panel** → game: `FTR Radar Panel` — game key `HULLPARTNAME_FTR_RADAR_PANEL`
- **Radar (Bottom)** → game: `Radar (Bottom)` — game key `HULLPARTNAME_RADAR_BOTTOM_`
- **Radar (Top)** → game: `Radar (Top)` — game key `HULLPARTNAME_RADAR_TOP_`
- **Top Radar** → game: `Top Radar` — game key `HULLPARTNAME_TOP_RADAR`
- **Bottom Radar** → game: `Bottom Radar` — game key `HULLPARTNAME_BOTTOM_RADAR`
- **CR10 Ant** → game: `CR10 Ant` — game key `HULLPARTNAME_CR10_ANT`
- **CR75 Ant** → game: `CR75 Ant` — game key `HULLPARTNAME_CR75_ANT`
- **Main 01** → game: `Main 01` — game key `HULLPARTNAME_MAIN_01`
- **Main 02** → game: `Main 02` — game key `HULLPARTNAME_MAIN_02`
- **Main 03** → game: `Main 03` — game key `HULLPARTNAME_MAIN_03`
- **Main 04** → game: `Main 04` — game key `HULLPARTNAME_MAIN_04`
- **Main 05** → game: `Main 05` — game key `HULLPARTNAME_MAIN_05`
- **Main 06** → game: `Main 06` — game key `HULLPARTNAME_MAIN_06`
- **Main 07** → game: `Main 07` — game key `HULLPARTNAME_MAIN_07`
- **Main 08** → game: `Main 08` — game key `HULLPARTNAME_MAIN_08`
- **Main 09** → game: `Main 09` — game key `HULLPARTNAME_MAIN_09`
- **Main 10** → game: `Main 10` — game key `HULLPARTNAME_MAIN_10`
- **Large Pad 01** → game: `Large Pad 01` — game key `HULLPARTNAME_LARGE_PAD_01`
- **Large Pad 02** → game: `Large Pad 02` — game key `HULLPARTNAME_LARGE_PAD_02`
- **Large Pad 03** → game: `Large Pad 03` — game key `HULLPARTNAME_LARGE_PAD_03`
- **Large Pad 04** → game: `Large Pad 04` — game key `HULLPARTNAME_LARGE_PAD_04`
- **Large Pad 05** → game: `Large Pad 05` — game key `HULLPARTNAME_LARGE_PAD_05`
- **Large Pad 06** → game: `Large Pad 06` — game key `HULLPARTNAME_LARGE_PAD_06`
- **Large Pad 07** → game: `Large Pad 07` — game key `HULLPARTNAME_LARGE_PAD_07`
- **Large Pad 08** → game: `Large Pad 08` — game key `HULLPARTNAME_LARGE_PAD_08`
- **Large Pad 09** → game: `Large Pad 09` — game key `HULLPARTNAME_LARGE_PAD_09`
- **Large Pad 10** → game: `Large Pad 10` — game key `HULLPARTNAME_LARGE_PAD_10`
- **Small Pad 01** → game: `Small Pad 01` — game key `HULLPARTNAME_SMALL_PAD_01`
- **Small Pad 02** → game: `Small Pad 02` — game key `HULLPARTNAME_SMALL_PAD_02`
- **Small Pad 03** → game: `Small Pad 03` — game key `HULLPARTNAME_SMALL_PAD_03`
- **Small Pad 04** → game: `Small Pad 04` — game key `HULLPARTNAME_SMALL_PAD_04`
- **Small Pad 05** → game: `Small Pad 05` — game key `HULLPARTNAME_SMALL_PAD_05`
- **Small Pad 06** → game: `Small Pad 06` — game key `HULLPARTNAME_SMALL_PAD_06`
- **Small Pad 07** → game: `Small Pad 07` — game key `HULLPARTNAME_SMALL_PAD_07`
- **Small Pad 08** → game: `Small Pad 08` — game key `HULLPARTNAME_SMALL_PAD_08`
- **Small Pad 09** → game: `Small Pad 09` — game key `HULLPARTNAME_SMALL_PAD_09`
- **Small Pad 10** → game: `Small Pad 10` — game key `HULLPARTNAME_SMALL_PAD_10`
- **Small Pad 11** → game: `Small Pad 11` — game key `HULLPARTNAME_SMALL_PAD_11`
- **Small Pad 12** → game: `Small Pad 12` — game key `HULLPARTNAME_SMALL_PAD_12`
- **Small Pad 13** → game: `Small Pad 13` — game key `HULLPARTNAME_SMALL_PAD_13`
- **Small Pad 14** → game: `Small Pad 14` — game key `HULLPARTNAME_SMALL_PAD_14`
- **Small Pad 15** → game: `Small Pad 15` — game key `HULLPARTNAME_SMALL_PAD_15`
- **Thruster 01** → game: `Thruster 01` — game key `HULLPARTNAME_THRUSTER_01`
- **Thruster 02** → game: `Thruster 02` — game key `HULLPARTNAME_THRUSTER_02`
- **Thruster 03** → game: `Thruster 03` — game key `HULLPARTNAME_THRUSTER_03`
- **Thruster 04** → game: `Thruster 04` — game key `HULLPARTNAME_THRUSTER_04`
- **Thruster 05** → game: `Thruster 05` — game key `HULLPARTNAME_THRUSTER_05`
- **Thruster 06** → game: `Thruster 06` — game key `HULLPARTNAME_THRUSTER_06`
- **Thruster 07** → game: `Thruster 07` — game key `HULLPARTNAME_THRUSTER_07`
- **Thruster 08** → game: `Thruster 08` — game key `HULLPARTNAME_THRUSTER_08`
- **Thruster 09** → game: `Thruster 09` — game key `HULLPARTNAME_THRUSTER_09`
- **Thruster 10** → game: `Thruster 10` — game key `HULLPARTNAME_THRUSTER_10`
- **Thruster 11** → game: `Thruster 11` — game key `HULLPARTNAME_THRUSTER_11`
- **Thruster 12** → game: `Thruster 12` — game key `HULLPARTNAME_THRUSTER_12`
- **Thruster 13** → game: `Thruster 13` — game key `HULLPARTNAME_THRUSTER_13`
- **Thruster 14** → game: `Thruster 14` — game key `HULLPARTNAME_THRUSTER_14`
- **Thruster 15** → game: `Thruster 15` — game key `HULLPARTNAME_THRUSTER_15`
- **Thruster 16** → game: `Thruster 16` — game key `HULLPARTNAME_THRUSTER_16`
- **Thruster 17** → game: `Thruster 17` — game key `HULLPARTNAME_THRUSTER_17`
- **Thruster 18** → game: `Thruster 18` — game key `HULLPARTNAME_THRUSTER_18`
- **Thruster 19** → game: `Thruster 19` — game key `HULLPARTNAME_THRUSTER_19`
- **Thruster 20** → game: `Thruster 20` — game key `HULLPARTNAME_THRUSTER_20`
- **CR75 Antenna** → game: `CR75 Antenna` — game key `HULLCOMPNAME_CR75_ANT`
- **Thruster S01** → game: `Thruster S01` — game key `HULLPARTNAME_THRUSTER_S1`
- **Thruster S02** → game: `Thruster S02` — game key `HULLPARTNAME_THRUSTER_S2`
- **Thruster S03** → game: `Thruster S03` — game key `HULLPARTNAME_THRUSTER_S3`
- **Thruster S04** → game: `Thruster S04` — game key `HULLPARTNAME_THRUSTER_S4`
- **Thruster S05** → game: `Thruster S05` — game key `HULLPARTNAME_THRUSTER_S5`
- **Thruster S06** → game: `Thruster S06` — game key `HULLPARTNAME_THRUSTER_S6`
- **Thruster S07** → game: `Thruster S07` — game key `HULLPARTNAME_THRUSTER_S7`
- **Thruster S08** → game: `Thruster S08` — game key `HULLPARTNAME_THRUSTER_S8`
- **Thruster S09** → game: `Thruster S09` — game key `HULLPARTNAME_THRUSTER_S9`
- **Thruster S10** → game: `Thruster S10` — game key `HULLPARTNAME_THRUSTER_S10`
- **Thruster B01** → game: `Thruster B01` — game key `HULLPARTNAME_THRUSTER_B1`
- **Thruster B02** → game: `Thruster B02` — game key `HULLPARTNAME_THRUSTER_B2`
- **Thruster B03** → game: `Thruster B03` — game key `HULLPARTNAME_THRUSTER_B3`
- **Thruster B04** → game: `Thruster B04` — game key `HULLPARTNAME_THRUSTER_B4`
- **Thruster B05** → game: `Thruster B05` — game key `HULLPARTNAME_THRUSTER_B5`
- **Thruster B06** → game: `Thruster B06` — game key `HULLPARTNAME_THRUSTER_B6`
- **Thruster B07** → game: `Thruster B07` — game key `HULLPARTNAME_THRUSTER_B7`
- **Thruster B08** → game: `Thruster B08` — game key `HULLPARTNAME_THRUSTER_B8`
- **Thruster B09** → game: `Thruster B09` — game key `HULLPARTNAME_THRUSTER_B9`
- **Thruster B10** → game: `Thruster B10` — game key `HULLPARTNAME_THRUSTER_B10`
- **Braking S01** → game: `Braking S01` — game key `HULLPARTNAME_BRAKING_S1`
- **Braking S02** → game: `Braking S02` — game key `HULLPARTNAME_BRAKING_S2`
- **Braking S03** → game: `Braking S03` — game key `HULLPARTNAME_BRAKING_S3`
- **Braking S04** → game: `Braking S04` — game key `HULLPARTNAME_BRAKING_S4`
- **Braking S05** → game: `Braking S05` — game key `HULLPARTNAME_BRAKING_S5`
- **Braking S06** → game: `Braking S06` — game key `HULLPARTNAME_BRAKING_S6`
- **Braking S07** → game: `Braking S07` — game key `HULLPARTNAME_BRAKING_S7`
- **Braking S08** → game: `Braking S08` — game key `HULLPARTNAME_BRAKING_S8`
- **Braking S09** → game: `Braking S09` — game key `HULLPARTNAME_BRAKING_S9`
- **Braking S10** → game: `Braking S10` — game key `HULLPARTNAME_BRAKING_S10`
- **Braking B01** → game: `Braking B01` — game key `HULLPARTNAME_BRAKING_B1`
- **Braking B02** → game: `Braking B02` — game key `HULLPARTNAME_BRAKING_B2`
- **Braking B03** → game: `Braking B03` — game key `HULLPARTNAME_BRAKING_B3`
- **Braking B04** → game: `Braking B04` — game key `HULLPARTNAME_BRAKING_B4`
- **Braking B05** → game: `Braking B05` — game key `HULLPARTNAME_BRAKING_B5`
- **Braking B06** → game: `Braking B06` — game key `HULLPARTNAME_BRAKING_B6`
- **Braking B07** → game: `Braking B07` — game key `HULLPARTNAME_BRAKING_B7`
- **Braking B08** → game: `Braking B08` — game key `HULLPARTNAME_BRAKING_B8`
- **Braking B09** → game: `Braking B09` — game key `HULLPARTNAME_BRAKING_B9`
- **Braking B10** → game: `Braking B10` — game key `HULLPARTNAME_BRAKING_B10`


## Munitions (shells, missiles, seekers, mines, bombs)

### Spelling conflicts (2)
- **250mm Bombshell** → game: `250mm Bomb Shell` — game key `AMMONAME_250MM_BOMB_SHELL` — wiki page `Munitions & Missiles`
- **CM-4D1 Decoy Container (Line Ship)** → game: `CM-4D2 Decoy Container (Line Ship)` — game key `AMMONAME_CM_4D2_DECOY_CONTAINER_LINE_SHIP_` — wiki page `Munitions & Missiles`

### In the wiki, absent from the installed game's strings (14)
- **SGM-100 Balestra Missile** → game: `` — wiki page `Munitions & Missiles`
- **SDM-100 Lunge Missile** → game: `` — wiki page `Munitions & Missiles`
- **SSM-100 Remise Missile** → game: `` — wiki page `Munitions & Missiles`
- **SGM-200 Tempest Missile** → game: `` — wiki page `Munitions & Missiles`
- **SDM-200 Typhoon Missile** → game: `` — wiki page `Munitions & Missiles`
- **SGM-300 Flail Hybrid Missile** → game: `` — wiki page `Munitions & Missiles`
- **SGT-300 Pilum Torpedo** → game: `` — wiki page `Munitions & Missiles`
- **SGM-H-200 Cyclone Hybrid Missile** → game: `` — wiki page `Munitions & Missiles`
- **SGM-H-300 Atlatl Hybrid Missile** → game: `` — wiki page `Munitions & Missiles`
- **CM-400 Container** → game: `` — wiki page `Munitions & Missiles`
- **CM-S-400 Container** → game: `` — wiki page `Munitions & Missiles`
- **Fixed Anti-Radiation Seeker (Home On Jam)** → game: `` — wiki page `Munitions & Missiles`
- **Fixed Anti-Radiation Seeker (Pulsed Radar)** → game: `` — wiki page `Munitions & Missiles`
- **Wake-Homing Seeker (THERM)** → game: `` — wiki page `Munitions & Missiles`

### In the installed game, absent from the wiki (37)
- **250mm Flak Shell** → game: `250mm Flak Shell` — game key `AMMONAME_250MM_FLAK_SHELL`
- **500mm Fragmentation Block** → game: `500mm Fragmentation Block` — game key `AMMONAME_500MM_FRAGMENTATION_BLOCK`
- **EA12 Chaff Decoy** → game: `EA12 Chaff Decoy` — game key `AMMONAME_EA12_CHAFF_DECOY`
- **EA14 Chaff Decoy** → game: `EA14 Chaff Decoy` — game key `AMMONAME_EA14_CHAFF_DECOY`
- **EA20 Flare Decoy** → game: `EA20 Flare Decoy` — game key `AMMONAME_EA20_FLARE_DECOY`
- **EA99 'Conure' Active Decoy** → game: `EA99 'Conure' Active Decoy` — game key `AMMONAME_EA99_CONURE_ACTIVE_DECOY`
- **Size 1 Missile** → game: `Size 1 Missile` — game key `MISSILE_CLASS_SIZE_1_MISSILE`
- **Size 2 Missile** → game: `Size 2 Missile` — game key `MISSILE_CLASS_SIZE_2_MISSILE`
- **Size 3 Missile** → game: `Size 3 Missile` — game key `MISSILE_CLASS_SIZE_3_MISSILE`
- **Size 3 Torpedo** → game: `Size 3 Torpedo` — game key `MISSILE_CLASS_SIZE_3_TORPEDO`
- **Size 1 Hybrid Missile** → game: `Size 1 Hybrid Missile` — game key `MISSILE_CLASS_SIZE_1_HYBRID_MISSILE`
- **Size 2 Hybrid Missile** → game: `Size 2 Hybrid Missile` — game key `MISSILE_CLASS_SIZE_2_HYBRID_MISSILE`
- **Size 3 Hybrid Missile** → game: `Size 3 Hybrid Missile` — game key `MISSILE_CLASS_SIZE_3_HYBRID_MISSILE`
- **Container Torpedo** → game: `Container Torpedo` — game key `MISSILE_CLASS_CONTAINER_TORPEDO`
- **flexible defensive missile with a booster** → game: `flexible defensive missile with a booster` — game key `MISSILE_FUNCDESC_LUNGE`
- **flexible defensive missile with a booster** → game: `flexible defensive missile with a booster` — game key `MISSILE_FUNCDESC_TYPHOON`
- **nimble general-purpose missile** → game: `nimble general-purpose missile` — game key `MISSILE_FUNCDEC_BALESTRA`
- **flexible mainstay anti-ship missile** → game: `flexible mainstay anti-ship missile` — game key `MISSILE_FUNCDESC_TEMPEST`
- **heavy anti-ship torpedo** → game: `heavy anti-ship torpedo` — game key `MISSILE_FUNCDESC_PILUM`
- **nimble space-superiority missile** → game: `nimble space-superiority missile` — game key `MISSILE_FUNCDESC_REMISE`
- **heavy anti-ship torpedo** → game: `heavy anti-ship torpedo` — game key `MISSILE_FUNCDESC_CONTAINER`
- **heavy support torpedo** → game: `heavy support torpedo` — game key `MISSILE_FUNCDESC_CONTAINERSUP`
- **Submunition Dispenser** → game: `Submunition Dispenser` — game key `MISSILECOMPNAME_SUBMUNITION_DISPENSER`
- **Wake-Thermal Seeker** → game: `Wake-Thermal Seeker` — game key `MISSILECOMPNAME_WAKE_THERMAL_SEEKER`
- **Kinetic Kill Mass** → game: `Kinetic Kill Mass` — game key `MISSILECOMPNAME_KINETIC_KILL_MASS`
- **SGM-1 Engine** → game: `SGM-1 Engine` — game key `MISSILECOMPNAME_SGM_1_ENGINE`
- **SDM-1 Booster Engine** → game: `SDM-1 Booster Engine` — game key `MISSILECOMPNAME_SDM_1_BOOSTER_ENGINE`
- **SDM-1 Main Engine** → game: `SDM-1 Main Engine` — game key `MISSILECOMPNAME_SDM_1_MAIN_ENGINE`
- **SGM-2 Engine** → game: `SGM-2 Engine` — game key `MISSILECOMPNAME_SGM_2_ENGINE`
- **SDM-2 Booster Engine** → game: `SDM-2 Booster Engine` — game key `MISSILECOMPNAME_SDM_2_BOOSTER_ENGINE`
- **SDM-2 Main Engine** → game: `SDM-2 Main Engine` — game key `MISSILECOMPNAME_SDM_2_MAIN_ENGINE`
- **SGM-H-2 Cruise Engine** → game: `SGM-H-2 Cruise Engine` — game key `MISSILECOMPNAME_SGM_H_2_CRUISE_ENGINE`
- **SGM-H-2 Sprint Engine** → game: `SGM-H-2 Sprint Engine` — game key `MISSILECOMPNAME_SGM_H_2_SPRINT_ENGINE`
- **SGM-H-3 Cruise Engine** → game: `SGM-H-3 Cruise Engine` — game key `MISSILECOMPNAME_SGM_H_3_CRUISE_ENGINE`
- **SGM-H-3 Sprint Engine** → game: `SGM-H-3 Sprint Engine` — game key `MISSILECOMPNAME_SGM_H_3_SPRINT_ENGINE`
- **SGT-3 Engine** → game: `SGT-3 Engine` — game key `MISSILECOMPNAME_SGT_3_ENGINE`
- **CM-4 Engine** → game: `CM-4 Engine` — game key `MISSILECOMPNAME_CM_4_ENGINE`



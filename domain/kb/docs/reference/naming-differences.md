# Wiki vs in-game naming differences

Source: Official wiki (wiki.hoodedhorse.com), game 0.6.2.6:260903-1430; game strings from `Nebulous_Data/StreamingAssets/Localization/en-US/en_assets.json` (same installed build).

## How this was checked

Every name on the official wiki was normalised (lower case, punctuation and apostrophes dropped) and matched against the game's own strings: `HULLCOMPNAME_*` for mounts, compartments and modules, `HULLPARTNAME_*` for built-in hull parts, `AMMONAME_*` for munitions and `MISSILECOMPNAME_*` for missile components. Numbers and roles always come from the wiki; the in-game name always comes from these strings.

## Renamed or renumbered (the game wins)

- The wiki row **E55 'Floodlight' Illuminator** is a wiki typo: in the game E55 is the **'Spotlight'** and E57 is the **'Floodlight' Illuminator**. The stats on that row belong to the Floodlight, so quote them as E57; use E55 only for the Spotlight.
- E15 'Masquerade' Signature Booster (wiki) = **E15 'Masquerade' Deception Module** in game. Same device, different function word.
- **CR10**: available to both factions, and most hulls also carry an integrated CR10 - that is why two entries exist. **CR70**: Shelter Alliance (ANS) only. **CR75**: only exists as an integrated part on some hulls, there is no CR75 module.

## Spellings that differ

- 250mm Bombshell (wiki) = **250mm Bomb Shell** in game.
- CM-4D1 Decoy Container (Line Ship) (wiki) = **CM-4D2 Decoy Container (Line Ship)** in game.
- Wake-Homing Seeker (THERM) (wiki) = **Wake-Thermal Seeker** in game.

- Missile engines and missile class names: SGM-1/SDM-1/SGM-2/SDM-2/SGM-H-2/SGM-H-3/SGT-3/CM-4 engines and boosters, plus Size 1/2/3 Missile, Size 3 Torpedo and Size 1/2/3 Hybrid Missile.
- Decoys and dispensed munitions: EA12 Chaff, EA14 Chaff, EA20 Flare, EA99 'Conure' Active Decoy, 250mm Flak Shell, 500mm Fragmentation Block, Submunition Dispenser, Kinetic Kill Mass.

## On the wiki but not in the game strings

- Named missile designs: SGM-100 Balestra, SDM-100 Lunge, SSM-100 Remise, SGM-200 Tempest, SDM-200 Typhoon, SGM-300 Flail, SGT-300 Pilum, SGM-H-200 Cyclone, SGM-H-300 Atlatl, CM-400 Container, CM-S-400 Container. The game builds missiles from bodies, payloads, avionics and seekers, so these are wiki examples rather than fixed loadouts.
- Seeker variants: Fixed Anti-Radiation Seeker (Home On Jam) and (Pulsed Radar). The game only names one `Fixed Anti-Radiation Seeker`; the two variants have no separate entry.
- Radar Array and Resupply are listed as built-in hull parts with no matching game string.

## Built-in hull parts: function names vs instance names

The wiki lists one row per function per hull (`Sprinter Main`, `Levy Large Pad`, `Radar Panel`), while the game names each physical instance (`Main 01`..`Main 10`, `Thruster 01`..`Thruster 20`, `Thruster S/B 01`..`10`, `Braking S/B 01`..`10`, `Small Pad 01`..`15`, `Large Pad 01`..`10`, and 12 radar-panel positions such as `TR Radar Panel`, `BL Radar Panel`). There is no name-level join between the two, and the wiki gives no position for any of them, so slot positions are still unknown.

## Rule for answers

The installed game is the default source. Use the game's names, the game's mechanics and the game's launcher/storage behaviour; quote wiki numbers only where they do not contradict the game, and always say which build the numbers come from (0.6.2.6:260903-1430). When a name does not exist in the game at all, say so instead of inventing numbers.

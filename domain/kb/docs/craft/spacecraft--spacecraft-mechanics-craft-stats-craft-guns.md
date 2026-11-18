# Spacecraft › Spacecraft Mechanics › Craft Stats › Craft guns

Source: Official wiki (wiki.hoodedhorse.com), game 0.6.2.6:260903-1430

## Body
| Gun | Mounted on | Fire mode | Rate of fire | Ammo | Closes to | Max range | Spread at 1 km |
|---|---|---|---|---|---|---|---|
| 35mm Gun (turret) | RS-35 Halberd nose and mission package | Continuous | 480 rpm | 300 | 1,575 m | 1,750 m | 1.7 m |
| 35mm Gun (fixed) | PF-440 Tanto, PF-386 Barracuda nose | 2 s bursts, 2 s pause | 360 rpm | 250 | 1,225 m | 1,750 m | 1.7 m |
| 20mm Gun | Tanto, Barracuda, RF-286 Pike nose | 1 s bursts, 2 s pause | 900 rpm | 300 | 1,225 m | 1,750 m | 5.2 m |
| 15mm Coilgun (7 pts) | Tanto nose | Single shots | 60 rpm | 6 | 1,500 m | 1,500 m (min. 400 m) | 0.9 m |
| 35mm Gun Pods | Tanto wings | 2 s bursts, 2 s pause | 360 rpm | 100 | 1,400 m | 1,750 m | 1.7 m |
| 35mm Gun Pods | Barracuda lower wings | 2 s bursts, 2 s pause | 360 rpm | 100 | 1,225 m | 1,750 m | 1.7 m |
| 100mm Gun Pods | B-45 Sturgeon inner wings | Single shots, alternating barrels | 120 rpm | 20 | 5,760 m | 7,200 m | 8.7 m |
| R-1 Rocket Pods | Barracuda wings | Single shots, alternating | 60 rpm | 6 | 2,380 m | 2,975 m | 17.5 m |
| R-1 Rocket Pods | Sturgeon inner wings | Single shots, alternating | 60 rpm | 20 | 2,380 m | 2,975 m | 1.7 m |

- "Closes to" is the range craft approach to before firing. Once a target is in reach, a gun fires out to the full range of its ammunition.

- "Spread at 1 km" is the width of the firing cone 1 km out, as shown in the craft editor. The Barracuda's rocket pods spread 10 times wider than the Sturgeon's.

- The Halberd's 35mm guns are turrets: 90°/s traverse, ±20° elevation. The nose turret is limited to ±90° traverse; the mission turret has no limit.

- A gun fires only when all of these hold:

  - the predicted lead point is lined up with the barrel, within 10–60 m depending on the gun;

  - the lead point is within range, and no closer than 5% of the ammunition's range: 88 m for 20mm and 35mm guns, 150 m for rockets, 360 m for the 100mm pods and 400 m for the coilgun;

  - no terrain or friendly ship is in the way.

- Fixed guns need the whole craft pointed at the lead point.

- Against ships, guns aim at a random point on the hull, picked again on each attack run, unless the ATGT setting selects a subsystem. Against craft and missiles they aim at the centre.

- The 20mm Gun never fires at ships.

- Craft dogfight with guns when the enemy craft is within gun range + 1 km, when they launched without missiles or rockets, or when RANGE is set to GUN.

- On a gun run, craft match the target's speed.

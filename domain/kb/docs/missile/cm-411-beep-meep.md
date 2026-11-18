# CM-411 Beep Meep (CM-411)

Tags: kind=missile template; cost=10 pts; body=CM-4 Body
Summary: Size-1 missile, body CM-4 Body; targeting seeker Steerable Extended Active Radar Seeker; validation seeker Fixed Anti-Radiation Seeker; guidance Cruise Guidance; payload Selectable Submunition; targeting seeker Wake-Homing Seeker; 10 points
Source: Player-built missile template (.missile save file); seeker/guidance settings and point cost read from the file.
Cost: wiki component cost 5.25 pts; not priced in the wiki: Cruise Guidance, Selectable Submunition; template total 10 pts, difference 4.75 pts = body + engine

## Slots

| # | Size | Component | Type | Settings |
|---|---|---|---|---|
| 1 | 1 | Steerable Extended Active Radar Seeker (+3 pts) | ActiveSeekerSettings | Mode=Targeting; RejectUnvalidated=false; DetectPDTargets=false |
| 2 | 1 | Fixed Anti-Radiation Seeker (+2 pts) | PassiveARHSeekerSettings | Mode=Validation; RejectUnvalidated=false; TargetType=All |
| 3 | 1 | Cruise Guidance | CruiseGuidanceSettings | Role=Offensive; HotLaunch=false; SelfDestructOnLost=false; Maneuvers=None; DefensiveDoctrine=Mode=Uniform, TargetSizeMask=12, TargetType=All, TargetSizeOrdering=Descending, SalvoSize=0, ConvSalvo=0, HybridSalvo=0, CraftSalvo=0, FarthestFirst=false |
| 4 | 5 | Selectable Submunition | SelectableSubmunitionWarheadSettings | Mode=TargetAcquisition; SpreadOption=0; Range=164; SubmunitionKey=Stock/S1 Rocket; Interval=1 |
| 5 | 9 | - | MissileEngineSettings | - |
| 6 | 1 | Wake-Homing Seeker (+0.25 pts) | PassiveSeekerSettings | Mode=Targeting; RejectUnvalidated=false; DetectPDTargets=false |

Description: mode cruise - mode active abbrev(RADAR)/[mode arad pulsed abbrev(RADAR)]/mode passive abbrev(WAKE) - short subm

## In-game stats

```
The CM-411 Beep Meep is a size 4 waypoint-capable cruise missile. It is based on the CM-4 body, which is a heavy anti-ship torpedo. This missile will deliver a Submunition Delivery warhead. It homes in on its target using an Active Radar seeker, validating that it is the correct target using a Radar Anti-Radiation seeker. If the primary seeker does not find a target or is jammed, it can fall back on a Passive Wake seeker.

controlmethod: mode cruise long
targetingmode: targetingmode pos targetingmode track[+targetingmode trp]

primaryseeker: mode active caps RADAR
validator: ANTI-RADIATION (All RADAR Signals)
backupseeker: mode passive caps (WAKE)

speed: 195 m/s
distance: 33,829 m
topspeedtime: 2.6 s
turnrate: 1.6 G
terminals: None

warhead: detail subm
sumbtype: R-2 'Piranha' Rocket
submcount: 3
submtotalvolume: 27.00 squaremeters
submspread: NARROW CONE
submtime: SHORT (0.25s)

health: 150 
wallthickness: 0.2
progtime: 20 s
radarsig: 100 %
boosttime: 3 s
booststrafe: 100 %
boostturn: 100 %
failrate: 0 %
```

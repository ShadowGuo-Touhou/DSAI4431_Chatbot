# SGM-269 Cucumbers (SGM-269)

Tags: kind=missile template; cost=5 pts; body=SGM-2 Body
Summary: Size-1 missile, body SGM-2 Body; targeting seeker Steerable Active Radar Seeker; targeting seeker Fixed Anti-Radiation Seeker; guidance Direct Guidance; payload Blast Fragmentation; 5 points
Source: Player-built missile template (.missile save file); seeker/guidance settings and point cost read from the file.
Cost: wiki component cost 3.75 pts; template total 5 pts, difference 1.25 pts = body + engine

## Slots

| # | Size | Component | Type | Settings |
|---|---|---|---|---|
| 1 | 1 | Steerable Active Radar Seeker (+1.5 pts) | ActiveSeekerSettings | Mode=Targeting; RejectUnvalidated=false; DetectPDTargets=true |
| 2 | 1 | Fixed Anti-Radiation Seeker (+2 pts) | PassiveARHSeekerSettings | Mode=Targeting; RejectUnvalidated=false; TargetType=JammingOnly |
| 3 | 1 | Direct Guidance (+0 pts) | DirectGuidanceSettings | Role=Defensive; HotLaunch=true; SelfDestructOnLost=false; Maneuvers=None; DefensiveDoctrine=Mode=Matrix, TargetSizeMask=12, TargetType=All, TargetSizeOrdering=Descending, SalvoSize=0, ConvSalvo=16908544, HybridSalvo=16777216, CraftSalvo=16908544, FarthestFirst=false; ApproachAngleControl=true |
| 4 | 6 | Blast Fragmentation (+0.25 pts) | - | - |
| 5 | 4 | - | MissileEngineSettings | - |

Description: mode direct - mode active abbrev(RADAR)/mode arad hoj abbrev(RADAR) - short blastfrag

## In-game stats

```
The SGM-269 Cucumbers is a size 2 direct guidance missile. It is based on the SGM-2 body, which is a flexible mainstay anti-ship missile. This missile will deliver a Proximity Fuze, High Explosive, Blast Fragmentation warhead. It homes in on its target using an Active Radar seeker. If the primary seeker does not find a target or is jammed, it can fall back on a Radar Home-on-Jam seeker.

controlmethod: mode direct
targetingmode: targetingmode pos targetingmode track

primaryseeker: mode active caps RADAR
backupseeker: HOME-ON-JAM (RADAR JAMMING Signals Only)

speed: 200 m/s
distance: 6,000 m
topspeedtime: 0.8 s
turnrate: 4.7 G
terminals: None

warhead: detail blastfrag
armordamage: 0.44cm
componentdamage: 139.30hp
blastradius: 99 m

health: 30 
wallthickness: 0.05
progtime: 8 s
radarsig: 100 %
boosttime: 3 s
booststrafe: 100 %
boostturn: 100 %
failrate: 0 %
```

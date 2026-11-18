# SGM-H-266 Jetpack (SGM-H-266)

Tags: kind=missile template; cost=8 pts; body=SGM-H-2 Body
Summary: Size-1 missile, body SGM-H-2 Body; targeting seeker Steerable Active Radar Seeker; targeting seeker Wake-Homing Seeker; guidance Direct Guidance; payload Blast Fragmentation; 8 points
Source: Player-built missile template (.missile save file); seeker/guidance settings and point cost read from the file.
Cost: wiki component cost 2 pts; template total 8 pts, difference 6 pts = body + engine

## Slots

| # | Size | Component | Type | Settings |
|---|---|---|---|---|
| 1 | 1 | Steerable Active Radar Seeker (+1.5 pts) | ActiveSeekerSettings | Mode=Targeting; RejectUnvalidated=false; DetectPDTargets=true |
| 2 | 1 | Wake-Homing Seeker (+0.25 pts) | PassiveSeekerSettings | Mode=Targeting; RejectUnvalidated=false; DetectPDTargets=true |
| 3 | 1 | Direct Guidance (+0 pts) | DirectGuidanceSettings | Role=Defensive; HotLaunch=false; SelfDestructOnLost=false; Maneuvers=None; DefensiveDoctrine=Mode=Uniform, TargetSizeMask=12, TargetType=All, TargetSizeOrdering=Descending, SalvoSize=0, ConvSalvo=16843008, HybridSalvo=16843008, CraftSalvo=16843008, FarthestFirst=false; ApproachAngleControl=true |
| 4 | 5 | Blast Fragmentation (+0.25 pts) | - | - |
| 5 | 3 | - | MissileEngineSettings | - |
| 6 | 1 | - | MissileEngineSettings | - |

Description: mode direct - mode active abbrev(RADAR)/mode passive abbrev(WAKE) - short blastfrag

## In-game stats

```
The SGM-H-266 Jetpack is a size 2 direct guidance missile. It is based on the SGM-H-2 body, which is a multi-purpose hybrid missile designed to penetrate point defense grids. This missile will deliver a Proximity Fuze, High Explosive, Blast Fragmentation warhead. It homes in on its target using an Active Radar seeker. If the primary seeker does not find a target or is jammed, it can fall back on a Passive Wake seeker.

controlmethod: mode direct
targetingmode: targetingmode pos targetingmode track

primaryseeker: mode active caps RADAR
backupseeker: mode passive caps (WAKE)

Cruise
speed: 350 m/s
distance: 13,234 m
topspeedtime: 4.4 s
turnrate: 0.9 G

Sprint
speed: 500 m/s
distance: 4,375 m
topspeedtime: 0.5 s
turnrate: 14.8 G

: Stage Trigger at 2,000m from Target (Limited By Seeker Range)

terminals: None

warhead: detail blastfrag
armordamage: 0.36cm
componentdamage: 113.74hp
blastradius: 81 m

health: 25 
wallthickness: 0.05
progtime: 10 s
radarsig: 100 %
boosttime: 3 s
booststrafe: 100 %
boostturn: 100 %
failrate: 0 %
```

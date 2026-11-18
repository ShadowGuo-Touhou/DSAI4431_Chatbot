# SGM-H-201 ADASHs (SGM-H-201)

Tags: kind=missile template; cost=10 pts; body=SGM-H-2 Body
Summary: Size-1 missile, body SGM-H-2 Body; targeting seeker Wake-Homing Seeker; guidance Direct Guidance; payload HE Impact; 10 points
Source: Player-built missile template (.missile save file); seeker/guidance settings and point cost read from the file.
Cost: wiki component cost 4 pts; template total 10 pts, difference 6 pts = body + engine

## Slots

| # | Size | Component | Type | Settings |
|---|---|---|---|---|
| 1 | 1 | Command Receiver (+3.5 pts) | CommandSeekerSettings | Mode=Targeting; RejectUnvalidated=false |
| 2 | 1 | Wake-Homing Seeker (+0.25 pts) | PassiveSeekerSettings | Mode=Targeting; RejectUnvalidated=false; DetectPDTargets=true |
| 3 | 1 | Direct Guidance (+0 pts) | DirectGuidanceSettings | Role=Defensive; HotLaunch=false; SelfDestructOnLost=false; Maneuvers=None; DefensiveDoctrine=Mode=Uniform, TargetSizeMask=14, TargetType=SmallCraft, TargetSizeOrdering=Descending, SalvoSize=0, ConvSalvo=16843008, HybridSalvo=16843008, CraftSalvo=16843008, FarthestFirst=false; ApproachAngleControl=true |
| 4 | 5 | HE Impact (+0.25 pts) | - | - |
| 5 | 3 | - | MissileEngineSettings | - |
| 6 | 1 | - | MissileEngineSettings | - |

Description: mode direct - mode command abbrev/mode passive abbrev(WAKE) - short heimpact

## In-game stats

```
The SGM-H-201 ADASHs is a size 2 direct guidance missile. It is based on the SGM-H-2 body, which is a multi-purpose hybrid missile designed to penetrate point defense grids. This missile will deliver a Contact Fuze, High Explosive, Shaped warhead. It homes in on its target using command guidance from its launching ship. If the primary seeker does not find a target or is jammed, it can fall back on a Passive Wake seeker.

controlmethod: mode direct
targetingmode: targetingmode pos targetingmode track

primaryseeker: mode command caps (command commsnote)
backupseeker: mode passive caps (WAKE)

Cruise
speed: 308 m/s
distance: 11,858 m
topspeedtime: 3.0 s
turnrate: 1.6 G

Sprint
speed: 503 m/s
distance: 3,212 m
topspeedtime: 0.4 s
turnrate: 21.7 G

: Stage Trigger at 2,630m from Target

terminals: None

warhead: detail heimpact
armordamage: 54cm
componentdamage: 960hp
blastangle: 70 deg
damageperfragment: 50.0

health: 25 
wallthickness: 0.05
progtime: 10 s
radarsig: 100 %
boosttime: 3 s
booststrafe: 100 %
boostturn: 100 %
failrate: 0 %
```

# SGM-300 Flail (SGM-300)

Tags: kind=missile template; cost=12 pts; body=SGM-3 Body
Summary: Size-1 missile, body SGM-3 Body; targeting seeker Steerable Extended Active Radar Seeker; guidance Direct Guidance; payload HE Impact; 12 points
Source: Player-built missile template (.missile save file); seeker/guidance settings and point cost read from the file.
Cost: wiki component cost 6.75 pts; template total 12 pts, difference 5.25 pts = body + engine

## Slots

| # | Size | Component | Type | Settings |
|---|---|---|---|---|
| 1 | 1 | Steerable Extended Active Radar Seeker (+3 pts) | ActiveSeekerSettings | Mode=Targeting; RejectUnvalidated=true; DetectPDTargets=false |
| 2 | 1 | Command Receiver (+3.5 pts) | CommandSeekerSettings | Mode=Validation; RejectUnvalidated=false |
| 3 | 1 | - | - | - |
| 4 | 1 | Direct Guidance (+0 pts) | DirectGuidanceSettings | Role=Offensive; HotLaunch=true; SelfDestructOnLost=false; Maneuvers=None; DefensiveDoctrine=Mode=Uniform, TargetSizeMask=12, TargetType=All, TargetSizeOrdering=Descending, SalvoSize=0, ConvSalvo=16843008, HybridSalvo=16843008, CraftSalvo=16843008, FarthestFirst=false; ApproachAngleControl=true |
| 5 | 5 | HE Impact (+0.25 pts) | - | - |
| 6 | 5 | - | MissileEngineSettings | - |
| 7 | 1 | - | MissileEngineSettings | - |

Description: mode direct - mode active abbrev(RADAR)/[mode command abbrev] - short heimpact

## In-game stats

```
The SGM-300 Flail is a size 3 direct guidance missile. It is based on the SGM-3 body, which is a TODO. This missile will deliver a Contact Fuze, High Explosive, Shaped warhead. It homes in on its target using an Active Radar seeker, validating that it is the correct target using command guidance from its launching ship.

controlmethod: mode direct
targetingmode: targetingmode pos targetingmode track

primaryseeker: mode active caps RADAR
validator: mode command caps (command commsnote)

Cruise
speed: 250 m/s
distance: 12,188 m
topspeedtime: 2.5 s
turnrate: 1.0 G

Terminal
speed: 440 m/s
distance: 4,041 m
topspeedtime: 1.7 s
turnrate: 9.2 G

: Stage Trigger at 3,470m from Target

terminals: None

warhead: detail heimpact
armordamage: 73cm
componentdamage: 1,800hp
blastangle: 70 deg
damageperfragment: 50.0

health: 60 
wallthickness: 0.05
progtime: 16 s
radarsig: 100 %
boosttime: 3 s
booststrafe: 100 %
boostturn: 100 %
failrate: 0 %
```

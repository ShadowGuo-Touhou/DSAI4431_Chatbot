# SGM-H-202 jkterjter Block II (SGM-H-202)

Tags: kind=missile template; cost=16 pts; body=SGM-H-2 Body
Summary: Size-1 missile, body SGM-H-2 Body; targeting seeker Steerable Extended Active Radar Seeker; guidance Cruise Guidance; payload HE Impact; 16 points
Source: Player-built missile template (.missile save file); seeker/guidance settings and point cost read from the file.
Cost: wiki component cost 6.75 pts; not priced in the wiki: Cruise Guidance; template total 16 pts, difference 9.25 pts = body + engine

## Slots

| # | Size | Component | Type | Settings |
|---|---|---|---|---|
| 1 | 1 | Steerable Extended Active Radar Seeker (+3 pts) | ActiveSeekerSettings | Mode=Targeting; RejectUnvalidated=false; DetectPDTargets=false |
| 2 | 1 | Command Receiver (+3.5 pts) | CommandSeekerSettings | Mode=Validation; RejectUnvalidated=false |
| 3 | 1 | Cruise Guidance | CruiseGuidanceSettings | Role=Offensive; HotLaunch=false; SelfDestructOnLost=false; Maneuvers=None; DefensiveDoctrine=Mode=Uniform, TargetSizeMask=12, TargetType=All, TargetSizeOrdering=Descending, SalvoSize=0, ConvSalvo=0, HybridSalvo=0, CraftSalvo=0, FarthestFirst=false |
| 4 | 4 | HE Impact (+0.25 pts) | - | - |
| 5 | 4 | - | MissileEngineSettings | - |
| 6 | 1 | - | MissileEngineSettings | - |

Description: mode cruise - mode active abbrev(RADAR)/[mode command abbrev] - short heimpact

## In-game stats

```
The SGM-H-202 jkterjter Block II is a size 2 waypoint-capable cruise missile. It is based on the SGM-H-2 body, which is a multi-purpose hybrid missile designed to penetrate point defense grids. This missile will deliver a Contact Fuze, High Explosive, Shaped warhead. It homes in on its target using an Active Radar seeker, validating that it is the correct target using command guidance from its launching ship.

controlmethod: mode cruise long
targetingmode: targetingmode pos targetingmode track[+targetingmode trp]

primaryseeker: mode active caps RADAR
validator: mode command caps (command commsnote)

Cruise
speed: 238 m/s
distance: 25,176 m
topspeedtime: 3.0 s
turnrate: 0.9 G

Sprint
speed: 750 m/s
distance: 5,620 m
topspeedtime: 0.7 s
turnrate: 19.5 G

: Stage Trigger at 4,620m from Target

terminals: None

warhead: detail heimpact
armordamage: 48cm
componentdamage: 768hp
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

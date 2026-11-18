# SGM-H-313 template II (SGM-H-313)

Tags: kind=missile template; cost=46 pts; body=SGM-H-3 Body
Summary: Size-1 missile, body SGM-H-3 Body; targeting seeker Fixed Anti-Radiation Seeker; payload Decoy Launcher; guidance Direct Guidance; payload HE Kinetic Penetrator; 46 points
Source: Player-built missile template (.missile save file); seeker/guidance settings and point cost read from the file.
Cost: wiki component cost 19.25 pts; template total 46 pts, difference 26.75 pts = body + engine

## Slots

| # | Size | Component | Type | Settings |
|---|---|---|---|---|
| 1 | 1 | Command Receiver (+3.5 pts) | CommandSeekerSettings | Mode=Targeting; RejectUnvalidated=false |
| 2 | 1 | Fixed Anti-Radiation Seeker (+2 pts) | PassiveARHSeekerSettings | Mode=Targeting; RejectUnvalidated=false; TargetType=JammingOnly |
| 3 | 1 | Decoy Launcher (+12 pts) | - | - |
| 4 | 1 | Direct Guidance (+0 pts) | DirectGuidanceSettings | Role=Offensive; HotLaunch=false; SelfDestructOnLost=false; Maneuvers=Weave; DefensiveDoctrine=Mode=Uniform, TargetSizeMask=12, TargetType=All, TargetSizeOrdering=Descending, SalvoSize=0, ConvSalvo=16843008, HybridSalvo=16843008, CraftSalvo=16843008, FarthestFirst=false; ApproachAngleControl=true |
| 5 | 5 | HE Kinetic Penetrator (+1.75 pts) | - | - |
| 6 | 5 | - | MissileEngineSettings | - |
| 7 | 1 | - | MissileEngineSettings | - |

Description: mode direct - mode command abbrev/mode arad hoj abbrev(RADAR) - short hekp

## In-game stats

```
The SGM-H-313 template II is a size 3 direct guidance missile. It is based on the SGM-H-3 body, which is a high speed hybrid missile designed to strike heavy targets. This missile will deliver a Delayed Contact Fuze, High Explosive, Kinetic Penetrator warhead. It homes in on its target using command guidance from its launching ship. If the primary seeker does not find a target or is jammed, it can fall back on a Radar Home-on-Jam seeker.

controlmethod: mode direct
targetingmode: targetingmode pos targetingmode track

primaryseeker: mode command caps (command commsnote)
backupseeker: HOME-ON-JAM (RADAR JAMMING Signals Only)

Cruise
speed: 200 m/s
distance: 15,667 m
topspeedtime: 3.3 s
turnrate: 0.7 G

Sprint
speed: 830 m/s
distance: 4,994 m
topspeedtime: 1.0 s
turnrate: 25.0 G

: Stage Trigger at 4,000m from Target (Limited By Seeker Range)

terminals: Weave
(terminals warn range)

warhead: detail hekp

penetrator
armordamage: 544 cm
componentdamage: 212 hp

explosive
componentdamage: 3,600 hp

health: 60 
wallthickness: 0.05
progtime: 16 s
radarsig: 100 %
boosttime: 3 s
booststrafe: 100 %
boostturn: 100 %
failrate: 0 %
```

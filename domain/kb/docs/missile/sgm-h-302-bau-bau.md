# SGM-H-302 Bau Bau (SGM-H-302)

Tags: kind=missile template; cost=19 pts; body=SGM-H-3 Body
Summary: Size-1 missile, body SGM-H-3 Body; targeting seeker Fixed Anti-Radiation Seeker; guidance Direct Guidance; payload HE Impact; 19 points
Source: Player-built missile template (.missile save file); seeker/guidance settings and point cost read from the file.
Cost: wiki component cost 5.75 pts; template total 19 pts, difference 13.25 pts = body + engine

## Slots

| # | Size | Component | Type | Settings |
|---|---|---|---|---|
| 1 | 1 | Command Receiver (+3.5 pts) | CommandSeekerSettings | Mode=Targeting; RejectUnvalidated=false |
| 2 | 1 | Fixed Anti-Radiation Seeker (+2 pts) | PassiveARHSeekerSettings | Mode=Targeting; RejectUnvalidated=false; TargetType=All |
| 3 | 1 | - | - | - |
| 4 | 1 | Direct Guidance (+0 pts) | DirectGuidanceSettings | Role=Offensive; HotLaunch=false; SelfDestructOnLost=false; Maneuvers=Weave; DefensiveDoctrine=Mode=Uniform, TargetSizeMask=12, TargetType=All, TargetSizeOrdering=Descending, SalvoSize=0, ConvSalvo=0, HybridSalvo=0, CraftSalvo=0, FarthestFirst=false; ApproachAngleControl=true |
| 5 | 6 | HE Impact (+0.25 pts) | - | - |
| 6 | 4 | - | MissileEngineSettings | - |
| 7 | 1 | - | MissileEngineSettings | - |

Description: mode direct - mode command abbrev/mode arad pulsed abbrev(RADAR) - short heimpact

## In-game stats

```
The SGM-H-302 Bau Bau is a size 3 direct guidance missile. It is based on the SGM-H-3 body, which is a high speed hybrid missile designed to strike heavy targets. This missile will deliver a Contact Fuze, High Explosive, Shaped warhead. It homes in on its target using command guidance from its launching ship. If the primary seeker does not find a target or is jammed, it can fall back on a Radar Anti-Radiation seeker.

controlmethod: mode direct
targetingmode: targetingmode pos targetingmode track

primaryseeker: mode command caps (command commsnote)
backupseeker: ANTI-RADIATION (All RADAR Signals)

Cruise
speed: 150 m/s
distance: 18,306 m
topspeedtime: 2.2 s
turnrate: 1.1 G

Sprint
speed: 645 m/s
distance: 4,939 m
topspeedtime: 0.8 s
turnrate: 22.9 G

: Stage Trigger at 4,000m from Target (Limited By Seeker Range)

terminals: Weave
(terminals warn range)

warhead: detail heimpact
armordamage: 88cm
componentdamage: 2,592hp
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

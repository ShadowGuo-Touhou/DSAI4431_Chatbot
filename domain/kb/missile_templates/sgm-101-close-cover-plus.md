# SGM-101 Close Cover Plus (SGM-101)

Tags: kind=missile template; cost=7 pts; body=SGM-1 Body
Summary: Size-1 missile, body SGM-1 Body; guidance Direct Guidance; payload Blast Fragmentation EL; 7 points
Source: Player-built missile template (.missile save file); seeker/guidance settings and point cost read from the file.
Cost: wiki component cost 7 pts; template total 7 pts, difference 0 pts = body + engine

## Slots

| # | Size | Component | Type | Settings |
|---|---|---|---|---|
| 1 | 1 | Command Receiver (+3.5 pts) | CommandSeekerSettings | Mode=Targeting; RejectUnvalidated=false |
| 2 | 1 | Direct Guidance (+0 pts) | DirectGuidanceSettings | Role=Defensive; HotLaunch=true; SelfDestructOnLost=false; Maneuvers=None; DefensiveDoctrine=Mode=Matrix, TargetSizeMask=14, TargetType=All, TargetSizeOrdering=Descending, SalvoSize=0, ConvSalvo=131329, HybridSalvo=131329, CraftSalvo=65793, FarthestFirst=false; ApproachAngleControl=true |
| 3 | 3 | Blast Fragmentation EL (+3.5 pts) | - | - |
| 4 | 4 | - | MissileEngineSettings | - |

Description: mode direct - mode command abbrev - short blastfrag

## In-game stats

```
The SGM-101 Close Cover Plus is a size 1 direct guidance missile. It is based on the SGM-1 body, which is a nimble general-purpose missile. This missile will deliver a Proximity Fuze, High Explosive, Blast Fragmentation warhead. It homes in on its target using command guidance from its launching ship.

controlmethod: mode direct
targetingmode: targetingmode pos targetingmode track

primaryseeker: mode command caps (command commsnote)

speed: 278 m/s
distance: 2,166 m
topspeedtime: 0.4 s
turnrate: 12.4 G
terminals: None

warhead: detail blastfrag
armordamage: 0.27cm
componentdamage: 56.58hp
blastradius: 53 m

health: 10 
wallthickness: 0.05
progtime: 6 s
radarsig: 100 %
boosttime: 3 s
booststrafe: 100 %
boostturn: 100 %
failrate: 0 %
```

# SGM-270 Cucumber MK II (SGM-270)

Tags: kind=missile template; cost=7 pts; body=SGM-2 Body
Summary: Size-1 missile, body SGM-2 Body; targeting seeker Fixed Anti-Radiation Seeker; guidance Direct Guidance; payload HE Impact; 7 points
Source: Player-built missile template (.missile save file); seeker/guidance settings and point cost read from the file.
Cost: wiki component cost 5.75 pts; template total 7 pts, difference 1.25 pts = body + engine

## Slots

| # | Size | Component | Type | Settings |
|---|---|---|---|---|
| 1 | 1 | Command Receiver (+3.5 pts) | CommandSeekerSettings | Mode=Targeting; RejectUnvalidated=false |
| 2 | 1 | Fixed Anti-Radiation Seeker (+2 pts) | PassiveARHSeekerSettings | Mode=Targeting; RejectUnvalidated=false; TargetType=JammingOnly |
| 3 | 1 | Direct Guidance (+0 pts) | DirectGuidanceSettings | Role=Offensive; HotLaunch=true; SelfDestructOnLost=false; Maneuvers=None; DefensiveDoctrine=Mode=Matrix, TargetSizeMask=12, TargetType=All, TargetSizeOrdering=Descending, SalvoSize=0, ConvSalvo=16908544, HybridSalvo=16777216, CraftSalvo=16908544, FarthestFirst=false; ApproachAngleControl=true |
| 4 | 6 | HE Impact (+0.25 pts) | - | - |
| 5 | 4 | - | MissileEngineSettings | - |

Description: mode direct - mode command abbrev/mode arad hoj abbrev(RADAR) - short heimpact

## In-game stats

```
The SGM-270 Cucumber MK II is a size 2 direct guidance missile. It is based on the SGM-2 body, which is a flexible mainstay anti-ship missile. This missile will deliver a Contact Fuze, High Explosive, Shaped warhead. It homes in on its target using command guidance from its launching ship. If the primary seeker does not find a target or is jammed, it can fall back on a Radar Home-on-Jam seeker.

controlmethod: mode direct
targetingmode: targetingmode pos targetingmode track

primaryseeker: mode command caps (command commsnote)
backupseeker: HOME-ON-JAM (RADAR JAMMING Signals Only)

speed: 200 m/s
distance: 6,000 m
topspeedtime: 0.8 s
turnrate: 4.7 G
terminals: None

warhead: detail heimpact
armordamage: 66cm
componentdamage: 1,440hp
blastangle: 70 deg
damageperfragment: 50.0

health: 30 
wallthickness: 0.05
progtime: 8 s
radarsig: 100 %
boosttime: 3 s
booststrafe: 100 %
boostturn: 100 %
failrate: 0 %
```

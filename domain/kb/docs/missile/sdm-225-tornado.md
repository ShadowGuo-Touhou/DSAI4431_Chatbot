# SDM-225 Tornado (SDM-225)

Tags: kind=missile template; cost=4 pts; body=SDM-2 Body
Summary: Size-1 missile, body SDM-2 Body; targeting seeker Fixed Active Radar Seeker; targeting seeker Wake-Homing Seeker; guidance Direct Guidance; payload Blast Fragmentation; 4 points
Source: Player-built missile template (.missile save file); seeker/guidance settings and point cost read from the file.
Cost: wiki component cost 1.5 pts; template total 4 pts, difference 2.5 pts = body + engine

## Slots

| # | Size | Component | Type | Settings |
|---|---|---|---|---|
| 1 | 1 | Fixed Active Radar Seeker (+1 pts) | ActiveSeekerSettings | Mode=Targeting; RejectUnvalidated=false; DetectPDTargets=false |
| 2 | 1 | Wake-Homing Seeker (+0.25 pts) | PassiveSeekerSettings | Mode=Targeting; RejectUnvalidated=false; DetectPDTargets=false |
| 3 | 1 | Direct Guidance (+0 pts) | DirectGuidanceSettings | Role=Defensive; HotLaunch=false; SelfDestructOnLost=false; Maneuvers=None; DefensiveDoctrine=TargetSizeMask=12, TargetType=SmallCraft, TargetSizeOrdering=Descending, SalvoSize=0, FarthestFirst=false; ApproachAngleControl=true |
| 4 | 4 | Blast Fragmentation (+0.25 pts) | - | - |
| 5 | 3 | - | MissileEngineSettings | - |
| 6 | 1 | - | MissileEngineSettings | - |

Description: DIRECT - ACT(RADAR)/PSV(WAKE) - HE FRAG

## In-game stats

```
The SDM-225 Tornado is a size 2 direct guidance missile. It is based on the SDM-2 body, which is a flexible defensive missile with a booster. This missile will deliver a Proximity Fuze, High Explosive, Blast Fragmentation warhead. It homes in on its target using an Active Radar seeker If the primary seeker does not find a target or is jammed, it can fall back on a Passive Wake seeker.

Control Method: DIRECT
Targeting Modes: POSITION TRACK

Primary Seeker: ACTIVE RADAR
Backup Seeker: PASSIVE (WAKE)

Boost
Speed: 850 m/s
Distance: 7,898 m
Top Speed In: 1.4 s
Turn Rate: 5.0 G

Main
Speed: 150 m/s
Distance: 1,765 m
Top Speed In: 0.5 s
Turn Rate: 8.2 G

: Stage Trigger at 820m from Target or On Burnout

Terminal Maneuvers: None

Warhead: Proximity Fuze, High Explosive, Blast Fragmentation
Armor: 0.31cm
Component: 98.50hp
Blast Radius: 70 m

Body Integrity: 25 
Wall Thickness: 0.05
Programming Time: 10 s
Radar Signature Bonus: 100 %
Boost-Phase Duration: 3 s
Boost-Phase Strafe: 100 %
Boost-Phase Turn Rate: 100 %
Failure Rate: 0 %
```

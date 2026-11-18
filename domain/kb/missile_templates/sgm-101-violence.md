# SGM-101 Violence (SGM-101)

Tags: kind=missile template; cost=2 pts; body=SGM-1 Body
Summary: Size-1 missile, body SGM-1 Body; targeting seeker Fixed Active Radar Seeker; guidance Direct Guidance; payload HE Impact; 2 points
Source: Player-built missile template (.missile save file); seeker/guidance settings and point cost read from the file.
Cost: wiki component cost 1.25 pts; template total 2 pts, difference 0.75 pts = body + engine

## Slots

| # | Size | Component | Type | Settings |
|---|---|---|---|---|
| 1 | 1 | Fixed Active Radar Seeker (+1 pts) | ActiveSeekerSettings | Mode=Targeting; RejectUnvalidated=false; DetectPDTargets=false |
| 2 | 1 | Direct Guidance (+0 pts) | DirectGuidanceSettings | Role=Offensive; HotLaunch=true; SelfDestructOnLost=false; Maneuvers=None; DefensiveDoctrine=TargetSizeMask=12, TargetType=All, TargetSizeOrdering=Descending, SalvoSize=0, FarthestFirst=false; ApproachAngleControl=false |
| 3 | 3 | HE Impact (+0.25 pts) | - | - |
| 4 | 4 | - | MissileEngineSettings | - |

Description: DIRECT - ACT(RADAR) - HE SHAPED

## In-game stats

```
The SGM-101 Violence is a size 1 direct guidance missile. It is based on the SGM-1 body, which is a nimble general-purpose missile. This missile will deliver a Contact Fuze, High Explosive, Shaped warhead. It homes in on its target using an Active Radar seeker.

Control Method: DIRECT
Targeting Modes:
 POSITION TRACK
Primary Seeker: ACTIVE RADAR

301 m/s for 7,050 m, top speed in 0.9 s
Terminal Maneuvers: None

Contact Fuze, High Explosive, Shaped
Armor: 27cm Component: 238hp
Blast Angle: 70 deg
Damage Per Fragment: 50.0

Body Integrity: 10 
Wall Thickness: 0.5
Programming Time: 6 s
Radar Signature Bonus: 100 %
Boost-Phase Duration: 3 s
Boost-Phase Strafe: 100 %
Boost-Phase Turn Rate: 100 %
Failure Rate: 0 %
```

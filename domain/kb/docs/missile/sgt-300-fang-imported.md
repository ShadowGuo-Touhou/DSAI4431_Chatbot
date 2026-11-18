# SGT-300 Fang (Imported) (SGT-300)

Tags: kind=missile template; cost=9 pts; body=SGT-3 Body
Summary: Size-1 missile, body SGT-3 Body; targeting seeker Fixed Anti-Radiation Seeker; guidance Direct Guidance; payload HE Impact; 9 points
Source: Player-built missile template (.missile save file); seeker/guidance settings and point cost read from the file.
Cost: wiki component cost 5.75 pts; template total 9 pts, difference 3.25 pts = body + engine

## Slots

| # | Size | Component | Type | Settings |
|---|---|---|---|---|
| 1 | 1 | Command Receiver (+3.5 pts) | CommandSeekerSettings | Mode=Targeting; RejectUnvalidated=false |
| 2 | 1 | Fixed Anti-Radiation Seeker (+2 pts) | PassiveARHSeekerSettings | Mode=Targeting; RejectUnvalidated=false; TargetType=JammingOnly |
| 3 | 1 | Direct Guidance (+0 pts) | DirectGuidanceSettings | Role=Offensive; HotLaunch=false; SelfDestructOnLost=false; Maneuvers=None; DefensiveDoctrine=TargetSizeMask=12, TargetSizeOrdering=Descending, SalvoSize=0, FarthestFirst=false; ApproachAngleControl=false |
| 4 | 4 | HE Impact (+0.25 pts) | - | - |
| 5 | 10 | - | MissileEngineSettings | - |

Description: DIRECT - CMD/HOJ(RADAR) - HE SHAPED

## In-game stats

```
The SGT-300 Fang (Imported) is a size 3 direct guidance missile. It is based on the SGT-3 body, which is a heavy anti-ship torpedo. This missile will deliver a Contact Fuze, High Explosive, Shaped warhead. It homes in on its target using command guidance from its launching ship If the primary seeker does not find a target or is jammed, it can fall back on a Radar Home-on-Jam seeker.

Control Method: DIRECT
Targeting Modes:
 POSITION TRACK
Primary Seeker: COMMAND (Requires COMMS Enabled)
Backup Seeker(s): HOME-ON-JAM (RADAR JAMMING Signals Only)

244 m/s for 4,674 m, top speed in 1.5 s
Terminal Maneuvers: None

Contact Fuze, High Explosive, Shaped
Armor: 93cm Component: 2,880hp
Blast Angle: 70 deg
Damage Per Fragment: 50.0

Body Integrity: 160 
Programming Time: 3 s
Radar Signature Bonus: 100 %
Boost-Phase Duration: 3 s
Boost-Phase Strafe: 100 %
Boost-Phase Turn Rate: 100 %
Failure Rate: 0 %
```

# SGM-H-200 Suisei Block II (SGM-H-200)

Tags: kind=missile template; cost=30 pts; body=SGM-H-2 Body
Summary: Size-1 missile, body SGM-H-2 Body; targeting seeker Electro-Optical Seeker; targeting seeker Steerable Extended Active Radar Seeker; guidance Cruise Guidance; payload HE Kinetic Penetrator; 30 points
Source: Player-built missile template (.missile save file); seeker/guidance settings and point cost read from the file.
Cost: wiki component cost 12.75 pts; not priced in the wiki: Cruise Guidance; template total 30 pts, difference 17.25 pts = body + engine

## Slots

| # | Size | Component | Type | Settings |
|---|---|---|---|---|
| 1 | 1 | Electro-Optical Seeker (+8 pts) | PassiveSeekerSettings | Mode=Targeting; RejectUnvalidated=false; DetectPDTargets=false |
| 2 | 1 | Steerable Extended Active Radar Seeker (+3 pts) | ActiveSeekerSettings | Mode=Targeting; RejectUnvalidated=false; DetectPDTargets=false |
| 3 | 1 | Cruise Guidance | CruiseGuidanceSettings | Role=Offensive; HotLaunch=false; SelfDestructOnLost=false; Maneuvers=Corkscrew; DefensiveDoctrine=TargetSizeMask=12, TargetType=All, TargetSizeOrdering=Descending, SalvoSize=0, FarthestFirst=false |
| 4 | 5 | HE Kinetic Penetrator (+1.75 pts) | - | - |
| 5 | 3 | - | MissileEngineSettings | - |
| 6 | 1 | - | MissileEngineSettings | - |

Description: CRUISE - PSV(EO)/ACT(RADAR) - HEKP

## In-game stats

```
The SGM-H-200 Suisei Block II is a size 2 waypoint-capable cruise missile. It is based on the SGM-H-2 body, which is a multi-purpose hybrid missile designed to penetrate point defense grids. This missile will deliver a Delayed Contact Fuze, High Explosive, Kinetic Penetrator warhead. It homes in on its target using a Passive Electro-Optical seeker If the primary seeker does not find a target or is jammed, it can fall back on an Active Radar seeker.

Control Method: CRUISE (Waypoint Capable)
Targeting Modes:
 POSITION TRACK[+TRP]
Primary Seeker: PASSIVE (EO)
Backup Seeker(s): ACTIVE RADAR

Cruise: 210 m/s for 15,685 m, top speed in 2.0 s
Sprint: 500 m/s for 4,375 m, top speed in 0.5 s
 Stage Trigger at 3,570m from Target
Terminal Maneuvers: Corkscrew

Delayed Contact Fuze, High Explosive, Kinetic Penetrator
Penetrator:
 Armor: 157 cm
 Component: 141 hp
Explosive:
 Component: 1,600 hp

Body Integrity: 25 
Wall Thickness: 0.5
Programming Time: 10 s
Radar Signature Bonus: 100 %
Boost-Phase Duration: 3 s
Boost-Phase Strafe: 100 %
Boost-Phase Turn Rate: 100 %
Failure Rate: 0 %
```

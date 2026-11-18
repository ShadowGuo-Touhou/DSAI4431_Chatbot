# SGM-29 EA29 Killjoy (SGM-29)

Tags: kind=missile template; cost=7 pts; body=SGM-2 Body
Summary: Size-1 missile, body SGM-2 Body; targeting seeker Fixed Active Radar Seeker; guidance Direct Guidance; 7 points
Source: Player-built missile template (.missile save file); seeker/guidance settings and point cost read from the file.
Cost: wiki component cost 6 pts; template total 7 pts, difference 1 pts = body + engine

## Slots

| # | Size | Component | Type | Settings |
|---|---|---|---|---|
| 1 | 1 | Fixed Active Radar Seeker (+1 pts) | ActiveSeekerSettings | Mode=Targeting; RejectUnvalidated=false; DetectPDTargets=false |
| 2 | 1 | Self-Screening Jammer (+5 pts) | - | - |
| 3 | 1 | Direct Guidance (+0 pts) | DirectGuidanceSettings | Role=Defensive; HotLaunch=true; SelfDestructOnLost=false; Maneuvers=None; DefensiveDoctrine=Mode=Matrix, TargetSizeMask=12, TargetType=All, TargetSizeOrdering=Descending, SalvoSize=0, ConvSalvo=0, HybridSalvo=0, CraftSalvo=0, FarthestFirst=false; ApproachAngleControl=true |
| 4 | 1 | - | - | - |
| 5 | 9 | - | MissileEngineSettings | - |

Description: mode direct - mode active abbrev(RADAR) - none

## In-game stats

```
The SGM-29 EA29 Killjoy is a size 2 direct guidance missile. It is based on the SGM-2 body, which is a flexible mainstay anti-ship missile. This missile will deliver no payload. It homes in on its target using an Active Radar seeker.

controlmethod: mode direct
targetingmode: targetingmode pos targetingmode track

primaryseeker: mode active caps RADAR

speed: 180 m/s
distance: 22,064 m
topspeedtime: 0.9 s
turnrate: 3.2 G
terminals: None

health: 30 
wallthickness: 0.05
progtime: 8 s
radarsig: 100 %
boosttime: 3 s
booststrafe: 100 %
boostturn: 100 %
failrate: 0 %
```

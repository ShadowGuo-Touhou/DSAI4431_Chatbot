# SGM-206 Musket (SGM-206)

Tags: kind=missile template; cost=7 pts; body=SGM-2 Body
Summary: Size-1 missile, body SGM-2 Body; targeting seeker Fixed Active Radar Seeker; validation seeker Wake-Homing Seeker; guidance Cruise Guidance; payload HE Impact; 7 points
Source: Player-built missile template (.missile save file); seeker/guidance settings and point cost read from the file.
Cost: wiki component cost 1.5 pts; not priced in the wiki: Cruise Guidance; template total 7 pts, difference 5.5 pts = body + engine

## Slots

| # | Size | Component | Type | Settings |
|---|---|---|---|---|
| 1 | 1 | Fixed Active Radar Seeker (+1 pts) | ActiveSeekerSettings | Mode=Targeting; RejectUnvalidated=false; DetectPDTargets=false |
| 2 | 1 | Wake-Homing Seeker (+0.25 pts) | PassiveSeekerSettings | Mode=Validation; RejectUnvalidated=false; DetectPDTargets=false |
| 3 | 1 | Cruise Guidance | CruiseGuidanceSettings | Role=Offensive; HotLaunch=true; SelfDestructOnLost=false; Maneuvers=Weave; DefensiveDoctrine=Mode=Uniform, TargetSizeMask=12, TargetType=All, TargetSizeOrdering=Descending, SalvoSize=0, ConvSalvo=16843008, HybridSalvo=16843008, CraftSalvo=16843008, FarthestFirst=false |
| 4 | 5 | HE Impact (+0.25 pts) | - | - |
| 5 | 5 | - | MissileEngineSettings | - |

Description: mode cruise - mode active abbrev(RADAR)/[mode passive abbrev(WAKE)] - short heimpact

## In-game stats

```
The SGM-206 Musket is a size 2 waypoint-capable cruise missile. It is based on the SGM-2 body, which is a flexible mainstay anti-ship missile. This missile will deliver a Contact Fuze, High Explosive, Shaped warhead. It homes in on its target using an Active Radar seeker, validating that it is the correct target using a Passive Wake seeker.

controlmethod: mode cruise long
targetingmode: targetingmode pos targetingmode track[+targetingmode trp]

primaryseeker: mode active caps RADAR
validator: mode passive caps (WAKE)

speed: 240 m/s
distance: 17,000 m
topspeedtime: 1.7 s
turnrate: 1.9 G
terminals: Weave
(terminals warn range)

warhead: detail heimpact
armordamage: 60cm
componentdamage: 1,200hp
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

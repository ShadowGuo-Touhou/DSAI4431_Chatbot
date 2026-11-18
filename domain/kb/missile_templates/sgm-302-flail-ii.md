# SGM-302 Flail II (SGM-302)

Tags: kind=missile template; cost=13 pts; body=SGM-3 Body
Summary: Size-1 missile, body SGM-3 Body; targeting seeker Steerable Extended Active Radar Seeker; targeting seeker Fixed Anti-Radiation Seeker; guidance Cruise Guidance; payload HE Impact; 13 points
Source: Player-built missile template (.missile save file); seeker/guidance settings and point cost read from the file.
Cost: wiki component cost 5.25 pts; not priced in the wiki: Cruise Guidance; template total 13 pts, difference 7.75 pts = body + engine

## Slots

| # | Size | Component | Type | Settings |
|---|---|---|---|---|
| 1 | 1 | Steerable Extended Active Radar Seeker (+3 pts) | ActiveSeekerSettings | Mode=Targeting; RejectUnvalidated=true; DetectPDTargets=false |
| 2 | 1 | Fixed Anti-Radiation Seeker (+2 pts) | PassiveARHSeekerSettings | Mode=Targeting; RejectUnvalidated=false; TargetType=All |
| 3 | 1 | - | - | - |
| 4 | 1 | Cruise Guidance | CruiseGuidanceSettings | Role=Offensive; HotLaunch=false; SelfDestructOnLost=false; Maneuvers=None; DefensiveDoctrine=Mode=Uniform, TargetSizeMask=12, TargetType=All, TargetSizeOrdering=Descending, SalvoSize=0, ConvSalvo=16843008, HybridSalvo=16843008, CraftSalvo=16843008, FarthestFirst=false |
| 5 | 5 | HE Impact (+0.25 pts) | - | - |
| 6 | 5 | - | MissileEngineSettings | - |
| 7 | 1 | - | MissileEngineSettings | - |

Description: mode cruise - mode active abbrev(RADAR)/mode arad pulsed abbrev(RADAR) - short heimpact

## In-game stats

```
The SGM-302 Flail II is a size 3 waypoint-capable cruise missile. It is based on the SGM-3 body, which is a TODO. This missile will deliver a Contact Fuze, High Explosive, Shaped warhead. It homes in on its target using an Active Radar seeker. If the primary seeker does not find a target or is jammed, it can fall back on a Radar Anti-Radiation seeker.

controlmethod: mode cruise long
targetingmode: targetingmode pos targetingmode track[+targetingmode trp]

primaryseeker: mode active caps RADAR
backupseeker: ANTI-RADIATION (All RADAR Signals)

Cruise
speed: 210 m/s
distance: 19,686 m
topspeedtime: 2.0 s
turnrate: 1.1 G

Terminal
speed: 440 m/s
distance: 4,041 m
topspeedtime: 1.7 s
turnrate: 9.2 G

: Stage Trigger at 3,450m from Target

terminals: None

warhead: detail heimpact
armordamage: 73cm
componentdamage: 1,800hp
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

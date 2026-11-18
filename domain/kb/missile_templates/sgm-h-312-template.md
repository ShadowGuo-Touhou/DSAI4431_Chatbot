# SGM-H-312 template (SGM-H-312)

Tags: kind=missile template; cost=22 pts; body=SGM-H-3 Body
Summary: Size-1 missile, body SGM-H-3 Body; targeting seeker Steerable Active Radar Seeker; targeting seeker Fixed Anti-Radiation Seeker; guidance Cruise Guidance; payload HE Impact; 22 points
Source: Player-built missile template (.missile save file); seeker/guidance settings and point cost read from the file.
Cost: wiki component cost 3.75 pts; not priced in the wiki: Cruise Guidance; template total 22 pts, difference 18.25 pts = body + engine

## Slots

| # | Size | Component | Type | Settings |
|---|---|---|---|---|
| 1 | 1 | Steerable Active Radar Seeker (+1.5 pts) | ActiveSeekerSettings | Mode=Targeting; RejectUnvalidated=false; DetectPDTargets=false |
| 2 | 1 | Fixed Anti-Radiation Seeker (+2 pts) | PassiveARHSeekerSettings | Mode=Targeting; RejectUnvalidated=false; TargetType=All |
| 3 | 1 | - | - | - |
| 4 | 1 | Cruise Guidance | CruiseGuidanceSettings | Role=Offensive; HotLaunch=false; SelfDestructOnLost=false; Maneuvers=Corkscrew; DefensiveDoctrine=Mode=Uniform, TargetSizeMask=12, TargetType=All, TargetSizeOrdering=Descending, SalvoSize=0, ConvSalvo=0, HybridSalvo=0, CraftSalvo=0, FarthestFirst=false |
| 5 | 5 | HE Impact (+0.25 pts) | - | - |
| 6 | 5 | - | MissileEngineSettings | - |
| 7 | 1 | - | MissileEngineSettings | - |

Description: mode cruise - mode active abbrev(RADAR)/mode arad pulsed abbrev(RADAR) - short heimpact

## In-game stats

```
The SGM-H-312 template is a size 3 waypoint-capable cruise missile. It is based on the SGM-H-3 body, which is a high speed hybrid missile designed to strike heavy targets. This missile will deliver a Contact Fuze, High Explosive, Shaped warhead. It homes in on its target using an Active Radar seeker. If the primary seeker does not find a target or is jammed, it can fall back on a Radar Anti-Radiation seeker.

controlmethod: mode cruise long
targetingmode: targetingmode pos targetingmode track[+targetingmode trp]

primaryseeker: mode active caps RADAR
backupseeker: ANTI-RADIATION (All RADAR Signals)

Cruise
speed: 150 m/s
distance: 20,050 m
topspeedtime: 2.3 s
turnrate: 1.0 G

Sprint
speed: 725 m/s
distance: 6,101 m
topspeedtime: 0.9 s
turnrate: 23.0 G

: Stage Trigger at 3,000m from Target (Limited By Seeker Range)

terminals: Corkscrew
(terminals warn range)

warhead: detail heimpact
armordamage: 80cm
componentdamage: 2,160hp
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

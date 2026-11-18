# CM-401 Broken Spine II (CM-401)

Tags: kind=missile template; cost=5 pts; body=CM-4 Body
Summary: Size-1 missile, body CM-4 Body; targeting seeker Fixed Anti-Radiation Seeker; validation seeker Wake-Homing Seeker; guidance Cruise Guidance; payload HE Impact; targeting seeker Steerable Active Radar Seeker; 5 points
Source: Player-built missile template (.missile save file); seeker/guidance settings and point cost read from the file.
Cost: wiki component cost 4 pts; not priced in the wiki: Cruise Guidance; template total 5 pts, difference 1 pts = body + engine

## Slots

| # | Size | Component | Type | Settings |
|---|---|---|---|---|
| 1 | 1 | Fixed Anti-Radiation Seeker (+2 pts) | PassiveARHSeekerSettings | Mode=Targeting; RejectUnvalidated=false; TargetType=All |
| 2 | 1 | Wake-Homing Seeker (+0.25 pts) | PassiveSeekerSettings | Mode=Validation; RejectUnvalidated=false; DetectPDTargets=false |
| 3 | 1 | Cruise Guidance | CruiseGuidanceSettings | Role=Offensive; HotLaunch=false; SelfDestructOnLost=false; Maneuvers=None; DefensiveDoctrine=Mode=Uniform, TargetSizeMask=12, TargetType=All, TargetSizeOrdering=Descending, SalvoSize=0, ConvSalvo=0, HybridSalvo=0, CraftSalvo=0, FarthestFirst=false |
| 4 | 4 | HE Impact (+0.25 pts) | - | - |
| 5 | 10 | - | MissileEngineSettings | - |
| 6 | 1 | Steerable Active Radar Seeker (+1.5 pts) | ActiveSeekerSettings | Mode=Targeting; RejectUnvalidated=false; DetectPDTargets=false |

Description: mode cruise - mode arad pulsed abbrev(RADAR)/[mode passive abbrev(WAKE)]/mode active abbrev(RADAR) - short heimpact

## In-game stats

```
The CM-401 Broken Spine II is a size 4 waypoint-capable cruise missile. It is based on the CM-4 body, which is a heavy anti-ship torpedo. This missile will deliver a Contact Fuze, High Explosive, Shaped warhead. It homes in on its target using a Radar Anti-Radiation seeker, validating that it is the correct target using a Passive Wake seeker. If the primary seeker does not find a target or is jammed, it can fall back on an Active Radar seeker.

controlmethod: mode cruise long
targetingmode: targetingmode pos targetingmode track[+targetingmode trp]

primaryseeker: ANTI-RADIATION (All RADAR Signals)
validator: mode passive caps (WAKE)
backupseeker: mode active caps RADAR

speed: 210 m/s
distance: 24,368 m
topspeedtime: 2.4 s
turnrate: 2.0 G
terminals: None

warhead: detail heimpact
armordamage: 76cm
componentdamage: 1,920hp
blastangle: 70 deg
damageperfragment: 50.0

health: 150 
wallthickness: 0.2
progtime: 20 s
radarsig: 100 %
boosttime: 3 s
booststrafe: 100 %
boostturn: 100 %
failrate: 0 %
```

# Intelligence › Intel Packets

Source: Official wiki (wiki.hoodedhorse.com), game 0.6.2.6:260903-1430

## Body
Warships have an identification difficulty of 200 per identity step. Marauder and Moorline liner hulls (Bulk Hauler, Container Hauler, and their civilian and refit variants) have 300. A Signature Scrambler adds +100%, and the civilian Bulk Hauler hull modifier is -90%. These are the baseline sizes of intel packets. If a ship has higher identification difficulty, only the identity steps scale. The status report always costs a fixed 200 and does not scale. Identity is revealed in four stages, each costing the identification difficulty (200 on a normal warship). Once the track is known as a warship, a 200-effort status report is worked at the same time, and it is gathered again only when that report's state changes:

- Packet 1 is of size 200.

- Once the track is identified as a warship, a 200-point status report (ship status, COND%, PD%, debuffs) is gathered in parallel with the remaining identity steps; the first status information appears at about 400 cumulative intel effort.

- After the first status report, each change in reported status fields (Condition, Command, movement status, etc.) requires 200 additional intel effort to refresh the report.

The track info update would progress as follows:

| Stage/report | Track information | Effort for this stage/report | Approximate time at 1 effort/s | Approximate time at 4 effort/s | Approximate time at 15 effort/s |
|---|---|---|---|---|---|
| Initial | Track ####-Unknown | 0 | 0s | 0s | 0s |
| Identity 1 | Warship | 200 | 200s | 50s | 13.3s |
| Identity 2 | Warship (Class) | 200 | 400s | 100s | 26.7s |
| First status report (parallel) | Ship Status, COND%, PD%, debuffs | 200 after Warship is known | about 400s | about 100s | about 26.7s |
| Identity 3 | Class (Hull) | 200 | 600s | 150s | 40s |
| Identity 4 | Ship Name (Hull), with the already gathered status report | 200 | 800s | 200s | 53.3s |
| Status refresh | Updated report after a reported field changes | 200 per refresh | 200s after the change | 50s after the change | 13.3s after the change |

Image of a track with the heading and velocity vectors labelled.

The intel gathered is shared to the entire team, and if the component providing intel is lost, other intel sources can continue where it left off assuming they can see the track.[2]

Missile identity is four 20-point stages (the first shows that it is a missile, the last shows its name), and those stages are never penalized. The seeker combination is a separate 20-point report that starts once the track is known to be a missile. That report takes a 0.1x penalty unless the intel component's class matches, so an Intelligence Center (1.5/s on the report) finishes seekers at about 14.7 s while the name is already shown at about 5.3 s. A Scryer keeps 10/s, so seekers finish at about 4 s and the name at about 8 s.

Once the contact is held as a Visual, Tracked or Locked track, its heading and velocity will be displayed in the tactical view as a disconnected line pointing out of the track and a line with a circle respectively. The velocity stick approximately shows where the ship will be in 10 seconds.needs confirmation

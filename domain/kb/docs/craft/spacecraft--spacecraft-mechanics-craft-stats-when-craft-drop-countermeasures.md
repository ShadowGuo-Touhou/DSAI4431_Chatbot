# Spacecraft › Spacecraft Mechanics › Craft Stats › When craft drop countermeasures

Source: Official wiki (wiki.hoodedhorse.com), game 0.6.2.6:260903-1430

## Body
- Craft drop countermeasures only while evading. An evasion starts when a missile is 5 s or less from impact (3 s or less with DFTAC OUT-G).

- Each evasion drops at most one pattern, at its start. An evasion lasts up to 6 s.

- When a different threat becomes the most urgent, a new evasion starts and drops a new pattern. A staggered salvo can use up several patterns.

- A new pattern can't start until 2.5 s after the previous one began.

- Craft know the incoming missile's seeker types without needing intel on it.

Evasion manoeuvres:

- Notch: fly straight away from the missile for 1.5 s (2.5 s when the Halberd, Barracuda, Pike or Tanto notches against a seeker that is neither radar nor wake), then turn across its path, presenting a side profile in the hopes that seduced missiles will be unable to re-acquire[5]. The pattern drops at the start, while the craft is still flying away, so the trail is usually not side-on to the missile.

- Scoot: turn onto a new, partly random course. The code tilts the direction to the missile by angles fixed to the map, so the course is not at a set angle to the missile.

- Flee: fly straight away from the threat.

- Jink: turn hard across the line to the threat. DFTAC OUT-G uses this against missiles.

- Sweeping turn: turn around to face an attacker behind the craft.

| Missile seeker | Halberd, Barracuda, Pike, Tanto | Claymore, Sturgeon, Sundial |
|---|---|---|
| Radar, or radar + wake | Notch + pattern | Notch + pattern |
| Wake only | Scoot + pattern | Scoot + pattern |
| Any other | Notch, no pattern | Flee + pattern |

Against gunfire from enemy craft:

- The Halberd, Barracuda and Pike jink when two or more enemy guns are firing at them and the fire is 1 s from impact. Two guns on one enemy craft count as two.

- The Tanto turns to face an attacker behind it under the same conditions, and its flight-mates are ordered to attack the shooter.

- The Claymore, Sturgeon and Sundial flee when gunfire is 5 s from impact.

- The same gun can't trigger another evasion until 12 s after the last one started.

- None of these drop a pattern unless CMSR is set to ALL.

| Setting | Behaviour |
|---|---|
| CMSR (countermeasure use) AUTO | As in the table above. With DFTAC set to NOTCH, SCRAM or OUT-G, a pattern only against radar or wake seekers. |
| CMSR ALL | A pattern on every evasion, including evasions from enemy gunfire. |
| CMSR NEVER | No automatic patterns. |
| DEFND (missile self-defense) AUTO | Evades missiles automatically. |
| DEFND MAN | Evades missiles only during a 30 s window opened with Left Shift + Z. Pressing it again while the window is open restarts the window and makes every craft in the flight drop one pattern at once. |
| DFTAC (missile self-defense tactics) NOTCH | Always notch, starting at 5 s from impact. |
| DFTAC SCRAM | Always flee, starting at 5 s from impact. |
| DFTAC OUT-G | Jink, starting later, at 3 s or less from impact. |

Gunfire evasion does not depend on DEFND.

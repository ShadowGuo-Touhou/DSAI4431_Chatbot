# Spacecraft › Spacecraft Mechanics › Controls › Stance Controls

Source: Official wiki (wiki.hoodedhorse.com), game 0.6.2.6:260903-1430

## Body
Spacecraft behaviour is controlled by toggling behaviors in the craft stance control board, similarly to ship postures. Spacecraft launch with the default stances shown on the right. The stances are:

| State | Behaviour |
|---|---|
| OFF | Craft will fly at their cruise speed, using the regular amount of fuel. |
| ON | Craft will fly at their hard-burn speed, (usually 1.5x cruise speed) and increased fuel consumption (varies by craft type) |

| State | Behaviour |
|---|---|
| WEDGE | Craft flights will fly in a wedge-shaped pattern, pointing in the direction of travel. |
| LINE | Craft flights will fly in a line-shaped pattern, perpendicular to the direction of travel. |
| CROSS | Craft flights will fly in a cross-shaped pattern, perpendicular to the direction of travel. |
| ECHE | Craft flights will fly in an echelon (diagonal line) shaped pattern. |

Craft not in formation will speed up faster than their top speed in attempt to form up; this includes when swapping formation.

| State | Behaviour |
|---|---|
| DIRECT | Craft will fly straight towards their destination, and remain still when loitering. |
| JUKE | Craft will constantly make small directional changes as they fly or loiter. |
| EVADE | Craft will constantly make large directional changes as they fly or loiter. |

| State | Behaviour |
|---|---|
| PSV | Craft will follow orders normally, unless dogfighting AI is triggered due to an enemy craft attack. |
| AGRSV | When not already attacking, craft attack the nearest enemy craft within about 5 km. Does not trigger on missiles. |
| EVASV | Craft will not automatically engage enemy craft, including when attacked or while guarding. They still dodge attacks with their normal evasion. |

| State | Behaviour |
|---|---|
| SKOSH | Craft will automatically return to base once all missiles in the flight are expended. |
| WINCH | Craft will automatically return to base once all ammo, including guns, in the flight is expended. |
| NEVER | Craft will not automatically return to base. |

| State | Behaviour |
|---|---|
| AUTO | Craft will attack multiple different targets if assigned to attack a craft/missile but will attack the selected target if ordered to attack a ship. |
| FOCUS | Craft will always attack the selected target. |
| SPLIT | Craft will always attack multiple different targets. |

| State | Behaviour |
|---|---|
| AUTO | Craft will fire as if on UNLIM against ships but will reduce missile amounts against craft/missiles. |
| ONE | Craft will not fire more missiles against a target if one missile is already in flight for that target. Resets on re-issuing attack order. |
| TWO | Craft will not fire more missiles against a target if two missiles are already in flight for that target. Resets on re-issuing attack order. |
| THREE | Craft will not fire more missiles against a target if three missiles are already in flight for that target. Resets on re-issuing attack order. |
| FOUR | Craft will not fire more missiles against a target if four missiles are already in flight for that target. Resets on re-issuing attack order. |
| UNLIM | Craft will fire missiles regardless of missiles already in flight. |

- The following rules about craft behavior applies for all craft launched with missiles; craft launched only with guns will follow old behavior (i.e. always closing to the range of the shortest range weapon, which is the gun).

- * Craft ordered to attack other craft loiter at about 75% of their missiles' maximum range (and, on STND-IN, no farther than about 4 km), or where they already were if that was closer, and fire missiles at the enemy group.

- Craft will not automatically close with the enemy group to use guns, even when out of missiles.

- Craft will only dogfight with guns if the enemy is within about 1 km beyond gun range, or they were already in gun range when the attack order was issued.

| State | Anti-Craft | Anti-Ship |
|---|---|---|
| STND-IN | Close to 4000m or 75% of munition max range, whichever is closer | Close to 4000m or 95% of munition max range, whichever is closer |
| STND-OF | Close to 75% of munition max range | Close to 95% of munition max range |
| GUN | Close to gun range[1] | Same as STND-IN Anti-Ship |

| State | Behaviour |
|---|---|
| ALL | Craft target random aimpoints like a ship would |
| ENGINE | Craft target drives and main thrusters |
| DEFWEP | Craft target Point Defense weapons |
| OFFWEP | Craft target Offensive weapons |
| SENSOR | Craft target Radar Panels |

| State | Behaviour |
|---|---|
| ON | Craft turn Radar(s) on |
| OFF | Craft turn Radar(s) off for a −5% Radar signature reduction, equivalent to a ×0.99 Detection range modifier |

| State | Behaviour |
|---|---|
| AUTO | Craft will evade missiles automatically according to the table here |
| MAN | Evades missiles only during a 30 s window opened with Left Shift + Z. Pressing it again while the window is open restarts the window and makes every craft in the flight drop one pattern at once. |

| State | Behaviour |
|---|---|
| AUTO | Evades missiles automatically. Craft will follow the default evasion behavior for the seeker targeting them described here. |
| NOTCH | Always notch, starting at 5 s from impact. |
| SCRAM | Always flee, starting at 5 s from impact.[2] |
| OUT-G | Jink, starting later, at 3 s or less from impact. Craft will attempt to out-pull the missile as it gets close |

| State | Behaviour |
|---|---|
| AUTO | As in the table here. With DFTAC set to NOTCH, SCRAM or OUT-G, a pattern is dropped only against radar or wake seekers. |
| ALL | A pattern on every evasion, even if the seeker type is not seduced by them, including evasions from enemy gunfire.[3] |
| NEVER | No automatic patterns. Manual patterns using Left Shift + Z are still accepted |

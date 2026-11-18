# Radar › Mechanics › Track Quality

Source: Official wiki (wiki.hoodedhorse.com), game 0.6.2.6:260903-1430

## Body
| Track Quality | Inaccuracy (m) |
|---|---|
| TQ15 | 0.0 - 4.0 |
| TQ14 | 4.0 - 9.1 |
| TQ13 | 9.1 - 14.6 |
| TQ12 | 14.6 - 20.5 |
| TQ11 | 20.5 - 26.9 |
| TQ10 | 26.9 - 34.0 |
| TQ9 | 34.0 - 41.8 |
| TQ8 | 41.8 - 50.5 |
| TQ7 | 50.5 - 60.3 |
| TQ6 | 60.3 - 71.7 |
| TQ5 | 71.7 - 85.2 |
| TQ4 | 85.2 - 101.6 |
| TQ3 | 101.6 - 122.9 |
| TQ2 | 122.9 - 152.8 |
| TQ1 | 152.8+ |

In game, track quality is graded on a scale from TQ15 to TQ1, where TQ15 is a near perfect track, and TQ1 is nearly unusable. This is calculated by the formula:

[math]\displaystyle{ \text{TQ}=\lfloor 15^{1.02-0.005\delta_R}\rfloor }[/math], clamped between 1 and 15,

where [math]\displaystyle{ \delta_R }[/math] is the position error of the track in meters.

This can be used to convert TQ into an approximate meters of inaccuracy

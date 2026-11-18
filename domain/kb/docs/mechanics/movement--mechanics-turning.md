# Movement › Mechanics › Turning

Source: Official wiki (wiki.hoodedhorse.com), game 0.6.2.6:260903-1430

## Body
Ships have an angular thrust for turning and rolling. It is possible to calculate the time to turn a ship's nose 180°.

| Hull | Inertia Factor [math]\displaystyle{ F_y }[/math] |
|---|---|
| Sprinter | 1.59 |
| Raines | 2.16 |
| Keystone | 4.09 |
| Vauxhall | 8.32 |
| Axford | 8.72 |
| Solomon | 17.2 |

- [math]\displaystyle{ P \equiv \text{Angular Thrust (as seen in-game)} }[/math]

- [math]\displaystyle{ M \equiv \text{Ship Mass (as seen in-game)} }[/math]

- [math]\displaystyle{ F \equiv \text{Ship Inertia Factor (see chart)} }[/math]

Because of damping, ships will accelerate only to a certain maximum speed given by (in radians per second), [math]\displaystyle{ \omega_\text{max} = \frac{1000P}{MF} }[/math]

The time in seconds, [math]\displaystyle{ t }[/math], to turn 180° is: [math]\displaystyle{ \large{{t \approx \frac{\pi}{\omega_\text{max}} + 10}} }[/math]

([math]\displaystyle{ \omega_\text{max} }[/math] is usually smaller than the listed max turn rate, [math]\displaystyle{ R }[/math], except for buffed light ships and possibly when rolling. To compare the two, take [math]\displaystyle{ R }[/math], multiply by [math]\displaystyle{ \pi }[/math], and divide by 180. If the result is [math]\displaystyle{ < \omega_\text{max} }[/math], then replace [math]\displaystyle{ \omega_\text{max} }[/math] in the equation above by the result.)

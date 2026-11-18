# Crew › Mechanics › Crew Damage

Source: Official wiki (wiki.hoodedhorse.com), game 0.6.2.6:260903-1430

## Body
Crew inside components can be damaged when the component is damaged.

When the component is below 50% health after being damaged, the crew has a chance to be damaged based on the hull's vulnerability stat and the attack's crew damage multiplier. That chance is doubled if the hit destroys the component or the component was already destroyed. e.g. a ship with 40% crew vulnerability would normally have a 40% chance, but a shell with a 0.75 or -25% crew vulnerability multiplier reduces that to 30%, reducing that shell's capability to damage crew. Conversely, a shell with 1.50 or +50% crew vulnerability multiplier increases that to 60%, boosting the shell's capability to damage crew.

If the chance succeeds, the amount of crew is reduced by [math]\displaystyle{ \frac{D}{12\times \text{MaxHp}} }[/math] where D is the incoming damage on that component and MaxHp is the maximum hp of the component they are in. This has a 50% chance to round up or round down.

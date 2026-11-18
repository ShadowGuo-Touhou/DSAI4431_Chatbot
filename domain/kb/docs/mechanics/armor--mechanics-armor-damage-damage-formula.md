# Armor › Mechanics › Armor Damage › Damage Formula

Source: Official wiki (wiki.hoodedhorse.com), game 0.6.2.6:260903-1430

## Body
For shells that do not ignore armor angling, AP is modified based on the impact angle and amount of armor remaining. Simply, AP is scaled by the fraction of itself over RA.

Putting it all together, the actual shredding applied to the armor is

[math]\displaystyle{ \text{actualDamage} = \text{AP}\times\rho\times\min\left(\frac{\text{AP}}{\text{RA}}\, ,\, 1\right) }[/math]

- where [math]\displaystyle{ \rho }[/math] is 0.2 if the shot ricochets or 1 if it does not. Then [math]\displaystyle{ \text{actualDamage} }[/math] is shredded from the armor in a rough circle across the armor shredding radius centered at the point of impact.

For example, a 120mm AP Shell strikes a Solomon at at 30 degree angle from the normal.

- AP = 45 cm.

- EA = NA / cos(30) = 64.7 cm.

- RA = EA (because this Solomon has not taken any hits there)

- Does not ricochet.

Then the actualDamage done is [math]\displaystyle{ \text{actualDamage} = 45 \times \frac{45}{64.7} = 31.3\, \text{cm} }[/math]. So the Solomon would have 24.7 cm of armor remaining in that spot.

- Note that even if armor is reduced to zero, the attack will not penetrate unless the earlier [math]\displaystyle{ \text{AP} \geq \text{RA} }[/math] condition is fulfilled. This generally happens at steeper angles, eg 60cm pen vs 56cm armor at 30 degrees will not penetrate, but will fully strip armor.[needs confirmation]

- Some damage types such as HEI warheads (missiles, rockets, mines), and Plasma ignore armor angle and will strip listed penetration regardless of angle. Beams never ricochet but still use effective armor thickness (nominal thickness divided by cos θ, capped at 2.5× nominal), so angled hits shred armor more slowly than perpendicular hits. [2]

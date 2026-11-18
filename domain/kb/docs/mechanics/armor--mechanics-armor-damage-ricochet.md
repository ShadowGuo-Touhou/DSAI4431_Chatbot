# Armor › Mechanics › Armor Damage › Ricochet

Source: Official wiki (wiki.hoodedhorse.com), game 0.6.2.6:260903-1430

## Body
Shells can ricochet off of armor at steep angles with reduced shredding and a visual effect.

If a shell does not have the AP to penetrate, it will ricochet if the angle to the normal is greater than 80 degrees:

[math]\displaystyle{ \text{ricochet if}\quad \theta\geq 80^\circ }[/math] Ignoring armor angling does not by itself prevent a ricochet: the ricochet test still uses the real impact angle. Missiles, rockets, mines, bombs and beams never ricochet because they set NeverRicochet. Plasma ignores angling for thickness and can still ricochet.[1]

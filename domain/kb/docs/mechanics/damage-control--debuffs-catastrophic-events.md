# Damage Control › Debuffs/Catastrophic Events

Source: Official wiki (wiki.hoodedhorse.com), game 0.6.2.6:260903-1430

## Body
Components can suffer various types of Critical Events (aka debuffs) in game, some would slow down the work speed of your damage control team, while others may degrade your ship's performance, or even obliterate your ship entirely.

Damage has a chance of causing debuffs on components. This chance is calculated by [math]\displaystyle{ \exp\left( -3Hp-0.5\right)\times C }[/math] where [math]\displaystyle{ Hp }[/math] is the current Hp percentage as a decimal and [math]\displaystyle{ C }[/math] is the critical event multiplier of the damage. This means baseline debuff chance for damage with 1x critical event multiplier starts at ∼3% and increases to ∼60% as the component takes damage.

This crit then has a chance of being a catastrophic based on the component's Catastrophic event probability.

The time to repair a debuff is determined by the repair speed of the DC team and the repair work required

# Component Damage › Damage Type Overviews › HEI (Missile)

Source: Official wiki (wiki.hoodedhorse.com), game 0.6.2.6:260903-1430

## Body
Diagram of the behavior of HEI and HEKP warheads on an Axford. Not to scale. By smolcake.

HEI splits its damage into multiple fragments (aka rays), each dealing 50 dmg. The amount of fragments totals up to the listed damage value. e.g. a missile that has a listed damage of 1440 will split its damage into 28 fragments dealing 50 dmg, with one fragment left over dealing 40 dmg.

These fragments spray out from the impact location in a 35 deg cone pattern in the direction of the missile (note that the cone angles given on this page use internal values, and are therefore only half of the full angle). Each fragment splits their damage among all components in a 70m line (ignores pendepth mechanics), and do not overpenetrate. (e.g. the damage ray hitting two components will deal 25 damage to each, hitting three components will deal ~17 damage to each)

HEI warheads ignore armor angling.

For missiles, HE armor shredding radius gradually increases with the warhead's armor penetration stat as warhead size increases. The shredding radius curve starts at 3.5m, goes to 5m at 1500 cm penetration, 8m at 5000 cm penetration. However HE Impact armor penetration stays about 27-150 cm, so the radius stays near the curve's start (about 3.5 in raw brush size) and does not reach the values listed at 5 and 8 m in practice, which sit at 1500 cm and 5000 cm of armor penetration.

Rockets function similarly, but with a slightly wider 45 deg cone and a variable ray length from 40m to 60m

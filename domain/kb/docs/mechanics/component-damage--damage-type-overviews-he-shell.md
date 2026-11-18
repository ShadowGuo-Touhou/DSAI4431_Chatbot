# Component Damage › Damage Type Overviews › HE (Shell)

Source: Official wiki (wiki.hoodedhorse.com), game 0.6.2.6:260903-1430

## Body
HE shells create an explosion (sphere) inside the ship at a point along their path of travel. Any components that touch this sphere are damaged. The damage of the round is spread between all components equally. For example, a 150 damage shell will do 30 damage to 5 components or 75 damage to 2 components. If they overpen, the round does not create an explosion and the reduced damage is spread equally among all components that the round intersected with.

The explosion position is determined by the pendepth and the penetration envelope stat. Most HE shells have a penetration envelope of 0.8, which places the explosion at a random point between 20% and 180% of pendepth (the code lerps from 1 - envelope to 1 + envelope, so the average is 100%). The component tooltip says 80-100%, but the placement method does not do that.

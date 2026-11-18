# Component Damage › Damage Type Overviews › HEKP (Missile)

Source: Official wiki (wiki.hoodedhorse.com), game 0.6.2.6:260903-1430

## Body
| ANS Hull | Armor | Internal Density (cm/m) | HEKP Pen |
|---|---|---|---|
| Sprinter | 8cm | 0.50 | 106cm |
| Raines | 15cm | 0.50 | 124cm |
| Keystone | 22cm | 0.50 | 141cm |
| Vauxhall | 26cm | 1.00 | 237cm |
| Axford | 40cm | 1.20 | 306cm |
| Solomon | 56cm | 1.20 | 346cm |
| OSP Hull | Armor | Internal Density (cm/m) | HEKP Pen |
| Ferryman | 5cm | 0.50 | 99cm |
| Draugr | 5cm | 0.50 | 99cm |
| Flathead | 48cm | 0.75 | 249cm |
| Ocello | 30cm | 1.20 | 281cm |
| Marauder | 20cm | 0.25 | 93cm |
| Moorline | 20cm | 0.25 | 93cm |

The HEKP penetrator is a spherical hitbox 10m wide and hits all components in a straight line up to 175m from the impact location. It spreads its listed damage equally among all hit components. The penetrator has a 2.0m armor shredding radius

The HEKP explosive creates a line of explosions along the path of the penetrator, and deals more overall damage as penetration depth increases, up to its listed maximum damage at 175m. HEKP does not suffer an explicit overpen penalty, but smaller hulls may not be large enough to allow the HEKP penetrator to travel 175m for maximum damage.

HEKP's explosion pattern is fixed, and broadly does not change regardless of warhead size, missile speed, or other factors. The HEKP Explosive splits its damage among 26 explosions[6]. It tries to drop one explosion exactly every 6.6m (up to the maximum depth of 175m). If the explosive cannot drop all 26 explosions (either because the ship's hull is thinner than 175m, or the Penetrator did not travel 175m), then the damage in those explosions are lost. However, the total explosion damage will never go below 40%; The remaining explosions will have their damage scaled up to meet the 40% minimum.

Explosion count is rounded down, one per 6.6 m. A hit that fails to penetrate creates none, but a penetrating hit is given at least 15 m of pendepth, so it always creates at least 2 explosions and those explosions are scaled up to the 40% damage minimum.

HEKP explosion radius varies throughout the explosion chain, peaking at ~25m radius at the 18th/19th explosion (~119m deep) and dropping off to ~7.5m radius near the beginning and end. Damage per explosion is the same for each explosion. Damage per explosion is distributed between components similarly to an HE shell. Armor shredding radius scales in a similar way, peaking at 6.0m (12m diameter in the best case) and dropping off to ~1.8m at the beginning and end. This is measured from the explosion point, not from the nearest surface.[7]

While the explosion damage and armor shredding value scales with warhead size, the shredding and damage radius are fixed regardless of warhead size

# Component Damage › Damage Type Overviews › RPF (Shell) › Bomb (Shell)

Source: Official wiki (wiki.hoodedhorse.com), game 0.6.2.6:260903-1430

## Body
Bomb shells hit all ships within their blast radius (500m radius for both 600mm and 250mm bomb shells) with multiple fragments. These fragments are distributed randomly across the target's bounding radius. Or in other words, if you imagine a circle that circumscribes the ship, the fragments fired at that ship will be distributed randomly inside that circle. Each fragment acts like an AP shell. 600mm Bomb Shells emit 12 fragments per target, each dealing 40 damage. 250mm Bomb shells emit 6 fragments per target, each dealing 16 damage. The listed damage assumes 5 targets for 600mm bomb shells and 4 targets for 250mm bomb shells.

This can result in some fragments missing the ship, e.g. 600mm bomb shells will not always score 12 hits on every ship in its radius as ships do not fully encompass their bounding radius. In addition, these fragments can strike other targets inside the blast radius besides their intended target. Each bomb shell fragment will now try up to several times to to find a ray which hits the target's hull, twice for 250mm bomb shells and 3 times for 600mm bomb shells.

Bomb shell fragments ignore normal penetration depth mechanics; if the fragment penetrates armor, they will always penetrate a certain depth into the hull regardless of interior density or leftover penetration.

Bomb shells explode with a timed fuze. When firing on tracks, that timed fuze is stepped back by 0.35 seconds (600mm) or 0.1875 seconds (250mm), and randomly varies ±0.2 seconds (600mm) or ±0.15 seconds (250mm)

Bomb shell fragments have a crit rate of 2%.

Missiles and Craft within 300m of a 600mm bomb shell explosion have a 25% chance of being damaged for 30 damage, 0.2cm pen. Missiles and Craft within 100m of a 250mm bomb shell explosion have a 50% chance of being damaged for 30 damage, 0.1cm pen. This blast radius is purely antimissile/craft and does not affect ships.

500mm Fracturing Block fired by Mass Drivers also has an on-hit bombshell fragment effect, with fragments cast at nearby ships that are visible from the impact point.

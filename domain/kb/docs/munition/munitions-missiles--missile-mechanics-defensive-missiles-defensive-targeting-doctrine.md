# Munitions & Missiles › Missile Mechanics › Defensive Missiles › Defensive Targeting Doctrine

Source: Official wiki (wiki.hoodedhorse.com), game 0.6.2.6:260903-1430

## Body
Doctrine decides how defensive missiles are fired against incoming missiles. These settings can be overridden by the Point Defense Missile Setting if Fire Mode is switched away from DCTRN/D.

Threat size controls which missile threats the AMM will automatically launch against. Size 1, 2, and/or 3 can be toggled on or off. There is an additional switch which allows the missile to target all missiles (ALL), conventional missiles only (CONV),hybrid missiles only (HYBRID), and spacecraft (CRAFT). The threat types of some special missiles are listed below.

- SDM-1: Size 1 conventional

- SDM-2: Size 2 Conventional

- SGM-H-2: Size 2 Hybrid

- SGM-H-3: Size 3 Hybrid

- SGM-3: Size 3 Hybrid

- Containers: Size 3 conventional

- R-2 Rockets: Size 1 conventional (size-2 body with its point-defense threat size overridden to 1)

- Mines: Size 3 conventional

- Fighters: Size 2 spacecraft

- Bombers: Size 3 spacecraft

- SEWAC / Skiff / Scout: Size 1 spacecraft

Alternatively, a more in-depth matrix targeting system can be used. This presents all of the same information above but allows for more defined behavior; for instance a missile can be targeted towards specific types of craft and missiles. Missiles using this matrix system, even if the information in it is otherwise identical to the above system, is easier for the game to read and allows for more reliable use of multiple types of defensive missiles on the same ship.

The size ordering setting has three modes.

- DESCEND: The missile will be fired at the largest valid threat size first before firing against smaller threats.

- ASCEND: The missile will be fired at the smallest valid threat size first before firing against larger threats.

- EQUAL: The missile launch sequence will be unaffected by threat size so long as it is the correct size.

The salvo size setting controls whether 1, 2 or 3 AMMs will be fired at a threat.

- NEAR-TO-FAR: The missile will be fired at the closest threats first before firing against further threats.

- FAR-TO-NEAR: The missile will be fired at the furthest threats first before firing against closer threats.

# Component Damage › Damage Mechanics › Structure break

Source: Official wiki (wiki.hoodedhorse.com), game 0.6.2.6:260903-1430

## Body
Structure boxes of the different hulls. Diagram by PuppyFromHell

All ships have a "Structure hitbox". If an attack's path crosses the structure hitbox and no component collider, destroyed components included, the damage is dealt to the structure. Hits below 20 damage after damage reduction do not count toward structure HP. Once enough damage has been dealt to the structure, the ship becomes structure broken, and any more damage to the structure is redirected to a random component, as if it had hit that components instead. In this state, crew also take 50% more damage

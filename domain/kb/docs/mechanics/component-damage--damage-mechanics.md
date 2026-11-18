# Component Damage › Damage Mechanics

Source: Official wiki (wiki.hoodedhorse.com), game 0.6.2.6:260903-1430

## Body
Most attacks will use some kind of ray or sphere collider (aka hitboxes) to determine which components are hit and damaged, with the specifics varying depending on damage type (some attacks even use multiple colliders).

Components that are damaged below 0 HP will be destroyed (greyed out). Destroyed components generally can't be hit by further attacks, and cannot be repaired unless a restore is used.

However, there are two mechanics that can prevent a component from being destroyed at 0 HP: Damage Threshold, and (Reinforced).

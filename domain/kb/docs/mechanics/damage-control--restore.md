# Damage Control › Restore

Source: Official wiki (wiki.hoodedhorse.com), game 0.6.2.6:260903-1430

## Body
A component becomes Destroyed only when a hit reduces it to 0 HP and that hit is larger than its damage threshold. A reinforced component must already be at 0 HP before that hit. A component at 0 HP that has not been destroyed can still be repaired normally. In this state, the component can no longer be hit by any further damage (and is therefore treated as empty space by attacks), nor will it be automatically repaired by the control team. To bring it back online, you need to spend the Restores provided in DC Lockers. By Shift+LClicking a destroyed component, you can order a damage control team to preform a restore on the destroyed component. After the restore progress is completed, the component is instantly repaired to its minimum functioning HP plus its max repair. Restores require 50 "hp" worth of work to apply.

Restores are taken first from a docked repair service if one is supplying them, otherwise from non-reinforced lockers, then from lockers with the lowest damage threshold, then from lockers with the fewest restores remaining. Distance does not matter. The restore is consumed when the restore work finishes.

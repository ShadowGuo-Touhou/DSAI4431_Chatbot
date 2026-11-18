# Munitions & Missiles › Notes

Source: Official wiki (wiki.hoodedhorse.com), game 0.6.2.6:260903-1430

## Body
- ↑ It can be assumed that the final result will either require all validators or only one validator in order to count as passed, but there appears to be a bug where the pass/fail status is set by an assignment operator rather than a bitwise operator, making each validator overwrite the previous one, resulting in only the last validator in the list having an impact.

- ↑ Stands for Time To Go to Intercept. This is measured using the missile's current speed. In addition, it's measured using the target's actual position, so direction only seekers will still benefit

- ↑ Minimum Sprint Engine Cost is 2

- ↑ Minimum Sprint Engine Cost is 3

- ↑ Mine comms are similar to CMD but do not check for same jammer cone

- ↑ Oddly, damage types that emit multiple rays (HEI, frac blocks, HE-SH) will only hit decoy containers with one ray, which results in strange behavior such as HEI always dealing 50 damage per hit regardless of warhead size, or fracturing blocks taking ten hits to destroy decoy containers. Decoy containers will also be hit by RPF fragments, unlike every other missile.

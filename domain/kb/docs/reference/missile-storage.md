# Missiles: launchers, storage and the designer

Source: Official wiki (wiki.hoodedhorse.com), game 0.6.2.6:260903-1430; launcher capacities are read from each launcher's own Stats block.

## How a missile gets to the target

A missile is a special munition. It is not fired from a gun: it is launched by a missile launcher, and the player builds it in the in-game missile designer from a body, a payload, avionics and a seeker package.

## VLS and TLS: cells inside the launcher

Vertical and trainable launch systems keep their missiles in the launcher itself. Each launcher's Stats block has `Capacity (cells, minimum)` and `Missile Size`; the wiki's "minimum" is the cell count in the launcher's own footprint, and the real ceiling is that count scaled by the slot (empty cells are the floor, never the ceiling). Fixed-cell launchers do not scale: VLS-1-23 always holds 23 S1 cells, VLS-1-46 always 46. Resizable ones (VLS-2 / VLS-3 / CLS-3) scale as `floor(slot.x / module.x) * floor(slot.z / module.z) * cells_per_module` — see `zh/弹药装载与弹库规则.md` for the measured table (VLS-2: 16 cells in a 3x4x3 slot, 24 in 3x4x5, 64 in 6x4x6, 80 in 8x7x8; VLS-3 and CLS-3 hold exactly a quarter of that). When planning a VLS/TLS ship, look up the slot, take the cell count, and put one missile of the matching size in each cell.

## MLS and SALS: magazine-fed

Missile launch systems that draw from the ship's ammunition storage do not carry cells of their own: their missiles compete with shells for the same magazine space. For these, plan magazine capacity and ammunition mixes, not launcher cells.

## Working rule for missile builds

Use the player-supplied missile templates as the reference loadout. Change only the seeker package the player asks for (primary, secondary, validation) and recompute the point cost from the component table. Do not design a missile from scratch unless the player explicitly asks for a new design; the named designs on the wiki are examples, not fixed loadouts.

# Radar › Mechanics › Burn-through sweep

Source: Official wiki (wiki.hoodedhorse.com), game 0.6.2.6:260903-1430

## Body
Some radars can perform a Burn-Through Sweep, or more simply "Burn sweep"[6]. A burn sweep releases a single pulse with greatly increased radiated power (the normal radiated power multiplied by the Burn-Through Power Mult.), capable of detecting stealthy targets or penetrating through jamming.

Anything the burn sweep detects will me marked as a purple circle, which will be called a burn track. These burn tracks are similar to regular radar tracks, and carry both position and velocity data (velocity data is not displayed in game but attacks fired on the track will account for it). Note that burn tracks are only a single snapshot, and do not update unless another burn sweep is performed. This means that burn tracks will become progressively inaccurate if the target moves away.

These tracks serve to update the range memory of jamming LOBs.

Burn tracks last for 30 seconds. They will replace ELINT tracks, but are in turn replaced by regular radar or vis tracks

Ships can detect when they are hit by a burn sweep, and will display an indicator when it happens.

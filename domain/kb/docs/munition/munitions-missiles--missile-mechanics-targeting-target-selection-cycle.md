# Munitions & Missiles › Missile Mechanics › Targeting › Target Selection Cycle

Source: Official wiki (wiki.hoodedhorse.com), game 0.6.2.6:260903-1430

## Body
Most seekers choose targets with a lottery. Every 0.5 seconds, the seeker sweeps its cone for targets and adds them to a list. Note that this list is not stored between search cycles, the only thing the missile remembers is the "current target".

- Each target is given an initial score based on its power, how strong the signal is. All powers fall off with distance, so closer targets are usually scored higher initially.

  - ACT and SAH power is based on the radar return power density. Also, targets further from the center of the missile's view are scored lower, down to 50% at the edge. ACT power is based on the distance from the missile to the target. SARH power uses both the illuminator-to-target distance, including where the target sits in the illuminator cone, and the target-to-missile distance.

  - For the EO seeker, ship size does not matter; ships give off the same "optical" power, modified only by their distance to the seeker.

- If the missile has an active validator, the validator checks each target and marks it as valid or invalid (this is not saved between seeker cycles for validators other than [ARAD], which has a 30 second memory)

  - If the missile has multiple validators, every validator will check each target.[1]

  - If the seeker is set to accept unvalidated, and at least one target is valid, then every invalid is removed from the list. If no targets are valid, then the validator is ignored.

  - If the seeker is set to reject unvalidated, invalid targets are always ignored.

- The scores of the targets are then modified based on a few factors

  - If the missile has a current target, and that target appears in the list again, then:

    - If the time to impact is less than the seeker's lock Target TTGI[2] stat (3.0 seconds for most vanilla seekers, 2.5s for ACT seekers, 2.0s for WAKE variants), the seeker is guaranteed to choose this target again.

    - Otherwise, its score is multiplied by the Target Affinity stat of the seeker (10x for most seekers, 3x for WAKE variants).

  - If the seeker is EO, and it was fired at a track with intel, all targets matching the same ship class have their scores multiplied by 250.

- Select a random target weighted by the scores of the targets remaining in the list.

CMD seekers do not undergo this process as their only target is the track they were fired on.

If the seeker is under jamming, the target's return power has to exceed the combined jamming power felt by the seeker to detect the target and add it to the lottery. Note that this is slightly different from the search radar calculations, as the combined jamming power is compared directly without converting it to noise first. As a result, missile seekers are not affected by ambient noise at all.

If the seeker is jammed and cannot see any targets, it will follow a fake target, therefore causing the missile to veer off target. This fake target is placed 1km away from the missile, at a random point up to 4 degrees off the nose with a velocity of 10m/s in a random direction, and changes once every second. Equipping the missile with any validator and setting the seeker to reject unvalidated will push the fake target out to 50km, preventing premature staging if the seeker can detect range.

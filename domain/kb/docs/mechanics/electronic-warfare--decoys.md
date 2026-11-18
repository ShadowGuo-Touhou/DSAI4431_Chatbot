# Electronic Warfare › Decoys

Source: Official wiki (wiki.hoodedhorse.com), game 0.6.2.6:260903-1430

## Body
The EA12 chaff decoy will burst into a cloud of radar-reflective chaff, creating a radar false-target with considerable RCS. This creates a stationary false contact on enemy and friendly radar, and also seduce ACT seekers of any type, and if it is located within the cone of radar illuminator, also has the chance of seducing SAH seekers. The decoy's signature starts out at ~22,000m2 signature and decays over time, down to ~14,500m2 after 38 seconds, and rapidly down to ∼3,300m2 when it expires after 45 seconds.

The more expensive EA14 decoy exclusive to OSP works in a similar way, but has ~40,000m2 sig instead, and decays down to ~26,400m2 after 38 seconds, and down to ∼6,000m2 when it expires after 45 seconds.

The EA20 flare decoy upon deployment will spray out a cloud of hot particles that seduce WAKE seekers. This decoy decays over time, down to 85% after 24 seconds, and down to 15% when it expires at 40 seconds

The EA99 active decoy exclusive to ANS imitates ship active and passive signature, seducing ACT ARAD and SAH(if illuminated). The decoy travels at 20m/s in a direction for 30 seconds before it expires and has a constant signature. Active decoys have an incredibly high signature size of ~400,000m2 However, the active decoy is only 1.0% as effective at reflecting illuminators, and therefore may struggle to attract SAH in certain cases. While EA99 decoys will not be fired by the untargeted decoy button or the decoy hotkey, Fire Decoy in the action menu opened on a track will launch them, and automatic point-defense decoy launch can launch them too. They can also be fired manually from the EWAR menu (although their slow speed and short range limits the utility of this function)

A special note about chaff is that they are assigned radar track numbers in a fixed order: if I deploy five chaff, with track numbers 1000, 1001, 1002, 1003, and 1004, upon the first chaff expiring redeploying chaff will see track number 1000 assigned to that new chaff cloud. This has practical applications via CMD; if a CMD missile were fired at track 1002 from the above example, it will guide onto the third chaff cloud deployed until it expires; I can then fire three more chaff, and the CMD guidance will re-acquire on the third chaff deployed.

One quirk of this is that chaff clouds use the same fixed order for all chaff clouds in the game, seemingly as long as said chaff clouds are tracked by your team. Thus, if one ship deploys chaff, another ship deploys chaff, and a third ship deploys chaff on the enemy team, they have numbers 1000, 1001, and 1002, as normal. This sequence can also break, under unknown circumstances.

The Craft countermeasures mounted onto each Spacecraft operate slightly different from the above decoys. Specifically the craft decoys are combination chaff and flare decoy that will seduce RADAR, WAKE, and THERM seekers. In addition they do not leave an additional sensor track when deployed.

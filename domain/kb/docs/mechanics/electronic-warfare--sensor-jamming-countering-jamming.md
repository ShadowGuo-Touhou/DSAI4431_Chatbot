# Electronic Warfare › Sensor Jamming › Countering Jamming

Source: Official wiki (wiki.hoodedhorse.com), game 0.6.2.6:260903-1430

## Body
The simplest approach to counter jamming is simply to get within the maximum range. However this may be impractical if the enemy is maneuvering or firing back. There are several tools available to raise the effective spotting range:

- Fire Control Radars such as the RF101 Bullseye or RF44 Pinpoint have better stats than search radars, and can greatly increase range once a lock is acquired.

- Burnthrough Sweeps greatly increase the transmitted power by the radar for a single pulse, providing a one-off track that can be used for a FCR to lock or RPF/Bombshell to get some fire on the target. Be aware that not every radar is capable of performing a Burnthrough Sweep.

- Illuminators, especially the E57 Floodlight, increase the return power. The general rule of thumb is that one Floodlight defeats one jammer.

- The Adaptive Radar Receiver improves noise filtering (i.e. makes it more negative).

The other primary way to defeat jamming is to simply not be in the jamming cone. The longest range for vanilla radar jammers is 10km for both the Blanket and Bellbird. The R400 Bloodhound (14 km, fixed, 10 degree beam) and the Early Warning Radar can stay beyond 10 km and still detect ships inside a vanilla radar jammer. The RS41 Spyglass (11.5 km instrumented) only does this against destroyer-size and larger targets: at best aspect it is signal-limited to about 9.6 km against a corvette and about 10.2 km against a frigate. Similarly, ships can move laterally to get outside of the enemy jamming cone, allowing them to spot the target and relay that to the team (called "offset spotters"). A team spread across a wide area is much more resistant to radar jamming compared to a team that is tightly grouped.

Jamming only works on active radar sensors, and therefore other sensors are unaffected. All ships can detect targets visually around themselves (roughly 3km around every ship), and ELINT systems such as the Pinard can detect enemy radar emissions even when jammed. Note that the Pinard cannot detect the jamming itself.

Most search radars will be able to produce a line of bearing (LOB) toward any jammers that are affecting the radar. The R400 Bloodhound, the R550 Early Warning Radar, and fire-control radars produce none. Jamming LOBs will remember the last range to the ship that is doing the jamming, provided a track on the ship was held within 30 seconds of when the jamming started (the stored range jitters by about 100 m). Any later track on that ship replaces it, and a bearing-only track (ELINT, or one ship's strobe correlator) places the contact about 100 km out along the bearing. This LOB range can be updated via crossfix, briefly regaining the track, or burn pings. Time-fuzed shells can base their timing on this last known range. While the accuracy of this Jam LOB varies from radar to radar, and is rarely accurate enough for gunfire or other dumb weaponry, the LOB is still useful for quickly responding with counterfire, whether it be RPF/Bombshell, missiles, sending jamming back at the enemy, or just knowing where to close in. LOBs can be crossfixed via strobe correlator.

Additionally, the purple LOB produced by the strobe correlator can be locked by a ship's FCR, unlike a normal red jamming LOB.

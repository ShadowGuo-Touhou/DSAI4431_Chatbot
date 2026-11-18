# Radar › Mechanics › Ship Signature Positioning Effect

Source: Official wiki (wiki.hoodedhorse.com), game 0.6.2.6:260903-1430

## Body
Ship Radar Cross Section (RCS, [math]\displaystyle{ \sigma }[/math]), also called "radar signature," is the primary way that the target impacts radar detection. RCS depends on angle and has a unique shape for each ship, based roughly on how a radar wave would reflect off of the target and back to the radar.

As a general rule of thumb, the RCS of a ship is based on the physical cross section of the ship relative to the radar and how "flat" the ship is at that aspect. There's also an increased signature for the engine nozzles. The effect is that RCS is generally greatest directly up, to the sides, or from behind; and RCS is generally lowest at a 45 degree angle off of the front.

We are working on porting interactable graphics for each ship to this wiki. Until then, these can be viewed on the old wiki on the appropriate ship page. For example, the RCS by angle for a Vauxhalllooks like:

From the above detection range equations, assuming that all other parameters in the equation are constant (the values that are crossed out and converted to the constant value C) and only the (RCS, [math]\displaystyle{ \sigma }[/math]) is changing, it can be shown that the change in detection distance is linearly changed by RCS value by the 4th root without jamming, and and the 2nd root with jamming.

A quick reference table is provided for the jammed and unjammed case. Remember that RCS should be divided by 10 for the formulas provided above.

The following images generate relative ratios RCS ratios when compared to the maximum signature facing (Top Red box) of each ship. The Maximum ship signature value as reported on the ship hull pages can then be used to determine the effect of the ship signature due to facing.

For a quick reference, the relative RCS ratio can be compared to the Radar Detection image to generate the Detection Distance Multiplier for the unjammed and Jammed Case and multiplier by the maximum detection range for each type of sensing radar shown the ship hull pages.

For example a Vauxhall at a 45° angle (between the bow and top surface) to the sensing ship will have the RCS of the ship reduce to a signature factor of 0.32. when compared with its top surface. The resulting unjammed Distance Multiplier when compared to the Radar Detection Range image above is around 0.71 for the unjammed case and the 0.5 for the jammed case. When compared to the Ithaca Bridgemaster Detection Range of 8.5km on the Vauxhall Ship page Radar Signature section.

The resulting distance for detection of an Ithaca Bridgemaster on the target that would normally detect the top surface of the Vauxhall at 8.5km, when at a 45 degree angle between the bow and the top would become 6.3km for the unjammed case and 4.25km for the jammed case.

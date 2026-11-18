# Electronic Warfare › Communication Jamming

Source: Official wiki (wiki.hoodedhorse.com), game 0.6.2.6:260903-1430

## Body
Comms jamming visualized. Not to scale. Diagram by jraamus

Communication jamming in the game works by saturating the victim's receiving antenna, effectively denying them from receiving data from their allies.

Note that:

- Comms jamming does NOT stop a ship from transmitting its own information.

- Both comms jamming and transmission fall off as the inverse square of distance.

- While communication antennae are not occluded by terrain, comms jammers ARE occluded by terrain and can be blocked by rocks

In most cases, a comms reciever (such as a ship, a CMD missile, or a mine) is successfully comms jammed and isolated from the comms network if the jamming strength is greater than the transmission strength of the strongest ally transmission (out of all allies who are not also jammed). With one ship doing the comms jamming, we can find the distance required to successfully jam.

Given:

- The distance from transmitting ally to the target, [math]\displaystyle{ d_A }[/math]

- The transmitting ally's antenna strength, [math]\displaystyle{ P_A }[/math]

- The ally's antenna gain [math]\displaystyle{ G_A }[/math]

- The target's antenna gain [math]\displaystyle{ G_T }[/math]

- And with [math]\displaystyle{ K = PG }[/math] for the comms jammer (or the sum for multiple jammers; no stacking penalty),

Then the maximum distance, [math]\displaystyle{ d_c }[/math], at which the target is comms jammed is given by [math]\displaystyle{ d_c = d_A \sqrt{\frac{G_TK}{G_AG_TP_A - (4\times 10^{-7})\pi d_A^2}} \approx d_A\sqrt{\frac{K}{P_AG_A}} }[/math]

Only the simpler approximation is needed for normal situations. For example, if the target's allies are using CR10 antennas ([math]\displaystyle{ P_AG_A = 2500 }[/math]), then one Hangup jammer ([math]\displaystyle{ K = 7500 }[/math]) can jam at a distance [math]\displaystyle{ \sqrt{3} = 1.73 }[/math] times further than the transmitting ally. If the allies are using a CR75 ([math]\displaystyle{ P_AG_A = 30000 }[/math]), then one hangup has to be at half the distance as the CR75. Receiver gain is not factored in as receiver gain amplifies both incoming transmissions and incoming jamming, which effectively cancels it out except in the rare case where ambient noise is a significant factor (as gain does not amplify ambient noise)

In addition, ships within the same comms jamming cone (or sphere) will not be able to directly transmit to eachother, but the jammed ships can transmit out, and if an external ship can communicate in, the two ships will still be connected indirectly via the external relay ship.

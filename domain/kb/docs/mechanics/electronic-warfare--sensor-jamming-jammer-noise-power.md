# Electronic Warfare › Sensor Jamming › Jammer Noise Power

Source: Official wiki (wiki.hoodedhorse.com), game 0.6.2.6:260903-1430

## Body
Given the jammer's radiated power, [math]\displaystyle{ P_j }[/math], and gain, [math]\displaystyle{ G_j }[/math], the jamming power on a target at distance [math]\displaystyle{ d }[/math] is given by

[math]\displaystyle{ j = \frac{{P_j}{G_j}}{4\pi d^2} }[/math]

If a track is within multiple jammed volumes due to multiple jammers, the sensor will have to overcome the combined power of the jammers. The combined power is not a simple total, each additional jammer after the strongest will only add a fraction of its power to the final combined power. The power multiplier for a given jammer is calculated by [math]\displaystyle{ e^{-(n/2.75)^2} }[/math], where [math]\displaystyle{ n }[/math] is the number of jammers imparting greater jamming power than this jammer. As a result, total combined jamming power will never exceed ~2.938× of the strongest jammer.[4]

Then the total jamming power seen by the target for a single jammer is:

[math]\displaystyle{ N_j = \frac{P_jG_jG_t}{4\pi d^2} }[/math]

where [math]\displaystyle{ G_t }[/math] is the target radar's gain. For [math]\displaystyle{ N }[/math] jammers with power, gain, and range [math]\displaystyle{ P_{j,n}, G_{j,n}, d_n }[/math] respectively and ordered in descending order, the jamming power seen by the target is:

[math]\displaystyle{ N_j = \sum_{n=1}^N \frac{P_{j,n}G_{j,n}G_t}{4\pi d_n^2}e^{-((n-1)/2.75)^2} }[/math]

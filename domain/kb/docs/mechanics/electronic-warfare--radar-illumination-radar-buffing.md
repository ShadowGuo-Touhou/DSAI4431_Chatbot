# Electronic Warfare › Radar Illumination › Radar Buffing

Source: Official wiki (wiki.hoodedhorse.com), game 0.6.2.6:260903-1430

## Body
The most common use of illuminators is to counter jamming by increasing the return power from a target ship. The illuminator effectively adds another copy of the radar calculations to the return power. Compute the radar-only return power as in the Radar page as [math]\displaystyle{ P_{r, \textrm{mono}} }[/math][6]. And find the following parameters:

- illuminator radiated power, [math]\displaystyle{ P_i }[/math]

- illuminator gain, [math]\displaystyle{ G_i }[/math]

- edge falloff stat [math]\displaystyle{ F }[/math]

- edge falloff angle [math]\displaystyle{ \theta }[/math]

- radar gain [math]\displaystyle{ G_r }[/math]

- aperture size, [math]\displaystyle{ A }[/math]

- distance from the illuminator to the target [math]\displaystyle{ d_i }[/math]

- distance from the radar to the target [math]\displaystyle{ d_r }[/math]

- target RCS [math]\displaystyle{ \sigma }[/math][7]

Then the return power is:

[math]\displaystyle{ P_{r, \textrm{total}} = P_{r, \textrm{mono}} + \frac{P_i\, G_i\, (1 - (F \cdot \theta)^2)\, G_r \, \sigma A}{16\pi^2 d_i^2 \, d_r^2} }[/math]

If there are multiple illuminators striking the same target, simply add up each of the return power terms. There is no diminishing returns, unlike radar jamming. See the main radar page for a longer discussion on how this impacts performance into jamming. In short: the Spotlight and Lighthouse have little effect on radar performance. The Floodlight acts roughly as a second copy of the radar. Thus [math]\displaystyle{ N }[/math] Floodlights improves detection range by roughly a factor of [math]\displaystyle{ \sqrt{N+1} }[/math].

In the rare event that you want to illuminate a Conure, be aware that the Conure has a reduced RCS for illumination. See below.

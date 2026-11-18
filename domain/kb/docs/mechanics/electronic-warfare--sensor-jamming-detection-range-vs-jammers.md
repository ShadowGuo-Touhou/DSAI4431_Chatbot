# Electronic Warfare › Sensor Jamming › Detection range vs jammers

Source: Official wiki (wiki.hoodedhorse.com), game 0.6.2.6:260903-1430

## Body
The distance that a target can be spotted by a radar when covered by jamming is complicated and depends greatly on the geometry. Here we present the formulas for a jammer against a radar under two scenarios:

- The jamming source is near or on the target. This is called "stand-in jamming." This commonly occurs with a tight formation of ships with jammers, or self-screening jammers on missiles.

- The jamming source is behind the target at a fixed range [math]\displaystyle{ d_j }[/math]. This is called "stand-off jamming." This commonly occurs with direct fire missile fleets that use ship jammers to cover missiles rather than self-screening jammers.

We also assume that there is only one jammer, and this jammer is significantly more powerful than the ambient noise. Refer to the Radar page for an explanation of the key equations.

In the case of multiple jammers at the same range, calculate the power density at the target [math]\displaystyle{ j }[/math] as given above for each jammer, and order the jammers from 1 to N decreasing in [math]\displaystyle{ j }[/math]. We then compute the effective total radiated power as:

[math]\displaystyle{ (P_j G_j)_{\textrm{eff}} = \sum_{n=1}^N P_{j,n} G_{j,n} \, e^{-((n-1)/2.75)^2} }[/math]

Substitute this in place of the product [math]\displaystyle{ P_j G_j }[/math] to go from the one-jammer case to the multiple-jammer case.

If multiple jammers are at different ranges, there is no simple substitution. This situation is rare, and typically only occurs when a ship launches direct fire missiles, the missiles have self-screening jammers, and the ship is providing offset jamming, e.g. CCKs. If needed this can be approximated by splitting the jammers into groups at the same range, computing the detection range for each, and taking the minimum. The minimum approach will overestimate the detection range by at most 40% and will never underestimate detection range.

Consider a search radar with:

- radiated power, [math]\displaystyle{ P_\text{t} }[/math]

- gain, [math]\displaystyle{ G_t }[/math]

- aperture size, [math]\displaystyle{ A }[/math]

- and noise filtering, [math]\displaystyle{ \nu }[/math]

Assume the target hidden by jamming has Radar Cross Section (RCS) [math]\displaystyle{ \sigma }[/math]. Recall that you should divide the RCS number provided in-game by 10 to get the RCS for these equations. Assume the hidden target is at distance [math]\displaystyle{ d }[/math], and the jammers are at distance [math]\displaystyle{ d_j }[/math]. Note that stand-in jamming is equivalent to setting [math]\displaystyle{ d_j = d }[/math]. So for stand-in jamming:

[math]\displaystyle{ d < \left(\frac{P_t\,G_t \,\sigma A}{4\pi \,P_j \, G_j} \right)^{1/2} \cdot 10^{-\nu/20} }[/math]

And for stand-off jamming:

[math]\displaystyle{ d < \left(\frac{P_t\,G_t \,\sigma A \,d_j^2}{4\pi \,P_j \, G_j} \right)^{1/4} \cdot 10^{-\nu/40} }[/math]

Fire control radars function nearly identical to search radars, with the additional stat [math]\displaystyle{ \textrm{SNR}_\textrm{min} }[/math].

For stand-in jamming:

[math]\displaystyle{ d < \left(\frac{P_t\,G_t \,\sigma A}{4\pi \,P_j \, G_j} \right)^{1/2} \cdot 10^{(- \textrm{SNR}_\textrm{min} -\nu)/20} }[/math]

And for stand-off jamming:

[math]\displaystyle{ d < \left(\frac{P_t\,G_t \,\sigma A \,d_j^2}{4\pi \,P_j \, G_j} \right)^{1/4} \cdot 10^{(-\textrm{SNR}_\textrm{min}-\nu)/40} }[/math]

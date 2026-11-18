# Radar › Notes

Source: Official wiki (wiki.hoodedhorse.com), game 0.6.2.6:260903-1430

## Body
- ↑ In battle, RCS interpolates between the hull box's minimum and maximum face areas depending on aspect. Wiki ship detection tables list a single number and are computed at maximum aspect unless stated otherwise; other aspects can reduce signal-limited detection range.

- ↑ There is actually an error in this equation compared to real life: in real life, gain should not be squared. Since Neb also uses gain in linear units rather than in dB (despite listing them in dB), this leads to the effect of gain being much different than might be expected from real life.

- ↑ Both the logarithm and the +30 are simply a unit change to get [math]\displaystyle{ P_r }[/math] from Watts to dB(milliwats) or dBm, which are the units for [math]\displaystyle{ S }[/math]. That is, this equation really just asks that the return power is greater than sensitivity after correcting for units.

- ↑ The Bloodhound LRT radar has exactly -40 dBm and thus cannot have detection buffed (except against jamming). All other vanilla radars can be buffed once by an Adaptive Radar Receiver before passing -40 dBm, so 2 or more ARRs is redundant (except against jamming).

- ↑ Notice that the exponent is now 1/2 instead of 1/4. This means that a jammed radar experiences significantly different scaling laws compared to an unjammed radar. See the EWAR page for more details.

- ↑ Another common abbreivation is simply calling it "Burnthrough", but that can be confused for the actual term used in real life to describe the range at which a given radar can see through jamming.

- ↑ This cannot reduce the sig radius below the default, but in practice this limit is irrelevant since default sig radius is very small, and ships with signature reductions are not likely to be detected at max range anyway, making sig radius irrelevant.

- ↑ This inexplicably uses the natural logarithm and therefore does not actually give SNR in dB. However, to maintain consistency with previous wiki pages, we'll still describe it as dB

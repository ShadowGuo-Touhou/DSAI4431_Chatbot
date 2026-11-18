# Radar › Mechanics › Detection Range

Source: Official wiki (wiki.hoodedhorse.com), game 0.6.2.6:260903-1430

## Body
We can solve for [math]\displaystyle{ d }[/math] in the above equations to give a formula for detection range for search radars.

If there is no jamming and the radar sensitivity is greater than -40 dB, we have:

[math]\displaystyle{ d < \left(\frac{P_t \, G_t^2 \, \sigma A}{16 \pi^2 \cdot 10^{-3 + S/10} }\right)^{1/4} \approx 1.586 \cdot (P_t \,G_t^2 \,\sigma A \cdot 10^{S/10})^{1/4} }[/math]

If there is no jamming and the radar sensitivity is less than -40 dB, we have:

[math]\displaystyle{ d < \left(\frac{P_t \, G_t^2 \, \sigma A}{16 \pi^2 \cdot 10^{-7} }\right)^{1/4} \approx 15.863 \cdot (P_t \,G_t^2 \,\sigma A)^{1/4} }[/math]

The formula for jamming is complicated and cannot be easily solved for detection range in every case. See the Electronic Warfare page for a more detailed breakdown. The most common scenario is for a set of jammers at the same range as the target that are significantly stronger than the ambient noise, which can be solved for range as follows:

Assume that we have [math]\displaystyle{ N }[/math] identical jammers all at range [math]\displaystyle{ d }[/math] each with radiated power [math]\displaystyle{ P_j }[/math] and gain [math]\displaystyle{ G_j }[/math]. The diminishing returns of multiple jammers give an effective multiplier of [math]\displaystyle{ M = \sum_{n=1}^{N} e^{-((n-1)/2.75)^2} }[/math]. The detection range is then[5]:

[math]\displaystyle{ d < \left(\frac{P_t\,G_t \,\sigma A}{4\pi \,P_j \, G_j \,M} \right)^{1/2} \cdot 10^{-\nu/20} }[/math]

If desired, we can make a catch-all equation by computing all 3 detection ranges and taking the minimum. This exercise is left to the reader.

For fire control radars with weak or no jamming, lock range is given by:

[math]\displaystyle{ d < \left(\frac{P_t \, G_t^2 \, \sigma A}{16 \pi^2 \cdot 10^{\textrm{SNR}_\textrm{min}/10} } \cdot 10^{\nu/10}\right)^{1/4} \approx 0.282 \cdot (P_t \,G_t^2 \,\sigma A)^{1/4} \cdot 10^{(- \textrm{SNR}_\textrm{min} -\nu )/40} }[/math]

Except for the Parallax, unjammed fire control radars have this distance above the hard maximum range of the radar, so they are generally not limited by this calculation. For a fire control radar being jammed by it's target (with the same setup as the search radar case above), we get the lock range:

[math]\displaystyle{ d < \left(\frac{P_t\,G_t \,\sigma A}{4\pi \,P_j \, G_j \,M} \right)^{1/2} \cdot 10^{(- \textrm{SNR}_\textrm{min} -\nu )/20} }[/math]

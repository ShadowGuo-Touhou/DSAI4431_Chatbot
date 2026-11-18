# Radar › Radar Jamming and Counter Jamming

Source: Official wiki (wiki.hoodedhorse.com), game 0.6.2.6:260903-1430

## Body
For more information on this section, please refer to EWAR.

The most common counter to radar jamming is illuminators. See the EWAR page for details on how return power is calculated. We use the same jamming setup as seen above in this page with [math]\displaystyle{ N }[/math] jammers all at the same range as the target. We then also assume that there are [math]\displaystyle{ N' }[/math] illuminators near the ship trying to get a track, with stats as follows:

- Illuminator radiated power [math]\displaystyle{ P_{i,n} }[/math]

- Illuminator gain [math]\displaystyle{ G_{i,n} }[/math]

We also assume that there is no edge falloff (which is automatically the case if you're track firing the illuminators). Recall that illuminators simply add return power without any diminishing returns. So the maximum detection range for a jamming target being illuminated paired with a search radar is:

[math]\displaystyle{ d < \left(\frac{\left(P_t\,G_t + \sum_{n=1}^{N'} P_{i,n}\,G_{i,n}\right)\sigma A}{4\pi\, P_j \,G_j \,M}\right)^{1/2}\cdot 10^{-\nu/20} }[/math]

And with a fire control radar:

[math]\displaystyle{ d < \left(\frac{\left(P_t\,G_t + \sum_{n=1}^{N'} P_{i,n}\,G_{i,n}\right)\sigma A}{4\pi\, P_j \,G_j \,M}\right)^{1/2}\cdot 10^{(-\textrm{SNR}_\textrm{max}-\nu)/20} }[/math]

The most common use-case is attempting to illuminate into jamming to maintain a lock with a fire control radar. We can simplify this by comparing [math]\displaystyle{ P_t\,G_t }[/math] to [math]\displaystyle{ P_i\,G_i }[/math]. Let's look at the relationships for the 3 common pairings:

- The Floodlight and Bullseye are have approximately similar stats, so [math]\displaystyle{ N' }[/math] Floodlights improves lock range by a factor of [math]\displaystyle{ \sqrt{N'+1} }[/math]

- The Spotlight has roughly half the stats of the Bullseye, so they improve lock range by a factor of [math]\displaystyle{ \sqrt{N'/2 + 1} }[/math]

- The Lighthouse has exactly half the stats of the Pinpoint, so they improve lock range by a factor of [math]\displaystyle{ \sqrt{N'/2 + 1} }[/math].

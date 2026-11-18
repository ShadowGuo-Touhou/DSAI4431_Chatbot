# Radar › Mechanics › Return Power Density

Source: Official wiki (wiki.hoodedhorse.com), game 0.6.2.6:260903-1430

## Body
Given the radar cross section (RCS) of an enemy ship[1] [math]\displaystyle{ \sigma }[/math] at a distance [math]\displaystyle{ d }[/math], The returned power density, [math]\displaystyle{ P_r }[/math] is calculated by[2]:

[math]\displaystyle{ P_r = \frac{P_t\,G_t^2 \,\sigma A}{16\pi^2\, d^4} }[/math]

On a burn-through sweep, [math]\displaystyle{ P_t }[/math] is multiplied by the Burn-Through Power Mult. stat.

Return Power must be sufficiently high for the target to be detected, with the threshold depending on radar type (search radar or fire control radar), radar sensitivity, and presence of jamming. Sensors sweep for new contacts about once per second, and locks are acquired on that cycle. Integrated PD fire-control panels that are still seeking a lock re-check every physics frame. Unlocked tracks update on a 0.25 s cycle (spread across fixed frames); locked tracks update every physics frame.

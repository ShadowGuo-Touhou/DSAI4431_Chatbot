# Radar › Mechanics

Source: Official wiki (wiki.hoodedhorse.com), game 0.6.2.6:260903-1430

## Body
The units are omitted here; use the values as you see them in-game, except divide the radar cross-section by [math]\displaystyle{ 10 }[/math]. All units listed in dB should be taken at face value as linear units, as the code makes the necessary conversions; e.g. a sensitivity of -40 dBm should be plugged into the equations as just -40.

Radars have a few stats that affect their ability to see objects:

- radiated power, [math]\displaystyle{ P_t }[/math] - gain, [math]\displaystyle{ G_t }[/math] - aperture size, [math]\displaystyle{ A }[/math] - sensitivity, [math]\displaystyle{ S }[/math] - noise filtering, [math]\displaystyle{ \nu }[/math] - and for fire control radars, minimum signal-to-noise, [math]\displaystyle{ \text{SNR}_\text{min} }[/math]. The Bullseye and Pinpoint do not show this row; both use a hidden −10 dB. Only the Parallax shows Min. Lock SNR (3).

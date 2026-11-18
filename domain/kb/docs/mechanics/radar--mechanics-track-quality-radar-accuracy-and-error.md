# Radar › Mechanics › Track Quality › Radar Accuracy and Error

Source: Official wiki (wiki.hoodedhorse.com), game 0.6.2.6:260903-1430

## Body
Each radar lists a position and velocity error stat, [math]\displaystyle{ 10\delta_r }[/math] and [math]\displaystyle{ 10\delta_v }[/math]. That is, divide the values you see in-game by 10 to use the formulas below, then take your final answer and multiply by 10 again to get back to meters.

Velocity inaccuracy scales with the target speed for search and multi-function radars. For speed [math]\displaystyle{ |\text{v}| }[/math], the error magnitude is [math]\displaystyle{ 2\,\delta_v\,|\text{v}| }[/math], applied in a random direction. For example, a radar listed with 5 m/s velocity error has [math]\displaystyle{ \delta_v = 0.5 }[/math], so a track moving at 15 m/s may show any speed from 0 to 30 m/s (±15 m/s). Turreted fire-control radars use a range-scaled deviation curve instead.

Each radar has its own deviation curve which gives a deviation [math]\displaystyle{ \delta_d }[/math]. For search radars, this scales with SNR. For fire control radars, this scales with target range.

For search radars, the deviation curve has entries from 0 dB to 30 dB. SNR is calculated as [math]\displaystyle{ \textrm{SNR} = \ln\left(\frac{P_r}{N_a + N_j}\right) }[/math] and clamped between 0 to 30[8]. Notice that noise filtering does not apply. At 0 dB, [math]\displaystyle{ \delta_d }[/math] is always exactly [math]\displaystyle{ \delta_r }[/math]. At 30.0 dB, error hits a floor between roughly [math]\displaystyle{ 0 }[/math] to [math]\displaystyle{ 0.3\delta_r }[/math] depending on the radar. See the component pages for each radar to see their curves (not implemented yet).

For fire control radars, the deviation is based on the ratio of the target distance to the radar's max distance. See component pages for the curve.

Then the true position error is a random point in the sphere of radius [math]\displaystyle{ 10\cdot\delta_d \delta_r }[/math]. Notice this means at 0 dB, this radius is [math]\displaystyle{ 10\cdot\delta_r^2 }[/math] and can be higher than the listed position accuracy for a listed position accuracy greater than 10 m. For a multifunction radar attempting to lock, this is also multiplied by the Lock Multiplier stat. Since this is a random point in a sphere, the expected lateral error is [math]\displaystyle{ \frac{3\pi}{16}\approx0.59 }[/math] times the sphere radius. Turreted fire-control radars instead pick a point uniformly in a cube whose side is the deviation-curve value times the raw position error (listed metres ÷ 10), so ± half that side on each axis, and the error is linear in listed error rather than quadratic.

For example, the Frontline radar shows 30 m inaccuracy for the position error. The maximum true error at 0 dB SNR would be 10(3*3) = 90 m. Until roughly 4.0 dB SNR, inaccuracy rapidly drops down to 30%, where a Frontline radar would have 90*0.3 = 27 m max error. This then slowly approaches 10% inaccuracy at 30.0 dB.

When multiple radars on the network see the same track, the game chooses the best (lowest) error for the track. This has the effect of improving your track quality, but note that multiple radars of the same type on one ship collapse to a single guess (for balance). Different types on the same ship are all evaluated, and the ship's track keeps the guess closest in 3D to the true position. For radars of the same type on multiple ships, the following table gives the combined average error in the plane facing your guns as a fraction of the maximum error [math]\displaystyle{ \delta_d\delta_r }[/math]:

| # of Radars | Average Error |
|---|---|
| 1 | 0.59 |
| 2 | 0.505 |
| 3 | 0.454 |
| 4 | 0.419 |
| n | [math]\displaystyle{ \frac{\pi}{4}\Gamma\left(\frac{4}{3}\right)\frac{n!}{\Gamma\left(n+\frac{4}{3}\right)} }[/math] |

# Radar › Mechanics › Noise

Source: Official wiki (wiki.hoodedhorse.com), game 0.6.2.6:260903-1430

## Body
Against small ships, unjammed range is usually limited by return power (sensitivity, or the 1e-7 W floor) rather than the listed maximum. Against cruisers and larger, most search radars reach that maximum (plus signature radius). Once jamming is present, detection range is limited by the Signal to Noise Ratio (SNR). Noise is modeled in-game as the sum of ambient noise and jamming noise.

Ambient noise is fixed at [math]\displaystyle{ N_a = 1 \times 10^{-7} }[/math] for all radars. If jamming is present, the jamming noise will add to the ambient noise. See the EWAR page for the calculation of jamming noise power [math]\displaystyle{ N_j }[/math]. The jamming noise power is the sum of the power from each individual jammer, weighted by diminishing returns. Then the total noise power is:

[math]\displaystyle{ N = (N_a + N_j)*10^{\nu / 10} = (10^{-7} + N_j)*10^{\nu / 10} }[/math]

Search radars have three checks:

First, return power [math]\displaystyle{ P_r }[/math] is compared against ambient background noise [math]\displaystyle{ N_a }[/math]. If the Return Power is less than the background noise [math]\displaystyle{ P_r < N_a }[/math], the target is not seen. Note that this check is unaffected by noise filtering, which means noise filtering cannot bring the overall noise below ambient background noise.

Second, return power is compared against the total noise power. If the SNR is below 1, that is, [math]\displaystyle{ P_r < N }[/math], the target is not seen. Note that, unlike the first check, this check is affected by noise filtering.

Third, the return power is used to compute the Signal Loss [math]\displaystyle{ S_L }[/math], then compared against the radar Sensitivity [math]\displaystyle{ S }[/math]:

[math]\displaystyle{ S_L = 10\log_{10}\left(\frac{P_r}{0.001}\right) = 10\log_{10}({P_r}) + 30 }[/math]

If [math]\displaystyle{ S_L < S }[/math], then the target is not seen[3]. This check is not affected by noise filtering, but is affected by sensitivity buffs.

If any of the three checks fail, the target is not seen. If all three checks succeed, then the target is seen.

The first and third checks are nearly redundant. If the radar sensitivity is greater than -40 dBm, then the third check will be more restrictive than the first check. If the radar sensitivity is less than -40 dBm, then the first check will be more restrictive. This means that search radars have no benefit to sensitivity less than -40 dBm[4]. In summary:

- When there is no jamming and radar sensitivity is greater than -40 dBm, the third check is the only one used: The target is spotted if [math]\displaystyle{ 10\log_{10}({P_r}) + 30 > S }[/math]

- When there is no jamming and radar sensitivity is less than -40 dBm, the first check is the only one used: The target is spotted if [math]\displaystyle{ P_r > 10^{-7} }[/math]

- When there is jamming, the second check is almost always used: The target is spotted if [math]\displaystyle{ P_r > N }[/math]. In the rare case that jamming power is very weak, this can theoretically fall back on the first or second check.

Turreted fire control radars (Bullseye, Pinpoint) have one power check: they lock if the SNR is greater than the minimum SNR required to lock (listed below), after a range, FOV and line-of-sight test. While unjammed, a held lock is not re-checked. The Parallax must also pass all three search-radar checks before that SNR test.

[math]\displaystyle{ 10\log_{10}\left(\frac{P_r}{N}\right) > \text{SNR}_\text{min} }[/math]

Fire control radars are not restricted by the background noise floor, so noise filtering will reduce background noise for locking and will increase their effective range.

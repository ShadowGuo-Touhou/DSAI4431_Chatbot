# Radar › Mechanics › Signature radius & bloom

Source: Official wiki (wiki.hoodedhorse.com), game 0.6.2.6:260903-1430

## Body
[wip]

Some signatures (such as ships), have a "sig radius" (calculated from half the max component of the signature's boxcollider) that can allow radars to detect the signature beyond the radar's nominal max range. Under normal conditions, this sig radius is a small value, ranging from 39.5m (sprinter) to 138m (solomon). This means that by default, every radar actually has slightly more range than their listed max range. Both search radars and fire control radars can take advantage of this (but radar guided missiles will not)

Any modifier that increases signature size will "bloom" radar sig, multiplying the sig radius by the same amount. For example, a +1500% sig increase (for a total of 1600% signature) will increase the sig radius from 135m to 2160m, so search radars can potentially detect it ~2km farther than their max range.

Components that modify the ship's signature will also factor into this, such as masquerades, EWAR emitters, raider engines, etc, but the radius difference is usually too minor to notice except for very large sig increases from components like firing railguns or mass drivers.

Sig Radius is also affected by signature reductions (eg, prowler, radars off), which can be used to counteract sig bloom from other sources.[7]

Note that sig radius only increases maximum range; radars still have to pass the noise and signal loss checks against the target's return power to detect a target, so radars may not always be able to make full use of the signature bloom if it can't detect the signature at max range.

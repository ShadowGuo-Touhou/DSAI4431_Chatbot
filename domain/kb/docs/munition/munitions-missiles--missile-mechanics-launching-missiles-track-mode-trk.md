# Munitions & Missiles › Missile Mechanics › Launching Missiles › Track mode (TRK)

Source: Official wiki (wiki.hoodedhorse.com), game 0.6.2.6:260903-1430

## Body
Firing missiles in track mode is accomplished by right clicking an enemy track and selecting the weapon from the list. This will create a red firing vector and the volley confirmation window. When moused over a track you will see the number of missiles to be fired, the volley count, the distance to target, and the estimated intercept time. ALT will add missiles to the volley one at a time while SHIFT+ALT will add one volley worth of missiles (based on the firing ships missile programming channel count). Right click will remove missiles one at a time and escape cancels the firing selector entirely. Note that while Track mode automatically assigns one missile to the original track, subsequent missiles can be assigned to other tracks. Track mode is useful for quickly getting missiles launched but care should be used both to confirm the correct target and to ensure that the target will not move beyond the seeker cones range by the time the missiles near the target.

Missiles fired in track mode will try to plot an intercept using the reported position and velocity from the sensor network. An automatically fired defensive missile using Direct guidance flies straight at the target instead, and only when the target's velocity is within about 32 degrees of pointing at the launching ship (dot product at least 0.85). Player-ordered track shots, and cruise-guided shots, always lead.

Cruise missiles fired in track mode can also make use of TRP waypoints while in the mode. TRP waypoints are selected with CTRL while in track fire mode and can be used to route cruise missiles around obstacles or to put them on advantageous strike angles.

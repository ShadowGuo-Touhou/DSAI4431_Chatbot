# Munitions & Missiles › Missile Construction › Avionics Package

Source: Official wiki (wiki.hoodedhorse.com), game 0.6.2.6:260903-1430

## Body
The avionics package determines how the missile is controlled. It has the following configuration options:

- Weapon Role sets how the missile may be launched:

  - DEFENSIVE: Missiles can be launched manually and by the point defense system.

  - OFFENSIVE: Missiles can be launched manually.

- Launch Type sets the behavior immediately after launching:

  - HOT: The missile's engine will ignite immediately, good for getting the missile moving quickly when fired in range of enemy point defenses.

  - COLD: The missile will maneuver around the launching ship with thrusters until it has an unobstructed line to the target or first waypoint before igniting the main engines.

- Target Lost Behavior sets what the missile will do if it loses the target:

  - RESUME SEARCH: The missile will search for a new target.

  - SELF DESTRUCT: The missile will self destruct.

- Terminal Maneuvers sets what evasive maneuvers the missile will perform on its terminal approach to the target:

  - NONE: No evasive maneuvers.

  - WEAVE: Missile will weave from side to side.

  - CORKSCREW: Missile will spiral towards the target.

- Trajectory Preference sets the approach angle the guidance system will try to maintain.

  - FREE APPRAOCH: Missile will fly directly towards the target.

  - MINIMUM ANGLE: The missile stays on the line between the launching ship and the target, which usually produces a head-on approach. Only Direct Guidance has this option, and it is on by default.

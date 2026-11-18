# Spacecraft › Spacecraft Mechanics › Controls › Right-Click Commands

Source: Official wiki (wiki.hoodedhorse.com), game 0.6.2.6:260903-1430

## Body
Craft are controlled similarly to ships, but with context-sensitive actions depending on the item the cursor is pointing at when right-clicked. Where multiple valid controls exist, additional commands may be accessed by holding Shift.

| Object clicked | Modifier | Requirements | Action | Explanation |
|---|---|---|---|---|
| Space |  | None | Move | Opens the dial widget to allow movement. Holding Shift will allow placement of waypoints as normal. May also be opened via the ship 'move to position' hotkey. |
| Friendly Ship |  | None | Guard/Orbit | Craft will move into a holding pattern moving around the target ship. If it has anti-craft/missile armaments, it will be slaved to the ship's PD controller and will attack incoming threats. |
| Friendly Ship | Shift | Landing Pad | Land | Craft will line up and attempt to land on the target ship. It will orbit the ship until a landing pad is free and the ship is within flight quarters speeds. |
| Friendly Craft |  | None | Guard/Orbit | Craft will move into a holding pattern moving around the target craft. If it has anti-craft/missile armaments, it will be slaved to the craft's PD controller and will attack incoming threats. |
| Friendly Craft | Shift | Target of same craft type | Merge flight | Craft will join with the target craft/flight to form a unified flight. |
| Enemy Ship |  | None | Attack Ship | Craft will move towards the target ship and attempt to attack it with appropriate weapons. Behaviour is dependent on the craft's set stance toggles. Craft will automatically deauthorise weapons that cannot harm ships when given an attack ship order. |
| Enemy Ship | Shift | Craft has standoff illuminator/Jammer/EO module | Designate target for Illumination/Jamming/Scanning | Craft will move into range of the target with its module and enter a holding pattern, attempting to keep the target jammed/illuminated/scanned. |
| Enemy Craft |  | None | Attack Craft | Craft will move toward the target craft/flight and attempt to attack it with appropriate weapons. Behaviour is dependent on the craft's set stance toggles. Craft will automatically deauthorise weapons that cannot harm craft when given an attack craft order. |

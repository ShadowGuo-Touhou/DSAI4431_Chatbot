# Spacecraft › Spacecraft Mechanics › Craft Stats › How facing changes the return

Source: Official wiki (wiki.hoodedhorse.com), game 0.6.2.6:260903-1430

## Body
- Ships use a fixed table of 162 directions. Their displayed signature is the maximum, and most angles are lower.

- Craft and missiles use a radar box fixed to the airframe. Their radar cross-section (RCS) is the area of that box as the radar sees it: each face counts by how squarely it faces the radar.[4]

- The return is smallest nose-on or tail-on.

- It is largest when the radar sees the side, top and nose at once, for example with the craft banked 45°. That happens about 57–63° off the nose for craft, and 65–75° for missiles.

- In level flight the largest return is only 1.24–1.35× the side-on value for craft, and 1.07–1.20× for missiles.

- The displayed craft signature is the side-on value.

  - For craft, the banked peak is 1.6–1.7× the displayed value, and nose-on is 0.73–0.91×.

  - For missiles, the banked peak is about 1.5× the side-on value, and nose-on is 0.38–0.66×.

- Pitch, yaw and roll all change the return, because the box turns with the airframe.

- The same value is used by search radars on ships and craft, by track accuracy, and by missile seekers. A ship holding a fire-control lock reuses the last value computed for that target.

- Detection range grows with the fourth root of the RCS: doubling the RCS gives about 19% more range.

  - A craft seen nose-on is detected at 0.82–0.86× the range of its peak angle.

  - A missile seen nose-on is detected at 0.71–0.81× that range.

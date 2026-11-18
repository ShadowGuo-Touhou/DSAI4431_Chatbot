# Electronic Warfare › Radar Illumination › Edge falloff

Source: Official wiki (wiki.hoodedhorse.com), game 0.6.2.6:260903-1430

## Body
All ship illuminators have "edge falloff"; this means that signatures near the edge of their cone will be illuminated less than signatures in the center of the cone. The falloff is calculated by [math]\displaystyle{ 1 - (F\cdot\theta)^2 }[/math] where [math]\displaystyle{ F }[/math] is the edge falloff stat of the illuminator, and [math]\displaystyle{ \theta }[/math] is how close the signature is to the edge of the cone (e.g. at the very edge of the cone [math]\displaystyle{ \theta }[/math] will be 1.0; at the center of the cone [math]\displaystyle{ \theta }[/math] will be 0).

Edge falloff for the Lighthouse and Spotlight is 0.75, and will be reduced to ∼44% power at the edge of their FoV. Edge falloff for the Floodlight is 0.4, and will be reduced to 84% instead. All craft illuminator pods are hardcoded to have 0 edge falloff.[5]

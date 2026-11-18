# Crew › Mechanics › Crew Status

Source: Official wiki (wiki.hoodedhorse.com), game 0.6.2.6:260903-1430

## Body
During battle, fighting can start to wear down the nerves of the crew. Your crew is under a certain amount of pressure, rated from 0 to 3000, based on the events going on around them and the amount of damage being sustained. The amount of pressure determines what state the crew is in, which affects the voice lines you receive when commanding the ship. Currently, crew status does not impact the performance of any components. The status levels are:

| Pressure | Status |
|---|---|
| <150 | Calm |
| <1000 | Heightened |
| <2500 | Rattled |
| ≥2500 | Panicked |

The following events change the pressure of your crew:

| Event | Pressure Change |
|---|---|
| Shots on armor that do not penetrate | +5 |
| Penetrating shots | +0.5 × total damage |
| Component destroyed | +200 |
| (applied per second) | -8 |

Although pressure drops by 8 per second, it cannot fall below another variable called static pressure (SP). SP represents tension that prevents the crew from totally being at ease due to the danger of the situation. Every time a crew member is killed, a part changes its destroyed status (destroyed or repaired), or a part changes its functioning status, the SP is recalculated by this formula:

[math]\displaystyle{ \text{SP} = (1000 \times \text{fraction of components not functional}) + (25 \times \text{number of active debuffs}) - (500 \times \text{fraction of crew still alive}) }[/math]

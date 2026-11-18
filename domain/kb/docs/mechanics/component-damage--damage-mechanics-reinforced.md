# Component Damage › Damage Mechanics › Reinforced

Source: Official wiki (wiki.hoodedhorse.com), game 0.6.2.6:260903-1430

## Body
A reinforced component can only be killed once it's at 0 HP. Any hit when the component is above 0 HP will only bring it down to 0 HP This means that a reinforced component with a DC team repairing it must be hit twice within the 0.25 second window between repair ticks or else the DC team will bring the component above 0 HP (Note that DC teams inside nearly destroyed modules are very vulnerable to damage and can be killed quickly)

The two hits do not have to be the same; any hit that brings the component down to 0 HP will count for the first hit, regardless of how little damage it deals or if it beats the component's DT. However, the second "greying" hit will have to beat DT as usual

Note that the reinforced tag is only "stripped" in the next frame, two hits in the same frame will both be resisted by reinforced, but if the second hit is delayed a moment afterwards, it will break through as expected.

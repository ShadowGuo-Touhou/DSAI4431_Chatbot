# Damage Control › Damage Control teams › Damage Control priorities

Source: Official wiki (wiki.hoodedhorse.com), game 0.6.2.6:260903-1430

## Body
Every ship has a damage control dispatcher that assigns DC teams to repair jobs and manages repair priorities.

DC dispatcher example list

Given a ship that has: - damaged drive (Critical prio) with atmo leak, fire, overload - damaged cic (high prio) - damaged magazine (med prio) with ammo cookoff - damaged DC locker (low prio)

the lists will look something like this:

Primary: - Drive Overload - Drive Atmo leak - Magazine Ammo cookoff - CIC hp

Secondary: -Drive HP -Magazine HP -DC locker HP

The dispatcher has a primary and secondary repair job list. These lists are filled with repair jobs, which include both damaged components and debuffs (aka critical events) that need repair. Each component adds its repair jobs in order of a sort key: DC priority (Low/Medium/High/Critical), plus one Critical step if it has a catastrophic event and a small step if it is on fire. Manually prioritized components always come first.

Within each component, up to two debuffs events are added to the list. Catastrophics are prioritized first and always added to the primary list. Then, regular debuffs are added (up to the two debuff cap), starting from the top of the component's debuffs list as seen in the DC board. The first regular debuff that still fits under the two-debuff cap goes to the primary list if the component is alive or manually prioritized, and to the secondary list otherwise. Any further regular debuff that still fits goes to the secondary list; regulars past the cap are not listed. On a destroyed, unprioritized component, every regular debuff that fits goes to secondary. Then, the component adds its HP repair to the secondary list. If the component has no debuffs and has medium or higher DC priority, it instead adds its HP repair to the primary list

Using these lists, the DC team then assigns teams to the repair jobs in the list, satisfying all jobs in the primary list before filling secondary jobs

Damage control teams from DC lockers higher in the component list are tasked to jobs first. eg, DC teams from compartment 1's locker will be assigned to tasks before DC teams from compartment 2's locker, regardless of difference in team move speed, repair speed, or distance to damaged component. The only exception to this rule is if there is already a DC team in that component; it will be tasked to work on repairs immediately. However, this will not be performed for repair jobs in the secondary list, those jobs will summon another DC team even if there is an idle DC team in the same component.

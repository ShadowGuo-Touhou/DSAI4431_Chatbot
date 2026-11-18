# Damage Control › Debuffs/Catastrophic Events › Debuffs list

Source: Official wiki (wiki.hoodedhorse.com), game 0.6.2.6:260903-1430

## Body
| In game name | Internal name | Stat Affected | Modifier | RepairWork |
|---|---|---|---|---|
| Atmosphere Leak | Atmosphere Leak | component-workspeed | -50% | 10 |
| Fire | Fire | component-workspeed | -20% | 10 |
| Fuel Line Fire | Fuel Line Fire | component-workspeed | -20% | 40 |
| Magazine Cookoff | Magazine Cookoff | component-workspeed | -20% | 30 |
| Reactor Overload | Reactor Overload | powerplant-prodefficiency | +25% | 65 |
| Main Bus Short | Main Bus Short | powerplant-prodefficiency | -50% | 30 |
| Cell Cookoff | Cell Launcher Cookoff | component-workspeed | -20% | 30 |
| Container Bank Cookoff | Container Bank Cookoff | component-workspeed | -20% | 60 |
| Ammunition Loader Jammed | Ammunition Loader Jammed | discreteweapon-reload, discreteweapon-recycle | +75%, +75% | 15 |
| FC Waveguide Bent | FC Waveguide Bent | sensor-power | -50% | 10 |
| Gyroscope Drift | Gyro Drift | muzzle-accuracy (spread) | +75% | 10 |
| Heatsink Ruptured | Heatsink Ruptured | continuousweapon-cooldown, continuousweapon-overheatdamageprob | +75%, +90% | 15 |
| Antenna Bent | Sensor Antenna Bent | sensor-gain | -50% | 10 |
| Antenna Bent | Sensor Oscillator Drift | sensor-maxposerror, sensor-maxvelerror | +100%, +100% | 10 |
| Bearing Surface Bent | Turret Bearing Surface Bent | turret-traverse, turret-elevate (rotation speed) | -80%, -80% | 20 |
| Focusing Element Misaligned | Focusing Element Misaligned | continuousweapon-directdamagemultiplier | -66% | 15 |

- component-workspeed affects the repair speed of the DC teams inside the component; penalty cannot reduce workspeed below 33%

- There are two types of Antenna Bent, and while they have different internal names, in-game there's no way to tell which type of debuff is in effect.

| In game name | Internal name | Affected class | Required Condition | Casualty class | On-hitOnly | Rare (catastrophic) |
|---|---|---|---|---|---|---|
| Atmosphere Leak | Atmosphere Leak | CrewedComponent | none | Decompression | TRUE | FALSE |
| Fire | Fire | HullComponent | none | Fire | FALSE | FALSE |
| Fuel Line Fire | Fuel Line Fire | DriveComponent | none | Fire | TRUE | TRUE |
| Magazine Cookoff | Magazine Cookoff | BulkMagazineComponent[1] | ContainsAnyAmmo | Fire | TRUE | TRUE |
| Reactor Overload | Reactor Overload | PowerplantComponent | none | Engineering | FALSE | TRUE |
| Main Bus Short | Main Bus Short | PowerplantComponent | none | Engineering | FALSE | FALSE |
| Cell Cookoff | Cell Launcher Cookoff | BaseCellLauncherComponent | ContainsAnyAmmo | CombatSystems | TRUE | TRUE |
| Container Bank Cookoff | Container Bank Cookoff | Container Bank[2] | ContainsAnyAmmo | CombatSystems | TRUE | TRUE |
| Ammunition Loader Jammed | Ammunition Loader Jammed | DiscreteWeaponComponent | none | CombatSystems | FALSE | FALSE |
| FC Waveguide Bent | FC Waveguide Bent | WeaponComponent | HasIntegratedFC | CombatSystems | FALSE | FALSE |
| Gyroscope Drift | Gyro Drift | WeaponComponent | none | CombatSystems | FALSE | FALSE |
| Heatsink Ruptured | Heatsink Ruptured | ContinuousWeaponComponent | HasCooldown | CombatSystems | FALSE | FALSE |
| Antenna Bent | Sensor Antenna Bent | BaseActiveSensorComponent, PassiveSensorComponent | none | CombatSystems | FALSE | FALSE |
| Antenna Bent | Sensor Oscillator Drift | BaseActiveSensorComponent, PassiveSensorComponent | none | CombatSystems | FALSE | FALSE |
| Bearing Surface Bent | Turret Bearing Surface Bent | TurretedDiscreteWeaponComponent, FixedDiscreteWeaponComponent, TurretedContinuousWeaponComponent | none | CombatSystems | FALSE | FALSE |
| Focusing Element Misaligned | Focusing Element Misaligned | Beams[3] | none | CombatSystems | TRUE | FALSE |

# Armor › Mechanics › Armor Damage › Terminology

Source: Official wiki (wiki.hoodedhorse.com), game 0.6.2.6:260903-1430

## Body
- Nominal armor (NA)

- NA is the actual thickness of the armor as listed in the hull description.

- Effective armor (EA)

- EA is based on the angle of the armor relative to the incoming projectile, increased from NA due to the projectile having to travel through more armor. This is capped at 2.5x nominal armor.

- [math]\displaystyle{ \text{EA} = \min\left(\frac{\text{NA}}{\cos\theta}\, ,\, 2.5\times\text{NA}\right) }[/math]

- where [math]\displaystyle{ \theta }[/math] is the angle from the normal to the incoming projectile.

- Some weapons ignore armor angling, so for these EA simply equals NA.

- Remaining armor (RA)

- RA is the remaining effective armor, i.e. EA times the current armor health in that location.

- [math]\displaystyle{ \text{RA} = \text{current armor health fraction}\times\text{EA} }[/math]

- Armor Penetration (AP)

- AP is the base penetration stat of the weapon.

If [math]\displaystyle{ \text{AP} \geq \text{RA} }[/math] then the attack penetrates and shreds all the armor at that location. If not, then the armor is damaged according to the process below.

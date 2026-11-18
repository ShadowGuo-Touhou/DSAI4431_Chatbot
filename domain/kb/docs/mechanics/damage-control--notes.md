# Damage Control › Notes

Source: Official wiki (wiki.hoodedhorse.com), game 0.6.2.6:260903-1430

## Body
- ↑ BulkMagazineComponents include all types of magazines, including reinforced and citadel magazines.

- ↑ Container bank cookoffs do not have an explicit affected class, but container banks have container bank cookoffs set as a unique debuff. it is unknown if container bank cookoffs can also suffer regular cell cookoffs or if it's overwritten. Magazine cookoff and cell cookoff can block eachother as they have identical keys, but container cookoff appears to have a different key. Additionally, unique debuffs are only added after the regular debuffs, which means container banks likely has a different key as otherwise the regular cell cookoff would block it.

- ↑ Similar to container bank cookoffs. Is explicitly defined in both the spinal beam and beam turret.

- ↑ n = ceil(BoundingVolumeRadius / 1 world unit). The count is an integer Random.Range(2n, 4n), so the top end is exclusive.

- ↑ These colors are for the default color settings. Colorblindness settings will change the colors.

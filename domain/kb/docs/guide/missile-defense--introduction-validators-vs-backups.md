# Missile Defense › Introduction › Validators Vs Backups

Source: Official wiki (wiki.hoodedhorse.com), game 0.6.2.6:260903-1430

## Body
In missile nomenclature you often see missile seekers with brackets ([CMD]) and without brackets. But what is the difference in behavior in the two?

Bracketed seekers are those that have been set to validate a primary seeker. Validation's main job is to discriminate between targets to avoid decoys. The validator inherits the range of the primary seeker, meaning range of the validator does not matter (As an example, an SEACT/[THERM] missile will be able to validate for the full 5km and not from the short THERM cone). Validators are great for missiles with ACT and SAH especially to discriminate between chaff and real ships. You can counter validators by decoying/jamming either the validator or the primary. For example, jamming out the EO seeker for ACT/[EO] will make the ACT chaffable, or simply jamming out ACT/[EO] will directly counter the primary since the validator relies on the primary in order to see.

Backup seekers are different and are mainly for jamming resistance. If a primary seeker does not see a target or if it is being actively jammed out, it will switch to its backup seeker to seek. This is an especially popular pick for missile setups like ARAD/SEACT, which uses the long range SEACT for staging before switching to ARAD once in range, or with CMD/BACKUP and SAH/BACKUP seeker setups to become more resistant to jamming. The only real way to defeat backup seekers is to do multiple softkill actions to cover your bases, or hoping that the primary seeker is decoyed by something.

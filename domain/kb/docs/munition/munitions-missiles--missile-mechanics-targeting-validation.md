# Munitions & Missiles › Missile Mechanics › Targeting › Validation

Source: Official wiki (wiki.hoodedhorse.com), game 0.6.2.6:260903-1430

## Body
Comparison of dual-seeker and seeker-validator behavior. Diagram by smolcake.

All seekers can be set to validation mode. When a seeker is operating in Validation mode, it does NOT provide its original function. Instead, it validates target tracks spotted by the targeting seekers, and tags them valid or invalid.

The validator checks every track spotted by the targeting seekers, ignoring the validator's default range and seeker cone. These targets are tagged valid if the validator can also see it, and tagged invalid otherwise. Validators otherwise spot targets in the same way as if it was a targeting seeker. SAH Validation is broken and behaves like ACT validation. Multiple Validators on the same missile are also broken; only one will work at a time and appear to inconsistently alternate which functions.

Validator reliability is the chance that the validator will provide accurate info. The seeker rolls its validator chance once on launch. If the check fails, the validator will always be wrong (eg, an invalid target will be tagged valid, and a valid target will be tagged invalid).

Validators can negate some secondary effects of jamming when paired with a targeting seeker set to reject unvalidated (assuming the validator itself is not jammed). The seeker will not follow the fake targets produced by jamming (unless the validator is also affected or attracted to the jamming source), and seekers will not stage early due to jamming (unless the seeker cannot detect distance, as the staging prevention comes from pushing the fake target from 1km to 50km). Both of these effects are not affected by validator reliability. Note that validators otherwise do not improve the seeker's ability to acquire targets through jamming; the targeting seeker will spot targets at the same range regardless if it has a validator or not.

Validators will apply to all targeting seekers in the missile, even if the targeting seeker is placed behind the validator.

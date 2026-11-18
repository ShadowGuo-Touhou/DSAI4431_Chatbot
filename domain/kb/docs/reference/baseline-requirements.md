# Baseline requirements (every ship, before its class rules)

Keywords: baseline, all ships, 基线, 通用要求, 通用基线, 每一艘船, 硬性要求, 必须满足, must, should, avoid, 合格, 不合规, 合法性
Summary: 所有舰船的通用基线（Ship Builds.txt 的 Baseline 段）：must 必须全部满足才算合法配装，should 是良好标准，avoid 是要避免的做法；先过基线，再对照 builds/<class>.md 的舰级要求。

Source: `other info/Ship Builds.txt`, section 「Baseline: For all ships」. Class-specific rules live in `builds/<class>.md`; both apply, baseline first.

## Must (missing any of these means the ship is not a legal build)

- have at least 1 drive
- have at least 1 CIC
- have at least 1 ammo storage
- Required power < 110% provided (with exceptions for some ships)
- for ships with cannons, there must be enough ammo for at least 10 minutes of firing
- for ships with hardkill PDT, there must be enough ammo for at least 1 minute of firing

## Should (a ship that misses these is a flawed build, not an illegal one)

- Have a radar
- have at least 1 reinforced ammo storage
- Have 1 arming missile (offensive S1 that cost 1 point)
- Required power =< 100% provided
- for ships with cannons, there is enough ammo for at least 20 minutes of firing
- for ships with hardkill PDT, there is enough ammo for at least 2 minutes of firing

## Avoid

- have Engineering modules
- have more than 1 internal radar (radar that are not EWR radar or LRT radar)
- have more than 2 ammo storage
- have TLS launchers

## How to use this in a review

1. Check every Must first; report each failed Must explicitly instead of giving a score.
2. `Required power < 110% provided` is the 「one switchable part over budget」 allowance: jammers and radars can be shut down, cannons and drives cannot (see `zh/供电预算与(n-1)规则.md`).
3. Ammo-duration rules (10 min cannons, 1 min hardkill PDT) cannot be computed from a `.fleet` file — say so instead of inventing a number.
4. Only after the baseline passes, check the class rules.

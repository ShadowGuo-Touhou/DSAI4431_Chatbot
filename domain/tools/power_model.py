"""电力预算：常开负载、可关负载、以及「武器式」的干扰器。

游戏里的耗电分三层：

1. **常开（hard）**：炮塔、近防、发射器、推进器——装上就一直吃电，缺电就是事故。
2. **常开但可关（switchable）**：雷达、泛光灯/照明器、ELINT、天线、通讯——默认开着，
   玩家可以在战斗里手动关掉，用来腾出电力。
3. **武器式（active）**：干扰器（Jammer）、激光眩光器（Dazzler）——**默认关闭、不耗电**。
   开火时才要电：只要**总供电**够就能开；但如果「开着的负载 + 它」超过总供电，
   它会先亮一瞬间，然后按游戏的耗电顺序把别的东西关掉。开着会持续消耗、到时间后
   自动关闭并装填；开 battleshort（BSHRT）可以强制超时工作，代价是持续掉血。

所以判定顺序是：先看常开负载够不够，再看开了干扰器还有没有余量。
"""

from __future__ import annotations

import re

# 干扰器 / 取眩器：武器式，默认关闭
ACTIVE_HINTS = ("jammer", "dazzler", "commjam", "eccm jammer")

# 默认开着、但玩家可以关掉来省电
SWITCHABLE_HINTS = (
    "radar", "spyglass", "huntress", "parallax", "bullseye", "scryer", "r400", "r50",
    "rf101", "ewr", "lrt", "early warning", "tracking radar",
    "illuminator", "floodlight", "spotlight",
    "antenna", "elint", "signature scrambler", "track correlator", "strobe",
    "scanner", "comms", "communications",
)

HARD_SECTIONS = ("projectile weapons", "energy weapons", "spinal weapons",
                 "missile launchers", "point defense weapons", "propulsion")

NEGLIGIBLE_KW = 20


def kind_of(section: str, name: str, draw: float) -> str:
    low_sec = (section or "").lower()
    low_name = (name or "").lower()
    if any(h in low_name for h in ACTIVE_HINTS):
        return "active"
    if any(h in low_sec for h in HARD_SECTIONS):
        return "hard"
    if draw <= NEGLIGIBLE_KW:
        return "hard"
    if any(h in low_name for h in SWITCHABLE_HINTS):
        return "switchable"
    if any(h in low_sec for h in ("sensors", "ewar", "communications")):
        return "switchable"
    return "hard"


def analyse(parts: list[dict], *, boost_pct: float = 0.0) -> dict:
    """parts: [{'name','section','draw','supply'}] → 预算结果。

    `boost_pct` is the powerplant-efficiency bonus in percent (Plant Control Center
    +20 each, Small Reactor Booster +10 each, plus any hull modifier). The game shows
    the boosted number, so the raw generator sum is reported separately.
    """
    supply_base = sum(max(0.0, p["supply"]) for p in parts)
    # Only reactors (section "Powerplants") are PowerplantComponent in the game and
    # get the efficiency multiplier; drives list their output separately.
    reactor_kw = sum(max(0.0, p["supply"]) for p in parts
                     if "powerplant" in (p.get("section") or "").lower())
    drive_kw = supply_base - reactor_kw
    supply = reactor_kw * (1.0 + boost_pct / 100.0) + drive_kw
    buckets = {"hard": [], "switchable": [], "active": []}
    for p in parts:
        kw = max(0.0, p["draw"])
        if kw <= 0:
            continue
        buckets[kind_of(p["section"], p["name"], kw)].append({"name": p["name"], "kw": round(kw, 1)})

    hard_kw = sum(i["kw"] for i in buckets["hard"])
    switch_kw = sum(i["kw"] for i in buckets["switchable"])
    jam_kw = sum(i["kw"] for i in buckets["active"])
    standing = hard_kw + switch_kw
    free = round(supply - standing, 1)

    out = {
        "draw": round(standing + jam_kw, 1),
        "standing": round(standing, 1),
        "supply": round(supply, 1),
        "supply_base": round(supply_base, 1),
        "reactor_kw": round(reactor_kw, 1),
        "drive_kw": round(drive_kw, 1),
        "boost_pct": round(boost_pct, 1),
        "hard_draw": round(hard_kw, 1),
        "switchable_kw": round(switch_kw, 1),
        "jammer_kw": round(jam_kw, 1),
        "free": free,
        "switchable": sorted(buckets["switchable"], key=lambda s: -s["kw"]),
        "jammers": sorted(buckets["active"], key=lambda s: -s["kw"]),
        "deficit": round(max(0.0, standing - supply), 1),
    }

    if supply <= 0:
        out["verdict"] = "no_powerplant"
        out["note"] = "没有发电机"
        out["jammer_ready"] = "no_powerplant"
        return out

    if standing <= supply:
        out["verdict"] = "ok"
        out["note"] = f"常开负载 {standing:.0f} kW / 供电 {supply:.0f} kW，余量 {free:.0f} kW"
    elif hard_kw <= supply and switch_kw >= standing - supply:
        deficit = standing - supply
        picked, acc = [], 0.0
        for item in sorted(buckets["switchable"], key=lambda s: -s["kw"]):
            picked.append(item)
            acc += item["kw"]
            if acc >= deficit:
                break
        names = " + ".join(f"{p['name']}({p['kw']:.0f} kW)" for p in picked)
        out["verdict"] = "ok_shutdown"
        out["shutdown"] = picked
        out["note"] = f"常开超 {deficit:.0f} kW，关掉 {names} 就够（(n-1) 余量）"
    else:
        out["verdict"] = "overload"
        if hard_kw > supply:
            out["note"] = (f"硬耗电 {hard_kw:.0f} kW 已超过供电 {supply:.0f} kW："
                           "缺电的是炮塔/近防这类关不掉的东西，属于设计事故")
        else:
            out["note"] = (f"常开负载缺 {standing - supply:.0f} kW，可关部件只有 {switch_kw:.0f} kW，"
                           "关一个也不够")

    # 干扰器能不能开：需要「总供电 - 常开负载」≥ 干扰器功率
    biggest = max((j["kw"] for j in buckets["active"]), default=0.0)
    out["biggest_jammer"] = biggest
    if biggest <= 0:
        out["jammer_ready"] = "none"
    elif free >= biggest:
        out["jammer_ready"] = "ready"
        out["jammer_note"] = f"余量 {free:.0f} kW ≥ 最大干扰器 {biggest:.0f} kW，全开状态下也能开干扰"
    elif free + switch_kw >= biggest:
        out["jammer_ready"] = "needs_shutdown"
        out["jammer_note"] = (f"干扰器要 {biggest:.0f} kW，余量只有 {free:.0f} kW："
                              "开之前得先关一个雷达/泛光灯，否则会被耗电顺序挤掉")
    else:
        out["jammer_ready"] = "cannot"
        out["jammer_note"] = f"干扰器要 {biggest:.0f} kW，余量 {free:.0f} kW 且可关部件也补不上"
    return out

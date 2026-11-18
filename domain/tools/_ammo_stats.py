import sys, json, collections
from pathlib import Path
sys.path.insert(0, 'domain/tools')
import fleet_lib

SAVES = Path(r"E:\SteamLibrary\steamapps\common\Nebulous\Saves")
paths = sorted(SAVES.rglob("*.fleet"))
fleets = []
for p in paths:
    try:
        fleets.append(fleet_lib.parse_fleet(p))
    except Exception as e:
        pass

launch = collections.defaultdict(collections.Counter)   # launcher -> Counter(munition)
launch_qty = collections.defaultdict(collections.Counter)
mag = collections.defaultdict(collections.Counter)
mag_qty = collections.defaultdict(collections.Counter)
empty = collections.Counter(); filled = collections.Counter()
per_comp = collections.Counter()

def fam(name):
    n = name.replace("Stock/", "")
    for k in ("VLS", "TLS", "MLS", "SALS", "TALS"):
        if n.upper().startswith(k):
            return k, n
    if "Magazine" in n:
        return "MAG", n
    return None, n

for f in fleets:
    for s in f.ships:
        for sock in s.sockets:
            if not sock.component_name:
                continue
            kind, name = fam(sock.component_name)
            if not kind:
                continue
            per_comp[name] += 1
            if sock.ammo:
                filled[kind] += 1
                for a in sock.ammo:
                    launch_qty[name][a.quantity] += 1
                    launch[name][a.item] += 1
            else:
                empty[kind] += 1

out = {
  "fleets": len(fleets),
  "ships": sum(len(f.ships) for f in fleets),
  "empty": dict(empty), "filled": dict(filled),
  "components": per_comp.most_common(40),
  "loads": {k: {"munitions": dict(v.most_common(8)), "quantities": dict(q.most_common(8))} for k, v in launch.items()},
}
Path("domain/data/ammo_load_stats.json").write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8")
print("fleets", len(fleets), "ships", out["ships"])
print("filled by family:", dict(filled))
print("empty by family:", dict(empty))
for k in ("VLS", "TLS", "MLS", "SALS", "TALS", "MAG"):
    if k in launch:
        print(f"\n{k} top loads:")
        for name, c in launch[k].most_common(4):
            q = launch_qty[name].most_common(3)
            print("  %-28s %-40s qty=%s" % (name, [m for m,_ in c.most_common(2)], q))

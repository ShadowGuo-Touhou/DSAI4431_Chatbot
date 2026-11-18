"""Rebuild the true socket order of every hull from the prefab hierarchy.

`Hull.AllSockets` returns `_socketLookup.Values`, a `Dictionary<string, HullSocket>`
keyed by `HullSocket.Key`.  Enumeration of a .NET `Dictionary` walks its entries
array, i.e. **insertion order**, and insertion happens in
`GetAllSocketsInternal()` = `_socketRoot.GetComponentsInChildren<HullSocket>(true)`
order — which is Unity's depth-first hierarchy order.

Object order inside the bundle file is NOT that order (all 52 sample ships came out
shuffled), so this script walks the Transform tree child-by-child (m_Children order)
and records sockets in visit order, then rewrites the `i` field of
`domain/data/hull_sockets.json`.

Run with the Python that has UnityPy:
    C:\\Users\\xxxbc\\AppData\\Local\\Programs\\Python\\Python312\\python.exe
"""

from __future__ import annotations

import json
from pathlib import Path

import UnityPy

ROOT = Path(__file__).resolve().parent.parent.parent
BASE = Path(r"E:\SteamLibrary\steamapps\common\Nebulous\Assets\AssetBundles")
SOCKETS = ROOT / "domain" / "data" / "hull_sockets.json"
BUNDLES = ("stock-f1", "stock-f2", "stock")


def script_name(mono):
    try:
        return getattr(mono.m_Script.read(), "m_ClassName", None)
    except Exception:  # noqa: BLE001
        return None


def main() -> int:
    table = json.loads(SOCKETS.read_text(encoding="utf-8"))
    # key -> hull
    key_hull = {}
    for hull, rec in table.items():
        for entry in rec["sockets"]:
            key_hull[entry["key"]] = hull

    ordered: dict[str, list[str]] = {}
    go_to_key: dict[int, str] = {}

    for bundle in BUNDLES:
        path = BASE / bundle
        if not path.exists():
            continue
        env = UnityPy.load(str(path))

        transforms = {}
        for obj in env.objects:
            if obj.type.name != "Transform":
                continue
            try:
                tr = obj.read()
            except Exception:  # noqa: BLE001
                continue
            father = None
            try:
                if tr.m_Father:
                    father = tr.m_Father.path_id
            except Exception:  # noqa: BLE001
                father = None
            children = []
            try:
                children = [c.path_id for c in tr.m_Children]
            except Exception:  # noqa: BLE001
                children = []
            transforms[obj.path_id] = {
                "go": getattr(tr.m_GameObject, "path_id", 0),
                "father": father,
                "children": children,
            }

        # sockets of this bundle: gameObject pid -> key
        for obj in env.objects:
            if obj.type.name != "MonoBehaviour":
                continue
            mono = obj.read()
            if script_name(mono) != "HullSocket":
                continue
            try:
                tree = obj.read_typetree()
            except Exception:  # noqa: BLE001
                continue
            key = tree.get("_key")
            if not key or key not in key_hull:
                continue
            go_pid = getattr(mono.m_GameObject, "path_id", None)
            if go_pid:
                go_to_key[go_pid] = key

        # go pid -> transform pid
        go_xf = {info["go"]: pid for pid, info in transforms.items()}

        # for every socket, walk to the root; group by root
        roots: dict[int, dict] = {}
        for go_pid, key in list(go_to_key.items()):
            xf = go_xf.get(go_pid)
            if xf is None:
                continue
            chain = []
            cur = xf
            seen = set()
            while cur is not None and cur not in seen:
                seen.add(cur)
                chain.append(cur)
                cur = transforms.get(cur, {}).get("father")
            root = chain[-1]
            roots.setdefault(root, {"keys": []})
            roots[root]["keys"].append((xf, key))

        for root, info in roots.items():
            hull = key_hull[info["keys"][0][1]]
            seq: list[str] = []

            def dfs(pid: int) -> None:
                node = transforms.get(pid)
                if node is None:
                    return
                key = go_to_key.get(node["go"])
                if key and key not in seq:
                    seq.append(key)
                for child in node["children"]:
                    dfs(child)

            dfs(root)
            if not seq:
                continue
            if hull in ordered and len(seq) <= len(ordered[hull]):
                continue
            ordered[hull] = seq

    # rewrite the index
    changed = 0
    for hull, rec in table.items():
        seq = ordered.get(hull)
        if not seq:
            continue
        pos = {key: n for n, key in enumerate(seq, 1)}
        for entry in rec["sockets"]:
            if entry["key"] in pos:
                entry["i"] = pos[entry["key"]]
                changed += 1
        rec["order_source"] = "prefab hierarchy (GetComponentsInChildren)"

    SOCKETS.write_text(json.dumps(table, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"hulls ordered: {len(ordered)} / {len(table)}, sockets indexed: {changed}")
    for hull in sorted(ordered)[:6]:
        print(f"  {hull:26s} {len(ordered[hull])}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

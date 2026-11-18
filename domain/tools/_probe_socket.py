import os

import UnityPy

BASE = r"E:\SteamLibrary\steamapps\common\Nebulous\Assets\AssetBundles"


def script_name(mono):
    try:
        return getattr(mono.m_Script.read(), "m_ClassName", None)
    except Exception:  # noqa: BLE001
        return None


def gameobject_name(mono):
    try:
        go = mono.m_GameObject.read()
        parent = go.m_Father.read() if go.m_Father else None
        chain = [go.m_Name]
        while parent is not None:
            chain.append(parent.m_Name)
            parent = parent.m_Father.read() if parent.m_Father else None
        return " / ".join(reversed(chain))
    except Exception as exc:  # noqa: BLE001
        return f"<err {type(exc).__name__}>"


env = UnityPy.load(os.path.join(BASE, "stock-f1"))
count = 0
for obj in env.objects:
    if obj.type.name != "MonoBehaviour":
        continue
    mono = obj.read()
    if script_name(mono) != "HullSocket":
        continue
    count += 1
    if count > 3:
        break
    print("== path_id", obj.path_id, "|", gameobject_name(mono))
    try:
        tree = obj.read_typetree()
        info = {k: tree.get(k) for k in ("_key", "_size", "_type", "_shortName", "_attachPoint", "_interiorOverhangSpace")}
        print("   typetree:", info)
    except Exception as exc:  # noqa: BLE001
        print("   typetree FAILED:", type(exc).__name__, str(exc)[:80])
        raw = obj.get_raw_data()
        print("   raw len", len(raw), raw[:140])

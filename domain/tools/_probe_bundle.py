import collections
import os

import UnityPy

BASE = r"E:\SteamLibrary\steamapps\common\Nebulous\Assets\AssetBundles"
BUNDLES = ["stock", "stock-f1", "stock-f2"]


def script_name(mono):
    try:
        script = mono.m_Script.read()
        return getattr(script, "m_ClassName", None) or getattr(script, "m_Name", "?")
    except Exception as exc:  # noqa: BLE001
        return f"<err {type(exc).__name__}>"


for bundle in BUNDLES:
    env = UnityPy.load(os.path.join(BASE, bundle))
    names = collections.Counter()
    for obj in env.objects:
        if obj.type.name != "MonoBehaviour":
            continue
        try:
            mono = obj.read()
        except Exception:
            continue
        names[script_name(mono)] += 1
    hits = {k: v for k, v in names.items() if "Hull" in str(k) or "Socket" in str(k)}
    print(bundle, "objects", len(env.objects), "mono types", len(names), "hits", hits)

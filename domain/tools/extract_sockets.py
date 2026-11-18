"""Extract hull socket geometry (size / type / 3D placement / limits) from bundles.

Each hull is a prefab: a root GameObject plus child GameObjects carrying a
`HullSocket` MonoBehaviour.  A Mono build ships no typetree for MonoBehaviours, so
the fields are parsed by hand in the declaration order of the decompiled class:

    string _key; Vector3Int _size; Sides _interiorOverhangSpace;
    Vector3 _attachPoint; HullSocketType _type; string _shortName;
    string _defaultComponent; PPtr _component; PPtr _cap; PPtr _collider;
    bool _hasTraverseLimits; TraversalLimits _traverseLimits;      // both structs
    bool _hasForwardLimits;  TraversalLimits _forwardLimits;       // are always written
    UnmaskVector _unmaskAxis; UnmaskSide _unmaskSide;
    Vector2 _socketUVMin; Vector2 _socketUVMax; float _socketUVRot;
    bool _useDefinedCraftReleasePoint; Vector3 _craftReleasePoint;
    Vector3 _craftApproachDir;

Socket *size* is a Vector3Int in grid cells of 0.25 m (`HullSocket.UnitSize`), and
the socket's position on the hull comes from its Transform, so the socket's
hull-local position is accumulated up the transform chain.
"""

from __future__ import annotations

import json
import struct
import sys
from pathlib import Path

import UnityPy

BUNDLES = [
    r"E:\SteamLibrary\steamapps\common\Nebulous\Assets\AssetBundles\stock-f1",
    r"E:\SteamLibrary\steamapps\common\Nebulous\Assets\AssetBundles\stock-f2",
    r"E:\SteamLibrary\steamapps\common\Nebulous\Assets\AssetBundles\stock",
]
OUT = Path(Path(__file__).resolve().parents[2] / "domain" / "data" / "hull_sockets.json")

SOCKET_TYPES = {0: "Surface", 1: "Compartment", 2: "Module"}
UNMASK_VECTOR = {0: "None", 1: "Right", 2: "Up"}
UNIT = 0.25


class Reader:
    def __init__(self, data: bytes, pos: int = 0) -> None:
        self.data = data
        self.pos = pos

    def align(self, n: int = 4) -> None:
        self.pos = (self.pos + n - 1) // n * n

    def i32(self) -> int:
        return struct.unpack_from("<i", self.data, self._take(4))[0]

    def i64(self) -> int:
        return struct.unpack_from("<q", self.data, self._take(8))[0]

    def f32(self) -> float:
        return round(struct.unpack_from("<f", self.data, self._take(4))[0], 4)

    def u8(self) -> int:
        v = self.data[self.pos]
        self.pos += 1
        return v

    def _take(self, n: int) -> int:
        pos = self.pos
        self.pos += n
        return pos

    def bool_(self) -> bool:
        v = self.u8() != 0
        self.align()
        return v

    def string(self) -> str:
        self.align()
        n = self.i32()
        if n < 0 or n > 4096:
            raise ValueError(f"bad string length {n} at {self.pos}")
        if n == 0:
            return ""
        raw = self.data[self.pos:self.pos + n]
        self.pos += n
        self.align()
        return raw.decode("utf-8", "replace")

    def v3(self) -> list[float]:
        return [self.f32(), self.f32(), self.f32()]

    def v2(self) -> list[float]:
        return [self.f32(), self.f32()]

    def v3i(self) -> list[int]:
        return [self.i32(), self.i32(), self.i32()]

    def pptr(self) -> None:
        self.i32()
        self.i64()

    def traversal(self) -> dict:
        limit_only = self.bool_()
        left = self.f32()
        right = self.f32()
        use_elev = self.bool_()
        elev = self.f32()
        return {"limit_firing_only": limit_only, "left": left, "right": right,
                "use_elevation": use_elev, "elevation": elev}


def parse_socket(data: bytes) -> dict:
    r = Reader(data)
    r.i32()
    go_pid = r.i64()
    r.u8()
    r.align()
    r.i32()
    r.i64()
    r.string()  # m_Name
    key = r.string()
    size = r.v3i()
    overhang = r.i32()
    attach = r.v3()
    stype = r.i32()
    short = r.string()
    default_component = r.string()
    r.pptr()
    r.pptr()
    r.pptr()
    has_trav = r.bool_()
    trav = r.traversal()
    has_fwd = r.bool_()
    fwd = r.traversal()
    unmask_axis = r.i32()
    unmask_side = r.i32()
    uvmin = r.v2()
    uvmax = r.v2()
    uvrot = r.f32()
    r.bool_()
    r.v3()  # _craftReleasePoint
    r.v3()  # _craftApproachDir
    return {
        "go_pid": go_pid,
        "key": key,
        "short": short,
        "type": SOCKET_TYPES.get(stype, stype),
        "size": size,
        "size_m": [round(v * UNIT, 3) for v in size],
        "attach": attach,
        "overhang": overhang,
        "default_component": default_component,
        "traverse": trav if has_trav else None,
        "forward": fwd if has_fwd else None,
        "unmask_axis": UNMASK_VECTOR.get(unmask_axis, unmask_axis),
        "unmask_side": unmask_side,
        "uv": {"min": uvmin, "max": uvmax, "rot": uvrot},
        "consumed": r.pos,
        "bytes": len(data),
    }


def quat_mul(a: list[float], b: list[float]) -> list[float]:
    ax, ay, az, aw = a
    bx, by, bz, bw = b
    return [
        aw * bx + ax * bw + ay * bz - az * by,
        aw * by - ax * bz + ay * bw + az * bx,
        aw * bz + ax * by - ay * bx + az * bw,
        aw * bw - ax * bx - ay * by - az * bz,
    ]


def quat_rotate(q: list[float], v: list[float]) -> list[float]:
    x, y, z, w = q
    vx, vy, vz = v
    tx = 2 * (y * vz - z * vy)
    ty = 2 * (z * vx - x * vz)
    tz = 2 * (x * vy - y * vx)
    return [
        vx + w * tx + (y * tz - z * ty),
        vy + w * ty + (z * tx - x * tz),
        vz + w * tz + (x * ty - y * tx),
    ]


def load_bundle(path: str, hulls: dict[str, dict], hull_aliases: dict[str, str]) -> None:
    env = UnityPy.load(path)
    scripts = {}
    for obj in env.objects:
        if obj.type.name == "MonoScript":
            try:
                scripts[obj.path_id] = obj.read().m_Name
            except Exception:  # noqa: BLE001
                pass
    socket_pid = next((p for p, n in scripts.items() if n == "HullSocket"), None)
    if socket_pid is None:
        print(f"{Path(path).name}: no HullSocket script", file=sys.stderr)
        return

    go_names: dict[int, str] = {}
    for obj in env.objects:
        if obj.type.name == "GameObject":
            try:
                go_names[obj.path_id] = obj.read().m_Name
            except Exception:  # noqa: BLE001
                pass

    tr: dict[int, dict] = {}
    go_to_tr: dict[int, int] = {}
    for obj in env.objects:
        if obj.type.name != "Transform":
            continue
        try:
            t = obj.read()
        except Exception:  # noqa: BLE001
            continue
        pid = obj.path_id
        tr[pid] = {
            "go": int(t.m_GameObject.m_PathID),
            "father": int(t.m_Father.m_PathID),
            "pos": [round(t.m_LocalPosition.x, 4), round(t.m_LocalPosition.y, 4),
                    round(t.m_LocalPosition.z, 4)],
            "rot": [round(t.m_LocalRotation.x, 5), round(t.m_LocalRotation.y, 5),
                    round(t.m_LocalRotation.z, 5), round(t.m_LocalRotation.w, 5)],
        }
        go_to_tr[int(t.m_GameObject.m_PathID)] = pid

    def hull_info(go_pid: int) -> tuple[str, list[float]]:
        """Return (hull root name, socket position relative to the hull root)."""
        pid = go_to_tr.get(go_pid)
        chain = []
        seen = set()
        while pid and pid not in seen:
            seen.add(pid)
            node = tr[pid]
            chain.append(node)
            pid = node["father"]
        if not chain:
            return "", [0.0, 0.0, 0.0]
        root = chain[-1]
        pos = [0.0, 0.0, 0.0]
        rot = [0.0, 0.0, 0.0, 1.0]
        for node in reversed(chain):
            local = node["pos"]
            rotated = quat_rotate(rot, local)
            pos = [round(pos[i] + rotated[i], 4) for i in range(3)]
            rot = quat_mul(rot, node["rot"])
        return go_names.get(root["go"], ""), pos

    sockets = []
    for obj in env.objects:
        if obj.type.name != "MonoBehaviour":
            continue
        data = obj.get_raw_data()
        if int.from_bytes(data[20:28], "little", signed=True) != socket_pid:
            continue
        try:
            parsed = parse_socket(data)
        except Exception as exc:  # noqa: BLE001
            print(f"parse fail {obj.path_id}: {exc}", file=sys.stderr)
            continue
        hull, pos = hull_info(parsed["go_pid"])
        parsed["hull"] = hull
        parsed["pos"] = pos
        sockets.append(parsed)

    bad = [s for s in sockets if s["consumed"] != s["bytes"]]
    print(f"{Path(path).name}: {len(sockets)} sockets / {len({s['hull'] for s in sockets})} hulls "
          f"/ size-mismatch {len(bad)}")
    for s in sockets:
        hull = s.get("hull") or "?"
        entry = hulls.setdefault(hull, {"bundle": Path(path).name, "sockets": []})
        entry["sockets"].append(s)


def main() -> int:
    hulls: dict[str, dict] = {}
    aliases: dict[str, str] = {}
    for path in BUNDLES:
        if Path(path).exists():
            load_bundle(path, hulls, aliases)
        else:
            print("missing", path, file=sys.stderr)
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(hulls, indent=1, ensure_ascii=False), encoding="utf-8")
    print(f"-> {OUT} ({len(hulls)} hulls, {sum(len(v['sockets']) for v in hulls.values())} sockets)")
    return 0


if __name__ == "__main__":
    sys.exit(main())

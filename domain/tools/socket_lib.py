"""Hull socket geometry, extracted from the game's asset bundles.

`domain/data/hull_sockets.json` is produced by `_extract_sockets.py` (workspace
root) which walks the `HullSocket` MonoBehaviours inside
`Assets/AssetBundles/stock-f1` / `stock-f2`:

* `size`      - Vector3Int in 0.25 m grid cells (`HullSocket.UnitSize`)
* `pos`       - socket position in hull-local metres (accumulated transform chain)
* `type`      - Surface / Compartment / Module (`HullSocketType`)
* `traverse`  - firing arc limits when the socket has them
* `default`   - component the editor pre-inserts on a new ship

The wiki only says "Slots: 3 Mounts, 3 Compartments" -- it never says where a
socket is or how big it is, so this file is the only source for fit checks.
"""

from __future__ import annotations

import json
import re
from dataclasses import dataclass, field
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SOCKETS_JSON = ROOT / "domain" / "data" / "hull_sockets.json"
UNIT = 0.25  # metres per grid cell (`HullSocket.UnitSize`)

# `<HullType>Stock/Foo` -> prefab name in the bundle, where the two differ.
ALIASES = {
    "Shuttle": "Shuttle Clipper",
    "Tugboat": "Tug Clipper",
    "Bulk Hauler": "Bulk",
    "Bulk Feeder": "Bulk Clipper",
    "Container Hauler": "Container",
    "Container Hauler Refit": "Container",
    "Civilian Container Hauler": "CivBulk",
}

# Multi-part hulls are several prefabs (`Container - A - Bow`, `- B - Core`, ...)
# that share one socket set; the `A/B/C` variants carry identical socket keys, so
# merging them by key keeps one entry per socket.
_SEGMENT = re.compile(r"^(?P<base>.+?) - [A-Z] - (?P<segment>Bow|Core|Stern)$")

SOCKET_TYPE_FROM_SECTION = {
    "mounts": "Surface",
    "compartments": "Compartment",
    "modules": "Module",
}

_DIMS = re.compile(r"(\d+)\s*[xX×]\s*(\d+)\s*[xX×]\s*(\d+)")


def dims(text: str | None) -> tuple[int, int, int] | None:
    """`"3x4x3"` -> `(3, 4, 3)` (order preserved; use `sorted` for comparisons)."""
    if not text:
        return None
    hit = _DIMS.search(text)
    if hit is None:
        return None
    return (int(hit.group(1)), int(hit.group(2)), int(hit.group(3)))


def socket_type_for_section(section: str) -> str:
    head = section.split("›")[0].strip().lower()
    return SOCKET_TYPE_FROM_SECTION.get(head, "")


def fits(component: tuple[int, int, int], socket: tuple[int, int, int]) -> bool:
    """Can the component box be placed in the socket box (any axis order)?"""
    return all(c <= s for c, s in zip(sorted(component), sorted(socket)))


@dataclass(frozen=True)
class SocketInfo:
    key: str
    short: str
    type: str
    cells: tuple[int, int, int]
    pos: tuple[float, float, float]
    default: str = ""
    traverse: dict | None = None

    @property
    def size_m(self) -> tuple[float, float, float]:
        return tuple(round(c * UNIT, 2) for c in self.cells)  # type: ignore[return-value]

    def describe(self) -> str:
        return f"{self.short} ({self.type} {'x'.join(str(c) for c in self.cells)})"


@dataclass
class HullSockets:
    name: str
    bundle: str = ""
    sockets: dict[str, SocketInfo] = field(default_factory=dict)
    segments: tuple[str, ...] = ()

    @classmethod
    def from_json(cls, name: str, blob: dict) -> "HullSockets":
        sockets = {
            item["key"]: SocketInfo(
                key=item["key"],
                short=item.get("short", ""),
                type=item.get("type", ""),
                cells=tuple(item.get("size", (1, 1, 1))),  # type: ignore[arg-type]
                pos=tuple(round(v, 3) for v in item.get("pos", (0.0, 0.0, 0.0))),  # type: ignore[arg-type]
                default=item.get("default_component", ""),
                traverse=item.get("traverse"),
            )
            for item in blob.get("sockets", [])
        }
        return cls(name=name, bundle=blob.get("bundle", ""), sockets=sockets)

    def merged(self, other: "HullSockets") -> "HullSockets":
        sockets = dict(self.sockets)
        for key, socket in other.sockets.items():
            sockets.setdefault(key, socket)
        segments = tuple(dict.fromkeys(self.segments + other.segments + (other.name,)))
        return HullSockets(name=self.name, bundle=self.bundle, sockets=sockets, segments=segments)

    def __len__(self) -> int:
        return len(self.sockets)

    def get(self, key: str) -> SocketInfo | None:
        return self.sockets.get(key)

    @property
    def counts(self) -> dict[str, int]:
        out: dict[str, int] = {}
        for socket in self.sockets.values():
            out[socket.type] = out.get(socket.type, 0) + 1
        return out


class SocketTables:
    """All hulls extracted from the bundles, looked up by `.fleet` hull type."""

    def __init__(self, path: Path | None = None) -> None:
        source = Path(path or SOCKETS_JSON)
        self.path = source
        self._raw: dict[str, dict] = {}
        self._hulls: dict[str, HullSockets] = {}
        self._by_name: dict[str, str] = {}
        self._groups: dict[str, HullSockets] = {}
        if source.exists():
            self._raw = json.loads(source.read_text(encoding="utf-8"))
            parts: dict[str, list[HullSockets]] = {}
            for name, blob in self._raw.items():
                hull = HullSockets.from_json(name, blob)
                self._hulls[name] = hull
                self._by_name.setdefault(name.lower(), name)
                hit = _SEGMENT.match(name)
                if hit is not None:
                    parts.setdefault(hit.group("base"), []).append(hull)
            for base, members in parts.items():
                merged = members[0]
                for other in members[1:]:
                    merged = merged.merged(other)
                merged.name = base
                self._groups[base.lower()] = merged

    def __len__(self) -> int:
        return len(self._hulls)

    @property
    def available(self) -> bool:
        return bool(self._hulls)

    def hull(self, hull_type: str) -> HullSockets | None:
        """`Stock/Ocello Cruiser` -> the extracted socket table, if known."""
        name = hull_type.split("/", 1)[-1].strip()
        for candidate in (name, name.removesuffix(" Class"), ALIASES.get(name, ""),
                          ALIASES.get(name.removesuffix(" Class"), "")):
            if not candidate:
                continue
            key = candidate.lower()
            if key in self._groups:
                return self._groups[key]
            hit = self._by_name.get(key)
            if hit is not None:
                return self._groups.get(hit.lower()) or self._hulls[hit]
        # last resort: prefer the longest prefab name that contains the hull name
        low = name.lower().removesuffix(" class")
        choices = [h for key, h in self._hulls.items() if low and low in key.lower()]
        if len(choices) == 1:
            return choices[0]
        return None

    def hull_by_keys(self, keys: set[str]) -> HullSockets | None:
        """Join by socket keys: the keys inside a `.fleet` are stable per hull."""
        if not keys:
            return None
        best: tuple[float, HullSockets] | None = None
        pool = {**{k: h for k, h in self._groups.items()},
                **{k: h for k, h in self._hulls.items()}}
        for hull in pool.values():
            overlap = len(keys & hull.sockets.keys())
            if overlap == 0:
                continue
            score = overlap / len(keys)
            if best is None or score > best[0]:
                best = (score, hull)
        if best is not None and best[0] >= 0.6:
            return best[1]
        return None


if __name__ == "__main__":  # quick sanity dump
    tables = SocketTables()
    print(f"{len(tables)} hulls from {tables.path}")
    for hull_type in ("Stock/Ocello Cruiser", "Stock/Keystone Destroyer", "Stock/Shuttle"):
        hull = tables.hull(hull_type)
        print(f"  {hull_type:28s} -> {hull.name if hull else '?'} {hull.counts if hull else ''}")

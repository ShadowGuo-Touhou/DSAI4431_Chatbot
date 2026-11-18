"""Resolve + download wheels for UnityPy (offline-friendly pip install)."""

from __future__ import annotations

import json
import re
import sys
import urllib.request
from pathlib import Path

OUT = Path(Path(__file__).resolve().parents[2] / "_wheels")
PKGS = [
    "UnityPy",
    "lz4",
    "brotli",
    "Pillow",
    "texture2ddecoder",
    "etcpak",
    "astc-encoder-py",
    "fmod_toolkit",
    "fsspec",
    "attrs",
    "tpk_ar",
]

PLAT = {"cp312-win_amd64": 0, "abi3-win_amd64": 1, "cp37-abi3-win_amd64": 2,
        "none-win_amd64": 3, "py3-none-any": 4, "none-any": 5}


def rank(filename: str) -> int:
    if "win_amd64" in filename:
        if "cp312" in filename:
            return 0
        if "abi3" in filename:
            return 1
    if "py3-none-any" in filename:
        return 4
    if "none-any" in filename:
        return 5
    return 99


def best(pkg: str) -> tuple[str, str] | None:
    with urllib.request.urlopen(f"https://pypi.org/pypi/{pkg}/json", timeout=30) as r:
        data = json.load(r)
    cands = []
    for f in data["urls"]:
        if not f["filename"].endswith((".whl",)):
            continue
        rk = rank(f["filename"])
        if rk < 99:
            cands.append((rk, f["filename"], f["url"]))
    if not cands:
        return None
    cands.sort()
    return cands[0][1], cands[0][2]


def main() -> int:
    OUT.mkdir(exist_ok=True)
    for pkg in PKGS:
        try:
            got = best(pkg)
        except Exception as exc:  # noqa: BLE001
            print(f"{pkg}: ERROR {exc}")
            continue
        if not got:
            print(f"{pkg}: NO WHEEL")
            continue
        name, url = got
        dest = OUT / name
        if dest.exists():
            print(f"{pkg}: cached {name}")
            continue
        with urllib.request.urlopen(url, timeout=120) as r, dest.open("wb") as fh:
            fh.write(r.read())
        print(f"{pkg}: {name} ({dest.stat().st_size // 1024} KB)")
    return 0


if __name__ == "__main__":
    sys.exit(main())

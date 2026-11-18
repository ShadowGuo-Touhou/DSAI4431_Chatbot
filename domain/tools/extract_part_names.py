"""从游戏资源包里导出「当前版本真实存在的部件名」。

存档里 `<ComponentName>Stock/xxx</ComponentName>` 用的是**安装时的名字**：老存档会带着
已经删掉的部件（`C54 Cannon`）或改名前的旧名（`P20 Flak PDT` 现在叫 `P20 'Bastion' PDT`）。
光看存档分不清「旧名」和「已删除」，所以这里直接翻资源包的 container 表 —— 那是当前版本
构建出来的一批 prefab，名字就是游戏内部名，比 wiki 更硬。

用法（必须用带 UnityPy 的 `.venv-tools`）::

    .venv-tools\\Scripts\\python.exe domain\\tools\\extract_part_names.py

输出 `domain/data/game_parts.json`::

    {
      "bundles": ["stock", "stock-f1", "stock-f2"],
      "weapons":    ["mk66 cannon", ...],     # 原样小写，含引号昵称
      "components": [...],
      "drives":     [...],
      "hulls":      [...],
      "munitions":  [...],
      "all":        [...]
    }
"""

from __future__ import annotations

import json
import pathlib
import sys

GAME = pathlib.Path(r"E:\SteamLibrary\steamapps\common\Nebulous\Assets\AssetBundles")
OUT = pathlib.Path(__file__).resolve().parents[1] / "data" / "game_parts.json"
BUNDLES = ("stock", "stock-f1", "stock-f2")
FOLDERS = ("weapons", "components", "drives", "hulls", "munitions", "missile components")


def main() -> int:
    try:
        import UnityPy  # noqa: WPS433 — 只有这个工具需要它
    except ModuleNotFoundError:
        print("UnityPy 缺失：请用 .venv-tools\\Scripts\\python.exe 运行本脚本", file=sys.stderr)
        return 1

    buckets: dict[str, set[str]] = {name.replace(" ", "_"): set() for name in FOLDERS}
    all_names: set[str] = set()
    seen_bundles: list[str] = []
    for bundle in BUNDLES:
        path = GAME / bundle
        if not path.exists():
            print(f"跳过不存在的资源包：{path}", file=sys.stderr)
            continue
        seen_bundles.append(bundle)
        env = UnityPy.load(str(path))
        for key in env.container:
            pure = pathlib.PurePosixPath(key)
            folder = pure.parent.name.lower()
            stem = pure.stem
            all_names.add(stem)
            if folder in buckets:
                buckets[folder].add(stem)

    payload = {
        "bundles": seen_bundles,
        "source": "UnityPy env.container keys (game asset bundles)",
        "note": "名字为 prefab 原名（小写、含昵称）；存档名到这里的匹配用词元（token）比对",
        **{name: sorted(values) for name, values in buckets.items()},
        "all": sorted(all_names),
    }
    OUT.write_text(json.dumps(payload, ensure_ascii=False, indent=0), encoding="utf-8")
    print(f"parts: {len(all_names)} -> {OUT.relative_to(OUT.parents[2])}")
    for name, values in buckets.items():
        print(f"  {name:20} {len(values)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

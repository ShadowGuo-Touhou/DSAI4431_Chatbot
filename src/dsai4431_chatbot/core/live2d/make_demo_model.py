"""给一个只含 Moc/Textures/Physics 的 Live2D 模型，生成带动作和表情引用的 demo 版 model3.json。

起因：从 VTube Studio 社区拿到的模型，动作和表情配在 .vtube.json 里，
原版 model3.json 的 FileReferences 里没有 Motions / Expressions 段，
所以 Cubism Web / pixi-live2d-display 读不到它们，下拉框一片空白。

这个脚本扫描模型目录下的 Animation/（*.motion3.json）与 Exp3/（*.exp3.json），
生成一份新 json，其余字段原样保留。原文件不动。

用法：
    python make_demo_model.py "路径/某模型.model3.json"
    # 生成 某模型.demo.model3.json，然后用 --model 指向它
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

# 动作目录候选名 -> 默认按 Idle 处理的文件名
ANIM_DIR_NAMES = ("Animation", "animation", "Motion", "motion", "Motions")
EXP_DIR_NAMES = ("Exp3", "exp3", "Expression", "expressions", "Expressions")


def find_dir(base: Path, names: tuple[str, ...]) -> Path | None:
    for n in names:
        p = base / n
        if p.is_dir():
            return p
    return None


def build(model_json: Path) -> Path:
    base = model_json.parent
    doc = json.loads(model_json.read_text(encoding="utf-8-sig"))
    refs = doc.setdefault("FileReferences", {})

    anim_dir = find_dir(base, ANIM_DIR_NAMES)
    exp_dir = find_dir(base, EXP_DIR_NAMES)

    added_motions = 0
    added_exprs = 0

    if anim_dir is not None:
        motions: dict[str, list[dict]] = {}
        for f in sorted(anim_dir.glob("*.motion3.json")):
            group = f.name[: -len(".motion3.json")]
            # IDLE 单独拎成 Idle 组，其余每个文件一组
            if group.lower().startswith("idle"):
                group = "Idle"
            motions.setdefault(group, []).append(
                {
                    "File": f"{anim_dir.name}/{f.name}",
                    "FadeInTime": 0.5,
                    "FadeOutTime": 0.5,
                }
            )
            added_motions += 1
        if motions:
            refs["Motions"] = motions

    if exp_dir is not None:
        exprs: list[dict] = []
        for f in sorted(exp_dir.glob("*.exp3.json")):
            name = f.name[: -len(".exp3.json")]
            exprs.append({"Name": name, "File": f"{exp_dir.name}/{f.name}"})
            added_exprs += 1
        if exprs:
            refs["Expressions"] = exprs

    out = model_json.with_name(model_json.stem.replace(".model3", "") + ".demo.model3.json")
    # 上面 replace 只是兜底；正常情况 model_json.stem 就是 "大肥鱼.model3"
    if out.name == model_json.name:
        out = model_json.with_name(model_json.stem + ".demo.json")

    out.write_text(json.dumps(doc, ensure_ascii=False, indent="\t"), encoding="utf-8")

    print(f"[ok] {out.name}")
    print(f"     动作组 {len(refs.get('Motions', {}))} 个（{added_motions} 个文件）")
    print(f"     表情   {added_exprs} 个")
    if not added_motions and not added_exprs:
        print("[!] 没找到 Animation/ 或 Exp3/ 目录，生成的文件和原版一样")
    return out


def main() -> int:
    if len(sys.argv) < 2:
        print(__doc__)
        return 2
    target = Path(sys.argv[1]).expanduser()
    if not target.is_file():
        print(f"[x] 找不到 {target}")
        return 1
    out = build(target)
    print()
    print("直接用：")
    print(f'    .\\.venv\\Scripts\\python.exe demo_interactive.py --model "{out}"')
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

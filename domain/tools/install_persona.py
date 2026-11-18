"""把 domain/persona 安装到项目的运行时人格目录，并（可选）切换当前人格。

用法：
    python domain/tools/install_persona.py            # 只安装，不切换
    python domain/tools/install_persona.py --activate # 安装并把 settings.ini 切到「舰队参谋」
"""

from __future__ import annotations

import argparse
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]          # domain/
REPO = ROOT.parent          # <repo>
sys.path.insert(0, str(REPO / "src"))

from dsai4431_chatbot.core.gui import chat_config, personas  # noqa: E402

PERSONA_ID = "Nebulous"


def install() -> Path:
    target = personas.personality_dir()
    target.mkdir(parents=True, exist_ok=True)
    src_dir = ROOT / "persona" / PERSONA_ID
    dst_dir = target / PERSONA_ID
    if dst_dir.exists():
        shutil.rmtree(dst_dir)
    shutil.copytree(src_dir, dst_dir)
    shutil.copy2(ROOT / "persona" / f"{PERSONA_ID}.json", target / f"{PERSONA_ID}.json")
    return dst_dir


def activate(dst_dir: Path) -> None:
    """Switch the GUI persona to the files declared in domain/persona/<id>.json."""
    import json

    spec = json.loads((ROOT / "persona" / f"{PERSONA_ID}.json").read_text(encoding="utf-8"))
    files = [str(f) for f in spec.get("files") or []]
    cfg = chat_config.load()
    cfg.persona_dir = str(dst_dir)
    cfg.persona_files = files
    chat_config.save(cfg)
    print(f"已切换：persona_dir={cfg.persona_dir}")
    print(f"         persona_files={cfg.persona_files}")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--activate", action="store_true")
    args = parser.parse_args(argv)

    dst = install()
    print(f"安装到 {dst}")

    found = [p for p in personas.list_personas()]
    print("可选人格：")
    for persona in found:
        print(f"  {persona.id:12s} {persona.label:8s} files={len(persona.files)} dir={persona.dir}")

    if args.activate:
        activate(dst)

    cfg = chat_config.load()
    prompt = cfg.system_prompt()
    print(f"\n当前 system prompt：{len(prompt)} 字（上限 {personas.PROMPT_LIMIT}）")
    print(prompt[:240].replace("\n", " ") + " …")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

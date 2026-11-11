"""人格清单：读 DSH 那份 `personas.json`，没有就退回单个默认目录。

DSH 的人格注入插件把「一套人格 = 一个目录 + 一组 .md」存在
`<DSH_HOME>/persona-inject/personas.json`（本机在 `P:\\.dsh\\persona-inject\\`）。
新建对话时要选 persona，直接读它 —— 和 DSH 用的是同一份配置，不用另建一套。

可用 `DSAI_PERSONA_JSON` 指到别的文件。
"""

from __future__ import annotations

import json
import os
import sys
from dataclasses import dataclass, field
from pathlib import Path

from dsai4431_chatbot.core.gui import chat_config

DEFAULT_JSON = r"P:\.dsh\persona-inject\personas.json"
# 系统提示词上限（和 chat_config 保持一致的做法）
PROMPT_LIMIT = 20000


@dataclass
class Persona:
    id: str
    label: str
    dir: str
    files: list[str] = field(default_factory=list)
    order: int = 0

    # --- 给 UI 用 -------------------------------------------------------
    @property
    def display(self) -> str:
        return self.label or self.id

    def path(self) -> Path:
        return Path(self.dir).expanduser()

    def as_dict(self) -> dict:
        """写进 session 头部的那个 persona 字段。"""
        return {"id": self.id, "label": self.label, "dir": self.dir, "files": list(self.files)}

    def system_prompt(self) -> str:
        return build_system_prompt(self.dir, self.files)


def _json_path() -> Path:
    override = os.environ.get("DSAI_PERSONA_JSON")
    if override:
        return Path(override).expanduser()
    return Path(DEFAULT_JSON)


def list_personas() -> list[Persona]:
    """读配置里 enabled 的人格；读不到就用「默认目录 + 当前勾选文件」造一条。"""
    path = _json_path()
    personas: list[Persona] = []
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError) as exc:
        if path.exists():           # 文件在但坏了 → 留个日志
            print(f"[persona] {path} 读不了：{exc}", file=sys.stderr)
        data = {}

    for item in (data.get("personas") or []) if isinstance(data, dict) else []:
        if not isinstance(item, dict):
            continue
        if item.get("enabled") is False:
            continue
        persona_id = str(item.get("id") or "").strip()
        directory = str(item.get("dir") or "").strip()
        if not persona_id or not directory:
            continue
        files = [str(f) for f in (item.get("files") or []) if str(f).strip()]
        personas.append(
            Persona(
                id=persona_id,
                label=str(item.get("label") or persona_id),
                dir=directory,
                files=files,
                order=int(item.get("order") or 0),
            )
        )

    if not personas:
        cfg = chat_config.load()
        personas.append(
            Persona(
                id="default",
                label="默认人格",
                dir=str(cfg.persona_path()),
                files=list(cfg.persona_files),
            )
        )

    personas.sort(key=lambda p: (p.order, p.label))
    return personas


def by_id(persona_id: str) -> Persona | None:
    for persona in list_personas():
        if persona.id == persona_id:
            return persona
    return None


def from_session(session_persona: dict, model: str = "") -> Persona | None:
    """把 session 头部里记的 persona 还原成对象（文件可能已经变了，仍按记的来）。"""
    if not isinstance(session_persona, dict) or not session_persona.get("dir"):
        return None
    return Persona(
        id=str(session_persona.get("id") or "default"),
        label=str(session_persona.get("label") or ""),
        dir=str(session_persona.get("dir") or ""),
        files=[str(f) for f in (session_persona.get("files") or [])],
    )


def build_system_prompt(directory: str, files: list[str]) -> str:
    """把勾选的 .md 拼成 system 提示词；读不到的文件直接跳过。"""
    base = Path(directory).expanduser() if directory else Path()
    chunks: list[str] = []
    for name in files:
        try:
            text = (base / name).read_text(encoding="utf-8", errors="ignore").strip()
        except OSError:
            continue
        if text:
            chunks.append(f"<!-- {name} -->\n{text}")
    prompt = "\n\n".join(chunks)
    if len(prompt) > PROMPT_LIMIT:
        prompt = prompt[:PROMPT_LIMIT] + "\n\n……（人格文件过长，已截断）"
    return prompt


# 可选的对话模型（DeepSeek 官方这两个；别的兼容网关填自己的名字也行）
MODELS = ["deepseek-chat", "deepseek-reasoner"]


def model_options(current: str = "") -> list[str]:
    options = list(MODELS)
    current = (current or "").strip()
    if current and current not in options:
        options.insert(0, current)
    return options

"""人格清单：一套人格 = 一个目录 + 里面若干个 .md。

设计抄的是 DSH 那个人格注入插件（`P:\\Deekseek_playground\\dsh-persona-inject`）：
清单是一份 `personas.json`，每条记 id / 显示名 / 目录 / 勾了哪几个 .md。
勾选的文件按顺序拼成一条 `system` 提示词发给模型 —— 这就是「人格」在本项目的落地。

存哪儿
------
默认 `<data>/personality/personas.json`，人格文件（IDENTITY.md / SOUL.md / USER.md）
也放在同一个目录里，跟代码一起入库（`.gitignore` 里有例外）。
新建的人格可以指向任意目录（用户自己选），清单里记绝对路径。

环境变量（测试用）
------------------
- `DSAI_PERSONA_DIR`：人格根目录
- `DSAI_PERSONA_JSON`：直接指到清单文件（优先级更高）
"""

from __future__ import annotations

import json
import os
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path

from dsai4431_chatbot.core.gui import settings_store

# 默认人格（仓库自带的那套）
DEFAULT_ID = "deepseek"
DEFAULT_LABEL = "大肥鱼"
DEFAULT_FILES = ["IDENTITY.md", "SOUL.md", "USER.md"]

# 系统提示词上限
PROMPT_LIMIT = 20000

# id 只允许 ASCII 字母数字下划线短横线：它会被用来命名记忆库文件
ID_RE = re.compile(r"^[A-Za-z0-9_-]{1,40}$")


# 新建人格时先塞这几个模板，用户再往里写内容
TEMPLATES = {
    "IDENTITY.md": (
        "# IDENTITY\n\n"
        "（这个人格是谁：名字、身份、会做什么、说话什么风格。\n"
        " 勾选它之后，这些文字会被拼进 system 提示词。）\n"
    ),
    "SOUL.md": (
        "# SOUL\n\n"
        "（这个人格的判断方式和底线：先做什么后做什么、什么情况下宁可停下来问。）\n"
    ),
    "USER.md": (
        "# USER\n\n"
        "（服务对象是谁、有什么长期偏好。只写长期有效的信息，别写一次性的。）\n"
    ),
}


@dataclass
class Persona:
    id: str
    label: str
    dir: str                                    # 空串 = 用 personality_dir()
    files: list[str] = field(default_factory=list)
    order: int = 0

    # --- 给 UI 用 -------------------------------------------------------
    @property
    def display(self) -> str:
        return self.label or self.id

    def path(self) -> Path:
        raw = (self.dir or "").strip()
        return Path(raw).expanduser() if raw else personality_dir()

    def as_dict(self) -> dict:
        """写进 session 头部的那个 persona 字段（目录写**绝对路径**）。

        会话里记绝对路径，以后清单被改了也不会把这通对话的人格换掉。
        """
        return {
            "id": self.id,
            "label": self.label,
            "dir": str(self.path()),
            "files": list(self.files),
        }

    def system_prompt(self) -> str:
        return build_system_prompt(str(self.path()), self.files)


# ---------------------------------------------------------------------------
# 位置
# ---------------------------------------------------------------------------
def personality_dir() -> Path:
    """人格根目录（默认 `<data>/personality`）。"""
    override = os.environ.get("DSAI_PERSONA_DIR")
    path = Path(override).expanduser() if override else settings_store.data_dir() / "personality"
    try:
        path.mkdir(parents=True, exist_ok=True)
    except OSError:
        pass
    return path


def manifest_path() -> Path:
    override = os.environ.get("DSAI_PERSONA_JSON")
    if override:
        return Path(override).expanduser()
    return personality_dir() / "personas.json"


# ---------------------------------------------------------------------------
# 读
# ---------------------------------------------------------------------------
def default_persona() -> Persona:
    """清单还没有（或坏了）时用的那一条：仓库自带的默认人格。"""
    directory = personality_dir()
    files = [name for name in DEFAULT_FILES if (directory / name).is_file()]
    return Persona(id=DEFAULT_ID, label=DEFAULT_LABEL, dir="", files=files)


def _read_manifest() -> list[Persona]:
    path = manifest_path()
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        return []
    except (OSError, ValueError) as exc:
        print(f"[persona] {path} 读不了：{exc}", file=sys.stderr, flush=True)
        return []

    items: list[Persona] = []
    for item in (data.get("personas") or []) if isinstance(data, dict) else []:
        if not isinstance(item, dict):
            continue
        if item.get("enabled") is False:
            continue
        persona_id = str(item.get("id") or "").strip()
        if not persona_id:
            continue
        files = [str(f) for f in (item.get("files") or []) if str(f).strip()]
        items.append(
            Persona(
                id=persona_id,
                label=str(item.get("label") or persona_id),
                dir=str(item.get("dir") or ""),
                files=files,
                order=int(item.get("order") or 0),
            )
        )
    return items


def list_personas() -> list[Persona]:
    """清单里所有启用的人格；空清单就退回默认人格（永远至少有一条）。"""
    items = _read_manifest()
    if not items:
        items = [default_persona()]
    items.sort(key=lambda p: (p.order, p.display))
    return items


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
        id=str(session_persona.get("id") or DEFAULT_ID),
        label=str(session_persona.get("label") or ""),
        dir=str(session_persona.get("dir") or ""),
        files=[str(f) for f in (session_persona.get("files") or [])],
    )


# ---------------------------------------------------------------------------
# 写
# ---------------------------------------------------------------------------
def save_personas(items: list[Persona]) -> Path:
    """整份写回清单（保持 DSH 插件的字段名，方便以后互通）。"""
    path = manifest_path()
    payload = {
        "version": 1,
        "personas": [
            {
                "id": p.id,
                "label": p.label,
                "dir": (p.dir or "").strip(),
                "files": list(p.files),
                "enabled": True,
                "order": int(p.order),
            }
            for p in items
        ],
    }
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    tmp.replace(path)          # 先写临时文件再换名：写到一半崩了不会毁掉清单
    return path


def upsert(persona: Persona) -> Path:
    """按 id 覆盖或追加一条，其余原样保留。"""
    items = _read_manifest()
    if not items:
        items = [default_persona()]
    for index, existing in enumerate(items):
        if existing.id == persona.id:
            items[index] = persona
            break
    else:
        persona.order = persona.order or (10 * (len(items) + 1))
        items.append(persona)
    return save_personas(items)


def remove(persona_id: str) -> None:
    items = [p for p in _read_manifest() if p.id != persona_id]
    save_personas(items)


def create_persona_dir(persona_id: str, templates: dict[str, str] | None = None) -> Path:
    """在人格根目录下建一个以 id 命名的目录，缺哪个文件补一个模板。

    已经有同名目录就复用（不覆盖用户写过的内容）。
    """
    target = personality_dir() / persona_id
    target.mkdir(parents=True, exist_ok=True)
    for name, body in (templates or TEMPLATES).items():
        path = target / name
        if path.exists():
            continue
        try:
            path.write_text(body, encoding="utf-8")
        except OSError as exc:
            print(f"[persona] 模板写不进去 {path}：{exc}", file=sys.stderr, flush=True)
    return target


# ---------------------------------------------------------------------------
# 提示词
# ---------------------------------------------------------------------------
def scan_files(directory: str | Path) -> list[tuple[str, int]]:
    """扫目录下的 .md，返回 [(文件名, 字符数)]。目录不在就返回空表。"""
    base = Path(directory).expanduser() if str(directory).strip() else personality_dir()
    try:
        paths = sorted(p for p in base.iterdir() if p.suffix.lower() == ".md")
    except OSError:
        return []
    rows: list[tuple[str, int]] = []
    for path in paths:
        try:
            chars = len(path.read_text(encoding="utf-8", errors="ignore"))
        except OSError:
            chars = 0
        rows.append((path.name, chars))
    return rows


def build_system_prompt(directory: str, files: list[str]) -> str:
    """把勾选的 .md 拼成 system 提示词；读不到的文件直接跳过。"""
    base = Path(directory).expanduser() if directory else personality_dir()
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

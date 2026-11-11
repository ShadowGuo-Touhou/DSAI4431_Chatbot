"""人格：一套人格 = 一个目录 + 里面若干个 .md。

存储结构（都在 `<data>/personality/` 下，路径全按这个根目录算，**不写死盘符**）
--------------------------------------------------------------------------
    <data>/personality/
        FatWhale/                  ← 默认人格「大肥鱼」，固定读这个目录下的 .md
            IDENTITY.md
            SOUL.md
            USER.md
        banki.json                 ← 自定义人格：一份定义一个 json（文件名就是 id）
        banki/                     ← 它的 .md（新建时自动建、塞模板）
            ...

为什么不再用一个 `personas.json` 装所有定义：那样改一条要重写整份文件，
两个人格同时保存就会互相覆盖；现在一条一个文件，互不影响。

`dir` 字段的写法
----------------
- 在人格根目录里 → 存**相对路径**（如 `"banki"`），换机器/挪仓库照样能用
- 在别处（用户自己挑的目录）→ 只能存绝对路径
读的时候：相对 → `<data>/personality/<dir>`；绝对 → 原样。

默认人格
--------
id = `FatWhale`，label = `大肥鱼`，目录固定 `<data>/personality/FatWhale`，
文件固定读该目录下所有 .md（按文件名排序）。它在 UI 上不可改、不可删。

环境变量（测试用）
------------------
- `DSAI_PERSONA_DIR`：人格根目录（默认 `<data>/personality`）
"""

from __future__ import annotations

import json
import os
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path

from dsai4431_chatbot.core.gui import settings_store

# 默认人格（固定目录、固定读取，不可改）
DEFAULT_ID = "FatWhale"
DEFAULT_LABEL = "大肥鱼"

# 系统提示词上限
PROMPT_LIMIT = 20000

# id 只允许 ASCII 字母数字下划线短横线：它会被当成文件名
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
    dir: str                                    # 相对人格根目录，或绝对路径；空 = 默认
    files: list[str] = field(default_factory=list)
    order: int = 0

    # --- 给 UI 用 -------------------------------------------------------
    @property
    def display(self) -> str:
        return self.label or self.id

    @property
    def readonly(self) -> bool:
        """默认人格不允许改（改名/换目录/取消勾选/删除都不行）。"""
        return self.id == DEFAULT_ID

    def path(self) -> Path:
        raw = (self.dir or "").strip()
        if not raw:
            return default_dir() if self.readonly else personality_dir()
        candidate = Path(raw).expanduser()
        return candidate if candidate.is_absolute() else personality_dir() / candidate

    def rel_dir(self) -> str:
        """存进 json 的写法：在人格根目录里就存相对路径。"""
        if self.readonly:
            return ""
        try:
            return self.path().resolve().relative_to(personality_dir().resolve()).as_posix()
        except (ValueError, OSError):
            return str(self.path())

    def as_dict(self) -> dict:
        """写进 session 头部的 persona 字段（目录写绝对路径，会话自带上下文）。"""
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
    """人格根目录（默认 `<data>/personality`，可被 DSAI_PERSONA_DIR 覆盖）。"""
    override = os.environ.get("DSAI_PERSONA_DIR")
    path = Path(override).expanduser() if override else settings_store.data_dir() / "personality"
    try:
        path.mkdir(parents=True, exist_ok=True)
    except OSError:
        pass
    return path


def default_dir() -> Path:
    """默认人格「大肥鱼」的固定目录。"""
    return personality_dir() / DEFAULT_ID


def definition_path(persona_id: str) -> Path:
    return personality_dir() / f"{persona_id}.json"


# ---------------------------------------------------------------------------
# 读
# ---------------------------------------------------------------------------
def default_persona() -> Persona:
    """固定读 `<人格根目录>/FatWhale/*.md`；文件没了就是空列表（不是错误）。"""
    rows = scan_files(default_dir())
    return Persona(
        id=DEFAULT_ID,
        label=DEFAULT_LABEL,
        dir="",
        files=[name for name, _chars in rows],
    )


def _persona_from_json(path: Path) -> Persona | None:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError) as exc:
        print(f"[persona] {path} 读不了：{exc}", file=sys.stderr, flush=True)
        return None
    if not isinstance(data, dict):
        return None
    persona_id = str(data.get("id") or path.stem).strip()
    if not persona_id or persona_id == DEFAULT_ID:
        return None
    files = [str(f) for f in (data.get("files") or []) if str(f).strip()]
    return Persona(
        id=persona_id,
        label=str(data.get("label") or persona_id),
        dir=str(data.get("dir") or ""),
        files=files,
        order=int(data.get("order") or 0),
    )


def list_personas() -> list[Persona]:
    """默认人格排第一，其余按 `<id>.json` 扫出来，再按显示名排序。"""
    items = [default_persona()]
    for path in sorted(personality_dir().glob("*.json")):
        persona = _persona_from_json(path)
        if persona is not None:
            items.append(persona)
    tail = sorted(items[1:], key=lambda p: (p.order, p.display))
    return items[:1] + tail


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
def save_persona(persona: Persona) -> Path:
    """一个 id 一份 json；先写 .tmp 再换名，写到一半崩了不会毁掉定义。"""
    if persona.readonly:
        raise ValueError("默认人格不可修改")
    path = definition_path(persona.id)
    payload = {
        "id": persona.id,
        "label": persona.label,
        "dir": persona.rel_dir(),
        "files": list(persona.files),
        "order": int(persona.order),
    }
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    tmp.replace(path)
    return path


def remove_persona(persona_id: str) -> bool:
    """删掉这一份定义（**不动目录和 .md**）。默认人格删不掉。"""
    if persona_id == DEFAULT_ID:
        return False
    path = definition_path(persona_id)
    try:
        path.unlink()
        return True
    except FileNotFoundError:
        return False
    except OSError as exc:
        print(f"[persona] 删不掉 {path}：{exc}", file=sys.stderr, flush=True)
        return False


def create_persona_dir(persona_id: str, templates: dict[str, str] | None = None) -> Path:
    """在人格根目录下建 `<id>/`，缺哪个模板文件补一个。

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
# 扫描 / 提示词
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

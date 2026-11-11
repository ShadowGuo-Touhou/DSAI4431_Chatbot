"""会话存储：`<repo>/data/session/`。

**结构照 DSH**（我解了一份真实 session 对着抄的，见 TODO 第 13 条）：

    data/session/<workspace-slug>/<session-id>/session.v1.jsonl
    data/session/index.json

`session.v1.jsonl` 第一行是头，其余每行一个事件：

    {"type":"session","version":1,"id":...,"createdAt":...,"cwd":...,
     "persona":{"id","label","dir","files"},"model":"deepseek-flash"}
    {"type":"user/message","seq":1,"time":...,"data":{"content":[{"type":"text","text":"..."}]}}
    {"type":"assistant/message","seq":2,"time":...,"data":{"message":{"role":"assistant",
      "content":[{"type":"reasoning","text":"..."},{"type":"text","text":"..."}]},
      "usage":{...},"stream":true}}
    {"type":"session/title","seq":3,"time":...,"data":{"title":"...","source":{"kind":"user"}}}

**有意与 DSH 不同的两点**：
1. 不压缩（DSH 是 `session.v4.jsonl.zstd`）—— 纯文本方便 grep，也省一个 zstd 依赖
2. 没有 `tool/*`、`job/*`、`approval/*` 这些事件（本项目的对话没有工具调用）

另外多写一份 `index.json`：会话列表看它就行，不用逐个打开大文件。
"""

from __future__ import annotations

import json
import re
import sys
import time
import uuid
from dataclasses import asdict, dataclass, field
from pathlib import Path

from dsai4431_chatbot.core.gui import settings_store

SCHEMA_VERSION = 1
FILE_NAME = "session.v1.jsonl"
INDEX_NAME = "index.json"
# 自动生成的标题最多这么长（跟 DSH 的 fallback 标题一个思路：取首条用户消息）
TITLE_LIMIT = 30


# ---------------------------------------------------------------------------
# 路径
# ---------------------------------------------------------------------------
def sessions_root() -> Path:
    path = settings_store.data_dir() / "session"
    path.mkdir(parents=True, exist_ok=True)
    return path


def workspace_slug() -> str:
    """当前工作目录 → DSH 那种目录名：`--P-Deekseek_playground--`。"""
    raw = str(settings_store.project_root())
    slug = re.sub(r"[^A-Za-z0-9]+", "-", raw).strip("-")
    if not slug:                     # 全中文路径：退化成固定名 + 短哈希
        slug = f"workspace-{abs(hash(raw)) % 10**8:08d}"
    return f"--{slug}--"


def workspace_dir() -> Path:
    path = sessions_root() / workspace_slug()
    path.mkdir(parents=True, exist_ok=True)
    return path


def _session_file(session_id: str) -> Path:
    return workspace_dir() / session_id / FILE_NAME


def _index_path() -> Path:
    return sessions_root() / INDEX_NAME


# ---------------------------------------------------------------------------
# 元数据
# ---------------------------------------------------------------------------
@dataclass
class SessionMeta:
    id: str
    title: str = ""
    persona: dict = field(default_factory=dict)   # {id,label,dir,files}
    model: str = ""
    created_at: int = 0            # 毫秒时间戳，和 DSH 一致
    updated_at: int = 0
    messages: int = 0              # 用户 + 助手消息条数
    prompt_tokens: int = 0
    completion_tokens: int = 0

    # --- 给 UI 用的 -----------------------------------------------------
    @property
    def display_title(self) -> str:
        return self.title.strip() or "（未命名对话）"

    @property
    def persona_label(self) -> str:
        return str(self.persona.get("label") or self.persona.get("id") or "")

    @property
    def tokens_total(self) -> int:
        return int(self.prompt_tokens) + int(self.completion_tokens)


def _now_ms() -> int:
    return int(time.time() * 1000)


# ---------------------------------------------------------------------------
# 索引
# ---------------------------------------------------------------------------
def _read_index() -> dict:
    path = _index_path()
    if not path.is_file():
        return {"version": SCHEMA_VERSION, "sessions": []}
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError) as exc:
        print(f"[session] 索引读不了，重建：{exc}", file=sys.stderr)
        return {"version": SCHEMA_VERSION, "sessions": []}
    if not isinstance(data, dict) or not isinstance(data.get("sessions"), list):
        return {"version": SCHEMA_VERSION, "sessions": []}
    return data


def _write_index(data: dict) -> None:
    path = _index_path()
    tmp = path.with_suffix(".json.tmp")
    tmp.write_text(
        json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    tmp.replace(path)              # 原子替换，写一半被掐也不会毁掉索引


def _meta_from_dict(raw: dict) -> SessionMeta:
    known = {f for f in SessionMeta.__dataclass_fields__}
    return SessionMeta(**{k: v for k, v in raw.items() if k in known})


def list_sessions() -> list[SessionMeta]:
    """按「最近更新」倒序。索引里没有但目录还在的会话会被补进来。"""
    data = _read_index()
    metas = [_meta_from_dict(item) for item in data["sessions"] if isinstance(item, dict)]

    known = {m.id for m in metas}
    for path in workspace_dir().glob("*"):
        if not path.is_dir() or path.name in known:
            continue
        if not (path / FILE_NAME).is_file():
            continue
        # 目录里有人、索引里没有：从文件头补一条
        meta = _meta_from_file(path.name)
        if meta is not None:
            metas.append(meta)

    metas.sort(key=lambda m: m.updated_at or m.created_at, reverse=True)
    return metas


def _meta_from_file(session_id: str) -> SessionMeta | None:
    """从文件头 + 事件里重建元数据（索引丢了时的兜底）。"""
    path = _session_file(session_id)
    if not path.is_file():
        return None
    header: dict = {}
    title = ""
    messages = 0
    prompt = 0
    completion = 0
    updated = 0
    try:
        with path.open("r", encoding="utf-8") as fh:
            for line in fh:
                line = line.strip()
                if not line:
                    continue
                try:
                    event = json.loads(line)
                except ValueError:
                    continue
                etype = event.get("type")
                if etype == "session" and not header:
                    header = event
                elif etype == "user/message":
                    messages += 1
                elif etype == "assistant/message":
                    messages += 1
                    usage = (event.get("data") or {}).get("usage") or {}
                    prompt += int(usage.get("prompt_tokens") or 0)
                    completion += int(usage.get("completion_tokens") or 0)
                elif etype == "session/title":
                    title = str((event.get("data") or {}).get("title") or title)
                updated = max(updated, int(event.get("time") or 0))
    except OSError:
        return None

    if not header:
        return None
    return SessionMeta(
        id=str(header.get("id") or session_id),
        title=title,
        persona=dict(header.get("persona") or {}),
        model=str(header.get("model") or ""),
        created_at=int(header.get("createdAt") or 0),
        updated_at=updated,
        messages=messages,
        prompt_tokens=prompt,
        completion_tokens=completion,
    )


def get_meta(session_id: str) -> SessionMeta | None:
    for meta in list_sessions():
        if meta.id == session_id:
            return meta
    return _meta_from_file(session_id)


def _upsert_meta(meta: SessionMeta) -> None:
    data = _read_index()
    items = [item for item in data["sessions"] if isinstance(item, dict)]
    for index, item in enumerate(items):
        if item.get("id") == meta.id:
            items[index] = asdict(meta)
            break
    else:
        items.append(asdict(meta))
    data["sessions"] = items
    data["version"] = SCHEMA_VERSION
    _write_index(data)


# ---------------------------------------------------------------------------
# 新建 / 删除 / 改名
# ---------------------------------------------------------------------------
def create_session(
    *,
    persona: dict | None = None,
    model: str = "",
    title: str = "",
) -> SessionMeta:
    """建一个会话：写目录 + 头部事件 + 索引项。"""
    session_id = f"session-{uuid.uuid4()}"
    now = _now_ms()
    meta = SessionMeta(
        id=session_id,
        title=title,
        persona=dict(persona or {}),
        model=model,
        created_at=now,
        updated_at=now,
    )

    directory = workspace_dir() / session_id
    directory.mkdir(parents=True, exist_ok=True)

    header = {
        "type": "session",
        "version": SCHEMA_VERSION,
        "id": session_id,
        "createdAt": now,
        "cwd": str(settings_store.project_root()),
        "persona": meta.persona,
        "model": model,
    }
    with _session_file(session_id).open("w", encoding="utf-8") as fh:
        fh.write(json.dumps(header, ensure_ascii=False) + "\n")

    if title:
        _append(session_id, "session/title", {"title": title, "source": {"kind": "user"}})
    _upsert_meta(meta)
    return meta


def rename_session(session_id: str, title: str) -> SessionMeta | None:
    """改名：写一条 `session/title` 事件（和 DSH 一样），再更新索引。"""
    meta = get_meta(session_id)
    if meta is None:
        return None
    title = title.strip()
    meta.title = title
    event = _append(session_id, "session/title", {"title": title, "source": {"kind": "user"}})
    meta.updated_at = event["time"]
    _upsert_meta(meta)            # 索引也要跟着改，否则列表还显示旧名字
    return meta


def delete_session(session_id: str) -> bool:
    """删掉整个会话目录并摘掉索引项。"""
    directory = workspace_dir() / session_id
    removed = False
    if directory.is_dir():
        for path in sorted(directory.rglob("*"), reverse=True):
            try:
                path.unlink() if path.is_file() else path.rmdir()
            except OSError as exc:
                print(f"[session] 删不掉 {path}：{exc}", file=sys.stderr)
        try:
            directory.rmdir()
        except OSError:
            pass
        removed = True

    data = _read_index()
    before = len(data["sessions"])
    data["sessions"] = [
        item for item in data["sessions"]
        if not (isinstance(item, dict) and item.get("id") == session_id)
    ]
    if len(data["sessions"]) != before:
        _write_index(data)
        removed = True
    return removed


def delete_sessions(session_ids: list[str]) -> int:
    return sum(1 for sid in set(session_ids) if delete_session(sid))


# ---------------------------------------------------------------------------
# 事件写入
# ---------------------------------------------------------------------------
def _next_seq(path: Path) -> int:
    """最后一条事件的 seq + 1（文件不大，扫一遍最稳；索引里的计数可能过期）。"""
    last = -1
    try:
        with path.open("r", encoding="utf-8") as fh:
            for line in fh:
                line = line.strip()
                if not line:
                    continue
                try:
                    event = json.loads(line)
                except ValueError:
                    continue
                seq = event.get("seq")
                if isinstance(seq, int):
                    last = max(last, seq)
    except OSError:
        pass
    return last + 1


def _append(session_id: str, event_type: str, data: dict) -> dict:
    path = _session_file(session_id)
    path.parent.mkdir(parents=True, exist_ok=True)
    event = {
        "type": event_type,
        "seq": _next_seq(path),
        "time": _now_ms(),
        "data": data,
    }
    with path.open("a", encoding="utf-8") as fh:
        fh.write(json.dumps(event, ensure_ascii=False) + "\n")
    return event


def append_user_message(session_id: str, text: str) -> dict:
    text = text or ""
    event = _append(
        session_id, "user/message", {"content": [{"type": "text", "text": text}]}
    )
    meta = get_meta(session_id)
    if meta is not None:
        meta.messages += 1
        meta.updated_at = event["time"]
        if not meta.title.strip():
            meta.title = _auto_title(text)
            _append(
                session_id,
                "session/title",
                {"title": meta.title, "messageSeqs": [event["seq"]], "source": {"kind": "fallback"}},
            )
        _upsert_meta(meta)
    return event


def append_assistant_message(
    session_id: str,
    text: str,
    reasoning: str = "",
    usage: dict | None = None,
) -> dict:
    content: list[dict] = []
    if reasoning:
        content.append({"type": "reasoning", "text": reasoning})
    content.append({"type": "text", "text": text or ""})

    event = _append(
        session_id,
        "assistant/message",
        {
            "message": {"role": "assistant", "content": content},
            "usage": dict(usage or {}),
            "stream": True,
        },
    )
    meta = get_meta(session_id)
    if meta is not None:
        meta.messages += 1
        meta.updated_at = event["time"]
        payload = dict(usage or {})
        meta.prompt_tokens += int(payload.get("prompt_tokens") or 0)
        meta.completion_tokens += int(payload.get("completion_tokens") or 0)
        _upsert_meta(meta)
    return event


def mark_turn_start(session_id: str, turn: int) -> dict:
    return _append(session_id, "turn/start", {"turn": int(turn)})


def mark_turn_end(session_id: str, turn: int, reason: str = "completed") -> dict:
    return _append(session_id, "turn/end", {"turn": int(turn), "reason": {"kind": reason}})


def _auto_title(text: str) -> str:
    flat = " ".join((text or "").split())
    return flat[:TITLE_LIMIT] + ("…" if len(flat) > TITLE_LIMIT else "")


# ---------------------------------------------------------------------------
# 读回来
# ---------------------------------------------------------------------------
def load_events(session_id: str) -> list[dict]:
    path = _session_file(session_id)
    if not path.is_file():
        return []
    events: list[dict] = []
    try:
        with path.open("r", encoding="utf-8") as fh:
            for line in fh:
                line = line.strip()
                if not line:
                    continue
                try:
                    events.append(json.loads(line))
                except ValueError:
                    continue
    except OSError as exc:
        print(f"[session] 读不了 {session_id}：{exc}", file=sys.stderr)
    return events


def load_messages(session_id: str) -> list[dict]:
    """把事件流折成 UI 要的气泡列表：`[{role, text, reasoning, time}]`。"""
    out: list[dict] = []
    for event in load_events(session_id):
        etype = event.get("type")
        data = event.get("data") or {}
        if etype == "user/message":
            texts = [
                block.get("text", "")
                for block in (data.get("content") or [])
                if isinstance(block, dict) and block.get("type") == "text"
            ]
            out.append(
                {"role": "user", "text": "".join(texts), "reasoning": "", "time": event.get("time", 0)}
            )
        elif etype == "assistant/message":
            content = (data.get("message") or {}).get("content") or []
            texts, reasoning = [], []
            for block in content:
                if not isinstance(block, dict):
                    continue
                if block.get("type") == "text":
                    texts.append(str(block.get("text") or ""))
                elif block.get("type") == "reasoning":
                    reasoning.append(str(block.get("text") or ""))
            out.append(
                {
                    "role": "bot",
                    "text": "".join(texts),
                    "reasoning": "".join(reasoning),
                    "time": event.get("time", 0),
                }
            )
    return out


def load_header(session_id: str) -> dict:
    for event in load_events(session_id):
        if event.get("type") == "session":
            return event
    return {}

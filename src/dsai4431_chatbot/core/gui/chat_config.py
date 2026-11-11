"""对话配置：API 地址 / Key / 模型，以及人格文件（系统提示词）与 RAG 路径。

和换肤、Live2D 配置共用同一份 `settings.ini`（`settings_store`）。

⚠ API Key 是**明文**存在 ini 里的（用户 2026-11-11 确认可以）。这是本机配置文件，
不是仓库文件，但拿到 ini 就能拿到 key —— 换机器/共享目录时注意。

人格文件（IDENTITY/SOUL/USER…）勾选后，内容会拼成一条 `system` 消息发给模型，
这就是「人格」在这里的落地方式。
"""

from __future__ import annotations

import sys
from dataclasses import dataclass, field
from pathlib import Path

from dsai4431_chatbot.core.gui import settings_store

GROUP = "chat"

DEFAULT_BASE_URL = "https://api.deepseek.com"
DEFAULT_MODEL = "deepseek-chat"
# 人格目录和设置页 Personality 页用的是同一个默认（可用 DSAI_PERSONA_DIR 改写）
DEFAULT_PERSONA_DIR = r"P:\.dsh\agentsoul"
DEFAULT_PERSONA_FILES = ["IDENTITY.md", "SOUL.md", "USER.md"]
# 系统提示词上限：勾了超大的文件也不至于把上下文撑爆
SYSTEM_PROMPT_LIMIT = 20000


@dataclass
class ChatConfig:
    base_url: str = DEFAULT_BASE_URL
    api_key: str = ""
    model: str = DEFAULT_MODEL
    persona_dir: str = ""                                  # 空 = 用默认目录
    persona_files: list[str] = field(default_factory=lambda: list(DEFAULT_PERSONA_FILES))
    rag_dir: str = ""
    rag_ollama: str = ""
    rag_embedding: str = ""

    # --- 派生信息 -------------------------------------------------------
    def persona_path(self) -> Path:
        raw = self.persona_dir.strip()
        return Path(raw).expanduser() if raw else Path(DEFAULT_PERSONA_DIR)

    def endpoint(self) -> str:
        """拼出 chat/completions 的完整 URL。

        允许用户填 3 种写法，都认：
            https://api.deepseek.com
            https://api.deepseek.com/v1
            https://api.deepseek.com/v1/chat/completions
        """
        base = (self.base_url or DEFAULT_BASE_URL).strip().rstrip("/")
        if base.endswith("/chat/completions"):
            return base
        return f"{base}/chat/completions"

    def ready(self) -> tuple[bool, str]:
        """能不能发请求；不能的话返回给用户看的原因。"""
        if not self.api_key.strip():
            return False, "还没有填 API Key（设置 → API KEY）"
        if not self.base_url.strip():
            return False, "还没有填 API 地址（设置 → API KEY）"
        return True, ""

    def system_prompt(self) -> str:
        """把勾选的人格文件拼成系统提示词；没有可用的就返回空串。"""
        directory = self.persona_path()
        chunks: list[str] = []
        for name in self.persona_files:
            path = directory / name
            try:
                text = path.read_text(encoding="utf-8", errors="ignore").strip()
            except OSError:
                continue
            if text:
                chunks.append(f"<!-- {name} -->\n{text}")
        prompt = "\n\n".join(chunks)
        if len(prompt) > SYSTEM_PROMPT_LIMIT:
            prompt = prompt[:SYSTEM_PROMPT_LIMIT] + "\n\n……（人格文件过长，已截断）"
        return prompt


# ---------------------------------------------------------------------------
# 读写
# ---------------------------------------------------------------------------
def _get(settings, key: str, default: str) -> str:
    raw = settings.value(f"{GROUP}/{key}", default)
    return default if raw is None else str(raw)


def _as_list(raw) -> list[str]:
    """QSettings 存空列表时读回来可能是 None 或空串，这里统一成 list。"""
    if raw is None:
        return []
    if isinstance(raw, str):
        return [part for part in raw.split(",") if part]
    try:
        return [str(part) for part in raw if str(part)]
    except TypeError:
        return []


def load() -> ChatConfig:
    """读配置。**任何异常都退回默认值** —— 配置坏了也不能让程序起不来。"""
    try:
        s = settings_store.app_settings()
        return ChatConfig(
            base_url=_get(s, "base_url", DEFAULT_BASE_URL),
            api_key=_get(s, "api_key", ""),
            model=_get(s, "model", DEFAULT_MODEL) or DEFAULT_MODEL,
            persona_dir=_get(s, "persona_dir", ""),
            persona_files=_as_list(
                s.value(f"{GROUP}/persona_files", None)
            ) or list(DEFAULT_PERSONA_FILES),
            rag_dir=_get(s, "rag_dir", ""),
            rag_ollama=_get(s, "rag_ollama", ""),
            rag_embedding=_get(s, "rag_embedding", ""),
        )
    except Exception as exc:  # noqa: BLE001 - 配置读挂了就退回默认，不能挡启动
        print(f"[chat] 配置读取失败，用默认值：{exc}", file=sys.stderr, flush=True)
        return ChatConfig()


def save(cfg: ChatConfig) -> None:
    s = settings_store.app_settings()
    s.setValue(f"{GROUP}/base_url", cfg.base_url)
    s.setValue(f"{GROUP}/api_key", cfg.api_key)
    s.setValue(f"{GROUP}/model", cfg.model)
    s.setValue(f"{GROUP}/persona_dir", cfg.persona_dir)
    s.setValue(f"{GROUP}/persona_files", list(cfg.persona_files))
    s.setValue(f"{GROUP}/rag_dir", cfg.rag_dir)
    s.setValue(f"{GROUP}/rag_ollama", cfg.rag_ollama)
    s.setValue(f"{GROUP}/rag_embedding", cfg.rag_embedding)
    s.sync()      # 立刻落盘

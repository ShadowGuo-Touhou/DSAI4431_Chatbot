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
# 官方现在只有 deepseek-flash / deepseek-v4-pro 两个（2026-11），默认用便宜的那个。
# 旧名字（deepseek-chat 等）的归一在 personas.normalize_model 里。
DEFAULT_MODEL = "deepseek-flash"
# 人格目录的默认值现在是 `<data>/personality`（见 personas.personality_dir）。
# 这两个常量只留给"ini 里没写"的兜底，换机器不该指到绝对路径。
DEFAULT_PERSONA_DIR = ""                                    # 空 = 用 personas.personality_dir()
DEFAULT_PERSONA_FILES = ["IDENTITY.md", "SOUL.md", "USER.md"]
# 系统提示词上限：勾了超大的文件也不至于把上下文撑爆
SYSTEM_PROMPT_LIMIT = 20000

# --- RAG（本地知识库）默认值与合法范围 --------------------------------
# 这里是**唯一**的默认值来源：设置页的数字框、索引器、检索器都读它。
# 与 rag/chunker.py 的 DEFAULT_SIZE / DEFAULT_OVERLAP 保持一致
# （测试里有一条断言盯着，改一边忘了另一边会红）。
RAG_DEFAULTS = {
    "enabled": True,
    "autostart": True,       # 探测不到 Ollama 时自己把它拉起来（退出时关掉自己起的那份）
    "top_k": 4,              # 每次最多注入几块
    "timeout_ms": 3000,      # 单次检索最长等待
    "min_score": 0.35,       # 余弦下限
    "chunk_chars": 480,      # 切块目标字数
    "chunk_overlap": 64,     # 超长段滑窗重叠
    "max_file_mb": 2,        # 单文件上限
    "max_chunks": 2000,      # 块数上限（防把整个盘当知识库）
    "inject_chars": 3000,    # 注入内容总字数上限
}
# 参数 → (最小, 最大, 步长)；设置页的 spinbox 直接用它建控件
RAG_LIMITS = {
    "top_k": (1, 20, 1),
    "timeout_ms": (200, 15000, 500),
    "min_score": (0.0, 1.0, 0.05),
    "chunk_chars": (120, 2000, 20),
    "chunk_overlap": (0, 500, 8),
    "max_file_mb": (1, 64, 1),
    "max_chunks": (50, 20000, 50),
    "inject_chars": (200, 20000, 200),
}


def clamp_int(value, key: str) -> int:
    """把 ini 里的值夹到合法范围；非数字回默认。"""
    low, high, _step = RAG_LIMITS[key]
    try:
        number = int(float(str(value).strip()))
    except (TypeError, ValueError, AttributeError):
        return int(RAG_DEFAULTS[key])
    return max(low, min(high, number))


def clamp_float(value, key: str) -> float:
    low, high, _step = RAG_LIMITS[key]
    try:
        number = float(str(value).strip())
    except (TypeError, ValueError, AttributeError):
        return float(RAG_DEFAULTS[key])
    return max(low, min(high, number))


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
    # 显示思考链（两个模型都能返回 reasoning_content）；默认关
    show_reasoning: bool = False
    # --- RAG（本地知识库）---------------------------------------------
    # 地址/模型名是文本，其余都在 RAG_LIMITS 范围内，越界会被夹住
    rag_enabled: bool = True
    rag_autostart: bool = True
    rag_top_k: int = 4
    rag_timeout_ms: int = 3000
    rag_min_score: float = 0.35
    rag_chunk_chars: int = 480
    rag_chunk_overlap: int = 64
    rag_max_file_mb: int = 2
    rag_max_chunks: int = 2000
    rag_inject_chars: int = 3000

    # --- 派生信息 -------------------------------------------------------
    def persona_path(self) -> Path:
        raw = self.persona_dir.strip()
        if raw:
            return Path(raw).expanduser()
        # 局部导入：personas 只依赖 settings_store，这样不会形成循环
        from dsai4431_chatbot.core.gui import personas

        return personas.personality_dir()

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


def _get_bool(settings, key: str, default: bool) -> bool:
    """INI 里 bool 存成 true/false（也可能被手改成 1/yes），都要认。"""
    raw = settings.value(f"{GROUP}/{key}", default)
    if raw is None:
        return default
    if isinstance(raw, bool):
        return raw
    return str(raw).strip().lower() in ("1", "true", "yes", "on")


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


def _model(raw: str) -> str:
    """把 ini 里存的模型名归一：旧名字（deepseek-chat 等）换成现在的，
    空的退回默认。局部导入 personas 免得和它形成循环。"""
    from dsai4431_chatbot.core.gui import personas

    return personas.normalize_model(raw) or DEFAULT_MODEL


def load() -> ChatConfig:
    """读配置。**任何异常都退回默认值** —— 配置坏了也不能让程序起不来。"""
    try:
        s = settings_store.app_settings()
        return ChatConfig(
            base_url=_get(s, "base_url", DEFAULT_BASE_URL),
            api_key=_get(s, "api_key", ""),
            model=_model(_get(s, "model", DEFAULT_MODEL)),
            persona_dir=_get(s, "persona_dir", ""),
            persona_files=_as_list(
                s.value(f"{GROUP}/persona_files", None)
            ) or list(DEFAULT_PERSONA_FILES),
            rag_dir=_get(s, "rag_dir", ""),
            rag_ollama=_get(s, "rag_ollama", ""),
            rag_embedding=_get(s, "rag_embedding", ""),
            show_reasoning=_get_bool(s, "show_reasoning", False),
            rag_enabled=_get_bool(s, "rag_enabled", RAG_DEFAULTS["enabled"]),
            rag_autostart=_get_bool(s, "rag_autostart", RAG_DEFAULTS["autostart"]),
            rag_top_k=clamp_int(_get(s, "rag_top_k", RAG_DEFAULTS["top_k"]), "top_k"),
            rag_timeout_ms=clamp_int(
                _get(s, "rag_timeout_ms", RAG_DEFAULTS["timeout_ms"]), "timeout_ms"
            ),
            rag_min_score=clamp_float(
                _get(s, "rag_min_score", RAG_DEFAULTS["min_score"]), "min_score"
            ),
            rag_chunk_chars=clamp_int(
                _get(s, "rag_chunk_chars", RAG_DEFAULTS["chunk_chars"]), "chunk_chars"
            ),
            rag_chunk_overlap=clamp_int(
                _get(s, "rag_chunk_overlap", RAG_DEFAULTS["chunk_overlap"]), "chunk_overlap"
            ),
            rag_max_file_mb=clamp_int(
                _get(s, "rag_max_file_mb", RAG_DEFAULTS["max_file_mb"]), "max_file_mb"
            ),
            rag_max_chunks=clamp_int(
                _get(s, "rag_max_chunks", RAG_DEFAULTS["max_chunks"]), "max_chunks"
            ),
            rag_inject_chars=clamp_int(
                _get(s, "rag_inject_chars", RAG_DEFAULTS["inject_chars"]), "inject_chars"
            ),
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
    s.setValue(f"{GROUP}/show_reasoning", bool(cfg.show_reasoning))
    s.setValue(f"{GROUP}/rag_enabled", bool(cfg.rag_enabled))
    s.setValue(f"{GROUP}/rag_autostart", bool(cfg.rag_autostart))
    s.setValue(f"{GROUP}/rag_top_k", clamp_int(cfg.rag_top_k, "top_k"))
    s.setValue(f"{GROUP}/rag_timeout_ms", clamp_int(cfg.rag_timeout_ms, "timeout_ms"))
    s.setValue(f"{GROUP}/rag_min_score", clamp_float(cfg.rag_min_score, "min_score"))
    s.setValue(f"{GROUP}/rag_chunk_chars", clamp_int(cfg.rag_chunk_chars, "chunk_chars"))
    s.setValue(
        f"{GROUP}/rag_chunk_overlap", clamp_int(cfg.rag_chunk_overlap, "chunk_overlap")
    )
    s.setValue(f"{GROUP}/rag_max_file_mb", clamp_int(cfg.rag_max_file_mb, "max_file_mb"))
    s.setValue(f"{GROUP}/rag_max_chunks", clamp_int(cfg.rag_max_chunks, "max_chunks"))
    s.setValue(
        f"{GROUP}/rag_inject_chars", clamp_int(cfg.rag_inject_chars, "inject_chars")
    )
    s.sync()      # 立刻落盘

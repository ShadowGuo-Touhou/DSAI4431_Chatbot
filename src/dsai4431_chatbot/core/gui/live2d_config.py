"""Live2D 显示配置：换模型 / 缩放 / 偏移 / 取景 / 行为开关 / 隐藏部件。

存在和换肤同一份 ini 里（`themes.settings_path()`），重启后保持。
部件显隐记的是 **部件 id**，而且只在当前模型内有效——换模型会清空，
因为不同 moc3 的部件 id 完全不是一回事。
"""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path

from dsai4431_chatbot.core.gui import themes

GROUP = "live2d"


@dataclass
class Live2DConfig:
    model: str = ""                 # models 目录下的相对路径；空 = 用默认模型
    framing: str = "bust"           # bust | full
    scale: float = 1.0              # 1.0 = 取景原始比例
    offset_x: int = 0               # 像素，正数往右
    offset_y: int = 0               # 像素，正数往下
    physics: bool = True
    blink: bool = True
    breath: bool = True
    follow: bool = True
    hidden_parts: list[str] = field(default_factory=list)

    def model_path(self) -> Path | None:
        """把配置里的 model 解析成实际文件；找不到就退回默认模型。"""
        from dsai4431_chatbot.core.gui import live2d_embed

        if self.model:
            candidate = live2d_embed.MODELS_DIR / self.model
            if candidate.is_file():
                return candidate
        return live2d_embed.default_model()


def _get(settings, key: str, default, kind):
    """QSettings 的 INI 后端会把 bool 存成 true/false，读回来要显式转换。"""
    raw = settings.value(f"{GROUP}/{key}", default)
    if raw is None:
        return default
    if kind is bool:
        if isinstance(raw, bool):
            return raw
        return str(raw).strip().lower() in ("1", "true", "yes", "on")
    try:
        return kind(raw)
    except (TypeError, ValueError):
        return default


def load() -> Live2DConfig:
    s = themes.app_settings()
    hidden = s.value(f"{GROUP}/hidden_parts", [])
    if isinstance(hidden, str):
        hidden = [h for h in hidden.split(",") if h]
    return Live2DConfig(
        model=str(s.value(f"{GROUP}/model", "") or ""),
        framing="full" if str(s.value(f"{GROUP}/framing", "bust")) == "full" else "bust",
        scale=_get(s, "scale", 1.0, float),
        offset_x=_get(s, "offset_x", 0, int),
        offset_y=_get(s, "offset_y", 0, int),
        physics=_get(s, "physics", True, bool),
        blink=_get(s, "blink", True, bool),
        breath=_get(s, "breath", True, bool),
        follow=_get(s, "follow", True, bool),
        hidden_parts=[str(h) for h in hidden],
    )


def save(cfg: Live2DConfig) -> None:
    s = themes.app_settings()
    s.setValue(f"{GROUP}/model", cfg.model)
    s.setValue(f"{GROUP}/framing", cfg.framing)
    s.setValue(f"{GROUP}/scale", cfg.scale)
    s.setValue(f"{GROUP}/offset_x", cfg.offset_x)
    s.setValue(f"{GROUP}/offset_y", cfg.offset_y)
    s.setValue(f"{GROUP}/physics", cfg.physics)
    s.setValue(f"{GROUP}/blink", cfg.blink)
    s.setValue(f"{GROUP}/breath", cfg.breath)
    s.setValue(f"{GROUP}/follow", cfg.follow)
    s.setValue(f"{GROUP}/hidden_parts", list(cfg.hidden_parts))
    s.sync()

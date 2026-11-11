"""Live2D 显示配置：换模型 / 缩放 / 偏移 / 取景 / 行为开关 / 隐藏部件。

存在和换肤同一份 ini 里（`themes.settings_path()`），重启后保持。
部件显隐记的是 **部件 id**，而且只在当前模型内有效——换模型会清空，
因为不同 moc3 的部件 id 完全不是一回事。
"""

from __future__ import annotations

import sys
from dataclasses import dataclass, field
from pathlib import Path

from dsai4431_chatbot.core.gui import themes

GROUP = "live2d"

# 默认套的「换装」。这套模型把换装做成了**表情名**（`expressions` 里那一串中文），
# 不是部件：胸口衣服 = 白衬衫盖住胸口，裙子切换 = 短裙换长裙。
# 学校项目要正经一点，所以默认就穿这套；要改就改 ini 里的 live2d/expressions。
DEFAULT_EXPRESSIONS = ("胸口衣服", "裙子切换")


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
    # 页面加载后套一次的表情（换装）；见 DEFAULT_EXPRESSIONS 的说明
    expressions: list[str] = field(
        default_factory=lambda: list(DEFAULT_EXPRESSIONS)
    )

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


def load() -> Live2DConfig:
    """读配置。**任何异常都退回默认值** —— 配置坏了也不能让程序起不来。"""
    try:
        s = themes.app_settings()
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
            hidden_parts=_as_list(s.value(f"{GROUP}/hidden_parts", None)),
            # 没设过就用默认那套；设成空列表表示「不套任何换装」
            expressions=(
                list(DEFAULT_EXPRESSIONS)
                if s.value(f"{GROUP}/expressions", None) is None
                else _as_list(s.value(f"{GROUP}/expressions", None))
            ),
        )
    except Exception as exc:  # noqa: BLE001 - 配置读挂了就退回默认，不能挡启动
        print(f"[live2d] 配置读取失败，用默认值：{exc}", file=sys.stderr, flush=True)
        return Live2DConfig()


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
    s.setValue(f"{GROUP}/expressions", list(cfg.expressions))
    s.sync()

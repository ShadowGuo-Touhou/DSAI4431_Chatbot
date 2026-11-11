"""界面语言（中文 / English）。

一个语言 = `asset/language/<code>.toml` 一个文件。用嵌套表写，键名就是
点分路径：

    [settings.nav]
    api_key = "API KEY"

读进来会摊平成 `{"settings.nav.api_key": "API KEY"}`，代码里 `t("settings.nav.api_key")`
取值。缺键时按四级回退：

    当前语言 → 回退语言（zh）→ 调用方给的 default → 键名本身

所以少翻译一条不会让界面出现空白或 None。

**换语言为什么不热更新**：文案在构造窗口时取一次（`t()` 直接返回字符串，
控件不会自己再来问）。要做到热更新，得给每个控件记下 key、再挨个 setText，
复杂度不值当 —— 所以按用户选定的方案：换语言 = 存盘 + 重启进程。重启走
`relaunch.py`（它负责等旧进程退干净再拉新的，避免两份 QtWebEngine 抢
同一个 profile 目录）。

启动时 `main()` 里调一次 `apply_saved()`，之后 `current()` 就是缓存值。
"""

from __future__ import annotations

import os
import sys
import tomllib
from dataclasses import dataclass, field
from pathlib import Path

from dsai4431_chatbot.core.gui.settings_store import app_settings

# 界面默认中文（整个项目原本就是中文文案）；缺键统一回退到中文。
DEFAULT_CODE = "zh"
FALLBACK_CODE = "zh"
SETTINGS_KEY = "language/code"

_HERE = Path(__file__).resolve().parent


def language_dir() -> Path:
    """语言包目录 `<repo>/asset/language`（可被 DSAI_LANG_DIR 覆盖）。

    与 live2d_embed 的 `_resolve_asset_root()` 同一套规则：从本文件所在目录
    逐级向上找 asset/language。找不到就返回一个不存在的路径，由加载失败
    分支兜底（界面退回键名，不会崩）。
    """
    env = os.environ.get("DSAI_LANG_DIR")
    if env:
        return Path(env).expanduser().resolve()
    for base in (_HERE, *_HERE.parents):
        cand = base / "asset" / "language"
        if cand.is_dir():
            return cand
    return _HERE / "asset" / "language"


@dataclass(frozen=True)
class Language:
    """一套语言包。`name` 用该语言自己的写法（下拉里显示"中文"/"English"）。"""

    code: str
    name: str
    strings: dict[str, str] = field(default_factory=dict, repr=False)


# 加载缓存：code -> Language
_cache: dict[str, Language] = {}
_current: Language | None = None


def _flatten(node, prefix: str = "") -> dict[str, str]:
    """把嵌套 dict 摊平成点分键；只收字符串叶子（注释/数字也转成字符串）。"""
    flat: dict[str, str] = {}
    for key, value in node.items():
        name = f"{prefix}.{key}" if prefix else str(key)
        if isinstance(value, dict):
            flat.update(_flatten(value, name))
        else:
            flat[name] = str(value)
    return flat


def _load_file(path: Path) -> Language | None:
    """读一个 toml；坏文件只打日志，不抛（配置坏了不能挡住启动）。"""
    try:
        with path.open("rb") as fh:
            data = tomllib.load(fh)
    except (OSError, tomllib.TOMLDecodeError) as exc:
        print(f"[i18n] 语言文件读不了，跳过：{path.name}（{exc}）", file=sys.stderr)
        return None

    strings = _flatten(data)
    code = strings.get("meta.code") or path.stem
    name = strings.get("meta.name") or code
    if not strings:
        print(f"[i18n] 语言文件是空的，跳过：{path.name}", file=sys.stderr)
        return None
    return Language(code=code, name=name, strings=strings)


def available() -> list[Language]:
    """扫描目录下所有语言包；按 code 排序，默认语言排最前。"""
    if _cache:
        return _sorted(_cache.values())

    for path in sorted(language_dir().glob("*.toml")):
        lang = _load_file(path)
        if lang is not None:
            _cache[lang.code] = lang
    return _sorted(_cache.values())


def _sorted(items) -> list[Language]:
    return sorted(items, key=lambda lang: (lang.code != DEFAULT_CODE, lang.code))


def by_code(code: str | None) -> Language | None:
    if not code:
        return None
    if code not in _cache:
        available()          # 触发一次扫描（同时也覆盖"文件刚放进来"的情况）
    return _cache.get(code)


def _fallback() -> Language:
    """回退语言；连 zh 都没有时给一个空壳（t() 会退回键名）。"""
    lang = by_code(FALLBACK_CODE)
    if lang is not None:
        return lang
    found = available()
    return found[0] if found else Language(code=FALLBACK_CODE, name="中文")


def saved_code() -> str:
    """上次选择的语言；没记录或读不出来就是默认中文。"""
    try:
        value = str(app_settings().value(SETTINGS_KEY, "") or "")
    except Exception as exc:          # 配置读坏了也不该挡住启动
        print(f"[i18n] 语言配置读取失败，用默认值：{exc}", file=sys.stderr)
        return DEFAULT_CODE
    return value or DEFAULT_CODE


def current() -> Language:
    global _current
    if _current is None:
        _current = by_code(saved_code()) or _fallback()
    return _current


def set_language(code: str) -> Language:
    """切到某个语言并**立刻落盘**（重启后新进程就按它读文案）。"""
    global _current
    lang = by_code(code) or _fallback()
    _current = lang
    try:
        settings = app_settings()
        settings.setValue(SETTINGS_KEY, lang.code)
        settings.sync()               # 进程马上要退出，不 sync 会丢
    except Exception as exc:
        print(f"[i18n] 语言写入失败：{exc}", file=sys.stderr)
    return lang


def apply_saved() -> Language:
    """启动时调一次：按上次的选择定下语言（就是 `current()`，语义更明确）。"""
    return current()


def t(key: str, default: str | None = None, **fmt) -> str:
    """取一条文案。

    `default` 用于"语言包里没有就用别的来源"的场景，比如主题名：主题自身
    的 toml 里有 label，语言包里没写就用它。
    """
    lang = current()
    text = lang.strings.get(key)
    if not text:
        fallback = _fallback()
        if fallback is not lang:
            text = fallback.strings.get(key)
    if not text:
        text = default if default is not None else key

    if fmt:
        try:
            return text.format(**fmt)
        except (KeyError, IndexError, ValueError):
            # 译文里写了花括号却没给对应参数：原样返回，不要炸界面
            return text
    return text


def reload() -> None:
    """丢掉缓存重新扫描（换语言包/测试用）。"""
    global _current
    _cache.clear()
    _current = None

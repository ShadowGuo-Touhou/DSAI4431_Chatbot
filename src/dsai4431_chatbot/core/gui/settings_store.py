"""界面配置与运行时数据的存放位置。

**程序产生的东西一律留在项目目录里**（用户 2026-11-11 明确要求：不出项目文件夹）：

    <repo>/
    ├── data/                    # 运行时数据（**不入库**：里面有 API Key）
    │   ├── settings.ini         # 主题 / 语言 / Live2D / 对话配置
    │   └── webengine/           # QtWebEngine 的 disk cache 与 local storage
    └── src/…

主题选择（`theme/id`）、界面语言（`language/code`）、Live2D 外观（`live2d/*`）、
对话配置（`chat/*`）都写同一份 ini。这层单独放，是为了让 `themes` 和 `i18n`
都能用，而不用互相 import 成环（主题卡上的名字要从语言包里取）。

覆盖：
- `DSAI_DATA_DIR`：整个 data 目录搬到别处（测试用它隔离）
- `DSAI_CONFIG_DIR`：只改 ini 所在目录

⚠ `data/settings.ini` 里可能有明文的 API Key —— 已在 `.gitignore` 里排除，
**不要**手工 `git add -f` 它，也别把整个项目文件夹打包发给别人。
"""

from __future__ import annotations

import os
import shutil
import sys
from pathlib import Path

from PySide6.QtCore import QSettings, QStandardPaths

ORG = "DSAI4431"
APP = "Chatbot"

DATA_DIRNAME = "data"
# 老版本（2026-11-11 之前）配置在用户目录里的位置，只用于一次性迁移
LEGACY_DIRNAME = "DSAI4431_Chatbot"

_migrated = False


def project_root() -> Path:
    """项目根目录：从本文件往上找带 `pyproject.toml` 的那一层。

    找不到（比如装成了 wheel）就退回当前工作目录 —— 至少还是"当前项目里"。
    """
    here = Path(__file__).resolve()
    for base in (here.parent, *here.parents):
        if (base / "pyproject.toml").is_file():
            return base
    return Path.cwd()


def data_dir() -> Path:
    """运行时数据目录 `<repo>/data`（可被 DSAI_DATA_DIR 覆盖）。"""
    override = os.environ.get("DSAI_DATA_DIR")
    if override:
        root = Path(override).expanduser()
    else:
        root = project_root() / DATA_DIRNAME
    root.mkdir(parents=True, exist_ok=True)
    return root


def webengine_dir() -> Path:
    """QtWebEngine 的缓存/local storage 目录。"""
    path = data_dir() / "webengine"
    path.mkdir(parents=True, exist_ok=True)
    return path


def _legacy_settings_path() -> Path:
    """老位置（用户目录里的 GenericConfigLocation/…），仅用于迁移。"""
    base = QStandardPaths.writableLocation(
        QStandardPaths.StandardLocation.GenericConfigLocation
    )
    if not base:
        return Path()
    return Path(base) / LEGACY_DIRNAME / "settings.ini"


def _migrate_legacy(target: Path) -> None:
    """把老位置那份 ini 复制过来（只做一次，且只在没用环境变量覆盖时做）。

    用户目录里的版本不删：万一新位置出问题，旧配置还在。
    """
    global _migrated
    if _migrated or target.exists():
        _migrated = True
        return
    _migrated = True

    legacy = _legacy_settings_path()
    if not legacy.is_file():
        return
    try:
        shutil.copy2(legacy, target)
        print(f"[settings] 已把旧配置搬到项目内：{target}", file=sys.stderr, flush=True)
    except OSError as exc:
        print(f"[settings] 旧配置迁移失败（不影响启动）：{exc}", file=sys.stderr, flush=True)


def settings_path() -> Path:
    """配置文件位置：`<repo>/data/settings.ini`。

    刻意**不用** `QSettings(org, app)` 的原生后端：Windows 下它写注册表
    `HKCU\\Software\\…`，实测在这台机器上 `status()` 直接是 AccessError，
    写进去也读不回来。落成 ini 文件可靠得多。
    """
    override = os.environ.get("DSAI_CONFIG_DIR")
    if override:
        # 测试用：指到临时目录，不读也不写项目里的那份
        root = Path(override).expanduser()
        root.mkdir(parents=True, exist_ok=True)
        return root / "settings.ini"

    root = data_dir()
    path = root / "settings.ini"
    _migrate_legacy(path)
    return path


def app_settings() -> QSettings:
    return QSettings(str(settings_path()), QSettings.Format.IniFormat)

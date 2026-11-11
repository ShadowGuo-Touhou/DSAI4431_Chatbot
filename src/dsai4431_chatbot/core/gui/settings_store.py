"""界面配置的存放位置（settings.ini）。

主题选择（`theme/id`）、界面语言（`language/code`）、Live2D 外观
（`live2d/*`）都写同一份 ini。这份「去哪儿读写配置」的逻辑单独放一层，
是为了让 `themes` 和 `i18n` 都能用，而不用互相 import 成环
（主题卡上的名字要从语言包里取，语言包不该反过来依赖主题）。

为什么不用 `QSettings(org, app)` 的原生后端：Windows 下它写注册表
`HKCU\\Software\\…`，实测在这台机器上 `status()` 直接是 AccessError，
写进去也读不回来。落成 ini 文件可靠得多。
"""

from __future__ import annotations

import os
from pathlib import Path

from PySide6.QtCore import QSettings, QStandardPaths

ORG = "DSAI4431"
APP = "Chatbot"


def settings_path() -> Path:
    """配置文件位置（Windows 上实测是 %USERPROFILE%\\AppData\\LocalLow\\DSAI4431_Chatbot\\settings.ini）。

    可用 `DSAI_CONFIG_DIR` 覆盖（测试就是这么隔离的）。
    """
    override = os.environ.get("DSAI_CONFIG_DIR")
    if override:
        root = Path(override).expanduser()
    else:
        # GenericConfigLocation 在 Windows 上实测是 %USERPROFILE%\AppData\LocalLow
        # （不是 Roaming 的 %APPDATA%），与 applicationName 无关；用 AppConfigLocation
        # 会变成 <该目录>\<应用名>，而脚本方式启动时应用名是 "python"，路径会跑偏。
        base = QStandardPaths.writableLocation(
            QStandardPaths.StandardLocation.GenericConfigLocation
        )
        root = (Path(base) if base else Path.home()) / "DSAI4431_Chatbot"
    root.mkdir(parents=True, exist_ok=True)
    return root / "settings.ini"


def app_settings() -> QSettings:
    return QSettings(str(settings_path()), QSettings.Format.IniFormat)

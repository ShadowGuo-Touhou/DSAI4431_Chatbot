"""主界面 GUI（PySide6 原生控件）。

框架阶段：只搭结构与样式，不接业务逻辑。
启动方式：

    python -m dsai4431_chatbot.core.gui
"""

from dsai4431_chatbot.core.gui.main_window import MainWindow, main

__all__ = ["MainWindow", "main"]

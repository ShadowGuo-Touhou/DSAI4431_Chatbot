"""启动加载页：一行一个阶段的清单式进度。

为什么要有它：启动要干几件重活 —— 装 Live2D 渲染页、可能要下载 Ollama
（Windows 包约 1.6 GB）与 embedding 模型、同步知识库索引。原来这些都躲在
`QTimer.singleShot(600, ...)` 后面，界面上一点提示都没有，用户会以为
"点了没反应"再点几下。

设计约束（用户 2026-11-12 的要求）：

1. **列表状、可追加**：一行一个阶段，`add_step()` 加。以后接语音模型
   （SenseVoice）只是再 append 一行，不用改这个文件的其它地方。
2. **显示当前阶段内容**：每行有状态（等待 / 进行中 / 完成 / 失败 / 跳过）、
   右侧细节文字（"12.3 / 224 MB"、"45%"）、进行中时的细进度条。
3. **加载期间用户不能互动**：覆盖层铺满客户区，鼠标和键盘事件全部吃掉；
   主内容另外 `setEnabled(False)` 兜住 Tab 焦点。

为什么是覆盖层而不是独立窗口：独立窗口会和主窗口抢激活状态，启动期
还容易一闪而过；覆盖层最省事，尺寸跟着 `MainWindow.resizeEvent` 同步。
"""

from __future__ import annotations

from PySide6.QtCore import QTimer, Qt, Signal
from PySide6.QtWidgets import (
    QFrame,
    QHBoxLayout,
    QLabel,
    QProgressBar,
    QPushButton,
    QSizePolicy,
    QVBoxLayout,
    QWidget,
)

from dsai4431_chatbot.core.gui.i18n import t

# 阶段状态
PENDING = "pending"
RUNNING = "running"
DONE = "done"
FAILED = "failed"
SKIPPED = "skipped"

# 状态字形。用字符而不是图片：不引资源文件，主题换色也能跟着 QSS 走。
_MARKS = {
    PENDING: "○",
    RUNNING: "◐",
    DONE: "✓",
    FAILED: "✕",
    SKIPPED: "–",
}


class StepRow(QWidget):
    """加载清单里的一行：状态字形 + 名称 + 右侧细节 + 细进度条。"""

    # 右侧细节最多这么长，超了截断加省略号。完整错误原因在控制台 / 设置页
    DETAIL_LIMIT = 56

    def __init__(self, key: str, title: str, parent=None) -> None:
        super().__init__(parent)
        self.setObjectName("loadStep")
        self.key = key
        self.status = PENDING                 # 注意别用 state：QWidget 没有但语义容易撞
        self._progress = 0.0

        lay = QVBoxLayout(self)
        lay.setContentsMargins(0, 0, 0, 0)
        lay.setSpacing(6)

        line = QHBoxLayout()
        line.setContentsMargins(0, 0, 0, 0)
        line.setSpacing(10)

        self._mark = QLabel(_MARKS[PENDING])
        self._mark.setObjectName("loadMark")
        self._mark.setFixedWidth(16)
        self._mark.setAlignment(Qt.AlignmentFlag.AlignCenter)
        line.addWidget(self._mark)

        self._title = QLabel(title)
        self._title.setObjectName("loadStepTitle")
        # 标题**不许被压缩**：QLabel 默认会伸展，右侧的细节一长就把名字挤成
        # 「Restoring the last co…」这个样子。设成 Fixed，宽度就跟着文字走。
        self._title.setSizePolicy(
            QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Preferred
        )
        line.addWidget(self._title)

        self._detail = QLabel("")
        self._detail.setObjectName("loadStepDetail")
        self._detail.setAlignment(
            Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter
        )
        # 细节自己吃掉中间所有剩余空间（文字右对齐）。**不能**用 addStretch
        # 顶开：stretch 会把宽抢光，detail 被压到只剩一个字（实测过）。
        self._detail.setSizePolicy(
            QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred
        )
        line.addWidget(self._detail, 1)
        lay.addLayout(line)

        self._bar = QProgressBar()
        self._bar.setObjectName("loadBar")
        self._bar.setFixedHeight(4)
        self._bar.setTextVisible(False)
        self._bar.setRange(0, 1000)
        self._bar.setValue(0)
        self._bar.hide()
        lay.addWidget(self._bar)

        self._apply()

    # --- 外观 -----------------------------------------------------------
    def _apply(self) -> None:
        """改完动态属性必须 unpolish/polish，否则 QSS 不重算（老坑）。"""
        self.setProperty("state", self.status)
        self._mark.setText(_MARKS[self.status])
        for widget in (self, self._mark, self._title, self._detail):
            style = widget.style()
            style.unpolish(widget)
            style.polish(widget)

    def set_detail(self, text: str) -> None:
        self._show_detail(text)

    def _show_detail(self, text: str) -> None:
        text = text or ""
        if len(text) > self.DETAIL_LIMIT:
            text = text[: self.DETAIL_LIMIT - 1] + "…"
        self._detail.setText(text)

    # --- 状态迁移 -------------------------------------------------------
    def start(self, detail: str = "") -> None:
        """进入"进行中"；进度条先给不确定态（等真实总量到了再转百分比）。"""
        self.status = RUNNING
        self._progress = 0.0
        if detail:
            self._show_detail(detail)
        self._bar.setRange(0, 0)              # 不确定：Qt 画滚动块
        self._bar.show()
        self._apply()

    def set_progress(self, fraction: float, detail: str | None = None) -> None:
        """确定的百分比。`fraction` 0..1。"""
        value = max(0.0, min(1.0, float(fraction)))
        self._progress = value
        self._bar.setRange(0, 1000)
        self._bar.setValue(int(value * 1000))
        self._bar.show()
        if detail is not None:
            self._show_detail(detail)

    def done(self, detail: str = "") -> None:
        self.status = DONE
        self._progress = 1.0
        self._settle(detail)

    def failed(self, detail: str = "") -> None:
        self.status = FAILED
        self._progress = 1.0
        self._settle(detail)

    def skipped(self, detail: str = "") -> None:
        self.status = SKIPPED
        self._progress = 1.0
        self._settle(detail)

    def _settle(self, detail: str) -> None:
        if detail:
            self._show_detail(detail)
        self._bar.hide()
        self._apply()


class LoadingPage(QWidget):
    """铺满客户区的加载覆盖层。

    信号：
    - `skip_requested`：用户点了「跳过下载」
    - `closed`：覆盖层已收起（主界面可以解禁）
    """

    skip_requested = Signal()
    closed = Signal()

    MAX_WIDTH = 620
    CLOSE_DELAY_MS = 280

    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.setObjectName("loadingPage")
        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)
        # 拿住焦点，Tab 才不会跑到下面被盖住的按钮上
        self.setFocusPolicy(Qt.FocusPolicy.StrongFocus)

        self._rows: dict[str, StepRow] = {}
        self._weights: dict[str, float] = {}
        self._closed = False

        outer = QVBoxLayout(self)
        outer.setContentsMargins(48, 40, 48, 40)
        outer.addStretch(3)

        card = QFrame()
        card.setObjectName("loadingCard")
        card.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)
        card.setMaximumWidth(self.MAX_WIDTH)
        col = QVBoxLayout(card)
        col.setContentsMargins(30, 26, 30, 20)
        col.setSpacing(12)

        self._title = QLabel(t("loading.title"))
        self._title.setObjectName("loadingTitle")
        col.addWidget(self._title)

        self._subtitle = QLabel(t("loading.subtitle"))
        self._subtitle.setObjectName("loadingSubtitle")
        self._subtitle.setWordWrap(True)
        col.addWidget(self._subtitle)

        self._list = QVBoxLayout()
        self._list.setContentsMargins(0, 8, 0, 8)
        self._list.setSpacing(13)
        col.addLayout(self._list)

        self._overall = QProgressBar()
        self._overall.setObjectName("loadOverall")
        self._overall.setFixedHeight(6)
        self._overall.setTextVisible(False)
        self._overall.setRange(0, 1000)
        self._overall.setValue(0)
        col.addWidget(self._overall)

        foot = QHBoxLayout()
        foot.setContentsMargins(0, 2, 0, 0)
        foot.setSpacing(8)

        self._hint = QLabel(t("loading.busy_hint"))
        self._hint.setObjectName("loadingHint")
        self._hint.setWordWrap(True)
        foot.addWidget(self._hint, 1)

        self._btn_skip = QPushButton(t("loading.skip"))
        self._btn_skip.setObjectName("loadingSkip")
        self._btn_skip.setCursor(Qt.CursorShape.PointingHandCursor)
        self._btn_skip.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self._btn_skip.clicked.connect(self.skip_requested.emit)
        self._btn_skip.hide()
        foot.addWidget(self._btn_skip)
        col.addLayout(foot)

        row = QHBoxLayout()
        row.setContentsMargins(0, 0, 0, 0)
        row.addStretch(1)
        row.addWidget(card)
        row.addStretch(1)
        outer.addLayout(row)
        outer.addStretch(5)

    # --- 阶段清单 -------------------------------------------------------
    def add_step(self, key: str, title: str, weight: float = 1.0) -> StepRow:
        """往清单里追加一行。`weight` 只影响底部总进度条的权重占比。"""
        if key in self._rows:
            raise KeyError(f"重复的加载阶段：{key}")
        row = StepRow(key, title, self)
        self._rows[key] = row
        self._weights[key] = max(0.01, float(weight))
        self._list.addWidget(row)
        self._refresh_overall()
        return row

    def row(self, key: str) -> StepRow | None:
        return self._rows.get(key)

    def step(self, key: str) -> StepRow:
        row = self._rows.get(key)
        if row is None:
            raise KeyError(f"没有这个加载阶段：{key}")
        return row

    def keys(self) -> list[str]:
        return list(self._rows)

    # --- 提示 / 按钮 ----------------------------------------------------
    def set_hint(self, text: str) -> None:
        self._hint.setText(text)

    def set_skip_text(self, text: str) -> None:
        self._btn_skip.setText(text)

    def show_skip(self, visible: bool) -> None:
        self._btn_skip.setVisible(bool(visible))

    # --- 总进度 ---------------------------------------------------------
    def _refresh_overall(self) -> None:
        total = sum(self._weights.values()) or 1.0
        acc = 0.0
        for key, weight in self._weights.items():
            row = self._rows[key]
            if row.status in (DONE, FAILED, SKIPPED):
                acc += weight
            elif row.status == RUNNING:
                acc += weight * row._progress
        self._overall.setRange(0, 1000)
        self._overall.setValue(int(acc / total * 1000))

    def refresh_progress(self) -> None:
        """某一行改过之后调一次（行自己不知道总进度）。"""
        self._refresh_overall()

    # --- 收尾 -----------------------------------------------------------
    def complete(self) -> None:
        """全部结束：总进度打满，稍等一下再收起（让用户看见 100%）。"""
        if self._closed:
            return
        self._closed = True
        self._overall.setRange(0, 1000)
        self._overall.setValue(1000)
        self._hint.setText(t("loading.enter_hint"))
        QTimer.singleShot(self.CLOSE_DELAY_MS, self._close)

    def _close(self) -> None:
        self.hide()
        self.closed.emit()

    # --- 吃掉所有输入 ---------------------------------------------------
    # 加载期间用户不能互动：覆盖层下面的控件既点不到（这些事件到此为止），
    # 焦点也切不过去（focusNextPrevChild 返回 True 表示"我处理了"）。
    def mousePressEvent(self, event):        # noqa: N802 - Qt 命名
        event.accept()

    def mouseReleaseEvent(self, event):      # noqa: N802
        event.accept()

    def mouseDoubleClickEvent(self, event):  # noqa: N802
        event.accept()

    def wheelEvent(self, event):             # noqa: N802
        event.accept()

    def keyPressEvent(self, event):          # noqa: N802
        event.accept()

    def keyReleaseEvent(self, event):        # noqa: N802
        event.accept()

    def focusNextPrevChild(self, _next):     # noqa: N802
        return True

    def showEvent(self, event):              # noqa: N802
        super().showEvent(event)
        self.setFocus(Qt.FocusReason.OtherFocusReason)

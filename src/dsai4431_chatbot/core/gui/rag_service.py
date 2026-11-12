"""知识库索引服务：后台同步 + 索引缓存 + 检索入口。

**线程模型（重要）**：worker 线程里**不碰任何 Qt 对象**。
后台任务只往一个带锁的 `_Job` 里写数据，主线程用 `QTimer` 每 120ms 读一次再发信号。
原因：在 QRunnable 里 emit 主线程 QObject 的信号，PySide6 会抛
`RuntimeError: Signal source has been deleted`（实测，且会把整次同步打断——
索引于是永远建不出来）。改成「worker 写数据 / 主线程轮询」，既没这个坑，
进度也不会因为事件队列忙而延迟。
"""

from __future__ import annotations

import threading

from PySide6.QtCore import QObject, QRunnable, QThreadPool, QTimer, Signal

from dsai4431_chatbot.core.gui import chat_config, ollama_launcher

POLL_MS = 120


class _Job:
    """worker 与主线程之间唯一的数据通道（纯 Python，自己加锁）。"""

    def __init__(self) -> None:
        self.lock = threading.Lock()
        self.progress = (0, 0, "")
        self.ticks = 0
        self.launch = None          # ollama_launcher.LaunchResult
        self.result = None          # indexer.SyncResult
        self.error: BaseException | None = None
        self.done = False

    def set_progress(self, done: int, total: int, rel: str) -> None:
        with self.lock:
            self.progress = (int(done), int(total), str(rel))
            self.ticks += 1

    def snapshot(self) -> tuple[tuple[int, int, str], int, object, object, BaseException | None, bool]:
        with self.lock:
            return (
                self.progress,
                self.ticks,
                self.launch,
                self.result,
                self.error,
                self.done,
            )


class _SyncTask(QRunnable):
    """后台跑一次「确保 Ollama 在跑 + 差量同步」。"""

    def __init__(self, cfg, job: _Job, embedder=None, ensure_runner=None) -> None:
        super().__init__()
        self.cfg = cfg
        self.job = job
        self.embedder = embedder
        self.ensure_runner = ensure_runner
        self.setAutoDelete(True)

    def run(self) -> None:                      # noqa: D401 - QRunnable 约定
        from dsai4431_chatbot.core.rag import indexer

        job = self.job
        try:
            # 1) 探测 / 按需拉起 Ollama（已经在跑就什么都不做）
            if self.ensure_runner is not None:
                try:
                    launch = self.ensure_runner(self.cfg)
                except Exception as exc:        # noqa: BLE001 - 后台不能把异常丢给 Qt
                    print(f"[rag] 拉起 Ollama 时出错：{exc}", flush=True)
                else:
                    with job.lock:
                        job.launch = launch

            # 2) 差量同步
            result = indexer.sync_once(
                self.cfg, runtime=self.embedder, progress=job.set_progress
            )
            with job.lock:
                job.result = result
        except BaseException as exc:            # noqa: BLE001 - 同上，交给主线程显示
            with job.lock:
                job.error = exc
            print(f"[rag] 同步失败：{exc}", flush=True)
        finally:
            with job.lock:
                job.done = True


class RagService(QObject):
    """索引缓存的持有者。`ChatColumn` 用它检索，`RagPage` 用它刷新状态。"""

    progress = Signal(int, int, str)            # 进度（done, total, 当前文件）
    ollama_ready = Signal(object)               # ollama_launcher.LaunchResult
    synced = Signal(object)                     # indexer.SyncResult
    syncing_changed = Signal(bool)              # 开始 / 结束

    def __init__(self, parent=None, *, embedder=None, ensure_runner=None) -> None:
        super().__init__(parent)
        self._pool = QThreadPool.globalInstance()
        self._cfg = None
        self._index = None
        self._loaded = False
        self._running = False
        self._again = False
        self._job: _Job | None = None
        self._seen_ticks = 0
        self._seen_launch = False
        self._embedder = embedder               # 测试注入；None = 按配置造
        # 传了 embedder（测试）时默认不真的去起 Ollama，避免测试去 spawn 真进程
        if ensure_runner is None and embedder is None:
            ensure_runner = ollama_launcher.ensure_running
        self._ensure_runner = ensure_runner
        self.last_result = None
        self.last_launch = None
        self._timer = QTimer(self)
        self._timer.setInterval(POLL_MS)
        self._timer.timeout.connect(self._poll)

    # --- 索引 -----------------------------------------------------------
    def index(self):
        """懒加载索引（第一次调用读盘）。

        ⚠ 只在 `_index` 有内容时才缓存：如果第一次读的时候索引还没建好（启动同步
        还没跑完），这里必须允许**下次再试**——否则这一轮启动直到重启都检索不到
        东西（实测过：点得比同步快一步，就永远空了）。
        """
        if self._index is None:
            from dsai4431_chatbot.core.rag import store

            self._index = store.load()
            self._loaded = True
        return self._index

    def reload_index(self) -> None:
        from dsai4431_chatbot.core.rag import store

        self._index = store.load()
        self._loaded = True

    def status(self) -> dict:
        from dsai4431_chatbot.core.rag import store

        return store.summary(self.index())

    # --- 同步 -----------------------------------------------------------
    def refresh(self, cfg=None) -> bool:
        """触发一次同步。正在跑就返回 False（会记下「再来一次」）。"""
        if self._running:
            self._again = True
            return False
        self._cfg = cfg or chat_config.load()
        job = _Job()
        self._job = job
        self._seen_ticks = 0
        self._seen_launch = False
        self._running = True
        self._again = False
        self.syncing_changed.emit(True)
        self._pool.start(_SyncTask(self._cfg, job, self._embedder, self._ensure_runner))
        self._timer.start()
        return True

    def is_syncing(self) -> bool:
        return self._running

    def _poll(self) -> None:
        """主线程侧：把 worker 写下来的东西变成 Qt 信号。"""
        job = self._job
        if job is None:
            self._timer.stop()
            return
        progress, ticks, launch, result, error, done = job.snapshot()

        if ticks != self._seen_ticks:
            self._seen_ticks = ticks
            self.progress.emit(*progress)

        if launch is not None and not self._seen_launch:
            self._seen_launch = True
            self.last_launch = launch
            self.ollama_ready.emit(launch)

        if not done:
            return

        self._timer.stop()
        self._job = None
        self._running = False
        self.last_result = result
        if error is None:
            self.synced.emit(result)
            if result is not None and result.status == "ok":
                self.reload_index()
        self.syncing_changed.emit(False)
        if self._again:
            self._again = False
            self.refresh(self._cfg if self._cfg is not None else chat_config.load())

    # --- 检索 -----------------------------------------------------------
    def search(self, query: str, cfg=None):
        """同步检索（调用方负责别在超时前卡太久；超时由 retriever 处理）。"""
        from dsai4431_chatbot.core.rag import retriever

        current = cfg or chat_config.load()
        index = self.index()
        if index is None or len(index) == 0:
            return retriever.Retrieval()
        return retriever.search(query, index, current, runtime=self._embedder)

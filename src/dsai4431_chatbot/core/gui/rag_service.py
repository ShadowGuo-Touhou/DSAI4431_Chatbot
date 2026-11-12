"""RAG 的 Qt 侧外壳：把「扫目录 + 切片 + 算向量」扔到后台线程，并缓存索引。

设计要点（都是踩过的坑）：

- **绝不在主线程算向量**：首次全量能跑几十秒，界面上得照常打字
- **同一时间只跑一个同步任务**：运行中再触发就记一笔，跑完再补一次（合并）
- **索引只读**：同步完成后把新索引读进内存；检索直接用缓存，不再碰磁盘
"""

from __future__ import annotations

from PySide6.QtCore import QObject, QRunnable, QThreadPool, Signal

from dsai4431_chatbot.core.gui import chat_config


class _SyncSignals(QObject):
    progress = Signal(int, int, str)
    finished = Signal(object)      # indexer.SyncResult


class _SyncTask(QRunnable):
    """后台跑一次差量同步。"""

    def __init__(self, cfg, embedder=None) -> None:
        super().__init__()
        self.cfg = cfg
        self.embedder = embedder
        self.signals = _SyncSignals()
        self.setAutoDelete(True)

    def run(self) -> None:                      # noqa: D401 - QRunnable 约定
        from dsai4431_chatbot.core.rag import indexer

        def report(done: int, total: int, rel: str) -> None:
            self.signals.progress.emit(int(done), int(total), str(rel))

        try:
            result = indexer.sync_once(self.cfg, runtime=self.embedder, progress=report)
        except Exception as exc:                # noqa: BLE001 - 后台线程不能把异常丢给 Qt
            print(f"[rag] 同步失败：{exc}", flush=True)
            return
        self.signals.finished.emit(result)


class RagService(QObject):
    """索引缓存的持有者。`ChatColumn` 用它检索，`RagPage` 用它刷新状态。"""

    progress = Signal(int, int, str)            # 进度（done, total, 当前文件）
    synced = Signal(object)                     # indexer.SyncResult
    syncing_changed = Signal(bool)              # 开始 / 结束

    def __init__(self, parent=None, *, embedder=None) -> None:
        super().__init__(parent)
        self._pool = QThreadPool.globalInstance()
        self._cfg = None
        self._index = None
        self._loaded = False
        self._running = False
        self._again = False
        self._embedder = embedder               # 测试注入；None = 按配置造
        self.last_result = None

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
        task = _SyncTask(self._cfg, self._embedder)
        task.signals.progress.connect(self.progress)
        task.signals.finished.connect(self._on_finished)
        self._running = True
        self._again = False
        self.syncing_changed.emit(True)
        self._pool.start(task)
        return True

    def is_syncing(self) -> bool:
        return self._running

    def _on_finished(self, result) -> None:
        self._running = False
        self.last_result = result
        self.synced.emit(result)
        self.syncing_changed.emit(False)
        if result is not None and result.status == "ok":
            self.reload_index()
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

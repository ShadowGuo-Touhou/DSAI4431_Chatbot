"""每份源文件「已经在语料库里没有」的判定（设置页右侧那个绿/红标记）。

判定口径和 `indexer` 完全一致：比**整文件的 sha256**。
为了不每次都把几 MB 全读一遍，先走「大小 + mtime 都没变 → 直接认为入库」的快路
（`indexer` 复用台账也是这个条件），只有变了才真算 hash。
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from dsai4431_chatbot.core.rag import loader

# 已入库（绿）
STATE_INDEXED = "indexed"
# 台账里有、但内容变了（红）
STATE_CHANGED = "changed"
# 台账里压根没有（红）
STATE_NEW = "new"
# 读不出来（灰）
STATE_UNREADABLE = "unreadable"


@dataclass
class FileState:
    rel: str
    size: int
    state: str
    sha256: str = ""

    @property
    def indexed(self) -> bool:
        return self.state == STATE_INDEXED


def file_states(
    root: Path,
    *,
    max_file_mb: int = 2,
    meta: dict | None = None,
) -> tuple[list[FileState], list[dict]]:
    """返回 (每份文件的状态, 被跳过的条目)。

    `meta` 是 `store.load().meta`（没建过索引就传 None → 全部算「新文件」）。
    """
    scanned = loader.scan(root, max_file_mb)
    ledger = dict((meta or {}).get("files") or {})

    rows: list[FileState] = []
    for rel in sorted(scanned.files):
        size, mtime_ns = scanned.files[rel]
        entry = ledger.get(rel)
        if (
            entry is not None
            and entry.get("size") == size
            and entry.get("mtime_ns") == mtime_ns
            and entry.get("digests")
        ):
            rows.append(FileState(rel, size, STATE_INDEXED, entry.get("sha256", "")))
            continue

        # 变了或者没见过：才真算 hash（大文件也就一次）
        digest = loader.sha256_file(root / rel)
        if not digest:
            rows.append(FileState(rel, size, STATE_UNREADABLE, ""))
            continue
        if entry is not None and entry.get("sha256") == digest:
            # mtime 变了但内容没变（复制/改时间戳）→ 索引里还是这份内容
            rows.append(FileState(rel, size, STATE_INDEXED, digest))
        else:
            rows.append(
                FileState(rel, size, STATE_CHANGED if entry is not None else STATE_NEW, digest)
            )
    return rows, list(scanned.skipped)


def counts(states: list[FileState]) -> dict[str, int]:
    """`{"indexed": 3, "pending": 2, ...}`，给状态行用。"""
    out = {STATE_INDEXED: 0, STATE_CHANGED: 0, STATE_NEW: 0, STATE_UNREADABLE: 0}
    for row in states:
        out[row.state] = out.get(row.state, 0) + 1
    out["pending"] = out[STATE_CHANGED] + out[STATE_NEW]
    return out

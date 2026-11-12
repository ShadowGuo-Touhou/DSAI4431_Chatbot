"""索引读写：`meta.json`（台账 + 切片文本）+ `index.npz`（向量）。

格式与写入协议见 `RAG_PLAN.md` §2。要点：

- 两个文件**按下标逐行对应**，`digests` 做交叉校验
- 写入先落 `.tmp/`，再 `os.replace`；任何时刻磁盘上都有一份完整可用的旧索引
- 读的时候校验不过就当没有（调用方会重建），**永远不信任缓存**
"""

from __future__ import annotations

import json
import os
from dataclasses import dataclass
from pathlib import Path

import numpy as np

from dsai4431_chatbot.core.rag import paths

META_NAME = "meta.json"
INDEX_NAME = "index.npz"


@dataclass
class Index:
    """载入内存的索引。`vectors` 与 `meta["chunks"]` 逐行对应。"""

    meta: dict
    vectors: np.ndarray

    @property
    def chunks(self) -> list[dict]:
        return self.meta.get("chunks", [])

    @property
    def files(self) -> dict:
        return self.meta.get("files", {})

    def __len__(self) -> int:
        return len(self.chunks)

    def digest_to_index(self) -> dict[str, int]:
        return {chunk["digest"]: row for row, chunk in enumerate(self.chunks)}


# ---------------------------------------------------------------------------
# 读
# ---------------------------------------------------------------------------
def load(index_dir: Path | None = None) -> Index | None:
    """读索引；文件缺失/损坏/对不上都返回 None（不当异常抛）。"""
    directory = Path(index_dir) if index_dir else paths.index_dir()
    meta_path = directory / META_NAME
    npz_path = directory / INDEX_NAME
    if not meta_path.is_file() or not npz_path.is_file():
        return None
    try:
        meta = json.loads(meta_path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return None
    if not isinstance(meta, dict) or meta.get("version") != paths.INDEX_VERSION:
        return None

    try:
        with np.load(npz_path) as data:
            vectors = np.asarray(data["vectors"], dtype=np.float32)
            digests = [str(item) for item in data["digests"]]
    except (OSError, KeyError, ValueError):
        return None

    if not _consistent(meta, vectors, digests):
        return None
    return Index(meta=meta, vectors=vectors)


def _consistent(meta: dict, vectors: np.ndarray, digests: list[str]) -> bool:
    chunks = meta.get("chunks") or []
    if vectors.ndim != 2:
        return False
    if len(chunks) != vectors.shape[0] or len(chunks) != len(digests):
        return False
    return all(chunk.get("digest") == digests[row] for row, chunk in enumerate(chunks))


# ---------------------------------------------------------------------------
# 写
# ---------------------------------------------------------------------------
def save(meta: dict, vectors: np.ndarray, index_dir: Path | None = None) -> None:
    """原子写入。先写两个临时文件，再按「先 npz 后 json」替换。"""
    directory = Path(index_dir) if index_dir else paths.index_dir()
    directory.mkdir(parents=True, exist_ok=True)
    tmp = directory / ".tmp"
    tmp.mkdir(exist_ok=True)

    meta = dict(meta)
    meta["version"] = paths.INDEX_VERSION
    chunks = meta.get("chunks") or []
    vectors = np.asarray(vectors, dtype=np.float32)
    if vectors.size == 0:
        vectors = np.zeros((0, 1), dtype=np.float32)
    digests = np.asarray([chunk["digest"] for chunk in chunks], dtype="<U12")

    tmp_meta = tmp / f"{META_NAME}.tmp"
    tmp_npz = tmp / f"{INDEX_NAME}.tmp"
    tmp_meta.write_text(json.dumps(meta, ensure_ascii=False, indent=2), encoding="utf-8")
    with open(tmp_npz, "wb") as handle:
        np.savez(handle, vectors=vectors, digests=digests)
        handle.flush()
        os.fsync(handle.fileno())

    os.replace(tmp_npz, directory / INDEX_NAME)
    os.replace(tmp_meta, directory / META_NAME)


def clear(index_dir: Path | None = None) -> None:
    """删掉索引文件（设置页「清空索引」）。"""
    directory = Path(index_dir) if index_dir else paths.index_dir()
    for name in (META_NAME, INDEX_NAME):
        try:
            (directory / name).unlink()
        except OSError:
            pass


def summary(index: Index | None) -> dict:
    """给状态栏用的一行摘要。"""
    if index is None or not index.chunks:
        return {"files": 0, "chunks": 0, "dim": 0, "built_at": ""}
    vectors = index.vectors
    return {
        "files": len(index.files),
        "chunks": len(index.chunks),
        "dim": int(vectors.shape[1]) if vectors.ndim == 2 else 0,
        "built_at": index.meta.get("built_at", ""),
    }

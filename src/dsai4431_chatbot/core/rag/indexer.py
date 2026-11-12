"""启动时差量同步：扫目录 → 比对台账 → 只对新增/改过的文件重新切片和算向量。

一次启动只跑一次（用户 2026-11-12 决定：不做文件监听、不做轮询）。
运行中想立刻生效就用设置页的「重新扫描」。

不变的部分**绝不重新 embed**：向量按 `digest` 复用，连改名/挪文件也能认出来
（内容一样 → digest 一样 → 直接搬向量）。
"""

from __future__ import annotations

import hashlib
import time
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path

import numpy as np

from dsai4431_chatbot.core.rag import chunker, embedder as embedder_mod, loader, paths, store


@dataclass
class SyncResult:
    """一次同步的结果。`status` 决定界面怎么说话。"""

    status: str = "ok"          # ok / empty / failed / too_many_chunks
    files: int = 0
    chunks: int = 0
    added: int = 0
    updated: int = 0
    removed: int = 0
    reused: int = 0
    embedded: int = 0
    skipped: list[dict] = field(default_factory=list)
    error: str = ""
    elapsed_s: float = 0.0

    @property
    def ok(self) -> bool:
        return self.status in ("ok", "empty")


def _iso_now() -> str:
    return datetime.now().astimezone().isoformat(timespec="seconds")


def _sha256(path: Path) -> str:
    """文件哈希（口径统一在 loader.sha256_file，设置页的「已入库/未入库」也用它）。"""
    return loader.sha256_file(path)


def sync_once(
    cfg,
    *,
    runtime=None,
    progress=None,
) -> SyncResult:
    """跑一次差量同步。`runtime` 是缓存的 embedder（没有就现场造一个）。"""
    started = time.perf_counter()
    result = SyncResult()

    root = paths.knowledge_root(getattr(cfg, "rag_dir", ""))
    scan = loader.scan(root, int(getattr(cfg, "rag_max_file_mb", 2)))
    result.skipped = list(scan.skipped)

    if not scan.files:
        result.status = "empty"
        result.elapsed_s = time.perf_counter() - started
        return result

    index_dir = paths.index_dir()
    signature = paths.signature(cfg)
    size_cfg = int(getattr(cfg, "rag_chunk_chars", chunker.DEFAULT_SIZE))
    overlap_cfg = int(getattr(cfg, "rag_chunk_overlap", chunker.DEFAULT_OVERLAP))
    max_chunks = int(getattr(cfg, "rag_max_chunks", 2000))

    old = store.load(index_dir)
    # 签名不一致（换模型 / 改块大小 / 换目录）→ 旧向量口径全废，一个都不复用
    fresh = old is None or old.meta.get("signature") != signature
    old_vectors = {} if fresh else _vector_map(old)
    old_chunks = {} if fresh else {c["digest"]: c for c in old.chunks}
    old_files = {} if fresh else dict(old.files)

    # --- 1) 逐个文件决定「复用台账」还是「重切」--------------------------
    per_file: list[tuple[str, tuple[int, int], list[chunker.Chunk], str]] = []
    total_files = len(scan.files)
    for done, (rel, stamp) in enumerate(sorted(scan.files.items()), start=1):
        if progress:
            progress(done, total_files, rel)
        previous = old_files.get(rel)
        unchanged = (
            previous is not None
            and (previous.get("size"), previous.get("mtime_ns")) == stamp
            and previous.get("digests")
            and all(digest in old_chunks for digest in previous["digests"])
        )
        if unchanged:
            per_file.append((rel, stamp, [], previous.get("sha256", "")))
            result.reused += len(previous["digests"])
            continue

        text = loader.read_text(root, rel)
        if text is None:
            result.skipped.append({"rel": rel, "reason": "read_failed"})
            continue
        pieces = chunker.split_document(
            rel, text, size=size_cfg, overlap=overlap_cfg
        )
        if pieces:
            if rel in old_files:
                result.updated += 1
            else:
                result.added += 1
        per_file.append((rel, stamp, pieces, _sha256(root / rel)))

    # --- 2) 组装最终的 chunks（按文件名排序，结果可复现）----------------
    chunks: list[dict] = []
    vectors_by_digest: dict[str, np.ndarray] = {}
    files_meta: dict[str, dict] = {}
    seen: dict[str, int] = {}          # digest → chunks 下标（去重）
    pending: list[str] = []            # 待 embed 的文本，按 digest 索引
    pending_text: dict[str, str] = {}

    for rel, stamp, pieces, sha in per_file:
        previous = old_files.get(rel)
        if not pieces and previous is not None:
            # 台账原样搬过来
            digests = list(previous.get("digests", []))
            for digest in digests:
                _place_chunk(chunks, seen, old_chunks[digest], digest, rel)
                vector = old_vectors.get(digest)
                if vector is not None:
                    vectors_by_digest[digest] = vector
            files_meta[rel] = dict(previous)
            continue

        digests: list[str] = []
        for piece in pieces:
            digests.append(piece.digest)
            _place_chunk(chunks, seen, _chunk_to_dict(piece), piece.digest, rel)
            if piece.digest not in vectors_by_digest:
                vector = old_vectors.get(piece.digest)
                if vector is not None:
                    vectors_by_digest[piece.digest] = vector
                elif piece.digest not in pending_text:
                    pending.append(piece.digest)
                    pending_text[piece.digest] = piece.text
        files_meta[rel] = {
            "size": stamp[0],
            "mtime_ns": stamp[1],
            "sha256": sha,
            "chunks": len(digests),
            "digests": digests,
            "indexed_at": int(time.time()),
        }

    result.files = len(files_meta)
    result.chunks = len(chunks)
    result.removed = max(0, len(old_files) - len(files_meta))

    if len(chunks) > max_chunks:
        result.status = "too_many_chunks"
        result.error = f"{len(chunks)} 块，超过上限 {max_chunks}"
        result.elapsed_s = time.perf_counter() - started
        return result

    # --- 3) 只 embed 缺的那些 ------------------------------------------
    if pending:
        engine = runtime or embedder_mod.make_embedder(cfg)
        try:
            matrix = engine.embed([pending_text[digest] for digest in pending])
        except embedder_mod.EmbedError as exc:
            result.status = "failed"
            result.error = str(exc)
            result.elapsed_s = time.perf_counter() - started
            return result
        for row, digest in enumerate(pending):
            vectors_by_digest[digest] = matrix[row]
        result.embedded = len(pending)

    # --- 4) 落盘（原子）------------------------------------------------
    dim = _guess_dim(chunks, vectors_by_digest)
    vectors = np.zeros((len(chunks), dim), dtype=np.float32)
    for row, chunk in enumerate(chunks):
        vector = vectors_by_digest.get(chunk["digest"])
        if vector is not None:
            vectors[row] = vector

    meta = {
        "signature": signature,
        "signature_parts": {
            "root": paths.rel_to_project(root),
            "model": getattr(cfg, "rag_embedding", ""),
            "dim": dim,
            "chunk_chars": size_cfg,
            "chunk_overlap": overlap_cfg,
            "max_file_mb": int(getattr(cfg, "rag_max_file_mb", 2)),
            "exts": list(loader.TEXT_EXTS),
        },
        "built_at": _iso_now(),
        "stats": {
            "files": len(files_meta),
            "chunks": len(chunks),
            "skipped": result.skipped,
        },
        "files": files_meta,
        "chunks": chunks,
    }
    try:
        store.save(meta, vectors, index_dir)
    except OSError as exc:
        result.status = "failed"
        result.error = f"写索引失败：{exc}"
        result.elapsed_s = time.perf_counter() - started
        return result

    result.status = "ok"
    result.elapsed_s = time.perf_counter() - started
    return result


# ---------------------------------------------------------------------------
# 小工具
# ---------------------------------------------------------------------------
def _chunk_to_dict(piece: chunker.Chunk) -> dict:
    return {
        "digest": piece.digest,
        "text": piece.text,
        "source": piece.source,
        "heading": piece.heading,
        "start_line": piece.start_line,
        "end_line": piece.end_line,
        "dupes": [],
    }


def _place_chunk(
    chunks: list[dict], seen: dict[str, int], chunk: dict, digest: str, rel: str
) -> None:
    """同一段内容只留一块；后来发现的来源记到 `dupes`。"""
    if digest in seen:
        existing = chunks[seen[digest]]
        if rel not in existing["dupes"] and existing["source"] != rel:
            existing["dupes"].append(rel)
        return
    item = dict(chunk)
    item["dupes"] = list(item.get("dupes") or [])
    item["i"] = len(chunks)
    seen[digest] = len(chunks)
    chunks.append(item)


def _vector_map(index: store.Index) -> dict[str, np.ndarray]:
    return {
        chunk["digest"]: index.vectors[row]
        for row, chunk in enumerate(index.chunks)
    }


def _guess_dim(chunks: list[dict], vectors: dict[str, np.ndarray]) -> int:
    for chunk in chunks:
        vector = vectors.get(chunk["digest"])
        if vector is not None:
            return int(np.asarray(vector).shape[0])
    return 1

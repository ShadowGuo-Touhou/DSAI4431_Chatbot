"""扫描知识库目录、读文本。不做切片（见 chunker），不做向量（见 embedder）。

忽略规则（都是硬编码，不暴露给用户，免得配置项爆炸）：

- 隐藏文件/目录（`.` 开头）
- 编辑器临时文件：`~$*`、`*.tmp`、`*.swp`、`*.bak`
- 扩展名只收 `.md` / `.txt`
- 单文件超过 `max_file_mb` 跳过
"""

from __future__ import annotations

import hashlib
import os
from dataclasses import dataclass, field
from pathlib import Path

# 只收这两种；要加 pdf/docx 得先加解析库，见 RAG_PLAN.md §9
TEXT_EXTS = (".md", ".txt")
# 目录递归深度上限（防止有人把整个盘丢进来）
MAX_DEPTH = 6
# 扫描到的文件数上限，超过就不扫了（保护）
MAX_FILES = 5000


@dataclass
class ScanResult:
    """一次扫描的结果。`skipped` 里放「为什么没进索引」，UI 要能看见。"""

    root: Path
    files: dict[str, tuple[int, int]] = field(default_factory=dict)   # rel → (size, mtime_ns)
    skipped: list[dict] = field(default_factory=list)

    def add_skip(self, rel: str, reason: str) -> None:
        self.skipped.append({"rel": rel, "reason": reason})


def scan(root: Path, max_file_mb: int = 2) -> ScanResult:
    """递归扫目录，只 stat 不读内容。路径统一成 POSIX 相对串。"""
    result = ScanResult(root=root)
    if not root.is_dir():
        return result

    limit = max(1, int(max_file_mb)) * 1024 * 1024
    base_depth = len(root.parts)

    for current, dirs, names in os.walk(root):
        depth = len(Path(current).parts) - base_depth
        # 隐藏目录 / 太深 / 太多文件：就地剪枝
        dirs[:] = sorted(
            name
            for name in dirs
            if not name.startswith(".") and depth < MAX_DEPTH
        )
        for name in sorted(names):
            if name.startswith(".") or name.startswith("~$"):
                continue
            path = Path(current) / name
            rel = path.relative_to(root).as_posix()
            suffix = path.suffix.lower()
            if suffix not in TEXT_EXTS:
                result.add_skip(rel, "unsupported_ext")
                continue
            if name.endswith((".tmp", ".swp", ".bak")):
                result.add_skip(rel, "temp_file")
                continue
            try:
                stat = path.stat()
            except OSError:
                result.add_skip(rel, "stat_failed")
                continue
            if stat.st_size > limit:
                result.add_skip(rel, "too_large")
                continue
            result.files[rel] = (stat.st_size, stat.st_mtime_ns)
            if len(result.files) >= MAX_FILES:
                return result
    return result


def read_text(root: Path, rel: str) -> str | None:
    """读一份文本；读不到（占用/编码异常）返回 None，由调用方记 skipped。"""
    path = root / rel
    try:
        raw = path.read_bytes()
    except OSError:
        return None
    for encoding in ("utf-8-sig", "utf-8", "gb18030"):
        try:
            return raw.decode(encoding)
        except UnicodeDecodeError:
            continue
    return raw.decode("utf-8", "replace")


def sha256_file(path: Path) -> str:
    """整个文件的 sha256（和台账里记的是同一个口径）；读不到返回空串。"""
    digest = hashlib.sha256()
    try:
        with open(path, "rb") as handle:
            for block in iter(lambda: handle.read(1 << 16), b""):
                digest.update(block)
    except OSError:
        return ""
    return digest.hexdigest()

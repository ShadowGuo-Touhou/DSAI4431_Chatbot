"""Embedding 后端：现在只有 Ollama（`POST /api/embed`）。

为什么不引 requests/httpx：只用 `urllib` 就够了，少一个依赖。
为什么不把向量算在进程内：sentence-transformers 要拖 2~3 GB 的 torch，
为了课程项目不值得；Ollama 是现成的本地 HTTP 服务，模型可换。

⚠ 没有 Ollama 时**任何**索引都建立不起来（会抛 `EmbedError`），
上层必须把它当成「这次不能用 RAG」，而不是让程序崩掉。

调试用：环境变量 `DSAI_RAG_EMBED=debug` 时改用 `DebugEmbedder`（字符哈希向量，
**语义无意义**，只用来在没有 Ollama 的情况下点一遍流程）。
"""

from __future__ import annotations

import hashlib
import json
import os
import urllib.error
import urllib.request

import numpy as np

# 一次请求最多带多少段文本（Ollama 端会自己 batch，这里只是别让请求体太大）
MAX_BATCH = 16
# 建索引时单次请求的超时（秒）。查询走自己那套 timeout，见 retriever
INDEX_TIMEOUT_S = 60.0
# 让 Ollama 把 embedding 模型保活多久（每次请求都会续期；超过这个时长没请求才卸载）。
# 实测不设的话每次请求后都可能卸载：冷启动 22 s、热 0.06 s，
# 而检索超时只有十几秒 → 闲置后第一句必然拿不到知识库。
# 用 "30m" 而不是 -1：常用时够快，长时间不用会把内存还回去。
KEEP_ALIVE = "30m"


class EmbedError(RuntimeError):
    """拿不到向量。`kind` 给上层决定怎么提示用户。"""

    def __init__(self, message: str, *, kind: str = "failed") -> None:
        super().__init__(message)
        self.kind = kind          # "unreachable" / "http" / "bad_response" / "failed"


def make_embedder(cfg, *, timeout_s: float = INDEX_TIMEOUT_S):
    """按配置造一个 embedder。`DSAI_RAG_EMBED=debug` 时走调试后端。"""
    if os.environ.get("DSAI_RAG_EMBED", "").strip().lower() == "debug":
        return DebugEmbedder()
    return OllamaEmbedder(
        base_url=getattr(cfg, "rag_ollama", "") or "http://127.0.0.1:11434",
        model=getattr(cfg, "rag_embedding", "") or "bge-m3",
        timeout_s=timeout_s,
    )


def _normalize(matrix: np.ndarray) -> np.ndarray:
    """L2 归一化：之后点积就是余弦。零向量保底不除零。"""
    norms = np.linalg.norm(matrix, axis=1, keepdims=True)
    norms[norms == 0] = 1.0
    return (matrix / norms).astype(np.float32)


class OllamaEmbedder:
    """Ollama 的 `/api/embed`。每批最多 `MAX_BATCH` 段。"""

    def __init__(self, base_url: str, model: str, timeout_s: float = INDEX_TIMEOUT_S) -> None:
        self.base_url = (base_url or "").strip().rstrip("/")
        self.model = (model or "").strip()
        self.timeout_s = max(1.0, float(timeout_s))
        self.dim = 0

    def endpoint(self) -> str:
        base = self.base_url or "http://127.0.0.1:11434"
        if base.endswith("/api/embed"):
            return base
        return f"{base}/api/embed"

    # --- 对外 ---------------------------------------------------------
    def embed(self, texts: list[str]) -> np.ndarray:
        if not texts:
            return np.zeros((0, max(self.dim, 1)), dtype=np.float32)
        rows: list[list[float]] = []
        for start in range(0, len(texts), MAX_BATCH):
            rows.extend(self._post(texts[start : start + MAX_BATCH]))
        matrix = np.asarray(rows, dtype=np.float32)
        if matrix.ndim != 2:
            raise EmbedError("Ollama 返回的向量维度不对", kind="bad_response")
        self.dim = int(matrix.shape[1])
        return _normalize(matrix)

    def probe(self) -> int:
        """试一次，返回维度；连不上就抛 EmbedError（给状态栏用）。"""
        return int(self.embed(["ping"]).shape[1])

    # --- 内部 ---------------------------------------------------------
    def _post(self, batch: list[str]) -> list[list[float]]:
        payload = json.dumps(
            {"model": self.model, "input": batch, "keep_alive": KEEP_ALIVE},
            ensure_ascii=False,
        ).encode("utf-8")
        request = urllib.request.Request(
            self.endpoint(),
            data=payload,
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        try:
            with urllib.request.urlopen(request, timeout=self.timeout_s) as response:
                body = response.read().decode("utf-8", "replace")
        except urllib.error.HTTPError as exc:
            detail = exc.read().decode("utf-8", "replace")[:200]
            raise EmbedError(
                f"Ollama 返回 HTTP {exc.code}：{detail}", kind="http"
            ) from exc
        except TimeoutError as exc:
            raise EmbedError(
                f"Ollama 超时（{self.timeout_s:.0f}s）", kind="unreachable"
            ) from exc
        except urllib.error.URLError as exc:
            raise EmbedError(
                f"连不上 Ollama（{self.base_url or '127.0.0.1:11434'}）：{exc.reason}",
                kind="unreachable",
            ) from exc

        try:
            data = json.loads(body)
        except ValueError as exc:
            raise EmbedError("Ollama 返回的不是 JSON", kind="bad_response") from exc

        vectors = data.get("embeddings")
        if vectors is None and "embedding" in data:          # 老接口兜底
            vectors = [data["embedding"]]
        if not isinstance(vectors, list) or len(vectors) != len(batch):
            raise EmbedError("Ollama 返回的向量条数对不上", kind="bad_response")
        return vectors


class DebugEmbedder:
    """调试用：字符三元组哈希 → 固定维度向量。

    只保证「同样的文本得到同样的向量」，**没有语义**；检索结果不可用，
    仅供在没有 Ollama 时把「扫描 → 切片 → 落盘 → 检索 → 注入」整条链路走通。
    """

    def __init__(self, dim: int = 256) -> None:
        self.dim = dim

    def embed(self, texts: list[str]) -> np.ndarray:
        matrix = np.zeros((len(texts), self.dim), dtype=np.float32)
        for row, text in enumerate(texts):
            for index in range(max(1, len(text) - 2)):
                gram = text[index : index + 3]
                digest = hashlib.md5(gram.encode("utf-8")).digest()
                bucket = int.from_bytes(digest[:4], "little") % self.dim
                matrix[row, bucket] += 1.0 if digest[4] % 2 else -1.0
        return _normalize(matrix)

    def probe(self) -> int:
        return self.dim

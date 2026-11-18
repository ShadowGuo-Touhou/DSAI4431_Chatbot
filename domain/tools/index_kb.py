"""把 domain/kb/docs 同步进 repo/asset/RAG，并建/更新向量索引，最后跑几条中文探针。

用法：
    python domain/tools/index_kb.py               # 拷贝 + 建索引 + 探针
    python domain/tools/index_kb.py --no-probe    # 只建索引
    python domain/tools/index_kb.py --probe-only  # 只跑探针（索引已存在时）
"""

from __future__ import annotations

import argparse
import shutil
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]          # domain/
DOCS = ROOT / "kb" / "docs"
REPO = ROOT.parent          # <repo>
sys.path.insert(0, str(REPO / "src"))

from dsai4431_chatbot.core.gui import ollama_launcher          # noqa: E402
from dsai4431_chatbot.core.gui import chat_config               # noqa: E402
from dsai4431_chatbot.core.rag import indexer, paths, retriever, store  # noqa: E402

QUERIES = [
    "VLS-2 能装多大的导弹？",
    "Ocello 级巡洋舰多少点数，装甲多厚？",
    "近防 PDT 能拦什么目标？",
    "导弹的制导方式有哪几种？",
    "什么是 MMT？",
    "Keystone 驱逐舰的信号半径是多少？",
    "为什么导弹打完之后这艘船就没用了",
    "fleet 里一艘船 3000 点是什么概念",
]


def install_docs() -> int:
    target = REPO / "asset" / "RAG"
    target.mkdir(parents=True, exist_ok=True)
    for old in target.rglob("*.md"):
        old.unlink()
    count = 0
    for src in sorted(DOCS.rglob("*.md")):
        rel = src.relative_to(DOCS)
        dst = target / rel
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, dst)
        count += 1
    return count


def probe(cfg, limit: int = 3) -> None:
    index = store.load(paths.index_dir())
    if index is None or len(index) == 0:
        print("索引是空的，先建索引")
        return
    print(f"\n索引：{len(index)} 块，向量维度 {index.vectors.shape[1] if index.vectors is not None else '?'}")
    for query in QUERIES:
        started = time.perf_counter()
        got = retriever.search(query, index, cfg)
        cost = (time.perf_counter() - started) * 1000
        print(f"\nQ: {query}   （{cost:.0f} ms, {len(got.hits)} 命中{', ' + got.error if got.error else ''}）")
        for hit in got.hits[:limit]:
            head = hit.text.split("\n")[0][:40]
            print(f"   {hit.score:.3f}  {hit.source}  [{hit.heading}]  {head}")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--no-probe", action="store_true")
    parser.add_argument("--probe-only", action="store_true")
    parser.add_argument("--no-start", action="store_true", help="不拉起 Ollama，假设已经在跑")
    args = parser.parse_args(argv)

    cfg = chat_config.load()

    if not args.probe_only:
        copied = install_docs()
        print(f"拷贝 {copied} 份文档到 {REPO / 'asset' / 'RAG'}")

        if not args.no_start and not ollama_launcher.is_alive(ollama_launcher.base_url(cfg)):
            result = ollama_launcher.ensure_running(cfg)
            print(f"Ollama：ok={result.ok} started={result.started} detail={result.detail} exe={result.exe}")

        last = {"done": 0}

        def progress(done: int, total: int, rel: str) -> None:
            if done == total or done - last["done"] >= 25:
                last["done"] = done
                print(f"  切块 {done}/{total}  {rel}", flush=True)

        result = indexer.sync_once(cfg, progress=progress)
        print(
            f"索引：status={result.status} files={result.files} chunks={result.chunks} "
            f"added={result.added} updated={result.updated} removed={result.removed} "
            f"reused={result.reused} embedded={result.embedded} 用时 {result.elapsed_s:.1f}s"
        )
        if result.skipped:
            print(f"  跳过 {len(result.skipped)} 个：{result.skipped[:3]}")
        if result.error:
            print(f"  错误：{result.error}")

    if not args.no_probe:
        probe(cfg)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

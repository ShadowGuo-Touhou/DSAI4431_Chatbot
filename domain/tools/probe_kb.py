"""检索体检：按类别各问几句中文，看命中是不是落在正确的文档上。

    python domain/tools/probe_kb.py           # 全部类别
    python domain/tools/probe_kb.py 模块      # 只跑某一组
"""

from __future__ import annotations

import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "src"))

from dsai4431_chatbot.core.gui import chat_config  # noqa: E402
from dsai4431_chatbot.core.rag import paths, retriever, store  # noqa: E402

GROUPS: dict[str, list[str]] = {
    "舱室": ["游戏里有哪些舱室？", "指挥舱有哪些", "损管舱室有什么不同"],
    "模块": ["有哪些模块可以装", "雷达模块有哪些", "动力模块哪个好"],
    "武器": ["挂载点能装哪些武器", "导弹发射器有哪几种", "近防炮有哪些", "轴炮是什么"],
    "弹药": ["穿甲弹和高爆弹有什么区别", "100mm 有哪些炮弹", "导弹的引导头怎么选"],
    "舰体": ["巡洋舰有哪些", "Ocello 多少点", "护卫舰和驱逐舰差别"],
    "舰载机": ["舰载机有哪些", "拦截机怎么用"],
    "地图": ["有哪些地图", "AE-10 这张图多大"],
    "机制": ["装甲是怎么算的", "电子战怎么工作", "软杀是什么", "什么是 MMT"],
}


def main() -> int:
    only = sys.argv[1] if len(sys.argv) > 1 else ""
    cfg = chat_config.load()
    index = store.load(paths.index_dir())
    print(f"index: {len(index.chunks)} chunks, dim {index.vectors.shape[1]}")
    for group, queries in GROUPS.items():
        if only and only not in group:
            continue
        print(f"\n### {group}")
        for q in queries:
            hits = retriever.search(q, index, cfg)
            top = hits.hits[:3]
            head = " | ".join(f"{h.score:.3f} {h.source}" for h in top) or f"err={hits.error!r}"
            print(f"  Q {q}\n    {head}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

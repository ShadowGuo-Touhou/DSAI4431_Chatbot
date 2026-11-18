"""Ad-hoc retrieval probe.

    python probe_one.py "query1" "query2" ...
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "src"))

from dsai4431_chatbot.core.gui import chat_config as cc  # noqa: E402
from dsai4431_chatbot.core.rag import paths as rag_paths  # noqa: E402
from dsai4431_chatbot.core.rag import retriever, store  # noqa: E402

cfg = cc.load()
index = store.load(rag_paths.index_dir())
print(f"索引：{len(index.chunks)} 块，向量维度 {index.vectors.shape[1]}")

for query in sys.argv[1:]:
    result = retriever.search(query, index, cfg)
    print(f"\n[{result.elapsed_ms:.0f} ms] {query}")
    for hit in result.hits[:4]:
        print(f"  {hit.score:.3f}  {hit.source} [{hit.heading}]")

"""One-off: raise the RAG injection budget so whole catalog tables survive injection."""

import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2] / "repo"
sys.path.insert(0, str(REPO / "src"))

from dsai4431_chatbot.core.gui import chat_config  # noqa: E402

cfg = chat_config.load()
print("before:", cfg.rag_inject_chars, "top_k:", cfg.rag_top_k)
cfg.rag_inject_chars = int(sys.argv[1] if len(sys.argv) > 1 else 6000)
chat_config.save(cfg)
print("after :", chat_config.load().rag_inject_chars)

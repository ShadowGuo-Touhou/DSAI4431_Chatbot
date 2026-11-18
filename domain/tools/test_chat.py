"""端到端测试：真的走一遍「模型 → search_knowledge → 用资料回答」。

用法：
    python domain/tools/test_chat.py "VLS-2 能装多大的导弹？"
    python domain/tools/test_chat.py --no-tools "你好呀"
"""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]          # domain/
REPO = ROOT.parent          # <repo>
sys.path.insert(0, str(REPO / "src"))

from PySide6.QtCore import QCoreApplication, QTimer                     # noqa: E402

from dsai4431_chatbot.core.gui import chat_config, chat_client, tool_router  # noqa: E402
from dsai4431_chatbot.core.rag import paths, retriever, store            # noqa: E402

# 与主程序 `_tools_for()` 保持一致：检索 + 生成舰队文件两个工具一起发
TOOLS = [tool_router.TOOL_SPEC, tool_router.FLEET_TOOL_SPEC]


class RagShim:
    """ToolRouter 只用到 rag.search(query)。"""

    def __init__(self, cfg) -> None:
        self.cfg = cfg
        self.index = store.load(paths.index_dir())

    def search(self, query: str):
        got = retriever.search(query, self.index, self.cfg)
        return got          # ToolRouter 读的是 result.hits / result.error


def main(argv: list[str]) -> int:
    log_path = None
    if "--log" in argv:
        i = argv.index("--log")
        try:
            log_path = argv[i + 1]
        except IndexError:
            log_path = None
        argv = argv[:i] + argv[i + 2 :]
    if not argv or argv[0].startswith("--"):
        question = "VLS-2 能装多大的导弹？"
        use_tools = "--no-tools" not in argv
    else:
        question = argv[0]
        use_tools = "--no-tools" not in argv

    app = QCoreApplication(sys.argv[:1])
    cfg = chat_config.load()
    ready, why = cfg.ready()
    print(f"endpoint={cfg.endpoint()} model={cfg.model} ready={ready} {why}")

    rag = RagShim(cfg)
    # 与主程序对齐：应用启动时会预热向量模型，这里先空跑一次，
    # 否则冷启动的首次检索会撞上 rag_timeout_ms（8s）而误报「没有命中」。
    try:
        rag.search("预热")
    except Exception as exc:  # noqa: BLE001 - 预热失败不该挡住测试
        print(f"[warmup] 失败：{exc!r}")
    router = tool_router.ToolRouter(rag)
    client = chat_client.ChatClient()
    messages = [
        {"role": "system", "content": cfg.system_prompt() + (tool_router.PROTOCOL_HINT if use_tools else "")},
        {"role": "user", "content": question},
    ]
    state = {"rounds": 0, "answer": ""}

    def write_log() -> None:
        if not log_path:
            return
        try:
            path = Path(log_path)
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(
                f"# {question}\n\nmodel={cfg.model}\n\n## 回答\n\n{state['answer']}\n",
                encoding="utf-8",
            )
        except OSError as exc:  # noqa: BLE001 - 日志写不了不该影响测试
            print(f"[log] 写入失败：{exc!r}")

    def on_tool_calls(calls: list) -> None:
        print(f"\n[tool] 模型要求检索：{calls}")
        if state["rounds"] >= tool_router.MAX_ROUNDS:
            # 与主程序一致：轮次用完后再逼一次「不许再查」的收尾请求
            print("[tool] 轮次用完，强制收尾")
            messages.append(
                {
                    "role": "system",
                    "content": "检索次数已用完，请立刻基于已有资料回答；资料不足就直说。",
                }
            )
            client.send(chat_config.load(), messages, model=cfg.model, tools=None)
            return
        messages.append(tool_router.assistant_message(calls, client.last_reasoning()))
        for call in calls:
            outcome = router.run(
                call,
                min_score=float(getattr(cfg, "rag_tool_min_score", 0.5)),
                max_chars=int(getattr(cfg, "rag_inject_chars", 3000) or 3000),
            )
            print(f"[tool] {outcome.summary()}")
            print(f"[tool] 注入 {len(outcome.content)} 字：")
            for line in outcome.content.splitlines()[:8]:
                print("   |", line[:110])
            messages.append(
                {
                    "role": "tool",
                    "tool_call_id": outcome.call_id or "",
                    "content": outcome.content,
                }
            )
        state["rounds"] += 1
        exhausted = state["rounds"] >= tool_router.MAX_ROUNDS
        client.send(
            chat_config.load(),
            messages,
            model=cfg.model,
            tools=None if exhausted else TOOLS,
        )

    def on_delta(text: str) -> None:
        state["answer"] += text

    def on_finish(text: str) -> None:
        print(f"\n=== 答案（{len(state['answer'])} 字）===\n{state['answer'] or text}")
        write_log()
        app.quit()

    def on_fail(reason: str) -> None:
        print(f"\n!!! 失败：{reason}")
        write_log()
        app.quit()

    client.tool_calls.connect(on_tool_calls)
    client.delta.connect(on_delta)
    client.finished_ok.connect(on_finish)
    client.failed.connect(on_fail)

    if not client.send(cfg, messages, model=cfg.model, tools=TOOLS if use_tools else None):
        print("发送失败")
        return 1
    QTimer.singleShot(120_000, app.quit)
    return app.exec()


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))

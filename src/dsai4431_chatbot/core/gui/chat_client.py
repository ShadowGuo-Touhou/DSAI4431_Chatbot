"""对话客户端：OpenAI 兼容的 `/chat/completions`，流式（SSE）。

用 Qt 自带的 `QNetworkAccessManager`，不引第三方 HTTP 库 —— 它是事件驱动的，
不需要另外开线程，也不会卡住界面。

流式协议（DeepSeek / OpenAI / 各种兼容网关都一样）：

    data: {"choices":[{"delta":{"content":"你"}}]}
    data: {"choices":[{"delta":{"content":"好"}}]}
    data: [DONE]

三种收尾情况都处理了：
1. 正常流式 —— 边收边发 `delta`，结束时 `finished_ok`
2. 网关不支持流式（直接回一整包 JSON）—— 在 finished 里整体解析，补发一次 delta
3. 出错 —— HTTP 状态码 + 服务端返回的 error.message 一起给出来，发 `failed`
"""

from __future__ import annotations

import json
import re

from PySide6.QtCore import QByteArray, QObject, QUrl, Signal
from PySide6.QtNetwork import QNetworkAccessManager, QNetworkReply, QNetworkRequest

from dsai4431_chatbot.core.gui import chat_config, personas

# 单次请求的超时（毫秒）。流式下这里指"这么久一个字节都没有就断"，
# 不是总时长；DeepSeek 偶尔首字节慢，给足 120 秒。
TRANSFER_TIMEOUT = 120_000
# 出错时把服务端响应体截这么长，足够看出是哪一步挂了
BODY_SNIPPET = 400

# --- DSML（DeepSeek 内部工具调用标记）-----------------------------------
# 有时模型不通过 tool_calls 通道，而是把调用写进正文，形如：
#   <｜｜DSML｜｜ calls>
#   <｜｜DSML｜｜ invoke name="search_knowledge">
#   <｜｜DSML｜｜ parameter name="query" string="true">租房</｜｜DSML｜｜ parameter>
#   </｜｜DSML｜｜ invoke>
#   </｜｜DSML｜｜ calls>
# 竖线是全角 U+FF5C（也兼容半角 |）。这种情况不能直接显示给用户，
# 要**识别出来、还原成一次真正的工具调用**，否则用户只会看到一堆噪声。
_DSML_PIPE = r"[|｜]{1,2}"
_DSML_START = re.compile(rf"<\s*{_DSML_PIPE}\s*DSML\s*{_DSML_PIPE}\s*calls\s*>", re.I)
_DSML_ANY = re.compile(rf"<\s*/?\s*{_DSML_PIPE}\s*DSML\s*{_DSML_PIPE}\s*(\w+)", re.I)
_DSML_END = re.compile(rf"<\s*/\s*{_DSML_PIPE}\s*DSML\s*{_DSML_PIPE}\s*calls\s*>", re.I)
_DSML_INVOKE = re.compile(
    rf"<\s*{_DSML_PIPE}\s*DSML\s*{_DSML_PIPE}\s*invoke\s+name=\"([^\"]+)\"\s*>(.*?)"
    rf"<\s*/\s*{_DSML_PIPE}\s*DSML\s*{_DSML_PIPE}\s*invoke\s*>",
    re.S | re.I,
)
_DSML_PARAM = re.compile(
    rf"<\s*{_DSML_PIPE}\s*DSML\s*{_DSML_PIPE}\s*parameter\s+name=\"([^\"]+)\"[^>]*>(.*?)"
    rf"<\s*/\s*{_DSML_PIPE}\s*DSML\s*{_DSML_PIPE}\s*parameter\s*>",
    re.S | re.I,
)
_DSML_CANON = ("<||DSML||calls>", "<｜｜DSML｜｜calls>", "<|DSML|calls>", "<｜DSML｜calls>")


def _dsml_progress(text: str) -> bool:
    """`text` 是不是「标记还没写完」的前缀（要扣住，先别显示）。"""
    compact = re.sub(r"\s+", "", text.lstrip())
    if not compact:
        return False
    for canon in _DSML_CANON:
        if len(compact) < len(canon) and canon.startswith(compact):
            return True
    return False


def _progress_suffix(text: str) -> str:
    """结尾那段还没写完的标记前缀（普通文本会返回空串）。"""
    limit = min(len(text), 16)
    for cut in range(len(text) - limit, len(text)):
        tail = text[cut:]
        if tail.startswith("<") and _dsml_progress(tail):
            return tail
    return ""


def parse_dsml_calls(text: str) -> list[dict]:
    """从正文里抠出 DSML 形式的工具调用；解析不出来就返回空列表。"""
    calls: list[dict] = []
    for block in _DSML_START.split(text)[1:]:
        body = _DSML_END.split(block)[0]
        for index, match in enumerate(_DSML_INVOKE.finditer(body)):
            name = match.group(1)
            params: dict[str, str] = {}
            for param in _DSML_PARAM.finditer(match.group(2)):
                params[param.group(1)] = param.group(2).strip()
            calls.append(
                {
                    "id": f"dsml_{len(calls)}_{index}",
                    "name": name,
                    "arguments": json.dumps(params, ensure_ascii=False),
                }
            )
    return calls


def strip_dsml(text: str) -> str:
    """把正文里的 DSML 段落整段删掉（invoke / parameter / 包裹标签都不留）。"""
    cleaned = _DSML_INVOKE.sub("", text)
    cleaned = re.sub(
        rf"<\s*/?\s*{_DSML_PIPE}\s*DSML\s*{_DSML_PIPE}\s*\w+[^>]*>", "", cleaned
    )
    return cleaned.strip()


def _partial_marker_tail(text: str) -> str:
    """兼容旧名：结尾那段「可能是标记开头」的字符。"""
    return _progress_suffix(text)



class ChatClient(QObject):
    """一次一把：正在回复时再 send 会返回 False（调用方负责提示）。"""

    delta = Signal(str)            # 增量文本
    reasoning_delta = Signal(str)  # 增量思考链（思考模式下才有）
    finished_ok = Signal(str)      # 完整文本
    failed = Signal(str)           # 人话版的错误
    # 模型要求调用工具：list[{"id","name","arguments"}]；来了这个就不再发 finished_ok
    tool_calls = Signal(list)

    def __init__(self, parent=None):
        super().__init__(parent)
        self._nam = QNetworkAccessManager(self)
        self._reply: QNetworkReply | None = None
        self._buffer = ""          # 还没凑成整行的 SSE 残留
        self._raw_text = ""        # 收到的全部原始文本（出错时要从里面抠错误信息）
        self._text = ""            # 已经收到的完整回复文本
        self._reasoning = ""       # 已经收到的思考链（reasoner 才有）
        self._got_delta = False
        self._server_error = ""    # 服务端在流里塞的 error
        self._aborted = False
        self._usage: dict = {}     # 最后一次响应里的 usage（流式要有才给）
        self._tool_calls: dict[int, dict] = {}   # index → {id,name,arguments}
        self._finish_reason = ""
        # DSML 防御：扣住可能的半截标记、收集整段标记（见 parse_dsml_calls）
        self._hold = ""
        self._dsml_mode = False
        self._dsml_buf = ""

    # --- 状态 -----------------------------------------------------------
    def busy(self) -> bool:
        return self._reply is not None

    def last_usage(self) -> dict:
        """最近一次请求的 token 用量；网关没给就是空字典。"""
        return dict(self._usage)

    def last_reasoning(self) -> str:
        """最近一次回复的思考链（reasoner 才有；chat 模型是空串）。"""
        return self._reasoning

    # --- 发请求 ---------------------------------------------------------
    def send(
        self,
        cfg,
        messages: list[dict],
        model: str | None = None,
        tools: list[dict] | None = None,
    ) -> bool:
        """cfg 是 chat_config.ChatConfig；messages 是 OpenAI 格式的对话数组。

        `model` 可以覆盖 cfg.model —— 每个会话自己记着用哪个模型。
        `tools` 给了就在 payload 里声明工具（OpenAI 格式），并让模型自己决定用不用。
        """
        if self._reply is not None:
            return False
        ok, reason = cfg.ready()
        if not ok:
            self.failed.emit(reason)
            return False

        payload = {
            # 旧会话文件里可能还存着 deepseek-chat 这种已经下线的名字，发之前归一
            "model": personas.normalize_model(model or cfg.model)
            or chat_config.DEFAULT_MODEL,
            "messages": messages,
            "stream": True,
        }
        if tools:
            payload["tools"] = tools
            payload["tool_choice"] = "auto"
        request = QNetworkRequest(QUrl(cfg.endpoint()))
        request.setHeader(
            QNetworkRequest.KnownHeaders.ContentTypeHeader, "application/json"
        )
        request.setRawHeader(b"Authorization", f"Bearer {cfg.api_key.strip()}".encode())
        request.setRawHeader(b"Accept", b"text/event-stream")
        request.setTransferTimeout(TRANSFER_TIMEOUT)
        request.setAttribute(
            QNetworkRequest.Attribute.RedirectPolicyAttribute,
            QNetworkRequest.RedirectPolicy.NoLessSafeRedirectPolicy,
        )

        self._buffer = ""
        self._raw_text = ""
        self._text = ""
        self._reasoning = ""
        self._got_delta = False
        self._server_error = ""
        self._aborted = False
        self._usage = {}
        self._tool_calls = {}
        self._finish_reason = ""
        self._hold = ""
        self._dsml_mode = False
        self._dsml_buf = ""

        body = QByteArray(json.dumps(payload, ensure_ascii=False).encode("utf-8"))
        self._reply = self._nam.post(request, body)
        self._reply.readyRead.connect(self._on_ready)
        self._reply.finished.connect(self._on_finished)
        return True

    def abort(self) -> None:
        """用户中途取消：保留已经收到的内容。"""
        reply = self._reply
        if reply is None:
            return
        self._aborted = True
        reply.abort()

    # --- 收数据 ---------------------------------------------------------
    def _on_ready(self) -> None:
        reply = self._reply
        if reply is None:
            return
        raw = bytes(reply.readAll().data())
        if not raw:
            return
        text = raw.decode("utf-8", "replace")
        # 一份留底：HTTP 4xx 的响应体没有 "data:" 前缀，会在下面被丢掉，
        # 但出错时正是要靠它给出「到底为什么被拒」
        self._raw_text += text
        # SSE 是逐行的；按 "\n" 切，最后不完整的一段留在 buffer 里
        self._buffer += text
        while "\n" in self._buffer:
            line, self._buffer = self._buffer.split("\n", 1)
            self._handle_line(line.strip())

    def _handle_line(self, line: str) -> None:
        if not line or line.startswith(":") or line.startswith("event:"):
            return                      # 空行 / 心跳 / 事件名，都不用管
        if not line.startswith("data:"):
            return
        data = line[len("data:"):].strip()
        if not data or data == "[DONE]":
            return
        try:
            payload = json.loads(data)
        except ValueError:
            return                      # 半截 JSON（极少见）：丢掉这一行
        self._consume(payload)

    def _consume(self, payload: dict) -> None:
        """吃一个 data JSON：可能是增量、可能是错误、也可能是一整条回复。"""
        usage = payload.get("usage")
        if isinstance(usage, dict) and usage:
            self._usage = usage

        error = payload.get("error")
        if error:
            self._server_error = _error_text(error)
            return

        choices = payload.get("choices") or []
        if not choices:
            return
        choice = choices[0] or {}
        delta = choice.get("delta") or {}

        if choice.get("finish_reason"):
            self._finish_reason = str(choice["finish_reason"])

        # 工具调用：流式下按 index 拼（第一片带 id + 函数名，之后只带 arguments 碎片；
        # 实测 DeepSeek 的 arguments 会被切成十几个小片，必须一路相加）
        pieces = delta.get("tool_calls") or (choice.get("message") or {}).get("tool_calls") or []
        for entry in pieces:
            if not isinstance(entry, dict):
                continue
            try:
                index = int(entry.get("index", 0) or 0)
            except (TypeError, ValueError):
                index = 0
            slot = self._tool_calls.setdefault(
                index, {"id": "", "name": "", "arguments": ""}
            )
            if entry.get("id"):
                slot["id"] = str(entry["id"])
            function = entry.get("function") or {}
            if function.get("name"):
                slot["name"] = str(function["name"])
            if function.get("arguments"):
                slot["arguments"] += str(function["arguments"])

        # 思考链先到（reasoner）：单独发，别和正文混在一起
        think = delta.get("reasoning_content") or (choice.get("message") or {}).get(
            "reasoning_content"
        )
        if think:
            self._reasoning += str(think)
            self.reasoning_delta.emit(str(think))

        piece = delta.get("content")
        if not piece:
            # 非流式网关：整条消息放在 message.content 里
            piece = (choice.get("message") or {}).get("content")
        if not piece:
            return
        self._feed_text(str(piece))

    # --- 正文：DSML 过滤 + 流式输出 -------------------------------------
    def _feed_text(self, piece: str) -> None:
        """吃一段正文：普通文字立刻发出去；DSML 标记扣下来，不让用户看到。"""
        self._hold += piece
        while self._hold:
            if self._dsml_mode:
                end = _DSML_END.search(self._hold)
                if end is None:
                    self._dsml_buf += self._hold
                    self._hold = ""
                    return
                self._dsml_buf += self._hold[: end.end()]
                self._hold = self._hold[end.end():]
                self._dsml_mode = False
                continue

            start = _DSML_START.search(self._hold)
            if start is not None:
                if start.start() > 0:
                    self._emit_visible(self._hold[: start.start()])
                self._dsml_buf += self._hold[start.start():]
                self._hold = ""
                self._dsml_mode = True
                continue

            tail = _partial_marker_tail(self._hold)
            if tail:
                safe = self._hold[: len(self._hold) - len(tail)]
                self._hold = tail
                self._emit_visible(safe)
                return
            safe, self._hold = self._hold, ""
            self._emit_visible(safe)
            return

    def _emit_visible(self, text: str) -> None:
        if not text:
            return
        self._got_delta = True
        self._text += text
        self.delta.emit(text)

    # --- 收尾 -----------------------------------------------------------
    def _on_finished(self) -> None:
        reply, self._reply = self._reply, None
        if reply is None:
            return
        reply.deleteLater()

        tail = bytes(reply.readAll().data()).decode("utf-8", "replace")
        if tail:
            self._raw_text += tail
        body = self._raw_text.strip()
        status = reply.attribute(
            QNetworkRequest.Attribute.HttpStatusCodeAttribute
        )

        # 没收到任何增量时，看看整包是不是一整条回复（非流式兜底）
        if not self._got_delta and body and not body.startswith("data:"):
            text = _extract_full_text(body)
            if text:
                self._feed_text(text)

        if self._aborted:
            self.finished_ok.emit(self._text)
            return

        # 收尾：先放出被扣住的普通文字，再把 DSML 段落还原成真正的工具调用
        if self._hold and not self._dsml_mode:
            self._emit_visible(self._hold)
        self._hold = ""
        self._dsml_mode = False
        if self._dsml_buf:
            pending = self._dsml_buf
            self._dsml_buf = ""
            parsed = parse_dsml_calls(pending)
            if parsed:
                print(f"[rag] 模型用正文写了工具调用，已还原：{[c['name'] for c in parsed]}",
                      flush=True)
                for offset, call in enumerate(parsed):
                    self._tool_calls[9000 + offset] = call
            elif not self._text:
                self.failed.emit(
                    "模型返回了一段无法解析的工具调用标记，这一轮没有结果，请再发一次。"
                )
                return

        # 模型要调工具：这一轮没有正文，交给上层去执行工具、然后再发一次请求
        if self._tool_calls:
            calls = [
                self._tool_calls[i]
                for i in sorted(self._tool_calls)
                if self._tool_calls[i].get("name")
            ]
            self._tool_calls = {}
            if calls:
                self.tool_calls.emit(calls)
                return

        if self._server_error and not self._text:
            self.failed.emit(self._server_error)
            return

        if self._text:
            # 有内容就先把内容给用户，状态码异常不覆盖已经生成的部分
            self.finished_ok.emit(self._text)
            return

        # 一个字都没有：拼一条能定位问题的错误
        detail = self._server_error or _error_text_from_body(body)
        if not detail:
            detail = reply.errorString() or "未知错误"
        prefix = f"HTTP {status} · " if status else ""
        self.failed.emit(f"{prefix}{detail}")


# ---------------------------------------------------------------------------
# 小工具
# ---------------------------------------------------------------------------
def _error_text(error) -> str:
    """把服务端的 error 字段变成一句人话。"""
    if isinstance(error, dict):
        msg = error.get("message") or error.get("code") or ""
        return str(msg).strip() or json.dumps(error, ensure_ascii=False)[:BODY_SNIPPET]
    return str(error).strip()


def _error_text_from_body(body: str) -> str:
    """从一整包响应体里抠错误信息（HTTP 4xx/5xx 常见）。"""
    if not body:
        return ""
    try:
        payload = json.loads(body)
    except ValueError:
        return body[:BODY_SNIPPET]
    if isinstance(payload, dict):
        if payload.get("error"):
            return _error_text(payload["error"])
        if payload.get("message"):
            return str(payload["message"])[:BODY_SNIPPET]
    return body[:BODY_SNIPPET]


def _extract_full_text(body: str) -> str:
    """非流式响应：直接拿 choices[0].message.content。"""
    try:
        payload = json.loads(body)
    except ValueError:
        return ""
    if not isinstance(payload, dict):
        return ""
    choices = payload.get("choices") or []
    if not choices:
        return ""
    return str((choices[0].get("message") or {}).get("content") or "")

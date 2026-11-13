"""附件：图片和纯文本。

只支持这两类，因为 **DeepSeek API 也只吃这两类**（2026-11 文档）：

- **图片**（JPEG / PNG / GIF / WebP，按文件内容判断）：只有 `deepseek-flash`
  支持。要放进 **user 消息**的 content 块数组：

      {"type": "image_url", "image_url": {"url": "data:image/png;base64,..."}}

  放进 system / assistant 消息会直接 400。
- **纯文本**：就是普通字符串，拼进 content 即可。
- **PDF / DOCX / XLSX**：API 完全不认，只能自己提文本 —— 所以文件选择框
  里直接把它们过滤掉，别让人选到再报错。

几个 API 侧的硬限制（写在这里免得散落各处）：

- 请求体 48 MiB；单张内联图片 32 MiB
- 每张图最多占 1024 token（大图会被缩到约 1300×1300）
- 图片只会出现在 user 消息里，所以「带图的历史消息」每轮都会重发、重复计费

`build_content()` 负责把正文 + 附件拼成 API 要的形状：
有图片就返回块数组，只有文本就还是普通字符串（这点很关键 —— 无附件时
保持原格式，避免把简单的请求也复杂化）。
"""

from __future__ import annotations

import base64
from dataclasses import dataclass, field
from pathlib import Path

# 图片：API 认这四种
IMAGE_SUFFIXES = {".png", ".jpg", ".jpeg", ".gif", ".webp"}
# 纯文本：能直接读成字符串的都算
TEXT_SUFFIXES = {
    ".md", ".markdown", ".txt", ".text", ".log",
    ".py", ".js", ".ts", ".tsx", ".jsx",
    ".json", ".jsonl", ".yaml", ".yml", ".toml", ".ini", ".cfg",
    ".csv", ".tsv", ".xml", ".html", ".htm", ".css", ".scss",
    ".c", ".h", ".cpp", ".hpp", ".cs", ".java", ".go", ".rs",
    ".sh", ".bat", ".ps1", ".sql", ".tex",
}

# 单张图片上限（API 是 32 MiB，这里留点余量）
MAX_IMAGE_BYTES = 30 * 1024 * 1024
# 单个文本附件上限：再大就不该塞进 prompt 了（会吃掉几万 token）
MAX_TEXT_BYTES = 200 * 1024
# 一次最多带几个附件
MAX_ATTACHMENTS = 8

MIME_BY_SUFFIX = {
    ".png": "image/png",
    ".jpg": "image/jpeg",
    ".jpeg": "image/jpeg",
    ".gif": "image/gif",
    ".webp": "image/webp",
}


@dataclass
class Attachment:
    """一个已经读进内存、可以发给模型的附件。"""

    path: Path
    name: str
    kind: str                       # "image" | "text"
    size: int = 0
    data_url: str = ""              # 图片：data:image/png;base64,...
    text: str = ""                  # 文本：文件内容
    error: str = ""                 # 有错时非空（不抛异常，界面直接显示）

    @property
    def ok(self) -> bool:
        return not self.error


def is_image(path: Path) -> bool:
    return path.suffix.lower() in IMAGE_SUFFIXES


def is_text(path: Path) -> bool:
    return path.suffix.lower() in TEXT_SUFFIXES


def supported(path: Path) -> bool:
    return is_image(path) or is_text(path)


def load(path: Path) -> Attachment:
    """读一个文件成附件。**任何问题都写进 `error`，不抛异常。**

    抛异常会让调用方为了一个选错的文件写一堆 try —— 界面也只是要一句提示。
    """
    path = Path(path)
    name = path.name
    try:
        size = path.stat().st_size
    except OSError as exc:
        return Attachment(path=path, name=name, kind="", error=f"读不到文件：{exc}")

    if is_image(path):
        if size > MAX_IMAGE_BYTES:
            return Attachment(
                path=path, name=name, kind="image", size=size,
                error=f"图片太大（{size / 1048576:.1f} MB，上限 {MAX_IMAGE_BYTES // 1048576} MB）",
            )
        try:
            raw = path.read_bytes()
        except OSError as exc:
            return Attachment(path=path, name=name, kind="image", size=size,
                              error=f"读不到文件：{exc}")
        mime = MIME_BY_SUFFIX.get(path.suffix.lower(), "image/png")
        encoded = base64.b64encode(raw).decode("ascii")
        return Attachment(
            path=path, name=name, kind="image", size=size,
            data_url=f"data:{mime};base64,{encoded}",
        )

    if is_text(path):
        if size > MAX_TEXT_BYTES:
            return Attachment(
                path=path, name=name, kind="text", size=size,
                error=f"文本太大（{size / 1024:.0f} KB，上限 {MAX_TEXT_BYTES // 1024} KB）",
            )
        try:
            text = path.read_text(encoding="utf-8", errors="replace")
        except OSError as exc:
            return Attachment(path=path, name=name, kind="text", size=size,
                              error=f"读不到文件：{exc}")
        return Attachment(path=path, name=name, kind="text", size=size, text=text)

    return Attachment(
        path=path, name=name, kind="",
        error="只支持图片（png/jpg/gif/webp）和纯文本文件",
    )


def build_content(text: str, attachments: list[Attachment]) -> str | list[dict]:
    """把正文 + 附件拼成 API 的 content。

    - 没有图片 → 返回**字符串**（和以前完全一样，不破坏简单请求）
    - 有图片 → 返回块数组：文本块 + 每个图片一个 image_url 块

    文本附件以 `<file name="…">…</file>` 包在正文前面 —— 模型能分出
    「这是文件内容」和「这是我说的话」。
    """
    good = [a for a in attachments if a.ok]
    images = [a for a in good if a.kind == "image"]
    texts = [a for a in good if a.kind == "text"]

    body = text or ""
    if texts:
        chunks = [f'<file name="{a.name}">\n{a.text.rstrip()}\n</file>' for a in texts]
        chunks.append(body)
        body = "\n\n".join(part for part in chunks if part.strip())

    if not images:
        return body

    blocks: list[dict] = []
    if body.strip():
        blocks.append({"type": "text", "text": body})
    for image in images:
        blocks.append(
            {"type": "image_url", "image_url": {"url": image.data_url}}
        )
    return blocks


def summary(attachments: list[Attachment]) -> str:
    """给会话文件用的一行摘要（图片的 base64 绝不落盘）。"""
    good = [a for a in attachments if a.ok]
    if not good:
        return ""
    names = "、".join(a.name for a in good)
    return f"[附件 {len(good)} 个：{names}]"


def strip_old_images(messages: list[dict], keep_turns: int = 10) -> list[dict]:
    """历史里只保留最近 `keep_turns` 轮的图片，更早的降级成纯文本。

    为什么：图片在**每次**请求里都会重发，每张最多占 1024 token。聊久了
    前面那些截图会一直计费，而且模型早就不需要再"看"它们了。

    只降级不改内容 —— 文字部分原样留着，模型仍然知道当时说过什么，
    只是不再重复付图片的 token。

    "一轮"按 **user 消息** 数：从最后一条往前数，数到第 `keep_turns` 条
    用户消息为止，再往前的 user 消息里的图片块全部摘掉。
    """
    if keep_turns <= 0 or not messages:
        return messages

    turns = 0
    result: list[dict] = []
    for message in reversed(messages):
        content = message.get("content")
        if message.get("role") == "user":
            turns += 1
            if turns > keep_turns and isinstance(content, list):
                # 降级：只留文本块，拼回一个字符串
                texts = [
                    str(block.get("text", ""))
                    for block in content
                    if isinstance(block, dict) and block.get("type") == "text"
                ]
                stripped = {**message, "content": "\n\n".join(t for t in texts if t)}
                result.append(stripped)
                continue
        result.append(message)

    result.reverse()
    return result


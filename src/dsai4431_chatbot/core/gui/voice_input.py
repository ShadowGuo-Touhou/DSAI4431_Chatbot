"""语音输入：录音（QtMultimedia） + 识别（sherpa-onnx / SenseVoice）。

为什么是这两样（和 DSH 同一套，见 README 的调研记录）：

- 引擎 sherpa-onnx：PySide6 项目本来就重，再加 torch/whisper 不划算；
  sherpa-onnx 是纯 CPU 的 ONNX 推理，Windows 轮子里自带 onnxruntime。
- 模型 SenseVoiceSmall int8（228 MB）：中/英/粤/日/韩，`language="auto"`
  能自己判语言，比 whisper 小一个量级。
- VAD 用 Silero：录完的音里常有大段静音，先切出真正说话的部分再识别，
  短句效果明显更好。

三条约束：

1. **主线程不能碰识别**：模型加载 2.5 s、解码 0.3~3 s，必须在后台线程。
2. **模型只加载一次**：228 MB 反复加载会卡到没法用，做成进程级单例。
3. **录音期间顺便预热**：用户按下麦克风到松手通常有 2~3 秒，正好够把
   模型加载完（`warm_up_background()`），第一次点击不会白等。

模型文件在 `asset/stt/`（`.gitignore` 掉，缺失时由启动加载页下载）。
"""

from __future__ import annotations

import threading
from pathlib import Path

import numpy as np
from PySide6.QtCore import QIODevice, QObject, Signal
from PySide6.QtMultimedia import (
    QAudioFormat,
    QAudioSource,
    QMediaDevices,
)

# 录音参数：SenseVoice 只吃 16 kHz，其他采样率要重采样，没必要
SAMPLE_RATE = 16000
CHANNELS = 1
# 单次录音上限（秒）。再长就该分段说了，而且内存吃不住
MAX_SECONDS = 60
# 低于这个长度的录音直接当"没说话"（误点一下）
MIN_SECONDS = 0.35

# 允许的识别语言（和 DSH 的 provider 一致）
LANGUAGES = ("auto", "zh", "en", "yue", "ja", "ko")


# ---------------------------------------------------------------------------
# 模型位置
# ---------------------------------------------------------------------------
def project_root() -> Path:
    from dsai4431_chatbot.core.gui import settings_store

    return settings_store.project_root()


def default_model_dir() -> Path:
    """默认模型目录：`asset/stt`。"""
    return project_root() / "asset" / "stt"


def resolve_model_dir(configured: str = "") -> Path:
    """设置里填的目录（存在才用） → `asset/stt`。

    和 Ollama 那边一个规矩：严格按输入的路径，填的路径不存在就退回默认，
    不让程序因为这些路径而瘫掉。
    """
    text = (configured or "").strip()
    if text:
        path = Path(text)
        if not path.is_absolute():
            path = project_root() / path
        if path.is_dir():
            return path
        print(f"[voice] 设置里的语音模型目录不存在（{text}），改用 asset/stt", flush=True)
    return default_model_dir()


def model_paths(model_dir: Path | None = None) -> tuple[Path, Path, Path]:
    """(模型, tokens, vad)。目录布局固定，缺失的文件由调用方判断。"""
    root = model_dir or default_model_dir()
    return (
        root / "sensevoice" / "model.int8.onnx",
        root / "sensevoice" / "tokens.txt",
        root / "silero_vad.onnx",
    )


def models_ready(model_dir: Path | None = None) -> bool:
    return all(path.is_file() for path in model_paths(model_dir))


# ---------------------------------------------------------------------------
# 识别器（进程级单例）
# ---------------------------------------------------------------------------
_recognizer = None
_recognizer_key: tuple[str, str] | None = None
_load_lock = threading.Lock()


def get_recognizer(language: str = "auto", model_dir: Path | None = None):
    """拿到（必要时加载）识别器。**不要在主线程第一次调用**。

    `language` 变化时不重建模型，只改配置（sherpa 的 set_config 很便宜）；
    这里为了简单，语言在构造时固定为 auto，识别时再按需重建是过度设计。
    """
    global _recognizer, _recognizer_key

    model, tokens, _vad = model_paths(model_dir)
    for path in (model, tokens):
        if not path.is_file():
            raise FileNotFoundError(f"语音模型缺失：{path}")

    key = (str(model), str(tokens))
    with _load_lock:
        if _recognizer is not None and _recognizer_key == key:
            return _recognizer

        import sherpa_onnx

        _recognizer = sherpa_onnx.OfflineRecognizer.from_sense_voice(
            model=str(model),
            tokens=str(tokens),
            num_threads=2,
            sample_rate=SAMPLE_RATE,
            feature_dim=80,
            language=language if language in LANGUAGES else "auto",
            use_itn=True,          # 数字/标点归一化，"二零二六" → "2026"
            provider="cpu",
            debug=False,
        )
        _recognizer_key = key
        return _recognizer


def warm_up_background(language: str = "auto", model_dir: Path | None = None) -> None:
    """后台加载模型（录音时调用，正好和用户说话的时间重叠）。"""
    def _run() -> None:
        try:
            get_recognizer(language, model_dir)
        except Exception as exc:                 # noqa: BLE001 - 预热失败不算错
            print(f"[voice] 预加载语音模型失败：{exc}", flush=True)

    threading.Thread(target=_run, name="voice-warmup", daemon=True).start()


def transcribe(samples: np.ndarray, language: str = "auto",
               model_dir: Path | None = None) -> str:
    """把 float32 [-1, 1] 的 16 kHz 单声道样本转成文字（阻塞，别在主线程调）。"""
    if samples is None or len(samples) == 0:
        return ""
    recognizer = get_recognizer(language, model_dir)
    stream = recognizer.create_stream()
    stream.accept_waveform(SAMPLE_RATE, samples)
    recognizer.decode_stream(stream)
    return (stream.result.text or "").strip()


# ---------------------------------------------------------------------------
# 录音
# ---------------------------------------------------------------------------
class Recorder(QObject):
    """录一段就停。

    用法：`start()` 开始 →（用户说话）→ `stop()` 拿样本。
    QAudioSource 是 push 模式：`start()` 返回一个 QIODevice，数据从它读。
    """

    # 录音中每秒发一次，给界面画时长
    tick = Signal(float)
    # 录到上限自动停（界面据此收起录音态）
    auto_stopped = Signal()

    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self._source: QAudioSource | None = None
        self._io: QIODevice | None = None
        self._chunks: list[bytes] = []
        self._frames = 0
        self._limit_hit = False

    # --- 设备 / 格式 ----------------------------------------------------
    @staticmethod
    def format() -> QAudioFormat:
        fmt = QAudioFormat()
        fmt.setSampleRate(SAMPLE_RATE)
        fmt.setChannelCount(CHANNELS)
        fmt.setSampleFormat(QAudioFormat.SampleFormat.Int16)
        return fmt

    @staticmethod
    def device():
        return QMediaDevices.defaultAudioInput()

    def supported(self) -> bool:
        """当前输入设备支不支持 16 kHz 单声道。"""
        device = self.device()
        if device.isNull():
            return False
        return device.isFormatSupported(self.format())

    # --- 录制 -----------------------------------------------------------
    def is_recording(self) -> bool:
        return self._source is not None

    def duration_s(self) -> float:
        return self._frames / SAMPLE_RATE

    def start(self) -> bool:
        """开始录。返回 False 表示没设备 / 格式不支持。"""
        if self.is_recording():
            return True
        device = self.device()
        if device.isNull():
            return False
        fmt = self.format()
        if not device.isFormatSupported(fmt):
            return False

        self._chunks.clear()
        self._frames = 0
        self._limit_hit = False

        source = QAudioSource(device, fmt, self)
        source.setBufferSize(SAMPLE_RATE * 2)     # 1 秒的缓冲，够用
        io = source.start()
        if io is None:
            return False
        io.readyRead.connect(self._read)
        self._source = source
        self._io = io
        return True

    def _read(self) -> None:
        if self._io is None:
            return
        data = bytes(self._io.readAll())
        if not data:
            return
        self._chunks.append(data)
        self._frames += len(data) // 2            # 16 bit = 2 字节一帧
        self.tick.emit(self.duration_s())
        if self.duration_s() >= MAX_SECONDS:
            self._limit_hit = True
            self.stop()
            self.auto_stopped.emit()

    def stop(self) -> np.ndarray | None:
        """停止并返回 float32 样本；太短（没说话）返回 None。"""
        source, self._source = self._source, None
        io, self._io = self._io, None
        if source is not None:
            try:
                io.readyRead.disconnect(self._read)
            except (RuntimeError, TypeError):
                pass
            source.stop()
            source.deleteLater()

        if not self._chunks:
            return None
        raw = b"".join(self._chunks)
        self._chunks.clear()
        samples = np.frombuffer(raw, dtype="<i2").astype(np.float32) / 32768.0
        if len(samples) < SAMPLE_RATE * MIN_SECONDS:
            return None
        return samples

    def cancel(self) -> None:
        """放弃这段录音，不返回任何东西。"""
        self._chunks.clear()
        self._frames = 0
        self.stop()
        self._chunks.clear()

    @property
    def hit_limit(self) -> bool:
        return self._limit_hit

    # --- 音量大不大（用来提示"没收到声音"）------------------------------
    def peak_level(self) -> float:
        """最近这段录音的峰值（0~1）。全程接近 0 说明麦克风没权限。"""
        if not self._chunks:
            return 0.0
        raw = self._chunks[-1]
        if len(raw) < 2:
            return 0.0
        arr = np.frombuffer(raw, dtype="<i2")
        return float(np.max(np.abs(arr)) / 32768.0) if len(arr) else 0.0

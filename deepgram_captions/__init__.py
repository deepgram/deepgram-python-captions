"""deepgram-captions — WebVTT and SRT caption generation for speech-to-text APIs.

Supported providers
-------------------
* **Deepgram** — :class:`~deepgram_captions.converters.DeepgramConverter`
* **AssemblyAI** — :class:`~deepgram_captions.converters.AssemblyAIConverter`
* **Whisper Timestamped** — :class:`~deepgram_captions.converters.WhisperTimestampedConverter`

Quick start::

    from deepgram_captions import DeepgramConverter, webvtt, srt

    converter = DeepgramConverter(dg_response)
    vtt_string = webvtt(converter)
    srt_string = srt(converter)
"""

from .converters import (
    AssemblyAIConverter,
    ConverterException,
    DeepgramConverter,
    WhisperTimestampedConverter,
)
from .helpers import EmptyTranscriptException
from .srt import srt
from .webvtt import webvtt

__all__ = [
    "DeepgramConverter",
    "AssemblyAIConverter",
    "WhisperTimestampedConverter",
    "ConverterException",
    "EmptyTranscriptException",
    "webvtt",
    "srt",
]

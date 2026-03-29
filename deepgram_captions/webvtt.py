"""WebVTT caption formatter."""

from __future__ import annotations

from typing import Any

from .helpers import EmptyTranscriptException, seconds_to_timestamp


def webvtt(converter: Any, line_length: int | None = None) -> str:
    """Generate a WebVTT caption string from a converter.

    `Web Video Text Tracks (WebVTT) <https://www.w3.org/TR/webvtt1/>`_ is the
    standard caption format for HTML5 ``<video>`` elements and most modern
    media players.

    The *converter* must implement ``get_lines(line_length: int) ->
    list[list[dict]]``.  Optionally it may implement ``get_headers() ->
    list[str]`` to inject a ``NOTE`` block after the ``WEBVTT`` header (used
    by :class:`~deepgram_captions.converters.DeepgramConverter` to embed
    request metadata).

    Speaker diarisation is handled automatically: when word dicts contain a
    ``"speaker"`` key the output uses WebVTT voice tags (``<v Speaker N>``).

    Args:
        converter:   A converter instance, e.g.
                     :class:`~deepgram_captions.converters.DeepgramConverter`.
        line_length: Maximum words per caption cue (default: 8).

    Returns:
        A complete WebVTT document as a string, ready to write to a ``.vtt``
        file or serve over HTTP with ``Content-Type: text/vtt``.

    Raises:
        EmptyTranscriptException: When the converter returns no caption lines.

    Example::

        from deepgram_captions import DeepgramConverter, webvtt

        converter = DeepgramConverter(dg_response)
        vtt = webvtt(converter)

        with open("captions.vtt", "w") as f:
            f.write(vtt)
    """
    if line_length is None:
        line_length = 8

    output: list[str] = ["WEBVTT", ""]

    if hasattr(converter, "get_headers") and callable(converter.get_headers):
        output.append("\n".join(converter.get_headers()))
        output.append("")

    if hasattr(converter, "get_lines") and callable(converter.get_lines):
        lines = converter.get_lines(line_length)

        if not lines[0]:
            raise EmptyTranscriptException("No transcript data found")

        speaker_labels = "speaker" in lines[0][0]

        for words in lines:
            first_word = words[0]
            last_word = words[-1]

            output.append(f"{seconds_to_timestamp(first_word['start'])} --> {seconds_to_timestamp(last_word['end'])}")

            line = " ".join(word.get("punctuated_word", word["word"]) for word in words)
            speaker_label = f"<v Speaker {first_word['speaker']}>" if speaker_labels else ""

            output.append(f"{speaker_label}{line}")
            output.append("")

    return "\n".join(output)

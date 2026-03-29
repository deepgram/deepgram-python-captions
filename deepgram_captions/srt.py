"""SRT (SubRip) caption formatter."""

from __future__ import annotations

from typing import Any

from .helpers import EmptyTranscriptException, seconds_to_timestamp


def srt(converter: Any, line_length: int | None = None) -> str:
    """Generate an SRT caption string from a converter.

    `SubRip Text (SRT) <https://en.wikipedia.org/wiki/SubRip>`_ is the
    most widely supported subtitle format, compatible with virtually every
    media player and video platform.

    The *converter* must implement ``get_lines(line_length: int) ->
    list[list[dict]]``.

    Speaker diarisation is handled automatically: when word dicts contain a
    ``"speaker"`` key a ``[speaker N]`` label is prepended to each cue block
    whenever the speaker changes.

    Args:
        converter:   A converter instance, e.g.
                     :class:`~deepgram_captions.converters.DeepgramConverter`.
        line_length: Maximum words per caption cue (default: 8).

    Returns:
        A complete SRT document as a string, ready to write to a ``.srt``
        file or embed in a video container.

    Raises:
        EmptyTranscriptException: When the converter returns no caption lines.

    Example::

        from deepgram_captions import DeepgramConverter, srt

        converter = DeepgramConverter(dg_response)
        subtitles = srt(converter)

        with open("captions.srt", "w") as f:
            f.write(subtitles)
    """
    if line_length is None:
        line_length = 8

    if hasattr(converter, "get_lines") and callable(converter.get_lines):
        lines = converter.get_lines(line_length)

        if not lines[0]:
            raise EmptyTranscriptException("No transcript data found")

        speaker_labels = "speaker" in lines[0][0]

        output: list[str] = []
        current_speaker: int | None = None

        for index, words in enumerate(lines, start=1):
            first_word = words[0]
            last_word = words[-1]

            output.append(str(index))
            output.append(
                f"{seconds_to_timestamp(first_word['start'], '%H:%M:%S,%f')} --> "
                f"{seconds_to_timestamp(last_word['end'], '%H:%M:%S,%f')}"
            )

            if speaker_labels:
                speaker = first_word.get("speaker")
                if speaker != current_speaker:
                    current_speaker = speaker
                    output.append(f"[speaker {speaker}]")

            line = " ".join(word.get("punctuated_word", word["word"]) for word in words)
            output.append(line)
            output.append("")

    return "\n".join(output)

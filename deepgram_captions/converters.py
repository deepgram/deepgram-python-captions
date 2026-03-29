"""Converter classes that normalise speech-to-text API responses.

Each converter wraps one provider's JSON response and exposes a common
``get_lines(line_length)`` interface consumed by :func:`~deepgram_captions.webvtt.webvtt`
and :func:`~deepgram_captions.srt.srt`.

Supported providers
-------------------
* **Deepgram** — :class:`DeepgramConverter`
* **AssemblyAI** — :class:`AssemblyAIConverter`
* **Whisper Timestamped** — :class:`WhisperTimestampedConverter`

Custom converters
-----------------
Any object that implements ``get_lines(line_length: int) -> list[list[dict]]``
can be passed to the formatters.  Optionally implement ``get_headers() ->
list[str]`` to inject a ``NOTE`` block into WebVTT output.
"""

from __future__ import annotations

import json
from typing import Any

from .helpers import chunk_array, replace_text_with_word


class ConverterException(Exception):
    """Raised when a Deepgram response contains no valid transcriptions."""


class DeepgramConverter:
    """Convert a Deepgram speech-to-text API response into caption lines.

    Accepts the full JSON response from either a pre-recorded or streaming
    Deepgram request.  When the response contains an ``utterances`` array it
    is preferred over ``channels[0].alternatives[0].words`` because utterances
    carry sentence-level grouping that produces more natural caption breaks.

    Speaker diarisation is supported: when word objects include a ``"speaker"``
    field, a new caption line is started on every speaker change (in addition
    to the normal ``line_length`` limit).

    Args:
        dg_response:   The full Deepgram API response.  Accepts either a
                       ``dict`` or any object that exposes a ``.to_json()``
                       method (e.g. the Deepgram Python SDK response models).
        use_exception: When ``True`` (default), raise
                       :class:`ConverterException` if no non-empty transcript
                       is found.  Set to ``False`` to suppress the exception
                       and return empty lines instead.

    Raises:
        ConverterException: If *use_exception* is ``True`` and no valid
                            transcript is present in the response.

    Example::

        import json
        from deepgram_captions import DeepgramConverter, webvtt

        with open("response.json") as f:
            dg_response = json.load(f)

        converter = DeepgramConverter(dg_response)
        print(webvtt(converter))
    """

    def __init__(self, dg_response: dict[str, Any] | Any, use_exception: bool = True) -> None:
        if not isinstance(dg_response, dict):
            self.response: dict[str, Any] = json.loads(dg_response.to_json())
        else:
            self.response = dg_response

        if use_exception:
            one_valid_transcription = False
            for channel in self.response["results"]["channels"]:
                if channel["alternatives"][0]["transcript"] != "":
                    one_valid_transcription = True
                    break
            if "utterances" in self.response["results"]:
                for utterance in self.response["results"]["utterances"]:
                    if utterance["transcript"] != "":
                        one_valid_transcription = True
                        break

            if not one_valid_transcription:
                raise ConverterException("No valid transcriptions found in response")

    def get_lines(self, line_length: int) -> list[list[dict[str, Any]]]:
        """Return caption lines as groups of word dicts.

        Args:
            line_length: Maximum number of words per caption line.

        Returns:
            A list of word-groups.  Each group is a list of word dicts
            containing at minimum ``word``, ``start`` (float seconds), and
            ``end`` (float seconds).  Speaker diarisation data (``speaker``
            key) is preserved when present.
        """
        results = self.response["results"]
        content: list[list[dict[str, Any]]] = []

        if results.get("utterances"):
            for utterance in results["utterances"]:
                if len(utterance["words"]) > line_length:
                    content.extend(chunk_array(utterance["words"], line_length))
                else:
                    content.append(utterance["words"])
        else:
            words: list[dict[str, Any]] = results["channels"][0]["alternatives"][0]["words"]
            diarize = "speaker" in words[0] if words else False
            buffer: list[dict[str, Any]] = []
            current_speaker = 0

            for word in words:
                if diarize and word.get("speaker", 0) != current_speaker:
                    content.append(buffer)
                    buffer = []

                if len(buffer) == line_length:
                    content.append(buffer)
                    buffer = []

                if diarize:
                    current_speaker = word.get("speaker", 0)

                buffer.append(word)

            content.append(buffer)

        return content

    def get_headers(self) -> list[str]:
        """Return lines for a WebVTT ``NOTE`` block containing request metadata.

        Returns:
            A list of strings to be joined as the ``NOTE`` section of a
            WebVTT file.  Includes the request ID, creation time, duration,
            and channel count when available in the response metadata.
        """
        output = [
            "NOTE",
            "Transcription provided by Deepgram",
        ]

        if self.response.get("metadata"):
            metadata = self.response["metadata"]
            if metadata.get("request_id"):
                output.append(f"Request Id: {metadata['request_id']}")
            if metadata.get("created"):
                output.append(f"Created: {metadata['created']}")
            if metadata.get("duration"):
                output.append(f"Duration: {metadata['duration']}")
            if metadata.get("channels"):
                output.append(f"Channels: {metadata['channels']}")

        return output


class AssemblyAIConverter:
    """Convert an AssemblyAI transcription response into caption lines.

    Accepts the JSON response from the AssemblyAI transcription API.
    Handles both responses that include an ``utterances`` array (preferred)
    and those that only include a flat ``words`` array.

    Args:
        assembly_response: The full AssemblyAI API response dict.

    Example::

        from deepgram_captions import AssemblyAIConverter, webvtt

        converter = AssemblyAIConverter(assembly_response)
        print(webvtt(converter))
    """

    def __init__(self, assembly_response: dict[str, Any]) -> None:
        self.response = assembly_response

    def word_map(self, word: dict[str, Any]) -> dict[str, Any]:
        """Map an AssemblyAI word object to the internal caption word format.

        AssemblyAI uses ``"text"`` for the word string; this normalises it to
        ``"word"`` / ``"punctuated_word"`` as expected by the formatters.

        Args:
            word: A single word object from the AssemblyAI response.

        Returns:
            Normalised word dict with keys: ``word``, ``start``, ``end``,
            ``confidence``, ``punctuated_word``, and ``speaker``.
        """
        return {
            "word": word["text"],
            "start": word["start"],
            "end": word["end"],
            "confidence": word["confidence"],
            "punctuated_word": word["text"],
            "speaker": word["speaker"],
        }

    def get_lines(self, line_length: int = 8) -> list[list[dict[str, Any]]]:
        """Return caption lines as groups of normalised word dicts.

        Args:
            line_length: Maximum number of words per caption line.

        Returns:
            A list of word-groups compatible with :func:`~deepgram_captions.webvtt.webvtt`
            and :func:`~deepgram_captions.srt.srt`.
        """
        results = self.response
        content: list[list[dict[str, Any]]] = []
        if results.get("utterances"):
            for utterance in results["utterances"]:
                mapped = [self.word_map(w) for w in utterance["words"]]
                if len(mapped) > line_length:
                    content.extend(chunk_array(mapped, line_length))
                else:
                    content.append(mapped)
        else:
            content.extend(chunk_array([self.word_map(w) for w in results["words"]], line_length))

        return content


class WhisperTimestampedConverter:
    """Convert a Whisper Timestamped response into caption lines.

    `Whisper Timestamped <https://github.com/linto-ai/whisper-timestamped>`_
    adds word-level timestamps to OpenAI Whisper transcriptions.  The plain
    OpenAI Whisper API does **not** include word-level timestamps and is
    therefore not supported.

    .. note::
        For OpenAI Whisper transcriptions *without* word-level timestamps,
        use Deepgram's hosted Whisper Cloud (``model="whisper"``) and the
        :class:`DeepgramConverter` instead.

    Args:
        whisper_response: The full response dict from Whisper Timestamped.

    Example::

        from deepgram_captions import WhisperTimestampedConverter, srt

        converter = WhisperTimestampedConverter(whisper_response)
        print(srt(converter))
    """

    def __init__(self, whisper_response: dict[str, Any]) -> None:
        self.response = whisper_response

    def get_lines(self, line_length: int = 8) -> list[list[dict[str, Any]]]:
        """Return caption lines as groups of normalised word dicts.

        Args:
            line_length: Maximum number of words per caption line.

        Returns:
            A list of word-groups compatible with :func:`~deepgram_captions.webvtt.webvtt`
            and :func:`~deepgram_captions.srt.srt`.
        """
        results = self.response
        content: list[list[dict[str, Any]]] = []
        if results.get("segments"):
            for segment in results["segments"]:
                if len(segment["words"]) > line_length:
                    content.extend(chunk_array(segment["words"], line_length))
                else:
                    content.append(segment["words"])

        return replace_text_with_word(content)

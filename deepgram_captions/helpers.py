"""Shared utilities for caption generation."""

from __future__ import annotations

import datetime
from datetime import timezone


class EmptyTranscriptException(Exception):
    """Raised when a caption formatter receives a response with no transcript content."""


def seconds_to_timestamp(seconds: float, format: str = "%H:%M:%S.%f") -> str:
    """Convert a float number of seconds to a caption timestamp string.

    Rounds to millisecond precision (3 decimal places).

    Args:
        seconds: Time offset in seconds, e.g. ``1.234``.
        format:  strftime format string.

                 - WebVTT default: ``"%H:%M:%S.%f"``  → ``00:00:01.234``
                 - SRT format:     ``"%H:%M:%S,%f"``   → ``00:00:01,234``

    Returns:
        Formatted timestamp string with millisecond precision.

    Example::

        >>> seconds_to_timestamp(65.4)
        '00:01:05.400'
        >>> seconds_to_timestamp(65.4, "%H:%M:%S,%f")
        '00:01:05,400'
    """
    seconds = round(seconds, 3)
    dt = datetime.datetime.fromtimestamp(seconds, timezone.utc)
    formatted_time = dt.strftime(format)
    # %f produces 6-digit microseconds; truncate to 3-digit milliseconds
    formatted_time = formatted_time[:-3] + formatted_time[-3:].lstrip("0")
    return formatted_time


def chunk_array(arr: list, length: int) -> list[list]:
    """Split a list into consecutive chunks of at most *length* items.

    Args:
        arr:    The list to split.
        length: Maximum number of items per chunk.

    Returns:
        A list of sub-lists, each containing at most *length* items.

    Example::

        >>> chunk_array([1, 2, 3, 4, 5], 2)
        [[1, 2], [3, 4], [5]]
    """
    return [arr[i : i + length] for i in range(0, len(arr), length)]


def replace_text_with_word(content: list[list[dict]]) -> list[list[dict]]:
    """Rename the ``"text"`` key to ``"word"`` in nested word dictionaries.

    Some converters (e.g. :class:`WhisperTimestampedConverter`) receive word
    objects where the transcript text is stored under ``"text"`` rather than
    the ``"word"`` key expected by the formatters.  This function normalises
    the key in-place.

    Args:
        content: Nested list of word dicts as returned by a converter's
                 ``get_lines()`` method.

    Returns:
        The same nested structure with ``"text"`` keys renamed to ``"word"``.
    """
    for word_list in content:
        for word in word_list:
            if "text" in word:
                word["word"] = word.pop("text")
    return content

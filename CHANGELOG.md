# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.2.0] - 2024-03-15

### Added
- `pyproject.toml` as the canonical build configuration (replaces `setup.py` as the primary build definition)
- `py.typed` marker file for PEP 561 compliance — fully typed package
- `Makefile` with `install`, `test`, `lint`, `lint-fix`, `format`, `format-check`, `typecheck`, `check`, and `dev` targets
- GitHub Actions CI workflow (`ci.yml`) running lint, type checking, and tests across Python 3.10–3.13
- `ruff` for linting and formatting (replaces `black`)
- `mypy` for static type checking
- Full type annotations on all public APIs in `helpers.py`, `converters.py`, `webvtt.py`, and `srt.py`
- Comprehensive docstrings for all public classes and functions
- `SECURITY.md` with responsible disclosure policy
- `CHANGELOG.md` (this file)

### Changed
- `DeepgramConverter`, `AssemblyAIConverter`, and `WhisperTimestampedConverter` now carry full type hints
- `webvtt()` and `srt()` functions are now fully typed with `Any` converter protocol
- `EmptyTranscriptException` and `ConverterException` are now exported from the top-level `deepgram_captions` package
- Updated classifiers to reflect Production/Stable status and Python 3.10–3.13 support
- Release workflow updated to use `actions/checkout@v4` and `actions/setup-python@v4`
- Release workflow version bumping now targets `pyproject.toml` instead of `_version.py` only

### Fixed
- `chunk_array` simplified to a single list comprehension (functionally identical, more idiomatic)

## [1.1.0] - 2023-11-08

### Added
- `AssemblyAIConverter` — support for AssemblyAI speech-to-text API responses
- `WhisperTimestampedConverter` — support for [Whisper Timestamped](https://github.com/linto-ai/whisper-timestamped) responses (word-level timestamps required)
- `replace_text_with_word()` helper to normalise `"text"` key to `"word"` for Whisper Timestamped compatibility
- Documentation note clarifying that OpenAI Whisper (without word timestamps) is not supported directly; users should use Deepgram's hosted Whisper Cloud (`model=whisper`) with `DeepgramConverter`

### Changed
- `get_lines()` on `AssemblyAIConverter` now respects `utterances` array when present, falling back to flat `words` array
- `WhisperTimestampedConverter.get_lines()` processes `segments` array and applies `replace_text_with_word` normalisation

## [1.0.0] - 2023-10-15

### Added
- Speaker diarisation support in `DeepgramConverter.get_lines()`: when word objects include a `"speaker"` field, caption lines break on speaker changes in addition to `line_length` limits
- Speaker labels in WebVTT output using voice tags: `<v Speaker 0>text</v>`
- Speaker labels in SRT output as `[speaker N]` prefix lines, emitted once per speaker change
- `use_exception` parameter on `DeepgramConverter.__init__()` — set to `False` to suppress `ConverterException` when no valid transcript is found
- `EmptyTranscriptException` raised by `webvtt()` and `srt()` when the converter returns an empty first line
- `line_length` parameter on `webvtt()` and `srt()` — controls the maximum number of words per caption cue (default: 8)
- `get_headers()` on `DeepgramConverter` returns a `NOTE` block for WebVTT output containing request ID, creation time, duration, and channel count from the Deepgram response metadata

### Changed
- `DeepgramConverter` now prefers the `utterances` array over `channels[0].alternatives[0].words` when both are present, producing more natural sentence-level caption breaks
- `webvtt()` checks for `get_headers()` capability via `hasattr`/`callable` — custom converters do not need to implement it

### Fixed
- Microsecond precision in `seconds_to_timestamp()` correctly truncated to milliseconds for both WebVTT (`.`) and SRT (`,`) formats

## [0.1.0] - 2023-09-20

### Added
- `DeepgramConverter` class wrapping Deepgram pre-recorded and streaming API responses
- `webvtt()` function generating valid WebVTT documents from any converter
- `srt()` function generating valid SRT documents from any converter
- `seconds_to_timestamp()` utility converting float seconds to `HH:MM:SS.mmm` or `HH:MM:SS,mmm`
- `chunk_array()` utility splitting word lists into fixed-length groups
- `EmptyTranscriptException` for empty transcript detection
- Support for Deepgram SDK response objects via `.to_json()` method detection
- Initial test suite covering Deepgram pre-recorded responses

## [0.0.1] - 2023-08-01

### Added
- Initial project scaffold
- Package structure: `deepgram_captions/` with `__init__.py`, `helpers.py`, `converters.py`, `webvtt.py`, `srt.py`
- `setup.py` with basic package metadata
- MIT License
- Initial README

[1.2.0]: https://github.com/deepgram/deepgram-python-captions/compare/v1.1.0...v1.2.0
[1.1.0]: https://github.com/deepgram/deepgram-python-captions/compare/v1.0.0...v1.1.0
[1.0.0]: https://github.com/deepgram/deepgram-python-captions/compare/v0.1.0...v1.0.0
[0.1.0]: https://github.com/deepgram/deepgram-python-captions/compare/v0.0.1...v0.1.0
[0.0.1]: https://github.com/deepgram/deepgram-python-captions/releases/tag/v0.0.1

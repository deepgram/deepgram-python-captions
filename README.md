# deepgram-captions

[![PyPI version](https://badge.fury.io/py/deepgram-captions.svg)](https://badge.fury.io/py/deepgram-captions)
[![Python 3.10+](https://img.shields.io/badge/python-3.10%2B-blue.svg)](https://www.python.org/downloads/)
[![MIT License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

Official Python library for generating **WebVTT** and **SRT** captions from
[Deepgram](https://deepgram.com) and other speech-to-text API responses.

Given a transcription response, this package returns valid WebVTT or SRT caption
strings ready to embed in video players, upload to streaming platforms, or store
as caption files. It handles word-level timestamps, speaker diarisation, and
configurable line lengths out of the box.

The library ships converters for **Deepgram**, **AssemblyAI**, and
**Whisper Timestamped**, and exposes a simple duck-typing interface so you can
add support for any other provider.

Full documentation is available at [developers.deepgram.com](https://developers.deepgram.com/docs).

---

## Installation

```bash
pip install deepgram-captions
```

Python 3.10 or higher is required. The package has no runtime dependencies.

---

## Quick Start

```python
import json
from deepgram_captions import DeepgramConverter, webvtt, srt

# Load a Deepgram pre-recorded transcription response
with open("response.json") as f:
    dg_response = json.load(f)

converter = DeepgramConverter(dg_response)

# Generate WebVTT
vtt = webvtt(converter)
with open("captions.vtt", "w") as f:
    f.write(vtt)

# Generate SRT
subtitles = srt(converter)
with open("captions.srt", "w") as f:
    f.write(subtitles)
```

---

## Deepgram

### Pre-recorded Transcription

Send an audio file to Deepgram's pre-recorded API, then pass the response
directly to `DeepgramConverter`. The Deepgram Python SDK returns response
objects with a `.to_json()` method — `DeepgramConverter` accepts both plain
`dict` responses and SDK response objects.

```python
import httpx
import json
from deepgram_captions import DeepgramConverter, webvtt, srt

# Using httpx / requests directly
url = "https://api.deepgram.com/v1/listen?model=nova-3&smart_format=true&utterances=true"
headers = {"Authorization": "Token YOUR_DEEPGRAM_API_KEY"}

with open("audio.wav", "rb") as f:
    response = httpx.post(url, headers=headers, content=f.read(),
                          headers={**headers, "Content-Type": "audio/wav"})

dg_response = response.json()

converter = DeepgramConverter(dg_response)
print(webvtt(converter))
print(srt(converter))
```

Using the [Deepgram Python SDK](https://github.com/deepgram/deepgram-python-sdk):

```python
from deepgram import DeepgramClient, PrerecordedOptions
from deepgram_captions import DeepgramConverter, webvtt, srt

deepgram = DeepgramClient("YOUR_DEEPGRAM_API_KEY")

with open("audio.wav", "rb") as f:
    buffer_data = f.read()

options = PrerecordedOptions(
    model="nova-3",
    smart_format=True,
    utterances=True,
)

response = deepgram.listen.rest.v("1").transcribe_file(
    {"buffer": buffer_data}, options
)

# DeepgramConverter accepts the SDK response object directly
converter = DeepgramConverter(response)
print(webvtt(converter))
```

> **Tip:** Enable `utterances=True` in your Deepgram request for the best
> caption results. When utterances are present, `DeepgramConverter` uses them
> for natural sentence-level caption breaks instead of chunking raw words.

### Live / Streaming Transcription

For streaming audio, Deepgram returns incremental `Results` messages. Each
message contains a `channel.alternatives[0].words` array for that audio chunk.
To generate captions from a completed stream, accumulate the word objects from
all `is_final=True` results and build a synthetic response object, then pass it
to `DeepgramConverter`.

```python
import asyncio
from deepgram import DeepgramClient, LiveOptions, LiveTranscriptionEvents
from deepgram_captions import DeepgramConverter, webvtt

all_words = []

def on_message(self, result, **kwargs):
    sentence = result.channel.alternatives[0]
    if result.is_final and sentence.words:
        all_words.extend(sentence.words)

async def main():
    deepgram = DeepgramClient("YOUR_DEEPGRAM_API_KEY")
    connection = deepgram.listen.asyncwebsocket.v("1")
    connection.on(LiveTranscriptionEvents.Transcript, on_message)

    options = LiveOptions(model="nova-3", smart_format=True)
    await connection.start(options)

    # ... stream your audio here ...

    await connection.finish()

    # Build a synthetic pre-recorded response from accumulated words
    synthetic_response = {
        "metadata": {"request_id": "streaming-session"},
        "results": {
            "channels": [
                {
                    "alternatives": [
                        {
                            "transcript": " ".join(w.word for w in all_words),
                            "words": [
                                {
                                    "word": w.word,
                                    "punctuated_word": w.punctuated_word,
                                    "start": w.start,
                                    "end": w.end,
                                    "confidence": w.confidence,
                                }
                                for w in all_words
                            ],
                        }
                    ]
                }
            ]
        },
    }

    converter = DeepgramConverter(synthetic_response)
    print(webvtt(converter))

asyncio.run(main())
```

---

## Output Formats

### WebVTT

[Web Video Text Tracks (WebVTT)](https://www.w3.org/TR/webvtt1/) is the standard
caption format for HTML5 `<video>` elements and most modern media players.
WebVTT files use the `.vtt` extension and should be served with
`Content-Type: text/vtt`.

```python
from deepgram_captions import DeepgramConverter, webvtt

converter = DeepgramConverter(dg_response)
captions = webvtt(converter)
print(captions)
```

When transcribing [https://dpgr.am/spacewalk.wav](https://dpgr.am/spacewalk.wav),
the output looks like:

```text
WEBVTT

NOTE
Transcription provided by Deepgram
Request Id: 686278aa-d315-4aeb-b2a9-713615544366
Created: 2023-10-27T15:35:56.637Z
Duration: 25.933313
Channels: 1

00:00:00.080 --> 00:00:03.220
Yeah. As as much as, it's worth celebrating,

00:00:04.400 --> 00:00:05.779
the first, spacewalk,

00:00:06.319 --> 00:00:07.859
with an all female team,

00:00:08.475 --> 00:00:10.715
I think many of us are looking forward

00:00:10.715 --> 00:00:13.215
to it just being normal and

00:00:13.835 --> 00:00:16.480
I think if it signifies anything, It is

00:00:16.779 --> 00:00:18.700
to honor the the women who came before

00:00:18.700 --> 00:00:21.680
us who, were skilled and qualified,

00:00:22.300 --> 00:00:24.779
and didn't get the same opportunities that we

00:00:24.779 --> 00:00:25.439
have today.
```

The `NOTE` block at the top is populated automatically by `DeepgramConverter`
from the response metadata (request ID, creation time, duration, channel count).

### SRT

[SubRip Text (SRT)](https://en.wikipedia.org/wiki/SubRip) is the most widely
supported subtitle format, compatible with virtually every media player and
video platform. SRT files use the `.srt` extension.

```python
from deepgram_captions import DeepgramConverter, srt

converter = DeepgramConverter(dg_response)
captions = srt(converter)
print(captions)
```

For the same spacewalk audio:

```text
1
00:00:00,080 --> 00:00:03,220
Yeah. As as much as, it's worth celebrating,

2
00:00:04,400 --> 00:00:07,859
the first, spacewalk, with an all female team,

3
00:00:08,475 --> 00:00:10,715
I think many of us are looking forward

4
00:00:10,715 --> 00:00:14,235
to it just being normal and I think

5
00:00:14,235 --> 00:00:17,340
if it signifies anything, It is to honor

6
00:00:17,340 --> 00:00:19,820
the the women who came before us who,

7
00:00:20,140 --> 00:00:23,580
were skilled and qualified, and didn't get the

8
00:00:23,580 --> 00:00:25,439
same opportunities that we have today.
```

Note the comma separator in SRT timestamps (`00:00:00,080`) versus the period
in WebVTT (`00:00:00.080`).

### Line Length

Both `webvtt()` and `srt()` accept an optional `line_length` integer that
controls the maximum number of words per caption cue. The default is `8`.

```python
from deepgram_captions import DeepgramConverter, webvtt

converter = DeepgramConverter(dg_response)

# Shorter captions — 5 words max per cue
captions = webvtt(converter, line_length=5)

# Longer captions — 12 words max per cue
captions = webvtt(converter, line_length=12)
```

When `utterances=True` is enabled on the Deepgram request, the `line_length`
acts as a maximum per utterance chunk rather than an absolute global limit —
each utterance is first broken at sentence boundaries, then further chunked if
it exceeds `line_length`.

### Speaker Diarisation

When Deepgram's `diarize=True` option is enabled, word objects include a
`speaker` field. `DeepgramConverter` detects this automatically and inserts
caption breaks on speaker changes in addition to the `line_length` limit.

**WebVTT** output uses standard voice tags:

```text
WEBVTT

00:00:00.080 --> 00:00:04.120
<v Speaker 0>Yeah. As as much as, it's worth celebrating,

00:00:04.400 --> 00:00:08.200
<v Speaker 1>the first, spacewalk, with an all female team,

00:00:08.475 --> 00:00:12.340
<v Speaker 0>I think many of us are looking forward to it
```

**SRT** output emits a `[speaker N]` label at the start of each speaker block,
repeated only when the speaker changes:

```text
1
00:00:00,080 --> 00:00:04,120
[speaker 0]
Yeah. As as much as, it's worth celebrating,

2
00:00:04,400 --> 00:00:08,200
[speaker 1]
the first, spacewalk, with an all female team,

3
00:00:08,475 --> 00:00:12,340
[speaker 0]
I think many of us are looking forward to it
```

To enable diarisation with the Deepgram API:

```python
options = PrerecordedOptions(
    model="nova-3",
    smart_format=True,
    diarize=True,
    utterances=True,
)
```

---

## Other Converters

### AssemblyAI

`AssemblyAIConverter` wraps the [AssemblyAI](https://www.assemblyai.com/)
transcription API response. It supports both the `utterances` array (preferred,
gives natural sentence breaks) and the flat `words` array.

```python
import httpx
from deepgram_captions import AssemblyAIConverter, webvtt, srt

# Poll for a completed AssemblyAI transcription
response = httpx.get(
    f"https://api.assemblyai.com/v2/transcript/{transcript_id}",
    headers={"authorization": "YOUR_ASSEMBLYAI_API_KEY"},
)
assembly_response = response.json()

converter = AssemblyAIConverter(assembly_response)
print(webvtt(converter))
print(srt(converter))
```

AssemblyAI word objects use `"text"` instead of `"word"` for the transcript
text. `AssemblyAIConverter` normalises this automatically via its `word_map()`
method.

### Whisper Timestamped

[Whisper Timestamped](https://github.com/linto-ai/whisper-timestamped) adds
word-level timestamps to OpenAI Whisper speech-to-text transcriptions. This is
required because the standard OpenAI Whisper API does **not** return
word-level timestamps and therefore cannot be used directly with this package.

```python
import whisper_timestamped as whisper
from deepgram_captions import WhisperTimestampedConverter, webvtt, srt

model = whisper.load_model("base")
result = whisper.transcribe(model, "audio.wav")

converter = WhisperTimestampedConverter(result)
print(webvtt(converter))
print(srt(converter))
```

### A Note on OpenAI Whisper

The standard OpenAI Whisper API (`openai.Audio.transcribe`) does not include
word-level timestamps in its response, so it is **not** directly compatible
with this package.

You have two options:

1. **Deepgram's hosted Whisper Cloud** — Use Deepgram's API with
   `model="whisper"`. You get Whisper transcriptions with full word-level
   timestamps and all Deepgram features. Use `DeepgramConverter` as normal.

   ```python
   from deepgram_captions import DeepgramConverter, webvtt

   # dg_response from Deepgram with model="whisper"
   converter = DeepgramConverter(dg_response)
   print(webvtt(converter))
   ```

2. **Whisper Timestamped** — Run Whisper locally with the
   `whisper-timestamped` library to get word-level timestamps, then use
   `WhisperTimestampedConverter`.

---

## Custom Converters

You can write a converter for any speech-to-text provider by implementing the
duck-typing interface consumed by `webvtt()` and `srt()`.

### Required

```python
def get_lines(self, line_length: int) -> list[list[dict]]:
    ...
```

Return a list of caption cue groups. Each group is a list of word dicts
containing at minimum:

| Key              | Type    | Description                                      |
| ---------------- | ------- | ------------------------------------------------ |
| `word`           | `str`   | The word text (used as fallback display text)    |
| `punctuated_word`| `str`   | Punctuated form of the word (preferred for display) |
| `start`          | `float` | Start time in seconds                            |
| `end`            | `float` | End time in seconds                              |
| `speaker`        | `int`   | (Optional) Speaker index for diarisation         |

If `punctuated_word` is absent, `word` is used instead.

### Optional

```python
def get_headers(self) -> list[str]:
    ...
```

Return a list of strings to be joined as a `NOTE` block in WebVTT output.
The `NOTE` block is placed after the `WEBVTT` header. If this method is not
present, no `NOTE` block is generated.

### Example

```python
from deepgram_captions import webvtt, srt
from deepgram_captions.helpers import chunk_array


class MyProviderConverter:
    def __init__(self, response: dict) -> None:
        self.response = response

    def get_headers(self) -> list[str]:
        return [
            "NOTE",
            "Transcription provided by MyProvider",
            f"Job ID: {self.response.get('job_id', 'unknown')}",
        ]

    def get_lines(self, line_length: int) -> list[list[dict]]:
        words = [
            {
                "word": w["token"],
                "punctuated_word": w.get("display_form", w["token"]),
                "start": w["offset_seconds"],
                "end": w["offset_seconds"] + w["duration_seconds"],
            }
            for w in self.response["words"]
        ]
        return chunk_array(words, line_length)


converter = MyProviderConverter(my_response)
print(webvtt(converter))
print(srt(converter))
```

---

## API Reference

### `DeepgramConverter(dg_response, use_exception=True)`

Converts a Deepgram pre-recorded or streaming API response.

| Parameter       | Type               | Default | Description                                                                      |
| --------------- | ------------------ | ------- | -------------------------------------------------------------------------------- |
| `dg_response`   | `dict` or SDK obj  | —       | The full Deepgram API response. SDK response objects are auto-serialised via `.to_json()`. |
| `use_exception` | `bool`             | `True`  | Raise `ConverterException` if no non-empty transcript is found.                  |

**Methods:**
- `get_lines(line_length: int) -> list[list[dict]]` — Returns caption word groups.
- `get_headers() -> list[str]` — Returns lines for a WebVTT `NOTE` block with request metadata.

**Raises:** `ConverterException` when `use_exception=True` and no valid transcript exists.

---

### `AssemblyAIConverter(assembly_response)`

Converts an AssemblyAI transcription API response.

| Parameter          | Type   | Description                           |
| ------------------ | ------ | ------------------------------------- |
| `assembly_response`| `dict` | The full AssemblyAI API response dict |

**Methods:**
- `get_lines(line_length: int = 8) -> list[list[dict]]` — Returns caption word groups.
- `word_map(word: dict) -> dict` — Normalises a single AssemblyAI word object.

---

### `WhisperTimestampedConverter(whisper_response)`

Converts a Whisper Timestamped response (requires word-level timestamps).

| Parameter         | Type   | Description                                    |
| ----------------- | ------ | ---------------------------------------------- |
| `whisper_response`| `dict` | The full Whisper Timestamped response dict     |

**Methods:**
- `get_lines(line_length: int = 8) -> list[list[dict]]` — Returns caption word groups.

---

### `webvtt(converter, line_length=None) -> str`

Generates a complete WebVTT document string.

| Parameter     | Type  | Default | Description                              |
| ------------- | ----- | ------- | ---------------------------------------- |
| `converter`   | Any   | —       | A converter instance with `get_lines()`  |
| `line_length` | `int` | `8`     | Maximum words per caption cue            |

**Returns:** A `str` containing a complete WebVTT document.

**Raises:** `EmptyTranscriptException` when the converter returns no caption lines.

---

### `srt(converter, line_length=None) -> str`

Generates a complete SRT document string.

| Parameter     | Type  | Default | Description                              |
| ------------- | ----- | ------- | ---------------------------------------- |
| `converter`   | Any   | —       | A converter instance with `get_lines()`  |
| `line_length` | `int` | `8`     | Maximum words per caption cue            |

**Returns:** A `str` containing a complete SRT document.

**Raises:** `EmptyTranscriptException` when the converter returns no caption lines.

---

### Exceptions

| Exception                 | Module                       | Description                                                    |
| ------------------------- | ---------------------------- | -------------------------------------------------------------- |
| `ConverterException`      | `deepgram_captions`          | Raised by `DeepgramConverter` when no valid transcript exists  |
| `EmptyTranscriptException`| `deepgram_captions`          | Raised by `webvtt()` / `srt()` when the converter returns empty lines |

Both exceptions are importable directly from the top-level package:

```python
from deepgram_captions import ConverterException, EmptyTranscriptException
```

---

## Development

Clone the repository and install the development dependencies:

```bash
git clone https://github.com/deepgram/deepgram-python-captions.git
cd deepgram-python-captions
pip install -e ".[dev]"
```

### Available Make targets

| Target          | Description                                              |
| --------------- | -------------------------------------------------------- |
| `make install`  | Install the package and dev dependencies in editable mode |
| `make test`     | Run the test suite with pytest                           |
| `make lint`     | Run ruff linter                                          |
| `make lint-fix` | Run ruff linter with auto-fix                            |
| `make format`   | Run ruff formatter                                       |
| `make format-check` | Check formatting without making changes              |
| `make typecheck`| Run mypy type checker                                    |
| `make check`    | Run format-check + lint + typecheck (no tests)           |
| `make dev`      | Run lint-fix + format + test (full development cycle)    |

### Running tests

```bash
make test
# or directly
pytest test/ -v
```

### Code style

This project uses [ruff](https://docs.astral.sh/ruff/) for both linting and
formatting, and [mypy](https://mypy.readthedocs.io/) for type checking. Line
length is set to 120 characters.

```bash
make check      # format-check + lint + typecheck
make dev        # lint-fix + format + test
```

---

## Contributing

We welcome contributions of all kinds — bug fixes, new converters, improved
documentation, and test coverage improvements.

Please read [CONTRIBUTING.md](CONTRIBUTING.md) before opening a pull request.

Key points:

- Open a GitHub Issue before starting work on a significant change.
- Ensure the test suite passes: `make test`.
- Ensure code quality checks pass: `make check`.
- Follow [Conventional Commits](https://www.conventionalcommits.org/) for
  commit messages.
- Be sure to review and agree to our [Code of Conduct](.github/CODE_OF_CONDUCT.md).

---

## Getting Help

We love to hear from you. If you have questions, comments, or find a bug, you can:

- [Open an issue](https://github.com/deepgram/deepgram-python-captions/issues/new) in this repository
- [Join the Deepgram GitHub Discussions Community](https://github.com/orgs/deepgram/discussions)
- [Join the Deepgram Discord Community](https://discord.gg/xWRaCDBtW4)

For questions about the Deepgram API itself, visit
[developers.deepgram.com](https://developers.deepgram.com/docs).

---

## License

This project is licensed under the MIT License. See [LICENSE](LICENSE) for details.

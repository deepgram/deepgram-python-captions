# Deepgram Python Captions

[![Discord](https://dcbadge.vercel.app/api/server/xWRaCDBtW4?style=flat)](https://discord.gg/xWRaCDBtW4) [![PyPI version](https://badge.fury.io/py/deepgram-captions.svg)](https://badge.fury.io/py/deepgram-captions)

This package is the Python implementation of Deepgram's WebVTT and SRT formatting. Given a transcription, this package can return a valid string to store as WebVTT or SRT caption files.

## Installation

```bash
pip install deepgram-captions
```

## WebVTT from Deepgram Transcriptions

```python
from deepgram_captions import DeepgramConverter, webvtt

transcription = DeepgramConverter(dg_response)
captions = webvtt(transcription)
```

## SRT from Deepgram Transcriptions

```py
from deepgram_captions import DeepgramConverter, srt

transcription = DeepgramConverter(dg_response)
captions = srt(transcription)
```

## Other Converters

### Whisper Timestamped

```py
from deepgram_captions import WhisperTimestampedConverter, webvtt

transcription = WhisperTimestampedConverter(whisper_response)
captions = webvtt(transcription)
```

[Whisper Timestamped](https://github.com/linto-ai/whisper-timestamped) adds word-level timestamps to OpenAI's Whisper speech-to-text transcriptions. Word-level timestamps are required for this package to create captions, which is why we have created the captions converter for Whisper Timestamped (and not OpenAI's Whisper).

### Assembly AI

```py
from deepgram_captions import AssemblyAIConverter, webvtt

transcription = AssemblyAIConverter(assembly_response)
captions = webvtt(transcription)
```

## Output WebVTT

When transcribing https://dpgr.am/spacewalk.wav, and running it through our library, this is the WebVTT output.

```py
from deepgram_captions.converters import DeepgramConverter
from deepgram_captions.webvtt import webvtt

transcription = DeepgramConverter(dg_response)
captions = webvtt(transcription)
print(captions)
```

This is the result:

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

## Output SRT

When transcribing https://dpgr.am/spacewalk.wav, and running it through our library, this is the SRT output.

```py
from deepgram_captions import DeepgramConverter, srt

transcription = DeepgramConverter(dg_response)
captions = srt(transcription)
print(captions)
```

This is the result:

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

## Documentation

You can learn more about the Deepgram API at [developers.deepgram.com](https://developers.deepgram.com/docs).

## Development and Contributing

Interested in contributing? We ❤️ pull requests!

To make sure our community is safe for all, be sure to review and agree to our
[Code of Conduct](./.github/CODE_OF_CONDUCT.md). Then see the
[Contribution](./.github/CONTRIBUTING.md) guidelines for more information.

## Getting Help

We love to hear from you so if you have questions, comments or find a bug in the
project, let us know! You can either:

- [Open an issue in this repository](https://github.com/deepgram/[reponame]/issues/new)
- [Join the Deepgram Github Discussions Community](https://github.com/orgs/deepgram/discussions)
- [Join the Deepgram Discord Community](https://discord.gg/xWRaCDBtW4)

[license]: LICENSE.txt

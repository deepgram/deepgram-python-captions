import pytest
import re
from deepgram_captions.srt import srt
from deepgram_captions.webvtt import webvtt
from deepgram_captions.converters import DeepgramConverter
import json

json_file_dg_transcription = "test/dg_transcription.json"
json_file_dg_utterances = "test/dg_utterances.json"
json_file_dg_speakers = "test/dg_speakers.json"
json_file_dg_speakers_no_utterances = "test/dg_speakers_no_utterances.json"

dg_transcription = None
dg_utterances = None
dg_speakers = None
dg_speakers_no_utterances = None

with open(json_file_dg_transcription, "r") as json_file:
    dg_transcription = json.load(json_file)
with open(json_file_dg_utterances, "r") as json_file:
    dg_utterances = json.load(json_file)
with open(json_file_dg_speakers, "r") as json_file:
    dg_speakers = json.load(json_file)
with open(json_file_dg_speakers_no_utterances, "r") as json_file:
    dg_speakers_no_utterances = json.load(json_file)


@pytest.mark.parametrize(
    "input_data",
    [
        DeepgramConverter(dg_transcription),
        DeepgramConverter(dg_utterances),
        DeepgramConverter(dg_speakers),
        DeepgramConverter(dg_speakers_no_utterances),
    ],
)
def test_webvtt_start_with_webvtt(input_data):
    """
    Test that WebVTT captions start with "WEBVTT".
    """
    result = webvtt(input_data)
    result = webvtt(input_data)

    lines = result.strip().split("\n")

    if lines:
        first_line = lines[0].strip()
        assert (
            first_line == "WEBVTT"
        ), f"WebVTT captions do not start with 'WEBVTT': {first_line}"


@pytest.mark.parametrize(
    "input_data",
    [
        DeepgramConverter(dg_transcription),
        DeepgramConverter(dg_utterances),
        DeepgramConverter(dg_speakers),
        DeepgramConverter(dg_speakers_no_utterances),
    ],
)
def test_webvtt_header(input_data):
    """
    Test if the WebVTT format header is generated correctly.
    """
    result = webvtt(input_data)
    assert isinstance(result, str), "Result should be a string"
    assert "NOTE" in result, "Result should contain 'NOTE' in header"
    assert (
        "Transcription provided by Deepgram" in result
    ), "Result should name Deepgram as transcription source in header"
    assert "Request Id" in result, "Result should contain Request Id in header"
    assert "Created" in result, "Result should contain Created timestamp in header"
    assert "Duration" in result, "Result should contain Duration information in header"
    assert "Channels" in result, "Result should contain Channels information in header"


@pytest.mark.parametrize(
    "input_data",
    [
        DeepgramConverter(dg_transcription),
        DeepgramConverter(dg_utterances),
        DeepgramConverter(dg_speakers),
        DeepgramConverter(dg_speakers_no_utterances),
    ],
)
def test_webvtt_timestamp_format(input_data):
    """
    Test if timestamps in the WebVTT output have the correct format.
    """
    result = webvtt(input_data)
    timestamp_pattern = r"\d{2}:\d{2}:\d{2}\.\d{3} --> \d{2}:\d{2}:\d{2}\.\d{3}"
    webvtt_captions = webvtt(result)
    timestamp_lines = re.findall(timestamp_pattern, webvtt_captions)
    for timestamp_line in timestamp_lines:
        assert (
            re.match(timestamp_pattern, timestamp_line) is not None
        ), f"Timestamp format is incorrect: {timestamp_line}"


@pytest.mark.parametrize(
    "input_data",
    [DeepgramConverter(dg_speakers), DeepgramConverter(dg_speakers_no_utterances)],
)
def test_webvtt_speaker_format(input_data):
    """
    Test if the WebVTT output contains speaker information in the correct format.
    """
    result = webvtt(input_data)
    caption_pattern = r"\d{2}:\d{2}:\d{2}\.\d{3} --> \d{2}:\d{2}:\d{2}\.\d{3}\n<v [^\s]+>[^\n]+\n<v [^\s]+>[^\n]+"
    captions = re.findall(caption_pattern, result)
    for caption in captions:
        assert (
            re.match(r"<v [^\s]+>", caption.split("\n")[1]) is not None
        ), f"Speaker format is incorrect: {caption}"


@pytest.mark.parametrize(
    "input_data",
    [
        DeepgramConverter(dg_transcription),
        DeepgramConverter(dg_utterances),
        DeepgramConverter(dg_speakers),
        DeepgramConverter(dg_speakers_no_utterances),
    ],
)
def test_srt_format(input_data):
    """
    Test if SRT captions follow the correct format.
    """
    result = srt(input_data)
    srt_captions = result.split("\n\n")

    for index, caption in enumerate(srt_captions, start=1):
        if caption.strip():
            lines = caption.split("\n")
            assert lines[0] == str(index), f"Caption number is incorrect: {lines[0]}"

            timestamp_pattern = r"\d{2}:\d{2}:\d{2},\d{3} --> \d{2}:\d{2}:\d{2},\d{3}"
            assert (
                re.match(timestamp_pattern, lines[1]) is not None
            ), f"Timestamp format is incorrect: {lines[1]}"

            assert len(lines) > 2, "Speech content is missing"


@pytest.mark.parametrize(
    "input_data",
    [
        DeepgramConverter(dg_transcription),
        DeepgramConverter(dg_utterances),
        DeepgramConverter(dg_speakers),
        DeepgramConverter(dg_speakers_no_utterances),
    ],
)
def test_srt_timestamp_format(input_data):
    """
    Test if timestamps in the SRT output have the correct format.
    """
    result = srt(input_data)
    srt_captions = result.split("\n\n")
    timestamp_pattern = r"\d{2}:\d{2}:\d{2}\,\d{3} --> \d{2}:\d{2}:\d{2}\,\d{3}"
    for caption in srt_captions:
        if caption.strip():
            lines = caption.split("\n")
            assert (
                re.match(timestamp_pattern, lines[1]) is not None
            ), f"Timestamp format is incorrect: {lines[1]}"


@pytest.mark.parametrize(
    "input_data",
    [
        DeepgramConverter(dg_transcription),
        DeepgramConverter(dg_utterances),
        DeepgramConverter(dg_speakers),
        DeepgramConverter(dg_speakers_no_utterances),
    ],
)
def test_first_caption_number(input_data):
    """
    Test that the first caption number in the SRT output is 1.
    """
    result = srt(input_data)
    srt_captions = result.split("\n\n")

    if srt_captions:
        first_caption_lines = srt_captions[0].split("\n")
        first_caption_number = int(first_caption_lines[0])

        assert (
            first_caption_number == 1
        ), f"First caption number is not 1: {first_caption_number}"


if __name__ == "__main__":
    pytest.main()

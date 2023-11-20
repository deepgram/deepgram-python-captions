from deepgram_captions import (
    srt,
    webvtt,
    DeepgramConverter,
    AssemblyAIConverter,
    WhisperTimestampedConverter,
)
import json

json_file_dg_transcription = "test/dg_transcription.json"
json_file_dg_utterances = "test/dg_utterances.json"
json_file_dg_speakers = "test/dg_speakers.json"
json_file_dg_speakers_no_utterances = "test/dg_speakers_no_utterances.json"
json_file_assemblyai_transcription = "test/assemblyai_transcription.json"
json_file_assemblyai_utterances = "test/assemblyai_utterances.json"
json_file_whisper_timestamped = "test/whisper_timestamped.json"
json_file_dg_whisper_transcription = "test/dg_whisper_transcription.json"

dg_transcription = None
dg_utterances = None
dg_speakers = None
dg_speakers_no_utterances = None
assemblyai_transcription = None
assemblyai_utterances = None
whisper_timestamped = None
dg_whisper_transcription = None

with open(json_file_dg_transcription, "r") as json_file:
    dg_transcription = json.load(json_file)
with open(json_file_dg_utterances, "r") as json_file:
    dg_utterances = json.load(json_file)
with open(json_file_dg_speakers, "r") as json_file:
    dg_speakers = json.load(json_file)
with open(json_file_dg_speakers_no_utterances, "r") as json_file:
    dg_speakers_no_utterances = json.load(json_file)
with open(json_file_assemblyai_transcription, "r") as json_file:
    assemblyai_transcription = json.load(json_file)
with open(json_file_assemblyai_utterances, "r") as json_file:
    assemblyai_utterances = json.load(json_file)
with open(json_file_whisper_timestamped, "r") as json_file:
    whisper_timestamped = json.load(json_file)
with open(json_file_dg_whisper_transcription, "r") as json_file:
    dg_whisper_transcription = json.load(json_file)

# Uncomment a section to test the converter:

line_length = 10

deepgram = DeepgramConverter(dg_speakers)
captions = webvtt(deepgram, line_length)
print(captions)

# assembly = AssemblyAIConverter(assemblyai_utterances)
# captions = webvtt(assembly)
# print(captions)

# whisperTS = WhisperTimestampedConverter(whisper_timestamped)
# captions = srt(whisperTS)
# print(captions)

# deepgram_whisper = DeepgramConverter(dg_whisper_transcription)
# captions = webvtt(deepgram_whisper)
# print(captions)

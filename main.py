from deepgram_captions.helpers import seconds_to_timestamp
from deepgram_captions.srt import srt
from deepgram_captions.converters import AssemblyAIConverter, DeepgramConverter
import json

# Specify the path to your JSON file
json_file_dg_transcription = "test/dg_transcription.json"
json_file_dg_utterances = "test/dg_utterances.json"
json_file_assemblyai_transcription = "test/assemblyai_transcription.json"
json_file_assemblyai_utterances = "test/assemblyai_utterances.json"

dg_transcription = None
dg_utterances = None
assemblyai_transcription = None
assemblyai_utterances = None
# Open and load the JSON data
with open(json_file_dg_transcription, "r") as json_file:
    dg_transcription = json.load(json_file)

with open(json_file_dg_utterances, "r") as json_file:
    dg_utterances = json.load(json_file)

with open(json_file_assemblyai_transcription, "r") as json_file:
    assemblyai_transcription = json.load(json_file)

with open(json_file_assemblyai_utterances, "r") as json_file:
    assemblyai_utterances = json.load(json_file)


assembly = AssemblyAIConverter(assemblyai_utterances)
captions = srt(assembly)
print(captions)

# deepgram = DeepgramConverter(dg_utterances)
# captions = srt(deepgram)
# print(captions)

# srt_result = srt(dg_utterances)
# print("SRT Result:\n", srt_result)



# result = seconds_to_timestamp(500, "%H:%M:%S,%f")
# print(result)
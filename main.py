from deepgram_captions.helpers import seconds_to_timestamp
from deepgram_captions.srt import srt
import json

# Specify the path to your JSON file
json_file_dg_transcription = "test/dg_transcription.json"
json_file_dg_utterances = "test/dg_utterances.json"

dg_transcription = None
dg_utterances = None
# Open and load the JSON data
with open(json_file_dg_transcription, "r") as json_file:
    dg_transcription = json.load(json_file)

with open(json_file_dg_utterances, "r") as json_file:
    dg_utterances = json.load(json_file)

srt_result = srt(dg_utterances)
# print("SRT Result:\n", srt_result)



# result = seconds_to_timestamp(500, "%H:%M:%S,%f")
# print(result)
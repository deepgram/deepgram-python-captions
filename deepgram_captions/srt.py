from .converters import DeepgramConverter


def srt(transcription_data):
  # check if transcription_data is in deepgram format. If it is, use deepgram_converter to format data
  converter = DeepgramConverter(transcription_data)
  lines = converter.get_lines()
  print(lines)
  
  # if it isn't, use the converter passed in by the user

  # create srt captions

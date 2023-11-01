from .helpers import chunk_array

class DeepgramConverter:
  def __init__(self, dg_response) -> None:
    # get the deepgram response.
    self.response = dg_response

  def get_lines(self, line_length: int = 8):
    results = self.response['results']
    content = []
    # check if response has utterances. If so, loop over each utterance and check if the utterances length is greater than the line_length. If so break down the given utterance.words array into smaller chunks, then push into content array
    if results['utterances']:
      for utterance in results['utterances']:
        if len(utterance['words']) > line_length:
          content.extend(chunk_array(utterance['words'], line_length))
        else:
          content.append(utterance['words'])
    
    # if no utterances, break down results.channels[0].alternatives[0].words into smaller chunks, then push into content array

    else:
      content.extend(chunk_array(results['channels'][0]['alternatives'][0]['words'], line_length))
  
    return content
  
  def get_headers():
    output = []
    # create headers for deepgram captions

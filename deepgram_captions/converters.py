from .helpers import chunk_array, replace_text_with_word


class DeepgramConverter:
    def __init__(self, dg_response):
        self.response = dg_response

    def get_lines(self, line_length: int = 8):
        results = self.response["results"]
        content = []

        if results.get("utterances"):
            for utterance in results["utterances"]:
                if len(utterance["words"]) > line_length:
                    content.extend(chunk_array(utterance["words"], line_length))
                else:
                    content.append(utterance["words"])

        else:
            words = results["channels"][0]["alternatives"][0]["words"]
            diarize = (
                "speaker" in words[0] if words else False
            )  # Check if diarization was used
            buffer = []
            current_speaker = 0

            for word in words:
                if diarize and word.get("speaker", 0) != current_speaker:
                    content.append(buffer)
                    buffer = []

                if len(buffer) == line_length:
                    content.append(buffer)
                    buffer = []

                if diarize:
                    current_speaker = word.get("speaker", 0)

                buffer.append(word)

            content.append(buffer)

        return content

    def get_headers(self):
        output = []

        output.append("NOTE")
        output.append("Transcription provided by Deepgram")

        if self.response.get("metadata"):
            metadata = self.response["metadata"]
            if metadata.get("request_id"):
                output.append(f"Request Id: {metadata['request_id']}")
            if metadata.get("created"):
                output.append(f"Created: {metadata['created']}")
            if metadata.get("duration"):
                output.append(f"Duration: {metadata['duration']}")
            if metadata.get("channels"):
                output.append(f"Channels: {metadata['channels']}")

        return output


class AssemblyAIConverter:
    def __init__(self, assembly_response):
        self.response = assembly_response

    def word_map(self, word):
        return {
            "word": word["text"],
            "start": word["start"],
            "end": word["end"],
            "confidence": word["confidence"],
            "punctuated_word": word["text"],
            "speaker": word["speaker"],
        }

    def get_lines(self, line_length: int = 8):
        results = self.response
        content = []
        if results.get("utterances"):
            for utterance in results["utterances"]:
                if len(utterance["words"]) > line_length:
                    content.extend(
                        chunk_array(
                            [self.word_map(w) for w in utterance["words"]], line_length
                        )
                    )
                else:
                    content.append([self.word_map(w) for w in utterance["words"]])
        else:
            content.extend(
                chunk_array([self.word_map(w) for w in results["words"]], line_length)
            )

        return content


class WhisperTimestampedConverter:
    def __init__(self, whisper_response):
        self.response = whisper_response

    def get_lines(self, line_length: int = 8):
        results = self.response
        content = []
        if results.get("segments"):
            for segment in results["segments"]:
                if len(segment["words"]) > line_length:
                    content.extend(chunk_array(segment["words"], line_length))
                else:
                    content.append(segment["words"])

        res = replace_text_with_word(content)
        return res

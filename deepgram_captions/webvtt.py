from .helpers import seconds_to_timestamp


def webvtt(converter):
    output = []
    output.append("WEBVTT")
    output.append("")

    if hasattr(converter, "get_headers") and callable(
        getattr(converter, "get_headers")
    ):
        output.append("\n".join(converter.get_headers()))

    if hasattr(converter, "get_headers") and callable(
        getattr(converter, "get_headers")
    ):
        output.append("")

    if hasattr(converter, "get_lines") and callable(getattr(converter, "get_lines")):
        lines = converter.get_lines()

        speaker_labels = "speaker" in lines[0][0]

        for words in lines:
            first_word = words[0]
            last_word = words[-1]

            output.append(
                f"{seconds_to_timestamp(first_word['start'])} --> {seconds_to_timestamp(last_word['end'])}"
            )

            line = " ".join(word.get("punctuated_word", word["word"]) for word in words)
            speaker_label = (
                f"<v Speaker {first_word['speaker']}>" if speaker_labels else ""
            )

            output.append(f"{speaker_label}{line}")
            output.append("")

    return "\n".join(output)

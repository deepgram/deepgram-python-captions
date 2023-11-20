from .helpers import seconds_to_timestamp


def srt(converter, line_length=None):
    output = []

    if line_length == None:
        line_length = 8

    lines = converter.get_lines(line_length)
    entry = 1

    current_speaker = None

    for words in lines:
        output.append(str(entry))
        entry += 1

        first_word = words[0]
        last_word = words[-1]

        start_time = seconds_to_timestamp(first_word["start"], "%H:%M:%S,%f")
        end_time = seconds_to_timestamp(last_word["end"], "%H:%M:%S,%f")

        output.append(f"{start_time} --> {end_time}")

        if "speaker" in first_word:
            if current_speaker is None or current_speaker != first_word["speaker"]:
                current_speaker = first_word["speaker"]
                output.append(f"[speaker {current_speaker}]")

        punctuated_words = [word.get("punctuated_word", word["word"]) for word in words]
        output.append(" ".join(punctuated_words))
        output.append("")

    return "\n".join(output)

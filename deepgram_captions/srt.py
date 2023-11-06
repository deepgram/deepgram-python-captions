from .helpers import seconds_to_timestamp


def srt(converter):
    output = []
    lines = converter.get_lines()
    entry = 1

    for words in lines:
        output.append(str(entry))
        entry += 1

        first_word = words[0]
        last_word = words[-1]

        start_time = seconds_to_timestamp(first_word["start"], "%H:%M:%S,%f")
        end_time = seconds_to_timestamp(last_word["end"], "%H:%M:%S,%f")

        output.append(f"{start_time} --> {end_time}")
        punctuated_words = [word.get("punctuated_word", word["word"]) for word in words]
        output.append(" ".join(punctuated_words))
        output.append("")

    return "\n".join(output)

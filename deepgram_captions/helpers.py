from datetime import datetime


def seconds_to_timestamp(seconds, format="%H:%M:%S.%f"):
    seconds = round(seconds, 3)
    dt = datetime.utcfromtimestamp(seconds)
    formatted_time = dt.strftime(format)
    formatted_time = formatted_time[:-3] + formatted_time[-3:].lstrip("0")
    return formatted_time


def chunk_array(arr, length):
    res = []

    for i in range(0, len(arr), length):
        chunk_arr = arr[i : i + length]
        res.append(chunk_arr)

    return res


def replace_text_with_word(content):
    for content_list in content:
        for dictionary in content_list:
            if "text" in dictionary:
                dictionary["word"] = dictionary.pop("text")
    return content

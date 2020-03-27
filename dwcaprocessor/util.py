def clean_record(record):
    return {k: v for k, v in record.items() if v or v == 0}


def string_escape(s):
    return bytes(s, "utf-8").decode("unicode_escape")

def cleanRecord(record):
    return {k: v for k, v in record.items() if v or v == 0}
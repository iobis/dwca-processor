class ExtensionIterator:

    def __init__(self, archive, extension):
        self._archive = archive
        self._extension = extension
        self._position = 0

    def __iter__(self):
        return self

    def next(self):

        # get next line from reader
        # reader needs to be reinitialized and limited to core id

        record = self._extension.reader.getLine(self._position)

        if self.core.type == "Event":
            stack = self._makeStack(record, [
                {
                    "descriptor": self.core,
                    "fk": "eventID",
                    "pk": "parentEventID",
                    "recursive": True
                }
            ])
            logger.debug("Stack :" + json.dumps(stack, indent=2))
            full = self._mergeStack(stack)
        else:
            full = record

        return {
            "source": cleanRecord(record),
            "full": cleanRecord(full)
        }

        self._position += 1
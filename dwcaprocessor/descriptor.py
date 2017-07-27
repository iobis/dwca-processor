import logging

logger = logging.getLogger(__name__)

class FileDescriptor(object):

    def extractTerm(self, input):
        return input.split("/")[-1]

    def __init__(self, xml, id="id"):

        self._encoding = xml["@encoding"].encode("utf-8")
        self._delimiter = xml["@fieldsTerminatedBy"].encode("utf-8").decode("string_escape")
        if xml["@fieldsEnclosedBy"].encode("utf-8").decode("string_escape") != "":
            self._quoteChar = xml["@fieldsEnclosedBy"].encode("utf-8").decode("string_escape")
        else:
            self._quoteChar = None
        self._headerLines = xml["@ignoreHeaderLines"].encode("utf-8")
        self._type = self.extractTerm(xml["@rowType"]).encode("utf-8")
        self._file = xml["files"]["location"].encode("utf-8")
        self._idIndex = int(xml[id]["@index"].encode("utf-8"))

        # set fields
        self._fields = {}
        for f in xml["field"]:
            self._fields[self.extractTerm(f["@term"]).encode("utf-8")] = int(self.extractTerm(f["@index"]).encode("utf-8"))

        # if ID column not in terms list, add "id" field with appropriate index
        if not self._idIndex in self._fields.values():
            self._fields["id"] = self._idIndex

    def __str__(self):
        lines = []
        lines.append("-" * len(self._file))
        lines.append(self._file)
        lines.append("-" * len(self._file))
        lines.append("Type: " + self._type)
        lines.append("ID column: " + str(self._idIndex))
        lines.append("Columns: " + str(self._fields))
        if self.reader is not None:
            lines.append(str(self.reader))
        return "\n".join(lines)

    def __getitem__(self, key):
        return getattr(self, key)

    def __setitem__(self, key, item):
        setattr(self, key, item)
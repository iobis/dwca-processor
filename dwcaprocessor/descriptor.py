import logging

logger = logging.getLogger(__name__)

class FileDescriptor(object):

    def extractTerm(self, input):
        return input.split("/")[-1]

    def __init__(self, xml, id="id"):

        self._encoding = xml["@encoding"]
        self._delimiter = xml["@fieldsTerminatedBy"]
        self._quoteChar = xml["@fieldsEnclosedBy"]
        self._headerLines = xml["@ignoreHeaderLines"]
        self._type = self.extractTerm(xml["@rowType"])
        self._file = xml["files"]["location"]
        self._idIndex = xml[id]["@index"]

        # set fields
        self._fields = {}
        for f in xml["field"]:
            self._fields[self.extractTerm(f["@term"])] = self.extractTerm(f["@index"])

        # todo: add ID field if not yet present, save name of id field

        # if ID column not in terms list, add "id" field with appropriate index
        if not self._idIndex in self._fields.values():
            self._fields["id"] = self._idIndex

    def __str__(self):
        lines = []
        lines.append("-" * len(self._file))
        lines.append(self._file)
        lines.append("-" * len(self._file))
        lines.append("Type: " + self._type)
        lines.append("ID column: " + self._idIndex)
        lines.append("Columns: " + str(self._fields))
        return "\n".join(lines)
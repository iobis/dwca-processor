import logging

logger = logging.getLogger(__name__)

class FileDescriptor(object):

    def extractTerm(self, input):
        return input.split("/")[-1]

    def __init__(self, xml, id="id"):

        self.encoding = xml["@encoding"].encode("utf-8")
        self.delimiter = xml["@fieldsTerminatedBy"].encode("utf-8").decode("string_escape")
        if xml["@fieldsEnclosedBy"].encode("utf-8").decode("string_escape") != "":
            self.quoteChar = xml["@fieldsEnclosedBy"].encode("utf-8").decode("string_escape")
        else:
            self.quoteChar = None
        self.headerLines = xml["@ignoreHeaderLines"].encode("utf-8")
        self.type = self.extractTerm(xml["@rowType"]).encode("utf-8")
        self.file = xml["files"]["location"].encode("utf-8")
        self.idIndex = int(xml[id]["@index"].encode("utf-8"))

        # create fields dict and determine name if identifier field
        self.fields = {}
        for f in xml["field"]:
            fieldName = self.extractTerm(f["@term"]).encode("utf-8")
            fieldIndex = int(self.extractTerm(f["@index"]).encode("utf-8"))
            self.fields[fieldName] = fieldIndex
            if fieldIndex == self.idIndex:
                self.idName = fieldName

        # if identifier column not in terms list, add an "id" field with the appropriate index
        if not self.idIndex in self.fields.values():
            self.fields["id"] = self.idIndex
            self.idName = "id"

    def __iter__(self, coreId=None):
        self.position = 0
        return self

    def next(self):



    def __str__(self):
        lines = []
        lines.append("=" * len(self.file))
        lines.append(self.file)
        lines.append("=" * len(self.file))
        lines.append("Type: " + self.type)
        lines.append("ID column: " + str(self.idIndex) + " (" + self.idName + ")")
        lines.append("Columns: " + str(self.fields))
        if self.reader is not None:
            lines.append(str(self.reader))
        return "\n".join(lines)

    def __getitem__(self, key):
        return getattr(self, key)

    def __setitem__(self, key, item):
        setattr(self, key, item)
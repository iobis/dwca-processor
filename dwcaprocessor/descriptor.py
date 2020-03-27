import logging
from .util import string_escape


logger = logging.getLogger(__name__)


class FileDescriptor(object):

    def extract_term(self, input):
        return input.split("/")[-1]

    def __init__(self, xml, id="id"):

        self.encoding = xml["@encoding"]
        self.delimiter = string_escape(xml["@fieldsTerminatedBy"])
        if xml["@fieldsEnclosedBy"] != "":
                self.quote_char = string_escape(xml["@fieldsEnclosedBy"])
        else:
            self.quote_char = None
        self.header_lines = xml["@ignoreHeaderLines"]
        self.type = self.extract_term(xml["@rowType"])
        self.file = xml["files"]["location"]
        self.id_index = int(xml[id]["@index"])

        # create fields dict and determine name if identifier field
        self.fields = {}
        if "field" in xml:
            if not isinstance(xml["field"], (list,)):
                xml["field"] = [ xml["field"] ]
            for f in xml["field"]:
                if "@index" in f:
                    field_name = self.extract_term(f["@term"])
                    field_index = int(self.extract_term(f["@index"]))
                    self.fields[field_name] = field_index
                    if field_index == self.id_index:
                        self.id_name = field_name

        # if identifier column not in terms list, add an "id" field with the appropriate index
        if not self.id_index in self.fields.values():
            self.fields["id"] = self.id_index
            self.id_name = "id"

    def __iter__(self, core_id=None):
        self._position = 0
        return self

    def next(self):
        if self._position >= len(self.reader):
            raise StopIteration
        else:
            result = self.reader.get_line(self._position)
            self._position += 1
            return result

    def __len__(self):
        return len(self.reader)

    def __str__(self):
        lines = list()
        lines.append("=" * len(self.file))
        lines.append(self.file)
        lines.append("=" * len(self.file))
        lines.append("Type: " + self.type)
        lines.append("ID column: " + str(self.id_index) + " (" + self.id_name + ")")
        lines.append("Columns: " + str(self.fields))
        if self.reader is not None:
            lines.append(str(self.reader))
        return "\n".join(lines)

    def __getitem__(self, key):
        return getattr(self, key)

    def __setitem__(self, key, item):
        setattr(self, key, item)
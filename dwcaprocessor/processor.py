from zipfile import ZipFile
import tempfile
import logging
import shutil
import os
import xmltodict
from .descriptor import FileDescriptor
from csvreader import CSVReader
import json
from .util import clean_record
import copy
from urllib.request import urlopen


logger = logging.getLogger(__name__)


class DwCAProcessor(object):

    def __init__(self, path):
        self._position = None
        self._path = path
        self._temp_dir = tempfile.mkdtemp()
        logger.debug("Temp directory: " + self._temp_dir)
        self._extract()
        self._parse_meta()
        self._read_eml()
        self._index_files()

    def __str__(self):
        lines = list()
        lines.append(str(self.core))
        for e in self.extensions:
            lines.append(str(e))
        return "\n".join(lines)

    def _which_field_to_index(self, descriptor):
        """Determines which fields to index based on core/extension and row type."""
        if descriptor.core:
            if descriptor.type == "Event":
                return list({descriptor.id_name, "eventID", "parentEventID"})
            elif descriptor.type == "Occurrence":
                return list({descriptor.id_name, "occurrenceID"})
            elif descriptor.type == "Taxon":
                return list({descriptor.id_name})
        else:
            if descriptor.type == "Occurrence":
                return list({descriptor.id_name, "occurrenceID"})
            elif descriptor.type == "MeasurementOrFact":
                return list({descriptor.id_name})
            elif descriptor.type == "ExtendedMeasurementOrFact":
                return list({descriptor.id_name, "occurrenceID"})

    def _index_files(self):
        """Index the appropriate columns of the core and extension files."""

        # index core

        i_fields = self._which_field_to_index(self.core)
        self.core["reader"] = CSVReader(self._temp_dir + "/" + self.core.file, delimiter=self.core.delimiter, quote_char=self.core.quote_char, field_names=self.core.fields, index_fields=i_fields)

        # index extensions

        for e in self.extensions:
            e["reader"] = CSVReader(self._temp_dir + "/" + e.file, delimiter=e.delimiter, quote_char=e.quote_char, field_names=e.fields, index_fields=self._which_field_to_index(e))

    def _extract(self):
        """Extract the archive to the temporary directory."""
        if "://" in self._path:
            response = urlopen(self._path)
            with tempfile.NamedTemporaryFile(delete=False) as tmp_file:
                shutil.copyfileobj(response, tmp_file)
                self._path = tmp_file.name
        with ZipFile(self._path, "r") as zipFile:
            zipFile.extractall(self._temp_dir)

    def _parse_meta(self):
        """Parse the archive descriptor XML file."""
        with open(self._temp_dir + "/meta.xml", "r") as metaFile:
            meta = xmltodict.parse(metaFile.read())

            self.core = FileDescriptor(meta["archive"]["core"])
            self.core["core"] = True
            self.extensions = []

            if "extension" in meta["archive"]:

                # handle dict as well as list
                if isinstance(meta["archive"]["extension"], dict):
                    meta["archive"]["extension"] = [meta["archive"]["extension"]]

                for e in meta["archive"]["extension"]:
                    descriptor = FileDescriptor(e, id="coreid")
                    descriptor["core"] = False
                    self.extensions.append(descriptor)

    def core_integrity(self):
        """Check referential integrity of core records."""
        if self.core.type == "Event":
            if "parentEventID" in self.core.reader._indexes:
                for parentEventID in self.core.reader._indexes["parentEventID"]:
                    if parentEventID and not parentEventID in self.core.reader._indexes["eventID"]:
                        yield parentEventID

    def extension_integrity(self, extension):
        """Checks if all IDs in the extension are present in the core."""
        core_id_name = self.core.id_name
        extension_id_name = extension.idName
        for fk in extension.reader._indexes[extension_id_name]:
            if fk and fk not in self.core.reader._indexes[core_id_name]:
                yield fk

    def custom_table_integrity(self, table_a, table_b, field_a, field_b):
        for fk in table_a.reader._indexes[field_a]:
            if fk and fk not in table_b.reader._indexes[field_b]:
                yield fk

    def core_records(self):
        """Core records generator."""
        self._position = -1

        while self._position < len(self.core.reader) - 1:
            self._position += 1
            record = self.core.reader.get_line(self._position)
            # lookup parent records by following the specified steps
            if self.core.type == "Event":
                # lookup parent events in the event table recursively
                steps = [
                    {
                        "descriptor": self.core,
                        "pk": "parentEventID",
                        "fk": "eventID",
                        "recursive": True
                    }
                ]
                stack = self._make_stack(record, steps)
                logger.debug("Stack :" + json.dumps(stack, indent=2))
                full = self._merge_stack(stack, steps)
            else:
                full = record
            yield {
                "source": clean_record(record),
                "full": clean_record(full)
            }

    def extension_records(self, extension):
        """Extension records generator."""
        # get current core record
        core_record = self.core.reader.getLine(self._position)
        for record in extension.reader.getLines(extension["idName"], core_record[self.core["idName"]]):
            if extension.type == "Occurrence" and self.core.type == "Event":
                steps = [
                    {
                        "descriptor": self.core,
                        "pk": extension["idName"],
                        "fk": self.core["idName"],
                        "recursive": False
                    },
                    {
                        "descriptor": self.core,
                        "pk": "parentEventID",
                        "fk": "eventID",
                        "recursive": True
                    }
                ]
                stack = self._make_stack(record, steps)
                full = self._merge_stack(stack, steps)
            elif (extension.type == "MeasurementOrFact" or extension.type == "ExtendedMeasurementOrFact") and self.core.type == "Event":
                steps = [
                    {
                        "descriptor": self.core,
                        "pk": extension["idName"],
                        "fk": self.core["idName"],
                        "recursive": False
                    },
                    {
                        "descriptor": self.core,
                        "pk": "parentEventID",
                        "fk": "eventID",
                        "recursive": True
                    }
                ]
                stack = self._make_stack(record, steps)
                full = self._merge_stack(stack, steps)
            # todo: get selected fields from occurrence core
            #elif (extension.type == "MeasurementOrFact" or extension.type == "ExtendedMeasurementOrFact") and self.core.type == "Occurrence":
            #    steps = [
            #        {
            #            "descriptor": self.core,
            #            "pk": extension["idName"],
            #            "fk": self.core["idName"],
            #            "recursive": False
            #        }
            #    ]
            #    stack = self._makeStack(record, steps)
            #    full = self._mergeStack(stack, steps)
            else:
                full = record
            yield {
                "source": clean_record(record),
                "full": clean_record(full)
            }

    def _make_stack(self, record, steps):
        stack = [copy.deepcopy(record)]
        for step in steps:
            # check if record has key (for example event record without parentEventID
            if not step["pk"] in record:
                return stack
            # make stack
            while True:
                # fetch parent records
                parents = list(step["descriptor"].reader.get_lines(step["fk"], record[step["pk"]]))
                if len(parents) == 0:
                    break
                elif len(parents) == 1:
                    stack.insert(0, parents[0])
                    # make parent master record for next step or iteration
                    record = parents[0]
                    if not step["recursive"]:
                        break
                elif len(parents) > 1:
                    raise RuntimeError("Key " + record[step["pk"]] + " corresponds to multiple parents")
        return stack

    def _merge_stack(self, stack, steps):
        result = {}
        for i in range(len(stack)):
            # merge records but discard None or empty string
            clean = clean_record(stack[i])
            # only pass selected fields
            if i < len(steps):
                if "fields" in steps[i] and steps[i]["fields"] is not None:
                    clean = {k: v for k, v in clean.items() if k in steps[i]["fields"]}
            result.update(clean)
        return result

    def _read_eml(self):
        with open(self._temp_dir + "/eml.xml", "r") as emlFile:
            self.eml = emlFile.read()

    def __del__(self):
        """Clean up the temporary directory."""
        if os.path.exists(self._temp_dir):
            logger.debug("Cleaning up " + self._temp_dir)
            shutil.rmtree(self._temp_dir)

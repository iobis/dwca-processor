from zipfile import ZipFile
import tempfile
import logging
import shutil
import os
import xmltodict
from descriptor import FileDescriptor
from csvreader import CSVReader
import json
from util import cleanRecord
import copy
import urllib2

logger = logging.getLogger(__name__)

class DwCAProcessor(object):

    def __init__(self, path):
        self._path = path
        self._temp_dir = tempfile.mkdtemp()
        logger.debug("Temp directory: " + self._temp_dir)
        self._extract()
        self._parseMeta()
        self._readEML()
        self._indexFiles()

    def __str__(self):
        lines = []
        lines.append(str(self.core))
        for e in self.extensions:
            lines.append(str(e))
        return "\n".join(lines)

    def _whichFieldToIndex(self, descriptor):
        """Determines which fields to index based on core/extension and row type."""
        if (descriptor.core):
            if (descriptor.type == "Event"):
                return list({descriptor.idName, "eventID", "parentEventID"})
            elif (descriptor.type == "Occurrence"):
                return list({descriptor.idName, "occurrenceID"})
            elif (descriptor.type == "Taxon"):
                return list({descriptor.idName})
        else:
            if (descriptor.type == "Occurrence"):
                return list({descriptor.idName, "occurrenceID"})
            elif (descriptor.type == "MeasurementOrFact"):
                return list({descriptor.idName})
            elif (descriptor.type == "ExtendedMeasurementOrFact"):
                return list({descriptor.idName, "occurrenceID"})

    def _indexFiles(self):
        """Index the appropriate columns of the core and extension files."""

        # index core

        iFields = self._whichFieldToIndex(self.core)
        self.core["reader"] = CSVReader(self._temp_dir + "/" + self.core.file, delimiter=self.core.delimiter, quoteChar=self.core.quoteChar, fieldNames=self.core.fields, indexFields=iFields)

        # index extensions

        for e in self.extensions:
            e["reader"] = CSVReader(self._temp_dir + "/" + e.file, delimiter=e.delimiter, quoteChar=e.quoteChar, fieldNames=e.fields, indexFields=self._whichFieldToIndex(e))

    def _extract(self):
        """Extract the archive to the temporary directory."""
        if "://" in self._path:
            response = urllib2.urlopen(self._path)
            with tempfile.NamedTemporaryFile(delete=False) as tmp_file:
                shutil.copyfileobj(response, tmp_file)
                self._path = tmp_file.name
        with ZipFile(self._path, "r") as zipFile:
            zipFile.extractall(self._temp_dir)

    def _parseMeta(self):
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

    def coreIntegrity(self):
        """Check referential integrity of core records."""
        if self.core.type == "Event":
            if "parentEventID" in self.core.reader._indexes:
                for parentEventID in self.core.reader._indexes["parentEventID"]:
                    if parentEventID and not parentEventID in self.core.reader._indexes["eventID"]:
                        yield parentEventID

    def extensionIntegrity(self, extension):
        """Checks if all IDs in the extension are present in the core."""
        coreIDName = self.core.idName
        extensionIDName = extension.idName
        for fk in extension.reader._indexes[extensionIDName]:
            if fk and not fk in self.core.reader._indexes[coreIDName]:
                yield fk

    def customTableIntegrity(self, table_a, table_b, field_a, field_b):
        for fk in table_a.reader._indexes[field_a]:
            if fk and not fk in table_b.reader._indexes[field_b]:
                yield fk

    def coreRecords(self):
        """Core records generator."""
        self._position = -1

        while self._position < len(self.core.reader) - 1:
            self._position += 1
            record = self.core.reader.getLine(self._position)
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
                stack = self._makeStack(record, steps)
                logger.debug("Stack :" + json.dumps(stack, indent=2))
                full = self._mergeStack(stack, steps)
            else:
                full = record
            yield {
                "source": cleanRecord(record),
                "full": cleanRecord(full)
            }

    def extensionRecords(self, extension):
        """Extension records generator."""
        # get current core record
        coreRecord = self.core.reader.getLine(self._position)
        for record in extension.reader.getLines(extension["idName"], coreRecord[self.core["idName"]]):
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
                stack = self._makeStack(record, steps)
                full = self._mergeStack(stack, steps)
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
                stack = self._makeStack(record, steps)
                full = self._mergeStack(stack, steps)
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
                "source": cleanRecord(record),
                "full": cleanRecord(full)
            }

    def _makeStack(self, record, steps):
        stack = [copy.deepcopy(record)]
        for step in steps:
            # check if record has key (for example event record without parentEventID
            if not step["pk"] in record:
                return stack
            # make stack
            while True:
                # fetch parent records
                parents = list(step["descriptor"].reader.getLines(step["fk"], record[step["pk"]]))
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

    def _mergeStack(self, stack, steps):
        result = {}
        for i in range(len(stack)):
            # merge records but discard None or empty string
            clean = cleanRecord(stack[i])
            # only pass selected fields
            if i < len(steps):
                if "fields" in steps[i] and steps[i]["fields"] is not None:
                    clean = {k: v for k, v in clean.items() if k in steps[i]["fields"]}
            result.update(clean)
        return result

    def _readEML(self):
        with open(self._temp_dir + "/eml.xml", "r") as emlFile:
            self.eml = emlFile.read()

    def __del__(self):
        """Clean up the temporary directory."""
        if os.path.exists(self._temp_dir):
            logger.debug("Cleaning up " + self._temp_dir)
            shutil.rmtree(self._temp_dir)

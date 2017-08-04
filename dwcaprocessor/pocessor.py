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

logger = logging.getLogger(__name__)

class DwCAProcessor(object):

    def __init__(self, path):
        self._path = path
        self._temp_dir = tempfile.mkdtemp()
        logger.debug("Temp directory: " + self._temp_dir)
        self._extract()
        self._parseMeta()
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

        self.core["reader"] = CSVReader(self._temp_dir + "/" + self.core.file, delimiter=self.core.delimiter, quoteChar=self.core.quoteChar, fieldNames=self.core.fields, indexFields=self._whichFieldToIndex(self.core))

        # index extensions

        for e in self.extensions:
            e["reader"] = CSVReader(self._temp_dir + "/" + e.file, delimiter=e.delimiter, quoteChar=e.quoteChar, fieldNames=e.fields, indexFields=self._whichFieldToIndex(e))

    def _extract(self):
        """Extract the archive to the temporary directory."""
        with ZipFile(self._path, "r") as zipFile:
            zipFile.extractall(self._temp_dir)

    def _parseMeta(self):
        """Parse the archive descriptor XML file."""
        with open(self._temp_dir + "/meta.xml", "r") as metaFile:
            meta = xmltodict.parse(metaFile.read())

            self.core = FileDescriptor(meta["archive"]["core"])
            self.core["core"] = True
            self.extensions = []

            for e in meta["archive"]["extension"]:
                descriptor = FileDescriptor(e, id="coreid")
                descriptor["core"] = False
                self.extensions.append(descriptor)

    def __iter__(self):
        self._position = 0
        return self

    def next(self):
        if self._position >= len(self.core.reader):
            raise StopIteration
        else:
            record = self.core.reader.getLine(self._position)

            # lookup parent records by following the specified steps
            if self.core.type == "Event":
                # lookup parent events in the event table recursively
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

            self._position += 1
            return {
                "source": cleanRecord(record),
                "full": full
            }

    def _makeStack(self, record, steps):
        stack = [copy.deepcopy(record)]
        for step in steps:
            while True:
                # fetch parent records
                parents = step["descriptor"].reader.getLines(step["fk"], record[step["pk"]])
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

    def _mergeStack(self, stack):
        result = {}
        for record in stack:
            # merge records but discard None or empty string
            result.update(cleanRecord(record))
        return result

    def __del__(self):
        """Clean up the temporary directory."""
        if os.path.exists(self._temp_dir):
            logger.debug("Cleaning up " + self._temp_dir)
            shutil.rmtree(self._temp_dir)
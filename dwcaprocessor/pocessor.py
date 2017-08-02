from zipfile import ZipFile
import tempfile
import logging
import shutil
import os
import xmltodict
from descriptor import FileDescriptor
from csvreader import CSVReader

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
        lines.append(str(self._core))
        for e in self._extensions:
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

        self._core["reader"] = CSVReader(self._temp_dir + "/" + self._core.file, delimiter=self._core.delimiter, quoteChar=self._core.quoteChar, fieldNames=self._core.fields, indexFields=self._whichFieldToIndex(self._core))

        # index extensions

        for e in self._extensions:
            e["reader"] = CSVReader(self._temp_dir + "/" + e.file, delimiter=e.delimiter, quoteChar=e.quoteChar, fieldNames=e.fields, indexFields=self._whichFieldToIndex(e))

    def _extract(self):
        """Extract the archive to the temporary directory."""
        with ZipFile(self._path, "r") as zipFile:
            zipFile.extractall(self._temp_dir)

    def _parseMeta(self):
        """Parse the archive descriptor XML file."""
        with open(self._temp_dir + "/meta.xml", "r") as metaFile:
            meta = xmltodict.parse(metaFile.read())

            self._core = FileDescriptor(meta["archive"]["core"])
            self._core["core"] = True
            self._extensions = []

            for e in meta["archive"]["extension"]:
                descriptor = FileDescriptor(e, id="coreid")
                descriptor["core"] = False
                self._extensions.append(descriptor)

    def __del__(self):
        """Clean up the temporary directory."""
        if os.path.exists(self._temp_dir):
            logger.debug("Cleaning up " + self._temp_dir)
            shutil.rmtree(self._temp_dir)
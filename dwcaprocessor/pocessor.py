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

    def _indexFiles(self):
        """Index the appropriate columns of the core and extension files."""

        self._core["reader"] = CSVReader(self._temp_dir + "/" + self._core._file, delimiter=self._core._delimiter, quoteChar=self._core._quoteChar, fieldNames=self._core._fields)
        for e in self._extensions:
            e["reader"] = CSVReader(self._temp_dir + "/" + e._file, delimiter=e._delimiter, quoteChar=e._quoteChar, fieldNames=e._fields)







    def _extract(self):
        """Extract the archive to the temporary directory."""
        with ZipFile(self._path, "r") as zipFile:
            zipFile.extractall(self._temp_dir)

    def _parseMeta(self):
        """Parse the archive descriptor XML file."""
        with open(self._temp_dir + "/meta.xml", "r") as metaFile:
            meta = xmltodict.parse(metaFile.read())

            self._core = FileDescriptor(meta["archive"]["core"])
            self._extensions = []

            for e in meta["archive"]["extension"]:
                self._extensions.append(FileDescriptor(e, id="coreid"))

    def __del__(self):
        """Clean up the temporary directory."""
        if os.path.exists(self._temp_dir):
            logger.debug("Cleaning up " + self._temp_dir)
            shutil.rmtree(self._temp_dir)
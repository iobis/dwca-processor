from zipfile import ZipFile
import tempfile
import logging
import shutil
import os
import xmltodict
import json

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

        self._fields = []
        for f in xml["field"]:
            self._fields.append({
                self.extractTerm(f["@term"]): self.extractTerm(f["@index"])
            })

class DwCAProcessor(object):

    def __init__(self, path):

        self._path = path
        self._temp_dir = tempfile.mkdtemp()
        logger.debug("Temp directory: " + self._temp_dir)
        self._extract()
        self._parseMeta()

    def _extract(self):
        with ZipFile(self._path, "r") as zipFile:
            zipFile.extractall(self._temp_dir)

    def _parseMeta(self):
        with open(self._temp_dir + "/meta.xml", "r") as metaFile:
            meta = xmltodict.parse(metaFile.read())

            self._core = FileDescriptor(meta["archive"]["core"])
            self._extensions = []

            for e in meta["archive"]["extension"]:
                self._extensions.append(FileDescriptor(e, id="coreid"))

    def __del__(self):
        if os.path.exists(self._temp_dir):
            logger.debug("Cleaning up " + self._temp_dir)
            shutil.rmtree(self._temp_dir)
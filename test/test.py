import unittest
import logging
import sys
import os
from dwcaprocessor import DwCAProcessor


sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../")))
logging.basicConfig(level=logging.INFO)


class TestDwCAProcessor(unittest.TestCase):

    def testNSBS(self):
        archive = DwCAProcessor("./data/archives/dwca-nsbs-v1.6.zip")
        self.assertTrue(archive.eml)
        for core_record in archive.core_records():
            if core_record["source"]["eventID"] == "Cruise1:Station783:Grabbiotic:980_1":
                self.assertTrue("eventDate" not in core_record["source"])
                self.assertTrue("eventDate" in core_record["full"])
                self.assertTrue("decimalLatitude" not in core_record["source"])
                self.assertTrue("decimalLatitude" in core_record["full"])
                break


if __name__ == "__main__":
    unittest.main()
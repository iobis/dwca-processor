import unittest
import logging
import sys
import os
import json
from dwcaprocessor import DwCAProcessor

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../")))
logging.basicConfig(level=logging.INFO)

class TestDwCAProcessor(unittest.TestCase):

    def testNSBS(self):
        archive = DwCAProcessor("./data/archives/dwca-nsbs-v1.6.zip")
        for coreRecord in archive.coreRecords():
            if coreRecord["source"]["eventID"] == "Cruise1:Station783:Grabbiotic:980_1":
                self.assertTrue("eventDate" not in coreRecord["source"])
                self.assertTrue("eventDate" in coreRecord["full"])
                self.assertTrue("decimalLatitude" not in coreRecord["source"])
                self.assertTrue("decimalLatitude" in coreRecord["full"])
                break

if __name__ == "__main__":
    unittest.main()
import unittest
import logging
from dwcaprocessor import DwCAProcessor

logging.basicConfig(level=logging.DEBUG)

class TestDwCAProcessor(unittest.TestCase):

    def testRead(self):

        DwCAProcessor("data/dwca-north_sea_hypbent_com-v1.9.zip")

if __name__ == "__main__":
    unittest.main()
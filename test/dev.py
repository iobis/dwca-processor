import sys
import os
import json
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../")))
from dwcaprocessor import DwCAProcessor


archive = DwCAProcessor("data/occurrence_mof.zip")
print archive
for line in archive:
    print json.dumps(line, indent=2)
    break



for e in archive.extensions:
    print e.type

    for line in archive.extensionIterator(e):
        print json.dumps(line, indent=2)
        break





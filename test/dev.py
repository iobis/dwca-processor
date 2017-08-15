import sys
import os
import json
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../")))
from dwcaprocessor import DwCAProcessor


archive = DwCAProcessor("data/occurrence_mof_2.zip")
#print archive

for coreRecord in archive.coreRecords():
    print json.dumps(coreRecord, indent=2)
    for e in archive.extensions:
        for extensionRecord in archive.extensionRecords(e):
            print json.dumps(extensionRecord, indent=2)
    break



#for e in archive.extensions:
#    print e.type
#    for line in archive.extensionIterator(e):
#        print json.dumps(line, indent=2)
#        break





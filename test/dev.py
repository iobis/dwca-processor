import sys
import os
import json
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../")))
from dwcaprocessor import DwCAProcessor

#f = os.path.join(os.path.dirname(__file__), "data/archives/dwca-maineinvasives-v1.0.zip")
f = "/data/archives/5f1ca9b6ada4b7380a37bd5885f313b8.zip"

archive = DwCAProcessor(f)
#print archive

#for id in archive.coreIntegrity():
#    print id
#for extension in archive.extensions:
#    print extension.type
#    for id in archive.extensionIntegrity(extension):
#        print id
#sys.exit()

for coreRecord in archive.coreRecords():
    print "+++ core: " + archive.core.type
    print json.dumps(coreRecord, indent=2)
    for e in archive.extensions:
        print "--- extension: " + e.type
        for extensionRecord in archive.extensionRecords(e):
            print json.dumps(extensionRecord, indent=2)

#for e in archive.extensions:
#    print e.type
#    for line in archive.extensionIterator(e):
#        print json.dumps(line, indent=2)
#        break





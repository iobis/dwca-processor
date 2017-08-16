import sys
import os
import json
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../")))
from dwcaprocessor import DwCAProcessor


archive = DwCAProcessor("data/event_occurrence_emof.zip")
print archive

count = 0
for coreRecord in archive.coreRecords():
    count += 1
    if count > 20: exit()
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





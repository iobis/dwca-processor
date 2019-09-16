import sys
import os
import json
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../")))
from dwcaprocessor import DwCAProcessor

#filename = "data/archives/dwca-ThorExpedition_EngraulidaeClupeidae-v1.7.zip"
filename = "http://ipt.vliz.be/eurobis/archive.do?r=pohjedatabase&v=1.1"

archive = DwCAProcessor(filename)
#print archive

for id in archive.coreIntegrity():
    print id
for extension in archive.extensions:
    print extension.type
    for id in archive.extensionIntegrity(extension):
        print id

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





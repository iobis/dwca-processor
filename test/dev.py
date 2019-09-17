import sys
import os
import json
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../")))
from dwcaprocessor import DwCAProcessor

filename = "http://ipt.vliz.be/eurobis/archive.do?r=pohjedatabase&v=1.1"
#filename = "http://ipt.iobis.org/mbon/archive.do?r=galapagos&v=1.2"

archive = DwCAProcessor(filename)
#print archive

print "***** Checking core"
for id in archive.coreIntegrity():
    print id
for extension in archive.extensions:
    print "***** Checking " + extension.type
    for id in archive.extensionIntegrity(extension):
        print id

print "***** Checking occurrenceID"

emof = None
occurrence = None
for extension in archive.extensions:
    if extension.type == "Occurrence":
        occurrence = extension
    elif extension.type == "ExtendedMeasurementOrFact":
        emof = extension
for id in archive.customTableIntegrity(emof, occurrence, "occurrenceID", "occurrenceID"):
    print id

sys.exit()










#for coreRecord in archive.coreRecords():
#    print "+++ core: " + archive.core.type
#    print json.dumps(coreRecord, indent=2)
#    for e in archive.extensions:
#        print "--- extension: " + e.type
#        for extensionRecord in archive.extensionRecords(e):
#            print json.dumps(extensionRecord, indent=2)

#for e in archive.extensions:
#    print e.type
#    for line in archive.extensionIterator(e):
#        print json.dumps(line, indent=2)
#        break





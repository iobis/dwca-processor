import sys
import os
import json
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../")))
from dwcaprocessor import DwCAProcessor

filename = "data/dev/dwca-smhi_epibenthos_reg-v1.1-subset.zip"
archive = DwCAProcessor(filename)
print(archive)

############### print structure

for coreRecord in archive.core_records():
    print("+++ core: " + archive.core.type)
    print(json.dumps(coreRecord, indent=2))
    for e in archive.extensions:
        print("--- extension: " + e.type)
        for extensionRecord in archive.extension_records(e):
            print(json.dumps(extensionRecord, indent=2))

sys.exit()

############### checking integrity
# print "***** Checking core"
# for id in archive.coreIntegrity():
#     print id
# for extension in archive.extensions:
#     print "***** Checking " + extension.type
#     for id in archive.extensionIntegrity(extension):
#         print id
# sys.exit()
# print "***** Checking occurrenceID"
# emof = None
# occurrence = None
# for extension in archive.extensions:
#     if extension.type == "Occurrence":
#         occurrence = extension
#     elif extension.type == "ExtendedMeasurementOrFact":
#         emof = extension
# for id in archive.customTableIntegrity(emof, occurrence, "occurrenceID", "occurrenceID"):
#     print id
# sys.exit()










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





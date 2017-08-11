import sys
import os
import json
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../")))
from dwcaprocessor import DwCAProcessor


archive = DwCAProcessor("data/occurrence_mof.zip")
#print archive
#for i, line in enumerate(archive):
#    print json.dumps(line, indent=2)
#    if i > 0:
#        break



for e in archive.extensions:
    print e.type




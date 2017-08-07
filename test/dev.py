# using source instead of installed package
import sys
import os
import json
testdir = os.path.dirname(__file__)
srcdir = "../"
path = os.path.abspath(os.path.join(testdir, srcdir))
print path
sys.path.insert(0, path)
from dwcaprocessor import DwCAProcessor

#archive = DwCAProcessor("data/occurrence_mof.zip")
archive = DwCAProcessor("data/event_occurrence_emof.zip")
print archive

for i, line in enumerate(archive):
    print json.dumps(line, indent=2)
    if i > 0:
        break


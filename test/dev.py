import logging
from dwcaprocessor import DwCAProcessor
import json

logging.basicConfig(level=logging.DEBUG)

#archive = DwCAProcessor("data/dwca-north_sea_hypbent_com-v1.9.zip")
#for i, line in enumerate(archive):
#    print json.dumps(line, indent=2)
#    if i > 100:
#        break

archive = DwCAProcessor("data/dwca-pinna_isotopos-v1.1.zip")
for i, line in enumerate(archive):
    print json.dumps(line, indent=2)
    if i > 100:
        break
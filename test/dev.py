import logging
from dwcaprocessor import DwCAProcessor

logging.basicConfig(level=logging.DEBUG)

archive = DwCAProcessor("data/dwca-north_sea_hypbent_com-v1.9.zip")

i = 0
for line in archive:
    i = i + 1
    if i > 100:
        break
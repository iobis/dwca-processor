# dwca-processor

Parses and denormalizes Darwin Core Archives

```
archive = DwCAProcessor("data/event_occurrence_emof.zip")

for coreRecord in archive.coreRecords():
    print "+++ core: " + archive.core.type
    print json.dumps(coreRecord, indent=2)
    for e in archive.extensions:
        print "--- extension: " + e.type
        for extensionRecord in archive.extensionRecords(e):
            print json.dumps(extensionRecord, indent=2)
```

```
+++ core: Event
{
  "source": {
    "eventID": "Cruise10:Station75:EventSorbeSledge966:Subsample300", 
    "parentEventID": "Cruise10:Station75:EventSorbeSledge966", 
    "id": "Cruise10:Station75:EventSorbeSledge966:Subsample300"
  }, 
  "full": {
    "eventID": "Cruise10:Station75:EventSorbeSledge966:Subsample300", 
    "datasetName": "Hyperbenthic communities of the North Sea", 
    "minimumDepthInMeters": "11.09", 
    "locality": "Station: 120-Ondiep (t-C5s/Kleine Rede swale)", 
    "parentEventID": "Cruise10:Station75:EventSorbeSledge966", 
    "decimalLatitude": "51.18", 
    "id": "Cruise10:Station75:EventSorbeSledge966:Subsample300", 
    "decimalLongitude": "2.70", 
    "maximumDepthInMeters": "11.09", 
    "waterBody": "North Sea", 
    "ownerInstitutionCode": "MARBIOL-Ugent", 
    "eventDate": "1995-03-23 07:56:08Z"
  }
}
--- extension: Occurrence
{
  "source": {
    "eventID": "Cruise10:Station75:EventSorbeSledge966:Subsample300", 
    "scientificNameID": "urn:lsid:marinespecies.org:taxname:127139", 
    "occurrenceID": "Ugenthyperbenthos45979", 
    "basisOfRecord": "HumanObservation", 
    "lifeStage": "Unknown", 
    "sex": "Unknown", 
    "scientificName": "Limanda limanda", 
    "id": "Cruise10:Station75:EventSorbeSledge966:Subsample300"
  }, 
  "full": {
    "eventID": "Cruise10:Station75:EventSorbeSledge966:Subsample300", 
    "scientificNameID": "urn:lsid:marinespecies.org:taxname:127139", 
    "datasetName": "Hyperbenthic communities of the North Sea", 
    "minimumDepthInMeters": "11.09", 
    "locality": "Station: 120-Ondiep (t-C5s/Kleine Rede swale)", 
    "parentEventID": "Cruise10:Station75:EventSorbeSledge966", 
    "basisOfRecord": "HumanObservation", 
    "decimalLatitude": "51.18", 
    "lifeStage": "Unknown", 
    "decimalLongitude": "2.70", 
    "maximumDepthInMeters": "11.09", 
    "waterBody": "North Sea", 
    "id": "Cruise10:Station75:EventSorbeSledge966:Subsample300", 
    "occurrenceID": "Ugenthyperbenthos45979", 
    "ownerInstitutionCode": "MARBIOL-Ugent", 
    "sex": "Unknown", 
    "eventDate": "1995-03-23 07:56:08Z", 
    "scientificName": "Limanda limanda"
  }
}
--- extension: ExtendedMeasurementOrFact
{
  "source": {
    "occurrenceID": "Ugenthyperbenthos45979", 
    "measurementTypeID": "http://vocab.nerc.ac.uk/collection/P01/current/OCOUNT01", 
    "measurementUnitID": "http://vocab.nerc.ac.uk/collection/P06/current/UUUU/", 
    "measurementValue": "1", 
    "measurementUnit": "ind.", 
    "measurementType": "Count (per taxon) of hyperbenthos >1000um in the water column by identification by optical microscopy", 
    "id": "Cruise10:Station75:EventSorbeSledge966:Subsample300"
  }, 
  "full": {
    "occurrenceID": "Ugenthyperbenthos45979", 
    "measurementTypeID": "http://vocab.nerc.ac.uk/collection/P01/current/OCOUNT01", 
    "measurementUnitID": "http://vocab.nerc.ac.uk/collection/P06/current/UUUU/", 
    "measurementValue": "1", 
    "measurementUnit": "ind.", 
    "measurementType": "Count (per taxon) of hyperbenthos >1000um in the water column by identification by optical microscopy", 
    "id": "Cruise10:Station75:EventSorbeSledge966:Subsample300"
  }
}
...
```

```
print archive
```

```
=========
event.txt
=========
Type: Event
ID column: 0 (id)
Columns: {'eventID': 3, 'datasetName': 1, 'minimumDepthInMeters': 8, 'locality': 7, 'parentEventID': 4, 'decimalLatitude': 10, 'footprintWKT': 12, 'decimalLongitude': 11, 'maximumDepthInMeters': 9, 'waterBody': 6, 'id': 0, 'ownerInstitutionCode': 2, 'eventDate': 5}
--------------------------------------------------------------------
/var/folders/v2/ybhcq3bj7b7886l38swjh3tm0000gn/T/tmpRws4LR/event.txt
--------------------------------------------------------------------
Fields: id, datasetName, ownerInstitutionCode, eventID, parentEventID, eventDate, waterBody, locality, minimumDepthInMeters, maximumDepthInMeters, decimalLatitude, decimalLongitude, footprintWKT
Indexed fields: eventID, parentEventID, id
==============
occurrence.txt
==============
Type: Occurrence
ID column: 0 (id)
Columns: {'eventID': 5, 'scientificNameID': 6, 'occurrenceID': 2, 'basisOfRecord': 1, 'lifeStage': 4, 'sex': 3, 'scientificName': 7, 'id': 0}
-------------------------------------------------------------------------
/var/folders/v2/ybhcq3bj7b7886l38swjh3tm0000gn/T/tmpRws4LR/occurrence.txt
-------------------------------------------------------------------------
Fields: id, basisOfRecord, occurrenceID, sex, lifeStage, eventID, scientificNameID, scientificName
Indexed fields: occurrenceID, id
=============================
extendedmeasurementorfact.txt
=============================
Type: ExtendedMeasurementOrFact
ID column: 0 (id)
Columns: {'occurrenceID': 1, 'measurementTypeID': 3, 'measurementUnitID': 7, 'measurementValue': 4, 'measurementUnit': 6, 'id': 0, 'measurementType': 2, 'measurementValueID': 5}
----------------------------------------------------------------------------------------
/var/folders/v2/ybhcq3bj7b7886l38swjh3tm0000gn/T/tmpRws4LR/extendedmeasurementorfact.txt
----------------------------------------------------------------------------------------
Fields: id, occurrenceID, measurementType, measurementTypeID, measurementValue, measurementValueID, measurementUnit, measurementUnitID
Indexed fields: occurrenceID, id
```

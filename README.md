# dwca-processor

Parses and denormalizes Darwin Core Archives

### Processing steps

- Extract archive and parse `meta.xml`.
- Parse and index core (`Occurrence`, `Event`, `Taxon`) and extension (`Occurrence`, `MeasurementOrFact`, `ExtendedMeasurementOrFact`) files using https://github.com/pieterprovoost/csvreader. 
- Process core file, in case of `Event` inherit properties from parent records. Stream raw and processed core records into data store.
- Process extension files. Inherit properties from core file, fields will depend on core and extension row types (e.g. `Event` to `Occurrence`, `Taxon` to `Occurrence`). In case of `ExtendedMeasurementOrFact` also inherit from `Occurrence` extension.
- For simplicity, inheritance happens recursively based on the raw data. This allows iteration over the records regardless of ordering. Stream raw and processed core records into data store.
- if `_id`s need to be aligned between core and extension records, keep an index of parent records.

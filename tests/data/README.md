This folder contains input files to test against. These were generated using the provided `load_fixures.R` script. Each test fixture exists in various formats supported by R: binary/ascii encoded data with varying compression types.

- rdata: Saved R sessions containing the `iris` dataset
- rds: R saves of the `iris` datasets
- types: Results of saving various non-dataframe variable types. The current set of fixture data includes:
  - `types/integer.*`: The integer value 5
  - `types/string.*`: The string value 'test123'
  - `types/integer_vec.*`: The integer vector value [1, 2, 3, 4, 5]

# TODO: maybe this could be merged with `load_fixures.R` as an RMarkdown document

# Operations Center Shapefile Unifier

Combine Shapefiles exported from **John Deere Operations Center** into one **GeoPackage** (`.gpkg`) per client, organization, field, and operation. When matching JSON metadata and a `Machine` column are available, the script adds `MachineSerial` and `OperatorName` to the output.

GeoPackage supports field names longer than the Shapefile format allows and stores each output dataset in a single file.

## Installation

You need Python 3 and the dependencies in [requirements.txt](requirements.txt). Supported Python versions depend on the dependency versions you install.

From the project directory, create and activate a virtual environment:

**Windows (PowerShell):**

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

**Linux / macOS:**

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Install the dependencies:

```bash
python -m pip install -r requirements.txt
```

## Usage

1. Extract the downloaded files into one directory. Keep each `.shp` together with its `.shx` and `.dbf` files, and include its `.prj` file to preserve coordinate reference information. Keep any accompanying JSON metadata in the same directory.
2. Edit the parameters at the top of [unify_shapefiles.py](unify_shapefiles.py):

   ```python
   input_dir = r"path/to/your/files"
   output_dir = f"{input_dir}/unificados"
   ```

   Replace the placeholder with an existing directory. You can set `output_dir` to another destination; the script creates it if needed.

3. Run the script from the project directory:

   ```bash
   python unify_shapefiles.py
   ```

The script prints progress and errors to the terminal. Each successfully processed group produces a `<Client>_<Organization>_<Field>_<Work>.gpkg` file in the output directory.

## Input naming and grouping

Use filenames following this pattern:

```text
Client_Organization_Field_Work_suffix.shp
```

The first four underscore-separated parts identify the output group. Keep underscores out of those individual identifiers so files group as intended. Use lowercase `.shp` and `.json` extensions; the script only searches the input directory itself, without scanning subdirectories.

For example:

```text
input/
├── Client_Org_Field_Work_abc.shp
├── Client_Org_Field_Work_abc.shx
├── Client_Org_Field_Work_abc.dbf
├── Client_Org_Field_Work_abc.prj
├── Client_Org_Field_Work_abc.json
├── Client_Org_Field_Work_def.shp
├── Client_Org_Field_Work_def.shx
├── Client_Org_Field_Work_def.dbf
├── Client_Org_Field_Work_def.prj
└── Client_Org_Field_Work_def.json
```

With the default output setting:

```text
input/unificados/
└── Client_Org_Field_Work.gpkg
```

## JSON metadata

The script selects the first JSON filename whose stem starts with the Shapefile stem. Use the same base name for each pair and avoid multiple JSON candidates with that prefix.

Metadata must contain a `MachineUsage` object keyed by machine ID, for example:

```json
{
  "MachineUsage": {
    "123": {
      "MachineSerial": "EXAMPLE-SERIAL",
      "OperatorName": "Example Operator"
    }
  }
}
```

When the Shapefile contains a `Machine` column, its values are converted to integer IDs and matched against those keys. The script adds `MachineSerial` and `OperatorName`; missing metadata values become empty strings. If there is no matching JSON or no `Machine` column, the file is combined without adding those columns.

## Current limitations

- Files in a group must use the same coordinate reference system (CRS). The script does not reproject them.
- A read or metadata error skips that Shapefile. A group error skips that group's output. Review the terminal messages: the final completion message also appears when errors occurred.
- Files are concatenated without removing duplicate records.
- Existing output files are not explicitly checked before writing. Use a separate output directory when you need to keep a previous run.

## License

This project is licensed under the [MIT License](LICENSE).

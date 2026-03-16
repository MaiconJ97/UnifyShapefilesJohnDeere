
# Operation Center Shapefile Unifier
When downloading work data from **John Deere Operation Center**, each field can come with multiple `.shp` files and a `.json` file containing additional metadata (machine name, operator, etc.). This script consolidates all those files into a single **GeoPackage** (`.gpkg`), automatically adding the machine and operator fields extracted from the JSON.

> GeoPackage was chosen as the output format because it has no character length limitations and handles large volumes of field data more efficiently than Shapefiles.

---

## What does it do?
1. **Scans** the input directory for `.shp` and `.json` files.
2. **Groups** Shapefiles by their naming structure: `Client_Organization_Area_Work_...`
3. **Enriches** each file with `MachineName` and `OperatorName` fields extracted from the corresponding JSON.
4. **Consolidates** all files from the same group into a single GeoPackage (`.gpkg`).

---

## Requirements
- Python 3.9+
- Dependencies listed in `requirements.txt`

## Usage
Edit the variables at the top of `unificarshapefilev2.py`:

```python
input_dir  = "path/to/your/files"   # Folder containing the downloaded .shp and .json files
output_dir = "unified/"              # Folder where the .gpkg files will be saved
```

Then run:
```bash
python unify_shapefiles.py
```

Output files will be saved in `output_dir/` named after their corresponding group.

---
## Expected file structure
**Input:**
├── Client_Org_Field_Work_abc.shp
├── Client_Org_Field_Work_abc.json
├── Client_Org_Field_Work_def.shp
└── Client_Org_Field_Work_def.json

**Output:**
unified/
└── Client_Org_Field_Work.gpkg
---

## License

MIT

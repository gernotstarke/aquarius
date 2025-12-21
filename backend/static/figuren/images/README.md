# Figure Images

Place your PNG or JPG figure images in this directory.

## File Naming Convention

Use lowercase with hyphens, matching the figure name:
- `ballettbein.png`
- `ballettbein-beidbeinig.png`
- `vertikale.png`
- `vertikale-angewinkelt.png`
- `flamingo.png`
- etc.

## After Adding Images

Run the import command to update the database:
```bash
make db-import-figures FILE=data/figuren-kataloge/figuren-v1.0-saison-2024.json
```

The script will:
- Check which images exist
- Update the database with image paths
- Report statistics on found/missing images

## Access Images

Once imported, images are accessible via:
```
http://localhost:8000/static/figuren/images/<filename>.png
```

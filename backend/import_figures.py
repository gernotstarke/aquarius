"""
Import figures from a JSON catalog file into the database.
Usage: python import_figures.py <path-to-json-file>
"""
import sys
import json
from pathlib import Path
from app.database import SessionLocal, engine
from app.models import Figur

def import_figures_from_json(json_path: str):
    """Import figures from JSON catalog into database."""

    # Load JSON catalog
    catalog_path = Path(json_path)
    if not catalog_path.exists():
        print(f"❌ Error: File not found: {json_path}")
        sys.exit(1)

    try:
        with open(catalog_path, 'r', encoding='utf-8') as f:
            katalog = json.load(f)
    except json.JSONDecodeError as e:
        print(f"❌ Error parsing JSON: {e}")
        sys.exit(1)

    figuren_data = katalog.get('figuren', [])

    if not figuren_data:
        print("⚠️  No figures found in JSON catalog")
        return

    print("=" * 60)
    print(f"📋 Importing Figures from JSON Catalog")
    print("=" * 60)
    print(f"   File: {json_path}")
    print(f"   Version: {katalog.get('version', 'N/A')}")
    print(f"   Saison: {katalog.get('saison', 'N/A')}")
    print(f"   Figures to import: {len(figuren_data)}")
    print()

    db = SessionLocal()

    try:
        imported = 0
        updated = 0
        skipped = 0
        bilder_gefunden = 0

        for figur_data in figuren_data:
            figur_id = figur_data.get('id')
            figur_name = figur_data['name']

            # Check if image file exists
            bild_pfad = figur_data.get('bild')
            if bild_pfad:
                vollstaendiger_pfad = Path(__file__).parent / 'static' / bild_pfad
                if not vollstaendiger_pfad.exists():
                    bild_pfad = None
                else:
                    bilder_gefunden += 1

            # Check if figure already exists (by name)
            existing_figur = db.query(Figur).filter(Figur.name == figur_name).first()

            if existing_figur:
                # Update existing figure
                existing_figur.kategorie = figur_data.get('kategorie')
                existing_figur.beschreibung = figur_data.get('beschreibung')
                existing_figur.schwierigkeitsgrad = figur_data.get('schwierigkeitsgrad')
                existing_figur.altersklasse = figur_data.get('altersklasse')
                existing_figur.bild = bild_pfad
                updated += 1
                print(f"   ↻ Updated: {figur_name}")
            else:
                # Create new figure
                neue_figur = Figur(
                    name=figur_name,
                    kategorie=figur_data.get('kategorie'),
                    beschreibung=figur_data.get('beschreibung'),
                    schwierigkeitsgrad=figur_data.get('schwierigkeitsgrad'),
                    altersklasse=figur_data.get('altersklasse'),
                    bild=bild_pfad
                )
                db.add(neue_figur)
                imported += 1
                print(f"   + Created: {figur_name}")

        db.commit()

        print()
        print("=" * 60)
        print("✨ Import Complete!")
        print("=" * 60)
        print(f"   ✓ {imported} figures created")
        print(f"   ↻ {updated} figures updated")
        print(f"   📸 {bilder_gefunden} images found")
        print(f"   ⚠️  {len(figuren_data) - bilder_gefunden} images missing")
        print()

    except Exception as e:
        db.rollback()
        print(f"\n❌ Error importing figures: {e}")
        sys.exit(1)
    finally:
        db.close()

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python import_figures.py <path-to-json-file>")
        print()
        print("Example:")
        print("  python import_figures.py data/figuren-kataloge/figuren-v1.0-saison-2024.json")
        sys.exit(1)

    json_path = sys.argv[1]
    import_figures_from_json(json_path)

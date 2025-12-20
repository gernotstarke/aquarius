"""
Database seeding script for Arqua42 CRUD prototype.
Populates the database with sample data for testing.
"""
import json
import os
from datetime import date, timedelta
from pathlib import Path
from app.database import SessionLocal, engine, Base
from app.models import Saison, Schwimmbad, Wettkampf, Kind, Figur, Anmeldung

# Pfad zum Figurenkatalog
FIGUREN_KATALOG = "data/figuren-kataloge/figuren-v1.0-saison-2024.json"

def reset_database():
    """Drop all tables and recreate them."""
    print("🗑️  Dropping all tables...")
    Base.metadata.drop_all(bind=engine)
    print("🔨 Creating all tables...")
    Base.metadata.create_all(bind=engine)
    print("✅ Database reset complete")

def seed_data():
    """Seed the database with sample data."""
    db = SessionLocal()
    try:
        print("\n📋 Seeding database with sample data...")

        # Create Saisons
        print("\n📅 Creating saisons...")
        saison_2024 = Saison(
            name="Saison 2024/2025",
            from_date=date(2024, 9, 1),
            to_date=date(2025, 6, 30)
        )
        saison_2023 = Saison(
            name="Saison 2023/2024",
            from_date=date(2023, 9, 1),
            to_date=date(2024, 6, 30)
        )
        db.add_all([saison_2024, saison_2023])
        db.commit()
        print(f"   ✓ Created: {saison_2024.name}")
        print(f"   ✓ Created: {saison_2023.name}")

        # Create Schwimmbäder
        print("\n🏊 Creating schwimmbäder...")
        schwimmbad1 = Schwimmbad(
            name="Stadtbad Mitte",
            adresse="Gartenstraße 5, 10115 Berlin",
            phone_no="030 12345678",
            manager="Frau Schmidt"
        )
        schwimmbad2 = Schwimmbad(
            name="Hallenbad Nord",
            adresse="Nordring 42, 13359 Berlin",
            phone_no="030 98765432",
            manager="Herr Müller"
        )
        schwimmbad3 = Schwimmbad(
            name="Schwimmzentrum Süd",
            adresse="Südstraße 18, 12099 Berlin",
            phone_no="030 55512345"
        )
        db.add_all([schwimmbad1, schwimmbad2, schwimmbad3])
        db.commit()
        print(f"   ✓ Created: {schwimmbad1.name}")
        print(f"   ✓ Created: {schwimmbad2.name}")
        print(f"   ✓ Created: {schwimmbad3.name}")

        # Create Wettkämpfe
        print("\n🏆 Creating wettkämpfe...")
        wettkampf1 = Wettkampf(
            name="Herbstcup 2024",
            datum=date(2024, 10, 15),
            max_teilnehmer=120,
            saison_id=saison_2024.id,
            schwimmbad_id=schwimmbad1.id
        )
        wettkampf2 = Wettkampf(
            name="Winterpokal 2024",
            datum=date(2024, 12, 8),
            max_teilnehmer=150,
            saison_id=saison_2024.id,
            schwimmbad_id=schwimmbad2.id
        )
        wettkampf3 = Wettkampf(
            name="Frühjahrsmeeting 2025",
            datum=date(2025, 3, 22),
            max_teilnehmer=100,
            saison_id=saison_2024.id,
            schwimmbad_id=schwimmbad3.id
        )
        wettkampf4 = Wettkampf(
            name="Sommerfest 2025",
            datum=date(2025, 6, 15),
            saison_id=saison_2024.id,
            schwimmbad_id=schwimmbad1.id
        )
        db.add_all([wettkampf1, wettkampf2, wettkampf3, wettkampf4])
        db.commit()
        print(f"   ✓ Created: {wettkampf1.name}")
        print(f"   ✓ Created: {wettkampf2.name}")
        print(f"   ✓ Created: {wettkampf3.name}")
        print(f"   ✓ Created: {wettkampf4.name}")

        # Create Kinder
        print("\n👶 Creating kinder...")
        kind1 = Kind(
            vorname="Anna",
            nachname="Schmidt",
            geburtsdatum=date(2012, 5, 15),
            geschlecht="W",
            verein="SC Neptun Berlin"
        )
        kind2 = Kind(
            vorname="Max",
            nachname="Müller",
            geburtsdatum=date(2013, 8, 22),
            geschlecht="M",
            verein="Schwimmclub Mitte"
        )
        kind3 = Kind(
            vorname="Sophie",
            nachname="Weber",
            geburtsdatum=date(2011, 3, 10),
            geschlecht="W",
            verein="SC Neptun Berlin"
        )
        kind4 = Kind(
            vorname="Leon",
            nachname="Fischer",
            geburtsdatum=date(2014, 11, 5),
            geschlecht="M"
        )
        kind5 = Kind(
            vorname="Emma",
            nachname="Wagner",
            geburtsdatum=date(2012, 7, 18),
            geschlecht="W",
            verein="Wassersportverein Berlin"
        )
        kind6 = Kind(
            vorname="Tim",
            nachname="Hoffmann",
            geburtsdatum=date(2013, 2, 28),
            geschlecht="M",
            verein="Schwimmclub Mitte"
        )
        db.add_all([kind1, kind2, kind3, kind4, kind5, kind6])
        db.commit()
        print(f"   ✓ Created: {kind1.vorname} {kind1.nachname}")
        print(f"   ✓ Created: {kind2.vorname} {kind2.nachname}")
        print(f"   ✓ Created: {kind3.vorname} {kind3.nachname}")
        print(f"   ✓ Created: {kind4.vorname} {kind4.nachname}")
        print(f"   ✓ Created: {kind5.vorname} {kind5.nachname}")
        print(f"   ✓ Created: {kind6.vorname} {kind6.nachname}")

        # Create Figuren (Kunstschwimm-Figuren) from JSON catalog
        print("\n🎯 Creating figuren from JSON catalog...")

        # Load figuren from JSON catalog
        katalog_path = Path(__file__).parent / FIGUREN_KATALOG
        if not katalog_path.exists():
            print(f"   ⚠️  Katalog nicht gefunden: {katalog_path}")
            print("   ℹ️  Verwende leere Figurenliste")
            figuren_data = []
        else:
            with open(katalog_path, 'r', encoding='utf-8') as f:
                katalog = json.load(f)
                figuren_data = katalog.get('figuren', [])
                print(f"   ℹ️  Katalog geladen: Version {katalog.get('version')}, Saison {katalog.get('saison')}")

        figuren = []
        bilder_gefunden = 0
        for figur_data in figuren_data:
            # Check if image file exists
            bild_pfad = figur_data.get('bild')
            if bild_pfad:
                vollstaendiger_pfad = Path(__file__).parent / 'static' / bild_pfad
                if not vollstaendiger_pfad.exists():
                    print(f"   ⚠️  Bild nicht gefunden: {bild_pfad}")
                    bild_pfad = None  # Set to None if file doesn't exist
                else:
                    bilder_gefunden += 1

            figur = Figur(
                name=figur_data['name'],
                kategorie=figur_data.get('kategorie'),
                beschreibung=figur_data.get('beschreibung'),
                schwierigkeitsgrad=figur_data.get('schwierigkeitsgrad'),
                altersklasse=figur_data.get('altersklasse'),
                bild=bild_pfad
            )
            figuren.append(figur)
            db.add(figur)

        db.commit()
        print(f"   ✓ Created {len(figuren)} Figuren")
        print(f"   ✓ {bilder_gefunden} Bilder gefunden, {len(figuren) - bilder_gefunden} fehlen noch")

        # Assign some figures to competitions
        print("\n🔗 Assigning figuren to wettkämpfe...")
        # Herbstcup: Einfache Figuren für Anfänger
        wettkampf1.figuren.extend([f for f in figuren if f.schwierigkeitsgrad <= 13])
        # Winterpokal: Mittelschwere Figuren
        wettkampf2.figuren.extend([f for f in figuren if 12 <= f.schwierigkeitsgrad <= 16])
        # Frühjahrsmeeting: Fortgeschrittene
        wettkampf3.figuren.extend([f for f in figuren if f.schwierigkeitsgrad >= 14])
        # Sommerfest: Alle Figuren
        wettkampf4.figuren.extend(figuren)
        db.commit()
        print(f"   ✓ Herbstcup: {len(wettkampf1.figuren)} Figuren")
        print(f"   ✓ Winterpokal: {len(wettkampf2.figuren)} Figuren")
        print(f"   ✓ Frühjahrsmeeting: {len(wettkampf3.figuren)} Figuren")
        print(f"   ✓ Sommerfest: {len(wettkampf4.figuren)} Figuren")

        # Create some sample registrations
        print("\n📝 Creating anmeldungen...")

        # Only create sample registrations if we have enough figures
        if len(figuren) >= 23:
            # Anna meldet sich für Herbstcup an
            anmeldung1 = Anmeldung(
                kind_id=kind1.id,
                wettkampf_id=wettkampf1.id,
                startnummer=1,
                anmeldedatum=date(2024, 9, 15),
                vorlaeufig=0,
                status="aktiv"
            )
            # Wähle 3 Figuren für Anna
            anmeldung1.figuren.extend([figuren[0], figuren[8], figuren[17]])  # Ballettbein, Flamingo, Hocke
            db.add(anmeldung1)

            # Max für Winterpokal
            anmeldung2 = Anmeldung(
                kind_id=kind2.id,
                wettkampf_id=wettkampf2.id,
                startnummer=1,
                anmeldedatum=date(2024, 10, 1),
                vorlaeufig=0,
                status="aktiv"
            )
            anmeldung2.figuren.extend([figuren[4], figuren[11], figuren[18]])  # Vertikale, Ritter, Pike
            db.add(anmeldung2)

            # Sophie für Frühjahrsmeeting
            anmeldung3 = Anmeldung(
                kind_id=kind3.id,
                wettkampf_id=wettkampf3.id,
                startnummer=1,
                anmeldedatum=date(2025, 2, 10),
                vorlaeufig=0,
                status="aktiv"
            )
            anmeldung3.figuren.extend([figuren[6], figuren[16], figuren[22]])  # Vertikale im Spagat, Spagat zur Vertikalen, Spagat zur Vertikalen
            db.add(anmeldung3)

            db.commit()
            print(f"   ✓ Created 3 Anmeldungen")
        else:
            print(f"   ⚠️  Skipping sample registrations (need at least 23 figures, have {len(figuren)})")

        print("\n✨ Database seeding complete!")
        print(f"\n📊 Summary:")
        print(f"   • {db.query(Saison).count()} Saisons")
        print(f"   • {db.query(Schwimmbad).count()} Schwimmbäder")
        print(f"   • {db.query(Wettkampf).count()} Wettkämpfe")
        print(f"   • {db.query(Kind).count()} Kinder")
        print(f"   • {db.query(Figur).count()} Figuren")
        print(f"   • {db.query(Anmeldung).count()} Anmeldungen")

    except Exception as e:
        print(f"\n❌ Error seeding database: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    print("=" * 60)
    print("Arqua42 Database Seeding")
    print("=" * 60)
    reset_database()
    seed_data()
    print("\n" + "=" * 60)

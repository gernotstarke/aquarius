"""
Database seeding script for Aquarius CRUD prototype.
Populates the database with sample data for testing.
"""
import json
import os
import random
import shutil
from datetime import date, timedelta
from pathlib import Path
from app.database import SessionLocal, engine, Base
from app.models import Saison, Schwimmbad, Wettkampf, Kind, Figur, Anmeldung, User, Verein, Verband, Versicherung
from app.auth import get_password_hash
from app.seed_constants import ensure_verbaende, ensure_versicherungen

# Pfad zum Figurenkatalog
FIGUREN_KATALOG = "data/figuren/figuren-v1.0-saison-2024.json"

# Diverse Vornamen (Deutsch, Schweiz, Migration Background)
VORNAMEN_M = [
    # Deutsch/Schweiz
    "Max", "Felix", "Leon", "Tim", "Lukas", "Jonas", "Noah", "Finn", "Elias", "Ben",
    "Paul", "Luca", "Moritz", "Jan", "Simon", "David", "Niklas", "Alexander", "Jakob",
    # Türkisch
    "Mehmet", "Ali", "Emre", "Ahmet", "Murat", "Cem",
    # Arabisch
    "Mohammed", "Omar", "Yusuf", "Hassan", "Amin",
    # Griechisch
    "Alexandros", "Dimitrios", "Georgios", "Nikos",
    # Italienisch
    "Marco", "Luca", "Giovanni", "Andrea", "Matteo",
    # Spanisch
    "Carlos", "Miguel", "Diego", "Pablo",
]

VORNAMEN_W = [
    # Deutsch/Schweiz
    "Anna", "Sophie", "Emma", "Lena", "Mia", "Laura", "Lea", "Marie", "Sarah", "Lisa",
    "Hannah", "Lara", "Julia", "Nina", "Clara", "Paula", "Emilia", "Amelie",
    # Türkisch
    "Aylin", "Elif", "Zeynep", "Ayse", "Fatma", "Selin",
    # Arabisch
    "Amira", "Layla", "Fatima", "Yasmin", "Nour",
    # Griechisch
    "Elena", "Maria", "Katerina", "Sofia",
    # Italienisch
    "Giulia", "Francesca", "Alessia", "Chiara",
    # Spanisch
    "Carmen", "Elena", "Isabella", "Lucia",
]

NACHNAMEN = [
    # Deutsch/Schweiz
    "Müller", "Schmidt", "Schneider", "Fischer", "Weber", "Meyer", "Wagner", "Becker",
    "Schulz", "Hoffmann", "Schäfer", "Koch", "Bauer", "Richter", "Klein", "Wolf",
    "Schröder", "Neumann", "Schwarz", "Zimmermann", "Braun", "Hofmann", "Hartmann",
    "Lange", "Schmitt", "Werner", "Krause", "Meier", "Lehmann", "Huber", "Mayer",
    # Türkisch
    "Yilmaz", "Kaya", "Demir", "Celik", "Sahin", "Özdemir", "Arslan", "Dogan",
    # Arabisch
    "Al-Ahmad", "Hassan", "Ibrahim", "Khalil", "Mansour", "Nasser",
    # Griechisch
    "Papadopoulos", "Georgiou", "Dimitriou", "Nikolaou",
    # Italienisch
    "Rossi", "Russo", "Ferrari", "Esposito", "Bianchi", "Romano", "Colombo",
    # Spanisch
    "García", "Martínez", "López", "González", "Rodríguez", "Sánchez",
]

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

        # Create Admin User
        print("\n🔑 Creating admin user...")
        admin_password = os.getenv("INITIAL_ADMIN_PASSWORD", "admin")
        admin_user = User(
            username="admin",
            full_name="System Administrator",
            hashed_password=get_password_hash(admin_password),
            role="ROOT",
            is_active=True
        )
        db.add(admin_user)
        db.commit()
        print(f"   ✓ Created user: admin (Role: ROOT)")
        if admin_password == "admin":
             print("   ⚠️  Using default password 'admin'. Change this in production!")

        # Create Verbände (constant data)
        print("\n🏢 Creating verbände...")
        verbaende_created, verbaende_total = ensure_verbaende(db)
        print(f"   ✓ Verbände loaded: {verbaende_created} new, {verbaende_total} total")

        # Create Versicherungen (constant data)
        print("\n🛡️  Creating versicherungen...")
        versicherungen_created, versicherungen_total = ensure_versicherungen(db)
        print(f"   ✓ Versicherungen loaded: {versicherungen_created} new, {versicherungen_total} total")

        # Create Saisons
        print("\n📅 Creating saisons...")
        saisons = [
            Saison(
                name="Winter 25/26",
                from_date=date(2025, 11, 1),
                to_date=date(2026, 2, 28)
            ),
            Saison(
                name="Frühjahrsmeeting 26",
                from_date=date(2026, 3, 1),
                to_date=date(2026, 5, 31)
            ),
            Saison(
                name="Sommerfest 26",
                from_date=date(2026, 6, 1),
                to_date=date(2026, 8, 31)
            ),
            Saison(
                name="Herbstpokal 26",
                from_date=date(2026, 9, 1),
                to_date=date(2026, 10, 31)
            ),
        ]
        db.add_all(saisons)
        db.commit()
        for saison in saisons:
            print(f"   ✓ Created: {saison.name}")

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

        # Create Vereine
        print("\n🏊 Creating vereine...")
        verein1 = Verein(
            name="SC Neptun Berlin",
            ort="Berlin",
            register_id="VR 12345",
            contact="info@neptun-berlin.de"
        )
        verein2 = Verein(
            name="Schwimmclub Mitte",
            ort="Berlin",
            register_id="VR 67890",
            contact="kontakt@sc-mitte.de"
        )
        verein3 = Verein(
            name="Wassersportverein Berlin",
            ort="Berlin",
            register_id="VR 11223",
            contact="buero@wsv-berlin.de"
        )

        db.add_all([verein1, verein2, verein3])
        db.commit()
        print(f"   ✓ Created: {verein1.name}")
        print(f"   ✓ Created: {verein2.name}")
        print(f"   ✓ Created: {verein3.name}")
        print(f"   ✓ Vereine total: {db.query(Verein).count()}")

        # Create Wettkämpfe
        print("\n🏆 Creating wettkämpfe...")
        wettkampf1 = Wettkampf(
            name="Wintercup 2025",
            datum=date(2025, 12, 8),
            max_teilnehmer=120,
            saison_id=saisons[0].id,
            schwimmbad_id=schwimmbad1.id
        )
        wettkampf2 = Wettkampf(
            name="Frühjahrsmeeting 2026",
            datum=date(2026, 4, 15),
            max_teilnehmer=150,
            saison_id=saisons[1].id,
            schwimmbad_id=schwimmbad2.id
        )
        wettkampf3 = Wettkampf(
            name="Sommerfest 2026",
            datum=date(2026, 7, 10),
            max_teilnehmer=100,
            saison_id=saisons[2].id,
            schwimmbad_id=schwimmbad3.id
        )
        wettkampf4 = Wettkampf(
            name="Herbstpokal 2026",
            datum=date(2026, 10, 5),
            saison_id=saisons[3].id,
            schwimmbad_id=schwimmbad1.id
        )
        db.add_all([wettkampf1, wettkampf2, wettkampf3, wettkampf4])
        db.commit()
        print(f"   ✓ Created: {wettkampf1.name}")
        print(f"   ✓ Created: {wettkampf2.name}")
        print(f"   ✓ Created: {wettkampf3.name}")
        print(f"   ✓ Created: {wettkampf4.name}")

        # Create Kinder (50 with diverse names)
        print("\n👶 Creating 50 kinder with diverse backgrounds...")

        # Get all Vereine and Verbände for random assignment
        all_vereine = db.query(Verein).all()
        all_verbaende = db.query(Verband).all()

        kinder = []
        for i in range(50):
            # Random gender
            geschlecht = random.choice(["M", "W"])
            vorname = random.choice(VORNAMEN_M if geschlecht == "M" else VORNAMEN_W)
            nachname = random.choice(NACHNAMEN)

            # Random birth date between 2010 and 2016
            year = random.randint(2010, 2016)
            month = random.randint(1, 12)
            day = random.randint(1, 28)  # Safe for all months
            geburtsdatum = date(year, month, day)

            # Randomly assign to Verein (70%), Verband (25%), or neither (5%)
            rand = random.random()
            if rand < 0.70 and all_vereine:
                # Assign to Verein
                kind = Kind(
                    vorname=vorname,
                    nachname=nachname,
                    geburtsdatum=geburtsdatum,
                    geschlecht=geschlecht,
                    verein_id=random.choice(all_vereine).id
                )
            elif rand < 0.95 and all_verbaende:
                # Assign to Verband
                kind = Kind(
                    vorname=vorname,
                    nachname=nachname,
                    geburtsdatum=geburtsdatum,
                    geschlecht=geschlecht,
                    verband_id=random.choice(all_verbaende).id
                )
            else:
                # No affiliation
                kind = Kind(
                    vorname=vorname,
                    nachname=nachname,
                    geburtsdatum=geburtsdatum,
                    geschlecht=geschlecht
                )

            kinder.append(kind)
            db.add(kind)

        db.commit()

        # Count assignments
        verein_count = sum(1 for k in kinder if k.verein_id is not None)
        verband_count = sum(1 for k in kinder if k.verband_id is not None)
        no_affiliation = len(kinder) - verein_count - verband_count

        print(f"   ✓ Created 50 Kinder:")
        print(f"      • {verein_count} assigned to Vereine")
        print(f"      • {verband_count} assigned to Verbände")
        print(f"      • {no_affiliation} without affiliation")

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
            # Handle image: find relative to JSON file, copy to static/figuren/
            bild_pfad = figur_data.get('bild')
            if bild_pfad:
                # Source: relative to JSON file (e.g., data/figuren/images/ballettbein.png)
                source_bild = katalog_path.parent / bild_pfad

                if source_bild.exists():
                    # Destination: static/figuren/<bild_pfad> (e.g., static/figuren/images/ballettbein.png)
                    dest_bild = Path(__file__).parent / 'static' / 'figuren' / bild_pfad

                    # Create destination directory if needed
                    dest_bild.parent.mkdir(parents=True, exist_ok=True)

                    # Copy image file
                    shutil.copy2(source_bild, dest_bild)

                    # Store relative path in DB: figuren/<bild_pfad>
                    bild_pfad = f"figuren/{bild_pfad}"
                    bilder_gefunden += 1
                else:
                    print(f"   ⚠️  Bild nicht gefunden: {source_bild}")
                    bild_pfad = None
            else:
                bild_pfad = None

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

        # Only create sample registrations if we have enough figures and kinder
        if len(figuren) >= 23 and len(kinder) >= 10:
            # Create 5-10 random registrations
            num_anmeldungen = random.randint(5, 10)
            for i in range(num_anmeldungen):
                kind = random.choice(kinder[:20])  # Use first 20 kinder
                wettkampf = random.choice([wettkampf1, wettkampf2, wettkampf3, wettkampf4])

                anmeldung = Anmeldung(
                    kind_id=kind.id,
                    wettkampf_id=wettkampf.id,
                    startnummer=i + 1,
                    anmeldedatum=wettkampf.datum - timedelta(days=random.randint(30, 90)),
                    vorlaeufig=0,
                    status="aktiv"
                )

                # Select 3 random figures from the competition's allowed figures
                if len(wettkampf.figuren) >= 3:
                    selected_figuren = random.sample(wettkampf.figuren, 3)
                    anmeldung.figuren.extend(selected_figuren)

                db.add(anmeldung)

            db.commit()
            print(f"   ✓ Created {num_anmeldungen} Anmeldungen")
        else:
            print(f"   ⚠️  Skipping sample registrations (need at least 23 figures and 10 kinder)")

        print("\n✨ Database seeding complete!")
        print(f"\n📊 Summary:")
        print(f"   • {db.query(User).count()} Users")
        print(f"   • {db.query(Verband).count()} Verbände")
        print(f"   • {db.query(Verein).count()} Vereine")
        print(f"   • {db.query(Saison).count()} Saisons")
        print(f"   • {db.query(Schwimmbad).count()} Schwimmbäder")
        print(f"   • {db.query(Verein).count()} Vereine")
        print(f"   • {db.query(Verband).count()} Verbände")
        print(f"   • {db.query(Versicherung).count()} Versicherungen")
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
    print("Aquarius Database Seeding")
    print("=" * 60)
    reset_database()
    seed_data()
    print("\n" + "=" * 60)

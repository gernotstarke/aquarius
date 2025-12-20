"""
Database seeding script for Arqua42 CRUD prototype.
Populates the database with sample data for testing.
"""
from datetime import date, timedelta
from app.database import SessionLocal, engine, Base
from app.models import Saison, Schwimmbad, Wettkampf, Kind, Figur, Anmeldung

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

        # Create Figuren (Kunstschwimm-Figuren)
        print("\n🎯 Creating figuren...")
        figuren_data = [
            ("Ballettbein", "Ballettbein", "Ein Bein senkrecht gestreckt aus dem Wasser, Körper stabil", 12, 8),
            ("Ballettbein beidbeinig", "Ballettbein", "Beide Beine senkrecht gestreckt", 15, 10),
            ("Ballettbein angewinkelt", "Ballettbein", "Ein Bein gestreckt, ein Bein angewinkelt", 13, 9),
            ("Ballettbein gestreckt", "Ballettbein", "Fokus auf maximale Streckung und Höhe", 14, 10),
            ("Vertikale", "Vertikale", "Beide Beine senkrecht gestreckt, Kopf nach unten", 16, 9),
            ("Vertikale angewinkelt", "Vertikale", "Vertikale mit angewinkeltem Bein", 17, 10),
            ("Vertikale im Spagat", "Vertikale", "Vertikale mit gespreizten Beinen", 19, 11),
            ("Vertikale beidbeinig", "Vertikale", "Klassische doppelte Beinführung", 16, 9),
            ("Flamingo", "Flamingo", "Ein Bein angewinkelt, ein Bein gestreckt", 11, 8),
            ("Flamingo angewinkelt", "Flamingo", "Variante mit stärkerer Beugung", 12, 8),
            ("Flamingo zur Vertikalen", "Flamingo", "Übergang von Flamingo in Vertikale", 16, 10),
            ("Ritter", "Ritter", "Ein Bein senkrecht, ein Bein horizontal", 13, 9),
            ("Ritter angewinkelt", "Ritter", "Variante mit angewinkeltem Bein", 14, 9),
            ("Ritter zur Vertikalen", "Ritter", "Übergang von Ritter in Vertikale", 17, 10),
            ("Spagat", "Spagat", "Beine im 180°-Winkel gespreizt", 14, 9),
            ("Spagat angewinkelt", "Spagat", "Spagat mit angewinkeltem Bein", 15, 10),
            ("Spagat zur Vertikalen", "Spagat", "Übergang vom Spagat in Vertikale", 18, 11),
            ("Hocke", "Grundposition", "Knie zur Brust gezogen, kompakte Position", 10, 8),
            ("Pike", "Grundposition", "Gestreckte Beine, Oberkörper nach unten", 12, 9),
            ("Strecklage", "Grundposition", "Körper vollständig gestreckt an der Wasseroberfläche", 11, 8),
            ("Umgekehrte Pike", "Grundposition", "Pike-Position mit Kopf nach unten", 15, 10),
            ("Ballettbein zur Vertikalen", "Kombination", "Übergang vom Ballettbein in Vertikale", 17, 10),
            ("Spagat zur Vertikalen", "Kombination", "Übergang vom Spagat in Vertikale", 18, 11),
            ("Ritter zur Vertikalen", "Kombination", "Übergang vom Ritter in Vertikale", 17, 10),
            ("Flamingo zur Vertikalen", "Kombination", "Übergang vom Flamingo in Vertikale", 16, 10),
            ("Umgekehrte Pike zur Vertikalen", "Kombination", "Übergang von umgekehrter Pike in Vertikale", 19, 11),
        ]

        figuren = []
        for name, kategorie, beschreibung, schwierigkeitsgrad, min_alter in figuren_data:
            figur = Figur(
                name=name,
                kategorie=kategorie,
                beschreibung=beschreibung,
                schwierigkeitsgrad=schwierigkeitsgrad,
                min_alter=min_alter,
                bild=None  # Wird später nachgepflegt
            )
            figuren.append(figur)
            db.add(figur)

        db.commit()
        print(f"   ✓ Created {len(figuren)} Figuren")

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

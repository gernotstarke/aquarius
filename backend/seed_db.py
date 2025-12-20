"""
Database seeding script for Arqua42 CRUD prototype.
Populates the database with sample data for testing.
"""
from datetime import date, timedelta
from app.database import SessionLocal, engine, Base
from app.models import Saison, Schwimmbad, Wettkampf, Kind

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

        print("\n✨ Database seeding complete!")
        print(f"\n📊 Summary:")
        print(f"   • {db.query(Saison).count()} Saisons")
        print(f"   • {db.query(Schwimmbad).count()} Schwimmbäder")
        print(f"   • {db.query(Wettkampf).count()} Wettkämpfe")
        print(f"   • {db.query(Kind).count()} Kinder")

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

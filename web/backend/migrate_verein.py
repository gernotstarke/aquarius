"""
Migration script to add Verein entity and update Kind table.

This script:
1. Creates the verein table if it doesn't exist
2. Adds verein_id column to kind table
3. Drops the old verein string column from kind table
"""
import os
import sys
from sqlalchemy import create_engine, text, inspect
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get database configuration
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./arqua42.db")
TURSO_AUTH_TOKEN = os.getenv("TURSO_AUTH_TOKEN")

# Create engine
connect_args = {}
if DATABASE_URL.startswith("libsql://"):
    connect_args = {
        "check_same_thread": False,
        "connect_args": {"auth_token": TURSO_AUTH_TOKEN} if TURSO_AUTH_TOKEN else {}
    }
    # Convert libsql:// to sqlite:// for sqlalchemy, but keep the full URL
    print(f"🔧 Connecting to Turso database...")
else:
    connect_args = {"check_same_thread": False}
    print(f"🔧 Connecting to local SQLite database...")

engine = create_engine(
    DATABASE_URL.replace("libsql://", "sqlite+libsql://") if DATABASE_URL.startswith("libsql://") else DATABASE_URL,
    connect_args=connect_args,
    echo=True
)

def run_migration():
    """Run the migration."""
    with engine.connect() as conn:
        inspector = inspect(engine)

        # Check if verein table exists
        if 'verein' not in inspector.get_table_names():
            print("\n✓ Creating verein table...")
            conn.execute(text("""
                CREATE TABLE verein (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name VARCHAR NOT NULL,
                    ort VARCHAR NOT NULL,
                    register_id VARCHAR NOT NULL,
                    contact VARCHAR NOT NULL
                )
            """))
            conn.execute(text("CREATE INDEX ix_verein_id ON verein (id)"))
            conn.execute(text("CREATE INDEX ix_verein_name ON verein (name)"))
            conn.commit()
            print("✓ Verein table created successfully")
        else:
            print("✓ Verein table already exists")

        # Check current kind table structure
        kind_columns = {col['name'] for col in inspector.get_columns('kind')}
        print(f"\n📊 Current kind table columns: {kind_columns}")

        # Add verein_id column if it doesn't exist
        if 'verein_id' not in kind_columns:
            print("\n✓ Adding verein_id column to kind table...")
            conn.execute(text("""
                ALTER TABLE kind ADD COLUMN verein_id INTEGER
            """))
            conn.commit()
            print("✓ verein_id column added successfully")
        else:
            print("✓ verein_id column already exists")

        # SQLite doesn't support DROP COLUMN directly, so we need to recreate the table
        # But first, let's check if the old verein column exists
        if 'verein' in kind_columns and 'verein_id' in kind_columns:
            print("\n⚠️  Both 'verein' (string) and 'verein_id' columns exist.")
            print("⚠️  To remove the old 'verein' column, we need to recreate the kind table.")
            print("⚠️  This will preserve all data but requires careful handling.")

            response = input("\nDo you want to remove the old 'verein' string column? (yes/no): ")
            if response.lower() == 'yes':
                print("\n✓ Recreating kind table without old verein column...")

                # Create new table with correct schema
                conn.execute(text("""
                    CREATE TABLE kind_new (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        vorname VARCHAR NOT NULL,
                        nachname VARCHAR NOT NULL,
                        geburtsdatum DATE NOT NULL,
                        geschlecht VARCHAR(1),
                        verein_id INTEGER,
                        FOREIGN KEY (verein_id) REFERENCES verein(id)
                    )
                """))

                # Copy data from old table to new table
                conn.execute(text("""
                    INSERT INTO kind_new (id, vorname, nachname, geburtsdatum, geschlecht, verein_id)
                    SELECT id, vorname, nachname, geburtsdatum, geschlecht, verein_id
                    FROM kind
                """))

                # Drop old table
                conn.execute(text("DROP TABLE kind"))

                # Rename new table to kind
                conn.execute(text("ALTER TABLE kind_new RENAME TO kind"))

                # Recreate indexes
                conn.execute(text("CREATE INDEX ix_kind_id ON kind (id)"))
                conn.execute(text("CREATE INDEX ix_kind_nachname ON kind (nachname)"))

                conn.commit()
                print("✓ Kind table recreated successfully without old verein column")
            else:
                print("⚠️  Skipped removing old verein column. Both columns will coexist.")

        print("\n✅ Migration completed successfully!")

if __name__ == "__main__":
    try:
        print("🚀 Starting migration...")
        print("=" * 60)
        run_migration()
        print("=" * 60)
        print("✅ All done! You can now restart your application.")
    except Exception as e:
        print(f"\n❌ Migration failed: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        sys.exit(1)

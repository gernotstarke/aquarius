"""
Database migration script for adding new fields to existing tables.
This handles schema changes without dropping existing data.
"""
import os
from sqlalchemy import text, inspect
from app.database import SessionLocal, engine

def column_exists(table_name: str, column_name: str) -> bool:
    """Check if a column exists in a table."""
    inspector = inspect(engine)
    columns = [col['name'] for col in inspector.get_columns(table_name)]
    return column_name in columns

def run_migration():
    """Run database migrations for new fields."""
    db = SessionLocal()

    try:
        print("🔄 Starting database migration...")
        print("=" * 60)

        # Migration 1: Add email to users table
        if not column_exists('users', 'email'):
            print("\n📝 Adding 'email' column to 'users' table...")
            db.execute(text("ALTER TABLE users ADD COLUMN email VARCHAR"))
            db.execute(text("CREATE INDEX IF NOT EXISTS ix_users_email ON users(email)"))
            db.commit()
            print("   ✅ Added 'email' to users")
        else:
            print("\n⏭️  'email' already exists in 'users' table")

        # Migration 2: Add email and hashed_password to kind table
        if not column_exists('kind', 'email'):
            print("\n📝 Adding 'email' column to 'kind' table...")
            db.execute(text("ALTER TABLE kind ADD COLUMN email VARCHAR"))
            db.execute(text("CREATE INDEX IF NOT EXISTS ix_kind_email ON kind(email)"))
            db.commit()
            print("   ✅ Added 'email' to kind")
        else:
            print("\n⏭️  'email' already exists in 'kind' table")

        if not column_exists('kind', 'hashed_password'):
            print("\n📝 Adding 'hashed_password' column to 'kind' table...")
            db.execute(text("ALTER TABLE kind ADD COLUMN hashed_password VARCHAR"))
            db.commit()
            print("   ✅ Added 'hashed_password' to kind")
        else:
            print("\n⏭️  'hashed_password' already exists in 'kind' table")

        # Migration 3: Add min_alter to figur table (if not exists)
        if not column_exists('figur', 'min_alter'):
            print("\n📝 Adding 'min_alter' column to 'figur' table...")
            db.execute(text("ALTER TABLE figur ADD COLUMN min_alter INTEGER"))
            db.commit()
            print("   ✅ Added 'min_alter' to figur")
        else:
            print("\n⏭️  'min_alter' already exists in 'figur' table")

        print("\n" + "=" * 60)
        print("✅ Migration completed successfully!")
        print("\nℹ️  Note: User roles should be updated manually:")
        print("   - Old roles: ROOT, PLANER, OFFIZIELLER")
        print("   - New roles: ADMIN, CLEO, VERWALTUNG, OFFIZIELLE, TEILNEHMENDE")
        print("\n   Update existing users with:")
        print("   UPDATE users SET role = 'ADMIN' WHERE role = 'ROOT';")
        print("   UPDATE users SET role = 'VERWALTUNG' WHERE role = 'PLANER';")
        print("   UPDATE users SET role = 'OFFIZIELLE' WHERE role = 'OFFIZIELLER';")

    except Exception as e:
        print(f"\n❌ Migration failed: {e}")
        db.rollback()
        raise
    finally:
        db.close()

if __name__ == "__main__":
    run_migration()

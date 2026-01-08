"""
Database migration script to add app user permission columns.

Adds is_app_user, can_read_all, and can_write_all columns to users table.
Handles both fresh installs and existing databases.
"""
import os
import sys
from sqlalchemy import text
from app.database import engine, SessionLocal
from app import models, auth

def migrate_app_user_columns():
    """Add app user permission columns to users table if they don't exist."""
    
    db = SessionLocal()
    try:
        # Check database type
        database_url = os.getenv("DATABASE_URL", "sqlite:///./aquarius.db")
        is_sqlite = "sqlite" in database_url
        
        if is_sqlite:
            # SQLite: Check if columns exist
            result = db.execute(text("PRAGMA table_info(users)")).fetchall()
            existing_columns = {col[1] for col in result}
            
            columns_to_add = [
                ("is_app_user", "BOOLEAN DEFAULT 0"),
                ("can_read_all", "BOOLEAN DEFAULT 1"),
                ("can_write_all", "BOOLEAN DEFAULT 0"),
            ]
            
            for col_name, col_def in columns_to_add:
                if col_name not in existing_columns:
                    print(f"  Adding column: {col_name}")
                    db.execute(text(f"ALTER TABLE users ADD COLUMN {col_name} {col_def}"))
            
            db.commit()
            print("✓ SQLite migration complete")
        else:
            print("ℹ️  Using non-SQLite database (Turso/libSQL). Columns should already exist.")
            print("   If this is a fresh database, tables will be created automatically.")
    
    except Exception as e:
        print(f"✗ Migration error: {e}")
        db.rollback()
        sys.exit(1)
    finally:
        db.close()


def create_default_app_user():
    """Create default app user for development mode if ENABLE_APP_AUTH=false."""
    enable_auth = os.getenv("ENABLE_APP_AUTH", "false").lower() == "true"
    
    if enable_auth:
        print("ℹ️  ENABLE_APP_AUTH=true (production mode), skipping default user creation")
        return
    
    db = SessionLocal()
    try:
        default_username = os.getenv("DEFAULT_APP_USER", "testuser")
        
        # Check if user exists
        user = db.query(models.User).filter(
            models.User.username == default_username
        ).first()
        
        if user:
            print(f"ℹ️  Default user '{default_username}' already exists")
            # Ensure it has correct permissions
            if not user.is_app_user or not user.can_write_all:
                user.is_app_user = True
                user.can_write_all = True
                user.can_read_all = True
                db.commit()
                print(f"  Updated permissions for '{default_username}'")
        else:
            # Create default user
            user = models.User(
                username=default_username,
                full_name="Default App User (Dev Mode)",
                hashed_password=auth.get_password_hash("dev-password"),
                role="OFFIZIELLER",
                is_app_user=True,
                can_read_all=True,
                can_write_all=True,
                is_active=True,
            )
            db.add(user)
            db.commit()
            print(f"✓ Created default user '{default_username}'")
            print(f"  Password: dev-password")
            print(f"  Permissions: read + write")
    
    except Exception as e:
        print(f"✗ Error creating default user: {e}")
        db.rollback()
        sys.exit(1)
    finally:
        db.close()


if __name__ == "__main__":
    print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    print("📊 App User Migration")
    print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    print()
    
    print("Step 1: Adding database columns...")
    migrate_app_user_columns()
    print()
    
    print("Step 2: Creating default app user (if dev mode)...")
    create_default_app_user()
    print()
    
    print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    print("✅ Migration complete!")
    print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")

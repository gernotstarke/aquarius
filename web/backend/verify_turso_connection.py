#!/usr/bin/env python3
"""Verify Turso database connection."""
import os
import sys
from dotenv import load_dotenv


def verify_turso_connection():
    """Verify connection to Turso database using environment variables."""
    load_dotenv()

    database_url = os.getenv("DATABASE_URL")
    auth_token = os.getenv("TURSO_AUTH_TOKEN")

    print("=" * 60)
    print("Turso Connection Verification")
    print("=" * 60)

    if not database_url:
        print("ERROR: DATABASE_URL not found in environment.")
        return False

    if not database_url.startswith("libsql://"):
        print(f"WARNING: DATABASE_URL doesn't look like Turso URL")
        print(f"  Current: {database_url}")
        print(f"  Expected: libsql://your-database.turso.io")

    if not auth_token:
        print("WARNING: TURSO_AUTH_TOKEN not set. Connection may fail.")

    # Extract hostname from libsql:// URL
    # libsql://aquarius-gernotstarke.aws-eu-west-1.turso.io -> aquarius-gernotstarke.aws-eu-west-1.turso.io
    if database_url.startswith("libsql://"):
        hostname = database_url.replace("libsql://", "")
    else:
        hostname = database_url

    # Build SQLAlchemy URL with secure=true for remote connections
    sa_url = f"sqlite+libsql://{hostname}?secure=true"

    print(f"  Target: {database_url}")
    print(f"  SQLAlchemy URL: {sa_url}")
    print(f"  Auth token: {'[set]' if auth_token else '[not set]'}")

    try:
        from sqlalchemy import create_engine, text

        print("\nConnecting...")
        engine = create_engine(
            sa_url,
            connect_args={"auth_token": auth_token} if auth_token else {},
        )

        with engine.connect() as conn:
            print("  Connection established")

            print("Executing 'SELECT 1'...")
            result = conn.execute(text("SELECT 1")).scalar()

            if result == 1:
                print("  Query successful")
            else:
                print(f"  Unexpected result: {result}")
                return False

        print("\nVERIFICATION SUCCESSFUL")
        print("  Your application can connect to Turso.")
        return True

    except Exception as e:
        print(f"\nCONNECTION FAILED")
        print(f"  Error: {e}")
        print("\nTroubleshooting:")
        print("  1. Verify DATABASE_URL is correct (libsql://...turso.io)")
        print("  2. Verify TURSO_AUTH_TOKEN is valid and not expired")
        print("  3. Check network connectivity")
        return False


if __name__ == "__main__":
    success = verify_turso_connection()
    sys.exit(0 if success else 1)

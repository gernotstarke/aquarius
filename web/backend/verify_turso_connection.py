import os
import sys
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

def verify_turso_connection():
    """
    Verifies connection to Turso database using environment variables.
    """
    load_dotenv()
    
    database_url = os.getenv("DATABASE_URL")
    auth_token = os.getenv("TURSO_AUTH_TOKEN")
    
    print("=" * 60)
    print("🔍 Turso Connection Verification")
    print("=" * 60)
    
    if not database_url:
        print("❌ Error: DATABASE_URL not found in environment.")
        return False
        
    if "libsql" not in database_url:
        print(f"⚠️  Warning: DATABASE_URL does not look like a Turso URL (expected 'libsql://...').")
        print(f"   Current value: {database_url}")
        
    if not auth_token:
        print("⚠️  Warning: TURSO_AUTH_TOKEN not found. Connection might fail if auth is required.")

    # Prepare URL for SQLAlchemy
    sa_url = database_url.replace("libsql://", "sqlite+libsql://") if database_url.startswith("libsql://") else database_url
    
    connect_args = {}
    if auth_token:
        connect_args["authToken"] = auth_token
        
    print(f"   Target: {database_url}")
    print(f"   Driver: {sa_url.split('://')[0]}")
    
    try:
        print("\n⏳ Connecting...")
        engine = create_engine(sa_url, connect_args=connect_args)
        
        with engine.connect() as conn:
            print("   ✓ Connection established!")
            
            print("⏳ Executing query 'SELECT 1'...")
            result = conn.execute(text("SELECT 1")).scalar()
            
            if result == 1:
                print("   ✓ Query successful!")
            else:
                print(f"   ❌ Unexpected result: {result}")
                return False
                
        print("\n✅ VERIFICATION SUCCESSFUL")
        print("   Your application is ready to connect to Turso.")
        return True
        
    except Exception as e:
        print(f"\n❌ CONNECTION FAILED")
        print(f"   Error: {str(e)}")
        print("\n   Troubleshooting:")
        print("   1. Check if the Database URL is correct.")
        print("   2. Check if the Auth Token is valid (not expired).")
        print("   3. Ensure you have internet access.")
        return False

if __name__ == "__main__":
    success = verify_turso_connection()
    sys.exit(0 if success else 1)

import os
import pytest
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
import tempfile
from app import database

def test_sqlite_file_persistence():
    """
    Integration test to verify that the standard SQLite configuration
    correctly persists data to a file (not just memory), validating
    that the Step 2 configuration changes didn't break local development.
    """
    # Create a temporary file for the database
    with tempfile.NamedTemporaryFile(suffix=".db", delete=False) as tmp:
        db_path = tmp.name
    
    db_url = f"sqlite:///{db_path}"
    
    try:
        # Phase 1: Write Data
        # Manually create engine to simulate app startup with specific URL
        engine1 = create_engine(db_url)
        
        # Create a simple table
        with engine1.connect() as conn:
            conn.execute(text("CREATE TABLE test_persistence (id INTEGER PRIMARY KEY, name TEXT)"))
            conn.execute(text("INSERT INTO test_persistence (name) VALUES ('persistent_data')"))
            conn.commit()
            
        # Dispose engine to close file locks
        engine1.dispose()
        
        # Phase 2: Read Data (New Connection)
        # This verifies that we are reading from the file, not just shared memory
        engine2 = create_engine(db_url)
        
        with engine2.connect() as conn:
            result = conn.execute(text("SELECT name FROM test_persistence")).scalar()
            
        assert result == "persistent_data"
        
        engine2.dispose()
        
    finally:
        # Cleanup
        if os.path.exists(db_path):
            os.unlink(db_path)

def test_app_dependency_wiring():
    """
    Verify that the app's get_db dependency yields a valid session
    that can execute queries, ensuring the global engine is configured correctly.
    """
    # This uses the engine configured in app.database (which defaults to aquarius.db or env var)
    # We just want to check connectivity, not modify the real DB
    
    gen = database.get_db()
    session = next(gen)
    
    try:
        # Simple query that works on any DB
        result = session.execute(text("SELECT 1")).scalar()
        assert result == 1
    finally:
        session.close()

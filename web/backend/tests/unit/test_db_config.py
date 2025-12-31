import os
import pytest
from unittest import mock
import importlib
from sqlalchemy.engine import Engine

def test_sqlite_configuration():
    """Verify standard SQLite configuration."""
    with mock.patch.dict(os.environ, {"DATABASE_URL": "sqlite:///./test.db"}):
        from app import database
        importlib.reload(database)
        
        assert str(database.engine.url) == "sqlite:///./test.db"
        assert database.engine.dialect.name == "sqlite"
        # Accessing connect_args from the engine/pool
        # SQLAlchemy 2.0 stores this in pool.connect_args or similar, but checking the module var is easier
        assert database.connect_args["check_same_thread"] is False
        assert "authToken" not in database.connect_args

def test_libsql_configuration():
    """Verify Turso/libSQL configuration."""
    turso_url = "libsql://database.turso.io"
    auth_token = "secret-token"
    
    with mock.patch.dict(os.environ, {
        "DATABASE_URL": turso_url,
        "TURSO_AUTH_TOKEN": auth_token
    }):
        from app import database
        importlib.reload(database)
        
        # URL should be converted to sqlite+libsql
        assert str(database.engine.url) == "sqlite+libsql://database.turso.io"
        
        # check connect_args for token
        assert database.connect_args["authToken"] == auth_token
        assert database.connect_args["check_same_thread"] is False

def test_default_configuration():
    """Verify default fallback to local sqlite."""
    # Ensure DATABASE_URL is unset
    with mock.patch.dict(os.environ, {}, clear=True):
        from app import database
        importlib.reload(database)
        
        assert str(database.engine.url) == "sqlite:///./arqua42.db"

import pytest

def test_libsql_dependencies_available():
    """
    Verify that the Turso/libSQL related dependencies are correctly installed
    and can be imported by the Python environment.
    """
    try:
        import libsql_client
        print("✅ libsql-client is available")
        
        # This is a bit tricky as it's a sqlalchemy dialect, 
        # but we can check if the module is findable
        import importlib.util
        spec = importlib.util.find_spec("sqlalchemy_libsql")
        assert spec is not None, "sqlalchemy-libsql dialect not found"
        print("✅ sqlalchemy-libsql dialect is available")
        
    except ImportError as e:
        pytest.fail(f"Required libSQL dependency missing or failing to import: {e}")
    except Exception as e:
        pytest.fail(f"An unexpected error occurred while verifying dependencies: {e}")

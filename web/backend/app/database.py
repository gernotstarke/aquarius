"""Database configuration with SQLite for CRUD prototype."""
import os
from sqlalchemy import create_engine, event
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv

load_dotenv()

# Database URL - defaults to local SQLite for prototype
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./arqua42.db")
TURSO_AUTH_TOKEN = os.getenv("TURSO_AUTH_TOKEN")

connect_args = {}

if DATABASE_URL.startswith("sqlite"):
    connect_args["check_same_thread"] = False

# Support for Turso/libSQL
if DATABASE_URL.startswith("libsql://"):
    DATABASE_URL = DATABASE_URL.replace("libsql://", "sqlite+libsql://")

if "libsql" in DATABASE_URL and TURSO_AUTH_TOKEN:
    connect_args["authToken"] = TURSO_AUTH_TOKEN
    # libSQL driver also benefits from check_same_thread=False in some contexts, 
    # ensuring consistent behavior with threads in FastAPI
    connect_args["check_same_thread"] = False

# Create engine
engine = create_engine(
    DATABASE_URL,
    connect_args=connect_args,
    echo=False  # Set to True for debugging
)

# Enable foreign keys for SQLite
@event.listens_for(engine, "connect")
def set_sqlite_pragma(dbapi_conn, connection_record):
    try:
        cursor = dbapi_conn.cursor()
        cursor.execute("PRAGMA foreign_keys=ON")
        cursor.close()
    except Exception:
        # Some drivers or remote connections might not support this pragma directly
        pass

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_db():
    """Dependency for FastAPI routes to get database session."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db():
    """Initialize database tables."""
    Base.metadata.create_all(bind=engine)

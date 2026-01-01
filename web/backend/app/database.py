"""Database configuration supporting SQLite and Turso/libSQL."""
import os
from sqlalchemy import create_engine, event
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv

load_dotenv()

# Database URL - defaults to local SQLite for development
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./arqua42.db")
TURSO_AUTH_TOKEN = os.getenv("TURSO_AUTH_TOKEN")

connect_args = {}

# Determine database type and configure accordingly
if DATABASE_URL.startswith("libsql://"):
    # Turso/libSQL remote connection
    # Extract hostname and build proper SQLAlchemy URL
    hostname = DATABASE_URL.replace("libsql://", "")
    DATABASE_URL = f"sqlite+libsql://{hostname}?secure=true"
    if TURSO_AUTH_TOKEN:
        connect_args["auth_token"] = TURSO_AUTH_TOKEN
elif DATABASE_URL.startswith("sqlite"):
    # Local SQLite
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
        # Remote connections may not support this pragma
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

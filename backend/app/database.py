"""Database configuration with Turso (libSQL) support."""
import os
from sqlalchemy import create_engine, event
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

load_dotenv()

# Database URL from environment
TURSO_DATABASE_URL = os.getenv("TURSO_DATABASE_URL", "file:./aquarius.db")
TURSO_AUTH_TOKEN = os.getenv("TURSO_AUTH_TOKEN", "")

# Create engine with libSQL/Turso support
if TURSO_DATABASE_URL.startswith("libsql://"):
    # Turso cloud database
    connect_args = {"check_same_thread": False}
    if TURSO_AUTH_TOKEN:
        # For Turso, use the experimental libsql driver
        engine = create_engine(
            TURSO_DATABASE_URL,
            connect_args={"authToken": TURSO_AUTH_TOKEN},
            echo=True
        )
    else:
        engine = create_engine(TURSO_DATABASE_URL, connect_args=connect_args, echo=True)
else:
    # Local SQLite for development
    connect_args = {"check_same_thread": False}
    engine = create_engine(
        TURSO_DATABASE_URL,
        connect_args=connect_args,
        echo=True
    )

# Enable foreign keys for SQLite
@event.listens_for(engine, "connect")
def set_sqlite_pragma(dbapi_conn, connection_record):
    cursor = dbapi_conn.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()

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

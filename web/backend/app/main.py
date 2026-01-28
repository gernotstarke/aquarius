"""
FastAPI main application for Aquarius CRUD prototype.
Simple CRUD operations for Kind, Wettkampf, Schwimmbad, and Saison.
"""
from fastapi import FastAPI, Depends, HTTPException, Response, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import text, or_, asc, desc, func, case
from typing import List, Optional
import os
import logging
import time
from datetime import datetime, timedelta
from contextlib import asynccontextmanager

from app.database import get_db, engine, Base
from app import models, schemas
from app.routers import auth, users, health, admin
from app.version import AQUARIUS_BACKEND_VERSION

# Domain routers
from app.grunddaten import router as grunddaten_router
from app.kind import router as kind_router
from app.wettkampf import router as wettkampf_router
from app.anmeldung import router as anmeldung_router

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Log database configuration at startup
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./aquarius.db")
logger.info(f"🔧 DATABASE_URL: {DATABASE_URL}")
logger.info(f"🔧 TURSO_AUTH_TOKEN present: {bool(os.getenv('TURSO_AUTH_TOKEN'))}")
logger.info(f"🔧 Engine URL: {engine.url}")
logger.info(f"🔧 Engine dialect: {engine.dialect.name}")

# Log authentication configuration
ENABLE_APP_AUTH = os.getenv("ENABLE_APP_AUTH", "false").lower() == "true"
DEFAULT_APP_USER = os.getenv("DEFAULT_APP_USER", "testuser")
logger.info(f"🔧 ENABLE_APP_AUTH: {ENABLE_APP_AUTH}")
if not ENABLE_APP_AUTH:
    logger.info(f"🔧 DEFAULT_APP_USER: {DEFAULT_APP_USER}")

# Create tables
Base.metadata.create_all(bind=engine)

# Import SessionLocal for startup event
from app.database import SessionLocal

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Initialize app user authentication on startup."""
    # Startup logic
    # Skip initialization if running tests (PYTEST_CURRENT_TEST env var is set)
    if "PYTEST_CURRENT_TEST" not in os.environ:
        if not ENABLE_APP_AUTH:
            logger.info(f"📝 Development mode: Creating default app user '{DEFAULT_APP_USER}' if needed...")
            from app import auth as auth_module
            db = SessionLocal()
            try:
                auth_module.get_or_create_default_app_user(db)
            except Exception as e:
                logger.warning(f"⚠️  Error initializing default app user: {e}")
            finally:
                db.close()
    
    yield
    # Shutdown logic (if any)

app = FastAPI(
    title="Aquarius CRUD API",
    description="Simple CRUD API for testing the tech stack",
    version=AQUARIUS_BACKEND_VERSION,
    lifespan=lifespan
)

# CORS middleware for frontend and documentation site
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",  # Local development
        "https://aquarius.fly.dev",  # Production app
        "https://aquarius.arc42.org",  # Documentation site
        "http://localhost:4000",  # Local Jekyll docs
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["X-Total-Count"], # Expose pagination header
)

# Mount static files for backend use
static_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "static")
if not os.path.exists(static_dir):
    os.makedirs(static_dir)
app.mount("/static", StaticFiles(directory=static_dir), name="static")

# Register routers BEFORE mounting frontend to ensure API routes take precedence
app.include_router(auth.router)
app.include_router(users.router)
app.include_router(health.router)
app.include_router(admin.router)

# Domain routers
app.include_router(grunddaten_router.router)
app.include_router(kind_router.router)
app.include_router(wettkampf_router.router)
app.include_router(anmeldung_router.router)

# Mount frontend static files (built React app)
# In production: /app/frontend/dist
# __file__ = /app/backend/app/main.py, so we go up 3 levels to /app
frontend_dist = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "frontend", "dist")
if os.path.exists(frontend_dist):
    # Mount assets directory for CSS, JS, images
    assets_dir = os.path.join(frontend_dist, "assets")
    if os.path.exists(assets_dir):
        app.mount("/assets", StaticFiles(directory=assets_dir), name="assets")

    logger.info(f"✓ Frontend static files mounted from {frontend_dist}")
else:
    logger.warning(f"⚠️  Frontend dist directory not found at {frontend_dist}")

@app.get("/")
def read_root():
    """Serve the frontend application or API info."""
    # Check if frontend is available
    # In production: /app/frontend/dist
    # __file__ = /app/backend/app/main.py, so we go up 3 levels to /app
    frontend_dist = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "frontend", "dist")
    index_html = os.path.join(frontend_dist, "index.html")

    if os.path.exists(index_html):
        return FileResponse(index_html)
    else:
        # Fallback to JSON response if frontend not available (development mode)
        return {"message": "Aquarius CRUD API", "version": AQUARIUS_BACKEND_VERSION}


@app.get("/{full_path:path}")
def spa_fallback(full_path: str, request: Request):
    """Serve SPA index.html for unknown routes (non-API/static)."""
    if full_path.startswith(("api", "docs", "redoc", "openapi.json", "static", "assets")):
        raise HTTPException(status_code=404, detail="Not Found")

    frontend_dist = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "frontend", "dist")
    index_html = os.path.join(frontend_dist, "index.html")
    if os.path.exists(index_html):
        return FileResponse(index_html)

    return {"message": "Aquarius CRUD API", "version": AQUARIUS_BACKEND_VERSION}


@app.get("/api/health")
def health_check(db: Session = Depends(get_db)):
    """Health check endpoint for monitoring and fly.io health checks."""
    try:
        # Test database connection
        db.execute(text("SELECT 1"))
        db_status = "healthy"
    except Exception as e:
        db_status = f"unhealthy: {str(e)}"

    return {
        "status": "healthy",
        "database": db_status,
        "version": AQUARIUS_BACKEND_VERSION
    }

@app.get("/api/status")
def status_overview(db: Session = Depends(get_db)):
    """Public status overview for the documentation dashboard."""
    database_url = os.getenv("DATABASE_URL", "sqlite:///./aquarius.db")
    db_type = "turso" if database_url.startswith(("libsql://", "sqlite+libsql://")) else "sqlite"

    fly_region = os.getenv("FLY_REGION")
    fly_app = os.getenv("FLY_APP_NAME")
    environment = "fly" if (fly_region or fly_app) else "local"
    region = fly_region or ("unknown" if environment == "fly" else "local")

    table_count = db.execute(
        text("SELECT count(*) FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%'")
    ).scalar() or 0

    page_count = db.execute(text("PRAGMA page_count")).scalar() or 0
    page_size = db.execute(text("PRAGMA page_size")).scalar() or 0
    db_size_bytes = page_count * page_size

    health_start = time.perf_counter()
    db.execute(text("SELECT 1"))
    health_latency_ms = round((time.perf_counter() - health_start) * 1000, 2)

    write_latency_ms = None
    read_latency_ms = None
    perf_rows = None

    try:
        db.execute(
            text(
                "CREATE TABLE IF NOT EXISTS performance_probe ("
                "id INTEGER PRIMARY KEY, "
                "created_at TEXT NOT NULL, "
                "payload TEXT)"
            )
        )
        db.commit()

        insert_start = time.perf_counter()
        db.execute(
            text("INSERT INTO performance_probe (created_at, payload) VALUES (:created_at, :payload)"),
            {
                "created_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
                "payload": "probe",
            },
        )
        db.commit()
        write_latency_ms = round((time.perf_counter() - insert_start) * 1000, 2)

        read_start = time.perf_counter()
        perf_rows = db.execute(text("SELECT count(*) FROM performance_probe")).scalar() or 0
        if perf_rows > 10000:
            db.execute(
                text(
                    "DELETE FROM performance_probe "
                    "WHERE id NOT IN ("
                    "  SELECT id FROM performance_probe "
                    "  ORDER BY id DESC "
                    "  LIMIT 10000"
                    ")"
                )
            )
            db.commit()
            perf_rows = db.execute(text("SELECT count(*) FROM performance_probe")).scalar() or 0
        read_latency_ms = round((time.perf_counter() - read_start) * 1000, 2)
    except Exception:
        db.rollback()

    # Get active users (active in the last 15 minutes)
    active_threshold = datetime.utcnow() - timedelta(minutes=15)
    active_users = db.query(models.User.username).filter(models.User.last_active >= active_threshold).all()
    active_user_names = [u[0] for u in active_users]

    return {
        "version": AQUARIUS_BACKEND_VERSION,
        "app": {
            "environment": environment,
            "region": region,
        },
        "database": {
            "type": db_type,
            "table_count": table_count,
            "size_bytes": db_size_bytes,
            "health_latency_ms": health_latency_ms,
            "write_latency_ms": write_latency_ms,
            "read_latency_ms": read_latency_ms,
            "performance_rows": perf_rows,
        },
        "counts": {
            "users": db.query(models.User).count(),
            "active_users": len(active_user_names),
            "kind": db.query(models.Kind).count(),
            "anmeldung": db.query(models.Anmeldung).count(),
            "wettkampf": db.query(models.Wettkampf).count(),
        },
        "active_users": active_user_names,
    }


# ============================================================================
# SPA ROUTING - Catch-all route for React Router
# ============================================================================
# This must be the LAST route to act as a catch-all for frontend routes

@app.get("/{full_path:path}")
async def serve_spa(full_path: str):
    """
    Catch-all route to serve the React SPA for client-side routing.
    First checks if a static file exists (e.g., vite.svg, favicon.ico).
    If not, returns index.html for React Router to handle navigation.
    """
    # In production: /app/frontend/dist
    # __file__ = /app/backend/app/main.py, so we go up 3 levels to /app
    frontend_dist = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "frontend", "dist")

    # Check if the requested path is a static file in dist root
    requested_file = os.path.join(frontend_dist, full_path)
    if os.path.isfile(requested_file):
        return FileResponse(requested_file)

    # Otherwise, serve index.html for SPA routing
    index_html = os.path.join(frontend_dist, "index.html")
    if os.path.exists(index_html):
        return FileResponse(index_html)
    else:
        raise HTTPException(status_code=404, detail="Frontend not found")

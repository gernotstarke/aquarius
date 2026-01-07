"""
FastAPI main application for Aquarius CRUD prototype.
Simple CRUD operations for Kind, Wettkampf, Schwimmbad, and Saison.
"""
from fastapi import FastAPI, Depends, HTTPException, Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import text, or_, asc, desc, func, case
from typing import List, Optional
import os
import logging

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

# Create tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Aquarius CRUD API",
    description="Simple CRUD API for testing the tech stack",
    version=AQUARIUS_BACKEND_VERSION
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

    return {
        "version": AQUARIUS_BACKEND_VERSION,
        "app": {
            "environment": environment,
            "region": region,
        },
        "database": {
            "type": db_type,
            "table_count": table_count,
        },
        "counts": {
            "kind": db.query(models.Kind).count(),
            "anmeldung": db.query(models.Anmeldung).count(),
            "wettkampf": db.query(models.Wettkampf).count(),
        },
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

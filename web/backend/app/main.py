"""
FastAPI main application for Aquarius CRUD prototype.
Simple CRUD operations for Kind, Wettkampf, Schwimmbad, and Saison.
"""
from fastapi import FastAPI, Depends, HTTPException, Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from sqlalchemy import text, or_, asc, desc, func
from typing import List, Optional
import os
import logging

from app.database import get_db, engine, Base
from app import models, schemas
from app.routers import auth, users, health, admin
from app.version import AQUARIUS_BACKEND_VERSION

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
# SAISON CRUD ENDPOINTS
# ============================================================================

@app.get("/api/saison", response_model=List[schemas.Saison])
def list_saison(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Get list of all seasons."""
    return db.query(models.Saison).offset(skip).limit(limit).all()


@app.get("/api/saison/{saison_id}", response_model=schemas.Saison)
def get_saison(saison_id: int, db: Session = Depends(get_db)):
    """Get a specific season by ID."""
    saison = db.query(models.Saison).filter(models.Saison.id == saison_id).first()
    if not saison:
        raise HTTPException(status_code=404, detail="Saison not found")
    return saison


@app.post("/api/saison", response_model=schemas.Saison, status_code=201)
def create_saison(saison: schemas.SaisonCreate, db: Session = Depends(get_db)):
    """Create a new season."""
    db_saison = models.Saison(**saison.model_dump())
    db.add(db_saison)
    db.commit()
    db.refresh(db_saison)
    return db_saison


@app.put("/api/saison/{saison_id}", response_model=schemas.Saison)
def update_saison(saison_id: int, saison: schemas.SaisonUpdate, db: Session = Depends(get_db)):
    """Update a season."""
    db_saison = db.query(models.Saison).filter(models.Saison.id == saison_id).first()
    if not db_saison:
        raise HTTPException(status_code=404, detail="Saison not found")

    for key, value in saison.model_dump().items():
        setattr(db_saison, key, value)

    db.commit()
    db.refresh(db_saison)
    return db_saison


@app.delete("/api/saison/{saison_id}", status_code=204)
def delete_saison(saison_id: int, db: Session = Depends(get_db)):
    """Delete a season."""
    db_saison = db.query(models.Saison).filter(models.Saison.id == saison_id).first()
    if not db_saison:
        raise HTTPException(status_code=404, detail="Saison not found")

    db.delete(db_saison)
    db.commit()
    return None


# ============================================================================
# SCHWIMMBAD CRUD ENDPOINTS
# ============================================================================

@app.get("/api/schwimmbad", response_model=List[schemas.Schwimmbad])
def list_schwimmbad(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Get list of all pools."""
    return db.query(models.Schwimmbad).offset(skip).limit(limit).all()


@app.get("/api/schwimmbad/{schwimmbad_id}", response_model=schemas.Schwimmbad)
def get_schwimmbad(schwimmbad_id: int, db: Session = Depends(get_db)):
    """Get a specific pool by ID."""
    schwimmbad = db.query(models.Schwimmbad).filter(models.Schwimmbad.id == schwimmbad_id).first()
    if not schwimmbad:
        raise HTTPException(status_code=404, detail="Schwimmbad not found")
    return schwimmbad


@app.post("/api/schwimmbad", response_model=schemas.Schwimmbad, status_code=201)
def create_schwimmbad(schwimmbad: schemas.SchwimmbadCreate, db: Session = Depends(get_db)):
    """Create a new pool."""
    db_schwimmbad = models.Schwimmbad(**schwimmbad.model_dump())
    db.add(db_schwimmbad)
    db.commit()
    db.refresh(db_schwimmbad)
    return db_schwimmbad


@app.put("/api/schwimmbad/{schwimmbad_id}", response_model=schemas.Schwimmbad)
def update_schwimmbad(schwimmbad_id: int, schwimmbad: schemas.SchwimmbadUpdate, db: Session = Depends(get_db)):
    """Update a pool."""
    db_schwimmbad = db.query(models.Schwimmbad).filter(models.Schwimmbad.id == schwimmbad_id).first()
    if not db_schwimmbad:
        raise HTTPException(status_code=404, detail="Schwimmbad not found")

    for key, value in schwimmbad.model_dump().items():
        setattr(db_schwimmbad, key, value)

    db.commit()
    db.refresh(db_schwimmbad)
    return db_schwimmbad


@app.delete("/api/schwimmbad/{schwimmbad_id}", status_code=204)
def delete_schwimmbad(schwimmbad_id: int, db: Session = Depends(get_db)):
    """Delete a pool."""
    db_schwimmbad = db.query(models.Schwimmbad).filter(models.Schwimmbad.id == schwimmbad_id).first()
    if not db_schwimmbad:
        raise HTTPException(status_code=404, detail="Schwimmbad not found")

    db.delete(db_schwimmbad)
    db.commit()
    return None


# ============================================================================
# VEREIN CRUD ENDPOINTS
# ============================================================================

@app.get("/api/verein", response_model=List[schemas.Verein])
def list_verein(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Get list of all clubs."""
    return db.query(models.Verein).offset(skip).limit(limit).all()


@app.get("/api/verein/{verein_id}", response_model=schemas.Verein)
def get_verein(verein_id: int, db: Session = Depends(get_db)):
    """Get a specific club by ID."""
    verein = db.query(models.Verein).filter(models.Verein.id == verein_id).first()
    if not verein:
        raise HTTPException(status_code=404, detail="Verein not found")
    return verein


@app.post("/api/verein", response_model=schemas.Verein, status_code=201)
def create_verein(verein: schemas.VereinCreate, db: Session = Depends(get_db)):
    """Create a new club."""
    db_verein = models.Verein(**verein.model_dump())
    db.add(db_verein)
    db.commit()
    db.refresh(db_verein)
    return db_verein


@app.put("/api/verein/{verein_id}", response_model=schemas.Verein)
def update_verein(verein_id: int, verein: schemas.VereinUpdate, db: Session = Depends(get_db)):
    """Update a club."""
    db_verein = db.query(models.Verein).filter(models.Verein.id == verein_id).first()
    if not db_verein:
        raise HTTPException(status_code=404, detail="Verein not found")

    for key, value in verein.model_dump().items():
        setattr(db_verein, key, value)

    db.commit()
    db.refresh(db_verein)
    return db_verein


@app.delete("/api/verein/{verein_id}", status_code=204)
def delete_verein(verein_id: int, db: Session = Depends(get_db)):
    """Delete a club."""
    db_verein = db.query(models.Verein).filter(models.Verein.id == verein_id).first()
    if not db_verein:
        raise HTTPException(status_code=404, detail="Verein not found")

    db.delete(db_verein)
    db.commit()
    return None


# ============================================================================
# WETTKAMPF CRUD ENDPOINTS
# ============================================================================

@app.get("/api/wettkampf", response_model=List[schemas.Wettkampf])
def list_wettkampf(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Get list of all competitions."""
    return db.query(models.Wettkampf).offset(skip).limit(limit).all()


@app.get("/api/wettkampf/{wettkampf_id}", response_model=schemas.Wettkampf)
def get_wettkampf(wettkampf_id: int, db: Session = Depends(get_db)):
    """Get a specific competition by ID."""
    wettkampf = db.query(models.Wettkampf).filter(models.Wettkampf.id == wettkampf_id).first()
    if not wettkampf:
        raise HTTPException(status_code=404, detail="Wettkampf not found")
    return wettkampf


@app.post("/api/wettkampf", response_model=schemas.Wettkampf, status_code=201)
def create_wettkampf(wettkampf: schemas.WettkampfCreate, db: Session = Depends(get_db)):
    """Create a new competition."""
    db_wettkampf = models.Wettkampf(**wettkampf.model_dump())
    db.add(db_wettkampf)
    db.commit()
    db.refresh(db_wettkampf)
    return db_wettkampf


@app.put("/api/wettkampf/{wettkampf_id}", response_model=schemas.Wettkampf)
def update_wettkampf(wettkampf_id: int, wettkampf: schemas.WettkampfUpdate, db: Session = Depends(get_db)):
    """Update a competition."""
    db_wettkampf = db.query(models.Wettkampf).filter(models.Wettkampf.id == wettkampf_id).first()
    if not db_wettkampf:
        raise HTTPException(status_code=404, detail="Wettkampf not found")

    for key, value in wettkampf.model_dump().items():
        setattr(db_wettkampf, key, value)

    db.commit()
    db.refresh(db_wettkampf)
    return db_wettkampf


@app.delete("/api/wettkampf/{wettkampf_id}", status_code=204)
def delete_wettkampf(wettkampf_id: int, db: Session = Depends(get_db)):
    """Delete a competition."""
    db_wettkampf = db.query(models.Wettkampf).filter(models.Wettkampf.id == wettkampf_id).first()
    if not db_wettkampf:
        raise HTTPException(status_code=404, detail="Wettkampf not found")

    db.delete(db_wettkampf)
    db.commit()
    return None


# ============================================================================
# KIND CRUD ENDPOINTS
# ============================================================================

@app.get("/api/kind", response_model=List[schemas.Kind])
def list_kind(
    response: Response,
    skip: int = 0,
    limit: int = 20,
    search: Optional[str] = None,
    sort_by: Optional[str] = "nachname",
    sort_order: Optional[str] = "asc",
    db: Session = Depends(get_db)
):
    """Get list of all children with search, sort, and pagination."""
    query = db.query(models.Kind)

    # Search (Filter)
    if search:
        search_term = f"%{search}%"
        query = query.join(models.Verein, isouter=True).filter(
            or_(
                models.Kind.vorname.ilike(search_term),
                models.Kind.nachname.ilike(search_term),
                models.Verein.name.ilike(search_term)
            )
        )
    
    # Total count for pagination headers
    total_count = query.count()
    response.headers["X-Total-Count"] = str(total_count)

    # Sorting
    if sort_by:
        sort_column = None
        if sort_by == "vorname":
            sort_column = models.Kind.vorname
        elif sort_by == "nachname":
            sort_column = models.Kind.nachname
        elif sort_by == "verein":
            # Ensure join if not already joined
            if not search:
                query = query.join(models.Verein, isouter=True)
            sort_column = models.Verein.name
        
        if sort_column is not None:
            if sort_order == "desc":
                query = query.order_by(desc(sort_column))
            else:
                query = query.order_by(asc(sort_column))
    
    # Default sorting if none provided (fallback)
    else:
        query = query.order_by(models.Kind.nachname)

    return query.offset(skip).limit(limit).all()


@app.get("/api/kind/{kind_id}", response_model=schemas.Kind)
def get_kind(kind_id: int, db: Session = Depends(get_db)):
    """Get a specific child by ID."""
    kind = db.query(models.Kind).filter(models.Kind.id == kind_id).first()
    if not kind:
        raise HTTPException(status_code=404, detail="Kind not found")
    return kind


@app.post("/api/kind", response_model=schemas.Kind, status_code=201)
def create_kind(kind: schemas.KindCreate, db: Session = Depends(get_db)):
    """Create a new child."""
    db_kind = models.Kind(**kind.model_dump())
    db.add(db_kind)
    db.commit()
    db.refresh(db_kind)
    return db_kind


@app.put("/api/kind/{kind_id}", response_model=schemas.Kind)
def update_kind(kind_id: int, kind: schemas.KindUpdate, db: Session = Depends(get_db)):
    """Update a child."""
    db_kind = db.query(models.Kind).filter(models.Kind.id == kind_id).first()
    if not db_kind:
        raise HTTPException(status_code=404, detail="Kind not found")

    for key, value in kind.model_dump().items():
        setattr(db_kind, key, value)

    db.commit()
    db.refresh(db_kind)
    return db_kind


@app.delete("/api/kind/{kind_id}", status_code=204)
def delete_kind(kind_id: int, db: Session = Depends(get_db)):
    """Delete a child."""
    db_kind = db.query(models.Kind).filter(models.Kind.id == kind_id).first()
    if not db_kind:
        raise HTTPException(status_code=404, detail="Kind not found")

    db.delete(db_kind)
    db.commit()
    return None


# ============================================================================
# VERBAND READ-ONLY ENDPOINTS
# ============================================================================

@app.get("/api/verband", response_model=List[schemas.VerbandWithCount])
def list_verbaende(
    skip: int = 0,
    limit: int = 200,
    sort_by: str = "name",
    sort_order: str = "asc",
    db: Session = Depends(get_db),
):
    """Get list of all associations (read-only) with nomination counts."""
    sort_fields = {
        "name": models.Verband.name,
        "nomination_count": "nomination_count",
    }
    sort_column = sort_fields.get(sort_by, models.Verband.name)
    order_fn = desc if sort_order.lower() == "desc" else asc

    nomination_count = func.count(models.Kind.id).label("nomination_count")
    query = (
        db.query(models.Verband, nomination_count)
        .outerjoin(models.Kind, models.Kind.verband_id == models.Verband.id)
        .group_by(models.Verband.id)
    )

    if sort_column == "nomination_count":
        query = query.order_by(order_fn(nomination_count), models.Verband.name)
    else:
        query = query.order_by(order_fn(sort_column), models.Verband.name)

    rows = query.offset(skip).limit(limit).all()
    return [
        schemas.VerbandWithCount(
            id=verband.id,
            name=verband.name,
            abkuerzung=verband.abkuerzung,
            land=verband.land,
            ort=verband.ort,
            nomination_count=count,
        )
        for verband, count in rows
    ]


# ============================================================================
# FIGUR CRUD ENDPOINTS
# ============================================================================

@app.get("/api/figur", response_model=List[schemas.Figur])
def list_figur(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Get list of all figures."""
    return db.query(models.Figur).offset(skip).limit(limit).all()


@app.get("/api/figur/{figur_id}", response_model=schemas.Figur)
def get_figur(figur_id: int, db: Session = Depends(get_db)):
    """Get a specific figure by ID."""
    figur = db.query(models.Figur).filter(models.Figur.id == figur_id).first()
    if not figur:
        raise HTTPException(status_code=404, detail="Figur not found")
    return figur


@app.post("/api/figur", response_model=schemas.Figur, status_code=201)
def create_figur(figur: schemas.FigurCreate, db: Session = Depends(get_db)):
    """Create a new figure."""
    db_figur = models.Figur(**figur.model_dump())
    db.add(db_figur)
    db.commit()
    db.refresh(db_figur)
    return db_figur


@app.put("/api/figur/{figur_id}", response_model=schemas.Figur)
def update_figur(figur_id: int, figur: schemas.FigurUpdate, db: Session = Depends(get_db)):
    """Update a figure."""
    db_figur = db.query(models.Figur).filter(models.Figur.id == figur_id).first()
    if not db_figur:
        raise HTTPException(status_code=404, detail="Figur not found")

    for key, value in figur.model_dump().items():
        setattr(db_figur, key, value)

    db.commit()
    db.refresh(db_figur)
    return db_figur


@app.delete("/api/figur/{figur_id}", status_code=204)
def delete_figur(figur_id: int, db: Session = Depends(get_db)):
    """Delete a figure."""
    db_figur = db.query(models.Figur).filter(models.Figur.id == figur_id).first()
    if not db_figur:
        raise HTTPException(status_code=404, detail="Figur not found")

    db.delete(db_figur)
    db.commit()
    return None


# ============================================================================
# ANMELDUNG CRUD ENDPOINTS
# ============================================================================

@app.get("/api/anmeldung", response_model=List[schemas.Anmeldung])
def list_anmeldung(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Get list of all registrations."""
    return db.query(models.Anmeldung).offset(skip).limit(limit).all()


@app.get("/api/anmeldung/{anmeldung_id}", response_model=schemas.Anmeldung)
def get_anmeldung(anmeldung_id: int, db: Session = Depends(get_db)):
    """Get a specific registration by ID."""
    anmeldung = db.query(models.Anmeldung).filter(models.Anmeldung.id == anmeldung_id).first()
    if not anmeldung:
        raise HTTPException(status_code=404, detail="Anmeldung not found")
    return anmeldung


@app.post("/api/anmeldung", response_model=schemas.Anmeldung, status_code=201)
def create_anmeldung(anmeldung: schemas.AnmeldungCreate, db: Session = Depends(get_db)):
    """
    Create a new registration with automatic startnummer assignment.

    - Startnummer is assigned atomically (next available number for the competition)
    - Registration is marked as 'vorläufig' (preliminary) if:
      1. No figures are selected yet, OR
      2. Maximum participants for the competition is reached
    """
    from datetime import date
    from sqlalchemy import func

    # Get wettkampf to check max_teilnehmer
    wettkampf = db.query(models.Wettkampf).filter(
        models.Wettkampf.id == anmeldung.wettkampf_id
    ).first()
    if not wettkampf:
        raise HTTPException(status_code=404, detail="Wettkampf not found")

    # Count current final (non-vorläufig) registrations
    final_count = db.query(models.Anmeldung).filter(
        models.Anmeldung.wettkampf_id == anmeldung.wettkampf_id,
        models.Anmeldung.vorlaeufig == 0,
        models.Anmeldung.status == "aktiv"
    ).count()

    # Determine if registration should be preliminary
    is_vorlaeufig = 0
    reasons = []

    if len(anmeldung.figur_ids) == 0:
        is_vorlaeufig = 1
        reasons.append("keine Figuren ausgewählt")

    if wettkampf.max_teilnehmer and final_count >= wettkampf.max_teilnehmer:
        is_vorlaeufig = 1
        reasons.append("maximale Teilnehmerzahl erreicht")

    # Atomically get next startnummer for this competition
    # Using database-level MAX to avoid race conditions
    max_startnummer = db.query(func.max(models.Anmeldung.startnummer)).filter(
        models.Anmeldung.wettkampf_id == anmeldung.wettkampf_id
    ).scalar()

    next_startnummer = (max_startnummer or 0) + 1

    # Create anmeldung with startnummer
    db_anmeldung = models.Anmeldung(
        kind_id=anmeldung.kind_id,
        wettkampf_id=anmeldung.wettkampf_id,
        startnummer=next_startnummer,
        anmeldedatum=date.today(),
        vorlaeufig=is_vorlaeufig,
        status="vorläufig" if is_vorlaeufig else "aktiv"
    )
    db.add(db_anmeldung)
    db.flush()  # Get the ID without committing

    # Add selected figures (if any)
    for figur_id in anmeldung.figur_ids:
        figur = db.query(models.Figur).filter(models.Figur.id == figur_id).first()
        if figur:
            db_anmeldung.figuren.append(figur)

    try:
        db.commit()
        db.refresh(db_anmeldung)

        # Log preliminary registration reasons
        if is_vorlaeufig:
            print(f"ℹ️  Vorläufige Anmeldung #{next_startnummer}: {', '.join(reasons)}")

        return db_anmeldung
    except Exception as e:
        db.rollback()
        # If unique constraint fails (race condition), retry would happen here
        # For now, just raise the error
        raise HTTPException(status_code=409, detail=f"Startnummer conflict: {str(e)}")


@app.put("/api/anmeldung/{anmeldung_id}", response_model=schemas.Anmeldung)
def update_anmeldung(anmeldung_id: int, anmeldung: schemas.AnmeldungUpdate, db: Session = Depends(get_db)):
    """
    Update a registration.

    - Automatically updates 'vorläufig' status based on figure selection
    - If figures are added to a preliminary registration, it may become final
    """
    db_anmeldung = db.query(models.Anmeldung).filter(models.Anmeldung.id == anmeldung_id).first()
    if not db_anmeldung:
        raise HTTPException(status_code=404, detail="Anmeldung not found")

    if anmeldung.status:
        db_anmeldung.status = anmeldung.status

    if anmeldung.vorlaeufig is not None:
        db_anmeldung.vorlaeufig = anmeldung.vorlaeufig

    if anmeldung.figur_ids is not None:
        # Clear existing figures
        db_anmeldung.figuren.clear()
        # Add new figures
        for figur_id in anmeldung.figur_ids:
            figur = db.query(models.Figur).filter(models.Figur.id == figur_id).first()
            if figur:
                db_anmeldung.figuren.append(figur)

        # Auto-update vorläufig status based on figures
        if len(anmeldung.figur_ids) > 0 and db_anmeldung.vorlaeufig == 1:
            # Check if max_teilnehmer is still a blocker
            wettkampf = db.query(models.Wettkampf).filter(
                models.Wettkampf.id == db_anmeldung.wettkampf_id
            ).first()

            final_count = db.query(models.Anmeldung).filter(
                models.Anmeldung.wettkampf_id == db_anmeldung.wettkampf_id,
                models.Anmeldung.vorlaeufig == 0,
                models.Anmeldung.status == "aktiv",
                models.Anmeldung.id != anmeldung_id  # Exclude current registration
            ).count()

            # If max not reached and figures are selected, make it final
            if not wettkampf.max_teilnehmer or final_count < wettkampf.max_teilnehmer:
                db_anmeldung.vorlaeufig = 0
                db_anmeldung.status = "aktiv"
                print(f"✓ Anmeldung #{db_anmeldung.startnummer} ist jetzt final (Figuren hinzugefügt)")

        elif len(anmeldung.figur_ids) == 0:
            # No figures selected - must be preliminary
            db_anmeldung.vorlaeufig = 1
            db_anmeldung.status = "vorläufig"

    db.commit()
    db.refresh(db_anmeldung)
    return db_anmeldung


@app.delete("/api/anmeldung/{anmeldung_id}", status_code=204)
def delete_anmeldung(anmeldung_id: int, db: Session = Depends(get_db)):
    """Delete a registration."""
    db_anmeldung = db.query(models.Anmeldung).filter(models.Anmeldung.id == anmeldung_id).first()
    if not db_anmeldung:
        raise HTTPException(status_code=404, detail="Anmeldung not found")

    db.delete(db_anmeldung)
    db.commit()
    return None


# ============================================================================
# WETTKAMPF SPECIAL ENDPOINTS
# ============================================================================

@app.get("/api/wettkampf/{wettkampf_id}/details", response_model=schemas.WettkampfWithDetails)
def get_wettkampf_with_details(wettkampf_id: int, db: Session = Depends(get_db)):
    """Get competition with all figures and registrations."""
    wettkampf = db.query(models.Wettkampf).filter(models.Wettkampf.id == wettkampf_id).first()
    if not wettkampf:
        raise HTTPException(status_code=404, detail="Wettkampf not found")
    return wettkampf


@app.post("/api/wettkampf/{wettkampf_id}/figuren/{figur_id}", status_code=201)
def add_figur_to_wettkampf(wettkampf_id: int, figur_id: int, db: Session = Depends(get_db)):
    """Add a figure to the competition's allowed figures."""
    wettkampf = db.query(models.Wettkampf).filter(models.Wettkampf.id == wettkampf_id).first()
    if not wettkampf:
        raise HTTPException(status_code=404, detail="Wettkampf not found")

    figur = db.query(models.Figur).filter(models.Figur.id == figur_id).first()
    if not figur:
        raise HTTPException(status_code=404, detail="Figur not found")

    if figur not in wettkampf.figuren:
        wettkampf.figuren.append(figur)
        db.commit()

    return {"message": "Figur added to Wettkampf"}


@app.delete("/api/wettkampf/{wettkampf_id}/figuren/{figur_id}", status_code=204)
def remove_figur_from_wettkampf(wettkampf_id: int, figur_id: int, db: Session = Depends(get_db)):
    """Remove a figure from the competition's allowed figures."""
    wettkampf = db.query(models.Wettkampf).filter(models.Wettkampf.id == wettkampf_id).first()
    if not wettkampf:
        raise HTTPException(status_code=404, detail="Wettkampf not found")

    figur = db.query(models.Figur).filter(models.Figur.id == figur_id).first()
    if not figur:
        raise HTTPException(status_code=404, detail="Figur not found")

    if figur in wettkampf.figuren:
        wettkampf.figuren.remove(figur)
        db.commit()

    return None


@app.put("/api/wettkampf/{wettkampf_id}/figuren", status_code=200)
def set_wettkampf_figuren(wettkampf_id: int, figur_ids: List[int], db: Session = Depends(get_db)):
    """Set all allowed figures for a competition at once."""
    wettkampf = db.query(models.Wettkampf).filter(models.Wettkampf.id == wettkampf_id).first()
    if not wettkampf:
        raise HTTPException(status_code=404, detail="Wettkampf not found")

    # Clear existing figures
    wettkampf.figuren.clear()

    # Add new figures
    for figur_id in figur_ids:
        figur = db.query(models.Figur).filter(models.Figur.id == figur_id).first()
        if figur:
            wettkampf.figuren.append(figur)

    db.commit()
    return {"message": f"{len(figur_ids)} figures set for Wettkampf"}


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

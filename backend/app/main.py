"""
FastAPI main application for Arqua42 CRUD prototype.
Simple CRUD operations for Kind, Wettkampf, Schwimmbad, and Saison.
"""
from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db, engine, Base
from app import models, schemas

# Create tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Arqua42 CRUD API",
    description="Simple CRUD API for testing the tech stack",
    version="0.1.0"
)

# CORS middleware for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Vite default port
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def read_root():
    return {"message": "Arqua42 CRUD API", "version": "0.1.0"}


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
    db_saison = models.Saison(**saison.dict())
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

    for key, value in saison.dict().items():
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
    db_schwimmbad = models.Schwimmbad(**schwimmbad.dict())
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

    for key, value in schwimmbad.dict().items():
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
    db_wettkampf = models.Wettkampf(**wettkampf.dict())
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

    for key, value in wettkampf.dict().items():
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
def list_kind(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Get list of all children."""
    return db.query(models.Kind).offset(skip).limit(limit).all()


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
    db_kind = models.Kind(**kind.dict())
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

    for key, value in kind.dict().items():
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

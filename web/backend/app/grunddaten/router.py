"""Grunddaten (Master Data) API Router.

Handles all master data endpoints:
- Saison (Season) - CRUD
- Schwimmbad (Swimming Pool) - CRUD
- Verein (Club) - CRUD
- Verband (Association) - Read-only
- Versicherung (Insurance) - Read-only
- Figur (Figure) - CRUD
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func, asc, desc
from typing import List

from app.database import get_db
from app import models, auth
from app.grunddaten import schemas as grunddaten_schemas

router = APIRouter(prefix="/api", tags=["grunddaten"])


# ============================================================================
# SAISON CRUD ENDPOINTS
# ============================================================================

@router.get("/saison", response_model=List[grunddaten_schemas.Saison])
def list_saison(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.require_app_read_permission)
):
    """Get list of all seasons."""
    return db.query(models.Saison).offset(skip).limit(limit).all()


@router.get("/saison/{saison_id}", response_model=grunddaten_schemas.Saison)
def get_saison(
    saison_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.require_app_read_permission)
):
    """Get a specific season by ID."""
    saison = db.query(models.Saison).filter(models.Saison.id == saison_id).first()
    if not saison:
        raise HTTPException(status_code=404, detail="Saison not found")
    return saison


@router.post("/saison", response_model=grunddaten_schemas.Saison, status_code=201)
def create_saison(
    saison: grunddaten_schemas.SaisonCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.require_app_write_permission)
):
    """Create a new season."""
    db_saison = models.Saison(**saison.model_dump())
    db.add(db_saison)
    db.commit()
    db.refresh(db_saison)
    return db_saison


@router.put("/saison/{saison_id}", response_model=grunddaten_schemas.Saison)
def update_saison(
    saison_id: int,
    saison: grunddaten_schemas.SaisonUpdate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.require_app_write_permission)
):
    """Update a season."""
    db_saison = db.query(models.Saison).filter(models.Saison.id == saison_id).first()
    if not db_saison:
        raise HTTPException(status_code=404, detail="Saison not found")

    for key, value in saison.model_dump().items():
        setattr(db_saison, key, value)

    db.commit()
    db.refresh(db_saison)
    return db_saison


@router.delete("/saison/{saison_id}", status_code=204)
def delete_saison(
    saison_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.require_app_write_permission)
):
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

@router.get("/schwimmbad", response_model=List[grunddaten_schemas.Schwimmbad])
def list_schwimmbad(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.require_app_read_permission)
):
    """Get list of all pools."""
    return db.query(models.Schwimmbad).offset(skip).limit(limit).all()


@router.get("/schwimmbad/{schwimmbad_id}", response_model=grunddaten_schemas.Schwimmbad)
def get_schwimmbad(
    schwimmbad_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.require_app_read_permission)
):
    """Get a specific pool by ID."""
    schwimmbad = db.query(models.Schwimmbad).filter(models.Schwimmbad.id == schwimmbad_id).first()
    if not schwimmbad:
        raise HTTPException(status_code=404, detail="Schwimmbad not found")
    return schwimmbad


@router.post("/schwimmbad", response_model=grunddaten_schemas.Schwimmbad, status_code=201)
def create_schwimmbad(
    schwimmbad: grunddaten_schemas.SchwimmbadCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.require_app_write_permission)
):
    """Create a new pool."""
    db_schwimmbad = models.Schwimmbad(**schwimmbad.model_dump())
    db.add(db_schwimmbad)
    db.commit()
    db.refresh(db_schwimmbad)
    return db_schwimmbad


@router.put("/schwimmbad/{schwimmbad_id}", response_model=grunddaten_schemas.Schwimmbad)
def update_schwimmbad(
    schwimmbad_id: int,
    schwimmbad: grunddaten_schemas.SchwimmbadUpdate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.require_app_write_permission)
):
    """Update a pool."""
    db_schwimmbad = db.query(models.Schwimmbad).filter(models.Schwimmbad.id == schwimmbad_id).first()
    if not db_schwimmbad:
        raise HTTPException(status_code=404, detail="Schwimmbad not found")

    for key, value in schwimmbad.model_dump().items():
        setattr(db_schwimmbad, key, value)

    db.commit()
    db.refresh(db_schwimmbad)
    return db_schwimmbad


@router.delete("/schwimmbad/{schwimmbad_id}", status_code=204)
def delete_schwimmbad(
    schwimmbad_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.require_app_write_permission)
):
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

@router.get("/verein", response_model=List[grunddaten_schemas.Verein])
def list_verein(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.require_app_read_permission)
):
    """Get list of all clubs."""
    return db.query(models.Verein).offset(skip).limit(limit).all()


@router.get("/verein/{verein_id}", response_model=grunddaten_schemas.Verein)
def get_verein(
    verein_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.require_app_read_permission)
):
    """Get a specific club by ID."""
    verein = db.query(models.Verein).filter(models.Verein.id == verein_id).first()
    if not verein:
        raise HTTPException(status_code=404, detail="Verein not found")
    return verein


@router.post("/verein", response_model=grunddaten_schemas.Verein, status_code=201)
def create_verein(
    verein: grunddaten_schemas.VereinCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.require_app_write_permission)
):
    """Create a new club."""
    db_verein = models.Verein(**verein.model_dump())
    db.add(db_verein)
    db.commit()
    db.refresh(db_verein)
    return db_verein


@router.put("/verein/{verein_id}", response_model=grunddaten_schemas.Verein)
def update_verein(
    verein_id: int,
    verein: grunddaten_schemas.VereinUpdate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.require_app_write_permission)
):
    """Update a club."""
    db_verein = db.query(models.Verein).filter(models.Verein.id == verein_id).first()
    if not db_verein:
        raise HTTPException(status_code=404, detail="Verein not found")

    for key, value in verein.model_dump().items():
        setattr(db_verein, key, value)

    db.commit()
    db.refresh(db_verein)
    return db_verein


@router.delete("/verein/{verein_id}", status_code=204)
def delete_verein(
    verein_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.require_app_write_permission)
):
    """Delete a club."""
    db_verein = db.query(models.Verein).filter(models.Verein.id == verein_id).first()
    if not db_verein:
        raise HTTPException(status_code=404, detail="Verein not found")

    db.delete(db_verein)
    db.commit()
    return None


# ============================================================================
# VERBAND READ-ONLY ENDPOINTS
# ============================================================================

@router.get("/verband", response_model=List[grunddaten_schemas.VerbandWithCount])
def list_verbaende(
    skip: int = 0,
    limit: int = 200,
    sort_by: str = "name",
    sort_order: str = "asc",
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.require_app_read_permission)
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
        grunddaten_schemas.VerbandWithCount(
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
# VERSICHERUNG READ-ONLY ENDPOINTS
# ============================================================================

@router.get("/versicherung", response_model=List[grunddaten_schemas.Versicherung])
def list_versicherungen(
    skip: int = 0,
    limit: int = 200,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.require_app_read_permission)
):
    """Get list of all insurance companies (read-only)."""
    return (
        db.query(models.Versicherung)
        .order_by(models.Versicherung.name)
        .offset(skip)
        .limit(limit)
        .all()
    )


# ============================================================================
# FIGUR CRUD ENDPOINTS
# ============================================================================

@router.get("/figur", response_model=List[grunddaten_schemas.Figur])
def list_figur(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.require_app_read_permission)
):
    """Get list of all figures."""
    return db.query(models.Figur).offset(skip).limit(limit).all()


@router.get("/figur/{figur_id}", response_model=grunddaten_schemas.Figur)
def get_figur(
    figur_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.require_app_read_permission)
):
    """Get a specific figure by ID."""
    figur = db.query(models.Figur).filter(models.Figur.id == figur_id).first()
    if not figur:
        raise HTTPException(status_code=404, detail="Figur not found")
    return figur


@router.post("/figur", response_model=grunddaten_schemas.Figur, status_code=201)
def create_figur(
    figur: grunddaten_schemas.FigurCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.require_app_write_permission)
):
    """Create a new figure."""
    db_figur = models.Figur(**figur.model_dump())
    db.add(db_figur)
    db.commit()
    db.refresh(db_figur)
    return db_figur


@router.put("/figur/{figur_id}", response_model=grunddaten_schemas.Figur)
def update_figur(
    figur_id: int,
    figur: grunddaten_schemas.FigurUpdate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.require_app_write_permission)
):
    """Update a figure."""
    db_figur = db.query(models.Figur).filter(models.Figur.id == figur_id).first()
    if not db_figur:
        raise HTTPException(status_code=404, detail="Figur not found")

    for key, value in figur.model_dump().items():
        setattr(db_figur, key, value)

    db.commit()
    db.refresh(db_figur)
    return db_figur


@router.delete("/figur/{figur_id}", status_code=204)
def delete_figur(
    figur_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.require_app_write_permission)
):
    """Delete a figure."""
    db_figur = db.query(models.Figur).filter(models.Figur.id == figur_id).first()
    if not db_figur:
        raise HTTPException(status_code=404, detail="Figur not found")

    db.delete(db_figur)
    db.commit()
    return None

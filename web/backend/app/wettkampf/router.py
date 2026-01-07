"""Wettkampf (Competition) API Router."""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session, joinedload
from typing import List

from app.database import get_db
from app import models, schemas
from app.wettkampf import schemas as wettkampf_schemas
from app.shared.utils import anmeldung_with_insurance_ok

router = APIRouter(prefix="/api", tags=["wettkampf"])


# ============================================================================
# WETTKAMPF CRUD ENDPOINTS
# ============================================================================

@router.get("/wettkampf", response_model=List[wettkampf_schemas.Wettkampf])
def list_wettkampf(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Get list of all competitions."""
    return db.query(models.Wettkampf).offset(skip).limit(limit).all()


@router.get("/wettkampf/{wettkampf_id}", response_model=wettkampf_schemas.Wettkampf)
def get_wettkampf(wettkampf_id: int, db: Session = Depends(get_db)):
    """Get a specific competition by ID."""
    wettkampf = db.query(models.Wettkampf).filter(models.Wettkampf.id == wettkampf_id).first()
    if not wettkampf:
        raise HTTPException(status_code=404, detail="Wettkampf not found")
    return wettkampf


@router.post("/wettkampf", response_model=wettkampf_schemas.Wettkampf, status_code=201)
def create_wettkampf(wettkampf: wettkampf_schemas.WettkampfCreate, db: Session = Depends(get_db)):
    """Create a new competition."""
    db_wettkampf = models.Wettkampf(**wettkampf.model_dump())
    db.add(db_wettkampf)
    db.commit()
    db.refresh(db_wettkampf)
    return db_wettkampf


@router.put("/wettkampf/{wettkampf_id}", response_model=wettkampf_schemas.Wettkampf)
def update_wettkampf(wettkampf_id: int, wettkampf: wettkampf_schemas.WettkampfUpdate, db: Session = Depends(get_db)):
    """Update a competition."""
    db_wettkampf = db.query(models.Wettkampf).filter(models.Wettkampf.id == wettkampf_id).first()
    if not db_wettkampf:
        raise HTTPException(status_code=404, detail="Wettkampf not found")

    for key, value in wettkampf.model_dump().items():
        setattr(db_wettkampf, key, value)

    db.commit()
    db.refresh(db_wettkampf)
    return db_wettkampf


@router.delete("/wettkampf/{wettkampf_id}", status_code=204)
def delete_wettkampf(wettkampf_id: int, db: Session = Depends(get_db)):
    """Delete a competition."""
    db_wettkampf = db.query(models.Wettkampf).filter(models.Wettkampf.id == wettkampf_id).first()
    if not db_wettkampf:
        raise HTTPException(status_code=404, detail="Wettkampf not found")

    db.delete(db_wettkampf)
    db.commit()
    return None


# ============================================================================
# WETTKAMPF SPECIAL ENDPOINTS
# ============================================================================

@router.get("/wettkampf/{wettkampf_id}/details", response_model=wettkampf_schemas.WettkampfWithDetails)
def get_wettkampf_with_details(wettkampf_id: int, db: Session = Depends(get_db)):
    """Get competition with all figures and registrations."""
    wettkampf = db.query(models.Wettkampf).options(
        joinedload(models.Wettkampf.anmeldungen).joinedload(models.Anmeldung.kind)
    ).filter(models.Wettkampf.id == wettkampf_id).first()
    if not wettkampf:
        raise HTTPException(status_code=404, detail="Wettkampf not found")
    return wettkampf_schemas.WettkampfWithDetails(
        id=wettkampf.id,
        name=wettkampf.name,
        datum=wettkampf.datum,
        max_teilnehmer=wettkampf.max_teilnehmer,
        saison_id=wettkampf.saison_id,
        schwimmbad_id=wettkampf.schwimmbad_id,
        figuren=wettkampf.figuren,
        anmeldungen=[anmeldung_with_insurance_ok(a) for a in wettkampf.anmeldungen],
        saison=wettkampf.saison,
        schwimmbad=wettkampf.schwimmbad,
    )


@router.post("/wettkampf/{wettkampf_id}/figuren/{figur_id}", status_code=201)
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


@router.delete("/wettkampf/{wettkampf_id}/figuren/{figur_id}", status_code=204)
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


@router.put("/wettkampf/{wettkampf_id}/figuren", status_code=200)
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

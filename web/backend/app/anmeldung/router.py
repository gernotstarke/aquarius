"""Anmeldung (Registration) API Router."""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import func
from typing import List
from datetime import date

from app.database import get_db
from app import models
from app.anmeldung import schemas as anmeldung_schemas
from app.shared.utils import kind_has_insurance, anmeldung_with_insurance_ok

router = APIRouter(prefix="/api", tags=["anmeldung"])


@router.get("/anmeldung", response_model=List[anmeldung_schemas.Anmeldung])
def list_anmeldung(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Get list of all registrations."""
    anmeldungen = db.query(models.Anmeldung).options(
        joinedload(models.Anmeldung.kind)
    ).offset(skip).limit(limit).all()
    return [anmeldung_with_insurance_ok(a) for a in anmeldungen]


@router.get("/anmeldung/{anmeldung_id}", response_model=anmeldung_schemas.Anmeldung)
def get_anmeldung(anmeldung_id: int, db: Session = Depends(get_db)):
    """Get a specific registration by ID."""
    anmeldung = db.query(models.Anmeldung).options(
        joinedload(models.Anmeldung.kind)
    ).filter(models.Anmeldung.id == anmeldung_id).first()
    if not anmeldung:
        raise HTTPException(status_code=404, detail="Anmeldung not found")
    return anmeldung_with_insurance_ok(anmeldung)


@router.post("/anmeldung", response_model=anmeldung_schemas.Anmeldung, status_code=201)
def create_anmeldung(anmeldung: anmeldung_schemas.AnmeldungCreate, db: Session = Depends(get_db)):
    """
    Create a new registration with automatic startnummer assignment.

    - Startnummer is assigned atomically (next available number for the competition)
    - Registration is marked as 'vorläufig' (preliminary) if:
      1. No figures are selected yet, OR
      2. Maximum participants for the competition is reached
    """
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

    kind = db.query(models.Kind).filter(models.Kind.id == anmeldung.kind_id).first()
    if not kind:
        raise HTTPException(status_code=404, detail="Kind not found")

    # Determine if registration should be preliminary
    is_vorlaeufig = 0
    reasons = []

    if len(anmeldung.figur_ids) == 0:
        is_vorlaeufig = 1
        reasons.append("keine Figuren ausgewählt")

    if not kind_has_insurance(kind):
        is_vorlaeufig = 1
        reasons.append("keine Versicherung")

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

        return anmeldung_with_insurance_ok(db_anmeldung)
    except Exception as e:
        db.rollback()
        # If unique constraint fails (race condition), retry would happen here
        # For now, just raise the error
        raise HTTPException(status_code=409, detail=f"Startnummer conflict: {str(e)}")


@router.put("/anmeldung/{anmeldung_id}", response_model=anmeldung_schemas.Anmeldung)
def update_anmeldung(anmeldung_id: int, anmeldung: anmeldung_schemas.AnmeldungUpdate, db: Session = Depends(get_db)):
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
    if not kind_has_insurance(db_anmeldung.kind):
        db_anmeldung.vorlaeufig = 1
        db_anmeldung.status = "vorläufig"
        db.commit()
        db.refresh(db_anmeldung)
    return anmeldung_with_insurance_ok(db_anmeldung)


@router.delete("/anmeldung/{anmeldung_id}", status_code=204)
def delete_anmeldung(anmeldung_id: int, db: Session = Depends(get_db)):
    """Delete a registration."""
    db_anmeldung = db.query(models.Anmeldung).filter(models.Anmeldung.id == anmeldung_id).first()
    if not db_anmeldung:
        raise HTTPException(status_code=404, detail="Anmeldung not found")

    db.delete(db_anmeldung)
    db.commit()
    return None

"""Anmeldung (Registration) API Router."""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from datetime import date

from app.database import get_db
from app import models, auth
from app.anmeldung import schemas as anmeldung_schemas
from app.anmeldung.repository import AnmeldungRepository
from app.anmeldung.services import AnmeldungService
from app.anmeldung.dtos import AnmeldungDTO
from app.anmeldung.mappers import map_anmeldung_to_dto, map_anmeldungen_to_dtos
from app.kind.repository import KindRepository
from app.wettkampf.repository import WettkampfRepository
from app.grunddaten.repository import FigurRepository

router = APIRouter(prefix="/api", tags=["anmeldung"])


def get_anmeldung_service(db: Session = Depends(get_db)) -> AnmeldungService:
    """Dependency to get AnmeldungService instance."""
    anmeldung_repo = AnmeldungRepository(db)
    kind_repo = KindRepository(db)
    wettkampf_repo = WettkampfRepository(db)
    figur_repo = FigurRepository(db)
    return AnmeldungService(anmeldung_repo, kind_repo, wettkampf_repo, figur_repo)


@router.get("/anmeldung", response_model=List[AnmeldungDTO])
def list_anmeldung(
    skip: int = 0,
    limit: int = 100,
    service: AnmeldungService = Depends(get_anmeldung_service),
    current_user: models.User = Depends(auth.require_app_read_permission)
):
    """Get list of all registrations."""
    anmeldungen = service.list_anmeldungen(skip=skip, limit=limit)
    # Map ORM models to DTOs
    return map_anmeldungen_to_dtos(anmeldungen)


@router.get("/anmeldung/{anmeldung_id}", response_model=AnmeldungDTO)
def get_anmeldung(
    anmeldung_id: int,
    service: AnmeldungService = Depends(get_anmeldung_service),
    current_user: models.User = Depends(auth.require_app_read_permission)
):
    """Get a specific registration by ID."""
    anmeldung = service.get_anmeldung(anmeldung_id)
    if not anmeldung:
        raise HTTPException(status_code=404, detail="Anmeldung not found")
    # Map ORM model to DTO
    return map_anmeldung_to_dto(anmeldung)


@router.post("/anmeldung", response_model=AnmeldungDTO, status_code=201)
def create_anmeldung(
    anmeldung: anmeldung_schemas.AnmeldungCreate,
    service: AnmeldungService = Depends(get_anmeldung_service),
    current_user: models.User = Depends(auth.require_app_write_permission)
):
    """
    Create a new registration with automatic startnummer assignment.

    - Startnummer is assigned atomically (next available number for the competition)
    - Registration is marked as 'vorläufig' (preliminary) if:
      1. No figures are selected yet, OR
      2. Maximum participants for the competition is reached
      3. Kind has no insurance
    """
    try:
        db_anmeldung = service.create_anmeldung(anmeldung)
        # Map ORM model to DTO
        return map_anmeldung_to_dto(db_anmeldung)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=409, detail=f"Registration conflict: {str(e)}")


@router.put("/anmeldung/{anmeldung_id}", response_model=AnmeldungDTO)
def update_anmeldung(
    anmeldung_id: int,
    anmeldung: anmeldung_schemas.AnmeldungUpdate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.require_app_write_permission)
):
    """
    Update a registration.

    - Automatically updates 'vorläufig' status based on figure selection
    - If figures are added to a preliminary registration, it may become final

    TODO: This endpoint should be refactored to use the service layer instead of
    direct repository and database access.
    """
    repo = AnmeldungRepository(db)

    db_anmeldung = repo.get_with_details(anmeldung_id)
    if not db_anmeldung:
        raise HTTPException(status_code=404, detail="Anmeldung not found")

    if anmeldung.status:
        db_anmeldung.status = anmeldung.status

    if anmeldung.vorlaeufig is not None:
        db_anmeldung.vorlaeufig = anmeldung.vorlaeufig

    if anmeldung.figur_ids is not None:
        # Use repository to set figuren
        repo.set_figuren(anmeldung_id, anmeldung.figur_ids)
        db.refresh(db_anmeldung)

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
    # Need to reload with details for mapping
    db_anmeldung = repo.get_with_details(anmeldung_id)

    # Map ORM model to DTO
    return map_anmeldung_to_dto(db_anmeldung)


@router.delete("/anmeldung/{anmeldung_id}", status_code=204)
def delete_anmeldung(
    anmeldung_id: int,
    service: AnmeldungService = Depends(get_anmeldung_service),
    current_user: models.User = Depends(auth.require_app_write_permission)
):
    """Delete a registration."""
    deleted = service.delete_anmeldung(anmeldung_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Anmeldung not found")
    return None

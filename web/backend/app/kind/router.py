"""Kind (Child) API Router."""
from fastapi import APIRouter, Depends, HTTPException, Response
from sqlalchemy.orm import Session
from typing import List, Optional

from app.database import get_db
from app import models
from app.kind import schemas as kind_schemas
from app.kind.repository import KindRepository
from app.shared.utils import kind_has_insurance

router = APIRouter(prefix="/api", tags=["kind"])


@router.get("/kind", response_model=List[kind_schemas.Kind])
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
    repo = KindRepository(db)
    results, total_count = repo.search(
        skip=skip,
        limit=limit,
        query=search,
        sort_by=sort_by,
        sort_order=sort_order
    )

    # Set pagination header
    response.headers["X-Total-Count"] = str(total_count)

    return results


@router.get("/kind/{kind_id}", response_model=kind_schemas.Kind)
def get_kind(kind_id: int, db: Session = Depends(get_db)):
    """Get a specific child by ID."""
    repo = KindRepository(db)
    kind = repo.get(kind_id)
    if not kind:
        raise HTTPException(status_code=404, detail="Kind not found")
    return kind


@router.post("/kind", response_model=kind_schemas.Kind, status_code=201)
def create_kind(kind: kind_schemas.KindCreate, db: Session = Depends(get_db)):
    """Create a new child."""
    repo = KindRepository(db)
    return repo.create(kind)


@router.put("/kind/{kind_id}", response_model=kind_schemas.Kind)
def update_kind(kind_id: int, kind: kind_schemas.KindUpdate, db: Session = Depends(get_db)):
    """Update a child."""
    repo = KindRepository(db)
    db_kind = repo.update(kind_id, kind)
    if not db_kind:
        raise HTTPException(status_code=404, detail="Kind not found")

    # Check insurance and update related anmeldungen if needed
    if not kind_has_insurance(db_kind):
        db.query(models.Anmeldung).filter(
            models.Anmeldung.kind_id == db_kind.id
        ).update({"vorlaeufig": 1, "status": "vorläufig"})
        db.commit()
    return db_kind


@router.delete("/kind/{kind_id}", status_code=204)
def delete_kind(kind_id: int, db: Session = Depends(get_db)):
    """Delete a child."""
    repo = KindRepository(db)
    deleted = repo.delete(kind_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Kind not found")
    return None

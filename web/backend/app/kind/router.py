"""Kind (Child) API Router."""
from fastapi import APIRouter, Depends, HTTPException, Response
from sqlalchemy.orm import Session
from typing import List, Optional

from app.database import get_db
from app import models
from app.kind import schemas as kind_schemas
from app.kind.repository import KindRepository
from app.kind.services import KindService

router = APIRouter(prefix="/api", tags=["kind"])


def get_kind_service(db: Session = Depends(get_db)) -> KindService:
    """Dependency to get KindService instance."""
    repo = KindRepository(db)
    return KindService(repo)


@router.get("/kind", response_model=List[kind_schemas.Kind])
def list_kind(
    response: Response,
    skip: int = 0,
    limit: int = 20,
    search: Optional[str] = None,
    sort_by: Optional[str] = "nachname",
    sort_order: Optional[str] = "asc",
    service: KindService = Depends(get_kind_service)
):
    """Get list of all children with search, sort, and pagination."""
    results, total_count = service.search_kinder(
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
def get_kind(kind_id: int, service: KindService = Depends(get_kind_service)):
    """Get a specific child by ID."""
    kind = service.get_kind(kind_id)
    if not kind:
        raise HTTPException(status_code=404, detail="Kind not found")
    return kind


@router.post("/kind", response_model=kind_schemas.Kind, status_code=201)
def create_kind(kind: kind_schemas.KindCreate, service: KindService = Depends(get_kind_service)):
    """Create a new child."""
    return service.create_kind(kind)


@router.put("/kind/{kind_id}", response_model=kind_schemas.Kind)
def update_kind(kind_id: int, kind: kind_schemas.KindUpdate, service: KindService = Depends(get_kind_service)):
    """Update a child."""
    db_kind = service.update_kind(kind_id, kind)
    if not db_kind:
        raise HTTPException(status_code=404, detail="Kind not found")
    return db_kind


@router.delete("/kind/{kind_id}", status_code=204)
def delete_kind(kind_id: int, service: KindService = Depends(get_kind_service)):
    """Delete a child."""
    deleted = service.delete_kind(kind_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Kind not found")
    return None

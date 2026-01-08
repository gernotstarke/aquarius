"""Kind (Child) API Router."""
from fastapi import APIRouter, Depends, HTTPException, Response
from sqlalchemy.orm import Session
from typing import List, Optional

from app.database import get_db
from app import models, auth
from app.kind import schemas as kind_schemas
from app.kind.repository import KindRepository
from app.kind.services import KindService
from app.kind.dtos import KindDTO
from app.kind.mappers import map_kind_to_dto, map_kinder_to_dtos

router = APIRouter(prefix="/api", tags=["kind"])


def get_kind_service(db: Session = Depends(get_db)) -> KindService:
    """Dependency to get KindService instance."""
    repo = KindRepository(db)
    return KindService(repo)


@router.get("/kind", response_model=List[KindDTO])
def list_kind(
    response: Response,
    skip: int = 0,
    limit: int = 20,
    search: Optional[str] = None,
    sort_by: Optional[str] = "nachname",
    sort_order: Optional[str] = "asc",
    service: KindService = Depends(get_kind_service),
    current_user: models.User = Depends(auth.require_app_read_permission),
):
    """Get list of all children with search, sort, and pagination. Requires read permission."""
    results, total_count = service.search_kinder(
        skip=skip,
        limit=limit,
        query=search,
        sort_by=sort_by,
        sort_order=sort_order
    )

    # Set pagination header
    response.headers["X-Total-Count"] = str(total_count)

    # Map ORM models to DTOs
    return map_kinder_to_dtos(results)


@router.get("/kind/{kind_id}", response_model=KindDTO)
def get_kind(
    kind_id: int,
    service: KindService = Depends(get_kind_service),
    current_user: models.User = Depends(auth.require_app_read_permission),
):
    """Get a specific child by ID. Requires read permission."""
    kind = service.get_kind(kind_id)
    if not kind:
        raise HTTPException(status_code=404, detail="Kind not found")
    # Map ORM model to DTO
    return map_kind_to_dto(kind)


@router.post("/kind", response_model=KindDTO, status_code=201)
def create_kind(
    kind: kind_schemas.KindCreate,
    service: KindService = Depends(get_kind_service),
    current_user: models.User = Depends(auth.require_app_write_permission),
):
    """Create a new child. Requires write permission."""
    created_kind = service.create_kind(kind)
    # Map ORM model to DTO
    return map_kind_to_dto(created_kind)


@router.put("/kind/{kind_id}", response_model=KindDTO)
def update_kind(
    kind_id: int,
    kind: kind_schemas.KindUpdate,
    service: KindService = Depends(get_kind_service),
    current_user: models.User = Depends(auth.require_app_write_permission),
):
    """Update a child. Requires write permission."""
    db_kind = service.update_kind(kind_id, kind)
    if not db_kind:
        raise HTTPException(status_code=404, detail="Kind not found")
    # Map ORM model to DTO
    return map_kind_to_dto(db_kind)


@router.delete("/kind/{kind_id}", status_code=204)
def delete_kind(
    kind_id: int,
    service: KindService = Depends(get_kind_service),
    current_user: models.User = Depends(auth.require_app_write_permission),
):
    """Delete a child. Requires write permission."""
    deleted = service.delete_kind(kind_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Kind not found")
    return None

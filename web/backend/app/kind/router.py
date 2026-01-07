"""Kind (Child) API Router."""
from fastapi import APIRouter, Depends, HTTPException, Response
from sqlalchemy.orm import Session
from sqlalchemy import or_, asc, desc, case
from typing import List, Optional

from app.database import get_db
from app import models
from app.kind import schemas as kind_schemas
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
        elif sort_by == "unversichert":
            has_contract_insurance = (
                models.Kind.versicherung_id.isnot(None)
                & models.Kind.vertrag.isnot(None)
                & (models.Kind.vertrag != "")
            )
            insurance_ok = case(
                (models.Kind.verein_id.isnot(None), 1),
                (models.Kind.verband_id.isnot(None), 1),
                (has_contract_insurance, 1),
                else_=0,
            )
            sort_column = insurance_ok
        
        if sort_column is not None:
            if sort_order == "desc":
                query = query.order_by(desc(sort_column), models.Kind.nachname)
            else:
                query = query.order_by(asc(sort_column), models.Kind.nachname)
    
    # Default sorting if none provided (fallback)
    else:
        query = query.order_by(models.Kind.nachname)

    return query.offset(skip).limit(limit).all()


@router.get("/kind/{kind_id}", response_model=kind_schemas.Kind)
def get_kind(kind_id: int, db: Session = Depends(get_db)):
    """Get a specific child by ID."""
    kind = db.query(models.Kind).filter(models.Kind.id == kind_id).first()
    if not kind:
        raise HTTPException(status_code=404, detail="Kind not found")
    return kind


@router.post("/kind", response_model=kind_schemas.Kind, status_code=201)
def create_kind(kind: kind_schemas.KindCreate, db: Session = Depends(get_db)):
    """Create a new child."""
    db_kind = models.Kind(**kind.model_dump())
    db.add(db_kind)
    db.commit()
    db.refresh(db_kind)
    return db_kind


@router.put("/kind/{kind_id}", response_model=kind_schemas.Kind)
def update_kind(kind_id: int, kind: kind_schemas.KindUpdate, db: Session = Depends(get_db)):
    """Update a child."""
    db_kind = db.query(models.Kind).filter(models.Kind.id == kind_id).first()
    if not db_kind:
        raise HTTPException(status_code=404, detail="Kind not found")

    for key, value in kind.model_dump().items():
        setattr(db_kind, key, value)

    db.commit()
    db.refresh(db_kind)
    if not kind_has_insurance(db_kind):
        db.query(models.Anmeldung).filter(
            models.Anmeldung.kind_id == db_kind.id
        ).update({"vorlaeufig": 1, "status": "vorläufig"})
        db.commit()
    return db_kind


@router.delete("/kind/{kind_id}", status_code=204)
def delete_kind(kind_id: int, db: Session = Depends(get_db)):
    """Delete a child."""
    db_kind = db.query(models.Kind).filter(models.Kind.id == kind_id).first()
    if not db_kind:
        raise HTTPException(status_code=404, detail="Kind not found")

    db.delete(db_kind)
    db.commit()
    return None

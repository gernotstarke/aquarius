"""Kind (Child) Repository - Data access layer for Kind domain."""
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import or_, asc, desc, case
from typing import List, Optional

from app import models
from app.kind import schemas as kind_schemas


class KindRepository:
    """Repository for Kind domain data access operations."""

    def __init__(self, db: Session):
        """Initialize repository with database session."""
        self.db = db

    def create(self, kind_data: kind_schemas.KindCreate) -> models.Kind:
        """Create a new Kind (child) in the database.

        Args:
            kind_data: Kind creation data

        Returns:
            Created Kind model instance with eagerly loaded relationships
        """
        db_kind = models.Kind(**kind_data.model_dump())
        self.db.add(db_kind)
        self.db.commit()
        self.db.refresh(db_kind)
        # Eagerly load relationships for response
        db_kind = self.db.query(models.Kind).options(
            joinedload(models.Kind.verein),
            joinedload(models.Kind.verband),
            joinedload(models.Kind.versicherung)
        ).filter(models.Kind.id == db_kind.id).first()
        return db_kind

    def get(self, kind_id: int) -> Optional[models.Kind]:
        """Get a Kind by ID.

        Args:
            kind_id: ID of the Kind to retrieve

        Returns:
            Kind model instance with eagerly loaded relationships if found, None otherwise
        """
        return self.db.query(models.Kind).options(
            joinedload(models.Kind.verein),
            joinedload(models.Kind.verband),
            joinedload(models.Kind.versicherung)
        ).filter(models.Kind.id == kind_id).first()

    def search(
        self,
        skip: int = 0,
        limit: int = 20,
        query: Optional[str] = None,
        sort_by: Optional[str] = "nachname",
        sort_order: Optional[str] = "asc"
    ) -> tuple[List[models.Kind], int]:
        """Search for Kind records with filtering, sorting, and pagination.

        This method encapsulates the complex search logic previously in the router,
        including searching across Kind and Verein names, and sorting by various fields.

        Args:
            skip: Number of records to skip (pagination offset)
            limit: Maximum number of records to return
            query: Optional search query to filter by vorname, nachname, or verein name
            sort_by: Field to sort by (vorname, nachname, verein, unversichert)
            sort_order: Sort order (asc or desc)

        Returns:
            Tuple of (list of Kind instances with eager loaded relationships, total count)
        """
        db_query = self.db.query(models.Kind).options(
            joinedload(models.Kind.verein),
            joinedload(models.Kind.verband),
            joinedload(models.Kind.versicherung)
        )

        # Search (Filter)
        if query:
            search_term = f"%{query}%"
            db_query = db_query.join(models.Verein, isouter=True).filter(
                or_(
                    models.Kind.vorname.ilike(search_term),
                    models.Kind.nachname.ilike(search_term),
                    models.Verein.name.ilike(search_term)
                )
            )

        # Total count for pagination
        total_count = db_query.count()

        # Sorting
        if sort_by:
            sort_column = None
            if sort_by == "vorname":
                sort_column = models.Kind.vorname
            elif sort_by == "nachname":
                sort_column = models.Kind.nachname
            elif sort_by == "verein":
                # Ensure join if not already joined
                if not query:
                    db_query = db_query.join(models.Verein, isouter=True)
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
                    db_query = db_query.order_by(desc(sort_column), models.Kind.nachname)
                else:
                    db_query = db_query.order_by(asc(sort_column), models.Kind.nachname)
        else:
            # Default sorting
            db_query = db_query.order_by(models.Kind.nachname)

        # Apply pagination
        results = db_query.offset(skip).limit(limit).all()

        return results, total_count

    def update(self, kind_id: int, kind_data: kind_schemas.KindUpdate) -> Optional[models.Kind]:
        """Update an existing Kind.

        Args:
            kind_id: ID of the Kind to update
            kind_data: Updated Kind data (partial updates supported)

        Returns:
            Updated Kind model instance with eagerly loaded relationships if found, None otherwise
        """
        db_kind = self.get(kind_id)
        if not db_kind:
            return None

        # Only update fields that were explicitly set (partial updates)
        for key, value in kind_data.model_dump(exclude_unset=True).items():
            setattr(db_kind, key, value)

        self.db.commit()
        self.db.refresh(db_kind)
        # Reload with eager loading to ensure relationships are loaded
        return self.get(kind_id)

    def delete(self, kind_id: int) -> bool:
        """Delete a Kind by ID.

        Args:
            kind_id: ID of the Kind to delete

        Returns:
            True if deleted, False if not found
        """
        db_kind = self.get(kind_id)
        if not db_kind:
            return False

        self.db.delete(db_kind)
        self.db.commit()
        return True

    def mark_anmeldungen_vorlaeufig(self, kind_id: int) -> int:
        """Mark all Anmeldungen for a Kind as vorläufig (preliminary).

        This is typically called when a Kind loses insurance coverage,
        as all their registrations must then be marked as preliminary.

        Args:
            kind_id: ID of the Kind whose Anmeldungen should be marked

        Returns:
            Number of Anmeldungen updated
        """
        updated_count = self.db.query(models.Anmeldung).filter(
            models.Anmeldung.kind_id == kind_id
        ).update({
            "vorlaeufig": 1,
            "status": "vorläufig"
        })
        self.db.commit()
        return updated_count

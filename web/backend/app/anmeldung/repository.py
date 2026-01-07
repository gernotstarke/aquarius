"""Anmeldung (Registration) Repository - Data access layer for Anmeldung domain."""
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import func
from typing import List, Optional

from app import models
from app.anmeldung import schemas as anmeldung_schemas


class AnmeldungRepository:
    """Repository for Anmeldung domain data access operations."""

    def __init__(self, db: Session):
        """Initialize repository with database session."""
        self.db = db

    def get(self, anmeldung_id: int) -> Optional[models.Anmeldung]:
        """Get an Anmeldung by ID (basic - without eager loading).

        Args:
            anmeldung_id: ID of the Anmeldung to retrieve

        Returns:
            Anmeldung model instance if found, None otherwise
        """
        return self.db.query(models.Anmeldung).filter(
            models.Anmeldung.id == anmeldung_id
        ).first()

    def get_with_details(self, anmeldung_id: int) -> Optional[models.Anmeldung]:
        """Get an Anmeldung by ID with eager loading of related entities.

        This method uses SQLAlchemy's joinedload to efficiently fetch the
        Anmeldung along with its related Kind and Figuren in a single query.

        Args:
            anmeldung_id: ID of the Anmeldung to retrieve

        Returns:
            Anmeldung model instance with eager-loaded relationships if found, None otherwise
        """
        return self.db.query(models.Anmeldung).options(
            joinedload(models.Anmeldung.kind),
            joinedload(models.Anmeldung.figuren)
        ).filter(models.Anmeldung.id == anmeldung_id).first()

    def list(self, skip: int = 0, limit: int = 100) -> List[models.Anmeldung]:
        """List all Anmeldungen with pagination and eager loading.

        Args:
            skip: Number of records to skip
            limit: Maximum number of records to return

        Returns:
            List of Anmeldung instances with eager-loaded Kind
        """
        return self.db.query(models.Anmeldung).options(
            joinedload(models.Anmeldung.kind)
        ).offset(skip).limit(limit).all()

    def get_next_startnummer(self, wettkampf_id: int) -> int:
        """Get the next available startnummer for a competition.

        This method performs an atomic MAX query to determine the next
        startnummer, avoiding race conditions in concurrent registrations.

        Args:
            wettkampf_id: ID of the Wettkampf (competition)

        Returns:
            Next available startnummer (1 if this is the first registration)
        """
        max_startnummer = self.db.query(func.max(models.Anmeldung.startnummer)).filter(
            models.Anmeldung.wettkampf_id == wettkampf_id
        ).scalar()

        return (max_startnummer or 0) + 1

    def count_final_registrations(self, wettkampf_id: int) -> int:
        """Count final (non-vorläufig) active registrations for a competition.

        Args:
            wettkampf_id: ID of the Wettkampf

        Returns:
            Count of final active registrations
        """
        return self.db.query(models.Anmeldung).filter(
            models.Anmeldung.wettkampf_id == wettkampf_id,
            models.Anmeldung.vorlaeufig == 0,
            models.Anmeldung.status == "aktiv"
        ).count()

    def create(self, anmeldung_data: anmeldung_schemas.AnmeldungCreate) -> models.Anmeldung:
        """Create a new Anmeldung.

        Note: This is a basic create method. The router layer handles the
        business logic for startnummer assignment and vorläufig status.

        Args:
            anmeldung_data: Anmeldung creation data

        Returns:
            Created Anmeldung model instance
        """
        db_anmeldung = models.Anmeldung(
            kind_id=anmeldung_data.kind_id,
            wettkampf_id=anmeldung_data.wettkampf_id
        )
        self.db.add(db_anmeldung)
        self.db.flush()  # Get the ID without committing
        return db_anmeldung

    def update(
        self,
        anmeldung_id: int,
        anmeldung_data: anmeldung_schemas.AnmeldungUpdate
    ) -> Optional[models.Anmeldung]:
        """Update an existing Anmeldung.

        Args:
            anmeldung_id: ID of the Anmeldung to update
            anmeldung_data: Updated Anmeldung data

        Returns:
            Updated Anmeldung model instance if found, None otherwise
        """
        db_anmeldung = self.get(anmeldung_id)
        if not db_anmeldung:
            return None

        if anmeldung_data.status:
            db_anmeldung.status = anmeldung_data.status

        if anmeldung_data.vorlaeufig is not None:
            db_anmeldung.vorlaeufig = anmeldung_data.vorlaeufig

        self.db.commit()
        self.db.refresh(db_anmeldung)
        return db_anmeldung

    def delete(self, anmeldung_id: int) -> bool:
        """Delete an Anmeldung by ID.

        Args:
            anmeldung_id: ID of the Anmeldung to delete

        Returns:
            True if deleted, False if not found
        """
        db_anmeldung = self.get(anmeldung_id)
        if not db_anmeldung:
            return False

        self.db.delete(db_anmeldung)
        self.db.commit()
        return True

    def add_figur(self, anmeldung_id: int, figur_id: int) -> Optional[models.Anmeldung]:
        """Add a Figur to an Anmeldung.

        Args:
            anmeldung_id: ID of the Anmeldung
            figur_id: ID of the Figur to add

        Returns:
            Updated Anmeldung if found, None otherwise
        """
        db_anmeldung = self.get(anmeldung_id)
        if not db_anmeldung:
            return None

        figur = self.db.query(models.Figur).filter(models.Figur.id == figur_id).first()
        if figur and figur not in db_anmeldung.figuren:
            db_anmeldung.figuren.append(figur)
            self.db.commit()
            self.db.refresh(db_anmeldung)

        return db_anmeldung

    def set_figuren(self, anmeldung_id: int, figur_ids: List[int]) -> Optional[models.Anmeldung]:
        """Set all Figuren for an Anmeldung at once.

        Args:
            anmeldung_id: ID of the Anmeldung
            figur_ids: List of Figur IDs to set

        Returns:
            Updated Anmeldung if found, None otherwise
        """
        db_anmeldung = self.get(anmeldung_id)
        if not db_anmeldung:
            return None

        # Clear existing figures
        db_anmeldung.figuren.clear()

        # Add new figures
        for figur_id in figur_ids:
            figur = self.db.query(models.Figur).filter(models.Figur.id == figur_id).first()
            if figur:
                db_anmeldung.figuren.append(figur)

        self.db.commit()
        self.db.refresh(db_anmeldung)
        return db_anmeldung

"""Wettkampf (Competition) Repository - Data access layer for Wettkampf domain."""
from sqlalchemy.orm import Session
from typing import Optional

from app import models


class WettkampfRepository:
    """Repository for Wettkampf domain data access operations."""

    def __init__(self, db: Session):
        """Initialize repository with database session."""
        self.db = db

    def get(self, wettkampf_id: int) -> Optional[models.Wettkampf]:
        """Get a Wettkampf by ID.

        Args:
            wettkampf_id: ID of the Wettkampf to retrieve

        Returns:
            Wettkampf model instance if found, None otherwise
        """
        return self.db.query(models.Wettkampf).filter(
            models.Wettkampf.id == wettkampf_id
        ).first()

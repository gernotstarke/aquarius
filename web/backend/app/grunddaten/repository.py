"""Grunddaten (Master Data) Repository - Data access layer for Grunddaten domain."""
from sqlalchemy.orm import Session
from typing import Optional

from app import models


class FigurRepository:
    """Repository for Figur data access operations."""

    def __init__(self, db: Session):
        """Initialize repository with database session."""
        self.db = db

    def get(self, figur_id: int) -> Optional[models.Figur]:
        """Get a Figur by ID.

        Args:
            figur_id: ID of the Figur to retrieve

        Returns:
            Figur model instance if found, None otherwise
        """
        return self.db.query(models.Figur).filter(
            models.Figur.id == figur_id
        ).first()

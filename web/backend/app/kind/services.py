"""Kind (Child) Service - Business logic layer for Kind domain."""
from typing import Optional

from app import models
from app.kind import schemas as kind_schemas
from app.kind.repository import KindRepository


class KindService:
    """Service layer for Kind domain business logic."""

    def __init__(self, repo: KindRepository):
        """Initialize service with repository."""
        self.repo = repo

    def is_insured(self, kind: models.Kind) -> bool:
        """Check if a Kind has valid insurance coverage.

        A Kind is considered insured if they have:
        - A Verein (club) membership, OR
        - A Verband (association) membership, OR
        - A private insurance with a valid contract

        Args:
            kind: The Kind model instance to check

        Returns:
            True if the Kind has valid insurance, False otherwise
        """
        # Check for Verein or Verband membership
        if kind.verein_id or kind.verband_id:
            return True

        # Check for private insurance with contract
        has_contract_insurance = bool(
            kind.versicherung_id and kind.vertrag and str(kind.vertrag).strip()
        )

        return has_contract_insurance

    def create_kind(self, kind_data: kind_schemas.KindCreate) -> models.Kind:
        """Create a new Kind.

        Args:
            kind_data: Kind creation data

        Returns:
            Created Kind model instance
        """
        return self.repo.create(kind_data)

    def get_kind(self, kind_id: int) -> Optional[models.Kind]:
        """Get a Kind by ID.

        Args:
            kind_id: ID of the Kind to retrieve

        Returns:
            Kind model instance if found, None otherwise
        """
        return self.repo.get(kind_id)

    def search_kinder(
        self,
        skip: int = 0,
        limit: int = 20,
        query: Optional[str] = None,
        sort_by: Optional[str] = "nachname",
        sort_order: Optional[str] = "asc"
    ) -> tuple[list[models.Kind], int]:
        """Search for Kinder with filtering, sorting, and pagination.

        Args:
            skip: Number of records to skip
            limit: Maximum number of records to return
            query: Optional search query
            sort_by: Field to sort by
            sort_order: Sort order (asc or desc)

        Returns:
            Tuple of (list of Kind instances, total count)
        """
        return self.repo.search(
            skip=skip,
            limit=limit,
            query=query,
            sort_by=sort_by,
            sort_order=sort_order
        )

    def update_kind(self, kind_id: int, kind_data: kind_schemas.KindUpdate) -> Optional[models.Kind]:
        """Update a Kind and handle side effects.

        If the Kind loses insurance status, all related Anmeldungen
        are marked as 'vorläufig' (preliminary).

        Args:
            kind_id: ID of the Kind to update
            kind_data: Updated Kind data

        Returns:
            Updated Kind model instance if found, None otherwise
        """
        # Get the existing Kind to check previous insurance status
        existing_kind = self.repo.get(kind_id)
        if not existing_kind:
            return None

        was_insured = self.is_insured(existing_kind)

        # Create a simulated updated kind to check insurance status
        # This allows us to detect insurance changes even with mocked repositories
        simulated_updated_kind = models.Kind(
            id=existing_kind.id,
            vorname=kind_data.vorname,
            nachname=kind_data.nachname,
            geburtsdatum=kind_data.geburtsdatum,
            geschlecht=kind_data.geschlecht,
            verein_id=kind_data.verein_id,
            verband_id=kind_data.verband_id,
            versicherung_id=kind_data.versicherung_id,
            vertrag=kind_data.vertrag
        )

        is_now_insured = self.is_insured(simulated_updated_kind)

        # Update the Kind in the database
        updated_kind = self.repo.update(kind_id, kind_data)
        if not updated_kind:
            return None

        # If Kind lost insurance, mark all related Anmeldungen as vorläufig
        if was_insured and not is_now_insured:
            self.repo.mark_anmeldungen_vorlaeufig(kind_id=kind_id)

        return updated_kind

    def delete_kind(self, kind_id: int) -> bool:
        """Delete a Kind.

        Args:
            kind_id: ID of the Kind to delete

        Returns:
            True if deleted, False if not found
        """
        return self.repo.delete(kind_id)

"""Anmeldung (Registration) Service - Business logic layer for Anmeldung domain."""
from datetime import date
from typing import List

from app import models
from app.anmeldung import schemas as anmeldung_schemas
from app.anmeldung.repository import AnmeldungRepository
from app.kind.repository import KindRepository
from app.wettkampf.repository import WettkampfRepository
from app.grunddaten.repository import FigurRepository


class AnmeldungService:
    """Service layer for Anmeldung domain business logic."""

    def __init__(
        self,
        anmeldung_repo: AnmeldungRepository,
        kind_repo: KindRepository,
        wettkampf_repo: WettkampfRepository,
        figur_repo: FigurRepository
    ):
        """Initialize service with required repositories."""
        self.anmeldung_repo = anmeldung_repo
        self.kind_repo = kind_repo
        self.wettkampf_repo = wettkampf_repo
        self.figur_repo = figur_repo

    def _is_kind_insured(self, kind: models.Kind) -> bool:
        """Check if a Kind has valid insurance coverage.

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

    def create_anmeldung(self, input_data: anmeldung_schemas.AnmeldungCreate) -> models.Anmeldung:
        """Create a new Anmeldung with business logic for vorläufig status.

        The registration is marked as 'vorläufig' (preliminary) if:
        1. Kind has no insurance coverage
        2. No figures are selected
        3. Maximum participants for the competition is reached

        Args:
            input_data: Anmeldung creation data

        Returns:
            Created Anmeldung model instance with status_reasons attribute
        """
        # Validate Wettkampf exists
        wettkampf = self.wettkampf_repo.get(input_data.wettkampf_id)
        if not wettkampf:
            raise ValueError("Wettkampf not found")

        # Validate Kind exists and check insurance
        kind = self.kind_repo.get(input_data.kind_id)
        if not kind:
            raise ValueError("Kind not found")

        # Determine if registration should be preliminary
        is_vorlaeufig = 0
        reasons = []

        # Check insurance
        if not self._is_kind_insured(kind):
            is_vorlaeufig = 1
            reasons.append("keine Versicherung")

        # Check figures
        if len(input_data.figur_ids) == 0:
            is_vorlaeufig = 1
            reasons.append("keine Figuren ausgewählt")

        # Check max participants
        if wettkampf.max_teilnehmer:
            final_count = self.anmeldung_repo.count_final_registrations(input_data.wettkampf_id)
            if final_count >= wettkampf.max_teilnehmer:
                is_vorlaeufig = 1
                reasons.append("maximale Teilnehmerzahl erreicht")

        # Get next startnummer
        next_startnummer = self.anmeldung_repo.get_next_startnummer(input_data.wettkampf_id)

        # Create a basic Anmeldung using repository
        # Note: The repository's create method creates a basic anmeldung
        # We then enhance it with business logic
        db_anmeldung = self.anmeldung_repo.create(input_data)

        # Apply business logic to the created anmeldung
        db_anmeldung.startnummer = next_startnummer
        db_anmeldung.anmeldedatum = date.today()
        db_anmeldung.vorlaeufig = is_vorlaeufig
        db_anmeldung.status = "vorläufig" if is_vorlaeufig else "aktiv"

        # Add figures using repository method if figures were selected
        if input_data.figur_ids:
            self.anmeldung_repo.set_figuren(db_anmeldung.id, input_data.figur_ids)
        else:
            # Commit if no figures to add (set_figuren commits internally)
            self.anmeldung_repo.db.commit()
            self.anmeldung_repo.db.refresh(db_anmeldung)

        # Add status_reasons as a dynamic attribute for the service layer
        db_anmeldung.status_reasons = reasons

        # Log preliminary registration reasons
        if is_vorlaeufig and reasons:
            print(f"ℹ️  Vorläufige Anmeldung #{next_startnummer}: {', '.join(reasons)}")

        return db_anmeldung

    def get_anmeldung(self, anmeldung_id: int) -> models.Anmeldung:
        """Get an Anmeldung by ID with details.

        Args:
            anmeldung_id: ID of the Anmeldung to retrieve

        Returns:
            Anmeldung model instance if found, None otherwise
        """
        return self.anmeldung_repo.get_with_details(anmeldung_id)

    def list_anmeldungen(self, skip: int = 0, limit: int = 100) -> List[models.Anmeldung]:
        """List all Anmeldungen with pagination.

        Args:
            skip: Number of records to skip
            limit: Maximum number of records to return

        Returns:
            List of Anmeldung instances
        """
        return self.anmeldung_repo.list(skip=skip, limit=limit)

    def delete_anmeldung(self, anmeldung_id: int) -> bool:
        """Delete an Anmeldung.

        Args:
            anmeldung_id: ID of the Anmeldung to delete

        Returns:
            True if deleted, False if not found
        """
        return self.anmeldung_repo.delete(anmeldung_id)

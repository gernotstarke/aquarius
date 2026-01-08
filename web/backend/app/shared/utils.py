"""Shared utility functions used across domains."""
from app import models, schemas


def kind_has_insurance(kind: models.Kind) -> bool:
    """Return True if a child has valid insurance coverage."""
    has_contract_insurance = bool(
        kind.versicherung_id and kind.vertrag and str(kind.vertrag).strip()
    )
    return bool(kind.verein_id or kind.verband_id or has_contract_insurance)


def anmeldung_with_insurance_ok(db_anmeldung: models.Anmeldung) -> schemas.Anmeldung:
    """Build Anmeldung schema with derived insurance status."""
    kind_dto = None
    if db_anmeldung.kind:
        # Explicitly convert ORM model to Pydantic model to ensure it's included
        kind_dto = schemas.Kind.model_validate(db_anmeldung.kind)

    return schemas.Anmeldung(
        id=db_anmeldung.id,
        kind_id=db_anmeldung.kind_id,
        wettkampf_id=db_anmeldung.wettkampf_id,
        startnummer=db_anmeldung.startnummer,
        anmeldedatum=db_anmeldung.anmeldedatum,
        vorlaeufig=db_anmeldung.vorlaeufig,
        status=db_anmeldung.status,
        figuren=db_anmeldung.figuren,
        insurance_ok=kind_has_insurance(db_anmeldung.kind),
        kind=kind_dto,
    )

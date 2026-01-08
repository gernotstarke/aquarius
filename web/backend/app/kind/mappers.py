"""Kind (Child) Domain - Mappers.

Mappers convert between domain models (ORM entities) and DTOs (API responses).
This decouples the API layer from the persistence layer.
"""
from typing import List, Optional

from app import models
from app.kind.dtos import KindDTO, VereinDTO, VerbandDTO, VersicherungDTO


def map_verein_to_dto(verein: Optional[models.Verein]) -> Optional[VereinDTO]:
    """Map Verein ORM model to DTO.

    Args:
        verein: Verein ORM model instance (may be None if not loaded)

    Returns:
        VereinDTO if verein exists, None otherwise
    """
    if not verein:
        return None

    return VereinDTO(
        id=verein.id,
        name=verein.name,
        ort=verein.ort,
        register_id=verein.register_id,
        contact=verein.contact
    )


def map_verband_to_dto(verband: Optional[models.Verband]) -> Optional[VerbandDTO]:
    """Map Verband ORM model to DTO.

    Args:
        verband: Verband ORM model instance (may be None if not loaded)

    Returns:
        VerbandDTO if verband exists, None otherwise
    """
    if not verband:
        return None

    return VerbandDTO(
        id=verband.id,
        name=verband.name,
        abkuerzung=verband.abkuerzung,
        land=verband.land,
        ort=verband.ort
    )


def map_versicherung_to_dto(versicherung: Optional[models.Versicherung]) -> Optional[VersicherungDTO]:
    """Map Versicherung ORM model to DTO.

    Args:
        versicherung: Versicherung ORM model instance (may be None if not loaded)

    Returns:
        VersicherungDTO if versicherung exists, None otherwise
    """
    if not versicherung:
        return None

    return VersicherungDTO(
        id=versicherung.id,
        name=versicherung.name,
        kurz=versicherung.kurz,
        land=versicherung.land,
        hauptsitz=versicherung.hauptsitz
    )


def map_kind_to_dto(kind: models.Kind) -> KindDTO:
    """Map Kind ORM model to DTO.

    This function converts a Kind entity from the domain/persistence layer
    to a DTO suitable for API responses. Related entities (verein, verband,
    versicherung) are mapped if they were eager-loaded.

    Args:
        kind: Kind ORM model instance

    Returns:
        KindDTO with all data mapped from the ORM model
    """
    return KindDTO(
        id=kind.id,
        vorname=kind.vorname,
        nachname=kind.nachname,
        geburtsdatum=kind.geburtsdatum,
        geschlecht=kind.geschlecht,
        verein_id=kind.verein_id,
        verband_id=kind.verband_id,
        versicherung_id=kind.versicherung_id,
        vertrag=kind.vertrag,
        # Map related entities if they exist
        verein=map_verein_to_dto(kind.verein) if hasattr(kind, 'verein') else None,
        verband=map_verband_to_dto(kind.verband) if hasattr(kind, 'verband') else None,
        versicherung=map_versicherung_to_dto(kind.versicherung) if hasattr(kind, 'versicherung') else None
    )


def map_kinder_to_dtos(kinder: List[models.Kind]) -> List[KindDTO]:
    """Map a list of Kind ORM models to DTOs.

    Args:
        kinder: List of Kind ORM model instances

    Returns:
        List of KindDTOs
    """
    return [map_kind_to_dto(kind) for kind in kinder]

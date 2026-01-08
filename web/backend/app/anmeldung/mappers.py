"""Anmeldung (Registration) Domain - Mappers.

Mappers convert between domain models (ORM entities) and DTOs (API responses).
This decouples the API layer from the persistence layer.
"""
from typing import List, Optional

from app import models
from app.anmeldung.dtos import (
    AnmeldungDTO,
    FigurDTO,
    KindDTOSimple,
    VereinDTOSimple,
    VerbandDTOSimple,
    VersicherungDTOSimple
)
from app.shared.utils import kind_has_insurance


def map_figur_to_dto(figur: models.Figur) -> FigurDTO:
    """Map Figur ORM model to DTO.

    Args:
        figur: Figur ORM model instance

    Returns:
        FigurDTO with all data mapped
    """
    return FigurDTO(
        id=figur.id,
        name=figur.name,
        kategorie=figur.kategorie,
        beschreibung=figur.beschreibung,
        schwierigkeitsgrad=figur.schwierigkeitsgrad,
        altersklasse=figur.altersklasse,
        bild=figur.bild
    )


def map_verein_to_simple_dto(verein: Optional[models.Verein]) -> Optional[VereinDTOSimple]:
    """Map Verein ORM model to simplified DTO.

    Args:
        verein: Verein ORM model instance (may be None if not loaded)

    Returns:
        VereinDTOSimple if verein exists, None otherwise
    """
    if not verein:
        return None

    return VereinDTOSimple(
        id=verein.id,
        name=verein.name,
        ort=verein.ort,
        register_id=verein.register_id,
        contact=verein.contact
    )


def map_verband_to_simple_dto(verband: Optional[models.Verband]) -> Optional[VerbandDTOSimple]:
    """Map Verband ORM model to simplified DTO.

    Args:
        verband: Verband ORM model instance (may be None if not loaded)

    Returns:
        VerbandDTOSimple if verband exists, None otherwise
    """
    if not verband:
        return None

    return VerbandDTOSimple(
        id=verband.id,
        name=verband.name,
        abkuerzung=verband.abkuerzung,
        land=verband.land,
        ort=verband.ort
    )


def map_versicherung_to_simple_dto(versicherung: Optional[models.Versicherung]) -> Optional[VersicherungDTOSimple]:
    """Map Versicherung ORM model to simplified DTO.

    Args:
        versicherung: Versicherung ORM model instance (may be None if not loaded)

    Returns:
        VersicherungDTOSimple if versicherung exists, None otherwise
    """
    if not versicherung:
        return None

    return VersicherungDTOSimple(
        id=versicherung.id,
        name=versicherung.name,
        kurz=versicherung.kurz,
        land=versicherung.land,
        hauptsitz=versicherung.hauptsitz
    )


def map_kind_to_simple_dto(kind: Optional[models.Kind]) -> Optional[KindDTOSimple]:
    """Map Kind ORM model to simplified DTO (with nested relationships).

    Args:
        kind: Kind ORM model instance (may be None if not loaded)

    Returns:
        KindDTOSimple if kind exists, None otherwise
    """
    if not kind:
        return None

    return KindDTOSimple(
        id=kind.id,
        vorname=kind.vorname,
        nachname=kind.nachname,
        geburtsdatum=kind.geburtsdatum,
        geschlecht=kind.geschlecht,
        verein_id=kind.verein_id,
        verband_id=kind.verband_id,
        versicherung_id=kind.versicherung_id,
        vertrag=kind.vertrag,
        # Map nested entities if they exist
        verein=map_verein_to_simple_dto(kind.verein) if hasattr(kind, 'verein') else None,
        verband=map_verband_to_simple_dto(kind.verband) if hasattr(kind, 'verband') else None,
        versicherung=map_versicherung_to_simple_dto(kind.versicherung) if hasattr(kind, 'versicherung') else None
    )


def map_anmeldung_to_dto(anmeldung: models.Anmeldung) -> AnmeldungDTO:
    """Map Anmeldung ORM model to DTO.

    This function converts an Anmeldung entity from the domain/persistence layer
    to a DTO suitable for API responses. Related entities (kind, figuren) are
    mapped if they were eager-loaded.

    The insurance_ok field is computed based on the Kind's insurance status.

    Args:
        anmeldung: Anmeldung ORM model instance

    Returns:
        AnmeldungDTO with all data mapped from the ORM model
    """
    # Compute insurance_ok if Kind is available
    insurance_ok = False
    if hasattr(anmeldung, 'kind') and anmeldung.kind:
        insurance_ok = kind_has_insurance(anmeldung.kind)

    # Map figuren if they exist
    figuren_dtos = []
    if hasattr(anmeldung, 'figuren') and anmeldung.figuren:
        figuren_dtos = [map_figur_to_dto(f) for f in anmeldung.figuren]

    # Map kind if it exists
    kind_dto = None
    if hasattr(anmeldung, 'kind'):
        kind_dto = map_kind_to_simple_dto(anmeldung.kind)

    return AnmeldungDTO(
        id=anmeldung.id,
        kind_id=anmeldung.kind_id,
        wettkampf_id=anmeldung.wettkampf_id,
        startnummer=anmeldung.startnummer,
        anmeldedatum=anmeldung.anmeldedatum,
        vorlaeufig=anmeldung.vorlaeufig,
        status=anmeldung.status,
        insurance_ok=insurance_ok,
        figuren=figuren_dtos,
        kind=kind_dto
    )


def map_anmeldungen_to_dtos(anmeldungen: List[models.Anmeldung]) -> List[AnmeldungDTO]:
    """Map a list of Anmeldung ORM models to DTOs.

    Args:
        anmeldungen: List of Anmeldung ORM model instances

    Returns:
        List of AnmeldungDTOs
    """
    return [map_anmeldung_to_dto(a) for a in anmeldungen]

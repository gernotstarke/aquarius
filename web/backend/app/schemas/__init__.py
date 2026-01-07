"""
Pydantic schemas for request/response validation.

This module now re-exports schemas from domain-specific modules for backward compatibility.
All schemas have been moved to their respective domain directories (Step 2 of DDD migration).
"""

# User schemas (not yet migrated to domain structure)
from .user import User, UserCreate, UserUpdate, Token, TokenData

# Re-export Grunddaten (Master Data) schemas
from app.grunddaten.schemas import (
    # Saison
    Saison,
    SaisonBase,
    SaisonCreate,
    SaisonUpdate,
    # Schwimmbad
    Schwimmbad,
    SchwimmbadBase,
    SchwimmbadCreate,
    SchwimmbadUpdate,
    # Verein
    Verein,
    VereinBase,
    VereinCreate,
    VereinUpdate,
    # Verband
    Verband,
    VerbandBase,
    VerbandCreate,
    VerbandUpdate,
    VerbandWithCount,
    # Versicherung
    Versicherung,
    VersicherungBase,
    VersicherungCreate,
    VersicherungUpdate,
    # Figur
    Figur,
    FigurBase,
    FigurCreate,
    FigurUpdate,
)

# Re-export Kind schemas
from app.kind.schemas import (
    Kind,
    KindBase,
    KindCreate,
    KindUpdate,
)

# Re-export Wettkampf schemas
from app.wettkampf.schemas import (
    Wettkampf,
    WettkampfBase,
    WettkampfCreate,
    WettkampfUpdate,
    WettkampfWithDetails,
)

# Re-export Anmeldung schemas
from app.anmeldung.schemas import (
    Anmeldung,
    AnmeldungCreate,
    AnmeldungUpdate,
)

__all__ = [
    # User
    "User",
    "UserCreate",
    "UserUpdate",
    "Token",
    "TokenData",
    # Grunddaten - Saison
    "Saison",
    "SaisonBase",
    "SaisonCreate",
    "SaisonUpdate",
    # Grunddaten - Schwimmbad
    "Schwimmbad",
    "SchwimmbadBase",
    "SchwimmbadCreate",
    "SchwimmbadUpdate",
    # Grunddaten - Verein
    "Verein",
    "VereinBase",
    "VereinCreate",
    "VereinUpdate",
    # Grunddaten - Verband
    "Verband",
    "VerbandBase",
    "VerbandCreate",
    "VerbandUpdate",
    "VerbandWithCount",
    # Grunddaten - Versicherung
    "Versicherung",
    "VersicherungBase",
    "VersicherungCreate",
    "VersicherungUpdate",
    # Grunddaten - Figur
    "Figur",
    "FigurBase",
    "FigurCreate",
    "FigurUpdate",
    # Kind
    "Kind",
    "KindBase",
    "KindCreate",
    "KindUpdate",
    # Wettkampf
    "Wettkampf",
    "WettkampfBase",
    "WettkampfCreate",
    "WettkampfUpdate",
    "WettkampfWithDetails",
    # Anmeldung
    "Anmeldung",
    "AnmeldungCreate",
    "AnmeldungUpdate",
]

# Resolve forward references now that all schemas are imported
# This is necessary for schemas that use TYPE_CHECKING imports
Kind.model_rebuild()
Anmeldung.model_rebuild()
WettkampfWithDetails.model_rebuild()

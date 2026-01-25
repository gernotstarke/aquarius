"""Anmeldung (Registration) Domain - Data Transfer Objects (DTOs).

DTOs are pure data containers for API responses, decoupled from database models.
They define the contract between the API and its clients.
"""
from datetime import date
from typing import List, Optional
from pydantic import BaseModel, Field, ConfigDict


class FigurDTO(BaseModel):
    """DTO for Figur (Figure) data in Anmeldung responses."""
    id: int
    name: str
    kategorie: Optional[str] = None
    beschreibung: Optional[str] = None
    schwierigkeitsgrad: Optional[float] = None
    altersklasse: Optional[str] = None
    bild: Optional[str] = None


class VereinDTOSimple(BaseModel):
    """Simplified DTO for Verein data in nested responses."""
    id: int
    name: str
    ort: str
    register_id: str
    contact: str


class VerbandDTOSimple(BaseModel):
    """Simplified DTO for Verband data in nested responses."""
    id: int
    name: str
    abkuerzung: str
    land: str
    ort: str


class VersicherungDTOSimple(BaseModel):
    """Simplified DTO for Versicherung data in nested responses."""
    id: int
    name: str
    kurz: str
    land: str
    hauptsitz: str


class KindDTOSimple(BaseModel):
    """Simplified DTO for Kind data in Anmeldung responses.

    Includes nested entities (verein, verband, versicherung) to prevent
    N+1 query problems. These are eagerly loaded and included in the response.
    """
    id: int
    vorname: str
    nachname: str
    geburtsdatum: date
    geschlecht: Optional[str] = None
    verein_id: Optional[int] = None
    verband_id: Optional[int] = None
    versicherung_id: Optional[int] = None
    vertrag: Optional[str] = None

    # Nested entities (included when eager-loaded)
    verein: Optional[VereinDTOSimple] = None
    verband: Optional[VerbandDTOSimple] = None
    versicherung: Optional[VersicherungDTOSimple] = None


class AnmeldungDTO(BaseModel):
    """Data Transfer Object for Anmeldung (Registration) API responses.

    This DTO is decoupled from the database layer and defines the
    contract for Anmeldung data exposed through the API.

    The 'insurance_ok' field is computed based on the Kind's insurance
    status and indicates whether the registration can be considered final.
    """
    id: int
    kind_id: int
    wettkampf_id: int
    startnummer: Optional[int] = None
    anmeldedatum: date
    vorlaeufig: int = Field(..., description="0 = final, 1 = preliminary")
    status: str = Field(..., description="Status: 'aktiv' or 'vorläufig'")

    # Computed field
    insurance_ok: bool = Field(..., description="Indicates if Kind has valid insurance")

    # Related entities (included when eager-loaded)
    figuren: List[FigurDTO] = Field(default_factory=list, description="Figures selected for this registration")
    kind: Optional[KindDTOSimple] = Field(None, description="Child data if eager-loaded")

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "id": 1,
                "kind_id": 5,
                "wettkampf_id": 10,
                "startnummer": 42,
                "anmeldedatum": "2025-01-05",
                "vorlaeufig": 0,
                "status": "aktiv",
                "insurance_ok": True,
                "figuren": [
                    {
                        "id": 1,
                        "name": "Barracuda",
                        "kategorie": "Intermediate",
                        "beschreibung": "Complex underwater rotation",
                        "schwierigkeitsgrad": 7.5,
                        "altersklasse": "12-14",
                        "bild": None
                    }
                ],
                "kind": {
                    "id": 5,
                    "vorname": "Anna",
                    "nachname": "Schmidt",
                    "geburtsdatum": "2015-03-15",
                    "geschlecht": "W",
                    "verein_id": 3,
                    "verband_id": None,
                    "versicherung_id": None,
                    "vertrag": None
                }
            }
        }
    )

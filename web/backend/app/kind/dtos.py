"""Kind (Child) Domain - Data Transfer Objects (DTOs).

DTOs are pure data containers for API responses, decoupled from database models.
They define the contract between the API and its clients.
"""
from datetime import date
from typing import Optional
from pydantic import BaseModel, Field


class VereinDTO(BaseModel):
    """DTO for Verein (Club) data in Kind responses."""
    id: int
    name: str
    ort: str
    register_id: str
    contact: str


class VerbandDTO(BaseModel):
    """DTO for Verband (Association) data in Kind responses."""
    id: int
    name: str
    abkuerzung: str
    land: str
    ort: str


class VersicherungDTO(BaseModel):
    """DTO for Versicherung (Insurance) data in Kind responses."""
    id: int
    name: str
    kurz: str
    land: str
    hauptsitz: str


class KindDTO(BaseModel):
    """Data Transfer Object for Kind (Child) API responses.

    This DTO is decoupled from the database layer and defines the
    contract for Kind data exposed through the API.

    Nested objects (verein, verband, versicherung) are included when
    eager-loaded, allowing clients to access related data without
    additional requests.
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

    # Related entities (included when eager-loaded)
    verein: Optional[VereinDTO] = None
    verband: Optional[VerbandDTO] = None
    versicherung: Optional[VersicherungDTO] = None

    class Config:
        """Pydantic configuration."""
        json_schema_extra = {
            "example": {
                "id": 1,
                "vorname": "Anna",
                "nachname": "Schmidt",
                "geburtsdatum": "2015-03-15",
                "geschlecht": "W",
                "verein_id": 5,
                "verband_id": None,
                "versicherung_id": None,
                "vertrag": None,
                "verein": {
                    "id": 5,
                    "name": "SC Neptun",
                    "ort": "Berlin",
                    "register_id": "VR12345",
                    "contact": "info@neptun.de"
                },
                "verband": None,
                "versicherung": None
            }
        }

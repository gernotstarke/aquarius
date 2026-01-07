"""Grunddaten (Master Data) schemas - Saison, Schwimmbad, Verein, Verband, Versicherung, Figur."""
from datetime import date
from pydantic import BaseModel, ConfigDict


# Saison Schemas
class SaisonBase(BaseModel):
    name: str
    from_date: date
    to_date: date


class SaisonCreate(SaisonBase):
    pass


class SaisonUpdate(SaisonBase):
    pass


class Saison(SaisonBase):
    model_config = ConfigDict(from_attributes=True)
    id: int


# Schwimmbad Schemas
class SchwimmbadBase(BaseModel):
    name: str
    adresse: str
    phone_no: str | None = None
    manager: str | None = None


class SchwimmbadCreate(SchwimmbadBase):
    pass


class SchwimmbadUpdate(SchwimmbadBase):
    pass


class Schwimmbad(SchwimmbadBase):
    model_config = ConfigDict(from_attributes=True)
    id: int


# Verein Schemas
class VereinBase(BaseModel):
    name: str
    ort: str
    register_id: str
    contact: str


class VereinCreate(VereinBase):
    pass


class VereinUpdate(VereinBase):
    pass


class Verein(VereinBase):
    model_config = ConfigDict(from_attributes=True)
    id: int


# Verband Schemas
class VerbandBase(BaseModel):
    name: str
    abkuerzung: str
    land: str
    ort: str


class VerbandCreate(VerbandBase):
    pass


class VerbandUpdate(VerbandBase):
    pass


class Verband(VerbandBase):
    model_config = ConfigDict(from_attributes=True)
    id: int


class VerbandWithCount(Verband):
    nomination_count: int


# Versicherung Schemas
class VersicherungBase(BaseModel):
    name: str
    kurz: str
    land: str
    hauptsitz: str


class VersicherungCreate(VersicherungBase):
    pass


class VersicherungUpdate(VersicherungBase):
    pass


class Versicherung(VersicherungBase):
    model_config = ConfigDict(from_attributes=True)
    id: int


# Figur Schemas
class FigurBase(BaseModel):
    name: str
    kategorie: str | None = None
    beschreibung: str | None = None
    schwierigkeitsgrad: float | None = None
    altersklasse: str | None = None
    bild: str | None = None


class FigurCreate(FigurBase):
    pass


class FigurUpdate(FigurBase):
    pass


class Figur(FigurBase):
    model_config = ConfigDict(from_attributes=True)
    id: int

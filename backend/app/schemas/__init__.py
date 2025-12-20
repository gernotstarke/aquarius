"""Pydantic schemas for request/response validation."""
from datetime import date
from typing import List
from pydantic import BaseModel


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
    id: int

    class Config:
        from_attributes = True


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
    id: int

    class Config:
        from_attributes = True


# Wettkampf Schemas
class WettkampfBase(BaseModel):
    name: str
    datum: date
    max_teilnehmer: int | None = None
    saison_id: int
    schwimmbad_id: int


class WettkampfCreate(WettkampfBase):
    pass


class WettkampfUpdate(WettkampfBase):
    pass


class Wettkampf(WettkampfBase):
    id: int

    class Config:
        from_attributes = True


# Kind Schemas
class KindBase(BaseModel):
    vorname: str
    nachname: str
    geburtsdatum: date
    geschlecht: str | None = None
    verein: str | None = None


class KindCreate(KindBase):
    pass


class KindUpdate(KindBase):
    pass


class Kind(KindBase):
    id: int

    class Config:
        from_attributes = True


# Figur Schemas
class FigurBase(BaseModel):
    name: str
    beschreibung: str | None = None
    schwierigkeitsgrad: int | None = None
    kategorie: str | None = None
    min_alter: int | None = None


class FigurCreate(FigurBase):
    pass


class FigurUpdate(FigurBase):
    pass


class Figur(FigurBase):
    id: int

    class Config:
        from_attributes = True


# Anmeldung Schemas
class AnmeldungBase(BaseModel):
    kind_id: int
    wettkampf_id: int
    anmeldedatum: date
    status: str = "aktiv"


class AnmeldungCreate(BaseModel):
    kind_id: int
    wettkampf_id: int
    figur_ids: List[int]  # List of figure IDs the child will perform


class AnmeldungUpdate(BaseModel):
    status: str | None = None
    figur_ids: List[int] | None = None


class Anmeldung(AnmeldungBase):
    id: int
    figuren: List[Figur] = []

    class Config:
        from_attributes = True


# Extended schemas with relationships
class WettkampfWithDetails(Wettkampf):
    """Wettkampf with related data."""
    figuren: List[Figur] = []
    anmeldungen: List[Anmeldung] = []

    class Config:
        from_attributes = True


class KindWithAnmeldungen(Kind):
    """Kind with their registrations."""
    anmeldungen: List[Anmeldung] = []

    class Config:
        from_attributes = True

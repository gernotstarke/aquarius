"""Pydantic schemas for request/response validation."""
from datetime import date
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
    verein_id: int | None = None
    verband_id: int | None = None
    versicherung_id: int | None = None
    vertrag: str | None = None


class KindCreate(KindBase):
    pass


class KindUpdate(KindBase):
    pass


class Kind(KindBase):
    id: int

    class Config:
        from_attributes = True

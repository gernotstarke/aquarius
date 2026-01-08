"""Pydantic schemas for request/response validation."""
from datetime import date
from typing import List, Optional
from pydantic import BaseModel, ConfigDict
from .user import User, UserCreate, UserUpdate, Token, TokenData

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
    model_config = ConfigDict(from_attributes=True)
    id: int

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

class KindUpdate(BaseModel):
    vorname: str | None = None
    nachname: str | None = None
    geburtsdatum: date | None = None
    geschlecht: str | None = None
    verein_id: int | None = None
    verband_id: int | None = None
    versicherung_id: int | None = None
    vertrag: str | None = None

class Kind(KindBase):
    model_config = ConfigDict(from_attributes=True)
    id: int
    verein: Optional[Verein] = None
    verband: Optional[Verband] = None
    versicherung: Optional[Versicherung] = None

# Anmeldung Schemas
class AnmeldungCreate(BaseModel):
    kind_id: int
    wettkampf_id: int
    figur_ids: List[int] = []

class AnmeldungUpdate(BaseModel):
    status: str | None = None
    vorlaeufig: int | None = None
    figur_ids: List[int] | None = None

class Anmeldung(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    kind_id: int
    wettkampf_id: int
    startnummer: int | None = None
    anmeldedatum: date
    vorlaeufig: int
    status: str
    figuren: List[Figur] = []
    insurance_ok: bool
    kind: Optional[Kind] = None

# Wettkampf With Details (Depends on Figur and Anmeldung)
class WettkampfWithDetails(Wettkampf):
    figuren: List[Figur] = []
    anmeldungen: List[Anmeldung] = []
    saison: Optional[Saison] = None
    schwimmbad: Optional[Schwimmbad] = None

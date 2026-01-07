"""Wettkampf (Competition) domain schemas."""
from datetime import date
from typing import List, Optional, TYPE_CHECKING
from pydantic import BaseModel, ConfigDict

if TYPE_CHECKING:
    from app.grunddaten.schemas import Figur, Saison, Schwimmbad
    from app.anmeldung.schemas import Anmeldung


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


# Wettkampf With Details (Depends on Figur and Anmeldung)
class WettkampfWithDetails(Wettkampf):
    figuren: List["Figur"] = []
    anmeldungen: List["Anmeldung"] = []
    saison: Optional["Saison"] = None
    schwimmbad: Optional["Schwimmbad"] = None

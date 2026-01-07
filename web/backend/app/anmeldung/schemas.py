"""Anmeldung (Registration) domain schemas."""
from datetime import date
from typing import List, Optional, TYPE_CHECKING
from pydantic import BaseModel, ConfigDict

if TYPE_CHECKING:
    from app.grunddaten.schemas import Figur
    from app.kind.schemas import Kind


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
    figuren: List["Figur"] = []
    insurance_ok: bool
    kind: Optional["Kind"] = None

"""Kind (Child) domain schemas."""
from datetime import date
from typing import Optional, TYPE_CHECKING
from pydantic import BaseModel, ConfigDict

if TYPE_CHECKING:
    from app.grunddaten.schemas import Verein, Verband, Versicherung


# Kind Schemas
class KindBase(BaseModel):
    vorname: str
    nachname: str
    email: str | None = None
    geburtsdatum: date
    geschlecht: str | None = None
    verein_id: int | None = None
    verband_id: int | None = None
    versicherung_id: int | None = None
    vertrag: str | None = None


class KindCreate(KindBase):
    password: str | None = None  # Optional for self-registration


class KindUpdate(BaseModel):
    """Schema for partial Kind updates - all fields optional."""
    vorname: str | None = None
    nachname: str | None = None
    email: str | None = None
    password: str | None = None  # If provided, will be hashed
    geburtsdatum: date | None = None
    geschlecht: str | None = None
    verein_id: int | None = None
    verband_id: int | None = None
    versicherung_id: int | None = None
    vertrag: str | None = None


class Kind(KindBase):
    model_config = ConfigDict(from_attributes=True)
    id: int
    verein: Optional["Verein"] = None
    verband: Optional["Verband"] = None
    versicherung: Optional["Versicherung"] = None

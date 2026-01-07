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
    model_config = ConfigDict(from_attributes=True)
    id: int
    verein: Optional["Verein"] = None
    verband: Optional["Verband"] = None
    versicherung: Optional["Versicherung"] = None

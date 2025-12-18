# ADR-018: Domain-Driven Design mit Bounded Contexts

**Status:** Accepted
**Datum:** 2025-12-18
**Entscheider:** Entwicklungsteam
**Bezieht sich auf:** [ADR-014 FastAPI Backend](ADR-014-python-fastapi-backend.md)

---

## Kontext

Das Aquarius-Backend muss eine **komplexe fachliche Domäne** abbilden:

**Fachliche Komplexität:**
- Wettkampf-Organisation (Stationen, Durchgänge, Gruppen)
- Anmeldungs-Logik (Startnummernvergabe, Doppelmeldungen)
- Bewertungs-Berechnung (Streichung höchster/niedrigster, Schwierigkeitsfaktor)
- Verschiedene Rollen (Präsident, Verein, Punktrichter, Stationsleiter)
- Geschäftsprozesse über mehrere Entitäten (Saison → Wettkampf → Anmeldung → Bewertung)

**Herausforderungen:**
- Code-Struktur muss fachliche Prozesse widerspiegeln
- Wartbarkeit durch Ehrenamtliche (unterschiedliche Skill-Levels)
- Klare Verantwortlichkeiten (welches Modul macht was?)
- Vermeidung von "Big Ball of Mud"

## Entscheidung

Wir strukturieren das Backend nach **Domain-Driven Design (DDD)** Prinzipien mit **6 Bounded Contexts**.

### Bounded Contexts

```
┌─────────────────────────────────────────────────────┐
│              Aquarius Backend                       │
├─────────────────────────────────────────────────────┤
│                                                      │
│  ┌────────────────┐     ┌────────────────┐         │
│  │  Stammdaten    │     │ Saisonplanung  │         │
│  │                │     │                │         │
│  │ • Verein       │     │ • Saison       │         │
│  │ • Team         │     │ • Figur        │         │
│  │ • Kind         │     │ • Wettkampf    │         │
│  │ • Offizieller  │     │ • Schwimmbad   │         │
│  └────────────────┘     └────────────────┘         │
│                                                      │
│  ┌────────────────┐     ┌────────────────┐         │
│  │  Anmeldung     │     │  Wettkampf     │         │
│  │                │     │                │         │
│  │ • Registrierung│     │ • Station      │         │
│  │ • Startnummer  │     │ • Gruppe       │         │
│  │ • Validierung  │     │ • Durchgang    │         │
│  └────────────────┘     └────────────────┘         │
│                                                      │
│  ┌────────────────┐     ┌────────────────┐         │
│  │  Bewertung     │     │  Auswertung    │         │
│  │                │     │                │         │
│  │ • Performance  │     │ • Rangliste    │         │
│  │ • Berechnung   │     │ • Preisvergabe │         │
│  │ • Validierung  │     │ • Export       │         │
│  └────────────────┘     └────────────────┘         │
└─────────────────────────────────────────────────────┘
```

### Modul-Struktur

Jedes Bounded Context folgt dem **3-Schichten-Modell**:

```
app/modules/{context}/
├── models/          # SQLAlchemy Models (Entitäten)
├── schemas/         # Pydantic DTOs (API-Kontrakte)
├── repositories/    # Data Access Layer
├── services/        # Business Logic Layer
└── routers/         # API Endpoints (REST)
```

## Begründung

### Pro Domain-Driven Design

**Vorteile:**
- ✅ **Fachliche Sprache**: Code verwendet Domain-Begriffe (Ubiquitous Language)
- ✅ **Klare Grenzen**: Jedes Modul hat definierte Verantwortlichkeit
- ✅ **Wartbarkeit**: Änderungen sind lokal begrenzt
- ✅ **Testbarkeit**: Module können isoliert getestet werden
- ✅ **Team-Skalierung**: Verschiedene Entwickler können parallel arbeiten
- ✅ **Verständlichkeit**: Fachexperten verstehen Code-Struktur

**Bounded Contexts:**
- ✅ Vermeiden von God-Objects
- ✅ Keine zyklischen Abhängigkeiten
- ✅ Klare Schnittstellen zwischen Modulen

**3-Schichten-Architektur:**
- ✅ Separation of Concerns
- ✅ Router: HTTP-Handling
- ✅ Service: Business-Logic
- ✅ Repository: Datenzugriff

### Alternative: Monolithische Struktur

```
app/
├── models.py        # Alle 15+ Entitäten in einer Datei
├── api.py           # Alle Endpoints in einer Datei
└── crud.py          # Alle DB-Operationen
```

**Contra:**
- ❌ Unübersichtlich bei Wachstum
- ❌ Merge-Konflikte bei paralleler Entwicklung
- ❌ Schwer testbar (alles gekoppelt)
- ❌ Keine fachlichen Grenzen

**Entscheidung gegen Monolith:** Nicht wartbar, keine Skalierung

### Alternative: Feature-basierte Struktur

```
app/
├── features/
│   ├── user_registration/
│   ├── competition_scoring/
│   └── results_export/
```

**Pro:**
- ✅ Gruppierung nach Use-Cases

**Contra:**
- ❌ Weniger fachliche Kohäsion (Features schneiden quer durch Domäne)
- ❌ Schwieriger, Bounded Contexts zu identifizieren
- ❌ Mehr Code-Duplizierung (Entitäten in mehreren Features)

**Entscheidung gegen Feature-basiert:** DDD ist besser für fachliche Domäne

### Alternative: Microservices

**Pro:**
- ✅ Unabhängiges Deployment pro Service
- ✅ Technology-Heterogenität

**Contra:**
- ❌ **Overkill** für kleine Liga (20 Kinder)
- ❌ Deployment-Komplexität (6+ Services)
- ❌ Netzwerk-Overhead zwischen Services
- ❌ Distributed Transactions kompliziert

**Entscheidung gegen Microservices:** Zu komplex für Projektgröße

## Konsequenzen

### Positiv

1. **Ubiquitous Language**: Code spricht fachliche Sprache (Anmeldung, Durchgang, etc.)
2. **Modulare Struktur**: Jedes Modul eigenständig wartbar
3. **Klare Abhängigkeiten**: Stammdaten/Saisonplanung unabhängig, andere Module darauf aufbauend
4. **Testbarkeit**: Service-Layer mit gemockten Repositories testbar
5. **Onboarding**: Neue Entwickler finden sich schnell zurecht

### Negativ

1. **Boilerplate**: Mehr Dateien/Klassen als Monolith
2. **Inter-Modul-Kommunikation**: Services müssen andere Services aufrufen
3. **Transaktionen**: Über mehrere Module hinweg komplexer
4. **Overhead**: Für sehr kleine Features viel Struktur

### Abhängigkeitsregeln

```
Auswertung
    ↓
Bewertung  →  Wettkampf
                 ↓
              Anmeldung
                 ↓
        ┌────────┴────────┐
        ↓                 ↓
   Stammdaten      Saisonplanung
```

**Regeln:**
1. **Keine zyklischen Abhängigkeiten**
2. **Nur über Service-Schnittstellen** (nie direkte Repository-Calls über Modulgrenzen)
3. **Top-Down Flow**: Auswertung → Bewertung → Wettkampf → Anmeldung → Basis

### Risiken

| Risiko | Wahrscheinlichkeit | Impact | Mitigation |
|--------|-------------------|--------|------------|
| Zu viel Boilerplate bei kleinen Features | Mittel | Niedrig | Pragmatischer Ansatz, keine Dogmatik |
| Inter-Modul-Calls verlangsamen System | Niedrig | Niedrig | Alles in einem Prozess, keine Netzwerk-Calls |
| Abhängigkeiten werden zyklisch | Niedrig | Hoch | Code-Reviews, Abhängigkeits-Graphen validieren |

## Implementierung

### 1. Modul-Struktur (Beispiel: Anmeldung)

```
app/modules/anmeldung/
├── __init__.py
├── models.py              # Anmeldung Entity
├── schemas.py             # AnmeldungCreate, AnmeldungResponse
├── repository.py          # AnmeldungRepository
├── service.py             # AnmeldungService
└── router.py              # /api/anmeldungen Endpoints
```

### 2. Entity (Model)

```python
# app/modules/anmeldung/models.py
from sqlalchemy import Column, Integer, ForeignKey, Enum, DateTime
from sqlalchemy.orm import relationship, Mapped, mapped_column
from app.database import Base
import enum

class AnmeldungStatus(enum.Enum):
    VORLAEUFIG = "vorlaeufig"
    BESTAETIGT = "bestaetigt"
    STORNIERT = "storniert"

class Anmeldung(Base):
    __tablename__ = "anmeldung"

    id: Mapped[int] = mapped_column(primary_key=True)
    kind_id: Mapped[int] = mapped_column(ForeignKey("kind.id"))
    wettkampf_id: Mapped[int] = mapped_column(ForeignKey("wettkampf.id"))
    startnummer: Mapped[int | None]
    status: Mapped[AnmeldungStatus]
    erstellt_am: Mapped[datetime] = mapped_column(default=datetime.utcnow)

    # Relationships
    kind: Mapped["Kind"] = relationship(back_populates="anmeldungen")
    wettkampf: Mapped["Wettkampf"] = relationship(back_populates="anmeldungen")
```

### 3. DTOs (Schemas)

```python
# app/modules/anmeldung/schemas.py
from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional

class AnmeldungCreate(BaseModel):
    """Request DTO für neue Anmeldung"""
    kind_id: int = Field(..., description="ID des Kindes")
    wettkampf_id: int = Field(..., description="ID des Wettkampfs")
    figuren: list[int] = Field(..., description="Gewünschte Figuren")

class AnmeldungResponse(BaseModel):
    """Response DTO"""
    id: int
    kind_id: int
    wettkampf_id: int
    startnummer: Optional[int]
    status: str
    erstellt_am: datetime

    model_config = {"from_attributes": True}
```

### 4. Repository (Data Access)

```python
# app/modules/anmeldung/repository.py
from sqlalchemy.orm import Session
from .models import Anmeldung
from typing import Optional

class AnmeldungRepository:
    def __init__(self, session: Session):
        self.session = session

    def find_by_id(self, id: int) -> Optional[Anmeldung]:
        return self.session.get(Anmeldung, id)

    def find_by_kind_und_wettkampf(
        self, kind_id: int, wettkampf_id: int
    ) -> Optional[Anmeldung]:
        return self.session.query(Anmeldung).filter(
            Anmeldung.kind_id == kind_id,
            Anmeldung.wettkampf_id == wettkampf_id
        ).first()

    def get_max_startnummer(self, wettkampf_id: int) -> Optional[int]:
        result = self.session.query(func.max(Anmeldung.startnummer)).filter(
            Anmeldung.wettkampf_id == wettkampf_id
        ).scalar()
        return result

    def save(self, anmeldung: Anmeldung) -> Anmeldung:
        self.session.add(anmeldung)
        self.session.commit()
        self.session.refresh(anmeldung)
        return anmeldung
```

### 5. Service (Business Logic)

```python
# app/modules/anmeldung/service.py
from .repository import AnmeldungRepository
from .models import Anmeldung, AnmeldungStatus
from .schemas import AnmeldungCreate
from app.modules.stammdaten.services import KindService
from app.modules.saisonplanung.services import WettkampfService

class DoppelmeldungError(Exception):
    pass

class AnmeldungService:
    def __init__(
        self,
        anmeldung_repo: AnmeldungRepository,
        kind_service: KindService,
        wettkampf_service: WettkampfService
    ):
        self.anmeldung_repo = anmeldung_repo
        self.kind_service = kind_service
        self.wettkampf_service = wettkampf_service

    def create_anmeldung(self, data: AnmeldungCreate) -> Anmeldung:
        """
        Geschäftslogik für Anmeldung:
        1. Kind validieren
        2. Wettkampf prüfen
        3. Doppelmeldung ausschließen
        4. Anmeldung erstellen
        """
        # 1. Kind validieren
        kind = self.kind_service.get_kind(data.kind_id)
        if not kind.ist_startberechtigt:
            raise ValueError("Kind ist nicht startberechtigt")

        # 2. Wettkampf prüfen
        wettkampf = self.wettkampf_service.get_wettkampf(data.wettkampf_id)
        if wettkampf.ist_voll():
            raise ValueError("Wettkampf ist ausgebucht")

        # 3. Doppelmeldung
        existing = self.anmeldung_repo.find_by_kind_und_wettkampf(
            data.kind_id, data.wettkampf_id
        )
        if existing:
            raise DoppelmeldungError("Kind bereits angemeldet")

        # 4. Anmeldung erstellen
        anmeldung = Anmeldung(
            kind_id=data.kind_id,
            wettkampf_id=data.wettkampf_id,
            status=AnmeldungStatus.VORLAEUFIG
        )

        return self.anmeldung_repo.save(anmeldung)

    def vergebe_startnummer(self, anmeldung_id: int) -> int:
        """Startnummer vergeben mit Optimistic Lock"""
        anmeldung = self.anmeldung_repo.find_by_id(anmeldung_id)
        max_nummer = self.anmeldung_repo.get_max_startnummer(
            anmeldung.wettkampf_id
        )
        neue_nummer = (max_nummer or 0) + 1

        anmeldung.startnummer = neue_nummer
        anmeldung.status = AnmeldungStatus.BESTAETIGT

        try:
            self.anmeldung_repo.save(anmeldung)
        except StaleDataError:
            # Retry bei Konflikt
            return self.vergebe_startnummer(anmeldung_id)

        return neue_nummer
```

### 6. Router (API Layer)

```python
# app/modules/anmeldung/router.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from .schemas import AnmeldungCreate, AnmeldungResponse
from .service import AnmeldungService, DoppelmeldungError
from .repository import AnmeldungRepository

router = APIRouter(prefix="/api/anmeldungen", tags=["anmeldung"])

def get_anmeldung_service(db: Session = Depends(get_db)) -> AnmeldungService:
    """Dependency Injection für Service"""
    anmeldung_repo = AnmeldungRepository(db)
    # ... andere Dependencies
    return AnmeldungService(anmeldung_repo, kind_service, wettkampf_service)

@router.post("/", response_model=AnmeldungResponse, status_code=status.HTTP_201_CREATED)
async def create_anmeldung(
    data: AnmeldungCreate,
    service: AnmeldungService = Depends(get_anmeldung_service)
):
    """Neue Anmeldung erstellen"""
    try:
        anmeldung = service.create_anmeldung(data)
        return anmeldung
    except DoppelmeldungError as e:
        raise HTTPException(status_code=409, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/{id}/startnummer", response_model=dict)
async def vergebe_startnummer(
    id: int,
    service: AnmeldungService = Depends(get_anmeldung_service)
):
    """Startnummer für Anmeldung vergeben"""
    startnummer = service.vergebe_startnummer(id)
    return {"startnummer": startnummer}
```

## Validierung

### Success Criteria

- ✅ **Keine zyklischen Abhängigkeiten** (validiert mit dependency-graph)
- ✅ **Jedes Modul hat klare Verantwortlichkeit**
- ✅ **Service-Layer ohne DB-Abhängigkeit** (mocking möglich)
- ✅ **Ubiquitous Language** durchgängig verwendet
- ✅ **Test-Coverage > 80%** pro Modul

### Metriken

```bash
# Abhängigkeits-Graph generieren
pydeps app --max-bacon=3 --cluster

# Zyklische Abhängigkeiten finden
pydeps app --show-cycles

# Test-Coverage pro Modul
pytest --cov=app/modules/anmeldung --cov-report=term
```

## Referenzen

- [Domain-Driven Design (Eric Evans)](https://www.domainlanguage.com/ddd/)
- [Implementing Domain-Driven Design (Vaughn Vernon)](https://vaughnvernon.co/)
- [Bounded Context (Martin Fowler)](https://martinfowler.com/bliki/BoundedContext.html)

## Historie

| Datum | Änderung | Autor |
|-------|----------|-------|
| 2025-12-18 | Initiale Version | Team |

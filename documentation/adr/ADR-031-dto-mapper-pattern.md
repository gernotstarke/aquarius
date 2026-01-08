# ADR-031: DTO/Mapper Pattern für API-Responses

**Status:** Accepted
**Datum:** 2026-01-08
**Entscheider:** Entwicklungsteam
**Bezieht sich auf:** [ADR-018 Domain-Driven Design](ADR-018-domain-driven-design.md)

---

## Kontext

Im Rahmen der DDD-Migration (siehe [Issue #38](https://github.com/gernotstarke/aquarius/issues/38)) haben wir festgestellt, dass unsere API-Responses zu eng an die SQLAlchemy ORM-Modelle gekoppelt sind:

**Probleme der aktuellen Implementierung:**
- Response-Schemas verwenden `ConfigDict(from_attributes=True)` → Direkte ORM-Kopplung
- Keine klare Trennung zwischen Domain-Modellen und API-Kontrakten
- Computed Fields (z.B. `insurance_ok`) werden inkonsistent berechnet
- Schwierige Testbarkeit durch ORM-Abhängigkeiten
- Eager Loading wird nicht explizit dokumentiert

**Beispiel (Problem):**
```python
# app/kind/schemas.py
class Kind(BaseModel):
    id: int
    vorname: str
    # ... weitere Felder

    model_config = ConfigDict(from_attributes=True)  # ⚠️  ORM-Kopplung!
```

## Entscheidung

Wir implementieren das **DTO/Mapper Pattern** zur Entkopplung von Domain-Modellen und API-Responses.

### Architektur-Übersicht

```
┌─────────────────────────────────────────────────────┐
│                    API Layer                        │
│  ┌─────────────┐        ┌─────────────┐            │
│  │   Router    │───────→│     DTO     │            │
│  └─────────────┘        └─────────────┘            │
│         ↓                                            │
│  ┌─────────────┐        ┌─────────────┐            │
│  │   Mapper    │───────→│   Domain    │            │
│  └─────────────┘        │   Models    │            │
│                         └─────────────┘            │
└─────────────────────────────────────────────────────┘
```

### Komponenten

1. **DTOs (Data Transfer Objects)**: Reine Datencontainer für API-Responses
2. **Mappers**: Konvertierungsfunktionen zwischen ORM-Modellen und DTOs
3. **Schemas**: Bleiben bestehen für Request-Validierung (Create/Update)

## Implementierung

### 1. DTOs erstellen

DTOs sind **reine Pydantic-Modelle ohne ORM-Kopplung**:

```python
# app/kind/dtos.py
from pydantic import BaseModel, Field
from datetime import date
from typing import Optional

class VereinDTO(BaseModel):
    """DTO für Verein-Daten in Kind-Responses."""
    id: int
    name: str
    ort: str
    register_id: str
    contact: str

class KindDTO(BaseModel):
    """Data Transfer Object für Kind API-Responses.

    Entkoppelt von der Datenbank-Schicht, definiert API-Kontrakt.
    """
    id: int
    vorname: str
    nachname: str
    geburtsdatum: date
    geschlecht: Optional[str] = None
    verein_id: Optional[int] = None

    # Nested entities (eagerly loaded)
    verein: Optional[VereinDTO] = None
    verband: Optional[VerbandDTO] = None
    versicherung: Optional[VersicherungDTO] = None

    # KEINE from_attributes - reine DTOs!
```

### 2. Mapper-Funktionen

Mapper konvertieren ORM → DTO und handhaben Eager Loading:

```python
# app/kind/mappers.py
from app import models
from app.kind.dtos import KindDTO, VereinDTO

def map_verein_to_dto(verein: Optional[models.Verein]) -> Optional[VereinDTO]:
    """Map Verein ORM model to DTO."""
    if not verein:
        return None

    return VereinDTO(
        id=verein.id,
        name=verein.name,
        ort=verein.ort,
        register_id=verein.register_id,
        contact=verein.contact
    )

def map_kind_to_dto(kind: models.Kind) -> KindDTO:
    """Map Kind ORM model to DTO.

    Mapped nested entities if eager-loaded using hasattr().
    """
    return KindDTO(
        id=kind.id,
        vorname=kind.vorname,
        nachname=kind.nachname,
        geburtsdatum=kind.geburtsdatum,
        geschlecht=kind.geschlecht,
        verein_id=kind.verein_id,
        # Map nested entities if eager-loaded
        verein=map_verein_to_dto(kind.verein) if hasattr(kind, 'verein') else None,
        verband=map_verband_to_dto(kind.verband) if hasattr(kind, 'verband') else None,
        versicherung=map_versicherung_to_dto(kind.versicherung) if hasattr(kind, 'versicherung') else None
    )

def map_kinder_to_dtos(kinder: List[models.Kind]) -> List[KindDTO]:
    """Map list of Kind ORM models to DTOs."""
    return [map_kind_to_dto(kind) for kind in kinder]
```

### 3. Router Integration

Router verwenden DTOs als `response_model` und rufen Mapper auf:

```python
# app/kind/router.py
from app.kind.dtos import KindDTO
from app.kind.mappers import map_kind_to_dto, map_kinder_to_dtos

@router.get("/kind", response_model=List[KindDTO])
def list_kind(
    skip: int = 0,
    limit: int = 20,
    service: KindService = Depends(get_kind_service)
):
    """Get list of all children."""
    results, total_count = service.search_kinder(skip=skip, limit=limit)

    # Map ORM models to DTOs
    return map_kinder_to_dtos(results)

@router.post("/kind", response_model=KindDTO, status_code=201)
def create_kind(kind: kind_schemas.KindCreate, service: KindService = Depends(get_kind_service)):
    """Create a new child."""
    created_kind = service.create_kind(kind)
    # Map ORM model to DTO
    return map_kind_to_dto(created_kind)
```

### 4. Eager Loading in Repositories

Repositories müssen nested entities eager loaden für vollständige DTOs:

```python
# app/anmeldung/repository.py
def list(self, skip: int = 0, limit: int = 100) -> List[models.Anmeldung]:
    """List all Anmeldungen with eager loading."""
    return self.db.query(models.Anmeldung).options(
        # Load Kind with nested entities
        joinedload(models.Anmeldung.kind).joinedload(models.Kind.verein),
        joinedload(models.Anmeldung.kind).joinedload(models.Kind.verband),
        joinedload(models.Anmeldung.kind).joinedload(models.Kind.versicherung)
    ).offset(skip).limit(limit).all()
```

### 5. Computed Fields

Computed Fields werden in Mappern berechnet:

```python
# app/anmeldung/mappers.py
def map_anmeldung_to_dto(anmeldung: models.Anmeldung) -> AnmeldungDTO:
    """Map Anmeldung ORM model to DTO."""
    # Compute insurance_ok if Kind is available
    insurance_ok = False
    if hasattr(anmeldung, 'kind') and anmeldung.kind:
        insurance_ok = kind_has_insurance(anmeldung.kind)

    return AnmeldungDTO(
        id=anmeldung.id,
        kind_id=anmeldung.kind_id,
        wettkampf_id=anmeldung.wettkampf_id,
        startnummer=anmeldung.startnummer,
        insurance_ok=insurance_ok,  # Computed field
        # ... weitere Felder
    )
```

## Pattern-Konventionen

### Naming Conventions

| Komponente | Naming | Beispiel |
|------------|--------|----------|
| DTO | `{Entity}DTO` | `KindDTO`, `AnmeldungDTO` |
| Nested DTO (simplified) | `{Entity}DTOSimple` | `KindDTOSimple` (in Anmeldung) |
| Mapper (single) | `map_{entity}_to_dto` | `map_kind_to_dto` |
| Mapper (list) | `map_{entities}_to_dtos` | `map_kinder_to_dtos` |
| File (DTOs) | `dtos.py` | `app/kind/dtos.py` |
| File (Mappers) | `mappers.py` | `app/kind/mappers.py` |

### Eager Loading Pattern

```python
# Repository: Define what to load
def list(self):
    return query.options(
        joinedload(Model.relation)
    ).all()

# Mapper: Check if loaded with hasattr()
def map_to_dto(model):
    return DTO(
        nested=map_nested(model.relation) if hasattr(model, 'relation') else None
    )
```

### Simplified DTOs für Nested Responses

Um tiefe Verschachtelungen zu vermeiden:

```python
# app/anmeldung/dtos.py
class KindDTOSimple(BaseModel):
    """Simplified Kind DTO for nested responses in Anmeldung."""
    id: int
    vorname: str
    nachname: str
    # Includes nested entities but avoids deep nesting
    verein: Optional[VereinDTOSimple] = None
```

## Konsequenzen

### Positiv ✅

1. **Klare Trennung**: API-Kontrakte unabhängig von Datenbank-Schema
2. **Testbarkeit**: DTOs sind reine Datenklassen, leicht zu testen
3. **Flexibilität**: API-Responses können unabhängig von DB-Struktur angepasst werden
4. **Explizite Mappings**: Dokumentiert durch Code, was im Response enthalten ist
5. **Computed Fields**: Einheitliche Stelle für Berechnungen (Mapper)
6. **JSON-Kompatibilität**: API-Kontrakt bleibt stabil

### Negativ ⚠️

1. **Boilerplate**: Mehr Code (DTOs + Mappers zusätzlich zu Schemas)
2. **Duplizierung**: DTOs ähneln oft stark den Schemas
3. **Wartungsaufwand**: Bei Schema-Änderungen müssen DTOs und Mapper angepasst werden
4. **Performance**: Zusätzlicher Mapping-Overhead (minimal)

### Risiken & Mitigationen

| Risiko | Wahrscheinlichkeit | Impact | Mitigation |
|--------|-------------------|--------|------------|
| DTOs und Schemas werden inkonsistent | Mittel | Mittel | Tests mit vollständigen API-Aufrufen |
| Vergessene Eager Loading führt zu N+1 | Mittel | Hoch | Tests prüfen Eager Loading explizit |
| Zu viele DTO-Varianten (Simple/Full) | Niedrig | Niedrig | Nur bei Bedarf erstellen |

## Validierung

### Test-Strategie

1. **Integration Tests**: Prüfen vollständige API-Responses inkl. nested entities
2. **Mapper Tests**: Unit-Tests für Mapper-Funktionen
3. **Eager Loading Tests**: Explizite Tests für N+1-Vermeidung

```python
# tests/integration/test_business_rules.py
def test_eager_loading_kind_in_anmeldung(client, db):
    """Verify Kind data is eagerly loaded with Anmeldung."""
    response = client.get("/api/anmeldung")
    anmeldungen = response.json()

    # Assert nested entities are present
    assert anmeldungen[0]["kind"] is not None
    assert anmeldungen[0]["kind"]["verein"] is not None  # Nested!
```

### Success Criteria

- ✅ Alle Tests bestanden (77 passed)
- ✅ JSON-Response-Struktur unverändert (Kompatibilität)
- ✅ Keine N+1 Queries (Eager Loading funktioniert)
- ✅ DTOs haben keine ORM-Kopplung (`from_attributes` entfernt)
- ✅ Computed Fields werden korrekt berechnet

## Migration-Pfad

Für neue Domains:

1. **DTOs erstellen** in `{domain}/dtos.py`
2. **Mapper erstellen** in `{domain}/mappers.py`
3. **Router anpassen**: `response_model=DTO` + Mapper-Aufruf
4. **Repository**: Eager Loading für nested entities
5. **Tests**: Integration-Tests für vollständige Responses

Bestehende Domains migrieren bei nächster Änderung (opportunistic refactoring).

## Referenzen

- **GitHub Issue**: [#38 - DDD Migration Step 6](https://github.com/gernotstarke/aquarius/issues/38)
- **Implementierte Domains**: `app/kind/`, `app/anmeldung/`
- **Test-Coverage**: `tests/mappers/`, `tests/integration/test_business_rules.py`

## Historie

| Datum | Änderung | Autor |
|-------|----------|-------|
| 2026-01-08 | Initiale Version | Team |

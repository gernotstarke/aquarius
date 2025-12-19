# ADR-005: Pydantic für Datenvalidierung

**Status:** Akzeptiert
**Datum:** 2025-12-17
**Entscheider:** Architektur-Team

## Kontext

Das Backend muss eingehende API-Requests validieren, Daten serialisieren/deserialisieren und Type-Safety garantieren zwischen API-Layer und Business-Logic.

## Entscheidung

Wir verwenden **Pydantic v2** für Datenvalidierung, Serialisierung und Settings-Management im Backend.

## Begründung

### Vorteile

- **FastAPI-Integration** - Native Unterstützung, automatische Dokumentation
- **Type Annotations** - Python Type Hints als Single Source of Truth
- **Automatische Validierung** - Request/Response-Validierung ohne Boilerplate
- **Performance** - Pydantic v2 ist Rust-basiert (sehr schnell)
- **JSON Schema** - Automatische OpenAPI-Dokumentation
- **Settings Management** - Environment Variables mit Type-Safety
- **Fehlerbehandlung** - Detaillierte Validierungsfehler

### Alternativen

| Alternative | Grund für Ablehnung |
|-------------|---------------------|
| **Marshmallow** | Langsamere Performance, mehr Boilerplate |
| **Dataclasses** | Keine Validierung, nur Structure |
| **Cerberus** | Separates Schema, nicht Type-Hint basiert |
| **Manuelle Validation** | Fehleranfällig, Wartungsaufwand |

## Konsequenzen

### Positiv

- Typsichere API-Endpoints
- Automatische Request-Validierung
- Selbst-dokumentierende API (OpenAPI/Swagger)
- Konsistente Fehlerbehandlung
- Settings aus Environment Variables type-safe

### Negativ

- Learning Curve für Pydantic v2 (minimal)
- Breaking Changes zwischen v1 und v2 (einmalige Migration)

## Technische Details

```python
from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime

# DTO Models
class AnmeldungCreate(BaseModel):
    """Request Schema für Anmeldung-Erstellung"""
    kind_id: int = Field(..., gt=0)
    wettkampf_id: int = Field(..., gt=0)
    figuren: list[int] = Field(default_factory=list)

    model_config = ConfigDict(from_attributes=True)

class AnmeldungResponse(BaseModel):
    """Response Schema für Anmeldung"""
    id: int
    kind_id: int
    wettkampf_id: int
    startnummer: int | None
    erstellt_am: datetime

# Settings Management
class Settings(BaseSettings):
    database_url: str = Field(..., alias="DATABASE_URL")
    turso_auth_token: str = Field(..., alias="TURSO_AUTH_TOKEN")
    log_level: str = Field(default="INFO")

    model_config = SettingsConfigDict(env_file=".env")

settings = Settings()
```

**Dependencies:**
```json
{
  "pydantic": "^2.5.0",
  "pydantic-settings": "^2.1.0"
}
```

## Integration

- **FastAPI Endpoints** - Automatische Request/Response-Validierung
- **SQLAlchemy Models** - `model_config = ConfigDict(from_attributes=True)`
- **Environment Config** - Type-safe Settings-Klassen

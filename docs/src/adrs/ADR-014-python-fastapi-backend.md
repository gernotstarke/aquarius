# ADR-014: Python + FastAPI als Backend-Framework

**Status:** Accepted
**Datum:** 2025-12-18
**Entscheider:** Entwicklungsteam
**Bezieht sich auf:** [ADR-015 Turso Database](ADR-015-turso-database.md), [ADR-018 Domain-Driven Design](ADR-018-domain-driven-design.md)

---

## Kontext

Das Aquarius-Backend muss folgende Anforderungen erfüllen:

**Funktionale Anforderungen:**
- REST API für zwei Frontend-Anwendungen
- Business-Logic für Wettkampf-Bewertung (komplex!)
- Datenvalidierung und -persistierung
- Berechnung von Endpunkten (Durchschnitt, Streichung, Schwierigkeitsfaktor)

**Nicht-funktionale Anforderungen:**
- **Performance**: Schnelle Response-Zeiten während Live-Bewertung
- **Wartbarkeit**: Ehrenamtliche Entwickler mit unterschiedlichen Skills
- **Lesbarkeit**: Code muss von Non-Experts verstanden werden
- **Typsicherheit**: Reduzierung von Runtime-Errors
- **API-Dokumentation**: Automatisch generiert

## Entscheidung

Wir verwenden **Python 3.11+** mit **FastAPI** als Backend-Framework.

### Technologie-Stack

```
Backend Stack:
├── Python 3.11+               (Programmiersprache)
├── FastAPI 0.109+             (Web Framework)
├── Pydantic v2                (Datenvalidierung)
├── SQLAlchemy 2.0             (ORM)
├── Alembic                    (Datenbank-Migrationen)
├── libsql-experimental        (Turso Client)
├── Uvicorn                    (ASGI Server)
└── Pytest                     (Testing Framework)
```

### Projektstruktur

```
backend/
├── app/
│   ├── main.py                # FastAPI App Entry
│   ├── database.py            # DB Connection
│   ├── models/                # SQLAlchemy Models
│   │   ├── kind.py
│   │   ├── wettkampf.py
│   │   └── ...
│   ├── schemas/               # Pydantic DTOs
│   │   ├── kind.py
│   │   └── ...
│   ├── routers/               # API Endpoints
│   │   ├── stammdaten.py
│   │   ├── anmeldung.py
│   │   └── ...
│   ├── services/              # Business Logic
│   │   ├── anmeldung_service.py
│   │   ├── bewertung_service.py
│   │   └── ...
│   └── repositories/          # Data Access
│       ├── kind_repository.py
│       └── ...
├── tests/
├── alembic/                   # DB Migrations
├── requirements.txt
└── pyproject.toml
```

## Begründung

### Pro Python + FastAPI

**Python:**
- ✅ **Lesbarkeit**: "Executable Pseudocode" - ideal für Ehrenamtliche
- ✅ **Reiches Ökosystem**: Zahlreiche Libraries für Data Processing
- ✅ **Community**: Große Community, viele Ressourcen
- ✅ **Data Science Ready**: Falls später Statistiken/ML gewünscht
- ✅ **Type Hints**: Python 3.11+ hat gute Type Support (mypy)

**FastAPI:**
- ✅ **Performance**: Einer der schnellsten Python-Frameworks (Starlette + Pydantic)
- ✅ **Async Support**: Native async/await für I/O-intensive Operationen
- ✅ **Automatische Docs**: OpenAPI (Swagger) out-of-the-box
- ✅ **Typsicherheit**: Pydantic-basierte Validation
- ✅ **Modern**: Python 3.6+ Type Hints als Basis
- ✅ **DX**: Exzellente Developer Experience, wenig Boilerplate

**Pydantic v2:**
- ✅ **Validation**: Automatische Request/Response-Validierung
- ✅ **Serialization**: JSON <-> Python Objects
- ✅ **Type Safety**: Runtime Type Checking
- ✅ **OpenAPI**: Automatische Schema-Generierung
- ✅ **Performance**: Pydantic v2 ist in Rust geschrieben (10x schneller)

### Alternative: Node.js + Express/NestJS

**Pro:**
- ✅ Eine Sprache (TypeScript) für Frontend + Backend
- ✅ Große Community

**Contra:**
- ❌ Callback Hell / Async-Komplexität
- ❌ Weniger lesbar für Non-Experts
- ❌ Validation erfordert zusätzliche Libraries (zod, class-validator)
- ❌ ORM-Landscape fragmentiert (Prisma, TypeORM, Sequelize)

**Entscheidung gegen Node:** Python ist lesbarer, FastAPI hat bessere DX

### Alternative: Java + Spring Boot

**Pro:**
- ✅ Enterprise-Ready, sehr ausgereift
- ✅ Starke Type Safety

**Contra:**
- ❌ Zu viel Boilerplate für kleine Liga (20 Kinder)
- ❌ Steile Lernkurve (Dependency Injection, Annotations)
- ❌ Langsamer Startup (JVM Warmup)
- ❌ Komplexer für Ehrenamtliche

**Entscheidung gegen Spring:** Overkill für Projektgröße

### Alternative: Go + Gin/Echo

**Pro:**
- ✅ Sehr performant, kompilierte Sprache
- ✅ Einfache Deployment (Single Binary)

**Contra:**
- ❌ Weniger lesbar (Error Handling: if err != nil)
- ❌ Keine ORM-Tradition (SQL-Builder statt ORM)
- ❌ Kleinere Community für Web-Entwicklung
- ❌ Weniger Libraries für Business-Logic

**Entscheidung gegen Go:** Python ist wartbarer für Team

## Konsequenzen

### Positiv

1. **Auto-Generated API Docs**: `/docs` Endpoint mit Swagger UI
2. **Type Safety**: Pydantic validiert Requests automatisch
3. **OpenAPI Client**: TypeScript-Client für Frontend auto-generierbar
4. **Testing**: Pytest ist sehr ausdrucksstark, einfach zu schreiben
5. **Async Support**: Nicht-blockierende DB-Operationen

### Negativ

1. **Performance**: Langsamer als kompilierte Sprachen (Go, Rust)
2. **GIL**: Global Interpreter Lock limitiert Threading (aber async ist OK)
3. **Deployment**: Python-Umgebung erforderlich (vs. Single Binary)
4. **Type Checking**: Optional, erfordert mypy für Compile-Time Checks

### Risiken

| Risiko | Wahrscheinlichkeit | Impact | Mitigation |
|--------|-------------------|--------|------------|
| Performance-Bottleneck bei 1000+ Wettkämpfen | Niedrig (20 Kinder Liga) | Mittel | Database Indexes, Query-Optimierung, Caching |
| Python-Versions-Inkompatibilität | Niedrig | Niedrig | Poetry/uv für Dependency Locking |
| Async-Code schwer zu debuggen | Mittel | Niedrig | Gute Tests, strukturiertes Exception Handling |

## Implementierung

### 1. FastAPI Application

```python
# app/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import stammdaten, anmeldung, bewertung

app = FastAPI(
    title="Aquarius API",
    description="Swimming Competition Rating System",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS für Frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:5174"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Router einbinden
app.include_router(stammdaten.router, prefix="/api/stammdaten", tags=["stammdaten"])
app.include_router(anmeldung.router, prefix="/api/anmeldungen", tags=["anmeldung"])
app.include_router(bewertung.router, prefix="/api/bewertungen", tags=["bewertung"])

@app.get("/health")
async def health_check():
    return {"status": "healthy"}
```

### 2. Pydantic Schemas

```python
# app/schemas/anmeldung.py
from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional

class AnmeldungCreate(BaseModel):
    """DTO für neue Anmeldung"""
    kind_id: int = Field(..., description="ID des Kindes")
    wettkampf_id: int = Field(..., description="ID des Wettkampfs")
    figuren: list[int] = Field(..., description="IDs der gewünschten Figuren")

class AnmeldungResponse(BaseModel):
    """DTO für Anmeldung in Response"""
    id: int
    kind_id: int
    wettkampf_id: int
    startnummer: Optional[int] = None
    status: str
    erstellt_am: datetime

    model_config = {"from_attributes": True}  # Für ORM Models
```

### 3. Repository Pattern

```python
# app/repositories/anmeldung_repository.py
from sqlalchemy.orm import Session
from app.models.anmeldung import Anmeldung
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

    def save(self, anmeldung: Anmeldung) -> Anmeldung:
        self.session.add(anmeldung)
        self.session.commit()
        self.session.refresh(anmeldung)
        return anmeldung
```

### 4. Service Layer

```python
# app/services/anmeldung_service.py
from app.repositories.anmeldung_repository import AnmeldungRepository
from app.schemas.anmeldung import AnmeldungCreate
from app.models.anmeldung import Anmeldung, AnmeldungStatus

class AnmeldungService:
    def __init__(
        self,
        anmeldung_repo: AnmeldungRepository,
        kind_service: "KindService",
        wettkampf_service: "WettkampfService"
    ):
        self.anmeldung_repo = anmeldung_repo
        self.kind_service = kind_service
        self.wettkampf_service = wettkampf_service

    def create_anmeldung(self, data: AnmeldungCreate) -> Anmeldung:
        # Business Logic
        kind = self.kind_service.get_kind(data.kind_id)
        if not kind.ist_startberechtigt:
            raise ValueError("Kind ist nicht startberechtigt")

        # Doppelmeldung prüfen
        existing = self.anmeldung_repo.find_by_kind_und_wettkampf(
            data.kind_id, data.wettkampf_id
        )
        if existing:
            raise ValueError("Kind bereits angemeldet")

        # Anmeldung erstellen
        anmeldung = Anmeldung(
            kind_id=data.kind_id,
            wettkampf_id=data.wettkampf_id,
            status=AnmeldungStatus.VORLAEUFIG
        )

        return self.anmeldung_repo.save(anmeldung)
```

## Validierung

### Success Criteria

- ✅ `/docs` Endpoint liefert vollständige OpenAPI-Spezifikation
- ✅ Alle Request/Response Bodies mit Pydantic validiert
- ✅ 100% Type Hints (mypy --strict ohne Errors)
- ✅ Test Coverage > 80%
- ✅ API Response Time < 100ms (p95)

### Metriken

```bash
# Type Checking
mypy app/ --strict

# Test Coverage
pytest --cov=app --cov-report=html

# Performance Testing
locust -f tests/load/locustfile.py --host=http://localhost:8000
```

## Referenzen

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Pydantic v2](https://docs.pydantic.dev/latest/)
- [SQLAlchemy 2.0](https://docs.sqlalchemy.org/en/20/)
- [Python Type Hints](https://docs.python.org/3/library/typing.html)

## Historie

| Datum | Änderung | Autor |
|-------|----------|-------|
| 2025-12-18 | Initiale Version | Team |

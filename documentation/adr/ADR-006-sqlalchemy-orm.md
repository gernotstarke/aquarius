# ADR-006: SQLAlchemy als ORM

**Status:** Akzeptiert
**Datum:** 2025-12-17
**Entscheider:** Architektur-Team

## Kontext

Das Backend benötigt einen Object-Relational Mapper (ORM) für Daten

zugriff auf die Turso/SQLite-Datenbank mit Type-Safety, Migrations-Support und Query-Building.

## Entscheidung

Wir verwenden **SQLAlchemy 2.0** mit dem neuen deklarativen Mapping-Stil als ORM.

## Begründung

### Vorteile

- **De-facto Standard** für Python ORMs
- **SQLAlchemy 2.0** - Moderne API mit Type Hints
- **Async Support** - Kompatibel mit FastAPI's async/await
- **Typsicherheit** - Vollständige MyPy/Pyright-Unterstützung
- **Flexible Queries** - Von einfachen bis zu komplexen Abfragen
- **Migrations** - Integration mit Alembic
- **Turso/libSQL-Kompatibilität** - SQLite-Dialekt funktioniert
- **Relationship Loading** - Lazy, Eager, Subquery Loading

### Alternativen

| Alternative | Grund für Ablehnung |
|-------------|---------------------|
| **Django ORM** | Benötigt Django Framework |
| **Tortoise ORM** | Kleinere Community, weniger Features |
| **Peewee** | Zu simpel für komplexe Queries |
| **Raw SQL** | Fehleranfällig, keine Type-Safety |
| **PonyORM** | Generatorbasierte Syntax ungewöhnlich |

## Konsequenzen

### Positiv

- Typsichere Datenbankabfragen
- Automatisches Schema-Management via Migrations
- Lazy/Eager Loading optimiert Performance
- N+1-Problem vermeidbar durch Relationship-Loading
- Testbarkeit durch In-Memory SQLite

### Negativ

- Learning Curve für SQLAlchemy 2.0 (mittlere Komplexität)
- Performance-Overhead bei sehr einfachen Queries (minimal)

## Technische Details

```python
from sqlalchemy import String, Integer, ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

class Base(DeclarativeBase):
    pass

class Anmeldung(Base):
    __tablename__ = "anmeldung"

    id: Mapped[int] = mapped_column(primary_key=True)
    kind_id: Mapped[int] = mapped_column(ForeignKey("kind.id"))
    wettkampf_id: Mapped[int] = mapped_column(ForeignKey("wettkampf.id"))
    startnummer: Mapped[int | None] = mapped_column()

    # Relationships
    kind: Mapped["Kind"] = relationship(back_populates="anmeldungen")
    wettkampf: Mapped["Wettkampf"] = relationship()

# Async Session Usage
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine

engine = create_async_engine("sqlite+aiosqlite:///aquarius.db")

async def get_anmeldung(session: AsyncSession, id: int) -> Anmeldung | None:
    return await session.get(Anmeldung, id)
```

**Dependencies:**
```json
{
  "sqlalchemy": "^2.0.0",
  "aiosqlite": "^0.19.0"  // Async SQLite driver
}
```

## Architektur-Integration

- **Repository Pattern** - SQLAlchemy Models in Repository-Schicht
- **3-Layer Architecture** - Repository → Service → Router
- **Async/Await** - AsyncSession für non-blocking DB-Access

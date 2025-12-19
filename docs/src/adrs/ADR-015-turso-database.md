# ADR-015: Turso (libSQL) als Datenbank

**Status:** Accepted
**Datum:** 2025-12-18
**Entscheider:** Entwicklungsteam
**Bezieht sich auf:** [ADR-014 FastAPI Backend](ADR-014-python-fastapi-backend.md), [ADR-016 PWA Architecture](ADR-016-pwa-architecture.md)

---

## Kontext

Die Aquarius-Anwendung muss in zwei unterschiedlichen Betriebsmodi funktionieren:

**1. Planungs-Modus (Online)**
- Büro/Desktop-Umgebung
- Stabile Internetverbindung
- Zentrale Datenverwaltung

**2. Durchführungs-Modus (Hybrid Online/Offline)**
- Schwimmbad-Umgebung
- **Kritisch**: Potenziell instabile/keine Internetverbindung
- Tablet-basiert (iPads, Android Tablets)
- Live-Bewertung darf nicht durch Netzwerkprobleme unterbrochen werden
- Automatische Synchronisation wenn Verbindung wieder da

**Anforderungen:**
- ✅ Offline-Fähigkeit für Tablets am Schwimmbad
- ✅ Automatische Synchronisation
- ✅ Konfliktauflösung (Last-Write-Wins ist OK für kleine Liga)
- ✅ Niedrige Latenz für Live-Bewertung
- ✅ Einfache Entwicklung (lokales SQLite

 für Tests)
- ✅ Günstiger Betrieb (kleine Liga, ~20 Kinder)

## Entscheidung

Wir verwenden **Turso (libSQL)** als Datenbank mit **Edge-Replication** und **Embedded Replicas**.

### Technologie-Stack

```
Database Stack:
├── Turso Cloud                # Primäre Datenbank (Edge-hosted)
│   ├── libSQL Server          # SQLite-kompatibler Server
│   ├── Edge Replication       # Multi-Region für Latenz
│   └── HTTP API               # Zugriff über HTTPS
├── Embedded Replicas          # Lokale SQLite auf Tablets
│   ├── libsql-client (Python) # Backend-Zugriff
│   └── Auto-Sync              # Bidirektionale Replikation
└── SQLite (Development)       # Lokale Entwicklung
```

### Architektur-Diagramm

```
                ┌─────────────────────────────┐
                │      Turso Cloud            │
                │   (Primary Database)        │
                │   - Edge Nodes (Global)     │
                └──────────┬──────────────────┘
                           │
           ┌───────────────┼───────────────┐
           │               │               │
           ▼               ▼               ▼
   ┌──────────────┐ ┌──────────────┐ ┌──────────────┐
   │   Backend    │ │  Tablet 1    │ │  Tablet 2    │
   │   Server     │ │  (Embedded)  │ │  (Embedded)  │
   │              │ │              │ │              │
   │  libSQL      │ │  libSQL      │ │  libSQL      │
   │  Client      │ │  Replica     │ │  Replica     │
   └──────────────┘ └──────────────┘ └──────────────┘
         │                 │                 │
         └─────────────────┴─────────────────┘
                    Sync when online
```

## Begründung

### Pro Turso (libSQL)

**SQLite-Kompatibilität:**
- ✅ Entwicklung mit lokalem SQLite (keine Cloud nötig)
- ✅ Bekanntes SQL-Syntax
- ✅ File-basiert, einfaches Backup
- ✅ Exzellente SQLAlchemy-Integration

**Edge-Replication:**
- ✅ Niedrige Latenz (nächster Edge-Node < 50ms)
- ✅ Global verteilt (Frankfurt, Amsterdam, etc.)
- ✅ Automatisches Failover

**Embedded Replicas:**
- ✅ **Offline-First**: Tablet funktioniert ohne Internet
- ✅ **Lokale Reads**: Keine Netzwerk-Latenz
- ✅ **Auto-Sync**: Automatische Synchronisation wenn Online
- ✅ **Conflict Resolution**: Last-Write-Wins (ausreichend für kleine Liga)

**Betrieb:**
- ✅ **Kostenlos bis 9 GB** Storage (mehr als genug für 20 Kinder)
- ✅ **Managed Service**: Keine Server-Verwaltung
- ✅ **Backups**: Automatisch, Point-in-Time Recovery
- ✅ **Schema-Migrationen**: Via Alembic (wie normale SQLite)

### Alternative: PostgreSQL + eigener Sync

**Pro:**
- ✅ Ausgereift, große Community
- ✅ Fortgeschrittene Features (Triggers, Stored Procedures)

**Contra:**
- ❌ Kein natives Offline-Support
- ❌ Eigener Sync-Mechanismus erforderlich (komplex!)
- ❌ Server-Betrieb erforderlich (Wartung, Updates)
- ❌ Höhere Kosten (Server + Traffic)

**Entscheidung gegen PostgreSQL:** Offline-Sync müssten wir selbst bauen

### Alternative: PouchDB + CouchDB

**Pro:**
- ✅ Offline-First Design
- ✅ Bidirektionale Sync

**Contra:**
- ❌ NoSQL (kein SQL, andere Query-Sprache)
- ❌ Keine Joins (denormalisiert)
- ❌ Weniger ORM-Support
- ❌ Komplexere Datenmodellierung für relationale Daten

**Entscheidung gegen CouchDB:** Relationales Modell passt besser

### Alternative: Supabase (PostgreSQL + Realtime)

**Pro:**
- ✅ PostgreSQL-basiert
- ✅ Realtime-Subscriptions

**Contra:**
- ❌ Kein natives Offline/Embedded
- ❌ Realtime nur über WebSocket (nicht für Tablets ideal)
- ❌ Teurer als Turso

**Entscheidung gegen Supabase:** Offline-Support nicht so gut wie Turso

## Konsequenzen

### Positiv

1. **Entwickler-Experience**: Lokales SQLite für Entwicklung/Tests
2. **Einfache Migrationen**: Alembic + SQLite/libSQL = bewährte Kombination
3. **Offline-Fähigkeit**: Wettkampf funktioniert auch ohne Internet
4. **Keine Server-Wartung**: Managed Service
5. **Günstiger Betrieb**: Free Tier reicht aus

### Negativ

1. **Beta-Status**: Turso ist noch relativ neu (seit 2023)
2. **Vendor Lock-In**: Embedded Replicas sind Turso-spezifisch
3. **Feature-Limit**: Weniger Features als PostgreSQL (keine Stored Procedures)
4. **Community**: Kleinere Community als PostgreSQL

### Risiken

| Risiko | Wahrscheinlichkeit | Impact | Mitigation |
|--------|-------------------|--------|------------|
| Turso-Service-Ausfall | Niedrig | Hoch | Embedded Replicas funktionieren offline, lokales Backup |
| Sync-Konflikte bei gleichzeitigen Schreibvorgängen | Mittel | Niedrig | Last-Write-Wins ist OK, keine kritischen Race Conditions |
| Migration zu anderer DB nötig | Niedrig | Hoch | SQLite-kompatibel → Einfacher Export, Standard SQL |
| Beta-Features brechen | Mittel | Mittel | Versionierung, gute Tests |

## Implementierung

### 1. Backend-Konfiguration

```python
# app/database.py
import os
from sqlalchemy import create_engine, event
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

load_dotenv()

# Turso Connection String
TURSO_DATABASE_URL = os.getenv(
    "TURSO_DATABASE_URL",
    "file:./aquarius.db"  # Fallback: lokales SQLite für Development
)
TURSO_AUTH_TOKEN = os.getenv("TURSO_AUTH_TOKEN", "")

# SQLAlchemy Engine
if TURSO_DATABASE_URL.startswith("libsql://"):
    # Production: Turso Cloud
    engine = create_engine(
        TURSO_DATABASE_URL,
        connect_args={"auth_token": TURSO_AUTH_TOKEN},
        echo=False
    )
else:
    # Development: lokales SQLite
    engine = create_engine(
        TURSO_DATABASE_URL,
        connect_args={"check_same_thread": False},
        echo=True
    )

# Foreign Keys aktivieren (wichtig für SQLite!)
@event.listens_for(engine, "connect")
def set_sqlite_pragma(dbapi_conn, connection_record):
    cursor = dbapi_conn.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    """Dependency für FastAPI"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
```

### 2. Embedded Replica (Frontend PWA)

```typescript
// frontend/apps/execution/src/lib/db.ts
import { createClient } from "@libsql/client";

const client = createClient({
  url: "libsql://aquarius-db.turso.io",
  authToken: import.meta.env.VITE_TURSO_AUTH_TOKEN,

  // Embedded Replica für Offline
  syncUrl: "libsql://aquarius-db.turso.io",
  syncInterval: 60, // Sync alle 60 Sekunden
});

// Sync manuell triggern
export async function syncDatabase() {
  await client.sync();
}

// Query-Funktion
export async function query<T>(sql: string, params: any[] = []): Promise<T[]> {
  const result = await client.execute({ sql, args: params });
  return result.rows as T[];
}
```

### 3. Alembic-Migrationen

```bash
# Initiale Migration erstellen
alembic revision --autogenerate -m "Initial schema"

# Migration auf Turso anwenden
TURSO_DATABASE_URL=libsql://aquarius-db.turso.io \
TURSO_AUTH_TOKEN=your_token \
alembic upgrade head
```

### 4. Connection String Beispiele

```bash
# .env.example

# Development (lokales SQLite)
TURSO_DATABASE_URL=file:./aquarius.db
TURSO_AUTH_TOKEN=

# Production (Turso Cloud)
TURSO_DATABASE_URL=libsql://aquarius-db.turso.io
TURSO_AUTH_TOKEN=eyJhbGc...your_token

# Test (In-Memory)
TURSO_DATABASE_URL=file::memory:?cache=shared
TURSO_AUTH_TOKEN=
```

## Validierung

### Success Criteria

- ✅ Backend kann mit lokalem SQLite UND Turso Cloud arbeiten
- ✅ Embedded Replica funktioniert offline (Tablet ohne Internet)
- ✅ Sync erfolgt automatisch bei Verbindung
- ✅ Alembic-Migrationen funktionieren
- ✅ Foreign Key Constraints werden enforced

### Metriken

```bash
# Connection-Test
python -c "from app.database import engine; print(engine.execute('SELECT 1').fetchone())"

# Sync-Performance messen
turso db show aquarius-db --json | jq '.size'

# Latenz testen
curl -w "@curl-format.txt" -o /dev/null -s https://aquarius-db.turso.io
```

### Offline-Test

1. Tablet mit Embedded Replica
2. Netzwerk trennen (Flugmodus)
3. Bewertungen erfassen
4. Netzwerk wieder aktivieren
5. Verifizieren: Daten auf Server synchronisiert

## Referenzen

- [Turso Documentation](https://docs.turso.tech/)
- [libSQL GitHub](https://github.com/libsql/libsql)
- [Embedded Replicas Guide](https://docs.turso.tech/features/embedded-replicas)
- [SQLAlchemy with libSQL](https://docs.turso.tech/sdk/python/guides/sqlalchemy)

## Historie

| Datum | Änderung | Autor |
|-------|----------|-------|
| 2025-12-18 | Initiale Version | Team |

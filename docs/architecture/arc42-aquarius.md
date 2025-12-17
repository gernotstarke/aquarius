# Aquarius - Architekturdokumentation
## Bewertungssystem für Kunstschwimmen-Wettkämpfe

**Version:** 1.0
**Datum:** 2025-12-17
**Template:** arc42 Version 8.2

---

## Über arc42

arc42, das Template zur Dokumentation von Software- und Systemarchitekturen.

Template Version 8.2 DE. (basiert auf AsciiDoc Version), Januar 2023

Created, maintained and © by Dr. Peter Hruschka, Dr. Gernot Starke and contributors. Siehe <https://arc42.org>.

---

# 1. Einführung und Ziele

## 1.1 Aufgabenstellung

Aquarius ist ein webbasiertes Bewertungssystem für regionale Kunstschwimmen-Wettkämpfe in der Kinderliga. Das System unterstützt den gesamten Wettkampfzyklus von der Saisonplanung über die Anmeldung bis zur Live-Bewertung und Ergebnisauswertung.

**Wesentliche Features:**
- Saisonplanung und Wettkampforganisation (Büro/Desktop)
- Anmeldungsverwaltung für Kinder und Teams
- Live-Bewertung durch Kampf- und Punktrichter (Schwimmbad/Mobile)
- Automatische Punkteberechnung nach Liga-Regeln
- Erstellung von Ranglisten und Preisvergabe nach Altersgruppen

**Fokus:** Figurenschwimmen (Synchronschwimmen nur erwähnt für Teamwertung)

## 1.2 Qualitätsziele

| Priorität | Qualitätsziel | Motivation |
|-----------|---------------|------------|
| 1 | **Benutzbarkeit** | Ehrenamtliche Helfer ohne IT-Affinität müssen System intuitiv bedienen können |
| 2 | **Verfügbarkeit** | Wettkampf darf nicht durch technische Probleme gestört werden (Offline-Fähigkeit) |
| 3 | **Korrektheit** | Bewertungsberechnung muss fehlerfrei nach Liga-Regeln erfolgen |
| 4 | **Performance** | Schnelle Reaktionszeiten bei Live-Bewertung unter Wettkampfbedingungen |
| 5 | **Wartbarkeit** | Figuren, Regeln und Altersgruppen ändern sich - System muss flexibel anpassbar sein |

## 1.3 Stakeholder

| Rolle | Erwartungshaltung |
|-------|-------------------|
| **Präsident** | Einfache Saisonplanung, Überblick über alle Wettkämpfe |
| **Verein** | Unkomplizierte Anmeldung von Kindern |
| **Offizieller** | Schnelle Wettkampfplanung, minimaler Administrationsaufwand |
| **Punktrichter** | Fokus auf Wettkampfablauf, System übernimmt Berechnungen |
| **Kampfrichter** | Einfache, schnelle Punkteeingabe (auch unter Stress) |
| **Kind** | Transparente Ergebnisse, faire Bewertung |

---

# 2. Randbedingungen

## 2.1 Technische Randbedingungen

| Randbedingung | Erläuterung |
|---------------|-------------|
| Web-Anwendung | Keine Installation, Zugriff über Browser |
| Mobile-First | Primär für Tablets im Schwimmbad optimiert |
| Progressive Web App | Installierbar, Offline-fähig, App-ähnliches Erlebnis |
| Cloud-Datenbank | Turso (libSQL) mit automatischer Synchronisation |
| Moderne Browser | Chrome, Firefox, Safari, Edge (jeweils aktuelle Versionen) |

## 2.2 Organisatorische Randbedingungen

| Randbedingung | Erläuterung |
|---------------|-------------|
| Zwei Betriebsmodi | **Planung** (Büro, Online) und **Durchführung** (Schwimmbad, Offline) |
| Zentral gehostet | Cloud-Hosting, keine lokale Serverinfrastruktur erforderlich |
| Ehrenamtliche Betreiber | Kein IT-Personal, einfache Wartung |
| Open Source | Transparenz, Anpassbarkeit, keine Lizenzkosten |

## 2.3 Konventionen

| Konvention | Erläuterung |
|------------|-------------|
| Fachsprache | Deutsche Domänenbegriffe im Code (Verein, Kind, Wettkampf) |
| REST API | Standardisierte HTTP-Methoden und Status-Codes |
| Responsive Design | Mobile-First mit TailwindCSS |
| Git Workflow | Feature-Branches, Pull Requests, Code Reviews |

---

# 3. Kontextabgrenzung

## 3.1 Fachlicher Kontext

```
┌─────────────────┐
│   Präsident     │────┐
└─────────────────┘    │
                       │
┌─────────────────┐    │    ┌──────────────────────┐
│  Schwimmverband │───────▶ │                      │
└─────────────────┘    │    │                      │
                       │    │      AQUARIUS        │
┌─────────────────┐    │    │   Bewertungssystem   │
│     Verein      │───────▶ │                      │
└─────────────────┘    │    │                      │
                       │    └──────────────────────┘
┌─────────────────┐    │              ▲
│      Kind       │────┘              │
└─────────────────┘                   │
                                      │
┌─────────────────┐                   │
│  Punktrichter   │───────────────────┘
└─────────────────┘

┌─────────────────┐
│  Kampfrichter   │───────────────────┘
└─────────────────┘
```

**Kommunikationsbeziehungen:**

| Partner | Eingabe | Ausgabe |
|---------|---------|---------|
| Präsident | Saisonplan, Wettkämpfe, Figurenkatalog | Auswertungen, Statistiken |
| Schwimmverband | Figurenkatalog-Updates, Regeländerungen | - |
| Verein | Kinderdaten, Teamzugehörigkeiten, Anmeldungen | Wettkampfbestätigungen |
| Kind | Wettkampfanmeldung, Figurenauswahl | Startnummer, Ergebnisse |
| Punktrichter | Stationszuweisung, Wettkampfstart | Berechnete Endpunkte, Ranglisten |
| Kampfrichter | Vorläufige Punktzahlen | Übersicht aller Bewertungen |

## 3.2 Technischer Kontext

```
┌────────────────────────────────────────────────────────┐
│                    Client (Browser)                     │
│  ┌──────────────────────┐  ┌──────────────────────┐   │
│  │  Planungs-Frontend   │  │ Durchführungs-       │   │
│  │  (Desktop-optimiert) │  │ Frontend (Mobile)    │   │
│  │  React + TypeScript  │  │ Touch-optimiert      │   │
│  └──────────┬───────────┘  └─────────┬────────────┘   │
│             │                         │                 │
│             │   Service Worker (PWA)  │                 │
│             │   Offline Cache         │                 │
└─────────────┼─────────────────────────┼─────────────────┘
              │                         │
              │    HTTPS / REST API     │
              │                         │
┌─────────────┴─────────────────────────┴─────────────────┐
│                Backend (FastAPI)                         │
│  ┌────────────┐  ┌────────────┐  ┌────────────────┐    │
│  │  Routers   │  │  Services  │  │  Repositories  │    │
│  │  (REST)    │─▶│ (Business) │─▶│  (Data Access) │    │
│  └────────────┘  └────────────┘  └────────┬───────┘    │
└───────────────────────────────────────────┼─────────────┘
                                            │
                                            │ SQL
                                            ▼
                              ┌──────────────────────────┐
                              │   Turso Database         │
                              │   (libSQL / SQLite)      │
                              │   + Cloud Sync           │
                              └──────────────────────────┘
```

**Technische Schnittstellen:**

| Schnittstelle | Technologie | Format |
|---------------|-------------|--------|
| Frontend ↔ Backend | REST API via HTTPS | JSON |
| Backend ↔ Datenbank | SQL (SQLAlchemy ORM) | libSQL/SQLite |
| Client ↔ Cache | Service Worker API | IndexedDB |
| Sync | Turso Cloud Sync | Proprietär |

---

# 4. Lösungsstrategie

## 4.1 Architekturansatz

**Progressive Web App (PWA)** mit klarer **Trennung von Planungs- und Durchführungskontext**

| Entscheidung | Begründung |
|--------------|------------|
| **Monorepo mit zwei Frontend-Modulen** | Gemeinsame Datenbasis, unterschiedliche UIs für Büro und Schwimmbad |
| **React SPA** | Moderne, komponentenbasierte UI, große Community, gute Mobile-Unterstützung |
| **FastAPI Backend** | Schnell, typsicher (Pydantic), automatische API-Dokumentation |
| **Turso (libSQL)** | SQLite-kompatibel, Cloud-Sync, hybride Online/Offline-Nutzung |
| **Service Worker** | Offline-Fähigkeit, App-ähnliches Erlebnis, schnelle Ladezeiten |

## 4.2 Technologie-Stack

### Frontend
- **React 18** + **TypeScript** - Typsicherheit, moderne Hooks
- **Vite** - Schneller Build, optimiertes Bundling
- **TailwindCSS** - Utility-First CSS, responsive Design
- **React Router** - Client-seitiges Routing
- **TanStack Query** - Server State Management, Caching
- **Zustand** - Lokales State Management
- **Workbox** - Service Worker für PWA

### Backend
- **Python 3.11+** - Moderne Sprache mit guter Lesbarkeit
- **FastAPI** - Async-fähig, automatische Validierung
- **Pydantic** - Datenvalidierung und Serialisierung
- **SQLAlchemy 2.0** - ORM mit Typsicherheit
- **Alembic** - Datenbank-Migrationen

### Datenbank & Infrastruktur
- **Turso (libSQL)** - Edge-Database mit Sync
- **SQLite** - Lokal für Entwicklung und Offline-Betrieb
- **Docker** - Containerisierung für Deployment
- **Nginx** - Reverse Proxy, Static File Serving

## 4.3 Zentrale Architekturentscheidungen

### AD-01: Trennung Planung vs. Durchführung

**Kontext:** Unterschiedliche Nutzungskontexte (Büro vs. Schwimmbad)

**Entscheidung:** Zwei separate Frontend-Module mit gemeinsamer Datenbasis

**Begründung:**
- Büro: Desktop-optimiert, komplexe Formulare, viele Daten
- Schwimmbad: Touch-optimiert, große Buttons, fokussierte Workflows
- Code-Sharing für gemeinsame Komponenten (Buttons, Forms)
- Unterschiedliche Routing-Strukturen
- Getrennte Service Worker Strategien

### AD-02: Progressive Web App statt Native App

**Kontext:** Mobile Nutzung im Schwimmbad erforderlich

**Entscheidung:** PWA mit Service Worker

**Begründung:**
- ✅ Kein App-Store-Prozess
- ✅ Plattform-unabhängig (iOS, Android, Desktop)
- ✅ Automatische Updates
- ✅ Offline-Fähigkeit über Service Worker
- ✅ Eine Codebasis für alle Geräte
- ❌ Einschränkungen: iOS-Safari hat begrenzte PWA-Features

### AD-03: Turso als Datenbank

**Kontext:** Hybride Online/Offline-Nutzung mit Synchronisation

**Entscheidung:** Turso (libSQL) mit Cloud-Sync

**Begründung:**
- ✅ SQLite-kompatibel (einfache Entwicklung)
- ✅ Edge-Replication für niedrige Latenz
- ✅ Automatische Synchronisation
- ✅ Embedded und Remote möglich
- ✅ Günstiger Betrieb
- ❌ Noch in Beta, kleinere Community als PostgreSQL

**Alternative:** PostgreSQL mit eigenem Sync-Mechanismus (mehr Aufwand)

### AD-04: Fachliche Modul-Struktur

**Kontext:** Wartbarkeit und klare fachliche Grenzen wichtig

**Entscheidung:** Domain-Driven Design mit fachlichen Modulen

**Bounded Contexts:**
1. **Stammdaten** - Vereine, Teams, Kinder, Offizielle
2. **Saisonplanung** - Saison, Figuren, Wettkämpfe
3. **Anmeldung** - Wettkampfanmeldungen, Startnummern
4. **Wettkampf** - Stationen, Durchgänge, Gruppen
5. **Bewertung** - Starts, Punkteerfassung, Berechnung
6. **Auswertung** - Ranglisten, Preise, Statistiken

**Begründung:**
- Klare fachliche Verantwortlichkeiten
- Module können unabhängig entwickelt werden
- Erleichtert Testing und Wartung
- Spiegelt Geschäftsprozesse wider

---

# 5. Bausteinsicht

> **Hinweis:** Dieses Kapitel wird nach technischer Abstimmung gemeinsam ausgearbeitet.

*Platzhalter für detaillierte Bausteinsicht mit Ebenen 1-3*

---

# 6. Laufzeitsicht

> **Hinweis:** Wird nach Bausteinsicht erstellt

---

# 7. Verteilungssicht

```
┌──────────────────────────────────────────────┐
│              Cloud-Infrastruktur              │
│                                               │
│  ┌─────────────────┐   ┌──────────────────┐  │
│  │  Web Server     │   │  Turso Cloud     │  │
│  │  (Docker)       │   │  Database        │  │
│  │  - Nginx        │   │  - Edge Nodes    │  │
│  │  - FastAPI      │──▶│  - Replication   │  │
│  └─────────────────┘   └──────────────────┘  │
│                                               │
└──────────────────────────────────────────────┘
            │                    │
            │  HTTPS            │  WSS (Sync)
            │                    │
┌───────────▼────────────────────▼───────────┐
│           Internet                          │
└───────────┬────────────────────┬───────────┘
            │                    │
    ┌───────▼────────┐   ┌───────▼────────┐
    │  Büro-PC       │   │  Tablet        │
    │  (Browser)     │   │  (Schwimmbad)  │
    │  - Planung     │   │  - Durchführung│
    │  - Online      │   │  - PWA         │
    │                │   │  - Offline     │
    └────────────────┘   └────────────────┘
```

**Deployment-Szenarien:**

| Komponente | Umgebung | Technologie |
|------------|----------|-------------|
| Backend API | Cloud (Docker Container) | FastAPI + Uvicorn |
| Static Frontend | CDN / Nginx | SPA (React) |
| Datenbank | Turso Cloud | libSQL mit Edge-Nodes |
| Büro (Planung) | Browser | Online-Zugriff |
| Schwimmbad (Durchführung) | PWA auf Tablet | Offline + Sync |

---

# 8. Querschnittliche Konzepte

## 8.1 Domänenmodell und Fachliche Architektur

### 8.1.1 Ubiquitous Language

Das System verwendet konsequent die Fachbegriffe der Domäne:

- **Verein**, **Team**, **Kind** (nicht: Club, Group, Child)
- **Wettkampf**, **Durchgang**, **Start** (nicht: Competition, Round, Attempt)
- **Kampfrichter**, **Punktrichter**, **Offizieller** (nicht: Judge, Referee, Official)
- **Figur**, **Schwierigkeitsfaktor** (nicht: Figure, Difficulty)

Diese Begriffe werden durchgängig verwendet: in der Datenbank, API, UI und Dokumentation.

### 8.1.2 Fachliche Module (Bounded Contexts)

```
┌─────────────────────────────────────────────────────────┐
│                     Aquarius System                      │
├─────────────────────────────────────────────────────────┤
│                                                          │
│  ┌────────────────┐    ┌────────────────┐              │
│  │  Stammdaten    │    │ Saisonplanung  │              │
│  │                │    │                │              │
│  │ • Verein       │    │ • Saison       │              │
│  │ • Team         │    │ • Figuren      │              │
│  │ • Kind         │    │ • Wettkämpfe   │              │
│  │ • Offizieller  │    │ • Schwimmbäder │              │
│  └────────────────┘    └────────────────┘              │
│                                                          │
│  ┌────────────────┐    ┌────────────────┐              │
│  │  Anmeldung     │    │  Wettkampf     │              │
│  │                │    │                │              │
│  │ • Registrierung│    │ • Stationen    │              │
│  │ • Startnummern │    │ • Gruppen      │              │
│  │ • Validierung  │    │ • Durchgänge   │              │
│  └────────────────┘    └────────────────┘              │
│                                                          │
│  ┌────────────────┐    ┌────────────────┐              │
│  │  Bewertung     │    │  Auswertung    │              │
│  │                │    │                │              │
│  │ • Punkteingabe │    │ • Ranglisten   │              │
│  │ • Berechnung   │    │ • Preisvergabe │              │
│  │ • Validierung  │    │ • Export       │              │
│  └────────────────┘    └────────────────┘              │
└─────────────────────────────────────────────────────────┘
```

**Abhängigkeiten zwischen Modulen:**
- Anmeldung → Stammdaten, Saisonplanung
- Wettkampf → Anmeldung, Stammdaten
- Bewertung → Wettkampf
- Auswertung → Bewertung, Wettkampf

**Regel:** Module dürfen nur über definierte Schnittstellen kommunizieren, keine direkten Datenbankzugriffe über Modulgrenzen.

## 8.2 Persistenz und Datenzugriff

### 8.2.1 Datenbank-Schema

**ORM:** SQLAlchemy 2.0 mit deklarativem Mapping

**Namenskonventionen:**
- Tabellen: Singular, Deutsch (z.B. `kind`, `wettkampf`)
- Fremdschlüssel: `{referenz}_id` (z.B. `team_id`)
- Junction-Tables: `{tabelle1}_{tabelle2}` (z.B. `kampfrichter_station`)

**Beispiel-Entität:**

```python
class Kind(Base):
    __tablename__ = "kind"

    id: Mapped[int] = mapped_column(primary_key=True)
    vorname: Mapped[str] = mapped_column(String(100))
    nachname: Mapped[str] = mapped_column(String(100))
    geburtsdatum: Mapped[date]
    adresse: Mapped[str] = mapped_column(Text)
    team_id: Mapped[int] = mapped_column(ForeignKey("team.id"))

    # Relationships
    team: Mapped["Team"] = relationship(back_populates="kinder")
    anmeldungen: Mapped[list["Anmeldung"]] = relationship(back_populates="kind")
```

### 8.2.2 Repository-Pattern

Jedes fachliche Modul hat ein Repository für Datenzugriff:

```python
class KindRepository:
    def __init__(self, session: Session):
        self.session = session

    def find_by_id(self, id: int) -> Optional[Kind]:
        return self.session.get(Kind, id)

    def find_by_verein(self, verein_id: int) -> list[Kind]:
        return self.session.query(Kind).join(Team).filter(
            Team.verein_id == verein_id
        ).all()

    def save(self, kind: Kind) -> Kind:
        self.session.add(kind)
        self.session.commit()
        self.session.refresh(kind)
        return kind
```

**Vorteile:**
- Trennung von Business-Logic und Datenzugriff
- Einfaches Mocking für Tests
- Zentrale Stelle für Query-Optimierung

### 8.2.3 Datenbank-Migrationen

**Tool:** Alembic

**Workflow:**
1. Model-Änderung in Python
2. `alembic revision --autogenerate -m "beschreibung"`
3. Review der generierten Migration
4. `alembic upgrade head`

**Versions-Schema:** `YYYY-MM-DD-HHMMSS_beschreibung.py`

## 8.3 Transaktionssteuerung

### 8.3.1 Transaktionsgrenzen

**Regel:** Eine Transaktion pro API-Request

```python
@app.post("/api/anmeldungen")
async def create_anmeldung(
    data: AnmeldungCreate,
    db: Session = Depends(get_db)
):
    try:
        # Gesamte Business-Logik in einer Transaktion
        service = AnmeldungService(db)
        result = service.create_anmeldung(data)
        db.commit()
        return result
    except BusinessError as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))
    except Exception:
        db.rollback()
        raise
```

### 8.3.2 Optimistic Locking

Für Entitäten mit möglichen Konflikten (z.B. Startnummern):

```python
class Anmeldung(Base):
    __tablename__ = "anmeldung"

    id: Mapped[int] = mapped_column(primary_key=True)
    version: Mapped[int] = mapped_column(default=0)  # Optimistic Lock
    startnummer: Mapped[Optional[int]]

    __mapper_args__ = {"version_id_col": version}
```

Bei Konflikten: `StaleDataError` → HTTP 409 Conflict

## 8.4 Fehlerbehandlung

### 8.4.1 Fehler-Hierarchie

```python
class AquariusError(Exception):
    """Basis für alle fachlichen Fehler"""
    pass

class ValidationError(AquariusError):
    """Validierungsfehler (400 Bad Request)"""
    pass

class NotFoundError(AquariusError):
    """Ressource nicht gefunden (404 Not Found)"""
    pass

class ConflictError(AquariusError):
    """Geschäftsregel-Konflikt (409 Conflict)"""
    pass

class WettkampfVollError(ConflictError):
    """Wettkampf ist voll"""
    pass

class DoppelmeldungError(ConflictError):
    """Kind bereits angemeldet"""
    pass
```

### 8.4.2 Global Exception Handler

```python
@app.exception_handler(ValidationError)
async def validation_error_handler(request, exc):
    return JSONResponse(
        status_code=400,
        content={
            "error": "validation_error",
            "message": str(exc)
        }
    )
```

### 8.4.3 Frontend-Fehlerbehandlung

```typescript
// Zentrale Error Boundary für React
class ErrorBoundary extends React.Component {
  // Fängt Rendering-Fehler
}

// API-Fehler via TanStack Query
const { error, isError } = useQuery({
  queryKey: ['kinder'],
  queryFn: fetchKinder,
  onError: (error) => {
    if (error.status === 401) {
      // Redirect to login
    } else if (error.status >= 500) {
      toast.error('Serverfehler - bitte später erneut versuchen')
    }
  }
})
```

## 8.5 Validierung

### 8.5.1 Multi-Layer Validierung

**1. Frontend-Validierung (UX):**
```typescript
// Zod für TypeScript-Schema-Validierung
const KindSchema = z.object({
  vorname: z.string().min(2, "Mindestens 2 Zeichen"),
  nachname: z.string().min(2),
  geburtsdatum: z.date().max(new Date(), "Darf nicht in Zukunft liegen"),
  adresse: z.string().min(10)
})
```

**2. Backend-Validierung (Security):**
```python
# Pydantic für Request-Validierung
class KindCreate(BaseModel):
    vorname: str = Field(min_length=2, max_length=100)
    nachname: str = Field(min_length=2, max_length=100)
    geburtsdatum: date
    adresse: str = Field(min_length=10)

    @validator('geburtsdatum')
    def nicht_in_zukunft(cls, v):
        if v > date.today():
            raise ValueError('Geburtsdatum darf nicht in Zukunft liegen')
        return v
```

**3. Datenbank-Constraints:**
```sql
CREATE TABLE kind (
    id INTEGER PRIMARY KEY,
    vorname TEXT NOT NULL CHECK(length(vorname) >= 2),
    nachname TEXT NOT NULL CHECK(length(nachname) >= 2),
    geburtsdatum DATE NOT NULL CHECK(geburtsdatum <= CURRENT_DATE)
);
```

### 8.5.2 Business-Rule-Validierung

Komplexe Geschäftsregeln in Service-Schicht:

```python
class AnmeldungService:
    def validate_anmeldung(self, kind_id: int, wettkampf_id: int):
        # Regel: Kind muss startberechtigt sein
        kind = self.kind_repo.find_by_id(kind_id)
        if not kind.ist_startberechtigt:
            raise ValidationError("Kind ist nicht startberechtigt")

        # Regel: Keine Doppelmeldung
        existing = self.anmeldung_repo.find_by_kind_und_wettkampf(
            kind_id, wettkampf_id
        )
        if existing:
            raise DoppelmeldungError("Kind bereits angemeldet")

        # Regel: Wettkampf nicht voll
        wettkampf = self.wettkampf_repo.find_by_id(wettkampf_id)
        if wettkampf.ist_voll():
            raise WettkampfVollError("Wettkampf ist ausgebucht")
```

## 8.6 Sicherheit

### 8.6.1 Authentifizierung

**Strategie:** JWT (JSON Web Tokens)

```python
from fastapi.security import HTTPBearer
from jose import jwt

security = HTTPBearer()

def get_current_user(token: str = Depends(security)):
    payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
    return payload["sub"]
```

**Rollen:**
- `admin` - Präsident, volle Rechte
- `official` - Offizieller, Wettkampfplanung
- `judge` - Kampf-/Punktrichter, nur Bewertung
- `club` - Verein, eigene Kinder verwalten

### 8.6.2 Autorisierung

```python
def require_role(required_role: str):
    def decorator(func):
        async def wrapper(*args, current_user = Depends(get_current_user), **kwargs):
            if current_user.role != required_role:
                raise HTTPException(403, "Keine Berechtigung")
            return await func(*args, **kwargs)
        return wrapper
    return decorator

@app.post("/api/saison")
@require_role("admin")
async def create_saison(data: SaisonCreate):
    # Nur für Admins
    pass
```

### 8.6.3 HTTPS & CORS

**Produktion:** Nur HTTPS, TLS 1.3

**CORS-Konfiguration:**
```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://aquarius.example.com"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)
```

### 8.6.4 Input Sanitization

- SQL Injection: Verhindert durch ORM (SQLAlchemy)
- XSS: React escaped automatisch, keine `dangerouslySetInnerHTML`
- CSRF: Token-basierte API, keine Cookie-Session

## 8.7 Logging und Monitoring

### 8.7.1 Strukturiertes Logging

```python
import structlog

logger = structlog.get_logger()

@app.post("/api/anmeldungen")
async def create_anmeldung(data: AnmeldungCreate):
    logger.info(
        "anmeldung.create.start",
        kind_id=data.kind_id,
        wettkampf_id=data.wettkampf_id
    )
    # ...
    logger.info(
        "anmeldung.create.success",
        anmeldung_id=result.id,
        startnummer=result.startnummer
    )
```

**Log-Levels:**
- DEBUG: Entwicklung
- INFO: Business Events (Anmeldung erstellt, Bewertung gespeichert)
- WARNING: Geschäftsregel-Verletzungen
- ERROR: Technische Fehler
- CRITICAL: System-Ausfall

### 8.7.2 Metriken

**Key Performance Indicators:**
- API Response Time (p50, p95, p99)
- Database Query Time
- Fehlerrate (4xx, 5xx)
- Aktive Wettkämpfe
- Bewertungen pro Minute

**Tool:** Prometheus + Grafana (optional in Phase 2)

### 8.7.3 Error Tracking

**Frontend:** Sentry für JavaScript-Fehler
**Backend:** Sentry für Python-Exceptions

```python
import sentry_sdk

sentry_sdk.init(
    dsn="...",
    environment="production",
    traces_sample_rate=0.1
)
```

## 8.8 Offline-Synchronisation

### 8.8.1 Sync-Strategie

**Turso Native Sync:**
- Embedded Replica auf Tablet
- Automatische Replikation bei Netzwerk
- Conflict-Free Replicated Data Type (CRDT) für Konfliktauflösung

**Sync-Richtungen:**
- **Download (Cloud → Tablet):** Wettkampfdaten, Anmeldungen, Figuren
- **Upload (Tablet → Cloud):** Bewertungen, Ergebnisse

### 8.8.2 Konfliktauflösung

**Last-Write-Wins für Bewertungen:**
- Jede Bewertung hat Timestamp
- Bei Konflikt: Neueste Bewertung gewinnt
- Rationale: Korrektur überschreibt Fehler

**Startnummern-Konflikte:**
- Zentrale Vergabe nur online
- Offline: Temporäre Nummern (negativ)
- Beim Sync: Permanent-Nummern zuweisen

### 8.8.3 Offline-Detection

```typescript
// Frontend: Network Status
const isOnline = useNetworkStatus()

if (isOnline) {
  // Trigger Sync
  syncService.sync()
}

// Service Worker: Background Sync
self.addEventListener('sync', (event) => {
  if (event.tag === 'sync-bewertungen') {
    event.waitUntil(syncBewertungen())
  }
})
```

## 8.9 User Experience (UX)

### 8.9.1 Responsive Design

**Breakpoints (TailwindCSS):**
- `sm`: 640px (Phones)
- `md`: 768px (Tablets)
- `lg`: 1024px (Desktop)
- `xl`: 1280px (Large Desktop)

**Ansatz:** Mobile-First

```tsx
// Beispiel: Button-Größe responsive
<button className="
  text-sm py-2 px-4      /* Mobile */
  md:text-base md:py-3 md:px-6  /* Tablet */
  lg:text-lg lg:py-4 lg:px-8    /* Desktop */
">
  Anmelden
</button>
```

### 8.9.2 Touch-Optimierung (Durchführungs-UI)

**Richtlinien:**
- Mindestgröße: 44×44px (Apple HIG)
- Abstand zwischen Touch-Targets: min. 8px
- Große Schrift: min. 16px (kein Browser-Zoom)
- Horizontales Scrollen vermeiden
- Gesten: Swipe für Navigation

**Komponenten:**
```tsx
// Punkteingabe: Große Buttons 1-10
<div className="grid grid-cols-5 gap-4">
  {[1,2,3,4,5,6,7,8,9,10].map(punkt => (
    <button
      key={punkt}
      className="h-20 w-20 text-3xl font-bold rounded-lg"
      onClick={() => handlePunkt(punkt)}
    >
      {punkt}
    </button>
  ))}
</div>
```

### 8.9.3 Loading & Feedback

**Sofortiges Feedback:**
- Button-States: default, hover, active, loading, disabled
- Optimistic Updates: UI sofort aktualisieren, bei Fehler zurückrollen
- Skeleton Screens für Ladezeiten

```tsx
const { mutate, isPending } = useMutation({
  mutationFn: saveAnmeldung,
  onMutate: async (newAnmeldung) => {
    // Optimistic Update
    queryClient.setQueryData(['anmeldungen'], (old) =>
      [...old, newAnmeldung]
    )
  },
  onError: (error, newAnmeldung, context) => {
    // Rollback
    queryClient.setQueryData(['anmeldungen'], context.previousData)
    toast.error('Fehler beim Speichern')
  }
})

<button disabled={isPending}>
  {isPending ? <Spinner /> : 'Anmelden'}
</button>
```

### 8.9.4 Barrierefreiheit (A11y)

**Ziel:** WCAG 2.1 Level AA

- **Semantisches HTML:** `<button>`, `<nav>`, `<main>`, `<form>`
- **Keyboard-Navigation:** Tab-Order, Focus-Styles, Shortcuts
- **Screen-Reader:** ARIA-Labels, alt-Texte
- **Kontraste:** Min. 4.5:1 für Text, 3:1 für UI
- **Fehler:** Visuell + auditiv (Screen Reader)

```tsx
<button
  aria-label="Anmeldung für Max Mustermann löschen"
  aria-describedby="delete-warning"
>
  <TrashIcon aria-hidden="true" />
</button>
<span id="delete-warning" className="sr-only">
  Diese Aktion kann nicht rückgängig gemacht werden
</span>
```

## 8.10 Performance

### 8.10.1 Frontend-Optimierung

**Code Splitting:**
```typescript
// Lazy Loading für Routes
const PlanungApp = lazy(() => import('./planungs-app'))
const DurchfuehrungApp = lazy(() => import('./durchfuehrungs-app'))

<Suspense fallback={<LoadingScreen />}>
  <Routes>
    <Route path="/planung/*" element={<PlanungApp />} />
    <Route path="/wettkampf/*" element={<DurchfuehrungApp />} />
  </Routes>
</Suspense>
```

**Virtualisierung für lange Listen:**
```typescript
import { useVirtualizer } from '@tanstack/react-virtual'

// Nur sichtbare Zeilen rendern
const virtualizer = useVirtualizer({
  count: kinder.length,
  getScrollElement: () => parentRef.current,
  estimateSize: () => 50
})
```

**Memoization:**
```typescript
const sortierteKinder = useMemo(() =>
  kinder.sort((a, b) => a.nachname.localeCompare(b.nachname)),
  [kinder]
)
```

### 8.10.2 Backend-Optimierung

**Eager Loading:**
```python
# N+1 Problem vermeiden
kinder = session.query(Kind).options(
    joinedload(Kind.team).joinedload(Team.verein)
).all()
```

**Pagination:**
```python
@app.get("/api/kinder")
async def list_kinder(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    total = db.query(func.count(Kind.id)).scalar()
    kinder = db.query(Kind).offset(skip).limit(limit).all()
    return {
        "items": kinder,
        "total": total,
        "skip": skip,
        "limit": limit
    }
```

**Caching:**
```python
from functools import lru_cache

@lru_cache(maxsize=128)
def get_figur_catalog(saison_id: int):
    # Figuren ändern sich selten, Cache 1h
    return db.query(Figur).filter_by(saison_id=saison_id).all()
```

### 8.10.3 Datenbank-Optimierung

**Indizes:**
```sql
-- Häufige Queries optimieren
CREATE INDEX idx_kind_team ON kind(team_id);
CREATE INDEX idx_anmeldung_wettkampf ON anmeldung(wettkampf_id);
CREATE INDEX idx_start_durchgang_kind ON start(durchgang_id, kind_id);
CREATE INDEX idx_bewertung_start ON bewertung(start_id);
```

**Query-Analyse:**
```python
# SQLAlchemy Echo für Query-Logging
engine = create_engine(url, echo=True)

# EXPLAIN für langsame Queries
result = db.execute(text("EXPLAIN QUERY PLAN SELECT ..."))
```

## 8.11 Testbarkeit

### 8.11.1 Test-Pyramide

```
        ┌─────────────┐
        │   E2E Tests │  (5% - Playwright)
        └─────────────┘
       ┌───────────────┐
       │ Integration   │   (15% - API Tests)
       │    Tests      │
       └───────────────┘
      ┌─────────────────┐
      │   Unit Tests    │    (80% - Jest, Pytest)
      └─────────────────┘
```

### 8.11.2 Backend-Testing

**Unit Tests (Pytest):**
```python
def test_bewertung_berechnung():
    bewertungen = [7.5, 8.0, 7.0, 8.5, 7.5]  # 5 Kampfrichter
    schwierigkeitsfaktor = 2.3

    service = BewertungService()
    endpunkte = service.berechne_endpunkte(bewertungen, schwierigkeitsfaktor)

    # Höchste (8.5) und niedrigste (7.0) streichen
    # Durchschnitt: (7.5 + 8.0 + 7.5) / 3 = 7.67
    # Endpunkte: 7.67 * 2.3 = 17.64
    assert endpunkte == pytest.approx(17.64, 0.01)
```

**Integration Tests:**
```python
def test_anmeldung_api(client: TestClient):
    response = client.post("/api/anmeldungen", json={
        "kind_id": 1,
        "wettkampf_id": 1,
        "figuren": [1, 2, 3]
    })
    assert response.status_code == 201
    data = response.json()
    assert "startnummer" in data
```

### 8.11.3 Frontend-Testing

**Component Tests (Vitest + Testing Library):**
```typescript
test('Punkteingabe Button gibt Feedback', async () => {
  const onPunkt = vi.fn()
  render(<PunkteingabeButtons onPunkt={onPunkt} />)

  const button = screen.getByRole('button', { name: '8' })
  await userEvent.click(button)

  expect(onPunkt).toHaveBeenCalledWith(8)
  expect(button).toHaveClass('bg-green-500')  // Visuelles Feedback
})
```

**E2E Tests (Playwright):**
```typescript
test('Kompletter Anmeldeprozess', async ({ page }) => {
  await page.goto('/planung/anmeldungen')
  await page.click('text=Neue Anmeldung')
  await page.fill('[name=kind]', 'Max Mustermann')
  await page.selectOption('[name=wettkampf]', '1')
  await page.click('text=Figur A wählen')
  await page.click('text=Anmelden')

  await expect(page.locator('text=Startnummer')).toBeVisible()
})
```

### 8.11.4 Test-Daten

**Factory Pattern:**
```python
class KindFactory:
    @staticmethod
    def create(
        vorname="Max",
        nachname="Mustermann",
        geburtsdatum=date(2015, 5, 10),
        **kwargs
    ):
        return Kind(
            vorname=vorname,
            nachname=nachname,
            geburtsdatum=geburtsdatum,
            **kwargs
        )

def test_altersgruppe():
    kind = KindFactory.create(geburtsdatum=date(2015, 1, 1))
    assert kind.altersgruppe == "10-12"
```

## 8.12 Deployment und Betrieb

### 8.12.1 Containerisierung

**Dockerfile (Backend):**
```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

**docker-compose.yml (Lokal):**
```yaml
version: '3.8'
services:
  backend:
    build: ./backend
    ports:
      - "8000:8000"
    environment:
      - TURSO_DATABASE_URL=file:./dev.db
    volumes:
      - ./backend:/app

  frontend:
    build: ./frontend
    ports:
      - "5173:5173"
    volumes:
      - ./frontend:/app
```

### 8.12.2 CI/CD Pipeline

**GitHub Actions:**
```yaml
name: CI/CD

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-python@v4
      - run: pip install -r requirements.txt
      - run: pytest
      - run: npm test

  deploy:
    needs: test
    if: github.ref == 'refs/heads/main'
    runs-on: ubuntu-latest
    steps:
      - name: Deploy to Production
        run: |
          docker build -t aquarius .
          docker push registry.example.com/aquarius
```

### 8.12.3 Monitoring

**Health Checks:**
```python
@app.get("/health")
async def health_check(db: Session = Depends(get_db)):
    # Datenbank-Check
    try:
        db.execute(text("SELECT 1"))
        db_status = "healthy"
    except Exception:
        db_status = "unhealthy"

    return {
        "status": "healthy" if db_status == "healthy" else "degraded",
        "database": db_status,
        "version": "1.0.0"
    }
```

### 8.12.4 Backup & Recovery

**Strategie:**
- **Daily Backup:** Automatisch via Turso
- **On-Demand:** Manueller Export vor Wettkampf
- **Recovery Time Objective (RTO):** < 1 Stunde
- **Recovery Point Objective (RPO):** < 5 Minuten

```python
# Export-Funktion für Backup
@app.get("/api/admin/backup")
async def create_backup():
    timestamp = datetime.now().isoformat()
    filename = f"aquarius-backup-{timestamp}.db"
    # Turso: .dump command
    return FileResponse(filename)
```

---

# 9. Architekturentscheidungen

Siehe Kapitel 4.3 für wichtige Architecture Decision Records (ADRs)

**Weitere ADRs:**
- ADR-05: TypeScript statt JavaScript (Typsicherheit)
- ADR-06: TailwindCSS statt CSS-in-JS (Performance, Utility-First)
- ADR-07: TanStack Query statt Redux (Server State vs. Client State)
- ADR-08: Monorepo mit gemeinsamen Packages (Code-Sharing)

---

# 10. Qualitätsanforderungen

Siehe Kapitel 1.2 und Requirements-Dokument Kapitel 6

---

# 11. Risiken und technische Schulden

| ID | Risiko | Mitigation |
|----|--------|------------|
| RISK-01 | Turso noch in Beta | Fallback auf lokales SQLite + manuelles Sync vorbereiten |
| RISK-02 | iOS PWA-Einschränkungen | Native App als Plan B, zunächst Android/Desktop priorisieren |
| RISK-03 | Komplexität Offline-Sync | Schrittweise Einführung: erst Online, dann Offline-Modus |
| TD-01 | Fehlende Authentifizierung | MVP ohne Auth, später nachrüsten |
| TD-02 | Keine Internationalisierung | Zunächst nur Deutsch, i18n-Struktur vorbereiten |

---

# 12. Glossar

Siehe Requirements-Dokument Kapitel 4.1

---

**Autoren:** Claude (AI), Gernot Starke
**Review:** [TBD]
**Nächste Review:** [Nach Bausteinsicht-Diskussion]

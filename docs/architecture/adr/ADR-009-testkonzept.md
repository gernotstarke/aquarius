# ADR-009: Testkonzept mit realer Datenbank

**Status:** Accepted
**Datum:** 2025-12-17
**Kontext:** Implementierung Aquarius Bewertungssystem
**Entscheider:** Architekt, Product Owner

---

## Kontext und Problem

Das Aquarius-System hat ein **komplexes Domänenmodell** mit vielen Entitäten und Beziehungen:

- **Hierarchien:** Kind → Team → Verein, Bewertung → Start → Durchgang → Figur
- **Geschäftsregeln mit DB-Abhängigkeit:**
  - Startnummernvergabe (Unique pro Wettkampf, lückenlos)
  - Doppelmeldungs-Prüfung (Kind + Wettkampf)
  - Bewertungsberechnung (Aggregation über mehrere Kampfrichter)
- **SQLAlchemy ORM:** Relationships, Eager Loading, Constraints, Cascade-Deletes
- **Fachliche Integrität:** Foreign Keys, Check Constraints müssen funktionieren

**Problem:**
Wie testen wir **realistische Szenarien** mit vollständiger Datenbankstruktur, ohne die Tests langsam oder fragil zu machen?

**Herausforderungen:**
1. ORM-Logik (Relationships, Lazy Loading) muss getestet werden
2. Datenbank-Constraints (Unique, Foreign Key) müssen enforced werden
3. Geschäftsregeln sind oft datenbank-abhängig
4. Tests müssen schnell und isoliert sein
5. Testdaten müssen realistisch, aber reproduzierbar sein

---

## Entscheidung

### 1. Test-Strategie (3-Ebenen-Pyramide)

```
         ┌─────────────┐
         │  E2E Tests  │  5% - Vollständige API-Tests (Playwright)
         └─────────────┘
       ┌─────────────────┐
       │  Integration    │  25% - Mit echter DB (Repository + Service)
       │     Tests       │
       └─────────────────┘
      ┌───────────────────┐
      │   Unit Tests      │  70% - Ohne DB (Geschäftslogik, Calculator)
      └───────────────────┘
```

**Fokus:** Integration-Tests mit echter Datenbank für kritische Workflows

### 2. Datenbank für Tests: SQLite In-Memory

**Entscheidung:** SQLite In-Memory für alle Integration-Tests

**Begründung:**
- ✅ **Schnell:** Keine Disk I/O, Tests laufen im RAM
- ✅ **Isoliert:** Jeder Test bekommt neue DB
- ✅ **Produktionsnah:** Turso = libSQL = SQLite-kompatibel
- ✅ **Einfach:** Kein Docker, keine externe Infrastruktur
- ✅ **CI-freundlich:** Funktioniert überall (GitHub Actions, lokal)

**Konfiguration:**
```python
# tests/conftest.py
SQLALCHEMY_TEST_DATABASE_URL = "sqlite:///:memory:"
```

### 3. Test-Datenbank-Setup pro Test

**Lifecycle:**
```
Für jeden Test:
1. Neue SQLite In-Memory DB erstellen
2. Alembic Migrations ausführen → Schema aufbauen
3. Basis-Fixtures laden (optional)
4. Test ausführen
5. DB verwerfen (automatisch durch In-Memory)
```

**Vorteile:**
- ✅ Vollständige Isolation zwischen Tests
- ✅ Schema immer aktuell (via Migrations)
- ✅ Kein Cleanup nötig

### 4. Fixtures & Factories

#### 4.1 Factory Pattern für Testdaten

**Entscheidung:** Eigene Factory-Klassen (KEIN pytest-factoryboy)

**Begründung:**
- Volle Kontrolle über Objekt-Erzeugung
- Einfacher zu verstehen für Team
- Explizite Abhängigkeiten (Team → Verein)

**Beispiel:**
```python
class KindFactory:
    def __init__(self, db_session: Session):
        self.db = db_session
        self._counter = 0
        self.faker = Faker('de_DE')

    def create(self, team: Team, **overrides) -> Kind:
        self._counter += 1
        kind = Kind(
            vorname=self.faker.first_name(),
            nachname=self.faker.last_name(),
            geburtsdatum=self.faker.date_of_birth(minimum_age=8, maximum_age=14),
            adresse=f"{self.faker.street_address()}, {self.faker.city()}",
            team=team,
            ist_startberechtigt=True,
            **overrides
        )
        self.db.add(kind)
        self.db.commit()
        self.db.refresh(kind)
        return kind
```

#### 4.2 Szenario-Fixture: "kleine_liga"

**Beschreibung:** Realistische Basis-Liga für Tests

**Umfang:**
- 2 Vereine ("SC Neptun", "Wasserfreunde")
- 4-5 Teams (je 2 pro Verein + ggf. Jugend/Kids)
- **~20 Kinder** mit Faker-generierten Namen + Adressen
- 1 Saison mit 5-8 Standard-Figuren
- 5 Offizielle (3 Kampfrichter, 2 Punktrichter)

**Verwendung:**
```python
def test_anmeldung_workflow(kleine_liga, wettkampf):
    # kleine_liga['kinder'] = Liste mit 20 Kindern
    # kleine_liga['vereine'] = [neptun, wasserfreunde]
    kind = kleine_liga['kinder'][0]
    # ...
```

#### 4.3 Faker für realistische Daten

**Entscheidung:** Faker-Library mit deutschem Locale

```python
from faker import Faker
fake = Faker('de_DE')

# Beispiel-Output:
# vorname: "Anna", "Lukas", "Sophie"
# nachname: "Müller", "Schmidt", "Weber"
# adresse: "Hauptstraße 42, 12345 Berlin"
# geburtsdatum: 2014-03-15
```

**Vorteile:**
- ✅ Realistische deutsche Namen
- ✅ Gültige Adressen (Stadt, PLZ)
- ✅ Deterministische Seeds möglich (Reproduzierbarkeit)

### 5. Transactional Tests mit Rollback

**Problem:** Tests dürfen sich nicht gegenseitig beeinflussen

**Lösung:** Nested Transactions mit Savepoints

```python
@pytest.fixture
def db_session(db_engine):
    """Session mit automatischem Rollback nach Test"""
    connection = db_engine.connect()
    transaction = connection.begin()
    session = Session(bind=connection)

    # Nested Transaction für Test
    nested = connection.begin_nested()

    yield session

    # Rollback nach Test
    session.close()
    transaction.rollback()
    connection.close()
```

**Vorteil:** Fixtures (z.B. `kleine_liga`) können in äußerer Transaktion erstellt werden, Test-Änderungen werden zurückgerollt

### 6. Test-Kategorien

#### 6.1 Unit-Tests (70%) - OHNE Datenbank

**Ziel:** Geschäftslogik isoliert testen

**Beispiele:**
- Bewertungsberechnung (höchste/niedrigste streichen)
- Altersgruppen-Bestimmung
- Validierungslogik (z.B. Datum in Vergangenheit)
- Utility-Funktionen

```python
def test_endpunkte_berechnung():
    bewertungen = [7.5, 8.0, 7.0, 8.5, 7.5]
    schwierigkeitsfaktor = Decimal('2.3')

    result = berechne_endpunkte(bewertungen, schwierigkeitsfaktor)

    # Gestrichen: 8.5 (max), 7.0 (min)
    # Durchschnitt: (7.5 + 8.0 + 7.5) / 3 = 7.67
    # Endpunkte: 7.67 × 2.3 = 17.64
    assert result == Decimal('17.64')
```

#### 6.2 Repository-Tests (Integration)

**Ziel:** Datenbankzugriff und ORM testen

**Beispiele:**
- CRUD-Operationen
- Queries mit Filtern und Joins
- Eager Loading (N+1-Problem vermeiden)
- Constraints (Unique, Foreign Key)

```python
def test_anmeldung_repository_doppelmeldung(db_session, kleine_liga, wettkampf):
    repo = AnmeldungRepository(db_session)
    kind = kleine_liga['kinder'][0]

    # Erste Anmeldung
    anmeldung1 = Anmeldung(kind=kind, wettkampf=wettkampf, startnummer=1)
    repo.save(anmeldung1)

    # Prüfe Doppelmeldung
    existing = repo.find_by_kind_und_wettkampf(kind.id, wettkampf.id)

    assert existing is not None
    assert existing.id == anmeldung1.id
```

#### 6.3 Service-Tests (Integration mit DB)

**Ziel:** Geschäftslogik MIT Datenbankzugriff

**Beispiele:**
- Anmeldungs-Workflow (Validierung + Startnummernvergabe)
- Bewertungs-Workflow (Punkteingabe + Berechnung)
- Business-Rule-Validierung (Doppelmeldung, Wettkampf voll)

```python
def test_anmeldung_service_vergibt_startnummern_lueckenlos(
    db_session,
    kleine_liga,
    wettkampf
):
    service = AnmeldungService(
        anmeldung_repo=AnmeldungRepository(db_session),
        kind_service=KindService(...),
        wettkampf_service=WettkampfService(...)
    )

    # Alle 20 Kinder anmelden
    anmeldungen = []
    for kind in kleine_liga['kinder']:
        anmeldung = service.create_anmeldung(
            AnmeldungCreate(
                kind_id=kind.id,
                wettkampf_id=wettkampf.id,
                figuren=[1, 2, 3]
            )
        )
        anmeldungen.append(anmeldung)

    # Assert: Startnummern 1-20, lückenlos, eindeutig
    startnummern = sorted([a.startnummer for a in anmeldungen])
    assert startnummern == list(range(1, 21))
```

#### 6.4 Model-Tests (Integration)

**Ziel:** ORM-Relationships und Computed Properties

```python
def test_kind_altersgruppe_property(db_session):
    team = Team(name="Test-Team", verein=Verein(name="Test-Verein"))
    kind = Kind(
        vorname="Test",
        nachname="Kind",
        geburtsdatum=date(2014, 5, 10),  # 11 Jahre alt
        team=team
    )
    db_session.add(kind)
    db_session.commit()

    # Property berechnet Altersgruppe
    assert kind.altersgruppe == "10-12"

def test_wettkampf_cascade_delete(db_session, wettkampf):
    # Anmeldungen erstellen
    anmeldung = Anmeldung(wettkampf=wettkampf, ...)
    db_session.add(anmeldung)
    db_session.commit()

    anmeldung_id = anmeldung.id

    # Wettkampf löschen
    db_session.delete(wettkampf)
    db_session.commit()

    # Anmeldung sollte auch gelöscht sein (Cascade)
    assert db_session.get(Anmeldung, anmeldung_id) is None
```

---

## Implementierung

### Verzeichnisstruktur

```
tests/
├── conftest.py                    # Shared fixtures (db_engine, db_session)
├── factories/
│   ├── __init__.py
│   ├── verein_factory.py
│   ├── team_factory.py
│   ├── kind_factory.py
│   ├── wettkampf_factory.py
│   └── figur_factory.py
├── fixtures/
│   ├── __init__.py
│   └── kleine_liga.py             # Szenario-Fixture
├── unit/                          # Keine DB
│   ├── test_bewertung_calculator.py
│   ├── test_altersgruppen.py
│   └── test_validations.py
├── integration/                   # Mit DB
│   ├── repositories/
│   │   ├── test_kind_repository.py
│   │   ├── test_anmeldung_repository.py
│   │   └── test_bewertung_repository.py
│   ├── services/
│   │   ├── test_anmeldung_service.py
│   │   ├── test_bewertung_service.py
│   │   └── test_wettkampf_service.py
│   ├── models/
│   │   ├── test_kind_model.py
│   │   └── test_relationships.py
│   └── workflows/
│       ├── test_anmeldung_workflow.py
│       └── test_bewertung_workflow.py
└── e2e/                           # API-Tests (später)
    └── test_anmeldung_api.py
```

### Pytest-Konfiguration

**pyproject.toml:**
```toml
[tool.pytest.ini_options]
testpaths = ["tests"]
python_files = ["test_*.py"]
python_classes = ["Test*"]
python_functions = ["test_*"]

# Marker
markers = [
    "unit: Unit tests without database",
    "integration: Integration tests with database",
    "slow: Slow tests (e.g., with migrations)",
    "e2e: End-to-end tests"
]

# Coverage
addopts = [
    "--cov=app",
    "--cov-report=html",
    "--cov-report=term-missing",
    "-v"
]
```

**Ausführung:**
```bash
# Nur Unit-Tests (schnell)
pytest -m unit

# Nur Integration-Tests
pytest -m integration

# Alles außer E2E
pytest -m "not e2e"

# Mit Coverage
pytest --cov=app --cov-report=html
```

### Basis-Fixtures (conftest.py)

```python
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from app.database import Base
from app.main import app

@pytest.fixture(scope="session")
def db_engine():
    """SQLite In-Memory Engine für alle Tests"""
    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
        echo=False  # True für Debugging
    )

    # Schema erstellen (via Alembic in Produktion, hier direkt)
    Base.metadata.create_all(bind=engine)

    yield engine

    engine.dispose()

@pytest.fixture
def db_session(db_engine):
    """DB-Session mit automatischem Rollback nach Test"""
    connection = db_engine.connect()
    transaction = connection.begin()
    session = Session(bind=connection)

    yield session

    session.close()
    transaction.rollback()
    connection.close()

@pytest.fixture
def factories(db_session):
    """Alle Factories als Bundle"""
    from tests.factories import (
        VereinFactory, TeamFactory, KindFactory,
        WettkampfFactory, FigurFactory
    )

    return {
        'verein': VereinFactory(db_session),
        'team': TeamFactory(db_session),
        'kind': KindFactory(db_session),
        'wettkampf': WettkampfFactory(db_session),
        'figur': FigurFactory(db_session)
    }
```

### Factory-Implementierung

**tests/factories/kind_factory.py:**
```python
from faker import Faker
from datetime import date, timedelta
from app.models import Kind

class KindFactory:
    """Factory für realistische Kind-Testdaten"""

    def __init__(self, db_session, seed=42):
        self.db = db_session
        self.faker = Faker('de_DE')
        self.faker.seed_instance(seed)  # Reproduzierbarkeit
        self._counter = 0

    def create(self, team, **overrides):
        """Erstellt ein Kind mit Faker-Daten"""
        self._counter += 1

        # Alter: 8-14 Jahre
        today = date.today()
        age_years = 8 + (self._counter % 7)  # Verteilt über Altersgruppen
        geburtsdatum = today - timedelta(days=365 * age_years)

        defaults = {
            'vorname': self.faker.first_name(),
            'nachname': self.faker.last_name(),
            'geburtsdatum': geburtsdatum,
            'adresse': f"{self.faker.street_address()}, {self.faker.postcode()} {self.faker.city()}",
            'team': team,
            'ist_startberechtigt': True
        }
        defaults.update(overrides)

        kind = Kind(**defaults)
        self.db.add(kind)
        self.db.commit()
        self.db.refresh(kind)

        return kind

    def create_batch(self, team, count: int):
        """Erstellt mehrere Kinder auf einmal"""
        return [self.create(team) for _ in range(count)]
```

### Szenario-Fixture: kleine_liga

**tests/fixtures/kleine_liga.py:**
```python
import pytest
from datetime import date
from app.models import Verein, Team, Saison, Figur, Offizieller
from tests.factories import KindFactory

@pytest.fixture
def kleine_liga(db_session):
    """
    Realistische kleine Liga für Tests:
    - 2 Vereine
    - 4 Teams (2 pro Verein)
    - ~20 Kinder mit Faker-Daten
    - 1 Saison mit 5 Figuren
    - 5 Offizielle
    """

    # Vereine
    verein_neptun = Verein(
        name="SC Neptun",
        adresse="Schwimmbadstraße 1, 10115 Berlin"
    )
    verein_wasser = Verein(
        name="Wasserfreunde München",
        adresse="Olympiapark 5, 80809 München"
    )
    db_session.add_all([verein_neptun, verein_wasser])
    db_session.commit()

    # Teams
    team_neptun_jugend = Team(name="Neptun Jugend", verein=verein_neptun)
    team_neptun_kids = Team(name="Neptun Kids", verein=verein_neptun)
    team_wasser_jugend = Team(name="Wasser Jugend", verein=verein_wasser)
    team_wasser_kids = Team(name="Wasser Kids", verein=verein_wasser)

    teams = [team_neptun_jugend, team_neptun_kids, team_wasser_jugend, team_wasser_kids]
    db_session.add_all(teams)
    db_session.commit()

    # Kinder (5 pro Team = 20 gesamt) mit Faker
    kind_factory = KindFactory(db_session, seed=42)
    kinder = []
    for team in teams:
        kinder.extend(kind_factory.create_batch(team, count=5))

    # Saison
    saison = Saison(
        name="Saison 2024/2025",
        start_datum=date(2024, 9, 1),
        end_datum=date(2025, 6, 30)
    )
    db_session.add(saison)
    db_session.commit()

    # Figuren
    figuren = [
        Figur(name="Rückenschwimmen mit Bein", schwierigkeitsfaktor=1.8, saison=saison),
        Figur(name="Spirale", schwierigkeitsfaktor=2.3, saison=saison),
        Figur(name="Delphin", schwierigkeitsfaktor=2.5, saison=saison),
        Figur(name="Flamingo", schwierigkeitsfaktor=2.0, saison=saison),
        Figur(name="Korkenzieher", schwierigkeitsfaktor=2.8, saison=saison),
    ]
    db_session.add_all(figuren)
    db_session.commit()

    # Offizielle
    offizielle = [
        Offizieller(vorname="Maria", nachname="Schmidt", rolle="Kampfrichter"),
        Offizieller(vorname="Hans", nachname="Müller", rolle="Kampfrichter"),
        Offizieller(vorname="Anna", nachname="Weber", rolle="Kampfrichter"),
        Offizieller(vorname="Peter", nachname="Meyer", rolle="Punktrichter"),
        Offizieller(vorname="Lisa", nachname="Fischer", rolle="Punktrichter"),
    ]
    db_session.add_all(offizielle)
    db_session.commit()

    return {
        'vereine': [verein_neptun, verein_wasser],
        'teams': teams,
        'kinder': kinder,
        'saison': saison,
        'figuren': figuren,
        'offizielle': offizielle
    }
```

### Beispiel-Test: Anmeldungs-Workflow

**tests/integration/workflows/test_anmeldung_workflow.py:**
```python
import pytest
from datetime import date
from app.models import Wettkampf, Schwimmbad
from app.services.anmeldung_service import AnmeldungService
from app.repositories.anmeldung_repository import AnmeldungRepository
from app.schemas.anmeldung import AnmeldungCreate

@pytest.mark.integration
def test_anmeldung_workflow_20_kinder_startnummern(db_session, kleine_liga):
    """
    Szenario: 20 Kinder melden sich für einen Wettkampf an
    Erwartung: Startnummern 1-20, lückenlos, eindeutig
    """
    # Arrange: Wettkampf erstellen
    schwimmbad = Schwimmbad(
        name="Stadtbad Berlin",
        adresse="Badstraße 10, 10115 Berlin"
    )
    wettkampf = Wettkampf(
        name="Herbstturnier 2024",
        datum=date(2024, 10, 15),
        schwimmbad=schwimmbad,
        saison=kleine_liga['saison']
    )
    db_session.add(wettkampf)
    db_session.commit()

    # Service erstellen
    service = AnmeldungService(
        anmeldung_repo=AnmeldungRepository(db_session),
        kind_service=...,  # Mock oder echte Services
        wettkampf_service=...
    )

    # Act: Alle 20 Kinder anmelden
    anmeldungen = []
    for kind in kleine_liga['kinder']:
        anmeldung = service.create_anmeldung(
            AnmeldungCreate(
                kind_id=kind.id,
                wettkampf_id=wettkampf.id,
                figuren=[1, 2, 3]  # Erste 3 Figuren
            )
        )
        anmeldungen.append(anmeldung)

    # Assert
    assert len(anmeldungen) == 20

    # Startnummern prüfen
    startnummern = sorted([a.startnummer for a in anmeldungen])
    assert startnummern == list(range(1, 21)), "Startnummern nicht lückenlos"

    # Eindeutigkeit
    assert len(set(startnummern)) == 20, "Startnummern nicht eindeutig"

    # Alle bestätigt
    assert all(a.status == "BESTAETIGT" for a in anmeldungen)

@pytest.mark.integration
def test_anmeldung_doppelmeldung_verhindert(db_session, kleine_liga, wettkampf):
    """
    Szenario: Kind versucht sich zweimal für gleichen Wettkampf anzumelden
    Erwartung: DoppelmeldungError
    """
    from app.exceptions import DoppelmeldungError

    service = AnmeldungService(...)
    kind = kleine_liga['kinder'][0]

    # Erste Anmeldung
    service.create_anmeldung(
        AnmeldungCreate(kind_id=kind.id, wettkampf_id=wettkampf.id, figuren=[1])
    )

    # Zweite Anmeldung sollte fehlschlagen
    with pytest.raises(DoppelmeldungError, match="bereits angemeldet"):
        service.create_anmeldung(
            AnmeldungCreate(kind_id=kind.id, wettkampf_id=wettkampf.id, figuren=[2])
        )
```

---

## Konsequenzen

### Vorteile ✅

1. **Realistische Tests:** Echte DB mit allen Constraints und Relationships
2. **Schnell:** SQLite In-Memory, Tests in Millisekunden
3. **Isoliert:** Jeder Test unabhängig, kein Cleanup nötig
4. **Reproduzierbar:** Faker mit Seeds, deterministische Testdaten
5. **Wartbar:** Factories + Szenarios wiederverwendbar
6. **CI-freundlich:** Keine externe Infrastruktur nötig
7. **Produktionsnah:** SQLite = libSQL (Turso-kompatibel)
8. **Entwicklerfreundlich:** Einfaches Setup, schnelles Feedback

### Nachteile ⚠️

1. **Langsamer als Pure Unit-Tests:** DB-Setup hat Overhead (~50-100ms pro Test)
2. **Schema-Pflege:** Bei Migrations müssen Tests ggf. angepasst werden
3. **Komplexere Debugging:** Mehr Moving Parts (DB, ORM, Factories)
4. **Memory-Limits:** In-Memory DB bei sehr großen Datenmengen limitiert (nicht relevant für kleine Liga)

### Trade-offs

| Aspekt | Entscheidung | Alternative |
|--------|--------------|-------------|
| Test-DB | SQLite In-Memory | PostgreSQL Test-Container (langsamer) |
| Factories | Eigene Klassen | pytest-factoryboy (mehr Magic) |
| Fixtures | Szenario-basiert | Pro-Test-Setup (weniger DRY) |
| Faker | 20 Namen | Hardcoded (weniger realistisch) |
| Migrations | Bei Test-Setup | Direkt `Base.metadata.create_all()` (schneller, aber Schema-Drift-Risiko) |

---

## Alternativen (verworfen)

### 1. Repository-Mocking (❌)

```python
# Pseudocode
mock_repo = Mock(AnmeldungRepository)
mock_repo.find_by_kind_und_wettkampf.return_value = None
```

**Warum verworfen:**
- ❌ ORM-Logik (Relationships, Eager Loading) wird nicht getestet
- ❌ Constraints werden nicht geprüft (Unique, Foreign Key)
- ❌ Mock-Verhalten ≠ echtes DB-Verhalten
- ❌ Refactoring schwieriger (Mocks müssen angepasst werden)

**Wann OK:** Nur für pure Unit-Tests der Service-Logik

### 2. Test-Container mit PostgreSQL (❌)

```yaml
# docker-compose.test.yml
services:
  test-db:
    image: postgres:15
    environment:
      POSTGRES_DB: aquarius_test
```

**Warum verworfen:**
- ❌ Langsamer (Docker-Start: 2-5 Sekunden)
- ❌ Komplexeres Setup (Docker required)
- ❌ CI-Integration aufwendiger
- ✅ Aber: Produktionsnäher (wenn Produktion PostgreSQL wäre)

**Relevanz:** Turso = libSQL = SQLite-kompatibel → SQLite In-Memory ausreichend

### 3. Shared Test-DB (persistent) (❌)

```python
# Eine DB für alle Tests, Cleanup nach Test
def teardown():
    db.query(Anmeldung).delete()
    db.query(Kind).delete()
    # ...
```

**Warum verworfen:**
- ❌ Tests beeinflussen sich gegenseitig (Race Conditions)
- ❌ Cleanup fehleranfällig (vergessene Tabellen)
- ❌ Parallele Ausführung unmöglich
- ❌ Debugging schwieriger (State von vorherigen Tests)

---

## Implementierungs-Checkliste

- [ ] `tests/conftest.py` mit `db_engine` und `db_session` Fixtures
- [ ] Factories für: Verein, Team, Kind, Wettkampf, Figur, Offizieller
- [ ] Szenario-Fixture `kleine_liga` mit Faker (20 Kinder)
- [ ] Repository-Tests (CRUD, Queries, Constraints)
- [ ] Service-Tests (Anmeldung, Bewertung, Startnummernvergabe)
- [ ] Model-Tests (Relationships, Computed Properties)
- [ ] Workflow-Tests (End-to-End Integration-Szenarien)
- [ ] pytest.ini mit Markern (`unit`, `integration`, `slow`)
- [ ] CI-Integration (GitHub Actions)
- [ ] Coverage-Target: 80% für Service- und Repository-Layer

---

## Referenzen

- [pytest Documentation](https://docs.pytest.org/)
- [SQLAlchemy Testing](https://docs.sqlalchemy.org/en/20/orm/session_transaction.html#joining-a-session-into-an-external-transaction-such-as-for-test-suites)
- [Faker Documentation](https://faker.readthedocs.io/)
- [Test-Driven Development with Python (Harry Percival)](https://www.obeythetestinggoat.com/)

---

**Nächste Schritte:**
1. Review dieses ADR
2. Implementierung Basis-Fixtures (conftest.py)
3. Implementierung Factories
4. Erste Integration-Tests für Anmeldung

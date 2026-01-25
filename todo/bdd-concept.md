# Konzept: Einführung von Behavior-Driven Development (BDD) in Aquarius

## Zielsetzung
Einführung einer BDD-Methodik, um:
1.  **Anforderungen direkt von Stakeholdern** in verständlicher Form (Gherkin-Syntax) zu erfassen.
2.  Diese Anforderungen **automatisiert prüfbar** zu machen.
3.  Die Testergebnisse **nahtlos in das bestehende Reporting** (Test-Report Seite) zu integrieren.
4.  Den bestehenden Applikationscode (Backend/Frontend) **nicht zu verändern** (Zero-Invasion Strategy).

## Technologiewahl: `pytest-bdd`

Für das Aquarius-Projekt ist **`pytest-bdd`** das Werkzeug der Wahl.

### Begründung
*   **Technologie-Fit:** Da das Backend bereits in Python (FastAPI) geschrieben ist, fügt sich `pytest-bdd` nativ in die bestehende `pytest`-Infrastruktur ein.
*   **Reporting-Integration:** `pytest-bdd` generiert Standard-Pytest-Testergebnisse. Das bestehende Reporting-Skript (`scripts/compile-test-results.py`) kann diese ohne Anpassung verarbeiten und auf der Dokumentationsseite anzeigen.
*   **Keine Code-Änderung:** Die Tests agieren als externer Client (gegen die API oder Service-Schicht), ohne dass der Produktionscode für Testbarkeit angepasst werden muss.

### Warum nicht `behave`?
Obwohl `behave` ein populäres Framework mit Gherkin-Support ist, passt es aus zwei Gründen nicht zu den Projekt-Constraints:
1.  **Reporting-Bruch:** `behave` nutzt einen eigenen Test-Runner mit eigenem JSON-Output-Format. Dies würde erhebliche Anpassungen an `scripts/compile-test-results.py` erfordern, um die Ergebnisse im zentralen Dashboard anzuzeigen. `pytest-bdd` hingegen erzeugt Standard-Pytest-Reports.
2.  **Fixture-Wiederverwendung:** Das Projekt nutzt komplexe `pytest`-Fixtures (`client`, `db_session`, `app_token_headers`) in `conftest.py`. `pytest-bdd` kann diese Fixtures *direkt* in die Gherkin-Steps injizieren. Mit `behave` müsste dieser gesamte Test-Harness in `environment.py` portiert (dupliziert) werden, was Wartungsaufwand erzeugt.

---

## Workflow

### 1. Requirements Engineering (Stakeholder & PO)
Anforderungen werden nicht als Freitext, sondern als `.feature`-Dateien im Gherkin-Format definiert. Diese Dateien leben im Repository und sind die "Single Source of Truth".

**Ort:** `web/backend/tests/features/`

**Beispiel (`anmeldung_validierung.feature`):**
```gherkin
Feature: Anmeldung Validierung
  Als Vereinsvertreter
  Möchte ich sicherstellen, dass nur gültige Anmeldungen akzeptiert werden
  Damit die Wettkampfplanung korrekt ist

  Scenario: Anmeldung ohne Figuren ist vorläufig
    Given ein Kind "Max" existiert
    And ein Wettkampf "Herbstpokal" existiert
    When ich "Max" für "Herbstpokal" anmelde
    And ich keine Figuren angebe
    Then sollte der Status der Anmeldung "vorläufig" sein
```

### 2. Implementierung der Steps (Developer)
Entwickler schreiben "Glue Code", der die Gherkin-Schritte mit Python-Code verbindet. Dabei werden die bestehenden `pytest`-Fixtures (`client`, `db_session`) wiederverwendet.

**Ort:** `web/backend/tests/step_definitions/test_anmeldung_steps.py`

**Beispiel:**
```python
from pytest_bdd import scenario, given, when, then, parsers
from app import models

@scenario('../features/anmeldung_validierung.feature', 'Anmeldung ohne Figuren ist vorläufig')
def test_anmeldung_ohne_figuren():
    pass # Wird von pytest ausgeführt

@given(parsers.parse('ein Kind "{name}" existiert'))
def kind_existiert(client, name):
    # Nutzt existierende API oder Factories
    return create_kind_via_api(client, name)

@when('ich keine Figuren angebe')
def keine_figuren():
    pass

@then(parsers.parse('sollte der Status der Anmeldung "{status}" sein'))
def check_status(response, status):
    assert response.json()['status'] == status
```

### 3. Ausführung & Reporting
Die BDD-Tests werden automatisch mit dem bestehenden Test-Befehl ausgeführt:
make test
```

### 4. Integration ins Reporting (Nahtlos)
Das Skript `scripts/compile-test-results.py` verarbeitet die `pytest`-Ausgabe.
*   Der **Szenario-Name** (z.B. "Anmeldung ohne Figuren ist vorläufig") wird automatisch zur **Business Explanation**.
*   Der Test erscheint im existierenden Test-Report unter `docs/architecture/test-reporting/`.
*   **Keine Anpassung am Reporting-Skript notwendig**, da `pytest-bdd` kompatible Node-IDs generiert.

---

## Implementierungs-Plan

1.  **Installation:** `pip install pytest-bdd` (in `web/backend/requirements.txt` hinzufügen).
2.  **Verzeichnisstruktur:**
    ```
    web/backend/tests/
    ├── features/           # Gherkin Dateien
    └── step_definitions/   # Python Step Code
    ```
3.  **Pilot-Szenario:** Umsetzung des Beispiels "Anmeldung Validierung" als Proof-of-Concept.

## Vorteile dieses Ansatzes
*   **Lebende Dokumentation:** Die `.feature` Dateien veralten nicht, da sie ausführbar sind.
*   **Stakeholder-Fokus:** Fachliche Diskussionen finden anhand konkreter Beispiele (Szenarien) statt.
*   **Investitionsschutz:** Bestehende Tests und Reporting-Pipelines bleiben 100% erhalten.

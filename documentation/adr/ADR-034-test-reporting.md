# ADR-034: Test Reporting für Dokumentations-Website

**Status:** Akzeptiert
**Datum:** 2026-01-23
**Entscheider:** Architektur-Team

## Kontext

Das Projekt verfügt über automatisierte Tests für das Backend (Python/pytest) und das Frontend (TypeScript/Vitest). Bisher sind die Ergebnisse dieser Tests nicht direkt in der öffentlichen Dokumentations-Website sichtbar, die mit Jekyll generiert wird. Es besteht Bedarf, die Transparenz und das Vertrauen in die Codequalität durch die Anzeige von Testergebnissen zu erhöhen.

## Entscheidung

Wir implementieren eine Test-Reporting-Funktion für die Jekyll-Dokumentations-Website. Dies wird erreicht durch:

1.  **Generierung von JSON-Reports:** Konfiguration von `pytest` (Backend) und `vitest` (Frontend), um Testläufe in maschinenlesbarem JSON-Format auszugeben.
2.  **Kompilierungsskript:** Erstellung eines Python-Skripts (`scripts/compile-test-results.py`), das die generierten JSON-Reports verarbeitet und eine einzige, für Jekyll lesbare Datendatei (`docs/_data/test_results.json`) erstellt.
3.  **Neue Jekyll-Seite:** Eine neue Seite (`docs/_pages/architecture/test-reporting.md`) mit "splash"-Layout wird erstellt. Diese Seite zeigt die Testergebnisse gruppiert nach Hauptentitäten mit Inhaltsverzeichnis und je Entität einer Tabelle (Business-Erklärung (Slug), Technischer Name, Ergebnis) an.
4.  **Integration in Architektur-Übersicht:** Ein neuer Kachel-Link wird zur Architektur-Übersichtsseite (`docs/_pages/architecture/index.md`) hinzugefügt, der zur neuen Test-Report-Seite führt.
5.  **Automatisierung über Makefile:** Ein neues Root-Makefile-Ziel (`make test`) wird erstellt. Dieses Ziel führt die Tests aus, kompiliert die Ergebnisse und stößt anschließend die Neukompilierung der Jekyll-Website an.
6.  **CI/CD-Integration:** Das GitHub Actions Workflow (`.github/workflows/build-aquarius-jekyll-site.yml`) wird modifiziert, um `make test` im CI-Prozess auszuführen. Dies stellt sicher, dass die Testresultate auf der öffentlichen Website sichtbar sind.

## Begründung

- **Transparenz:** Macht die Testabdeckung und den Erfolg von Testläufen für alle Projektbeteiligten und Benutzer der Dokumentation sichtbar.
- **Qualitätssicherung:** Verstärkt das Engagement für Codequalität und Zuverlässigkeit.
- **Automatisierung:** Stellt sicher, dass die Testberichte automatisch mit jeder Website-Generierung aktuell gehalten werden.
- **Integration:** Nutzt bestehende Werkzeuge und Prozesse (Make, Jekyll, Docker, GitHub Actions) zur nahtlosen Integration.

## Konsequenzen

### Positiv
- Erhöhte Transparenz über den Projektgesundheitszustand.
- Ermutigung zu besseren Testpraktiken und Dokumentation von Tests.
- Nahtlose Integration der Testresultate in die bestehende Dokumentationsarchitektur.

### Negativ
- Wartungsaufwand für das Kompilierungsskript (`compile-test-results.py`), falls sich die Ausgabeformate der Test-Runner signifikant ändern.
- Leichte Erhöhung der Build-Zeit im CI/CD-Prozess.

## Hinweis zur Erstellung von Python Docstrings für Tests

Um die "Beschreibung" für Tests im Report aussagekräftiger zu gestalten, sollten Python-Tests eine kurze, domänenspezifische Erklärung in ihren Docstrings enthalten. Die erste Zeile des Docstrings kann als primäre Beschreibung für die Anzeige im Testreport dienen und liefert Kontext, der über den rein technischen Testnamen hinausgeht. Dies verbessert das Verständnis des Geschäftsnutzens eines Tests.

### Beispiel: Python-Test mit erklärendem Docstring

**Originaler Test (ohne aussagekräftigen Docstring):**
```python
# tests/api/test_verein.py
def test_create_verein(client, app_token_headers):
    """Test zum Anlegen eines neuen Vereins.""" # Vage Beschreibung
    response = client.post(
        "/api/verein",
        json={
            "name": "Test Schwimmverein",
            "ort": "Berlin",
            "register_id": "VR-12345",
            "contact": "info@testschwimmverein.de"
        },
        headers=app_token_headers
    )
    assert response.status_code == status.HTTP_201_CREATED
    # ... Assertions ...
```

**Test mit erklärendem Docstring:**
```python
# tests/api/test_verein.py
def test_create_verein(client, app_token_headers):
    """
    API-Test - Vereinsverwaltung: Ein neuer Verein kann erfolgreich angelegt werden.
    Dieser Test stellt sicher, dass der API-Endpunkt zum Anlegen eines Vereins
    gültige Daten korrekt verarbeitet und den Status 201 Created zurückgibt.
    """ # Aussagekräftige Beschreibung, die den Geschäftskontext erklärt
    response = client.post(
        "/api/verein",
        json={
            "name": "Test Schwimmverein",
            "ort": "Berlin",
            "register_id": "VR-12345",
            "contact": "info@testschwimmverein.de"
        },
        headers=app_token_headers
    )
    assert response.status_code == status.HTTP_201_CREATED
    # ... Assertions ...
```
Nach Ausführung von `make test` wird die erste Zeile des Docstrings ("API-Test - Vereinsverwaltung: Ein neuer Verein kann erfolgreich angelegt werden.") als "Beschreibung" im Testreport angezeigt, was deutlich mehr geschäftlichen Kontext liefert als nur "Api Test verein: Create verein".

**Hinweis für Frontend-Tests:** Für Frontend-Tests in TypeScript/JavaScript können ähnliche Prinzipien angewendet werden, z. B. durch aussagekräftige `describe`-Blöcke oder JSDoc-Kommentare direkt über den Testfunktionen. Das Kompilierungsskript versucht, diese Informationen zu extrahieren, fällt aber auf eine generierte Beschreibung zurück, wenn keine klaren Hinweise gefunden werden.

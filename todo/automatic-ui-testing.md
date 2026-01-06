## Automatisches UI‑Testing (Frontend)

Ziel: Ein schlankes, zuverlässiges Testkonzept, damit wir nicht jedes Mal manuell testen müssen. Fokus auf wenige, stabile „Happy‑Path“ End‑to‑End‑Szenarien plus ein paar Smoke‑Checks.

---

## Werkzeug‑Empfehlung

**Playwright** ist sehr gut geeignet:
- stabil, schnell, cross‑browser
- gute Debug‑Tools und Trace‑Viewer
- einfache Integration in CI

Alternativen:
- **Cypress** (breite Community, etwas schwergewichtig)
- **Vitest + Testing Library** für komponentennahe Tests (kein echtes Browser‑E2E)

Empfehlung: **Playwright** für E2E + optional **Vitest** für komponentennahe Logik.

---

## Testziele (Minimalset)

1) **Smoke**
- App lädt
- Navigation/Sidebar sichtbar
- Grunddaten‑Übersicht erreichbar

2) **CRUD‑Happy‑Paths**
- Kind anlegen (minimal), erscheint in Liste
- Kind bearbeiten (z.B. Nachname), Änderung sichtbar
- Anmeldung anlegen (mit Kind, Wettkampf, Figuren) – Status sichtbar

3) **Regel: Versicherungspflicht**
- Kind ohne Versicherung -> Anmeldung wird „vorläufig“ + „unversichert“ markiert
- Kind mit Versicherung/Verband/Verein -> Anmeldung „aktiv“

4) **Grunddaten‑Listen**
- Verbände, Versicherungen listenbar

---

## Testdaten & Umgebung

- Für E2E ideal: **lokale SQLite DB** + Seed‑Daten (make db-reset).
- Tests laufen gegen `http://localhost:...` (via `make dev` oder `docker compose`).
- Für CI: eigener Test‑DB‑Container oder in‑memory (wenn möglich).

---

## Teststruktur (Playwright)

```
web/frontend/tests/e2e/
  smoke.spec.ts
  kind.spec.ts
  anmeldung.spec.ts
  grunddaten.spec.ts
  fixtures/
```

---

## Beispiel‑Scenarios (skizziert)

**smoke.spec.ts**
- Öffne `/`
- Prüfe Titel + Sidebar + Link „Grunddaten“

**kind.spec.ts**
- Erstelle Kind (minimal)
- Suche Kind in Liste
- Bearbeite Kind (Nachname) und prüfe Anzeige

**anmeldung.spec.ts**
- Erstelle Anmeldung ohne Versicherung -> „vorläufig“ + „unversichert“
- Aktualisiere Kind (Versicherung setzen) -> Anmeldung aktualisiert (optional)

---

## Qualitätsregeln

- Tests sollen **stabil** sein (keine fragilen Selektoren).
- Bevorzugt `data-testid` für kritische Elemente.
- Max. 5–8 E2E‑Tests als Start.

---

## CI‑Integration (später)

- Playwright‑Tests in GitHub Actions
- Artefakte: Screenshots + Trace bei Fehlern

---

## Erweiterungen (optional)

- Visual Regression (z.B. Playwright snapshot)
- Performance‑Smoke (Ladezeiten der Startseite)

---

## Nächster Schritt

Wenn du einverstanden bist, kann ich als erstes:
1) Playwright einrichten
2) eine Smoke‑Suite + 1–2 Happy‑Path‑Tests implementieren
3) `make test-ui` ergänzen

# From PoC to DDD-influenced Modularisierung

Ziel: In kleinen, testbaren Schritten von der aktuellen PoC-Struktur zu einer besser modularisierten, Domain‑Driven‑Design‑angelehnten Architektur kommen. Nach jedem Schritt bleibt die Anwendung vollständig lauffähig.

## Ausgangslage (kurz)
- Backend: FastAPI mit `app/main.py` als Monolith, zentrale `schemas/__init__.py`, Models teils in `models/__init__.py`.
- Frontend: Seiten + API‑Zugriffe pro Page, gemeinsame Types in `src/types/index.ts`.
- Business Rules liegen verteilt in Handlern (z.B. Anmeldung‑Logik).

## Leitprinzipien für die Schritte
- **Rückwärtskompatibilität**: alte Imports/Endpunkte bleiben bestehen, ggf. über Re‑Exports.
- **Inkremente**: Jede Änderung in einem PR/Issue testbar.
- **Domain‑Fokus**: Module/Services pro fachlichem Kontext, nicht nach Technik.
- **Keine Funktionalitätsverluste**: App bleibt nutzbar, Tests laufen weiterhin.

---

## Schritt 0 — Baseline sichern (Vorbereitung)
**Ziel**: Minimale Test- und Strukturabsicherung, bevor wir umbauen.

**Tasks**
- Dokumentieren, welche Endpunkte/Pages „kritisch“ sind.
- Optional: Smoketests (minimal) für Start + Kernflows.

**Akzeptanz**
- `make test` (Backend) läuft weiterhin.
- Keine Änderungen an Laufzeitverhalten.

---

## Schritt 1 — Domain‑Ordnerstruktur im Backend anlegen (ohne Umzug)
**Ziel**: Zielstruktur anlegen, ohne bestehende Imports zu brechen.

**Tasks**
- Unter `app/` neue Pakete anlegen: `kind/`, `anmeldung/`, `wettkampf/`, `grunddaten/`, `shared/`.
- Je Paket: `__init__.py`, Platzhalter `services.py`, `schemas.py`, `repository.py`.
- Re‑Exports in `app/schemas/__init__.py` und `app/models/__init__.py` (vorerst leer/alias).

**Akzeptanz**
- App startet unverändert.
- Keine Codepfade wurden verändert.

---

## Schritt 2 — Schemas modularisieren (nur Schemas umziehen)
**Ziel**: Pydantic‑Schemas je Domain bündeln, ohne API‑Signaturen zu ändern.

**Tasks**
- `Kind`, `Anmeldung`, `Wettkampf`, `Verband`, `Versicherung`, `Verein`, `Figur`, `Schwimmbad`, `Saison` in passende Domain‑`schemas.py` verschieben.
- In `app/schemas/__init__.py` Re‑Exports beibehalten.

**Akzeptanz**
- Alle API‑Responses/Requests unverändert.
- `pytest` grün.

---

## Schritt 3 — Router pro Domain (API‑Schicht trennen)
**Ziel**: `main.py` entlasten, Endpunkte in Domain‑Router verschieben.

**Tasks**
- Pro Domain `router.py` anlegen (FastAPI APIRouter).
- Endpunkte schrittweise aus `main.py` verschieben (z.B. zuerst `kind`, dann `anmeldung`).
- In `main.py` Router mounten.

**Akzeptanz**
- Alle URLs bleiben gleich.
- `pytest` grün.

---

## Schritt 4 — Repository‑Schicht pro Domain
**Ziel**: SQLAlchemy‑Zugriff zentralisieren.

**Tasks**
- Repository‑Funktionen pro Domain (CRUD + spezifische Queries).
- Handler/Router rufen Repos statt direkt `db.query(...)`.

**Akzeptanz**
- Keine Logikänderung, nur Struktur.
- `pytest` grün.

---

## Schritt 5 — Domain‑Services für Geschäftsregeln
**Ziel**: Geschäftslogik außerhalb der API‑Schicht bündeln.

**Tasks**
- Services für `Anmeldung` (vorläufig/versicherung‑Regel) und `Kind` (Versicherungsvalidität).
- Router ruft Services; Services nutzen Repositories.
- Logik in Tests abdecken.

**Akzeptanz**
- Business Rules unverändert.
- Tests spezifisch für Service‑Funktionen vorhanden.

---

## Schritt 6 — DTOs/Mapper für API‑Antworten
**Ziel**: Trennung zwischen Domain‑Modell und API‑Response (z.B. `insurance_ok`).

**Tasks**
- Mapper/Assembler‑Funktionen je Domain (`to_anmeldung_dto`, `to_kind_dto`).
- Router verwenden Mapper.

**Akzeptanz**
- API‑Outputs unverändert.
- Mapper‑Tests vorhanden.

---

## Schritt 7 — Frontend: Domain‑Slices & API‑Clients
**Ziel**: UI‑Logik pro Domain bündeln.

**Tasks**
- `src/api/{kind,anmeldung,grunddaten,wettkampf}.ts` mit Funktionen.
- `src/types` in Domain‑Dateien splitten (Re‑Exports in `types/index.ts`).
- Pages nutzen die Domain‑Clients statt Inline‑API‑Calls.

**Akzeptanz**
- UI unverändert.
- Builds/Tests laufen.

---

## Schritt 8 — Fachliche Validierung im Frontend ergänzen
**Ziel**: Nutzerfeedback zu Versicherungsstatus.

**Tasks**
- Anzeige von Versicherungsstatus konsistent in allen Listen.
- Optional: Hinweise in Kind‑Detail bei fehlender Versicherung.

**Akzeptanz**
- Visuals konsistent und getestet (manuell + ggf. Snapshot).

---

## Schritt 9 — Dokumentation & ADRs
**Ziel**: Architekturänderungen dokumentieren.

**Tasks**
- ADR: „Modularisierung nach DDD‑Prinzipien“.
- Docs: Übersicht der Bounded Contexts/Module.

**Akzeptanz**
- Dokumentation im `docs/src/` aktualisiert.

---

## Issue‑Schnitt (Beispiele)
Jeder Schritt kann als GitHub‑Issue angelegt werden, z.B.:
- “Backend: Schemas für Kind/Anmeldung modularisieren (Re‑Exports behalten)”
- “Backend: Anmeldung‑Router aus main.py auslagern”
- “Frontend: Versicherungs‑UI konsolidieren”

---

## Prüfkriterien pro Schritt
- `make test` (Backend) grün.
- App startet (Frontend/Backend).
- Keine API‑Breaking‑Changes ohne Re‑Export/Fallback.

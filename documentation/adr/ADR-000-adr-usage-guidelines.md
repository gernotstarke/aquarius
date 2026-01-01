# ADR-000: ADR-Nutzungsrichtlinien

**Status:** Accepted
**Datum:** 2025-12-31
**Entscheider:** Architektur-Team

## Kontext

Dieses Dokument beschreibt, wie Architecture Decision Records (ADRs) im Aquarius-Projekt verwendet werden.

## Was sind ADRs?

ADRs dokumentieren **wichtige Architekturentscheidungen** mit:
- **Kontext**: Warum stand eine Entscheidung an?
- **Entscheidung**: Was wurde beschlossen?
- **Konsequenzen**: Welche Auswirkungen hat das?

Siehe: [Michael Nygard: Documenting Architecture Decisions](https://cognitect.com/blog/2011/11/15/documenting-architecture-decisions)

## Dateistruktur

```
/documentation/adr/
├── ADR-000-adr-usage-guidelines.md    ← Diese Datei
├── ADR-001-vite-build-tool.md
├── ADR-002-...
└── ...
```

**Namenskonvention:** `ADR-XXX-kurzer-titel.md`

## Automatische Website-Integration

ADRs werden automatisch auf die Jekyll-Website unter `/architecture/adrs/` publiziert:

```
Source:  /documentation/adr/ADR-001-*.md
  ↓ (make website-dev / GitHub Actions)
Output:  /docs/_adrs/ADR-001-*.md (mit Jekyll Front Matter)
  ↓ (Jekyll Build)
Website: https://aquarius.arc42.org/architecture/adrs/ADR-001/
```

Das Verzeichnis `/docs/_adrs/` ist in `.gitignore` – nur die Quelldateien werden versioniert.

## Erlaubte Status

| Status | Deutsch | Bedeutung |
|--------|---------|-----------|
| **Proposed** | Vorgeschlagen | In Diskussion, noch nicht final |
| **Accepted** | Akzeptiert | Entscheidung getroffen und gültig |
| **Deprecated** | Veraltet | Noch gültig, aber Ablösung geplant |
| **Superseded** | Ersetzt | Durch neuere Entscheidung ersetzt |
| **Rejected** | Abgelehnt | Bewusst nicht umgesetzt |

Details: Siehe [ADR-020: Status-Lebenszyklus](ADR-020-decision-status-lifecycle.md)

## ADR-Template

```markdown
# ADR-XXX: Titel der Entscheidung

**Status:** Proposed
**Datum:** YYYY-MM-DD
**Entscheider:** Team/Person

## Kontext
[Warum steht diese Entscheidung an?]

## Entscheidung
[Was wurde beschlossen?]

## Konsequenzen
[Positive und negative Auswirkungen]
```

## Wann braucht es ein ADR?

- Technologie-Auswahl (Framework, Datenbank, etc.)
- Architekturmuster (Microservices, Monolith, etc.)
- Wichtige Design-Entscheidungen
- Abweichungen von Standards

**Kein ADR nötig für:** Bugfixes, kleine Refactorings, UI-Änderungen.

# ADR-020: Status-Lebenszyklus für Architekturentscheidungen

**Status:** Accepted
**Datum:** 2025-12-31
**Entscheider:** Architektur-Team

## Kontext

Architecture Decision Records (ADRs) durchlaufen verschiedene Phasen ihres Lebenszyklus. Ein klares Status-Modell hilft bei:

- **Übersichtlichkeit**: Schnell erkennen, welche Entscheidungen gelten
- **Nachvollziehbarkeit**: Historie von Entscheidungen verstehen
- **Kommunikation**: Einheitliche Sprache im Team

Bisher wurden Status informell verwendet ("Accepted", "Akzeptiert"), ohne klare Definition der erlaubten Werte und ihrer Bedeutung.

## Entscheidung

Wir definieren **fünf erlaubte Status** für ADRs mit klarer Semantik und visuellem Indikator.

### Status-Definitionen

| Status | Deutsch | Icon | Farbe | Bedeutung |
|--------|---------|------|-------|-----------|
| **Proposed** | Vorgeschlagen | ❓ | Blau | Entscheidung in Diskussion, noch nicht final |
| **Accepted** | Akzeptiert | ✅ | Grün | Entscheidung getroffen und gültig |
| **Deprecated** | Veraltet | ⚠️ | Orange | Entscheidung noch gültig, aber Ablösung geplant |
| **Superseded** | Ersetzt | → | Grau | Durch neuere Entscheidung ersetzt |
| **Rejected** | Abgelehnt | ❌ | Rot | Entscheidung wurde bewusst abgelehnt |

### Lebenszyklus

```
                    ┌──────────────┐
                    │   Proposed   │
                    │      ❓       │
                    └──────┬───────┘
                           │
              ┌────────────┼────────────┐
              │            │            │
              ▼            ▼            ▼
       ┌──────────┐ ┌──────────┐ ┌──────────┐
       │ Accepted │ │ Rejected │ │(zurück-  │
       │    ✅     │ │    ❌     │ │ gezogen) │
       └────┬─────┘ └──────────┘ └──────────┘
            │
            │ Zeit / neue Erkenntnisse
            │
    ┌───────┴───────┐
    │               │
    ▼               ▼
┌──────────┐  ┌──────────┐
│Deprecated│  │Superseded│
│    ⚠️     │  │    →     │
└────┬─────┘  └──────────┘
     │             ▲
     │             │
     └─────────────┘
      (durch neue ADR)
```

### Übergänge

| Von | Nach | Trigger |
|-----|------|---------|
| Proposed | Accepted | Team-Entscheidung für Umsetzung |
| Proposed | Rejected | Team-Entscheidung gegen Umsetzung |
| Accepted | Deprecated | Bessere Alternative identifiziert, Migration geplant |
| Accepted | Superseded | Neue ADR ersetzt diese direkt |
| Deprecated | Superseded | Migration abgeschlossen |

### Format in ADR-Dateien

```markdown
# ADR-XXX: Titel der Entscheidung

**Status:** Accepted
**Datum:** 2025-12-31
**Entscheider:** Team/Person

<!-- Bei Superseded: -->
**Ersetzt durch:** [ADR-YYY](ADR-YYY-neue-entscheidung.md)

<!-- Bei Deprecated: -->
**Ablösung geplant:** [ADR-YYY](ADR-YYY-neue-entscheidung.md)
```

## Begründung

### Warum genau fünf Status?

- **Proposed**: Ermöglicht Diskussion vor finaler Entscheidung
- **Accepted**: Klarer "aktiv"-Status für gültige Entscheidungen
- **Deprecated**: Wichtig für Übergangsphase bei Migrationen
- **Superseded**: Zeigt klar, dass neuere Entscheidung existiert
- **Rejected**: Dokumentiert bewusste Nicht-Entscheidungen (verhindert erneute Diskussion)

### Warum zweisprachig?

Das Projekt verwendet sowohl deutsche als auch englische Begriffe. Beide Varianten werden vom System erkannt:
- `Accepted` = `Akzeptiert`
- `Proposed` = `Vorgeschlagen`
- etc.

### Warum visuelle Indikatoren?

- **Schnelle Erfassung**: Farben und Icons kommunizieren Status auf einen Blick
- **Barrierefreiheit**: Icons haben Titel-Attribute für Screenreader
- **Konsistenz**: Gleiche Visualisierung auf Website und in Tools

## Konsequenzen

### Positiv

- Einheitliche Status-Sprache im Team
- Klare Visualisierung auf der Website
- Historische Entscheidungen bleiben nachvollziehbar
- Vermeidung von "Zombie-ADRs" ohne klaren Status

### Negativ

- Bestehende ADRs müssen ggf. Status normalisieren
- Zusätzliche Pflege bei Status-Änderungen

### Migration bestehender ADRs

Alle bestehenden ADRs mit `Accepted` oder `Akzeptiert` behalten ihren Status. Keine Migration erforderlich, da beide Varianten unterstützt werden.

## Implementierung

### Website-Integration

Die Jekyll-Website zeigt Status-Icons in der ADR-Liste:

```liquid
{% raw %}{% include adr-status-icon.html status=adr.adr_status %}{% endraw %}
```

### Validierung (optional, zukünftig)

Ein Pre-Commit-Hook könnte ungültige Status ablehnen:

```bash
# Erlaubte Status
VALID_STATUS="proposed|accepted|deprecated|superseded|rejected"
VALID_STATUS+="|vorgeschlagen|akzeptiert|veraltet|ersetzt|abgelehnt"
```

## Referenzen

- [Michael Nygard: Documenting Architecture Decisions](https://cognitect.com/blog/2011/11/15/documenting-architecture-decisions)
- [ADR GitHub Organization](https://adr.github.io/)

# ADR-019: Dokumentations-Kompilierung für Jekyll Website

**Status:** Accepted
**Datum:** 2025-12-31
**Entscheider:** Gernot Starke

## Kontext

Die Aquarius-Dokumentation existiert in verschiedenen Formaten an verschiedenen Stellen:

- **ADRs** in `/documentation/adr/` als Markdown
- **arc42-Dokumentation** (geplant) in AsciiDoc
- **Weitere Dokumentation** möglicherweise in anderen Formaten

Diese Dokumentation soll auf der Jekyll-basierten Website unter `aquarius.arc42.org` verfügbar sein, jedoch:

1. Die **Quelldateien** sollen an ihrem ursprünglichen Ort bleiben (Single Source of Truth)
2. Die Website benötigt **Jekyll-spezifisches Front Matter** für Layout, Permalinks, etc.
3. Die Website ist **passwortgeschützt** (Architektur-Bereich)
4. Der **Build-Prozess** muss sowohl lokal (Docker) als auch in CI/CD (GitHub Actions) funktionieren

## Entscheidung

Wir implementieren einen **Kompilierungsschritt**, der Dokumentation aus den Quellverzeichnissen in Jekyll-kompatibles Format konvertiert.

### Architektur

```
┌─────────────────────────┐      ┌─────────────────────────┐
│   Quell-Dokumentation   │      │    Jekyll Website       │
│                         │      │                         │
│  documentation/         │      │  docs/                  │
│  ├── adr/              │─────▶│  ├── _adrs/            │
│  │   └── ADR-*.md      │      │  │   └── ADR-*.md      │
│  └── arc42/            │─────▶│  └── _arc42/           │
│      └── *.adoc        │      │      └── *.md          │
└─────────────────────────┘      └─────────────────────────┘
         │                                   │
         │   compile-adrs.sh                 │
         │   (future: compile-arc42.sh)      │
         └───────────────────────────────────┘
```

### Compile-Skripte

Jedes Quellformat erhält ein eigenes Kompilierungsskript:

| Skript | Quelle | Ziel | Konvertierung |
|--------|--------|------|---------------|
| `compile-adrs.sh` | `documentation/adr/*.md` | `docs/_adrs/*.md` | Front Matter hinzufügen |
| `compile-arc42.sh` (geplant) | `documentation/arc42/*.adoc` | `docs/_arc42/*.md` | AsciiDoc → Markdown |

### Front Matter Generation

Die Skripte extrahieren Metadaten aus den Quelldateien und generieren Jekyll Front Matter:

```yaml
---
title: "ADR-001: Vite als Build-Tool"
adr_number: "001"
adr_status: "accepted"
adr_date: "2025-12-17"
permalink: /architecture/adrs/ADR-001/
layout: protected  # Automatisch durch Jekyll defaults
---
```

### Build-Integration

```makefile
# Makefile
website-compile:  # Kompiliert alle Dokumentation
    docker compose run --rm compile-adrs
    # future: docker compose run --rm compile-arc42

website-dev: website-compile
    docker compose run --rm obfuscate
    docker compose up jekyll
```

## Begründung

### Warum Kompilierung statt Kopieren?

1. **Front Matter**: Jekyll benötigt YAML-Header, die in den Quelldateien nicht vorhanden sind
2. **Metadaten-Extraktion**: Status, Datum etc. werden aus dem Inhalt geparst
3. **Format-Konvertierung**: AsciiDoc → Markdown für arc42
4. **Flexibilität**: Unterschiedliche Transformationen je nach Quellformat

### Warum Single Source of Truth?

1. **Keine Duplikation**: Änderungen nur an einer Stelle
2. **Versionskontrolle**: Klare Historie in `/documentation/`
3. **Tool-Unabhängigkeit**: Quelldateien funktionieren auch ohne Website

### Warum gitignore für generierte Dateien?

1. **Kein Merge-Konflikt**: Generierte Dateien nie committet
2. **Frischer Build**: Jeder Build startet sauber
3. **CI/CD-Kompatibilität**: Gleicher Prozess lokal und in Pipeline

## Konsequenzen

### Positiv

- Dokumentation an einer Stelle gepflegt
- Website automatisch aktualisiert bei Änderungen
- Erweiterbar für neue Dokumentationsformate
- Konsistente Metadaten durch Skript-Extraktion

### Negativ

- Zusätzlicher Build-Schritt
- Skripte müssen gepflegt werden
- Debugging bei Fehlern komplexer

### Risiken

| Risiko | Mitigation |
|--------|------------|
| Skript-Fehler bei unerwarteten Formaten | Robuste Regex, Fallback-Werte |
| Performance bei vielen Dateien | Shell-Skripte sind schnell, parallelisierbar |
| Inkonsistenz zwischen lokal und CI | Identische Skripte, getestet |

## Implementierung

### Phase 1 (implementiert)
- `compile-adrs.sh` für ADR-Konvertierung
- Jekyll Collection `_adrs`
- Makefile-Integration

### Phase 2 (geplant)
- `compile-arc42.sh` für AsciiDoc-Konvertierung
- Jekyll Collection `_arc42`
- Asciidoctor-Integration

## Validierung

- ✅ ADRs erscheinen auf Website unter `/architecture/adrs/`
- ✅ Metadaten korrekt extrahiert
- ✅ Passwortschutz aktiv
- ✅ `make website-dev` kompiliert automatisch
- ✅ GitHub Actions kompiliert vor Jekyll Build

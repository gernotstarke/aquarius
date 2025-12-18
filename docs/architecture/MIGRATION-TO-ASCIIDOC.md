# Migration der arc42-Dokumentation nach AsciiDoc

**Status:** Vorschlag
**Datum:** 2025-12-18

---

## Motivation

Die aktuelle Markdown-basierte Dokumentation hat Einschränkungen:
- ❌ Keine `include::`-Statements (alles in einer Datei oder manuelle Verweise)
- ❌ PlantUML-Integration nur über externe Dateien + Bilder
- ❌ Schwierigere Wartung bei großen Dokumenten (aktuell 1500+ Zeilen)
- ❌ Keine standardisierten arc42-Templates für Markdown

**AsciiDoc-Vorteile:**
- ✅ Native `include::`-Direktiven für modulare Docs
- ✅ PlantUML-Integration: `[plantuml]` Blöcke direkt im Text
- ✅ arc42-Standard: Offizielle Templates in AsciiDoc
- ✅ Bessere Tooling (asciidoctor, arc42-generator)
- ✅ PDF-Generierung mit asciidoctor-pdf
- ✅ Versionierung einzelner Kapitel

---

## Vorgeschlagene Struktur

```
docs/
├── architecture.adoc                    # 🎯 Hauptdokument (Entry Point)
│
├── architecture/                        # arc42 Kapitel
│   ├── 01-einfuehrung.adoc
│   ├── 02-randbedingungen.adoc
│   ├── 03-kontextabgrenzung.adoc
│   ├── 04-loesungsstrategie.adoc
│   ├── 05-bausteinsicht.adoc
│   ├── 06-laufzeitsicht.adoc
│   ├── 07-verteilungssicht.adoc
│   ├── 08-querschnittliche-konzepte.adoc
│   │   ├── 08-01-domaenenmodell.adoc
│   │   ├── 08-02-persistenz.adoc
│   │   └── ...
│   ├── 09-architekturentscheidungen.adoc
│   ├── 10-qualitaetsanforderungen.adoc
│   ├── 11-risiken.adoc
│   └── 12-glossar.adoc
│
├── architecture/images/                 # 🖼️ Alle Diagramme
│   ├── puml/                            # PlantUML-Quellen
│   │   ├── 01-system-overview.puml
│   │   ├── 02-backend-modules.puml
│   │   ├── 03-anmeldung-module.puml
│   │   ├── 04-bewertung-module.puml
│   │   ├── 05-frontend-structure.puml
│   │   └── 06-entity-relationship.puml
│   ├── generated/                       # Generierte PNGs (aus puml)
│   │   ├── 01-system-overview.png
│   │   └── ...
│   └── screenshots/                     # Screenshots, Wireframes
│
├── architecture/adr/                    # ADRs (unverändert)
│   ├── ADR-009-testkonzept.md
│   ├── ADR-010-makefile.md
│   ├── ...
│   └── ADR-018-domain-driven-design.md
│
└── requirements/
    └── requirements.md                  # Anforderungen (bleibt Markdown)
```

---

## Hauptdokument: `docs/architecture.adoc`

```asciidoc
= Aquarius: Architektur-Dokumentation
Aquarius-Team <team@aquarius.io>
v1.0, 2025-12-18
:toc: left
:toclevels: 3
:sectnums:
:icons: font
:plantuml-server-url: http://www.plantuml.com/plantuml
:imagesdir: architecture/images
:source-highlighter: rouge

[.lead]
Architektur-Dokumentation für das Aquarius Wettkampf-Bewertungssystem nach arc42-Template.

'''

// Kapitel 1
include::architecture/01-einfuehrung.adoc[]

// Kapitel 2
include::architecture/02-randbedingungen.adoc[]

// Kapitel 3
include::architecture/03-kontextabgrenzung.adoc[]

// Kapitel 4
include::architecture/04-loesungsstrategie.adoc[]

// Kapitel 5
include::architecture/05-bausteinsicht.adoc[]

// Kapitel 6
include::architecture/06-laufzeitsicht.adoc[]

// Kapitel 7
include::architecture/07-verteilungssicht.adoc[]

// Kapitel 8
include::architecture/08-querschnittliche-konzepte.adoc[]

// Kapitel 9
include::architecture/09-architekturentscheidungen.adoc[]

// Kapitel 10
include::architecture/10-qualitaetsanforderungen.adoc[]

// Kapitel 11
include::architecture/11-risiken.adoc[]

// Kapitel 12
include::architecture/12-glossar.adoc[]
```

---

## Beispiel-Kapitel: `05-bausteinsicht.adoc`

```asciidoc
== Bausteinsicht

=== 5.1 Whitebox Gesamtsystem (Level 0)

Das Aquarius-System besteht aus zwei Hauptanwendungen, die auf einem gemeinsamen Backend operieren:

[plantuml, 01-system-overview, png]
----
include::images/puml/01-system-overview.puml[]
----

**Begründung:**

* **Zwei Frontend-Anwendungen** für unterschiedliche Nutzungskontexte (Büro vs. Schwimmbad)
* **Ein Backend** für zentrale Business-Logik und Datenkonsistenz
* **Eine Datenbank** mit Cloud-Sync für hybride Online/Offline-Nutzung

=== 5.2 Bausteinsicht Level 1 - Backend-Module

Das Backend ist in **6 fachliche Module** (Bounded Contexts) strukturiert:

[plantuml, 02-backend-modules, png]
----
include::images/puml/02-backend-modules.puml[]
----

==== Übersicht der Module

[cols="2,3,3,2", options="header"]
|===
| Modul | Verantwortlichkeit | Zentrale Entitäten | Abhängigkeiten

| *Stammdaten*
| Verwaltung von Basisentitäten
| Verein, Team, Kind, Offizieller
| - (keine)

| *Saisonplanung*
| Planung von Saison und Wettkämpfen
| Saison, Figur, Wettkampf, Schwimmbad
| - (keine)

| *Anmeldung*
| Wettkampfanmeldung und Startnummernvergabe
| Anmeldung
| Stammdaten, Saisonplanung
|===
```

---

## Beispiel mit Sub-Includes: `08-querschnittliche-konzepte.adoc`

```asciidoc
== Querschnittliche Konzepte

// 8.1 Domänenmodell
include::08-querschnittliche-konzepte/08-01-domaenenmodell.adoc[leveloffset=+1]

// 8.2 Persistenz
include::08-querschnittliche-konzepte/08-02-persistenz.adoc[leveloffset=+1]

// 8.3 Transaktionssteuerung
include::08-querschnittliche-konzepte/08-03-transaktionssteuerung.adoc[leveloffset=+1]

// ... weitere Unterkapitel
```

---

## PlantUML-Integration

### Inline PlantUML (empfohlen)

```asciidoc
[plantuml, system-context, svg]
----
@startuml
!include https://raw.githubusercontent.com/plantuml-stdlib/C4-PlantUML/master/C4_Context.puml

Person(user, "Benutzer")
System(aquarius, "Aquarius")
System_Ext(turso, "Turso DB")

Rel(user, aquarius, "Nutzt")
Rel(aquarius, turso, "Speichert Daten")
@enduml
----
```

### Include externe .puml-Datei

```asciidoc
[plantuml, entity-model, png]
----
include::images/puml/06-entity-relationship.puml[]
----
```

### Generierte Bilder einbinden

```asciidoc
image::generated/01-system-overview.png[System Overview, 600]
```

---

## Migrationsstrategie

### Phase 1: Struktur aufbauen

1. ✅ `docs/architecture.adoc` erstellen (Hauptdokument)
2. ✅ Kapitel-Dateien erstellen (`01-einfuehrung.adoc`, etc.)
3. ✅ `images/puml/` verschieben (bereits vorhanden)
4. ✅ Bilder-Verzeichnis umstrukturieren

### Phase 2: Content migrieren (Kapitel für Kapitel)

1. Markdown → AsciiDoc konvertieren:
```bash
pandoc -f markdown -t asciidoc \
  docs/architecture/arc42-aquarius.md \
  -o docs/architecture/temp.adoc
```

2. Manuell aufteilen in Kapitel
3. PlantUML-Referenzen anpassen
4. Testen mit `asciidoctor`

### Phase 3: Tooling einrichten

```bash
# Installation
gem install asciidoctor asciidoctor-diagram asciidoctor-pdf

# HTML generieren
asciidoctor docs/architecture.adoc -o docs/architecture.html

# PDF generieren
asciidoctor-pdf docs/architecture.adoc -o docs/architecture.pdf

# PlantUML-Diagramme generieren
asciidoctor -r asciidoctor-diagram docs/architecture.adoc
```

### Phase 4: CI/CD Integration

```yaml
# .github/workflows/docs.yml
name: Generate Documentation

on:
  push:
    paths:
      - 'docs/**'

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - name: Install AsciiDoctor
        run: |
          gem install asciidoctor asciidoctor-diagram asciidoctor-pdf
          sudo apt-get install -y graphviz plantuml

      - name: Generate HTML
        run: asciidoctor docs/architecture.adoc -o dist/architecture.html

      - name: Generate PDF
        run: asciidoctor-pdf docs/architecture.adoc -o dist/architecture.pdf

      - name: Deploy to GitHub Pages
        uses: peaceiris/actions-gh-pages@v3
        with:
          github_token: ${{ secrets.GITHUB_TOKEN }}
          publish_dir: ./dist
```

---

## Vorteile der Migration

| Feature | Markdown | AsciiDoc |
|---------|----------|----------|
| **Includes** | ❌ Manuell mit Links | ✅ Native `include::` |
| **PlantUML** | ⚠️ Externe Dateien | ✅ Inline + Include |
| **PDF-Export** | ⚠️ Pandoc (limitiert) | ✅ asciidoctor-pdf (professionell) |
| **Tabellen** | ⚠️ Basic | ✅ Erweitert (colspan, rowspan) |
| **Admonitions** | ❌ | ✅ NOTE, TIP, WARNING, etc. |
| **Versionierung** | ⚠️ Eine große Datei | ✅ Kapitel einzeln versionierbar |
| **arc42-Standard** | ❌ | ✅ Offizielle Templates |

---

## Makefile-Targets

```makefile
# Makefile
.PHONY: docs docs-html docs-pdf docs-watch

docs: docs-html docs-pdf

docs-html:
	@echo "Generating HTML documentation..."
	asciidoctor docs/architecture.adoc -o docs/architecture.html

docs-pdf:
	@echo "Generating PDF documentation..."
	asciidoctor-pdf docs/architecture.adoc -o docs/architecture.pdf

docs-watch:
	@echo "Watching docs for changes..."
	find docs -name '*.adoc' | entr make docs-html

docs-serve:
	@echo "Serving docs on http://localhost:8000"
	python3 -m http.server 8000 -d docs/
```

---

## Entscheidung

**Option A: Vollständige Migration** (empfohlen)
- Alle Kapitel nach AsciiDoc migrieren
- PlantUML inline einbinden
- PDF-Generierung einrichten
- CI/CD für automatische Generierung

**Option B: Hybrid-Ansatz**
- Hauptdokument in AsciiDoc
- Einige Kapitel bleiben Markdown
- Schrittweise Migration

**Option C: Status Quo beibehalten**
- Markdown mit separaten PlantUML-Dateien
- Kein PDF-Export
- Manuelle Verwaltung

**Empfehlung:** **Option A** für beste Wartbarkeit und professionelle Dokumentation.

---

## Nächste Schritte

1. ☐ Entscheidung für Migration (A, B, oder C)
2. ☐ AsciiDoc-Tooling installieren (`gem install asciidoctor`)
3. ☐ Hauptdokument `docs/architecture.adoc` erstellen
4. ☐ Kapitel 1-3 migrieren (Test)
5. ☐ PlantUML-Integration testen
6. ☐ Restliche Kapitel migrieren
7. ☐ Makefile-Targets für `make docs` erstellen
8. ☐ CI/CD konfigurieren

---

## Referenzen

- [AsciiDoc Syntax Quick Reference](https://docs.asciidoctor.org/asciidoc/latest/syntax-quick-reference/)
- [arc42 AsciiDoc Templates](https://arc42.org/download)
- [asciidoctor-diagram](https://docs.asciidoctor.org/diagram-extension/latest/)
- [Pandoc Markdown → AsciiDoc](https://pandoc.org/MANUAL.html)

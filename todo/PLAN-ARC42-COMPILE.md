# Plan: arc42-Dokumentation für Jekyll kompilieren

## Ausgangslage

```
/documentation/architecture/
├── 01-einfuehrung-ziele.adoc
├── 02-randbedingungen.adoc
├── 03-kontextabgrenzung.adoc
├── 04-loesungsstrategie.adoc
├── 05-bausteinsicht.adoc
├── 08-querschnittliche-konzepte.adoc
├── 08-4-cloud-deployment.adoc
├── 08-CAP-device-binding.adoc
├── 08-fly-io-concept-proposal-gemini.adoc
├── 09-architekturentscheidungen.adoc
├── 09-user-management-admin-concept.adoc
└── images/puml/*.puml (9 Diagramme)
```

**Aktuell:** `make docs` (in `/documentation/`) erzeugt HTML in `build/`
**Ziel:** Integration in Jekyll unter `/architecture/arc42/`

---

## Option A: AsciiDoc → HTML-Fragment → Jekyll (Empfohlen)

### Ablauf
```
AsciiDoc (Source)     →  HTML-Fragment      →  Jekyll Page
01-einfuehrung.adoc   →  01-einfuehrung.html →  /architecture/arc42/01/
```

### Umsetzung

1. **Neues Script:** `docs/scripts/compile-arc42.sh`
   - Verwendet `asciidoctor` im Docker-Container
   - Erzeugt HTML-Fragmente (ohne `<html>`, `<head>`, etc.)
   - Fügt Jekyll Front Matter hinzu
   - Output: `docs/_arc42/*.html`

2. **Docker-Service:** `compile-arc42` in `docs/docker-compose.yml`
   ```yaml
   compile-arc42:
     image: asciidoctor/docker-asciidoctor
     volumes:
       - ../documentation/architecture:/source:ro
       - ./_arc42:/output
       - ./scripts:/scripts:ro
     command: ["sh", "/scripts/compile-arc42.sh"]
   ```

3. **Jekyll-Collection:** `_arc42` in `_config.yml`
   ```yaml
   collections:
     arc42:
       output: true
       permalink: /architecture/arc42/:name/
   ```

4. **Makefile:** `website-compile` erweitern
   ```makefile
   website-compile:
     @mkdir -p docs/_adrs docs/_arc42
     @cd docs && docker compose run --rm compile-adrs
     @cd docs && docker compose run --rm compile-arc42
   ```

5. **Bilder:** PlantUML → SVG
   - Option 1: Vorher manuell generieren, in Git committen
   - Option 2: Bei compile-arc42 mit generieren (PlantUML-Server)

### Vorteile
- ✅ Bewährtes Muster (wie ADRs)
- ✅ Source of Truth bleibt `/documentation/`
- ✅ Volle AsciiDoc-Features (Tabellen, Admonitions, etc.)
- ✅ Funktioniert mit GitHub Pages

### Nachteile
- ⚠️ Zusätzlicher Docker-Container (asciidoctor)
- ⚠️ PlantUML-Bilder brauchen Extra-Handling

---

## Option B: jekyll-asciidoc Plugin

### Umsetzung
- AsciiDoc-Dateien direkt in `docs/_arc42/` kopieren
- Jekyll-Plugin `jekyll-asciidoc` parst sie

### Vorteile
- ✅ Kein Konvertierungsschritt

### Nachteile
- ❌ Funktioniert NICHT mit GitHub Pages (unsupported plugin)
- ❌ Lokaler Build weicht von Production ab
- ❌ CI/CD muss Jekyll selbst bauen (kein `github-pages` gem)

**→ Nicht empfohlen**

---

## Option C: AsciiDoc → Markdown (Pandoc)

### Umsetzung
- `pandoc` oder `kramdoc` für Konvertierung
- Output: Markdown-Dateien für Jekyll

### Vorteile
- ✅ Native Jekyll-Unterstützung

### Nachteile
- ❌ Verlust von AsciiDoc-Features (komplexe Tabellen, Admonitions)
- ❌ Manuelle Nacharbeit nötig
- ❌ Bilder/Includes funktionieren anders

**→ Nicht empfohlen**

---

## Empfehlung: Option A

### Dateien zu erstellen/ändern

| Datei | Aktion |
|-------|--------|
| `docs/scripts/compile-arc42.sh` | Neu |
| `docs/docker-compose.yml` | Service hinzufügen |
| `docs/_config.yml` | Collection hinzufügen |
| `Makefile` | `website-compile` erweitern |
| `docs/_pages/architecture/arc42.md` | Index-Seite mit Kapitel-Links |
| `.gitignore` | `_arc42` hinzufügen |

### Offene Fragen

1. **Kapitel-Struktur:**
   - Alle Kapitel einzeln?
   - Oder ein großes Dokument?

2. **PlantUML-Diagramme:**
   - Vorher generieren und committen?
   - Oder bei jedem Build generieren?

3. **Navigation:**
   - Inhaltsverzeichnis auf arc42-Seite?
   - Vor-/Zurück-Navigation zwischen Kapiteln?

4. **Geschützter Bereich:**
   - arc42 auch hinter Passwort (`layout: protected`)?

---

## Nächste Schritte (nach Freigabe)

1. `compile-arc42.sh` Script erstellen
2. Docker-Service hinzufügen
3. Jekyll-Collection konfigurieren
4. Makefile erweitern
5. arc42-Index-Seite erstellen
6. Testen mit `make website-dev`

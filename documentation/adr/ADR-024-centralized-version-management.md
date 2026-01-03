# ADR-024: Centralized Version Management

**Status:** Akzeptiert
**Datum:** 2026-01-03
**Entscheider:** Gernot Starke

## Kontext

Aquarius besteht aus mehreren unabhängig deployten Komponenten (Backend API und Mobile App). Bisher waren Versionsnummern an mehreren Stellen im Code hardcodiert, was bei Releases zu Inkonsistenzen und vergessenen Updates führen kann.

Wir benötigen eine zentrale Stelle zur Versionsverwaltung, die:
- Einfach zu finden und zu aktualisieren ist
- Keine Duplikation erfordert
- Mit bestehenden Tools und Workflows kompatibel ist
- Die unabhängige Versionierung von Backend und Mobile ermöglicht

## Entscheidung

Wir führen **zwei separate Versionskonstanten** ein, jeweils in einer dedizierten Datei innerhalb der jeweiligen Anwendung:

### Backend Version
**Datei:** `/web/backend/app/version.py`
```python
AQUARIUS_BACKEND_VERSION = "0.1.0"
```

**Verwendung:**
```python
from app.version import AQUARIUS_BACKEND_VERSION

app = FastAPI(version=AQUARIUS_BACKEND_VERSION)
```

### Mobile Version
**Datei:** `/mobile/src/version.ts`
```typescript
export const AQUARIUS_MOBILE_VERSION = "1.0.0";
```

**Verwendung:**
```typescript
import { AQUARIUS_MOBILE_VERSION } from './version';
```

## Begründung

### Warum separate Dateien statt einer zentralen Datei?

1. **Unabhängige Deployments:** Backend und Mobile werden separat deployed und haben unterschiedliche Release-Zyklen
2. **Keine Cross-Dependencies:** Backend muss nicht TypeScript-Dateien lesen und umgekehrt
3. **Standard-Praktiken:** Jede Anwendung folgt ihren Ökosystem-Konventionen (Python: `__version__.py`/`version.py`, JS/TS: `version.ts` oder `package.json`)
4. **Build-Tool-Kompatibilität:** Keine speziellen Build-Steps zum Lesen externer Dateien nötig

### Warum nicht in Konfigurationsdateien?

- `fly.toml`: Deployment-spezifisch, nicht für Anwendungslogik
- `package.json`: Nur für npm-Metadaten, nicht für Runtime-Code
- Environment Variables: Zu viele Deployment-Umgebungen, fehleranfällig

### Alternativen (verworfen)

**❌ Root-Level `/VERSION` Datei:**
- Benötigt File-I/O zur Laufzeit
- Kompliziert Deployment (Datei muss mitgepackt werden)
- Keine Type-Safety

**❌ Git Tags:**
- Nicht zur Laufzeit verfügbar
- Erfordert CI/CD-Integration zum Einfügen

**❌ Monorepo-weite Versionierung:**
- Backend und Mobile haben unterschiedliche Release-Zyklen
- Unnötige Versionsnummern-Sprünge bei Updates nur einer Komponente

## Konsequenzen

### Positiv ✅

- **Single Source of Truth:** Pro Komponente genau eine Stelle zum Aktualisieren
- **Type-Safe:** Konstanten sind typisiert und können nicht zur Laufzeit fehlen
- **IDE-Support:** Autocomplete und "Find Usages" funktionieren
- **Git-Verfolgbar:** Änderungen sind im Commit-Log sichtbar
- **Kein Build-Overhead:** Keine speziellen Tools oder Scripts nötig
- **Testbar:** Versionsnummern können in Tests überprüft werden

### Neutral ⚖️

- **Zwei Dateien:** Separate Wartung, aber das ist gewollt
- **Manuelle Updates:** Versionsbump muss bewusst durchgeführt werden (könnte mit Git Hooks/CI automatisiert werden)

### Negativ ❌

- **Kein automatisches Semver-Management:** Entwickler müssen Semantic Versioning selbst einhalten
- **Potenzielle Vergesslichkeit:** Bei Releases muss daran gedacht werden, die Version zu erhöhen

### Mitigationen

- **Pre-Commit Hooks:** Könnten prüfen, ob Version bei Code-Änderungen erhöht wurde
- **CI/CD Checks:** Release-Pipeline kann validieren, dass Version aktualisiert wurde
- **Release-Checkliste:** Standard-Prozess dokumentieren

## Implementierung

### Backend
1. ✅ Datei `/web/backend/app/version.py` erstellt
2. ✅ Import in `app/main.py` hinzugefügt
3. ✅ Alle hardcodierten `"0.1.0"` durch `AQUARIUS_BACKEND_VERSION` ersetzt

### Mobile
1. ✅ Datei `/mobile/src/version.ts` erstellt
2. ⏳ Import in relevanten Komponenten (bei Bedarf)
3. ⏳ Display in App-Info-Screen (zukünftig)

## Verwandte Entscheidungen

- ADR-008: Monorepo-Struktur - Begründet separate Versionierung
- ADR-014: Python FastAPI Backend
- ADR-016: PWA Architecture

## Referenzen

- [Python Packaging: Single-sourcing the version](https://packaging.python.org/en/latest/guides/single-sourcing-package-version/)
- [Semantic Versioning 2.0.0](https://semver.org/)

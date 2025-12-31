# ADR-012: Act für lokale GitHub Actions Ausführung

**Status:** Rejected
**Datum:** 2025-12-31
**Kontext:** Lokale CI/CD-Pipeline-Ausführung
**Entscheider:** Gernot

---

## Kontext und Problem

Aquarius nutzt GitHub Actions für CI/CD:
- Linting (Ruff, ESLint)
- Tests (Pytest, Vitest)
- Builds (Docker Images)
- Deployment (Production)

**Probleme mit Cloud-CI:**
1. **Feedback-Loop langsam**
2. **Debugging schwierig**: Kein direkter Zugriff auf CI-Umgebung
3. **"Works locally, fails in CI"**: Unterschiedliche Umgebungen

**Anforderungen:**
1. GitHub Actions **lokal ausführen** ohne Push
2. **Gleiche Umgebung** wie in GitHub Actions

---

## Entscheidung

**[Act](https://github.com/nektos/act)** aktuell nicht benötigt, weil primär lokale Entwicklung.

Aktuell läuft einzige der jekyll-build auf GitHub Action, und den können wir lokal ausreichend testen.


## Vorteile

| Vorteil | Beschreibung |
|---------|--------------|
| **Schnelles Feedback** | 2-3 Min statt 5-10 Min |
| **Kostenersparnis** | Weniger CI-Minuten verbraucht |
| **Debugging** | Interaktiver Zugriff auf Container |
| **Offline-Fähig** | Arbeiten ohne Internet (nach initialem Pull) |
| **Konsistenz** | Gleiche Workflows lokal und Cloud |

---

## Nachteile & Limitierungen

| Nachteil | Mitigation |
|----------|------------|
| **Setup-Aufwand** | Optional: Nicht jeder muss Act nutzen |
| **Docker erforderlich** | Bereits für Dev-Environment vorhanden |
| **Nicht 100% kompatibel** | GitHub-spezifische Features im echten CI testen |


**Zusammenhang mit anderen ADRs:**
- [ADR-010: Makefile](ADR-010-makefile-build-interface.md) - Act führt `make` Commands aus
- [ADR-011: Docker](ADR-011-docker-development.md) - Act nutzt Docker für Container

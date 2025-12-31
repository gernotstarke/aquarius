# ADR-012: Act für lokale GitHub Actions Ausführung

**Status:** Vorgeschlagen.
**Datum:** 2025-12-17
**Kontext:** Lokale CI/CD-Pipeline-Ausführung
**Entscheider:** Architekt, Team

---

## Kontext und Problem

Aquarius nutzt GitHub Actions für CI/CD:
- Linting (Ruff, ESLint)
- Tests (Pytest, Vitest)
- Builds (Docker Images)
- Deployment (Production)

**Probleme mit Cloud-CI:**
1. **Feedback-Loop langsam**: Push → warten 2-5 Min → Fehler → Fix → Push → ...
2. **CI-Minuten kosten Geld** bei vielen Entwicklern/Commits
3. **Debugging schwierig**: Kein direkter Zugriff auf CI-Umgebung
4. **"Works locally, fails in CI"**: Unterschiedliche Umgebungen

**Anforderungen:**
1. GitHub Actions **lokal ausführen** ohne Push
2. **Gleiche Umgebung** wie in GitHub Actions
3. **Schnelles Feedback** (Sekunden statt Minuten)
4. **Optional**: Nicht jeder muss es nutzen (für Git-Puristen)

---

## Entscheidung

Wir verwenden **[Act](https://github.com/nektos/act)** für lokale GitHub Actions Ausführung.

**Prinzip:** "Test your CI/CD pipeline locally before pushing"

```bash
# Statt: git push → warten → Fehler sehen
# Jetzt: act → Fehler lokal → fixen → act → erfolgreich → git push
```

**Architektur:**

```
┌────────────────────────────────────────┐
│  Developer Laptop                       │
│                                         │
│  ┌──────────────────────────────────┐  │
│  │  act (CLI Tool)                  │  │
│  │  - Liest .github/workflows/*.yml │  │
│  │  - Startet Docker Container      │  │
│  │  - Führt Jobs aus                │  │
│  └──────────┬───────────────────────┘  │
│             │                           │
│  ┌──────────▼───────────────────────┐  │
│  │  Docker Container                │  │
│  │  (nektos/act-environments)       │  │
│  │  - Ubuntu 22.04                  │  │
│  │  - Git, Node, Python             │  │
│  │  - Actions Runner                │  │
│  │                                  │  │
│  │  Führt aus:                      │  │
│  │  1. make lint                    │  │
│  │  2. make test                    │  │
│  │  3. make build                   │  │
│  └──────────────────────────────────┘  │
└────────────────────────────────────────┘
```

---

## Installation

### 1. Act installieren

**macOS:**
```bash
brew install act
```

**Linux:**
```bash
curl https://raw.githubusercontent.com/nektos/act/master/install.sh | sudo bash
```

**Windows (WSL):**
```bash
curl https://raw.githubusercontent.com/nektos/act/master/install.sh | bash
```

### 2. Docker muss laufen

```bash
docker --version  # Check
```

Act nutzt Docker im Hintergrund (wie bei Docker Compose).

---

## Verwendung

### Basis-Commands

```bash
# Alle Workflows ausführen
act

# Nur bestimmten Event (z.B. push)
act push

# Nur bestimmten Job
act -j test

# Nur bestimmten Workflow
act -W .github/workflows/ci.yml

# Dry-Run (zeigt was passieren würde)
act --dryrun

# Liste aller Jobs
act --list
```

### Aquarius-Workflow

```bash
# CI-Pipeline lokal testen
act push

# Nur Tests
act -j test

# Mit Secrets (falls benötigt)
act --secret-file .secrets

# Mit Custom Image (schneller)
act --container-architecture linux/amd64 \
    -P ubuntu-latest=catthehacker/ubuntu:act-latest
```

---

## GitHub Actions Workflow

### .github/workflows/ci.yml

```yaml
name: CI

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main ]

jobs:
  # ============================================
  # Lint
  # ============================================
  lint:
    name: Lint Code
    runs-on: ubuntu-latest

    steps:
      - name: Checkout Code
        uses: actions/checkout@v4

      - name: Run Linters
        run: make lint

  # ============================================
  # Type Check
  # ============================================
  type-check:
    name: Type Check
    runs-on: ubuntu-latest

    steps:
      - name: Checkout Code
        uses: actions/checkout@v4

      - name: Run Type Checkers
        run: make type-check

  # ============================================
  # Test
  # ============================================
  test:
    name: Run Tests
    runs-on: ubuntu-latest

    steps:
      - name: Checkout Code
        uses: actions/checkout@v4

      - name: Run Tests
        run: make test

      - name: Upload Coverage
        if: always()
        uses: codecov/codecov-action@v3
        with:
          files: ./backend/coverage.xml,./frontend/coverage/coverage-final.json

  # ============================================
  # Build
  # ============================================
  build:
    name: Build Production Images
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main'

    steps:
      - name: Checkout Code
        uses: actions/checkout@v4

      - name: Build Images
        run: make build

      - name: Push to Registry
        if: github.event_name == 'push'
        run: |
          echo "${{ secrets.DOCKER_PASSWORD }}" | docker login -u "${{ secrets.DOCKER_USERNAME }}" --password-stdin
          docker-compose push
```

**Wichtig:** Workflow nutzt `make` Commands → Act kann diese lokal ausführen!

---

## Lokale Ausführung mit Act

### 1. Einfacher Test

```bash
# Alle Jobs ausführen
act push

# Output:
# [CI/lint] 🚀  Start image=catthehacker/ubuntu:act-latest
# [CI/lint]   🐳  docker pull image=catthehacker/ubuntu:act-latest
# [CI/lint]   🐳  docker create image=catthehacker/ubuntu:act-latest
# [CI/lint] ⭐  Run Checkout Code
# [CI/lint] ⭐  Run make lint
# [CI/lint]   ✅  Success - make lint
# [CI/lint] Cleaning up container
```

### 2. Nur ein Job

```bash
# Nur Linting
act -j lint

# Nur Tests
act -j test
```

### 3. Mit Secrets

```bash
# .secrets Datei erstellen (nicht in Git!)
echo "DOCKER_USERNAME=myuser" >> .secrets
echo "DOCKER_PASSWORD=mypass" >> .secrets

# Act mit Secrets
act push --secret-file .secrets
```

### 4. Interaktiver Modus (Debugging)

```bash
# Shell in Container öffnen bei Fehler
act --interactive
```

---

## Konfiguration

### .actrc - Act Config

```bash
# .actrc (im Projekt-Root)
-P ubuntu-latest=catthehacker/ubuntu:act-latest
--container-architecture linux/amd64
--artifact-server-path /tmp/act-artifacts
```

**Vorteile:**
- Schnelleres Image (bereits Docker, Node, Python installiert)
- Konsistente Konfiguration für Team
- Keine langen Command-Line-Args

### Makefile-Integration

```makefile
# Makefile
.PHONY: ci-local
ci-local: ## Run CI pipeline locally with act
	act push

.PHONY: ci-local-job
ci-local-job: ## Run specific CI job (usage: make ci-local-job job=test)
	@if [ -z "$(job)" ]; then \
		echo "Error: Specify job, e.g.: make ci-local-job job=test"; \
		exit 1; \
	fi
	act -j $(job)
```

**Nutzung:**
```bash
make ci-local           # Alle Jobs
make ci-local-job job=test  # Nur Test-Job
```

---

## Unterschiede: Act vs. GitHub Actions

### Kompatibilität

| Feature | Act Support | Anmerkung |
|---------|-------------|-----------|
| **Basic Workflows** | ✅ Vollständig | `on`, `jobs`, `steps`, `run` |
| **Actions (uses:)** | ✅ Meiste | Populäre Actions funktionieren |
| **Secrets** | ✅ Mit `--secret-file` | Manuell bereitstellen |
| **Artifacts** | ⚠️ Begrenzt | `--artifact-server-path` |
| **Matrix Builds** | ✅ Ja | Mehrere Versionen parallel |
| **Services** | ⚠️ Eingeschränkt | Docker-in-Docker-Probleme |
| **GitHub Context** | ⚠️ Simuliert | `github.sha` etc. sind Dummy-Werte |

### Nicht unterstützt

❌ **GitHub-spezifische Features:**
- `github.event.pull_request` (nur bei echten PRs)
- GitHub Packages Registry (lokal nicht vorhanden)
- Branch Protection Rules
- Code Scanning / Security Alerts

**Workaround:** Diese Features nur in echtem CI testen.

---

## Performance-Vergleich

| Metrik | GitHub Actions | Act (lokal) |
|--------|---------------|-------------|
| **Setup-Zeit** | 1-2 Min (Cold Start) | 10-30 Sek (Docker Pull) |
| **Job-Ausführung** | 2-5 Min | 1-3 Min |
| **Feedback-Loop** | 5-10 Min (mit Queue) | 2-5 Min (sofort) |
| **Kosten** | CI-Minuten (€) | Lokal (Strom 😄) |
| **Parallelität** | Max. 20 Jobs | Begrenzt durch CPU |

**Fazit:** Act ist 2-3x schneller für Feedback-Loops.

---

## Best Practices

### 1. Workflow-Design für Act

```yaml
# ✅ RICHTIG: Verwende make Commands
- name: Run Tests
  run: make test

# ❌ FALSCH: Viele Inline-Commands
- name: Run Tests
  run: |
    cd backend
    pip install -r requirements.txt
    pytest tests/
```

**Warum?** `make test` funktioniert lokal und in Act identisch.

### 2. Conditional Steps für GitHub

```yaml
# Nur in GitHub Actions ausführen
- name: Upload to Codecov
  if: ${{ !env.ACT }}  # ACT=true bei act
  uses: codecov/codecov-action@v3
```

### 3. Secrets Management

```bash
# .secrets (nicht in Git!)
DOCKER_USERNAME=user
DOCKER_PASSWORD=pass

# .gitignore
.secrets
```

### 4. Fast Feedback mit act

```bash
# Vor Commit:
make lint      # Schnell (lokal)
act -j test    # Mittel (Docker)
git commit

# Nach Push:
# GitHub Actions läuft (langsam, aber vollständig)
```

---

## Troubleshooting

### Problem: "Error: Cannot connect to Docker"

```bash
# Symptom: act: error during connect: ... docker daemon

# Lösung: Docker starten
docker ps  # Check ob Docker läuft
```

### Problem: Workflow findet Dateien nicht

```bash
# Symptom: make: *** No rule to make target 'test'

# Ursache: Checkout-Action läuft nicht korrekt

# Lösung: Explizit Checkout hinzufügen
steps:
  - uses: actions/checkout@v4  # Wichtig!
  - run: make test
```

### Problem: Langsam bei erstem Start

```bash
# Symptom: Docker Pull dauert 5-10 Minuten

# Lösung: Kleineres Image verwenden
# .actrc
-P ubuntu-latest=catthehacker/ubuntu:act-latest

# Einmalig Pull:
docker pull catthehacker/ubuntu:act-latest
```

### Problem: Secrets fehlen

```bash
# Symptom: Error: required secret not provided

# Lösung: .secrets Datei erstellen
echo "MY_SECRET=value" >> .secrets
act --secret-file .secrets
```

---

## Integration in Entwickler-Workflow

### Workflow 1: Pre-Commit Check

```bash
# Vor jedem Commit
make lint              # Lokal (Sekunden)
act -j test            # Act (2-3 Min)

# Wenn erfolgreich:
git commit -m "..."
git push

# GitHub Actions läuft als finale Absicherung
```

### Workflow 2: Pull Request Vorbereitung

```bash
# Vor PR erstellen
act push               # Alle Jobs lokal

# Wenn erfolgreich:
git push origin feature-branch
gh pr create           # GitHub Actions läuft automatisch
```

### Workflow 3: Debugging fehlgeschlagener CI

```bash
# CI in GitHub ist fehlgeschlagen

# Lokal reproduzieren:
act push

# Interaktiver Debug-Modus:
act --interactive

# In Container:
# → Logs anschauen
# → Commands manuell ausführen
# → Fix finden
```

---

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
| **Disk-Space** | Docker-Images (~1-2 GB), regelmäßig `docker system prune` |

---

## Alternativen

| Alternative | Pro | Contra |
|-------------|-----|--------|
| **GitLab CI (lokal)** | Offizielle CLI | Nur für GitLab |
| **Drone CI** | Selbst-gehostet | Setup-Aufwand hoch |
| **CircleCI CLI** | Offiziell | Nur für CircleCI |
| **Gar keine lokale CI** | Einfach | Langsame Feedback-Loops |

**Entscheidung:** Act ist die beste Option für GitHub Actions Projekte.

---

## Konsequenzen

### Positiv ✅

- **Entwickler-Produktivität:** Schnelleres Feedback
- **CI-Kosten:** Weniger GitHub Actions Minutes
- **Debugging:** Einfacher bei CI-Problemen
- **Qualität:** Weniger "Quick Fixes" Commits

### Negativ ⚠️

- **Optional Tool:** Team muss Act lernen (oder nicht nutzen)
- **Nicht perfekt:** Kleine Unterschiede zu echtem GitHub Actions
- **Disk-Space:** Weitere Docker-Images

### Neutral ℹ️

- **Adoption:** Entwickler können selbst entscheiden (Make bleibt primär)
- **Maintenance:** `.github/workflows/*.yml` müssen Act-kompatibel bleiben

---

## Offene Fragen

- [ ] Sollten wir Act als Pflicht-Tool etablieren oder optional lassen?
- [ ] Brauchen wir Pre-Commit Hooks mit `act -j lint`?
- [ ] Sollen wir ein Custom Docker-Image für Act bauen (mit Dependencies vorinstalliert)?

---

## Referenzen

- [Act GitHub Repository](https://github.com/nektos/act)
- [Act Documentation](https://nektosact.com/)
- [GitHub Actions Syntax](https://docs.github.com/en/actions/reference/workflow-syntax-for-github-actions)
- [catthehacker/ubuntu Images](https://github.com/catthehacker/docker_images)

---

## Quick Reference

```bash
# Installation
brew install act  # macOS
curl ... | bash   # Linux

# Grundlagen
act                    # Alle Workflows
act push              # Push-Event
act -j test           # Nur Test-Job
act --list            # Alle Jobs anzeigen

# Mit Secrets
act --secret-file .secrets

# Debugging
act --dryrun          # Zeigt was passieren würde
act --interactive     # Shell bei Fehler
act -v                # Verbose Output

# Makefile-Integration
make ci-local         # Über Makefile

# Konfiguration
# .actrc erstellen mit:
-P ubuntu-latest=catthehacker/ubuntu:act-latest
```

---

**Zusammenhang mit anderen ADRs:**
- [ADR-010: Makefile](ADR-010-makefile-build-interface.md) - Act führt `make` Commands aus
- [ADR-011: Docker](ADR-011-docker-development.md) - Act nutzt Docker für Container

# ADR-010: Makefile als Build-Interface

**Status:** Accepted
**Datum:** 2025-12-17
**Kontext:** CI/CD-Automatisierung für Aquarius
**Entscheider:** Architekt, Team

---

## Kontext und Problem

Entwickler müssen verschiedene Build-, Test- und Deployment-Tasks ausführen:
- Linting (Backend: Ruff, Frontend: ESLint)
- Tests (Pytest, Vitest)
- Builds (Docker Images, Frontend Bundle)
- Entwicklungs-Server starten

**Probleme ohne einheitliches Interface:**
- Jeder Entwickler muss Commands kennen (`docker-compose run ...`, `npm run ...`, `pytest ...`)
- Unterschiedliche Ausführung lokal vs. CI
- Lange, fehleranfällige Commands
- Keine Konsistenz

**Anforderungen:**
1. Einheitliche Commands für alle Tasks
2. Einfach zu merken (`make lint`, `make test`)
3. Gleiche Commands lokal und in CI
4. Selbst-dokumentierend
5. Kein Vendor-Lock-in (unabhängig von GitHub Actions, GitLab CI, etc.)

---

## Entscheidung

Wir verwenden ein **Makefile** als zentrale Build-Interface.

**Prinzip:** Alle Build-Tasks laufen über `make <target>`

```makefile
# Entwickler lernt nur:
make help      # Was kann ich tun?
make dev       # Entwicklung starten
make lint      # Code prüfen
make test      # Tests ausführen
make build     # Production Build
```

**Vorteile:**
- ✅ **Einfach**: `make <command>` statt komplexe Docker/npm Commands
- ✅ **Plattform-unabhängig**: Make auf Linux/Mac/Windows (WSL) verfügbar
- ✅ **CI-Integration**: GitHub Actions, GitLab CI können `make` nutzen
- ✅ **Selbst-dokumentierend**: `make help` zeigt alle Commands
- ✅ **Abstraktion**: Implementation-Details versteckt (Docker, npm, etc.)

---

## Implementierung

### Makefile-Struktur

```makefile
# ============================================
# Aquarius - Makefile
# ============================================

# Default target: help
.DEFAULT_GOAL := help

# ============================================
# Help
# ============================================
.PHONY: help
help: ## Show this help message
	@echo "Aquarius Development Commands"
	@echo ""
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | \
		awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-20s\033[0m %s\n", $$1, $$2}'
	@echo ""

# ============================================
# Development
# ============================================
.PHONY: dev
dev: ## Start development environment (Backend + Frontend + DB)
	docker-compose -f docker-compose.yml -f docker-compose.dev.yml up

.PHONY: dev-detached
dev-detached: ## Start development environment in background
	docker-compose -f docker-compose.yml -f docker-compose.dev.yml up -d

.PHONY: logs
logs: ## Show logs from running containers
	docker-compose logs -f

.PHONY: stop
stop: ## Stop development environment
	docker-compose down

# ============================================
# Code Quality
# ============================================
.PHONY: lint
lint: lint-backend lint-frontend ## Run all linters

.PHONY: lint-backend
lint-backend: ## Lint backend code (Ruff)
	@echo "→ Linting Backend..."
	docker-compose run --rm backend-lint

.PHONY: lint-frontend
lint-frontend: ## Lint frontend code (ESLint + Prettier)
	@echo "→ Linting Frontend..."
	docker-compose run --rm frontend-lint

.PHONY: format
format: format-backend format-frontend ## Format all code

.PHONY: format-backend
format-backend: ## Format backend code (Ruff)
	@echo "→ Formatting Backend..."
	docker-compose run --rm backend sh -c "ruff format ."

.PHONY: format-frontend
format-frontend: ## Format frontend code (Prettier)
	@echo "→ Formatting Frontend..."
	docker-compose run --rm frontend sh -c "npm run format"

.PHONY: type-check
type-check: type-check-backend type-check-frontend ## Run type checkers

.PHONY: type-check-backend
type-check-backend: ## Type check backend (mypy)
	@echo "→ Type checking Backend..."
	docker-compose run --rm backend sh -c "mypy app"

.PHONY: type-check-frontend
type-check-frontend: ## Type check frontend (tsc)
	@echo "→ Type checking Frontend..."
	docker-compose run --rm frontend sh -c "npm run type-check"

# ============================================
# Testing
# ============================================
.PHONY: test
test: test-backend test-frontend ## Run all tests

.PHONY: test-backend
test-backend: ## Run backend tests (Pytest)
	@echo "→ Testing Backend..."
	docker-compose run --rm backend-test

.PHONY: test-frontend
test-frontend: ## Run frontend tests (Vitest)
	@echo "→ Testing Frontend..."
	docker-compose run --rm frontend-test

.PHONY: test-watch
test-watch: ## Run tests in watch mode
	docker-compose run --rm backend sh -c "pytest --watch" & \
	docker-compose run --rm frontend sh -c "npm run test:watch"

.PHONY: test-coverage
test-coverage: ## Run tests with coverage report
	@echo "→ Running tests with coverage..."
	docker-compose run --rm backend-test --cov-report=html
	docker-compose run --rm frontend sh -c "npm run test:coverage"
	@echo "→ Coverage reports:"
	@echo "  Backend:  backend/htmlcov/index.html"
	@echo "  Frontend: frontend/coverage/index.html"

# ============================================
# Build
# ============================================
.PHONY: build
build: build-backend build-frontend ## Build production images

.PHONY: build-backend
build-backend: ## Build backend production image
	@echo "→ Building Backend..."
	docker-compose build backend

.PHONY: build-frontend
build-frontend: ## Build frontend production image
	@echo "→ Building Frontend..."
	docker-compose build frontend

# ============================================
# Database
# ============================================
.PHONY: db-migrate
db-migrate: ## Run database migrations
	docker-compose run --rm backend sh -c "alembic upgrade head"

.PHONY: db-migration-create
db-migration-create: ## Create new migration (usage: make db-migration-create msg="description")
	@if [ -z "$(msg)" ]; then \
		echo "Error: Please provide a message: make db-migration-create msg='your message'"; \
		exit 1; \
	fi
	docker-compose run --rm backend sh -c "alembic revision --autogenerate -m '$(msg)'"

.PHONY: db-reset
db-reset: ## Reset database (WARNING: deletes all data)
	@echo "→ Resetting database..."
	docker-compose down -v
	docker-compose up -d db
	sleep 2
	$(MAKE) db-migrate

# ============================================
# Clean
# ============================================
.PHONY: clean
clean: ## Remove containers and volumes
	docker-compose down -v

.PHONY: clean-all
clean-all: clean ## Remove containers, volumes, and images
	docker-compose down -v --rmi all

.PHONY: prune
prune: ## Remove unused Docker resources
	docker system prune -af --volumes

# ============================================
# Install
# ============================================
.PHONY: install
install: ## Install dependencies (first-time setup)
	@echo "→ Installing dependencies..."
	docker-compose build
	docker-compose run --rm backend sh -c "pip install -r requirements.txt"
	docker-compose run --rm frontend sh -c "npm ci"

# ============================================
# Shell Access
# ============================================
.PHONY: shell-backend
shell-backend: ## Open shell in backend container
	docker-compose run --rm backend sh

.PHONY: shell-frontend
shell-frontend: ## Open shell in frontend container
	docker-compose run --rm frontend sh

.PHONY: shell-db
shell-db: ## Open database shell
	docker-compose exec db sqlite3 /var/lib/sqld/data.db

# ============================================
# CI/CD
# ============================================
.PHONY: ci
ci: lint type-check test ## Run full CI pipeline (lint + type-check + test)

.PHONY: ci-fast
ci-fast: lint test ## Run fast CI pipeline (skip type-check)
```

---

## Nutzung

### Entwickler-Workflow

```bash
# 1. Erstes Setup
make install

# 2. Entwicklung starten
make dev
# → Backend: http://localhost:8000
# → Frontend: http://localhost:5173

# 3. In anderem Terminal: Code prüfen
make lint
make type-check

# 4. Tests ausführen
make test

# 5. Vor Commit: CI-Pipeline lokal
make ci

# 6. Aufräumen
make clean
```

### CI-Integration (GitHub Actions)

```yaml
# .github/workflows/ci.yml
name: CI

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - name: Run CI Pipeline
        run: make ci

      - name: Build Production
        if: github.ref == 'refs/heads/main'
        run: make build
```

**Vorteil:** CI nutzt exakt die gleichen Commands wie lokal!

---

## Design-Prinzipien

### 1. Konsistente Namensgebung

| Pattern | Beispiel | Bedeutung |
|---------|----------|-----------|
| `<action>` | `lint`, `test`, `build` | Hauptaktion |
| `<action>-<component>` | `lint-backend`, `test-frontend` | Aktion für Komponente |
| `<component>-<action>` | `db-migrate`, `shell-backend` | Komponenten-spezifisch |

### 2. Komposition über Duplikation

```makefile
# ✅ RICHTIG: Targets kombinieren
.PHONY: lint
lint: lint-backend lint-frontend

# ❌ FALSCH: Duplikation
.PHONY: lint
lint:
	docker-compose run --rm backend-lint
	docker-compose run --rm frontend-lint
```

### 3. Fail-Fast bei Fehlern

```makefile
# Makefile stoppt automatisch bei Fehler
.PHONY: ci
ci: lint type-check test  # Stoppt wenn lint fehlschlägt
```

### 4. Hilfe für Entwickler

```makefile
# Jedes Target hat Beschreibung
.PHONY: test
test: test-backend test-frontend ## Run all tests
#                                 ^^^ wird von make help angezeigt
```

---

## Vorteile

| Vorteil | Beschreibung |
|---------|--------------|
| **Einfachheit** | `make test` statt `docker-compose run --rm backend-test` |
| **Konsistenz** | Gleiche Commands lokal, CI, Produktion |
| **Dokumentation** | `make help` zeigt alle Commands |
| **Flexibilität** | Implementation austauschbar (Docker, npm, etc.) |
| **Tooling-Agnostisch** | Keine Abhängigkeit von GitHub Actions, GitLab CI |
| **Standards** | Make ist de-facto Standard in Unix-Welt |

---

## Nachteile & Alternativen

### Nachteile

| Nachteil | Mitigation |
|----------|------------|
| Make-Syntax gewöhnungsbedürftig | Gut dokumentiert, Beispiele |
| Windows-Support begrenzt | WSL, Git Bash, oder `make.exe` |
| Keine Parameter-Validierung | In Targets prüfen (siehe `db-migration-create`) |

### Alternativen

| Alternative | Pro | Contra |
|-------------|-----|--------|
| **NPM Scripts** | JavaScript-native | Nur für Frontend, nicht Backend |
| **Task (Go)** | Moderne Syntax (YAML) | Neue Dependency, weniger verbreitet |
| **Just** | Bessere Syntax als Make | Neue Dependency, weniger verbreitet |
| **Bash Scripts** | Einfach | Kein Dependency-Management, keine Hilfe |

**Entscheidung:** Make ist der beste Kompromiss aus Standardisierung und Funktionalität.

---

## Konsequenzen

### Positiv ✅

- Entwickler lernen **5 Commands** (`dev`, `lint`, `test`, `build`, `clean`)
- CI-Pipelines werden **einfacher** (nur `make ci`)
- **Onboarding** schneller (README: "Run `make help`")
- **Refactoring** einfacher (Implementations-Details versteckt)

### Negativ ⚠️

- Team muss **Make-Basics lernen** (oder nur nutzen)
- Windows-Entwickler brauchen **WSL oder Git Bash**
- **Zusätzliche Abstraktionsschicht** (könnte übertrieben sein für kleine Projekte)

### Neutral ℹ️

- Makefile muss **gepflegt** werden (wie alle Build-Scripts)
- **Neue Commands** müssen dokumentiert werden (`## comment`)

---

## Offene Fragen

- [ ] Sollten wir `make watch` für Live-Reload hinzufügen?
- [ ] Brauchen wir `make deploy` für Production-Deployment?
- [ ] Sollen wir `make doctor` für System-Checks hinzufügen (Docker installiert, etc.)?

---

## Referenzen

- [GNU Make Manual](https://www.gnu.org/software/make/manual/)
- [Makefile Best Practices](https://clarkgrubb.com/makefile-style-guide)
- [Self-Documenting Makefiles](https://www.thapaliya.com/en/writings/well-documented-makefiles/)

---

**Zusammenhang mit anderen ADRs:**
- [ADR-011: Docker & Docker Compose](ADR-011-docker-development.md) - Makefile ruft Docker Commands auf
- [ADR-012: Act für lokale CI](ADR-012-act-local-ci.md) - Makefile wird von Act genutzt

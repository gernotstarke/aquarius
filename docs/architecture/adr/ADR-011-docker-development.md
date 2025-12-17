# ADR-011: Docker & Docker Compose für Development

**Status:** Accepted
**Datum:** 2025-12-17
**Kontext:** Lokale Entwicklungsumgebung für Aquarius
**Entscheider:** Architekt, Team

---

## Kontext und Problem

Aquarius ist eine Full-Stack-Anwendung mit:
- **Backend:** Python 3.11, FastAPI, SQLAlchemy
- **Frontend:** Node.js 20, React, TypeScript, Vite
- **Datenbank:** Turso (libSQL)

**Herausforderungen:**
1. Entwickler brauchen Python 3.11, Node 20, Turso lokal installiert
2. Versionskonflikte (Python 3.8 vs 3.11, Node 18 vs 20)
3. "Works on my machine" - unterschiedliche Umgebungen
4. CI/CD-Umgebung ≠ lokale Umgebung → schwer reproduzierbare Fehler
5. Onboarding: Neue Entwickler müssen viel installieren

**Anforderungen:**
1. **Einheitliche Umgebung**: Lokal = CI = Production
2. **Einfaches Setup**: Nur Docker installieren
3. **Hot-Reload**: Code-Änderungen sofort sichtbar
4. **Isolation**: Keine Konflikte mit anderen Projekten
5. **Performance**: Schnelle Entwicklungs-Zyklen

---

## Entscheidung

Wir verwenden **Docker & Docker Compose** für die lokale Entwicklung.

**Prinzip:** "Docker-First Development"

```bash
# Setup (einmalig)
docker --version  # Check: Docker installiert?

# Start Development
make dev
# → Backend, Frontend, DB laufen in Containern
# → Code-Änderungen werden live reloaded
```

**Architektur:**
```
┌─────────────────────────────────────────┐
│   Host-System (Developer-Laptop)        │
│   - Docker Engine                        │
│   - Source Code (mounted)                │
│                                          │
│  ┌────────────────────────────────────┐ │
│  │  Docker Compose Network            │ │
│  │                                    │ │
│  │  ┌──────────┐  ┌──────────┐      │ │
│  │  │ Backend  │  │ Frontend │      │ │
│  │  │ FastAPI  │  │ Vite Dev │      │ │
│  │  │ :8000    │  │ :5173    │      │ │
│  │  └────┬─────┘  └──────────┘      │ │
│  │       │                           │ │
│  │  ┌────▼─────┐                     │ │
│  │  │    DB    │                     │ │
│  │  │  libSQL  │                     │ │
│  │  └──────────┘                     │ │
│  └────────────────────────────────────┘ │
└─────────────────────────────────────────┘
```

---

## Implementierung

### 1. Multi-Stage Dockerfiles

**Strategie:** Ein Dockerfile pro Service mit mehreren Stages

#### backend/Dockerfile

```dockerfile
# ============================================
# Stage: base - Shared dependencies
# ============================================
FROM python:3.11-slim AS base

WORKDIR /app

# System dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Python dependencies
COPY requirements.txt requirements-dev.txt ./
RUN pip install --no-cache-dir -r requirements.txt -r requirements-dev.txt

# ============================================
# Stage: dev - Development with hot-reload
# ============================================
FROM base AS dev

# Development tools
RUN pip install --no-cache-dir watchfiles ipdb

EXPOSE 8000

# Hot-reload via uvicorn --reload
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]

# ============================================
# Stage: lint - Linting & Type Checking
# ============================================
FROM base AS lint

RUN pip install --no-cache-dir ruff mypy

COPY . .

# Run checks
RUN ruff check . && \
    ruff format --check . && \
    mypy app

# ============================================
# Stage: test - Testing
# ============================================
FROM base AS test

RUN pip install --no-cache-dir pytest pytest-cov faker

COPY . .

CMD ["pytest", "--cov=app", "--cov-report=term-missing", "-v"]

# ============================================
# Stage: prod - Production
# ============================================
FROM python:3.11-slim AS prod

WORKDIR /app

# Only production dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy only source code
COPY app ./app

# Non-root user
RUN useradd -m -u 1000 aquarius && \
    chown -R aquarius:aquarius /app
USER aquarius

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

#### frontend/Dockerfile

```dockerfile
# ============================================
# Stage: base - Dependencies
# ============================================
FROM node:20-alpine AS base

WORKDIR /app

# Install dependencies
COPY package.json package-lock.json ./
RUN npm ci

# ============================================
# Stage: dev - Development Server
# ============================================
FROM base AS dev

COPY . .

EXPOSE 5173

# Vite dev server with HMR
CMD ["npm", "run", "dev", "--", "--host", "0.0.0.0"]

# ============================================
# Stage: lint - ESLint & Prettier
# ============================================
FROM base AS lint

COPY . .

RUN npm run lint && \
    npm run format:check

# ============================================
# Stage: test - Vitest
# ============================================
FROM base AS test

COPY . .

CMD ["npm", "run", "test"]

# ============================================
# Stage: build - Production Build
# ============================================
FROM base AS build

COPY . .

RUN npm run build

# ============================================
# Stage: prod - Nginx Static Server
# ============================================
FROM nginx:alpine AS prod

COPY --from=build /app/dist /usr/share/nginx/html

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
```

---

### 2. docker-compose.yml - Orchestration

```yaml
version: '3.8'

services:
  # ============================================
  # Database (libSQL Server)
  # ============================================
  db:
    image: ghcr.io/tursodatabase/libsql-server:latest
    container_name: aquarius-db
    ports:
      - "8080:8080"  # libSQL HTTP API
    volumes:
      - db-data:/var/lib/sqld
    environment:
      - SQLD_NODE=primary
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8080/health"]
      interval: 10s
      timeout: 5s
      retries: 5

  # ============================================
  # Backend (FastAPI)
  # ============================================
  backend:
    build:
      context: ./backend
      target: dev
    container_name: aquarius-backend
    ports:
      - "8000:8000"
    volumes:
      # Mount source code for hot-reload
      - ./backend:/app
      # Prevent overwriting Python packages
      - /app/.venv
    depends_on:
      db:
        condition: service_healthy
    environment:
      - TURSO_DATABASE_URL=http://db:8080
      - DEBUG=True
      - PYTHONUNBUFFERED=1
    restart: unless-stopped

  # Backend - Lint (on-demand)
  backend-lint:
    build:
      context: ./backend
      target: lint
    volumes:
      - ./backend:/app
    profiles:
      - tools  # Only run with: docker-compose run backend-lint

  # Backend - Test (on-demand)
  backend-test:
    build:
      context: ./backend
      target: test
    volumes:
      - ./backend:/app
      - test-cache:/app/.pytest_cache
    depends_on:
      db:
        condition: service_healthy
    environment:
      - TURSO_DATABASE_URL=http://db:8080
    profiles:
      - tools

  # ============================================
  # Frontend (React + Vite)
  # ============================================
  frontend:
    build:
      context: ./frontend
      target: dev
    container_name: aquarius-frontend
    ports:
      - "5173:5173"
    volumes:
      # Mount source code for hot-reload
      - ./frontend:/app
      # Prevent overwriting node_modules
      - /app/node_modules
    depends_on:
      - backend
    environment:
      - VITE_API_URL=http://localhost:8000
    restart: unless-stopped

  # Frontend - Lint (on-demand)
  frontend-lint:
    build:
      context: ./frontend
      target: lint
    volumes:
      - ./frontend:/app
      - /app/node_modules
    profiles:
      - tools

  # Frontend - Test (on-demand)
  frontend-test:
    build:
      context: ./frontend
      target: test
    volumes:
      - ./frontend:/app
      - /app/node_modules
    profiles:
      - tools

volumes:
  db-data:
    name: aquarius-db-data
  test-cache:
    name: aquarius-test-cache

networks:
  default:
    name: aquarius-network
```

**Wichtige Konzepte:**

1. **Profiles (`tools`)**: Services wie `backend-lint` laufen nur bei explizitem Aufruf
   ```bash
   docker-compose run --rm backend-lint
   ```

2. **Healthchecks**: Backend wartet auf DB-Readiness

3. **Anonymous Volumes**: `node_modules` und `.venv` werden nicht überschrieben

4. **Named Volumes**: Persistente Daten (DB) überleben `docker-compose down`

---

### 3. docker-compose.dev.yml - Development Overrides

```yaml
# Overrides for development (optional)
version: '3.8'

services:
  backend:
    environment:
      - LOG_LEVEL=DEBUG
      - RELOAD=true
    command: ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--reload", "--log-level", "debug"]

  frontend:
    environment:
      - VITE_LOG_LEVEL=debug
```

**Nutzung:**
```bash
# Nur dev
docker-compose up

# Dev mit Overrides
docker-compose -f docker-compose.yml -f docker-compose.dev.yml up
```

---

### 4. .dockerignore - Build-Performance

```
# backend/.dockerignore
__pycache__/
*.pyc
*.pyo
.pytest_cache/
.mypy_cache/
.ruff_cache/
*.egg-info/
.venv/
venv/
.git/
.env
*.db
htmlcov/

# frontend/.dockerignore
node_modules/
dist/
.git/
.env
.env.local
coverage/
```

---

## Hot-Reload Mechanismus

### Backend (FastAPI)

```python
# uvicorn --reload nutzt watchfiles
# Automatisch bei Dateiänderung in /app neu geladen
```

**Volume-Mapping:**
```yaml
volumes:
  - ./backend:/app  # Host -> Container
```

**Ablauf:**
1. Entwickler ändert `backend/app/services/kind_service.py`
2. Datei wird im Container unter `/app/app/services/kind_service.py` sichtbar
3. Uvicorn erkennt Änderung (via `watchfiles`)
4. Server wird neu geladen (~1-2 Sekunden)

### Frontend (Vite)

```javascript
// Vite HMR (Hot Module Replacement)
// WebSocket-Verbindung zum Dev-Server
```

**Volume-Mapping:**
```yaml
volumes:
  - ./frontend:/app
  - /app/node_modules  # Wichtig: Nicht überschreiben!
```

**Ablauf:**
1. Entwickler ändert `frontend/src/components/KindForm.tsx`
2. Datei wird im Container sichtbar
3. Vite erkennt Änderung (via `chokidar`)
4. HMR-Update im Browser (~100ms)

---

## Performance-Optimierung

### Problem: Docker auf Mac/Windows ist langsam

**Ursache:** File-Watching über OSXFS (Mac) oder WSL2 (Windows) hat Latenz

**Lösungen:**

#### 1. Delegated/Cached Volumes (Mac)

```yaml
volumes:
  - ./backend:/app:delegated  # Mac-spezifisch
```

#### 2. Turbo Mode (Docker Desktop)

```bash
# Docker Desktop Settings
# → Features in Development → Enable VirtioFS
```

#### 3. Dev Containers (VS Code)

```json
// .devcontainer/devcontainer.json
{
  "name": "Aquarius Dev",
  "dockerComposeFile": "../docker-compose.yml",
  "service": "backend",
  "workspaceFolder": "/app"
}
```

**Vorteil:** VS Code läuft IM Container → keine File-Watching-Latenz

---

## Vorteile

| Vorteil | Beschreibung |
|---------|--------------|
| **Konsistenz** | Lokal = CI = Production (gleiche Versionen) |
| **Isolation** | Keine Konflikte mit anderen Projekten |
| **Einfaches Setup** | `docker-compose up` statt 10 Installationen |
| **Reproduzierbar** | "Works on my machine" → "Works in the container" |
| **Flexibilität** | Multi-Stage Builds (dev, lint, test, prod) |
| **Cleanup** | `docker-compose down` entfernt alles |

---

## Nachteile & Mitigations

| Nachteil | Mitigation |
|----------|------------|
| **Lernkurve** | Docker-Basics dokumentieren, Makefile abstrahiert |
| **Performance (Mac/Windows)** | VirtioFS aktivieren, Dev Containers |
| **Disk-Space** | `docker system prune` regelmäßig |
| **Debugging** | VS Code Remote Debugging, `docker-compose logs` |

---

## Entwickler-Workflows

### 1. Erste Schritte

```bash
# 1. Docker installieren
# https://docs.docker.com/get-docker/

# 2. Projekt clonen
git clone https://github.com/user/aquarius.git
cd aquarius

# 3. Entwicklung starten
make dev
# → Lädt Images, startet Container
# → Backend: http://localhost:8000
# → Frontend: http://localhost:5173
```

### 2. Tägliche Entwicklung

```bash
# Code ändern in VS Code/IDE
# → Hot-Reload funktioniert automatisch

# In anderem Terminal: Tests
make test

# Logs anschauen
make logs

# Shell im Container
docker-compose exec backend bash
docker-compose exec frontend sh
```

### 3. Debugging

```bash
# Backend: Debugger mit breakpoint()
# → In Code einfügen: breakpoint()
# → Terminal attached: docker-compose up (ohne -d)

# Frontend: Browser DevTools + React DevTools

# Logs einzelner Service
docker-compose logs -f backend
```

### 4. Cleanup

```bash
# Stop (Daten bleiben)
make stop

# Remove (auch Volumes)
make clean

# Remove alles (auch Images)
make clean-all
```

---

## CI/CD Integration

**GitHub Actions nutzt gleiche Docker-Images:**

```yaml
# .github/workflows/ci.yml
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - name: Run Tests
        run: make test  # Nutzt Docker Compose
```

**Vorteile:**
- Gleiche Umgebung lokal und CI
- Keine dualen Configurations (Docker Compose + GitHub Actions)
- Entwickler können CI lokal reproduzieren

---

## Troubleshooting

### Problem: Port bereits belegt

```bash
# Error: Bind for 0.0.0.0:8000 failed: port is already allocated

# Lösung 1: Anderen Port nutzen
docker-compose up -e BACKEND_PORT=8001

# Lösung 2: Konflikt finden und beenden
lsof -i :8000
kill <PID>
```

### Problem: Volumes nicht gemountet

```bash
# Symptom: Code-Änderungen werden nicht übernommen

# Lösung: Container neu bauen
docker-compose down
docker-compose build
docker-compose up
```

### Problem: "Permission denied"

```bash
# Symptom: Container kann nicht in gemountete Volumes schreiben

# Lösung: User ID anpassen
# In Dockerfile:
ARG UID=1000
RUN useradd -m -u ${UID} aquarius
USER aquarius

# Build mit Host-UID:
docker-compose build --build-arg UID=$(id -u)
```

---

## Alternativen

| Alternative | Pro | Contra |
|-------------|-----|--------|
| **Lokale Installation** | Native Performance | "Works on my machine", Setup-Hölle |
| **Vagrant** | VM-basiert, vollständig | Langsam, hoher Overhead |
| **devbox / nix** | Reproduzierbar | Steile Lernkurve, noch nicht mainstream |

**Entscheidung:** Docker ist der beste Kompromiss aus Standardisierung, Performance und Funktionalität.

---

## Konsequenzen

### Positiv ✅

- **Setup-Zeit:** 30 Min → 5 Min (nur Docker installieren)
- **"Works on my machine"**: Eliminiert (gleiche Umgebung)
- **CI/CD**: Konsistent (gleiche Images)
- **Onboarding**: Einfacher für neue Entwickler

### Negativ ⚠️

- **Docker lernen**: Team muss Basics kennen
- **Performance**: Leichte Einbußen auf Mac/Windows
- **Disk-Space**: Docker-Images brauchen Platz (~2-5 GB)

### Neutral ℹ️

- **IDE-Integration**: Dev Containers empfohlen für beste Erfahrung
- **Debugging**: Unterschiedlich zu lokaler Entwicklung (aber machbar)

---

## Offene Fragen

- [ ] Sollten wir Docker Desktop empfehlen oder Podman/Rancher Desktop?
- [ ] Brauchen wir einen `make doctor` Command für Docker-Health-Checks?
- [ ] Sollen wir Dev Containers als Standard empfehlen?

---

## Referenzen

- [Docker Compose Documentation](https://docs.docker.com/compose/)
- [Multi-Stage Builds](https://docs.docker.com/build/building/multi-stage/)
- [VS Code Dev Containers](https://code.visualstudio.com/docs/devcontainers/containers)
- [Best Practices for Dockerfiles](https://docs.docker.com/develop/develop-images/dockerfile_best-practices/)

---

**Zusammenhang mit anderen ADRs:**
- [ADR-010: Makefile](ADR-010-makefile-build-interface.md) - Makefile ruft Docker Compose Commands
- [ADR-012: Act](ADR-012-act-local-ci.md) - Act nutzt Docker für lokale CI-Ausführung

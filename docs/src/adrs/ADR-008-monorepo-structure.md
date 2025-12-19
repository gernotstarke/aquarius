# ADR-008: Monorepo mit zwei Frontend-Modulen

**Status:** Akzeptiert
**Datum:** 2025-12-17
**Entscheider:** Architektur-Team

## Kontext

Das System hat zwei unterschiedliche Nutzungskontexte:
1. **Planung** - Desktop-optimierte Verwaltung (Büro, Online)
2. **Durchführung** - Touch-optimierte Bewertung (Schwimmbad, Offline)

Beide teilen gemeinsame Daten, Business-Logic und UI-Komponenten.

## Entscheidung

Wir verwenden eine **Monorepo-Struktur** mit zwei separaten Frontend-Modulen für Planung und Durchführung, plus ein gemeinsames Shared-Modul.

## Begründung

### Vorteile

- **Code-Sharing** - Gemeinsame UI-Komponenten, Hooks, Utils
- **Typsicherheit** - Shared Types zwischen Frontend und Backend
- **Atomic Commits** - Änderungen an mehreren Modulen in einem Commit
- **Konsistente Versionen** - Dependencies zentral verwaltet
- **Einfaches Refactoring** - Cross-Module-Refactorings möglich
- **Einheitliches Tooling** - ESLint, Prettier, TypeScript-Config geteilt

### Alternativen

| Alternative | Grund für Ablehnung |
|-------------|---------------------|
| **Separate Repos** | Code-Duplizierung, schwierige Synchronisation |
| **Multirepo mit npm packages** | Overhead, Versionierungs-Probleme |
| **Monolith-App mit Routing** | Zu viel Bundle-Size, unterschiedliche Anforderungen |

## Konsequenzen

### Positiv

- Gemeinsame Komponenten reduzieren Entwicklungsaufwand
- Konsistentes Look-and-Feel zwischen Apps
- Einfachere Dependency-Verwaltung
- Schnellere Cross-App-Features

### Negativ

- Größeres Repository
- Build-Zeiten potentiell länger (via Caching lösbar)
- CI/CD etwas komplexer

## Technische Details

### Verzeichnisstruktur

```
aquarius/
├── apps/
│   ├── planning/          # Desktop-App (Planung)
│   │   ├── src/
│   │   ├── package.json
│   │   └── vite.config.ts
│   │
│   └── execution/         # Mobile-App (Durchführung)
│       ├── src/
│       ├── package.json
│       └── vite.config.ts
│
├── packages/
│   ├── ui/                # Shared UI Components
│   │   └── src/
│   │       ├── Button/
│   │       ├── Form/
│   │       └── Table/
│   │
│   ├── shared/            # Shared Business Logic
│   │   └── src/
│   │       ├── hooks/
│   │       ├── utils/
│   │       └── types/
│   │
│   └── api-client/        # API Client Library
│       └── src/
│           ├── endpoints/
│           └── types/
│
├── backend/               # FastAPI Backend
│   └── src/
│
└── package.json           # Root package.json (workspaces)
```

### Workspace-Konfiguration

```json
{
  "name": "aquarius-monorepo",
  "private": true,
  "workspaces": [
    "apps/*",
    "packages/*",
    "backend"
  ],
  "scripts": {
    "dev:planning": "npm run dev --workspace=apps/planning",
    "dev:execution": "npm run dev --workspace=apps/execution",
    "build:all": "npm run build --workspaces"
  }
}
```

### Unterschiede zwischen den Apps

| Aspekt | Planning App | Execution App |
|--------|-------------|---------------|
| **Viewport** | Desktop (1280px+) | Tablet/Mobile (768px-1024px) |
| **Input** | Maus + Tastatur | Touch |
| **Navigation** | Sidebar, Multi-Panel | Bottom-Nav, Single-Panel |
| **Offline** | Optional | Zwingend erforderlich |
| **Service Worker** | Cache-First | Network-First mit Fallback |

## Build & Deployment

- **Separate Builds** - Jede App hat eigenen Build-Output
- **Separate Deployments** - Unterschiedliche URLs möglich
- **Shared CDN** - Gemeinsame Assets gecacht

```bash
# Development
npm run dev:planning    # http://localhost:5173
npm run dev:execution   # http://localhost:5174

# Production Build
npm run build:planning  # → apps/planning/dist
npm run build:execution # → apps/execution/dist
```

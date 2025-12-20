# Arqua42 CRUD Prototype

Simple CRUD application for testing the Arqua42 tech stack.

## Features

- **Backend**: FastAPI + SQLAlchemy + SQLite
- **Frontend**: React + TypeScript + Vite + TailwindCSS
- **State Management**: TanStack Query for server state
- **Styling**: TailwindCSS with custom design system
- **Database**: SQLite with Docker volume persistence

## Entities

The prototype manages four main entities:

1. **Saison** - Competition seasons
2. **Schwimmbad** - Swimming pools and facilities
3. **Wettkampf** - Competitions (linked to Saison and Schwimmbad)
4. **Kind** - Children participants

## Quick Start

### Start the application

```bash
make dev
```

This starts:
- Backend API at http://localhost:8000
- Frontend at http://localhost:5173
- API Documentation at http://localhost:8000/docs

### Seed the database

In a new terminal, seed the database with sample data:

```bash
make db-seed
```

This creates:
- 2 Saisons
- 3 Schwimmbäder
- 4 Wettkämpfe
- 6 Kinder

### Reset the database

To clear all data and start fresh:

```bash
make db-reset
```

### Stop the application

```bash
make dev-down
```

## Design System

The frontend uses a carefully designed system for high usability:

### Typography
- **Large, readable fonts** - Base size 1rem with large headings
- **Ample line height** - 1.6 for body text
- **Clear hierarchy** - Display, H1, H2, H3 with distinct sizes

### Spacing
- **Base-8 grid** - Consistent spacing throughout
- **Generous whitespace** - Ample padding and margins
- **Clean layout** - Focused content areas

### Touch Targets
- **Minimum 44px** - All interactive elements
- **Large buttons** - Easy to tap on mobile
- **Clear focus states** - Accessible keyboard navigation

### Colors
- **Simple palette** - Primary blue and neutral grays
- **High contrast** - WCAG AA compliant
- **Semantic colors** - Danger red for destructive actions

## Project Structure

```
├── backend/
│   ├── app/
│   │   ├── models/        # SQLAlchemy models
│   │   ├── schemas/       # Pydantic schemas
│   │   ├── database.py    # Database configuration
│   │   └── main.py        # FastAPI app with CRUD endpoints
│   ├── seed_db.py         # Database seeding script
│   ├── requirements.txt   # Python dependencies
│   └── Dockerfile         # Backend container
├── frontend/
│   ├── src/
│   │   ├── api/           # API client
│   │   ├── components/    # Reusable UI components
│   │   ├── pages/         # CRUD pages for each entity
│   │   ├── styles/        # TailwindCSS configuration
│   │   ├── types/         # TypeScript interfaces
│   │   ├── App.tsx        # Main app with routing
│   │   └── main.tsx       # Entry point
│   ├── package.json       # Node dependencies
│   ├── vite.config.ts     # Vite configuration
│   ├── tailwind.config.js # TailwindCSS design tokens
│   └── Dockerfile         # Frontend container
└── docker-compose.yml     # Multi-container setup

## API Endpoints

All entities follow the same REST pattern:

- `GET /api/{entity}` - List all
- `GET /api/{entity}/{id}` - Get single
- `POST /api/{entity}` - Create new
- `PUT /api/{entity}/{id}` - Update existing
- `DELETE /api/{entity}/{id}` - Delete

Entities: `saison`, `schwimmbad`, `wettkampf`, `kind`

## Database Persistence

The SQLite database is stored in a Docker volume, so data persists between container restarts. To completely reset:

```bash
make dev-down
docker volume rm aquarius_sqlite-data
make dev
make db-seed
```

## Technology Stack Validation

This prototype validates:

✅ FastAPI works well for REST APIs
✅ SQLAlchemy 2.0 provides good type safety
✅ Pydantic simplifies validation
✅ React + TypeScript provides type-safe frontend
✅ TanStack Query handles server state elegantly
✅ TailwindCSS enables rapid UI development
✅ Vite provides fast development experience
✅ Docker Compose simplifies development setup
✅ SQLite is sufficient for prototyping

## Next Steps

Based on this prototype, we can:

1. Add authentication and authorization
2. Implement the full domain model (6 bounded contexts)
3. Add PWA capabilities (service worker, offline support)
4. Implement the separation between office and pool UIs
5. Migrate to Turso for production database
6. Add comprehensive test coverage
7. Implement the rating calculation logic

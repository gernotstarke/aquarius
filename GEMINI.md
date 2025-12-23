# Arqua42 (Aquarius)

## Project Overview
Arqua42 is a swimming competition rating system designed for children's competitions. It is a Progressive Web Application (PWA) optimized for offline-first operation and touch-friendly interfaces. The system is split into two main components:
- **Planning Application:** Desktop-optimized for organizing competitions, managing participants/teams, and configuring events.
- **Execution Application:** Mobile/tablet-optimized for real-time scoring during competitions, featuring offline capabilities.

The project follows **Domain-Driven Design (DDD)** principles with 6 identified Bounded Contexts (Club Management, Competition Management, Registration, Judging, Results, System Admin).

## Technology Stack

### Frontend (`/frontend`)
- **Framework:** React 18 + TypeScript
- **Build Tool:** Vite
- **Styling:** TailwindCSS
- **State/Data:** TanStack Query, Zustand (inferred from ADRs)
- **HTTP Client:** Axios
- **Routing:** React Router DOM

### Backend (`/backend`)
- **Language:** Python 3.11+
- **Framework:** FastAPI
- **ORM:** SQLAlchemy
- **Validation:** Pydantic
- **Server:** Uvicorn

### Database
- **Primary:** Turso (libSQL) with embedded replicas for offline support.

### DevOps & Documentation
- **Containerization:** Docker & Docker Compose
- **Build Automation:** Make
- **Documentation:** AsciiDoc, PlantUML, Architecture Decision Records (ADRs)

## Architecture & Domain
The core domain model focuses on swimming competitions ("Wettkampf") organized in seasons ("Saison"). Key entities include:
- **Verein (Club)** & **Team**
- **Kind (Child)** & **Anmeldung (Registration)**
- **Figur (Figure)** & **Durchgang (Round)**
- **Offizieller (Official)**: Kampfrichter (Judges) & Punktrichter (Scorekeepers)

## Development Workflow

### Prerequisites
- Docker (Recommended)
- Make
- Python 3.11+ (Local fallback)
- Node.js 18+ (Local fallback)

### Key Commands
The project uses `make` as the primary interface for all tasks.

#### Documentation
- **Generate all docs:** `make docs` (Builds HTML, diagrams, ADRs)
- **Serve docs:** `make docs-serve` (Host at http://localhost:8000)
- **Watch mode:** `make docs-watch` (Requires Docker Compose)

#### Application Development
- **Start Stack:** `make dev` (Starts Backend at :8000, Frontend at :5173)
- **Stop Stack:** `make dev-down`
- **Reset DB:** `make db-reset` (Drops and recreates tables)
- **Seed DB:** `make db-seed` (Populates with sample data)

#### Frontend (Local)
Located in `frontend/`:
- `npm run dev`: Start dev server
- `npm run build`: Type-check and build
- `npm run lint`: Lint code

#### Backend (Local)
Located in `backend/`:
- `uvicorn app.main:app --reload`: Start server (requires env setup)

## Directory Structure
- `backend/`: API source code, database models, and schemas.
- `frontend/`: React application source code, components, and pages.
- `docs/src/`: Source files for architecture documentation (ADRs, diagrams, text).
- `docs/build/`: Generated output for documentation (ignored by git).
- `.crush/`: System logs and artifacts.

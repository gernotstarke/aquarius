# Agent Documentation - Aquarius Swimming Rating System

This document provides essential information for AI agents working with the Aquarius codebase - a computerized scoring system for artistic swimming competitions for children's leagues.

## Project Overview

**Aquarius** is a full-stack web application for managing and scoring artistic swimming competitions (specifically figure swimming). The system supports the complete competition organization workflow from season planning through registration to live scoring and results analysis.

### Project Structure

```
aquarius/
├── backend/                  # Python FastAPI backend
│   ├── app/
│   │   ├── __init__.py
│   │   └── database.py      # Database configuration with Turso (libSQL)
│   ├── .env.example         # Environment variables template
│   └── requirements.txt     # Python dependencies
├── docs/                    # Documentation
│   ├── adrs/               # Architecture Decision Records
│   ├── architecture/       # Architecture documentation (AsciiDoc)
│   ├── requirements/       # Requirements documentation
│   ├── architecture.adoc   # Main architecture document
│   └── domain-model.md     # Domain model documentation
├── logo/                    # Logo assets
├── Makefile                 # Build automation
├── LICENSE
└── README.md
```

## Tech Stack

### Backend (Python + FastAPI)
- **Python 3.11+** - Programming language
- **FastAPI 0.109+** - Web framework
- **Pydantic v2** - Data validation
- **SQLAlchemy 2.0** - ORM
- **libsql-experimental** - Turso database client
- **uvicorn** - ASGI server

### Database
- **Turso (libSQL)** - Cloud-native SQLite fork with sync capabilities
- Supports both cloud (`libsql://`) and local SQLite file mode
- Offline-capable with automatic synchronization

### Frontend (Planned)
- **React 18** with **TypeScript** (as per ADR-013)
- **Vite 5.x** - Build tool
- **TailwindCSS** - Styling (as per ADR-017)
- **TanStack Query v5** - Server state management
- **Zustand** - Local state management
- **Workbox** - Service Worker/PWA support

## Essential Commands

### Documentation Commands

```bash
# Generate all documentation (diagrams + HTML)
make docs

# Generate HTML documentation from AsciiDoc
make docs-html

# Generate PNG diagrams from PlantUML sources
make docs-diagrams

# Generate PDF documentation (requires asciidoctor-pdf)
make docs-pdf

# Watch documentation files for changes and rebuild
make docs-watch

# Serve documentation on http://localhost:8000
make docs-serve

# Clean generated files
make clean
```

### Development Commands (Planned/Not Yet Implemented)

```bash
# Start development environment
make dev      # Currently shows "not yet implemented"

# Run linters
make lint     # Currently shows "not yet implemented"

# Run tests
make test     # Currently shows "not yet implemented"
```

### Backend Setup

1. **Install Python dependencies:**
   ```bash
   cd backend
   pip install -r requirements.txt
   ```

2. **Configure environment:**
   ```bash
   cp backend/.env.example backend/.env
   # Edit .env with your Turso database credentials
   ```

3. **Environment variables:**
   - `TURSO_DATABASE_URL`: Database URL (e.g., `libsql://your-database.turso.io` or `file:./aquarius.db` for local)
   - `TURSO_AUTH_TOKEN`: Authentication token for Turso cloud
   - `APP_NAME`: Application name
   - `DEBUG`: Debug mode (True/False)
   - `CORS_ORIGINS`: Allowed CORS origins

## Code Organization

### Backend Structure

The backend follows a modular structure:

- `app/` - Main application package
  - `database.py` - Database configuration with Turso support (cloud and local modes)
  - Additional modules to be added for models, routes, services, etc.

### Database Configuration

The database module (`backend/app/database.py`) provides:
- Automatic detection of Turso cloud vs local SQLite mode
- SQLAlchemy engine with appropriate configuration
- Session management via `SessionLocal`
- Database initialization via `init_db()`
- Dependency injection for FastAPI routes via `get_db()`
- Foreign key enforcement for SQLite

## Domain Model

The system manages the following core entities:

### Organization Structure
- **Verein** (Club) - Sports club with teams
- **Team** - Group of children within a club
- **Kind** (Child) - Participant in the children's swimming league
- **Offizieller** (Official) - Volunteer league member
  - **Kampfrichter** (Judge) - Scores performances
  - **Punktrichter** (Score Judge) - Manages station and calculates final scores

### Competition Structure
- **Saison** (Season) - Period with planned competitions
- **Wettkampf** (Competition) - Sporting event for figure and synchronized swimming
- **Station** - Location at pool where performances are executed and scored
- **Durchgang** (Round) - Part of competition where all children in a group perform a figure
- **Figur** (Figure) - Prescribed movement sequence with scoring rules and difficulty factor
- **Start** (Attempt) - A child's performance of a specific figure
- **Bewertung** (Score) - Judges give preliminary scores, score judge calculates final (drop highest/lowest, average × difficulty)

## Important Patterns & Conventions

### Python Code Style
- Standard Python naming conventions (snake_case for functions/variables)
- Type hints encouraged for better code clarity
- Docstrings for modules and complex functions
- SQLAlchemy declarative base for models

### Database Patterns
- Foreign key constraints enabled
- Echo mode enabled in development for SQL debugging
- Support for both local development (SQLite) and production (Turso cloud)
- Session management with context managers

### Architecture Decisions

The project follows several important architecture decisions documented in ADRs:

1. **ADR-009**: Test concept defined
2. **ADR-010**: Makefile as build interface
3. **ADR-011**: Docker for development environment
4. **ADR-012**: Act for local CI testing
5. **ADR-013**: React + TypeScript for frontend
6. **ADR-014**: Python + FastAPI for backend
7. **ADR-015**: Turso (libSQL) as database
8. **ADR-016**: PWA architecture for offline capability
9. **ADR-017**: TailwindCSS for styling
10. **ADR-018**: Domain-Driven Design approach

## Gotchas and Non-Obvious Patterns

### Database Connection
- The system automatically detects if using Turso cloud (URL starts with `libsql://`) or local SQLite
- Authentication token is only required for Turso cloud connections
- SQLite foreign keys are explicitly enabled via pragma

### Offline Capability
- The system is designed to work offline at swimming pools (critical requirement)
- Uses Turso's embedded replicas for offline sync
- Automatic synchronization when connection is restored
- Last-write-wins conflict resolution is acceptable for this small league

### Two Frontend Apps (Planned)
The system will have two distinct frontend applications:
1. **Planning App**: Desktop-optimized for office/administration
2. **Execution App**: Mobile/touch-optimized for competitions at pools

## Testing Approach

Currently, test infrastructure is planned but not yet implemented. The Makefile includes a `test` target that will be configured once tests are added.

## Documentation System

The project uses:
- **AsciiDoc** for architecture documentation
- **PlantUML** for diagrams (in `docs/architecture/images/puml/`)
- **Markdown** for ADRs and domain model
- Generated documentation served via Python's HTTP server

## Environment Requirements

### Required Tools
- Python 3.11+
- Make (for Makefile commands)

### Optional Tools for Documentation
- `plantuml` - For generating diagrams from PlantUML
- `asciidoctor` - For generating HTML from AsciiDoc
- `asciidoctor-pdf` - For generating PDF documentation
- `watchexec` - For watching file changes

### Installation Commands

**macOS:**
```bash
brew install plantuml
gem install asciidoctor asciidoctor-pdf asciidoctor-diagram
brew install watchexec
```

**Linux:**
```bash
apt install plantuml
gem install asciidoctor asciidoctor-pdf asciidoctor-diagram
apt install watchexec
```

## Next Steps for Development

1. **Backend Implementation**:
   - Add domain models based on the domain model documentation
   - Implement API routes for competitions, teams, scoring
   - Add authentication and authorization
   - Implement business logic for score calculation

2. **Frontend Setup**:
   - Initialize React + TypeScript projects for both apps
   - Set up Vite build configuration
   - Configure PWA manifest and service workers
   - Implement offline synchronization with Turso

3. **Testing**:
   - Add unit tests for backend business logic
   - Add integration tests for API endpoints
   - Configure test runners in Makefile

4. **CI/CD**:
   - Set up Docker development environment (as per ADR-011)
   - Configure Act for local CI testing (as per ADR-012)
   - Add GitHub Actions workflows

## Contact and Resources

- Main documentation: `docs/architecture.adoc`
- Domain model: `docs/domain-model.md`
- Requirements: `docs/requirements/requirements.md`
- Architecture decisions: `docs/adrs/`
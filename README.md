# Arqua42

A swimming competition rating system for children's competitions, optimized for offline-first operation and touch-friendly interfaces.

## Overview

Arqua42 is a Progressive Web Application (PWA) designed to manage swimming competitions for children. It consists of two main applications:

- **Planning Application**: Desktop-optimized interface for organizing competitions, managing participants, and configuring events
- **Execution Application**: Mobile/tablet-optimized interface for real-time scoring during competitions with offline capability

## Technology Stack

- **Frontend**: React 18 + TypeScript + Vite + TailwindCSS
- **Backend**: Python 3.11+ + FastAPI + Pydantic + SQLAlchemy
- **Database**: SQLite (development) / Turso (production, planned)
- **Architecture**: Domain-Driven Design
- **Data Management**: JSON-based catalogs for maintainability

## Documentation

Full architecture documentation is available in `docs/architecture.html` (generated from AsciiDoc sources).

### Building Documentation

The project uses a **Docker-based build system** to avoid dependency installation nightmares. You only need:

- **Make** (prerequisite)
- **Docker** (recommended) or local tools as fallback

#### Quick Start

```bash
# Generate all documentation (diagrams + HTML)
make docs

# View documentation in browser
make docs-serve
# Then open http://localhost:8000/architecture.html
```

#### Available Make Targets

Run `make help` to see all available targets. Key targets include:

**Documentation Targets:**

- `make docs` - Generate all documentation (diagrams + HTML) using Docker
- `make docs-diagrams` - Generate PNG diagrams from PlantUML sources (Docker-based)
- `make docs-html` - Generate HTML documentation from AsciiDoc (Docker-based)
- `make docs-pdf` - Generate PDF documentation (Docker-based)
- `make docs-serve` - Serve documentation on http://localhost:8000
- `make docs-watch` - Watch for changes and rebuild automatically (requires docker-compose)

**Docker Targets:**

- `make docs-build-image` - Build the Docker image for documentation generation

**Development Targets:**

- `make dev` - Start development environment (Backend + Frontend + Database)
- `make dev-down` - Stop development environment
- `make db-reset` - Reset database (drop all tables and recreate)
- `make db-seed` - Seed database with sample data from JSON catalog
- `make db-import-figures FILE=<path>` - Import figures from JSON catalog (updates existing, adds new)
- `make test` - Run all tests
- `make lint` - Run linters (not yet implemented)

**Cleanup:**

- `make clean` - Remove generated files (HTML, PDF, diagrams)

#### Docker-First Approach

The build system follows a **Docker-first** approach with local fallback:

1. **If Docker image exists**: Use it for fast builds
2. **If Docker available but no image**: Build image automatically, then use it
3. **If Docker not available**: Fall back to local tools (plantuml, asciidoctor, etc.)
4. **If neither available**: Show helpful error message with installation instructions

This ensures:
- ✅ **Reproducible builds** across different machines
- ✅ **No version conflicts** with system-installed tools
- ✅ **Consistent output** for all team members
- ✅ **Fallback support** for environments without Docker

#### Building the Docker Image

The documentation Docker image includes:
- Ruby 3.2 (Alpine-based)
- PlantUML 1.2024.7
- AsciiDoctor 2.0.23 with diagram and PDF support
- Graphviz for diagram rendering

Build manually if needed:

```bash
make docs-build-image
```

The image is automatically built when needed by documentation targets.

#### Local Development (without Docker)

If you prefer local tools, install:

```bash
# PlantUML (for diagrams)
# macOS:
brew install plantuml

# Linux:
apt install plantuml

# AsciiDoctor (for HTML/PDF)
gem install asciidoctor asciidoctor-diagram asciidoctor-pdf rouge
```

Then use the same `make` commands - they'll automatically use local tools.

## Project Structure

```
arqua42/
├── docs/                          # Documentation
│   ├── src/                       # Documentation source files
│   │   ├── architecture.adoc      # Main architecture document (AsciiDoc)
│   │   ├── architecture/          # Modular architecture chapters
│   │   │   ├── 05-bausteinsicht.adoc
│   │   │   ├── 08-querschnittliche-konzepte.adoc
│   │   │   ├── adr/               # Architecture Decision Records
│   │   │   └── images/
│   │   │       ├── puml/          # PlantUML source files
│   │   │       └── screenshots/   # Screenshots and mockups
│   │   ├── requirements/          # Requirements documentation
│   │   └── domain-model.md        # Domain model documentation
│   └── build/                     # Generated documentation (git-ignored)
│       ├── architecture.html      # Generated HTML (via make docs)
│       ├── architecture.pdf       # Generated PDF (via make docs-pdf)
│       └── images/                # Generated PNG diagrams
├── backend/                       # FastAPI backend
│   ├── app/                       # Application code
│   │   ├── models/                # SQLAlchemy models
│   │   ├── schemas/               # Pydantic schemas
│   │   ├── main.py                # FastAPI application
│   │   └── database.py            # Database configuration
│   ├── data/                      # Data files
│   │   └── figuren-kataloge/      # Figure catalogs (JSON)
│   │       ├── figuren-v1.0-saison-2024.json
│   │       └── README.md
│   ├── static/                    # Static files
│   │   └── figuren/               # Figure images (PNG/JPG)
│   │       └── README.md
│   ├── seed_db.py                 # Database seeding script
│   └── requirements.txt           # Python dependencies
├── frontend/                      # React frontend
│   ├── src/
│   │   ├── components/            # Reusable components
│   │   ├── pages/                 # Page components
│   │   ├── types/                 # TypeScript types
│   │   └── App.tsx                # Main application
│   └── package.json               # Node.js dependencies
├── BILDER_UND_KATALOG.md         # Figure images and catalog guide
├── Dockerfile.docs                # Docker image for documentation build
├── docker-compose.yml             # Docker Compose for development
├── docker-compose.docs.yml        # Docker Compose for documentation services
├── Makefile                       # Build automation
└── README.md                      # This file
```

## Getting Started

### Prerequisites

- **Docker** (recommended) or local development tools
- **Make**
- **Python 3.11+** (for backend, when implemented)
- **Node.js 18+** (for frontend, when implemented)

### Build Documentation

```bash
# Clone repository
git clone <repository-url>
cd arqua42

# Generate documentation
make docs

# View documentation
make docs-serve
```

### Development Setup

```bash
# Start development environment (Backend, Frontend, Database)
make dev

# Access the applications:
# - Backend API:  http://localhost:8000
# - Frontend UI:  http://localhost:5173
# - API Docs:     http://localhost:8000/docs
```

#### Database Seeding

The project uses a JSON-based figure catalog system for easy maintenance:

```bash
# Seed database with sample data (from JSON catalog)
make db-seed

# Or reset and seed from scratch
make db-reset

# Import/update figures from a specific JSON catalog
make db-import-figures FILE=data/figuren-kataloge/figuren-v1.0-saison-2024.json
```

**Seeding vs. Importing:**

- `make db-seed` - **Full seeding**: Drops all tables, recreates them, and populates with sample data (seasons, pools, competitions, children, registrations, figures)
- `make db-import-figures` - **Figures only**: Updates existing figures or adds new ones from a JSON catalog without affecting other data

**Importing Figures:**

```bash
# Import the default catalog
make db-import-figures FILE=data/figuren-kataloge/figuren-v1.0-saison-2024.json

# Import a different version
make db-import-figures FILE=data/figuren-kataloge/figuren-v2.0-saison-2025.json
```

The import process:
- Loads figures from the specified JSON catalog
- Updates existing figures (matched by name)
- Creates new figures that don't exist yet
- Checks for figure images in `backend/static/figuren/`
- Reports statistics (created, updated, images found/missing)

**Adding Figure Images:**

1. Place your PNG/JPG images in `backend/static/figuren/`
2. Run `make db-import-figures FILE=<path-to-catalog>` to update the database
3. See `BILDER_UND_KATALOG.md` for detailed instructions

**Editing the Figure Catalog:**

The JSON catalog can be manually edited:
- File: `backend/data/figuren-kataloge/figuren-v1.0-saison-2024.json`
- Contains all 26 swimming figures with IDs, difficulty, age groups, and image paths
- After editing, run `make db-import-figures FILE=<path>` to apply changes
- See `backend/data/figuren-kataloge/README.md` for schema documentation

## Architecture

The system follows **Domain-Driven Design** with 6 Bounded Contexts:

1. **Club Management**: Managing clubs and their members
2. **Competition Management**: Planning and configuring competitions
3. **Registration**: Enrolling children in competitions
4. **Judging**: Real-time scoring during competitions
5. **Results**: Computing and publishing results
6. **System Administration**: User management and configuration

For detailed architecture documentation, see `docs/architecture.html`.

## Contributing

*Contribution guidelines will be added as the project evolves.*

## License

*License information to be added.*

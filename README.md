# Aquarius

A swimming competition rating system for children's competitions, optimized for offline-first operation and touch-friendly interfaces.

## Overview

Aquarius is a Progressive Web Application (PWA) designed to manage swimming competitions for children. It consists of two main applications:

- **Planning Application**: Desktop-optimized interface for organizing competitions, managing participants, and configuring events
- **Execution Application**: Mobile/tablet-optimized interface for real-time scoring during competitions with offline capability

## Technology Stack

- **Frontend**: React 18 + TypeScript + Vite + TailwindCSS
- **Backend**: Python 3.11+ + FastAPI + Pydantic
- **Database**: Turso (libSQL) with embedded replicas for offline support
- **Architecture**: Domain-Driven Design with 6 Bounded Contexts

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

- `make test` - Run tests (not yet implemented)
- `make lint` - Run linters (not yet implemented)
- `make dev` - Start development environment (not yet implemented)

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
aquarius/
├── docs/                          # Documentation
│   ├── architecture.adoc          # Main architecture document (AsciiDoc)
│   ├── architecture/              # Modular architecture chapters
│   │   ├── 05-bausteinsicht.adoc
│   │   ├── 08-querschnittliche-konzepte.adoc
│   │   ├── adr/                   # Architecture Decision Records
│   │   └── images/
│   │       ├── puml/              # PlantUML source files
│   │       ├── generated/         # Generated PNG diagrams
│   │       └── screenshots/       # Screenshots and mockups
│   ├── architecture.html          # Generated HTML (via make docs)
│   └── architecture.pdf           # Generated PDF (via make docs-pdf)
├── backend/                       # FastAPI backend (to be implemented)
├── frontend/                      # React frontend (to be implemented)
├── Dockerfile.docs                # Docker image for documentation build
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
cd aquarius

# Generate documentation
make docs

# View documentation
make docs-serve
```

### Development Setup

*Coming soon - Development environment setup will be added once implementation begins.*

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

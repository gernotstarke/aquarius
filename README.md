# Aquarius - Kunstschwimmen Wettkampf-Verwaltungssystem

Ein Monorepo für die komplette Aquarius-Plattform zur Verwaltung von Kunstschwimm-Wettkämpfen.

## 📦 Monorepo-Struktur

```
aquarius/
├── web/                    # Desktop/Web Application
│   ├── backend/           # FastAPI Backend
│   ├── frontend/          # React Frontend
│   ├── Dockerfile         # Production build
│   ├── fly.toml           # fly.io deployment config
│   └── docker-compose.yml # Development environment
│
├── mobile/                 # Mobile App (iOS/Android)
│   ├── ios/               # iOS-specific code
│   ├── android/           # Android-specific code
│   └── shared/            # Shared business logic
│
├── documentation/          # Architecture & Requirements
│   ├── adr/               # Architecture Decision Records (shared!)
│   ├── architecture/      # arc42 Documentation
│   ├── requirements/      # Requirements & User Stories
│   └── guides/            # Development Guides
│
├── docs/                   # Jekyll Static Website (GitHub Pages)
│   └── (placeholder for future Jekyll site)
│
├── shared/                 # Shared Code & Types (optional)
│   ├── types/             # TypeScript/Python type definitions
│   └── schemas/           # OpenAPI/JSON schemas
│
└── Makefile               # Root orchestration
```

## 🚀 Quick Start

### Prerequisites

- Docker & Docker Compose
- Node.js 20+ & npm
- Python 3.11+
- (Optional) fly.io CLI for deployment
- (Optional) Turso CLI for database

### Installation

```bash
# Install all dependencies
make install

# Or install per project:
cd web/backend && pip install -r requirements.txt
cd web/frontend && npm install
cd mobile && npm install
```

### Development

**Web App:**
```bash
# Start backend + frontend
make web-dev

# Or from web/ directory
cd web && make dev
```

Access:
- Frontend: http://localhost:5173
- Backend API: http://localhost:8000
- API Docs: http://localhost:8000/docs

**Mobile App:**
```bash
# iOS Simulator
make mobile-ios

# Android Emulator
make mobile-android
```

**Documentation:**
```bash
# Generate docs
make docs-build

# Serve locally
make docs-serve
```

## 📚 Project-Specific Documentation

Each project has its own README with detailed information:

- **[Web App](web/README.md)** - Desktop/Web application setup, development, and deployment
- **[Mobile App](mobile/README.md)** - Mobile app development for iOS/Android
- **[Documentation](documentation/README.md)** - How to write and generate documentation

## 🎯 Common Tasks

### Database Operations

```bash
# Reset database (web app)
make web-db-reset

# Seed with sample data
make web-db-seed

# If you see "(trapped) error reading bcrypt version", rebuild the web backend
# (bcrypt 4.x is incompatible with passlib 1.7.x).
# Example:
# docker compose build backend

# Import figures from JSON catalog
cd web && make db-import-figures FILE=backend/data/figuren/figuren-v1.0-saison-2024.json
```

### Deployment

```bash
# Deploy web app to fly.io
make web-deploy

# Check deployment status
make web-deploy-status

# View logs
make web-logs
```

### Testing

```bash
# Run web app tests
make web-test

# Run mobile app tests
make mobile-test
```

## 📖 Architecture Decision Records (ADRs)

ADRs are located in `documentation/adr/` and are **shared across all projects**.

Naming convention:
- `ADR-001-web-*` - Web app specific
- `ADR-002-mobile-*` - Mobile app specific
- `ADR-003-shared-*` - Affects multiple projects

## 🌐 Deployment

### Web App (fly.io + Turso)

```bash
# Initial setup
cd web && make deploy-setup

# Deploy
make web-deploy
```

**Production URL:** https://aquarius.arc42.org

### Mobile App (App Store / TestFlight)

See [mobile/README.md](mobile/README.md) for deployment instructions.

### Documentation (GitHub Pages)

Documentation is automatically published to GitHub Pages from the `docs/` directory.

## 🛠️ Tech Stack

### Web App
- **Backend:** Python 3.11, FastAPI, SQLAlchemy, uvicorn
- **Frontend:** React 18, TypeScript, Vite, TailwindCSS
- **Database:** Turso (libSQL) - Managed SQLite in the cloud
- **Deployment:** fly.io
- **Development:** Docker Compose

### Mobile App
- **Framework:** React Native / Flutter (TBD)
- **Database:** Turso local replica (offline-first)
- **Platform:** iOS (primary), Android (future)

### Documentation
- **Format:** AsciiDoc (arc42), Markdown (ADRs)
- **Build:** asciidoctor
- **Website:** Jekyll (GitHub Pages)

## 🤝 Contributing

1. Create a feature branch
2. Make your changes
3. Write/update tests
4. Update documentation (ADRs if architectural change)
5. Submit a Pull Request

## 📝 License

[Add your license here]

## 🔗 Links

- **Web App:** https://aquarius.arc42.org
- **Documentation:** https://gernotstarke.github.io/aquarius
- **Repository:** https://github.com/gernotstarke/aquarius

---

**Made with 🏊 in Cologne**

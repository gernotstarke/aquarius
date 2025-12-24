# Web App - Aquarius Desktop/Web Application

FastAPI Backend + React Frontend für die Aquarius Wettkampf-Verwaltung.

## 🚀 Quick Start

```bash
# Start development servers
make dev

# Access:
# - Frontend: http://localhost:5173
# - Backend API: http://localhost:8000
# - API Docs: http://localhost:8000/docs
```

## 📋 Available Commands

```bash
make help             # Show all available commands
make dev              # Start development servers
make dev-down         # Stop development servers
make test             # Run tests
make db-reset         # Reset database
make db-seed          # Seed with sample data
make deploy           # Deploy to fly.io
make deploy-status    # Check deployment status
make clean            # Clean build artifacts
```

## 🗄️ Database

**Local Development:** SQLite in Docker volume
**Production:** Turso (libSQL) - https://aquarius.arc42.org

### Seeding

```bash
# Full reset + sample data
make db-seed

# Import figures only
make db-import-figures FILE=backend/data/figuren/figuren-v1.0-saison-2024.json
```

## 🌐 Deployment

```bash
# Initial setup (one-time)
make deploy-setup

# Deploy to production
make deploy

# Monitor
make deploy-status
make deploy-logs
```

## 📁 Structure

```
web/
├── backend/           # FastAPI application
│   ├── app/          # Application code
│   ├── data/         # Seed data, figure catalogs
│   └── static/       # Static files (images)
├── frontend/         # React application
│   ├── src/          # Source code
│   └── public/       # Public assets
├── Dockerfile        # Production build
└── fly.toml          # fly.io config
```

## 🛠️ Tech Stack

- **Backend:** Python 3.11, FastAPI, SQLAlchemy, Pydantic
- **Frontend:** React 18, TypeScript, Vite, TailwindCSS, React Query
- **Database:** SQLite (dev), Turso/libSQL (prod)
- **Deployment:** fly.io, Docker

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

# If you see "(trapped) error reading bcrypt version",
# rebuild the backend image (bcrypt 4.x is incompatible with passlib 1.7.x).
# Example: docker compose build backend

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

## 🩺 Troubleshooting

### Seeding fails with "(trapped) error reading bcrypt version"
`passlib 1.7.x` expects `bcrypt.__about__.__version__`, which was removed in `bcrypt 4.x`.

Fix: rebuild the backend image so the pinned `bcrypt<4` is installed.
```bash
docker compose build backend
make db-seed
```

### `make db-seed` says the backend container is not running
The seed command runs inside the backend container.

Fix:
```bash
make dev
```

### Database is empty after seeding
Most often you’re using a different database than the app.

Fix: confirm the DB URL inside the backend container:
```bash
docker compose exec backend env | rg TURSO_DATABASE_URL
```

### `make db-import-figures` fails with file not found
The import runs inside the container, so use a path that exists there.

Fix:
```bash
make db-import-figures FILE=backend/data/figuren/figuren-v1.0-saison-2024.json
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

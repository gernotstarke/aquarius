# AGENTS.md - Aquarius Web Development Guide

This document helps agents work effectively in the Aquarius web repository. It contains project structure, essential commands, code patterns, and gotchas.

## Overview

**Aquarius** is a competitive swimming registration and management system with:
- **Backend**: Python FastAPI with SQLAlchemy ORM
- **Frontend**: React 18 with TypeScript, Vite, React Query, TailwindCSS
- **Database**: SQLite (local development) or Turso/libSQL (production)
- **Deployment**: fly.io with Docker Compose

**Repository**: `/Users/gernotstarke/projects/arc42/aquarius/web`

## Essential Commands

All commands are defined in the root `Makefile`. Run `make help` to see all available commands.

### Development

```bash
make dev              # Start both backend (8000) and frontend (5173) with local SQLite
make dev-with-turso   # Start with Turso cloud database instead
make dev-down         # Stop development servers
make clean            # Remove __pycache__, .vite, node_modules/.vite
```

**Access during development**:
- Frontend: http://localhost:5173
- Backend API: http://localhost:8000
- API Documentation: http://localhost:8000/docs

### Testing

```bash
make test             # Run backend pytest (auto-discovers tests/ directory)
make test-ui          # Run frontend Playwright E2E tests locally
```

**Important**: E2E tests run locally (not in Docker) due to ARM architecture limitations - see Makefile lines 30-51.

### Database Operations

```bash
make db-reset         # Delete all data and recreate tables (prompts for confirmation)
make db-seed          # Seed database with sample data
make db-init-admin    # Interactive admin user creation (production-safe)
make db-import-figures FILE=path/to/catalog.json  # Import figure catalog
make db-export-local  # Export local SQLite from Docker to backend/exports/
make db-export-turso  # Export Turso production database
```

### Deployment

```bash
make deploy           # Deploy to fly.io (prompts for confirmation)
make deploy-status    # Show deployment status and logs
make deploy-logs      # Stream live logs from fly.io
make deploy-ssh       # SSH into fly.io container
make deploy-rollback  # Rollback to previous deployment version
make deploy-setup     # Initial fly.io setup wizard
```

**Prerequisites for deploy**: flyctl installed, logged in, Turso database created, secrets configured.

## Project Structure

```
web/
├── backend/                  # FastAPI application
│   ├── app/
│   │   ├── main.py          # FastAPI app setup, middleware, SPA routing (IMPORTANT: routes in register order)
│   │   ├── database.py      # SQLAlchemy engine, session, Base (supports SQLite and Turso)
│   │   ├── auth.py          # Authentication, password hashing
│   │   ├── totp.py          # 2FA TOTP implementation
│   │   ├── version.py       # Backend version constant
│   │   ├── models/          # SQLAlchemy ORM models (Kind, Wettkampf, Anmeldung, etc.)
│   │   ├── schemas/         # Pydantic schemas for API validation
│   │   ├── routers/         # API routers (auth, users, health, admin)
│   │   ├── [domain]/        # Domain modules (kind, wettkampf, anmeldung, grunddaten, etc.)
│   │   │   ├── router.py    # API endpoints
│   │   │   ├── services.py  # Business logic
│   │   │   ├── repository.py # Data access layer
│   │   │   ├── schemas.py   # Pydantic schemas
│   │   │   ├── dtos.py      # Data Transfer Objects (if used)
│   │   │   └── mappers.py   # ORM model to DTO mapping
│   │   ├── shared/          # Shared utilities (repository base, services, schemas, utils)
│   │   └── seed_constants.py # Constants used by seed_db.py
│   ├── tests/
│   │   ├── conftest.py      # pytest fixtures (client, db, admin_token_headers)
│   │   ├── unit/            # Unit tests for models, database, rules
│   │   ├── services/        # Service layer tests
│   │   ├── repositories/    # Repository tests
│   │   ├── mappers/         # DTO mapper tests
│   │   ├── integration/     # Full integration tests
│   │   └── api/             # API endpoint tests
│   ├── data/
│   │   └── figuren/         # Figure/movement catalog (JSON + images)
│   ├── database/            # SQLite volume mount (git-ignored)
│   ├── exports/             # Database exports (git-ignored)
│   ├── static/              # Static files served by backend
│   ├── Dockerfile           # Backend Docker image
│   ├── requirements.txt     # Python dependencies
│   ├── pytest.ini           # pytest configuration
│   ├── seed_db.py           # Database seeding script
│   ├── init_admin.py        # Interactive admin user creation
│   ├── import_figures.py    # Figure catalog import script
│   └── .env / .env.local    # Environment configuration
│
├── frontend/                # React TypeScript application
│   ├── src/
│   │   ├── main.tsx         # React entry point
│   │   ├── App.tsx          # Main routing, QueryClient setup, Auth guard
│   │   ├── api/             # API client functions (axios-based)
│   │   ├── types/           # TypeScript type definitions
│   │   ├── pages/           # Page components (forms, lists, admin)
│   │   │   ├── __tests__/   # Page-level tests
│   │   │   └── admin/       # Admin pages (Login, TOTPSetup, Dashboard, etc.)
│   │   ├── components/      # Reusable UI components (Button, Input, Card, Tabs, etc.)
│   │   │   └── __tests__/   # Component tests
│   │   └── styles/          # TailwindCSS global styles
│   ├── tests/
│   │   ├── e2e/             # Playwright E2E tests
│   │   └── __tests__/       # Unit tests via Vitest
│   ├── public/              # Public assets (logo, favicon)
│   ├── Dockerfile           # Frontend Docker image (builds React app)
│   ├── package.json         # npm dependencies and scripts
│   ├── vite.config.ts       # Vite build config with API proxy
│   ├── vitest.config.ts     # Vitest configuration
│   ├── playwright.config.ts # Playwright configuration
│   ├── tsconfig.json        # TypeScript config
│   ├── tailwind.config.js   # TailwindCSS config
│   ├── postcss.config.js    # PostCSS config
│   └── index.html           # HTML entry point
│
├── Dockerfile               # Production build (multi-stage, builds both backend and frontend)
├── docker-compose.yml       # Development environment setup
├── fly.toml                 # fly.io deployment configuration
├── Makefile                 # Development commands
└── README.md               # User-facing quick start guide
```

## Code Patterns and Conventions

### Backend Python

#### Architecture Pattern: Layered with Domain Organization

The backend follows a **layered architecture with domain-driven organization**:

1. **Router Layer** (`routers/`, `*/router.py`):
   - FastAPI APIRouter endpoints
   - Parameter validation, HTTP status codes
   - Response models (Pydantic schemas or DTOs)
   - Example: `app/kind/router.py` - GET/POST/PUT/DELETE endpoints

2. **Service Layer** (`*/services.py`):
   - Business logic and validation rules
   - Methods return model instances or DTOs
   - Methods document complex logic in docstrings
   - Example: `app/kind/services.py` - `is_insured()`, `create_kind()`, `search_kinder()`

3. **Repository Layer** (`*/repository.py`):
   - Database queries and persistence
   - Methods return ORM model instances
   - Generic base repository in `app/shared/repository.py`
   - Example: `app/kind/repository.py` - query methods for Kind

4. **Models** (`models/`, `schemas/`):
   - SQLAlchemy ORM models: `app/models/user.py`, `app/models/original_models.py`
   - Pydantic schemas for input validation: `app/schemas/` (per-domain in domain folders)

5. **Data Transfer Objects (DTOs)** (`*/dtos.py`):
   - Subset of model data for API responses
   - Example: `app/kind/dtos.py` - `KindDTO` with specific fields
   - Mappers (`*/mappers.py`) convert ORM models to DTOs

#### Key Files to Understand

- **app/main.py**: FastAPI app initialization, CORS setup, router registration, SPA catch-all route (LAST route)
- **app/database.py**: SQLAlchemy engine setup (supports SQLite and Turso), session factory, Base declaration class
- **app/auth.py**: JWT token generation, password hashing (bcrypt), user validation
- **app/shared/repository.py**: Base repository class with common query methods

#### Naming Conventions

- **Models**: Singular, PascalCase (e.g., `Kind`, `Wettkampf`, `User`)
- **Schemas**: Pydantic class per action (e.g., `KindCreate`, `KindUpdate`, `KindRead`)
- **DTOs**: Full name ending in `DTO` (e.g., `KindDTO`)
- **Services**: Singular domain + `Service` (e.g., `KindService`)
- **Repositories**: Singular domain + `Repository` (e.g., `KindRepository`)
- **Endpoints**: Plural for collections, singular for resources (e.g., `/api/kind`, `/api/kind/{id}`)

#### Dependency Injection

Dependencies are injected via FastAPI `Depends()`:
```python
def get_kind_service(db: Session = Depends(get_db)) -> KindService:
    repo = KindRepository(db)
    return KindService(repo)

@router.get("/kind")
def list_kind(service: KindService = Depends(get_kind_service)):
    # ...
```

#### Database Configuration

- **Development**: Uses local SQLite (`backend/database/aquarius.db`) via `DATABASE_URL=sqlite:///./database/aquarius.db`
- **Production**: Uses Turso/libSQL (cloud) via `DATABASE_URL=libsql://aquarius-xyz.turso.io` + `TURSO_AUTH_TOKEN`
- **Turso Support**: Configured in `app/database.py` - automatically adapts connection based on URL prefix

### Frontend React/TypeScript

#### Architecture Pattern: Component-Based with Hooks

The frontend follows a **component-based architecture with React Hooks**:

1. **Pages** (`src/pages/`):
   - Main routed components (KindList, KindForm, WettkampfDetail, etc.)
   - Use hooks for state management (useState) and data fetching (useQuery, useMutation)
   - Route guard: `RequireAuth` component in App.tsx

2. **Components** (`src/components/`):
   - Reusable UI components (Button, Input, Card, Tabs, Sidebar, etc.)
   - Accept props, emit callbacks
   - Styled with TailwindCSS utility classes
   - Optional: Unit tests in `__tests__/`

3. **API Client** (`src/api/`):
   - Axios client with JWT token injection
   - Per-domain API functions (e.g., `api/kind.ts` exports `getKind()`, `listKind()`, `createKind()`)
   - Returns promises resolved/rejected based on HTTP status
   - No instance data caching (React Query handles that)

4. **Types** (`src/types/`):
   - TypeScript interfaces matching API schemas
   - Examples: `Kind`, `KindCreate`, `Wettkampf`, `Anmeldung`

#### Routing

Configured in `src/App.tsx` using **React Router v6**:
- All routes require admin auth token in localStorage
- `RequireAuth` guard redirects to `/admin/login` if no token
- Admin routes nested under `/admin`
- SPA catch-all on backend: FastAPI `/{full_path:path}` returns `index.html` for client-side routing

#### Data Fetching

Uses **React Query (TanStack Query)** with `useQuery` and `useMutation`:
```typescript
const { data: kind } = useQuery<Kind>({
  queryKey: ['kind', id],
  queryFn: () => getKind(Number(id)),
  enabled: isEdit,
});

const mutation = useMutation({
  mutationFn: (data: KindCreate) => createKind(data),
  onSuccess: () => {
    queryClient.invalidateQueries({ queryKey: ['kind'] });
    navigate('/kind');
  },
});
```

#### Styling

**TailwindCSS** only - no CSS files or styled-components:
- Use Tailwind utility classes directly in JSX
- Configure in `tailwind.config.js` (color schemes, plugins)
- PostCSS processes in `postcss.config.js`
- Global styles in `src/styles/index.css`

#### Naming Conventions

- **Components**: PascalCase (e.g., `KindForm`, `SaisonList`, `AdminLayout`)
- **API functions**: camelCase (e.g., `listKind`, `getKind`, `updateKind`)
- **Types/Interfaces**: PascalCase (e.g., `Kind`, `KindCreate`, `Wettkampf`)
- **Pages**: File name matches component name (e.g., `KindForm.tsx` exports `KindForm`)

#### Build

- **Dev**: `npm run dev` starts Vite dev server with API proxy (`/api` → `http://backend:8000`)
- **Build**: `npm run build` - runs TypeScript check, then builds to `dist/`
- **Preview**: `npm run preview` - serves built dist locally
- **Tests**: `npm run test` (unit tests with Vitest), `npm run test:e2e` (Playwright)

### API Design

#### Endpoints

Structured by domain with consistent patterns:
- **GET /api/{resource}**: List with pagination (skip, limit), search, sort
- **GET /api/{resource}/{id}**: Get single resource
- **POST /api/{resource}**: Create
- **PUT /api/{resource}/{id}**: Update
- **DELETE /api/{resource}/{id}**: Delete

#### Pagination Header

Responses include `X-Total-Count` header for total count (used by frontend for pagination UI).

#### Error Handling

- Backend returns **HTTPException** with status_code and detail
- Frontend handles errors in useMutation `onError` callback
- 401 errors trigger optional redirect to login (commented in client.ts)

### Testing

#### Backend Testing

- **Framework**: pytest with FastAPI TestClient
- **Database**: In-memory SQLite for tests (StaticPool, no persistence)
- **Fixtures** in `tests/conftest.py`:
  - `db`: Fresh in-memory database per test
  - `client`: FastAPI TestClient with DB dependency override
  - `admin_token_headers`: Admin user + JWT token for auth tests
- **Organization**: Tests mirror source structure (unit/, services/, repositories/, mappers/, integration/, api/)
- **Run**: `make test` or `docker compose exec backend pytest`

#### Frontend Testing

- **Unit Tests**: Vitest with React Testing Library
- **E2E Tests**: Playwright (local execution due to ARM Docker issues)
- **Run**: `npm run test` (unit), `make test-ui` (E2E)
- **Note**: E2E tests need running services (make dev + npm install + npx playwright install chromium)

## Database

### Schema and Models

Core entities:
- **User**: Admin/staff accounts with roles (ROOT, VERWALTER, etc.)
- **Kind**: Children in competition system
- **Wettkampf**: Swim competitions
- **Anmeldung**: Children's registration for competitions
- **Verein**: Swim clubs
- **Verband**: Associations
- **Versicherung**: Insurance providers
- **Saison**: Competition seasons
- **Schwimmbad**: Swimming pools
- **Figuren**: Movement figures/exercises

### Seeding

- `backend/seed_db.py`: Creates tables, inserts seed constants (Versicherung, Verband, etc.)
- `backend/import_figures.py`: Imports figure catalog from JSON (see `backend/data/figuren/`)
- Run via `make db-seed` or `make db-import-figures FILE=...`

### Foreign Keys

SQLite foreign keys must be explicitly enabled - done in `app/database.py` via `PRAGMA foreign_keys=ON`.

### Turso/libSQL

Remote database uses libSQL protocol:
- Connection string: `libsql://aquarius-xyz.turso.io?authToken=...`
- Converted to SQLAlchemy URL: `sqlite+libsql://aquarius-xyz.turso.io?secure=true`
- Auth token passed via `auth_token` connect arg
- Uses `sqlalchemy-libsql` and `libsql-client` libraries

## Important Gotchas and Patterns

### 1. Route Registration Order (Backend)

**In `app/main.py`**, API routes must be registered **BEFORE** the SPA catch-all route (`/{full_path:path}`). The catch-all returns `index.html` for any unmatched path, so it must be last. Otherwise, API requests will get HTML instead of JSON.

### 2. Frontend Build Required for Production

The production Dockerfile builds the frontend (`npm run build`) and mounts `dist/` to backend. During development, frontend runs separately. If backend doesn't find `frontend/dist`, it falls back to serving JSON API info at `/`.

### 3. Environment Configuration

- **Backend**: Reads `.env` or `.env.local` (via `ENV_FILE` variable in docker-compose.yml)
- **Python**: Uses `python-dotenv` to load `.env` into `os.environ`
- **Frontend**: Environment variables prefixed with `VITE_` are injectable; others compile-time only
- **Production**: Secrets set via `flyctl secrets set` (not committed to repo)

### 4. CORS Configuration

Backend CORS middleware allows:
- `http://localhost:5173` (dev frontend)
- `https://aquarius.fly.dev` (old production)
- `https://aquarius.arc42.org` (current production + docs site)
- All methods/headers/credentials

If frontend is on a different origin, update CORS list in `app/main.py`.

### 5. Database Transactions

SQLAlchemy sessions are per-request (dependency injection). Commits happen automatically at end of request if no error. For manual control, use `db.commit()` explicitly.

### 6. JWT Token Storage

Frontend stores JWT in `localStorage['token']`. No automatic refresh; token must be valid for entire session. On 401 response, token is likely expired (frontend can redirect to login).

### 7. ARM Architecture Limitation

Playwright E2E tests cannot run in Docker on ARM (Apple Silicon). They run locally instead - see `make test-ui` which requires local npm install and chromium. Backend/frontend Docker services run fine on ARM via proper base images.

### 8. Docker Compose Healthcheck

Backend has a healthcheck that polls `/api/health`. Frontend depends on backend being healthy (`service_healthy` condition). This ensures backend is ready before frontend tries to connect.

### 9. Static Files

- **Backend**: Serves `/static/` from `backend/static/` directory (for backend-specific files)
- **Frontend**: Serves `/assets/` from `frontend/dist/assets/` (built Vite output)
- **Public Assets**: In `frontend/public/` during dev; copied to `dist/` during build

### 10. TypeScript Strict Mode

Frontend uses strict TypeScript - all types must be explicit, no implicit `any`. If type is unknown, use union types or generics:
```typescript
const { data: kind } = useQuery<Kind>({...});  // Type is Kind
const [value, setValue] = useState<string>(''); // Type is string
```

### 11. Pydantic Schema Validation

Backend uses Pydantic v2 for input validation. Validation errors return 422 status with detailed field errors. Custom validators use `@field_validator` (not deprecated `@validator`).

### 12. ORM Model to DTO Pattern

For endpoints returning multiple fields or related data, map ORM models to DTOs:
```python
# Router
results = service.search_kinder(...)
return map_kinder_to_dtos(results)  # ORM models → DTOs
```

This decouples API schema from database schema and allows data transformation.

### 13. Admin Authentication

Admin pages require login at `/admin/login`. The login endpoint (`POST /api/auth/token`) returns JWT token, which frontend stores and includes in all subsequent requests via `Authorization: Bearer {token}` header.

## Debugging Tips

### Backend

1. **Enable SQL logging**: Set `echo=True` in `app/database.py` `create_engine()`
2. **Print debug info**: Use `logger.info()` (logging is configured in `main.py`)
3. **Test endpoints**: Use FastAPI `/docs` UI at http://localhost:8000/docs
4. **Database inspection**: `docker compose exec backend sqlite3 database/aquarius.db` (for local SQLite)
5. **Inspect requests**: Check `docker compose logs backend`

### Frontend

1. **React Query DevTools**: Not configured by default, but can add `import { ReactQueryDevtools } from '@tanstack/react-query-devtools'`
2. **Network tab**: Use browser DevTools to inspect API requests/responses
3. **Component state**: React DevTools browser extension useful for inspecting props/state
4. **Console logs**: `console.log()` in components/functions
5. **Vite logging**: Vite outputs to console during dev server startup

## Common Tasks

### Adding a New API Endpoint

1. Create model in `app/models/` or use existing
2. Create schema in `app/{domain}/schemas.py`
3. Create repository method in `app/{domain}/repository.py`
4. Add business logic in `app/{domain}/services.py`
5. Add router function in `app/{domain}/router.py`
6. Test with `make test` or FastAPI `/docs` UI
7. Add frontend API function in `frontend/src/api/{domain}.ts`
8. Add TypeScript type in `frontend/src/types/{domain}.ts`
9. Use in component with `useQuery`/`useMutation`

### Adding a New Page

1. Create component in `frontend/src/pages/{Page}.tsx`
2. Add route in `frontend/src/App.tsx`
3. Add navigation link if needed
4. Use existing components (Input, Button, Card) for consistency
5. Call API functions from `src/api/`
6. Test with `npm run test` or manual browser testing

### Deploying to Production

1. Ensure all tests pass: `make test && make test-ui`
2. Push to main branch (CI/CD can be added)
3. Run `make deploy` (will prompt, connects to fly.io)
4. Monitor with `make deploy-status` and `make deploy-logs`

### Exporting Database

- Local: `make db-export-local` → `backend/exports/aquarius-local-TIMESTAMP.db`
- Production: `make db-export-turso` → `backend/exports/aquarius-turso-TIMESTAMP.sql` (requires turso CLI)

## Performance Considerations

1. **React Query Caching**: Queries are cached for 30 seconds (staleTime) by default - configure in `App.tsx`
2. **SQL Indexes**: Add to frequently queried columns for large datasets
3. **Pagination**: Use `skip` and `limit` parameters to avoid loading entire tables
4. **Frontend Bundle**: Vite automatically code-splits components; monitor with `npm run build`
5. **Database Queries**: Avoid N+1 problems - use SQLAlchemy `joinedload()` or `selectinload()`

## Security Notes

- **Passwords**: Hashed with bcrypt (passlib library)
- **JWT Tokens**: Signed with secret key (set via environment variable)
- **CORS**: Restricted to known origins
- **HTTPS**: Production enforces HTTPS (configured in fly.toml)
- **Admin Routes**: Protected with token verification
- **TOTP 2FA**: Implemented for additional admin account security

## Version and Build Info

- **Backend Version**: Defined in `app/version.py` (exposed via `/api/health` and `/api/status`)
- **Python**: 3.11 (see Dockerfile)
- **Node**: Latest LTS (see frontend Dockerfile)
- **FastAPI**: 0.109.0
- **React**: 18.2.0

## Useful Resources

- **FastAPI Docs**: http://localhost:8000/docs (interactive API testing)
- **FastAPI Tutorial**: https://fastapi.tiangolo.com/
- **React Query Docs**: https://tanstack.com/query/latest
- **Tailwind Docs**: https://tailwindcss.com/docs
- **SQLAlchemy Docs**: https://docs.sqlalchemy.org/
- **Playwright Docs**: https://playwright.dev/python/

## Configuration Files Reference

| File | Purpose |
|------|---------|
| `Makefile` | Development commands |
| `docker-compose.yml` | Local dev environment (backend, frontend, volumes) |
| `Dockerfile` | Production multi-stage build (backend + frontend) |
| `fly.toml` | fly.io deployment config |
| `backend/requirements.txt` | Python dependencies |
| `frontend/package.json` | Node dependencies and scripts |
| `frontend/vite.config.ts` | Vite build and dev config |
| `frontend/vitest.config.ts` | Vitest unit test config |
| `frontend/playwright.config.ts` | Playwright E2E test config |
| `frontend/tailwind.config.js` | TailwindCSS customization |
| `backend/pytest.ini` | pytest configuration |
| `backend/.env` / `backend/.env.local` | Environment variables (git-ignored) |
| `.env`, `.env.local` | Docker Compose environment (git-ignored) |

---

**Last Updated**: January 8, 2026

For questions or updates to this guide, refer to the project README.md or check recent commits in git log.

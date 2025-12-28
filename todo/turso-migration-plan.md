# Turso Migration Plan (Stepwise)

This plan outlines the steps to migrate the backend database from standard SQLite to Turso (libSQL), starting with a local libSQL server instance.

## Phase 1: Local libSQL Integration

### Step 1: Add Python Dependencies
Update `web/backend/requirements.txt` to include the necessary libraries for connecting to libSQL via SQLAlchemy.
*   **Add**: `libsql-client`
*   **Add**: `sqlalchemy-libsql`

### Step 2: Update Database Configuration
Modify `web/backend/app/database.py` to handle `libsql://` connection strings and authentication tokens.
*   **Update**: `create_engine` logic to check for `libsql://` prefix.
*   **Update**: Pass `auth_token` if provided in environment variables.
*   **Maintain**: Fallback to standard `sqlite:///` for backward compatibility during migration.

### Step 3: Run Local libSQL Server
Use Docker to run a local instance of `sqld` (libSQL server) to simulate the Turso environment locally.
*   **Command**: `docker run -p 8080:8080 -ti ghcr.io/tursodatabase/libsql-server:latest`
*   **Goal**: Verify the backend can connect to a libSQL server over HTTP.

### Step 4: Verify Connection & Migration
*   **Update Env**: Set `DATABASE_URL=libsql://localhost:8080` in `.env` (or temporary export).
*   **Run**: `make db-reset` (or `python seed_db.py`) to verify table creation and data seeding works against the local libSQL server.
*   **Test**: Run existing tests or manual curl requests to ensure API functionality.

## Phase 2: Turso Cloud Integration (Future)

*   Create Turso Database (`turso db create`).
*   Get URL and Auth Token.
*   Update production/staging environment variables.
*   Deploy and Verify.

---

**Next Action:** Execute Step 1 (Add Python Dependencies).

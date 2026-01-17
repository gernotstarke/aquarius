# E2E Test Authentication Setup

## Overview

This document describes the authentication setup for Playwright E2E tests. Tests are automatically authenticated to focus on business logic rather than login flows.

## Architecture

### Test User Lifecycle

1. **globalSetup** (runs once before all tests)
   - Creates ephemeral test user via `backend/tests/test_user_cli.py`
   - Obtains JWT token from backend
   - Saves token to `frontend/.auth/token.json`

2. **Each Test** (using `auth.fixture.ts`)
   - Loads token from `.auth/token.json`
   - Injects token into `localStorage` before navigation
   - Tests run fully authenticated

3. **globalTeardown** (runs once after all tests)
   - Deletes ephemeral test user
   - Cleans up `.auth/token.json`

### Test User Details

- **Username**: `e2e_test_user`
- **Password**: `test_password_123`
- **Role**: `APP_USER` (full app permissions)
- **Permissions**: `can_read_all=true`, `can_write_all=true`
- **Scope**: Ephemeral (created/destroyed per test run)

## Implementation Files

### Backend

**`backend/tests/test_user_cli.py`**
- CLI helper for test user management
- Commands:
  - `create [username] [password]` - Create test user
  - `delete [username]` - Delete test user
  - `token [username] [password]` - Get JWT token

### Frontend

**`playwright.config.ts`**
- Added `globalSetup` and `globalTeardown` hooks

**`playwright-globalSetup.ts`**
- Runs before all tests
- Creates test user and obtains JWT token
- Saves token to `.auth/token.json`

**`playwright-globalTeardown.ts`**
- Runs after all tests
- Cleans up test user and `.auth/token.json`

**`tests/e2e/auth.fixture.ts`**
- Extends Playwright's `test` fixture
- Injects JWT token into localStorage before each test
- All tests automatically use this fixture

**`tests/e2e/*.spec.ts`**
- Updated to import from `auth.fixture.ts` instead of `@playwright/test`
- No other changes needed - tokens are injected transparently

## Usage

### Running Tests

```bash
make test-ui
```

This command:
1. Starts Docker services (backend + frontend)
2. Waits for backend to be healthy
3. Runs `npm run test:e2e` with authenticated setup

### Test Environment

- Backend runs in Docker with SQLite database
- Tests run locally (Playwright)
- Tests connect to `http://localhost:5173` (frontend)
- Tokens injected into `localStorage` automatically

## Future: Limited-Access User Tests

When implementing tests for limited-access users (e.g., students who can only edit their own data):

1. Modify `auth.fixture.ts` to support multiple user roles:
   ```typescript
   const test = base.extend({
     page: async ({ page }, use) => {
       const token = loadToken(userRole); // Pass role parameter
       await injectAuthToken(page, token);
       await use(page);
     },
   });
   ```

2. Extend `test_user_cli.py` to support different roles:
   ```bash
   python tests/test_user_cli.py create kind_user test_password kind_role
   ```

3. Update globalSetup to create multiple test users as needed

## Troubleshooting

### Auth file not found
```
Error: Auth file not found at .../frontend/.auth/token.json
```
- Ensure globalSetup ran successfully (check logs)
- Check if Docker services are running
- Verify backend is healthy

### Failed to create test user
- Check backend logs: `docker compose logs backend`
- Ensure database migrations have run
- Verify `backend/tests/test_user_cli.py` exists

### Token injection fails
- Check browser console for `localStorage` errors
- Verify token format is valid JWT
- Ensure frontend is loading from correct URL

## Notes

- Test users are ephemeral - they don't persist between test runs
- Using a single test user for all tests keeps setup simple and fast
- Token expires after 24 hours (configured in backend)
- No 2FA required for E2E test users

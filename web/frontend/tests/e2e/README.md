# E2E Test Suite

## Overview

This directory contains end-to-end tests for the Aquarius frontend application using Playwright.

## Test Categories

### 1. Smoke Tests (`smoke.spec.ts`) ✅
**Status:** All passing (6/6)

Basic page load and navigation tests:
- Home page loads with navigation
- Grunddaten page shows tiles
- Kinder list page loads
- Wettkämpfe list page loads
- Anmeldungen list page loads
- Figuren list page loads

### 2. Workflow Tests (`workflows.spec.ts`) ⚠️
**Status:** Failing due to timing issues (0/1)

Tests complete user workflows:
- Kind → Anmeldung creation workflow

**Known Issues:**
- Kind doesn't immediately appear in select dropdowns after creation
- Needs better wait conditions or reload logic

### 3. Business Rule Tests (`business-rules.spec.ts`) ⚠️
**Status:** Partially implemented (1/4 passing)

Critical domain logic tests for DDD migration:

#### Passing:
- ✅ **Kind list shows Verein names not IDs** - Verifies eager loading works

#### Failing (timing/selection issues):
- ❌ **Anmeldung without insurance is vorläufig** - Tests insurance business rule
- ❌ **Anmeldung without figuren is vorläufig** - Tests figuren requirement rule
- ❌ **Wettkampf details shows Kind names** - Tests cross-aggregate data loading

**Root Cause:** Newly created Kinder don't immediately appear in dropdown selections on Anmeldung form. Likely causes:
- Cache/state sync issue
- API response timing
- Need for explicit page reload after creation

## Running Tests

```bash
# From project root
make test-ui

# Or directly (requires Playwright browsers installed)
cd frontend
PLAYWRIGHT_BASE_URL=http://localhost:5173 npm run test:e2e

# Run specific test file
npx playwright test smoke.spec.ts

# Run with UI
npx playwright test --ui
```

## First-Time Setup

```bash
cd frontend
npm install
npx playwright install chromium
```

## Test Architecture

- **Base URL:** `http://localhost:5173` (configurable via `PLAYWRIGHT_BASE_URL`)
- **Timeouts:** 30s test timeout, 5s expect timeout
- **Traces:** Retained on failure for debugging
- **Screenshots:** Captured on failure

## Why Business Rule Tests Matter for DDD

These tests verify critical domain invariants that will be preserved during DDD refactoring:

1. **Vorläufig Status Logic** - Will move into `AnmeldungAggregate`
   - No insurance → vorläufig
   - No figuren → vorläufig
   - Both present → final (aktiv)

2. **Cross-Aggregate Queries** - Will use repositories
   - Wettkampf showing Anmeldungen with Kind details
   - Proper eager loading vs N+1 queries

3. **Entity Relationships** - Will become aggregate boundaries
   - Kind as part of Anmeldung aggregate?
   - Wettkampf as separate aggregate root

## TODO: Fix Failing Tests

### Immediate fixes needed:

1. **Add explicit reload after Kind creation**
   ```typescript
   await page.goto('/kind/new');
   // ... create kind ...
   await page.goto('/kind'); // Reload list
   await page.waitForLoadState('networkidle');
   ```

2. **Use more robust selectors for dropdowns**
   - Wait for specific option count
   - Retry selection logic
   - Add explicit waitFor with longer timeouts

3. **Consider API-level test data setup**
   - Create test data via API calls instead of UI
   - Reduces brittleness
   - Faster execution

### Alternative approach:

Create **API-driven E2E tests** that:
1. Set up data via direct API calls
2. Test only the UI display logic
3. Much more reliable and faster

Example:
```typescript
test('vorläufig status displays correctly', async ({ page, request }) => {
  // Setup via API
  const kind = await request.post('/api/kind', { data: {...} });
  const anmeldung = await request.post('/api/anmeldung', {
    data: { kind_id: kind.id, /* no figuren */ }
  });

  // Test UI
  await page.goto('/anmeldung/liste');
  await expect(page.locator(`[data-anmeldung-id="${anmeldung.id}"]`))
    .toContainText('vorläufig');
});
```

## Current Test Coverage

- **Backend API:** 33/33 tests passing ✅
- **Frontend E2E:**
  - Smoke tests: 6/6 passing ✅
  - Workflow tests: 0/1 passing ⚠️
  - Business rules: 1/4 passing ⚠️

**Total E2E:** 7/11 passing (64%)

## Recommendations

### For DDD Migration:

**Priority 1:** Fix the 3 failing business rule tests
- Critical for ensuring domain logic survives refactoring
- Documents expected behavior
- Acts as regression safety net

**Priority 2:** Add backend integration tests for business rules
- Test vorläufig calculation logic directly
- Test wettkampf capacity limits
- Test cascade delete behavior

**Priority 3:** Expand E2E coverage after DDD
- Test new aggregate boundaries
- Test repository query patterns
- Test domain events (if implemented)

### For Test Reliability:

1. **Use Page Object Model** - Encapsulate selectors and wait logic
2. **API Test Data Setup** - Don't rely on UI for test data creation
3. **Add data-testid attributes** - Make selectors more stable
4. **Increase wait times** - Frontend is slow to hydrate data
5. **Add retry logic** - Handle flaky network/timing issues

## Notes

- Tests run **locally** (not in Docker) due to ARM/Playwright compatibility issues
- See ADR-029 (when created) for Docker testing strategy
- Backend/Frontend must be running for tests to execute
- `make test-ui` handles service startup automatically

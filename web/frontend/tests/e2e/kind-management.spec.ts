import { test, expect } from '@playwright/test';

/**
 * Kind Management E2E Tests - Tests DDD Frontend Slicing
 *
 * These tests verify that the frontend domain structure (API services + types)
 * works correctly with real backend APIs.
 *
 * Tests the Kind domain end-to-end:
 * - Create Kind via UI
 * - Search and filter Kind
 * - Update Kind details
 * - Verify insurance logic
 * - Delete Kind
 */

test.describe('Kind Management Workflow', () => {
  // Store created IDs for cleanup
  const createdIds: { kind: number[]; verein: number[] } = { kind: [], verein: [] };

  test.afterAll(async ({ request }) => {
    // Cleanup any created entities, regardless of test success/failure
    for (const id of createdIds.kind) {
      await request.delete(`http://localhost:8000/api/kind/${id}`).catch(() => {});
    }
    for (const id of createdIds.verein) {
      await request.delete(`http://localhost:8000/api/verein/${id}`).catch(() => {});
    }
  });

  test('create, search, edit, and delete kind', async ({ page, request }) => {
    const timestamp = Date.now();
    const uniqueName = `E2E-Kind-${timestamp}`;

    // Step 1: Create prerequisite data (Verein) via API
    const vereinResponse = await request.post('http://localhost:8000/api/verein', {
      data: {
        name: `Test Verein ${timestamp}`,
        ort: 'Berlin',
        register_id: `REG-${timestamp}`,
        contact: 'test@verein.de'
      }
    });
    expect(vereinResponse.ok()).toBeTruthy();
    const verein = await vereinResponse.json();
    createdIds.verein.push(verein.id);

    // Step 2: Create Kind via UI
    await page.goto('/kind/new');
    await page.waitForLoadState('networkidle');

    await page.fill('input[name="vorname"]', uniqueName);
    await page.fill('input[name="nachname"]', 'AAA-E2E-Test');
    await page.fill('input[name="geburtsdatum"]', '2012-06-15');
    await page.selectOption('select[name="geschlecht"]', 'M');
    await page.selectOption('select[name="verein_id"]', verein.id.toString());

    await page.click('button[type="submit"]');
    await page.waitForURL('/kind');

    // We need to fetch the ID of the created Kind for cleanup
    // We can infer it by searching for it
    const searchResponse = await request.get('http://localhost:8000/api/kind', {
      params: { search: uniqueName }
    });
    if (searchResponse.ok()) {
      const results = await searchResponse.json();
      if (results.length > 0) {
        createdIds.kind.push(results[0].id);
      }
    }

    // Step 3: Verify Kind appears in list with insurance indicator
    await page.goto('/kind');
    await page.waitForLoadState('networkidle');

    const kindRow = page.locator('a').filter({ hasText: uniqueName });
    await expect(kindRow).toBeVisible();

    // Verify Kind has insurance (green dot) because of Verein
    const kindCard = page.locator('div').filter({ hasText: uniqueName }).first();
    const greenDot = kindCard.locator('.bg-green-200');
    await expect(greenDot).toBeVisible();

    // Step 4: Test search functionality
    await page.fill('input[placeholder*="Suche"]', uniqueName);
    await page.waitForTimeout(500); // Debounce

    // Should still show our Kind
    await expect(kindRow).toBeVisible();

    // Search for non-existent kind
    await page.fill('input[placeholder*="Suche"]', 'NonExistentKind123');
    await page.waitForTimeout(500);
    await expect(page.locator('text=/Keine Kinder gefunden/i')).toBeVisible();

    // Clear search
    await page.fill('input[placeholder*="Suche"]', '');
    await page.waitForTimeout(500);

    // Step 5: Edit Kind details
    await page.goto('/kind');
    await page.waitForLoadState('networkidle');

    const editButton = page.locator('a').filter({ hasText: uniqueName })
      .locator('..').locator('..').locator('button', { hasText: 'Bearbeiten' });
    await editButton.click();
    await page.waitForLoadState('networkidle');

    // Update nachname
    await page.fill('input[name="nachname"]', 'UpdatedTestperson');
    await page.click('button[type="submit"]');
    await page.waitForURL('/kind');

    // Verify update
    await page.goto('/kind');
    await page.waitForLoadState('networkidle');
    await expect(page.locator('text=UpdatedTestperson')).toBeVisible();

    // Step 6: Delete Kind
    await page.goto('/kind');
    await page.waitForLoadState('networkidle');

    const deleteButton = page.locator('a').filter({ hasText: uniqueName })
      .locator('..').locator('..').locator('button', { hasText: 'Löschen' });

    // Handle confirmation dialog
    page.on('dialog', dialog => dialog.accept());
    await deleteButton.click();

    // Wait for deletion
    await page.waitForTimeout(1000);

    // Verify Kind is gone
    await page.goto('/kind');
    await page.waitForLoadState('networkidle');
    await expect(page.locator('a').filter({ hasText: uniqueName })).not.toBeVisible();
  });

  test('insurance logic displays correctly', async ({ page, request }) => {
    const timestamp = Date.now();

    // Test 1: Kind with Verein (insured)
    const vereinResponse = await request.post('http://localhost:8000/api/verein', {
      data: {
        name: `Insurance Test Verein ${timestamp}`,
        ort: 'Munich',
        register_id: `INS-${timestamp}`,
        contact: 'insurance@test.de'
      }
    });
    const verein = await vereinResponse.json();
    createdIds.verein.push(verein.id);

    const insuredKindResponse = await request.post('http://localhost:8000/api/kind', {
      data: {
        vorname: `Insured-${timestamp}`,
        nachname: 'AAA-E2E-Insurance-Test',
        geburtsdatum: '2013-03-20',
        verein_id: verein.id
      }
    });
    const insuredKind = await insuredKindResponse.json();
    createdIds.kind.push(insuredKind.id);

    // Test 2: Kind without any insurance
    const uninsuredKindResponse = await request.post('http://localhost:8000/api/kind', {
      data: {
        vorname: `Uninsured-${timestamp}`,
        nachname: 'AAA-E2E-Insurance-Test',
        geburtsdatum: '2013-03-20'
      }
    });
    const uninsuredKind = await uninsuredKindResponse.json();
    createdIds.kind.push(uninsuredKind.id);

    // Verify UI shows insurance status correctly
    await page.goto('/kind');
    await page.waitForLoadState('networkidle');

    // Insured Kind should have green dot
    const insuredCard = page.locator('div').filter({ hasText: `Insured-${timestamp}` }).first();
    await expect(insuredCard.locator('.bg-green-200')).toBeVisible();

    // Uninsured Kind should have red dot
    const uninsuredCard = page.locator('div').filter({ hasText: `Uninsured-${timestamp}` }).first();
    await expect(uninsuredCard.locator('.bg-red-500')).toBeVisible();
  });

  test('sorting and pagination work correctly', async ({ page, request }) => {
    const timestamp = Date.now();

    // Create multiple Kinder with predictable names
    const kinderPromises = ['Anna', 'Bernd', 'Clara'].map(name =>
      request.post('http://localhost:8000/api/kind', {
        data: {
          vorname: `${name}-Sort-${timestamp}`,
          nachname: 'AAA-E2E-Sort-Test',
          geburtsdatum: '2014-01-01'
        }
      })
    );

    const kinderResponses = await Promise.all(kinderPromises);
    const kinder = await Promise.all(kinderResponses.map(r => r.json()));
    kinder.forEach(k => createdIds.kind.push(k.id));

    // Navigate to Kind list
    await page.goto('/kind');
    await page.waitForLoadState('networkidle');

    // Test sorting by Vorname (ascending - default)
    await page.selectOption('select[name="sort_by"]', 'vorname');
    await page.waitForTimeout(500);

    // Verify Anna appears before Clara
    const kinderList = await page.locator('a[href^="/kind/"]').allTextContents();
    const annaIndex = kinderList.findIndex(text => text.includes(`Anna-Sort-${timestamp}`));
    const claraIndex = kinderList.findIndex(text => text.includes(`Clara-Sort-${timestamp}`));
    expect(annaIndex).toBeGreaterThanOrEqual(0);
    expect(claraIndex).toBeGreaterThan(annaIndex);

    // Test sorting order toggle
    await page.click('button:has-text("Aufsteigend")');
    await page.waitForTimeout(500);
    await expect(page.locator('button:has-text("Absteigend")')).toBeVisible();
  });
});

test.describe('Kind API Integration', () => {
  // Store created IDs for cleanup
  const createdIds: { kind: number[] } = { kind: [] };

  test.afterAll(async ({ request }) => {
     for (const id of createdIds.kind) {
      await request.delete(`http://localhost:8000/api/kind/${id}`).catch(() => {});
    }
  });

  test('frontend API service communicates correctly with backend', async ({ request }) => {
    const timestamp = Date.now();

    // This test verifies that the frontend API service structure
    // (created in step 7 of DDD migration) works with real backend

    // Test Create
    const createResponse = await request.post('http://localhost:8000/api/kind', {
      data: {
        vorname: `API-Test-${timestamp}`,
        nachname: 'Integration',
        geburtsdatum: '2015-08-10'
      }
    });
    expect(createResponse.ok()).toBeTruthy();
    const created = await createResponse.json();
    createdIds.kind.push(created.id);
    
    expect(created.id).toBeDefined();
    expect(created.vorname).toBe(`API-Test-${timestamp}`);

    // Test Read
    const getResponse = await request.get(`http://localhost:8000/api/kind/${created.id}`);
    expect(getResponse.ok()).toBeTruthy();
    const fetched = await getResponse.json();
    expect(fetched.id).toBe(created.id);

    // Test List with pagination
    const listResponse = await request.get('http://localhost:8000/api/kind', {
      params: {
        skip: 0,
        limit: 10,
        sort_by: 'vorname',
        sort_order: 'asc'
      }
    });
    expect(listResponse.ok()).toBeTruthy();
    const list = await listResponse.json();
    expect(Array.isArray(list)).toBeTruthy();
    expect(listResponse.headers()['x-total-count']).toBeDefined();

    // Test Update
    const updateResponse = await request.put(`http://localhost:8000/api/kind/${created.id}`, {
      data: {
        nachname: 'Updated'
      }
    });
    expect(updateResponse.ok()).toBeTruthy();
    const updated = await updateResponse.json();
    expect(updated.nachname).toBe('Updated');

    // Test Delete
    const deleteResponse = await request.delete(`http://localhost:8000/api/kind/${created.id}`);
    expect(deleteResponse.ok()).toBeTruthy();

    // Verify deletion
    const verifyResponse = await request.get(`http://localhost:8000/api/kind/${created.id}`);
    expect(verifyResponse.status()).toBe(404);
  });
});
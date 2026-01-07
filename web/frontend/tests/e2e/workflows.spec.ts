import { test, expect } from '@playwright/test';

/**
 * Workflow Tests - Complete Business Workflows
 *
 * Strategy: Use API to set up test data for reliability, then verify UI displays correctly.
 * This approach is more stable than UI-driven data creation while still testing workflows.
 */

test.describe('Kind and Anmeldung Workflow', () => {
  test('complete kind → anmeldung workflow displays correctly', async ({ page, request }) => {
    const timestamp = Date.now();
    const kindVorname = `Workflow-${timestamp}`;

    // Step 1: Create complete workflow data via API (more reliable)
    // Create Verein
    const vereinResponse = await request.post('http://localhost:8000/api/verein', {
      data: {
        name: 'Workflow Verein',
        ort: 'Stuttgart',
        register_id: `REG-WF-${timestamp}`,
        contact: 'workflow@test.de'
      }
    });
    const verein = await vereinResponse.json();

    // Create Kind
    const kindResponse = await request.post('http://localhost:8000/api/kind', {
      data: {
        vorname: kindVorname,
        nachname: 'E2E-Workflow',
        geburtsdatum: '2015-05-15',
        geschlecht: 'M',
        verein_id: verein.id
      }
    });
    const kind = await kindResponse.json();

    // Create Saison, Schwimmbad, Wettkampf
    const saisonResponse = await request.post('http://localhost:8000/api/saison', {
      data: {
        name: `Workflow Saison ${timestamp}`,
        from_date: '2024-01-01',
        to_date: '2024-12-31'
      }
    });
    const saison = await saisonResponse.json();

    const schwimmbadResponse = await request.post('http://localhost:8000/api/schwimmbad', {
      data: {
        name: `Workflow Schwimmbad ${timestamp}`,
        adresse: 'Workflow Str. 1'
      }
    });
    const schwimmbad = await schwimmbadResponse.json();

    const wettkampfResponse = await request.post('http://localhost:8000/api/wettkampf', {
      data: {
        name: `Workflow Wettkampf ${timestamp}`,
        datum: '2024-09-15',
        saison_id: saison.id,
        schwimmbad_id: schwimmbad.id
      }
    });
    const wettkampf = await wettkampfResponse.json();

    // Create Anmeldung (without figuren - creates vorläufig)
    const anmeldungResponse = await request.post('http://localhost:8000/api/anmeldung', {
      data: {
        kind_id: kind.id,
        wettkampf_id: wettkampf.id,
        figur_ids: []
      }
    });
    const anmeldung = await anmeldungResponse.json();

    // Step 2: Verify UI displays the complete workflow correctly

    // Test 1: Anmeldung list shows Kind name with vorläufig status
    await page.goto('/anmeldung/liste');
    await page.waitForLoadState('networkidle');

    const anmeldungRow = page.locator('a').filter({ hasText: kindVorname });
    await expect(anmeldungRow).toBeVisible();

    // Verify vorläufig status (no figuren → vorläufig business rule)
    await expect(anmeldungRow.getByText(/vorläufig|Vorläufig/i).first()).toBeVisible();

    // Test 2: Wettkampf details page properly displays data with eager loading
    await page.goto(`/wettkampf/${wettkampf.id}`);
    await page.waitForLoadState('networkidle');

    // Core business rule: No "Kind-ID:" text should appear (proper eager loading)
    const hasKindIdText = await page.locator('text=/Kind-ID:\\s*\\d+/').count();
    expect(hasKindIdText).toBe(0);

    // Test 3: Verify Verein also eager loads correctly on Kind (cross-reference check)
    await page.goto('/kind');
    await page.waitForLoadState('networkidle');

    // Should not see "Verein-ID:" text
    const hasVereinIdText = await page.locator('text=/Verein-ID:\\s*\\d+/').count();
    expect(hasVereinIdText).toBe(0);

    // Complete workflow verified: Kind → Anmeldung → Wettkampf data flow works with proper eager loading
  });
});

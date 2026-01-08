import { test, expect } from '@playwright/test';

/**
 * Wettkampf & Anmeldung E2E Tests - Complex Nested Data
 *
 * Tests the DDD frontend slicing with complex nested relationships:
 * - Wettkampf → Saison, Schwimmbad
 * - Anmeldung → Kind, Wettkampf, Figuren
 *
 * Verifies that the domain-specific API services handle nested data correctly.
 */

test.describe('Wettkampf and Anmeldung Flow', () => {
  // Store created IDs for cleanup
  // Order matters for deletion due to Foreign Keys:
  // Anmeldung -> Wettkampf -> (Kind, Saison, Schwimmbad, Verein, Figur)
  const createdIds: { 
    anmeldung: number[], 
    wettkampf: number[], 
    kind: number[], 
    verein: number[],
    saison: number[],
    schwimmbad: number[],
    figur: number[] 
  } = { 
    anmeldung: [], 
    wettkampf: [], 
    kind: [], 
    verein: [],
    saison: [],
    schwimmbad: [],
    figur: [] 
  };

  test.afterAll(async ({ request }) => {
    // Cleanup in correct order to avoid Foreign Key Constraint errors
    for (const id of createdIds.anmeldung) await request.delete(`http://localhost:8000/api/anmeldung/${id}`).catch(() => {});
    for (const id of createdIds.wettkampf) await request.delete(`http://localhost:8000/api/wettkampf/${id}`).catch(() => {});
    for (const id of createdIds.kind) await request.delete(`http://localhost:8000/api/kind/${id}`).catch(() => {});
    for (const id of createdIds.verein) await request.delete(`http://localhost:8000/api/verein/${id}`).catch(() => {});
    for (const id of createdIds.figur) await request.delete(`http://localhost:8000/api/figur/${id}`).catch(() => {});
    for (const id of createdIds.schwimmbad) await request.delete(`http://localhost:8000/api/schwimmbad/${id}`).catch(() => {});
    for (const id of createdIds.saison) await request.delete(`http://localhost:8000/api/saison/${id}`).catch(() => {});
  });

  test('create wettkampf and register kind with figuren', async ({ page, request }) => {
    const timestamp = Date.now();

    // Setup: Create all prerequisite data
    const saisonResponse = await request.post('http://localhost:8000/api/saison', {
      data: {
        name: `E2E Saison ${timestamp}`,
        from_date: '2024-01-01',
        to_date: '2024-12-31'
      }
    });
    const saison = await saisonResponse.json();
    createdIds.saison.push(saison.id);

    const schwimmbadResponse = await request.post('http://localhost:8000/api/schwimmbad', {
      data: {
        name: `E2E Schwimmbad ${timestamp}`,
        adresse: 'Test Straße 1'
      }
    });
    const schwimmbad = await schwimmbadResponse.json();
    createdIds.schwimmbad.push(schwimmbad.id);

    const vereinResponse = await request.post('http://localhost:8000/api/verein', {
      data: {
        name: `E2E Verein ${timestamp}`,
        ort: 'Hamburg',
        register_id: `E2E-${timestamp}`,
        contact: 'e2e@test.de'
      }
    });
    const verein = await vereinResponse.json();
    createdIds.verein.push(verein.id);

    const kindResponse = await request.post('http://localhost:8000/api/kind', {
      data: {
        vorname: `Wettkampf-${timestamp}`,
        nachname: 'Teilnehmer',
        geburtsdatum: '2013-09-10',
        verein_id: verein.id
      }
    });
    const kind = await kindResponse.json();
    createdIds.kind.push(kind.id);

    // Step 1: Create Wettkampf via UI
    await page.goto('/wettkampf/new');
    await page.waitForLoadState('networkidle');

    await page.fill('input[name="name"]', `E2E Wettkampf ${timestamp}`);
    await page.fill('input[name="datum"]', '2024-10-15');
    await page.fill('input[name="max_teilnehmer"]', '50');
    await page.selectOption('select[name="saison_id"]', saison.id.toString());
    await page.selectOption('select[name="schwimmbad_id"]', schwimmbad.id.toString());

    await page.click('button[type="submit"]');
    await page.waitForURL('/wettkampf');

    // Infer Wettkampf ID via API list for cleanup
    const wkListResponse = await request.get('http://localhost:8000/api/wettkampf');
    const wkList = await wkListResponse.json();
    const createdWk = wkList.find((w: any) => w.name === `E2E Wettkampf ${timestamp}`);
    if (createdWk) createdIds.wettkampf.push(createdWk.id);

    // Step 2: Verify Wettkampf appears in list
    await page.goto('/wettkampf');
    await page.waitForLoadState('networkidle');

    const wettkampfLink = page.locator('a').filter({ hasText: `E2E Wettkampf ${timestamp}` });
    await expect(wettkampfLink).toBeVisible();

    // Step 3: Navigate to Wettkampf details and verify nested data
    await wettkampfLink.click();
    await page.waitForLoadState('networkidle');

    // Verify Saison and Schwimmbad are displayed (eager loading)
    await expect(page.locator(`text=${saison.name}`)).toBeVisible();
    await expect(page.locator(`text=${schwimmbad.name}`)).toBeVisible();

    // Verify no raw IDs are shown (proper eager loading)
    const hasSaisonId = await page.locator(`text=/Saison-ID.*${saison.id}/`).count();
    expect(hasSaisonId).toBe(0);

    // Use the wettkampf ID we already have from the API response
    const wettkampfId = createdWk!.id.toString();

    // Step 4: Create Anmeldung (registration) via UI
    await page.goto('/anmeldung/new');
    await page.waitForLoadState('networkidle');

    // Wait for dropdowns to populate (check for attached state, not visible)
    await page.waitForSelector(`select[name="kind_id"] option[value="${kind.id}"]`, { state: 'attached', timeout: 5000 });
    await page.selectOption('select[name="kind_id"]', kind.id.toString());

    // Wait for wettkampf option to be available
    await page.waitForSelector(`select[name="wettkampf_id"] option[value="${wettkampfId}"]`, { state: 'attached', timeout: 5000 });
    await page.selectOption('select[name="wettkampf_id"]', wettkampfId!);
    // No figures selected → creates vorläufig anmeldung

    await page.click('button[type="submit"]');
    await page.waitForURL('/anmeldung/liste');

    // Infer Anmeldung ID for cleanup
    // We can assume it's created if we are here
    // But since we can't easily query by "name", we might rely on CASCADE delete from Wettkampf/Kind
    // Or fetch all anmeldungen for this wettkampf
    const anmeldungResponse = await request.get('http://localhost:8000/api/anmeldung');
    const anmeldungen = await anmeldungResponse.json();
    // Filter locally or just rely on cascade delete. 
    // Ideally we should track it. 
    // Let's rely on cascade delete for Anmeldung (it belongs to Wettkampf), 
    // but just in case, let's try to find it.
    const myAnmeldung = anmeldungen.find((a: any) => a.wettkampf_id == wettkampfId && a.kind_id == kind.id);
    if (myAnmeldung) createdIds.anmeldung.push(myAnmeldung.id);


    // Step 5: Verify Anmeldung appears with Kind name (not ID)
    await page.goto('/anmeldung/liste');
    await page.waitForLoadState('networkidle');

    const anmeldungRow = page.locator('a').filter({ hasText: `Wettkampf-${timestamp}` });
    await expect(anmeldungRow).toBeVisible();

    // Verify vorläufig status (business rule: no figuren → vorläufig)
    // Check within the specific anmeldung row
    await expect(anmeldungRow.locator('text=/vorläufig/i')).toBeVisible();

    // Verify Kind name is shown (not Kind-ID)
    await expect(anmeldungRow).toContainText(`Wettkampf-${timestamp} Teilnehmer`);

    // Step 6: Verify eager loading on Wettkampf details page
    await page.goto(`/wettkampf/${wettkampfId}`);
    await page.waitForLoadState('networkidle');

    // Should show Kind name in anmeldungen section (check for vorname at least)
    await expect(page.locator(`text=Wettkampf-${timestamp}`)).toBeVisible();
    await expect(page.locator(`text=Teilnehmer`)).toBeVisible();

    // Should NOT show "Kind-ID: X" (proper eager loading)
    const hasKindIdText = await page.locator('text=/Kind-ID:.*\d+/').count();
    expect(hasKindIdText).toBe(0);
  });

  test('anmeldung business rules - vorläufig status', async ({ request }) => {
    const timestamp = Date.now();

    // Setup minimal data
    const vereinResponse = await request.post('http://localhost:8000/api/verein', {
      data: {
        name: `Rule Test Verein ${timestamp}`,
        ort: 'Frankfurt',
        register_id: `RULE-${timestamp}`,
        contact: 'rule@test.de'
      }
    });
    const verein = await vereinResponse.json();
    createdIds.verein.push(verein.id);

    const kindResponse = await request.post('http://localhost:8000/api/kind', {
      data: {
        vorname: `Rule-${timestamp}`,
        nachname: 'Test',
        geburtsdatum: '2014-05-05',
        verein_id: verein.id
      }
    });
    const kind = await kindResponse.json();
    createdIds.kind.push(kind.id);

    const saisonResponse = await request.post('http://localhost:8000/api/saison', {
      data: {
        name: `Rule Saison ${timestamp}`,
        from_date: '2024-01-01',
        to_date: '2024-12-31'
      }
    });
    const saison = await saisonResponse.json();
    createdIds.saison.push(saison.id);

    const schwimmbadResponse = await request.post('http://localhost:8000/api/schwimmbad', {
      data: {
        name: `Rule Schwimmbad ${timestamp}`,
        adresse: 'Rule Str. 1'
      }
    });
    const schwimmbad = await schwimmbadResponse.json();
    createdIds.schwimmbad.push(schwimmbad.id);

    const wettkampfResponse = await request.post('http://localhost:8000/api/wettkampf', {
      data: {
        name: `Rule Wettkampf ${timestamp}`,
        datum: '2024-11-20',
        saison_id: saison.id,
        schwimmbad_id: schwimmbad.id
      }
    });
    const wettkampf = await wettkampfResponse.json();
    createdIds.wettkampf.push(wettkampf.id);

    // Test 1: Anmeldung without figuren should be vorläufig
    const anmeldung1Response = await request.post('http://localhost:8000/api/anmeldung', {
      data: {
        kind_id: kind.id,
        wettkampf_id: wettkampf.id,
        figur_ids: []  // No figures
      }
    });
    expect(anmeldung1Response.ok()).toBeTruthy();
    const anmeldung1 = await anmeldung1Response.json();
    createdIds.anmeldung.push(anmeldung1.id);

    // Verify business rule: no figuren → vorläufig
    expect(anmeldung1.vorlaeufig).toBe(1);
    expect(anmeldung1.status).toBe('vorläufig');

    // Verify Kind data is eagerly loaded
    expect(anmeldung1.kind).toBeDefined();
    expect(anmeldung1.kind.vorname).toBe(`Rule-${timestamp}`);
    expect(anmeldung1.kind.verein).toBeDefined();
    expect(anmeldung1.kind.verein.name).toBe(`Rule Test Verein ${timestamp}`);

    // Test 2: Anmeldung with figuren should be aktiv
    // First create a figur
    const figurResponse = await request.post('http://localhost:8000/api/figur', {
      data: {
        name: `Test Figur ${timestamp}`,
        kategorie: 'Test',
        schwierigkeitsgrad: 5.0
      }
    });
    const figur = await figurResponse.json();
    createdIds.figur.push(figur.id);

    const anmeldung2Response = await request.post('http://localhost:8000/api/anmeldung', {
      data: {
        kind_id: kind.id,
        wettkampf_id: wettkampf.id,
        figur_ids: [figur.id]  // With figure
      }
    });
    expect(anmeldung2Response.ok()).toBeTruthy();
    const anmeldung2 = await anmeldung2Response.json();
    createdIds.anmeldung.push(anmeldung2.id);

    // Verify business rule: figuren present → aktiv
    expect(anmeldung2.vorlaeufig).toBe(0);
    expect(anmeldung2.status).toBe('aktiv');

    // Verify figuren are eagerly loaded
    expect(anmeldung2.figuren).toBeDefined();
    expect(anmeldung2.figuren.length).toBe(1);
    expect(anmeldung2.figuren[0].name).toBe(`Test Figur ${timestamp}`);
  });

  test('getWettkampfWithDetails returns complete nested data', async ({ request }) => {
    const timestamp = Date.now();

    // Create complete nested structure
    const saison = await (await request.post('http://localhost:8000/api/saison', {
      data: { name: `Nested Saison ${timestamp}`, from_date: '2024-01-01', to_date: '2024-12-31' }
    })).json();
    createdIds.saison.push(saison.id);

    const schwimmbad = await (await request.post('http://localhost:8000/api/schwimmbad', {
      data: { name: `Nested Schwimmbad ${timestamp}`, adresse: 'Nested Str. 1' }
    })).json();
    createdIds.schwimmbad.push(schwimmbad.id);

    const wettkampf = await (await request.post('http://localhost:8000/api/wettkampf', {
      data: {
        name: `Nested Wettkampf ${timestamp}`,
        datum: '2024-12-10',
        saison_id: saison.id,
        schwimmbad_id: schwimmbad.id
      }
    })).json();
    createdIds.wettkampf.push(wettkampf.id);

    // Create an Anmeldung to verify it is included
    const verein = await (await request.post('http://localhost:8000/api/verein', {
      data: { name: `Nested Verein ${timestamp}`, ort: 'Test', register_id: `N-${timestamp}`, contact: 'c' }
    })).json();
    createdIds.verein.push(verein.id);

    const kind = await (await request.post('http://localhost:8000/api/kind', {
      data: { vorname: 'Max', nachname: 'Nested', geburtsdatum: '2010-01-01', verein_id: verein.id }
    })).json();
    createdIds.kind.push(kind.id);

    const anmeldung = await (await request.post('http://localhost:8000/api/anmeldung', {
      data: { kind_id: kind.id, wettkampf_id: wettkampf.id, figur_ids: [] }
    })).json();
    createdIds.anmeldung.push(anmeldung.id);

    // Fetch with details endpoint
    const detailsResponse = await request.get(`http://localhost:8000/api/wettkampf/${wettkampf.id}/details`);
    expect(detailsResponse.ok()).toBeTruthy();
    const details = await detailsResponse.json();

    // Verify all nested data is present
    expect(details.id).toBe(wettkampf.id);
    expect(details.saison).toBeDefined();
    expect(details.saison.name).toBe(`Nested Saison ${timestamp}`);
    expect(details.schwimmbad).toBeDefined();
    expect(details.schwimmbad.name).toBe(`Nested Schwimmbad ${timestamp}`);
    expect(details.figuren).toBeDefined();
    expect(Array.isArray(details.figuren)).toBeTruthy();
    expect(details.anmeldungen).toBeDefined();
    expect(Array.isArray(details.anmeldungen)).toBeTruthy();
    
    // Verify Kind is present in Anmeldung
    expect(details.anmeldungen.length).toBeGreaterThan(0);
    expect(details.anmeldungen[0].kind).toBeDefined();
    expect(details.anmeldungen[0].kind.vorname).toBe('Max');
  });
});
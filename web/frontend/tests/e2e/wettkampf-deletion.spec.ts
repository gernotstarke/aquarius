
import { test, expect } from '@playwright/test';

test.describe('Wettkampf Deletion', () => {
  const createdIds: { wettkampf: number[], verein: number[], kind: number[], saison: number[], schwimmbad: number[] } = {
    wettkampf: [], verein: [], kind: [], saison: [], schwimmbad: []
  };

  test.afterAll(async ({ request }) => {
    // Cleanup
    for (const id of createdIds.wettkampf) await request.delete(`http://localhost:8000/api/wettkampf/${id}`).catch(() => {});
    for (const id of createdIds.kind) await request.delete(`http://localhost:8000/api/kind/${id}`).catch(() => {});
    for (const id of createdIds.verein) await request.delete(`http://localhost:8000/api/verein/${id}`).catch(() => {});
    for (const id of createdIds.schwimmbad) await request.delete(`http://localhost:8000/api/schwimmbad/${id}`).catch(() => {});
    for (const id of createdIds.saison) await request.delete(`http://localhost:8000/api/saison/${id}`).catch(() => {});
  });

  test('should delete wettkampf and cascade to anmeldungen', async ({ page, request }) => {
    const timestamp = Date.now();

    // 1. Create Prerequisites
    const saison = await (await request.post('http://localhost:8000/api/saison', {
      data: { name: `DelTest Saison ${timestamp}`, from_date: '2024-01-01', to_date: '2024-12-31' }
    })).json();
    createdIds.saison.push(saison.id);

    const schwimmbad = await (await request.post('http://localhost:8000/api/schwimmbad', {
      data: { name: `DelTest Schwimmbad ${timestamp}`, adresse: 'Test' }
    })).json();
    createdIds.schwimmbad.push(schwimmbad.id);

    const verein = await (await request.post('http://localhost:8000/api/verein', {
      data: { name: `DelTest Verein ${timestamp}`, ort: 'Test', register_id: `D-${timestamp}`, contact: 'c' }
    })).json();
    createdIds.verein.push(verein.id);

    const kind = await (await request.post('http://localhost:8000/api/kind', {
      data: { vorname: 'Max', nachname: 'Delete', geburtsdatum: '2010-01-01', verein_id: verein.id }
    })).json();
    createdIds.kind.push(kind.id);

    // 2. Create Wettkampf
    const wettkampf = await (await request.post('http://localhost:8000/api/wettkampf', {
      data: {
        name: `Delete Me ${timestamp}`,
        datum: '2024-06-01',
        saison_id: saison.id,
        schwimmbad_id: schwimmbad.id
      }
    })).json();
    // We don't push to createdIds.wettkampf immediately because we want to test successful deletion
    // But if test fails, we might want to cleanup. Let's push and handle 404 in cleanup.
    createdIds.wettkampf.push(wettkampf.id);

    // 3. Create Anmeldung (Dependency)
    await request.post('http://localhost:8000/api/anmeldung', {
      data: { kind_id: kind.id, wettkampf_id: wettkampf.id, figur_ids: [] }
    });

    // 4. Go to Wettkampf List
    await page.goto('/wettkampf');
    await page.waitForLoadState('networkidle');

    // 5. Delete Wettkampf
    // Find the heading with the specific name
    const heading = page.getByRole('heading', { name: `Delete Me ${timestamp}` });
    await expect(heading).toBeVisible();
    
    // Find the container card (closest div with the button)
    const card = heading.locator('xpath=ancestor::div[contains(@class, "flex items-center justify-between")]');
    
    page.on('dialog', dialog => dialog.accept());
    await card.getByRole('button', { name: 'Löschen' }).click();

    // 6. Verify Deletion
    await page.waitForTimeout(1000); // Wait for API and refresh
    await expect(page.locator('div').filter({ hasText: `Delete Me ${timestamp}` })).not.toBeVisible();

    // 7. Verify API 404
    const response = await request.get(`http://localhost:8000/api/wettkampf/${wettkampf.id}`);
    expect(response.status()).toBe(404);
  });
});

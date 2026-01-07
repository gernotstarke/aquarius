import { test, expect } from '@playwright/test';

test.describe('Kind and Anmeldung Workflow', () => {
  test('create kind, create anmeldung, cleanup', async ({ page }) => {
    // Generate unique name to avoid conflicts
    const timestamp = Date.now();
    const kindVorname = `Test-${timestamp}`;
    const kindNachname = 'E2E-Kind';

    // Step 1: Create a Kind
    await page.goto('/kind/new');

    // Fill kind form
    await page.getByLabel(/Vorname/i).fill(kindVorname);
    await page.getByLabel(/Nachname/i).fill(kindNachname);
    await page.getByLabel(/Geburtsdatum/i).fill('2015-05-15');

    // Select gender (if dropdown exists)
    const genderSelect = page.locator('select').filter({ hasText: /Geschlecht/i }).or(
      page.getByLabel(/Geschlecht/i)
    );
    if (await genderSelect.count() > 0) {
      await genderSelect.selectOption('M');
    }

    // Save kind
    await page.getByRole('button', { name: /Speichern|Erstellen/i }).click();

    // Verify redirect to kind list and success (redirects to /kind, not /kinder)
    await expect(page).toHaveURL(/\/kind($|\/)/);
    await expect(page.getByText(kindVorname)).toBeVisible({ timeout: 10000 });

    // Step 2: Navigate to create anmeldung
    await page.goto('/anmeldung/new');

    // Wait for form to load and data to be fetched
    await expect(page.getByRole('heading', { name: /Neue Anmeldung/i })).toBeVisible();
    await page.waitForLoadState('networkidle');

    // Wait for Kind options to load (check that they exist, not visible since options are hidden)
    await page.locator(`option:has-text("${kindVorname}")`).waitFor({ state: 'attached', timeout: 10000 });

    // Select the kind by getting the full option text
    const kindOption = await page.locator(`option:has-text("${kindVorname}")`).textContent();
    await page.locator('select').first().selectOption({ label: kindOption?.trim() || kindVorname });

    // Select a wettkampf (assumes at least one exists from seed data)
    // Use the second select element (first is Kind, second is Wettkampf)
    const wettkampfSelect = page.locator('select').nth(1);
    // Select first available wettkampf option (index 1, skipping "Bitte wählen" at index 0)
    await wettkampfSelect.selectOption({ index: 1 });

    // Submit anmeldung (even without figures, creates preliminary anmeldung)
    await page.getByRole('button', { name: /Anmelden/i }).click();

    // Verify redirect to anmeldung list
    await expect(page).toHaveURL(/\/anmeldung\/liste/);
    await expect(page.getByText(kindVorname)).toBeVisible({ timeout: 10000 });

    // Note: Cleanup (deletion) is skipped in this test
    // Manual cleanup: navigate to /kind and delete test entries if needed
  });
});

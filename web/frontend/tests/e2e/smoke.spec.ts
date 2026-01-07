import { test, expect } from '@playwright/test';

test('home loads and shows main navigation', async ({ page }) => {
  await page.goto('/');

  await expect(page.getByRole('heading', { name: 'Aquarius' })).toBeVisible();
  await expect(page.getByRole('button', { name: /Grunddaten/ })).toBeVisible();
  await expect(page.getByRole('button', { name: /Anmeldung/ })).toBeVisible();
  await expect(page.getByRole('button', { name: /Kinder/ })).toBeVisible();
});

test('grunddaten page shows kinder tile', async ({ page }) => {
  await page.goto('/grunddaten');

  await expect(page.getByRole('heading', { name: 'Grunddaten' })).toBeVisible();
  await expect(page.getByText('Teilnehmende Kinder verwalten')).toBeVisible();
});

test('kinder list page loads and shows table', async ({ page }) => {
  await page.goto('/kinder');

  await expect(page.getByRole('heading', { name: 'Kinder' })).toBeVisible();
  await expect(page.getByText('Neues Kind')).toBeVisible();
});

test('wettkämpfe list page loads', async ({ page }) => {
  await page.goto('/wettkaempfe');

  await expect(page.getByRole('heading', { name: /Wettkämpfe/i })).toBeVisible();
  await expect(page.getByText('Neuer Wettkampf')).toBeVisible();
});

test('anmeldungen list page loads', async ({ page }) => {
  await page.goto('/anmeldung/liste');

  await expect(page.getByRole('heading', { name: 'Anmeldungen' })).toBeVisible();
  await expect(page.getByText('Neue Anmeldung')).toBeVisible();
});

test('figuren list page loads', async ({ page }) => {
  await page.goto('/grunddaten/figuren');

  await expect(page.getByRole('heading', { name: 'Figuren' })).toBeVisible();
  await expect(page.getByText('Neue Figur')).toBeVisible();
});

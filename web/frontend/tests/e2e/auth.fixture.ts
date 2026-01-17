import { test as base, Page } from '@playwright/test';
import * as fs from 'fs';
import * as path from 'path';

/**
 * Extended test with authentication.
 * This fixture automatically injects the JWT token into localStorage
 * before each test runs, so all tests are authenticated by default.
 */

let cachedToken: string | null = null;

function loadToken(): string {
  if (cachedToken) {
    return cachedToken;
  }

  // Load token from frontend root .auth directory
  const authFile = path.resolve(process.cwd(), '.auth', 'token.json');

  if (!fs.existsSync(authFile)) {
    throw new Error(
      `Auth file not found at ${authFile}. ` +
      'Did globalSetup run successfully? Check logs above.'
    );
  }

  const authData = JSON.parse(fs.readFileSync(authFile, 'utf-8'));
  cachedToken = authData.token;
  return cachedToken;
}

async function injectAuthToken(page: Page): Promise<void> {
  const token = loadToken();

  // Navigate to a page first to establish context
  await page.goto('/');

  // Inject token into localStorage
  await page.evaluate((token) => {
    localStorage.setItem('token', token);
  }, token);
}

export const test = base.extend({
  page: async ({ page }, use) => {
    // Inject auth token before each test
    await injectAuthToken(page);

    // Yield the authenticated page to the test
    await use(page);

    // Cleanup after test
    await page.evaluate(() => {
      localStorage.removeItem('token');
    });
  },
});

export { expect } from '@playwright/test';

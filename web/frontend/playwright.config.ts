import { defineConfig } from '@playwright/test';
import * as path from 'path';

const baseURL = process.env.PLAYWRIGHT_BASE_URL || 'http://localhost:5173';

export default defineConfig({
  testDir: './tests/e2e',
  timeout: 60000,
  expect: {
    timeout: 10000,
  },
  globalSetup: path.join(__dirname, './playwright-globalSetup.ts'),
  globalTeardown: path.join(__dirname, './playwright-globalTeardown.ts'),
  use: {
    baseURL,
    headless: true,
    trace: 'retain-on-failure',
    screenshot: 'only-on-failure',
    launchOptions: {
      args: [
        '--disable-gpu',
        '--disable-dev-shm-usage',
        '--disable-setuid-sandbox',
        '--no-sandbox',
      ],
    },
  },
});

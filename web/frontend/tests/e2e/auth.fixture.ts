import { test as base, Page, APIRequestContext } from '@playwright/test';
import * as fs from 'fs';
import * as path from 'path';

/**
 * Extended test with authentication.
 * This fixture automatically:
 * 1. Injects JWT token into localStorage (for page-based API calls)
 * 2. Provides an authenticated request fixture with Authorization headers (for direct API calls)
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

  // Inject token into localStorage BEFORE any page navigation
  // This ensures AuthContext finds the token when it initializes
  await page.addInitScript((tokenData: { app_token: string; token: string }) => {
    localStorage.setItem('app_token', tokenData.app_token);
    localStorage.setItem('token', tokenData.token);
  }, { app_token: token, token });

  // Now navigate to a page - localStorage will already be set
  await page.goto('/');
}

export const test = base.extend({
  page: async ({ page }, use) => {
    // Inject auth token into localStorage before each test
    await injectAuthToken(page);

    // Yield the authenticated page to the test
    await use(page);

    // Cleanup after test
    await page.evaluate(() => {
      localStorage.removeItem('app_token');
      localStorage.removeItem('token');
    });
  },

  request: async ({ request }, use) => {
    // Wrap the request context to add Authorization header to all requests
    const token = loadToken();
    const authHeader = `Bearer ${token}`;

    // Create a wrapper that intercepts all requests
    const authenticatedRequest = {
      async get(url: string, options?: any) {
        return request.get(url, {
          ...options,
          headers: {
            ...options?.headers,
            'Authorization': authHeader,
          },
        });
      },

      async post(url: string, options?: any) {
        return request.post(url, {
          ...options,
          headers: {
            ...options?.headers,
            'Authorization': authHeader,
          },
        });
      },

      async put(url: string, options?: any) {
        return request.put(url, {
          ...options,
          headers: {
            ...options?.headers,
            'Authorization': authHeader,
          },
        });
      },

      async patch(url: string, options?: any) {
        return request.patch(url, {
          ...options,
          headers: {
            ...options?.headers,
            'Authorization': authHeader,
          },
        });
      },

      async delete(url: string, options?: any) {
        return request.delete(url, {
          ...options,
          headers: {
            ...options?.headers,
            'Authorization': authHeader,
          },
        });
      },

      async head(url: string, options?: any) {
        return request.head(url, {
          ...options,
          headers: {
            ...options?.headers,
            'Authorization': authHeader,
          },
        });
      },

      async fetch(urlOrRequest: string | any, options?: any) {
        const url = typeof urlOrRequest === 'string' ? urlOrRequest : urlOrRequest.url;
        return request.fetch(url, {
          ...options,
          headers: {
            ...options?.headers,
            'Authorization': authHeader,
          },
        });
      },
    };

    // Yield the authenticated request wrapper to the test
    await use(authenticatedRequest as APIRequestContext);
  },
});

export { expect } from '@playwright/test';

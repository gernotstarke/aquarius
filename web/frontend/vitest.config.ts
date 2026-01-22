import { defineConfig } from 'vitest/config';
import react from '@vitejs/plugin-react';

export default defineConfig({
  plugins: [react()],
  test: {
    environment: 'jsdom',
    globals: true,
    setupFiles: './src/setupTests.ts',
    exclude: [
      '**/node_modules/**',
      '**/dist/**',
      '**/tests/e2e/**',  // Exclude Playwright E2E tests
    ],
  },
});

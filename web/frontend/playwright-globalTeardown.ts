import { execSync } from 'child_process';
import * as fs from 'fs';
import * as path from 'path';

/**
 * Global teardown: Clean up test user and auth state after tests complete.
 * This runs once after all tests finish.
 */

const TEST_USER = 'e2e_test_user';
// Store auth state in frontend root .auth directory (not in __dirname which is build output)
const AUTH_DIR = path.resolve(process.cwd(), '.auth');
const AUTH_FILE = path.join(AUTH_DIR, 'token.json');

function runBackendCommand(command: string): string {
  try {
    // Run from project root so docker compose can find docker-compose.yml
    const projectRoot = path.resolve(process.cwd(), '..');
    const result = execSync(command, {
      encoding: 'utf-8',
      stdio: ['pipe', 'pipe', 'pipe'],
      cwd: projectRoot
    });
    return result.trim();
  } catch (error: any) {
    // Don't fail if delete fails - the test user might not exist
    return '';
  }
}

async function globalTeardown() {
  console.log('\n🧹 Playwright Global Teardown: Cleaning up...');

  try {
    // Delete test user (using docker compose)
    console.log('🗑️  Deleting test user...');
    const deleteCmd = `docker compose run --rm backend python tests/test_user_cli.py delete ${TEST_USER}`;

    runBackendCommand(deleteCmd);
    console.log('✓ Test user deleted');

    // Clean up auth file
    if (fs.existsSync(AUTH_FILE)) {
      fs.unlinkSync(AUTH_FILE);
      console.log('✓ Auth state cleaned up');
    }

    console.log('✅ Global teardown complete!\n');
  } catch (error: any) {
    console.error('⚠️  Teardown warning:', error.message);
    // Don't fail the entire test suite if cleanup fails
  }
}

export default globalTeardown;

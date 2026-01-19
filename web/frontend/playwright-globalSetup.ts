import { execSync } from 'child_process';
import * as fs from 'fs';
import * as path from 'path';

/**
 * Global setup: Create test user and obtain JWT token before tests run.
 * This runs once before all tests begin.
 */

const TEST_USER = 'e2e_test_user';
const TEST_PASSWORD = 'test_password_123';
// Store auth state in frontend root .auth directory (not in __dirname which is build output)
const AUTH_DIR = path.resolve(process.cwd(), '.auth');
const AUTH_FILE = path.join(AUTH_DIR, 'token.json');

function ensureAuthDir() {
  if (!fs.existsSync(AUTH_DIR)) {
    fs.mkdirSync(AUTH_DIR, { recursive: true });
  }
}

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
    const stderr = error.stderr?.toString() || error.stdout?.toString() || error.message;
    throw new Error(`Command failed: ${stderr}`);
  }
}

function extractValue(output: string, prefix: string): string {
  if (output.startsWith(`${prefix}:`)) {
    return output.substring(`${prefix}:`.length);
  }
  throw new Error(`Unexpected output: ${output}`);
}

async function globalSetup() {
  console.log('🔧 Playwright Global Setup: Creating test user...');

  try {
    ensureAuthDir();

    // Create test user via backend CLI (using docker compose)
    console.log('📝 Creating test user...');
    const createCmd = `docker compose run --rm backend python tests/test_user_cli.py create ${TEST_USER} ${TEST_PASSWORD}`;

    const createOutput = runBackendCommand(createCmd);
    if (!createOutput.startsWith('OK:')) {
      throw new Error(`Failed to create user: ${createOutput}`);
    }
    console.log('✓ Test user created');

    // Get JWT token
    console.log('🔐 Obtaining JWT token...');
    const tokenCmd = `docker compose run --rm backend python tests/test_user_cli.py token ${TEST_USER} ${TEST_PASSWORD}`;

    const tokenOutput = runBackendCommand(tokenCmd);
    const token = extractValue(tokenOutput, 'OK');

    if (!token) {
      throw new Error('Failed to obtain token');
    }
    console.log('✓ JWT token obtained');

    // Save token to file for use in tests
    const authData = {
      token,
      username: TEST_USER,
      timestamp: new Date().toISOString(),
    };

    fs.writeFileSync(AUTH_FILE, JSON.stringify(authData, null, 2));
    console.log(`✓ Auth state saved to ${AUTH_FILE}`);

    console.log('✅ Global setup complete!\n');
  } catch (error: any) {
    console.error('❌ Global setup failed:', error.message);
    process.exit(1);
  }
}

export default globalSetup;

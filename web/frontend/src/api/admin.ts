/**
 * Admin API Service - Administration and authentication
 *
 * Encapsulates all API calls related to admin domain (auth, users, database).
 */

import adminApiClient from './adminClient';

// ===== Auth API =====

export interface LoginCredentials {
  username: string;
  password: string;
}

export interface LoginResponse {
  access_token: string;
  token_type: string;
}

export interface TOTPSetupResponse {
  secret: string;
  qr_code: string;
}

export interface TOTPEnableRequest {
  token: string;
  backup_codes?: string[];
}

export interface TOTPVerifyRequest {
  token: string;
}

export interface TOTPVerifyBackupRequest {
  backup_code: string;
}

export interface User {
  id: number;
  username: string;
  is_active: boolean;
  is_superuser: boolean;
  totp_enabled: boolean;
}

export interface UserCreate {
  username: string;
  password: string;
  is_superuser?: boolean;
}

/**
 * Get current authenticated user
 */
export const getCurrentUser = async (): Promise<User> => {
  const response = await adminApiClient.get<User>('/auth/me');
  return response.data;
};

/**
 * Login with username and password
 */
export const login = async (credentials: LoginCredentials): Promise<LoginResponse> => {
  const params = new URLSearchParams();
  params.append('username', credentials.username);
  params.append('password', credentials.password);

  const response = await adminApiClient.post<LoginResponse>('/auth/token', params, {
    headers: {
      'Content-Type': 'application/x-www-form-urlencoded',
    },
  });
  return response.data;
};

/**
 * Setup TOTP (2FA) for current user
 */
export const setupTOTP = async (): Promise<TOTPSetupResponse> => {
  const response = await adminApiClient.post<TOTPSetupResponse>('/auth/totp/setup');
  return response.data;
};

/**
 * Enable TOTP with verification token
 */
export const enableTOTP = async (request: TOTPEnableRequest): Promise<void> => {
  await adminApiClient.post('/auth/totp/enable', request);
};

/**
 * Verify TOTP token
 */
export const verifyTOTP = async (request: TOTPVerifyRequest): Promise<LoginResponse> => {
  const response = await adminApiClient.post<LoginResponse>('/auth/totp/verify', request);
  return response.data;
};

/**
 * Verify TOTP backup code
 */
export const verifyTOTPBackup = async (request: TOTPVerifyBackupRequest): Promise<LoginResponse> => {
  const response = await adminApiClient.post<LoginResponse>('/auth/totp/verify-backup', request);
  return response.data;
};

// ===== User Management API =====

/**
 * Fetch list of users
 */
export const listUsers = async (): Promise<User[]> => {
  const response = await adminApiClient.get<User[]>('/users/');
  return response.data;
};

/**
 * Create a new user
 */
export const createUser = async (user: UserCreate): Promise<User> => {
  const response = await adminApiClient.post<User>('/users/', user);
  return response.data;
};

/**
 * Update an existing user
 */
export const updateUser = async (id: number, user: Partial<UserCreate>): Promise<User> => {
  const response = await adminApiClient.put<User>(`/users/${id}`, user);
  return response.data;
};

/**
 * Delete a user by ID
 */
export const deleteUser = async (id: number): Promise<void> => {
  await adminApiClient.delete(`/users/${id}`);
};

// ===== Database Admin API =====

export interface DatabaseStats {
  total_tables: number;
  total_records: number;
  database_size_mb?: number;
  tables: Array<{
    name: string;
    count: number;
  }>;
}

export interface SystemHealth {
  status: string;
  database: string;
  version: string;
}

/**
 * Get database statistics
 */
export const getDatabaseStats = async (): Promise<DatabaseStats> => {
  const response = await adminApiClient.get<DatabaseStats>('/admin/database/stats');
  return response.data;
};

/**
 * Get system health status
 */
export const getSystemHealth = async (): Promise<SystemHealth> => {
  const response = await adminApiClient.get<SystemHealth>('/health/');
  return response.data;
};

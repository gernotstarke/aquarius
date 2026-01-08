/**
 * Central API exports - Re-exports all domain API services
 *
 * This file provides convenient access to all API services.
 * Components can import specific services they need.
 *
 * Example:
 *   import { listKinder, createKind } from '../api/kind';
 * Or:
 *   import * as kindApi from '../api/kind';
 */

// Export the base client for custom API calls
export { default as apiClient } from './client';

// Domain API services
export * as kindApi from './kind';
export * as grunddatenApi from './grunddaten';
export * as saisonApi from './saison';
export * as schwimmbadApi from './schwimmbad';
export * as figurApi from './figur';
export * as wettkampfApi from './wettkampf';
export * as anmeldungApi from './anmeldung';
export * as adminApi from './admin';

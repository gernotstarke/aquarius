/**
 * Grunddaten API Service - Verein, Verband, Versicherung
 *
 * Encapsulates all API calls related to base data (Grunddaten domain).
 */

import apiClient from './client';
import { Verein, VereinCreate, Verband, Versicherung } from '../types/grunddaten';

// ===== Verein API =====

export interface VereinListParams {
  skip?: number;
  limit?: number;
}

/**
 * Fetch list of Vereine
 */
export const listVereine = async (params: VereinListParams = {}): Promise<Verein[]> => {
  const response = await apiClient.get<Verein[]>('/verein', { params });
  return response.data;
};

/**
 * Fetch a single Verein by ID
 */
export const getVerein = async (id: number): Promise<Verein> => {
  const response = await apiClient.get<Verein>(`/verein/${id}`);
  return response.data;
};

/**
 * Create a new Verein
 */
export const createVerein = async (verein: VereinCreate): Promise<Verein> => {
  const response = await apiClient.post<Verein>('/verein', verein);
  return response.data;
};

/**
 * Update an existing Verein
 */
export const updateVerein = async (id: number, verein: Partial<VereinCreate>): Promise<Verein> => {
  const response = await apiClient.put<Verein>(`/verein/${id}`, verein);
  return response.data;
};

/**
 * Delete a Verein by ID
 */
export const deleteVerein = async (id: number): Promise<void> => {
  await apiClient.delete(`/verein/${id}`);
};

// ===== Verband API =====

export interface VerbandListParams {
  skip?: number;
  limit?: number;
  sort_by?: string;
  sort_order?: 'asc' | 'desc';
}

/**
 * Fetch list of Verbände
 */
export const listVerbaende = async (params: VerbandListParams = {}): Promise<Verband[]> => {
  const response = await apiClient.get<Verband[]>('/verband', { params });
  return response.data;
};

// ===== Versicherung API =====

export interface VersicherungListParams {
  skip?: number;
  limit?: number;
}

/**
 * Fetch list of Versicherungen
 */
export const listVersicherungen = async (params: VersicherungListParams = {}): Promise<Versicherung[]> => {
  const response = await apiClient.get<Versicherung[]>('/versicherung', { params });
  return response.data;
};

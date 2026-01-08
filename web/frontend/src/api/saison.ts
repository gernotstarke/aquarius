/**
 * Saison API Service - Season management
 *
 * Encapsulates all API calls related to Saison domain.
 */

import apiClient from './client';
import { Saison, SaisonCreate } from '../types/saison';

export interface SaisonListParams {
  skip?: number;
  limit?: number;
}

/**
 * Fetch list of Saisons
 */
export const listSaisons = async (params: SaisonListParams = {}): Promise<Saison[]> => {
  const response = await apiClient.get<Saison[]>('/saison', { params });
  return response.data;
};

/**
 * Fetch a single Saison by ID
 */
export const getSaison = async (id: number): Promise<Saison> => {
  const response = await apiClient.get<Saison>(`/saison/${id}`);
  return response.data;
};

/**
 * Create a new Saison
 */
export const createSaison = async (saison: SaisonCreate): Promise<Saison> => {
  const response = await apiClient.post<Saison>('/saison', saison);
  return response.data;
};

/**
 * Update an existing Saison
 */
export const updateSaison = async (id: number, saison: Partial<SaisonCreate>): Promise<Saison> => {
  const response = await apiClient.put<Saison>(`/saison/${id}`, saison);
  return response.data;
};

/**
 * Delete a Saison by ID
 */
export const deleteSaison = async (id: number): Promise<void> => {
  await apiClient.delete(`/saison/${id}`);
};

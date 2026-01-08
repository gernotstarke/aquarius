/**
 * Anmeldung API Service - Registration management
 *
 * Encapsulates all API calls related to Anmeldung domain.
 */

import apiClient from './client';
import { Anmeldung, AnmeldungCreate } from '../types/anmeldung';

export interface AnmeldungListParams {
  skip?: number;
  limit?: number;
}

/**
 * Fetch list of Anmeldungen
 */
export const listAnmeldungen = async (params: AnmeldungListParams = {}): Promise<Anmeldung[]> => {
  const response = await apiClient.get<Anmeldung[]>('/anmeldung', { params });
  return response.data;
};

/**
 * Fetch a single Anmeldung by ID
 */
export const getAnmeldung = async (id: number): Promise<Anmeldung> => {
  const response = await apiClient.get<Anmeldung>(`/anmeldung/${id}`);
  return response.data;
};

/**
 * Create a new Anmeldung
 */
export const createAnmeldung = async (anmeldung: AnmeldungCreate): Promise<Anmeldung> => {
  const response = await apiClient.post<Anmeldung>('/anmeldung', anmeldung);
  return response.data;
};

/**
 * Update an existing Anmeldung
 */
export const updateAnmeldung = async (id: number, anmeldung: Partial<AnmeldungCreate>): Promise<Anmeldung> => {
  const response = await apiClient.put<Anmeldung>(`/anmeldung/${id}`, anmeldung);
  return response.data;
};

/**
 * Delete an Anmeldung by ID
 */
export const deleteAnmeldung = async (id: number): Promise<void> => {
  await apiClient.delete(`/anmeldung/${id}`);
};

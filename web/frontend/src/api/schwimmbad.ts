/**
 * Schwimmbad API Service - Swimming pool / venue management
 *
 * Encapsulates all API calls related to Schwimmbad domain.
 */

import apiClient from './client';
import { Schwimmbad, SchwimmbadCreate } from '../types/schwimmbad';

export interface SchwimmbadListParams {
  skip?: number;
  limit?: number;
}

/**
 * Fetch list of Schwimmbäder
 */
export const listSchwimmbaeder = async (params: SchwimmbadListParams = {}): Promise<Schwimmbad[]> => {
  const response = await apiClient.get<Schwimmbad[]>('/schwimmbad', { params });
  return response.data;
};

/**
 * Fetch a single Schwimmbad by ID
 */
export const getSchwimmbad = async (id: number): Promise<Schwimmbad> => {
  const response = await apiClient.get<Schwimmbad>(`/schwimmbad/${id}`);
  return response.data;
};

/**
 * Create a new Schwimmbad
 */
export const createSchwimmbad = async (schwimmbad: SchwimmbadCreate): Promise<Schwimmbad> => {
  const response = await apiClient.post<Schwimmbad>('/schwimmbad', schwimmbad);
  return response.data;
};

/**
 * Update an existing Schwimmbad
 */
export const updateSchwimmbad = async (id: number, schwimmbad: Partial<SchwimmbadCreate>): Promise<Schwimmbad> => {
  const response = await apiClient.put<Schwimmbad>(`/schwimmbad/${id}`, schwimmbad);
  return response.data;
};

/**
 * Delete a Schwimmbad by ID
 */
export const deleteSchwimmbad = async (id: number): Promise<void> => {
  await apiClient.delete(`/schwimmbad/${id}`);
};

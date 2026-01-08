/**
 * Wettkampf API Service - Competition management
 *
 * Encapsulates all API calls related to Wettkampf domain.
 */

import apiClient from './client';
import { Wettkampf, WettkampfCreate, WettkampfWithDetails } from '../types/wettkampf';

export interface WettkampfListParams {
  skip?: number;
  limit?: number;
}

/**
 * Fetch list of Wettkämpfe
 */
export const listWettkaempfe = async (params: WettkampfListParams = {}): Promise<Wettkampf[]> => {
  const response = await apiClient.get<Wettkampf[]>('/wettkampf', { params });
  return response.data;
};

/**
 * Fetch a single Wettkampf by ID
 */
export const getWettkampf = async (id: number): Promise<Wettkampf> => {
  const response = await apiClient.get<Wettkampf>(`/wettkampf/${id}`);
  return response.data;
};

/**
 * Fetch a Wettkampf with full details (figuren, anmeldungen, etc.)
 */
export const getWettkampfWithDetails = async (id: number): Promise<WettkampfWithDetails> => {
  const response = await apiClient.get<WettkampfWithDetails>(`/wettkampf/${id}/details`);
  return response.data;
};

/**
 * Create a new Wettkampf
 */
export const createWettkampf = async (wettkampf: WettkampfCreate): Promise<Wettkampf> => {
  const response = await apiClient.post<Wettkampf>('/wettkampf', wettkampf);
  return response.data;
};

/**
 * Update an existing Wettkampf
 */
export const updateWettkampf = async (id: number, wettkampf: Partial<WettkampfCreate>): Promise<Wettkampf> => {
  const response = await apiClient.put<Wettkampf>(`/wettkampf/${id}`, wettkampf);
  return response.data;
};

/**
 * Delete a Wettkampf by ID
 */
export const deleteWettkampf = async (id: number): Promise<void> => {
  await apiClient.delete(`/wettkampf/${id}`);
};

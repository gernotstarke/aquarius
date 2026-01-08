/**
 * Kind API Service - Child/participant management
 *
 * Encapsulates all API calls related to Kind domain.
 */

import apiClient from './client';
import { Kind, KindCreate } from '../types/kind';

export interface KindListParams {
  skip?: number;
  limit?: number;
  search?: string;
  sort_by?: string;
  sort_order?: 'asc' | 'desc';
}

export interface KindListResponse {
  items: Kind[];
  total: number;
}

/**
 * Fetch list of Kinder with pagination and filtering
 */
export const listKinder = async (params: KindListParams = {}): Promise<KindListResponse> => {
  const response = await apiClient.get<Kind[]>('/kind', { params });
  return {
    items: response.data,
    total: parseInt(response.headers['x-total-count'] || '0', 10),
  };
};

/**
 * Fetch a single Kind by ID
 */
export const getKind = async (id: number): Promise<Kind> => {
  const response = await apiClient.get<Kind>(`/kind/${id}`);
  return response.data;
};

/**
 * Create a new Kind
 */
export const createKind = async (kind: KindCreate): Promise<Kind> => {
  const response = await apiClient.post<Kind>('/kind', kind);
  return response.data;
};

/**
 * Update an existing Kind
 */
export const updateKind = async (id: number, kind: Partial<KindCreate>): Promise<Kind> => {
  const response = await apiClient.put<Kind>(`/kind/${id}`, kind);
  return response.data;
};

/**
 * Delete a Kind by ID
 */
export const deleteKind = async (id: number): Promise<void> => {
  await apiClient.delete(`/kind/${id}`);
};

/**
 * Check if a Kind has valid insurance
 */
export const isKindInsured = (kind: Kind): boolean => {
  const hasContractInsurance = Boolean(kind.versicherung_id && kind.vertrag);
  return Boolean(kind.verein_id || kind.verband_id || hasContractInsurance);
};

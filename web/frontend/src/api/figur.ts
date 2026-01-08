/**
 * Figur API Service - Figure/routine catalog
 *
 * Encapsulates all API calls related to Figur domain.
 */

import apiClient from './client';
import { Figur, FigurCreate } from '../types/figur';

export interface FigurListParams {
  skip?: number;
  limit?: number;
}

/**
 * Fetch list of Figuren
 */
export const listFiguren = async (params: FigurListParams = {}): Promise<Figur[]> => {
  const response = await apiClient.get<Figur[]>('/figur', { params });
  return response.data;
};

/**
 * Fetch a single Figur by ID
 */
export const getFigur = async (id: number): Promise<Figur> => {
  const response = await apiClient.get<Figur>(`/figur/${id}`);
  return response.data;
};

/**
 * Create a new Figur
 */
export const createFigur = async (figur: FigurCreate): Promise<Figur> => {
  const response = await apiClient.post<Figur>('/figur', figur);
  return response.data;
};

/**
 * Update an existing Figur
 */
export const updateFigur = async (id: number, figur: Partial<FigurCreate>): Promise<Figur> => {
  const response = await apiClient.put<Figur>(`/figur/${id}`, figur);
  return response.data;
};

/**
 * Delete a Figur by ID
 */
export const deleteFigur = async (id: number): Promise<void> => {
  await apiClient.delete(`/figur/${id}`);
};

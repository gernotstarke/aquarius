/**
 * Unit tests for Kind API Service
 */

import { describe, it, expect, vi, beforeEach } from 'vitest';
import { listKinder, getKind, createKind, updateKind, deleteKind, isKindInsured } from '../../api/kind';
import apiClient from '../../api/client';
import { Kind, KindCreate } from '../../types/kind';

// Mock the apiClient
vi.mock('../../api/client');

describe('Kind API Service', () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  describe('listKinder', () => {
    it('should fetch list of kinder with pagination', async () => {
      const mockKinder: Kind[] = [
        {
          id: 1,
          vorname: 'Max',
          nachname: 'Mustermann',
          geburtsdatum: '2010-01-01',
        },
        {
          id: 2,
          vorname: 'Anna',
          nachname: 'Schmidt',
          geburtsdatum: '2011-02-15',
        },
      ];

      const mockResponse = {
        data: mockKinder,
        headers: { 'x-total-count': '2' },
      };

      vi.mocked(apiClient.get).mockResolvedValue(mockResponse);

      const result = await listKinder({ skip: 0, limit: 20 });

      expect(apiClient.get).toHaveBeenCalledWith('/kind', {
        params: { skip: 0, limit: 20 },
      });
      expect(result.items).toEqual(mockKinder);
      expect(result.total).toBe(2);
    });

    it('should handle search and sorting parameters', async () => {
      const mockResponse = {
        data: [],
        headers: { 'x-total-count': '0' },
      };

      vi.mocked(apiClient.get).mockResolvedValue(mockResponse);

      await listKinder({
        skip: 10,
        limit: 20,
        search: 'Max',
        sort_by: 'nachname',
        sort_order: 'desc',
      });

      expect(apiClient.get).toHaveBeenCalledWith('/kind', {
        params: {
          skip: 10,
          limit: 20,
          search: 'Max',
          sort_by: 'nachname',
          sort_order: 'desc',
        },
      });
    });
  });

  describe('getKind', () => {
    it('should fetch a single kind by ID', async () => {
      const mockKind: Kind = {
        id: 1,
        vorname: 'Max',
        nachname: 'Mustermann',
        geburtsdatum: '2010-01-01',
        verein_id: 5,
      };

      vi.mocked(apiClient.get).mockResolvedValue({ data: mockKind });

      const result = await getKind(1);

      expect(apiClient.get).toHaveBeenCalledWith('/kind/1');
      expect(result).toEqual(mockKind);
    });
  });

  describe('createKind', () => {
    it('should create a new kind', async () => {
      const newKind: KindCreate = {
        vorname: 'Max',
        nachname: 'Mustermann',
        geburtsdatum: '2010-01-01',
        verein_id: 5,
      };

      const createdKind: Kind = {
        id: 1,
        ...newKind,
      };

      vi.mocked(apiClient.post).mockResolvedValue({ data: createdKind });

      const result = await createKind(newKind);

      expect(apiClient.post).toHaveBeenCalledWith('/kind', newKind);
      expect(result).toEqual(createdKind);
    });
  });

  describe('updateKind', () => {
    it('should update an existing kind', async () => {
      const updates = {
        nachname: 'Schmidt',
      };

      const updatedKind: Kind = {
        id: 1,
        vorname: 'Max',
        nachname: 'Schmidt',
        geburtsdatum: '2010-01-01',
      };

      vi.mocked(apiClient.put).mockResolvedValue({ data: updatedKind });

      const result = await updateKind(1, updates);

      expect(apiClient.put).toHaveBeenCalledWith('/kind/1', updates);
      expect(result).toEqual(updatedKind);
    });
  });

  describe('deleteKind', () => {
    it('should delete a kind by ID', async () => {
      vi.mocked(apiClient.delete).mockResolvedValue({} as any);

      await deleteKind(1);

      expect(apiClient.delete).toHaveBeenCalledWith('/kind/1');
    });
  });

  describe('isKindInsured', () => {
    it('should return true if kind has verein', () => {
      const kind: Kind = {
        id: 1,
        vorname: 'Max',
        nachname: 'Mustermann',
        geburtsdatum: '2010-01-01',
        verein_id: 5,
      };

      expect(isKindInsured(kind)).toBe(true);
    });

    it('should return true if kind has verband', () => {
      const kind: Kind = {
        id: 1,
        vorname: 'Max',
        nachname: 'Mustermann',
        geburtsdatum: '2010-01-01',
        verband_id: 3,
      };

      expect(isKindInsured(kind)).toBe(true);
    });

    it('should return true if kind has contract insurance', () => {
      const kind: Kind = {
        id: 1,
        vorname: 'Max',
        nachname: 'Mustermann',
        geburtsdatum: '2010-01-01',
        versicherung_id: 2,
        vertrag: 'V123',
      };

      expect(isKindInsured(kind)).toBe(true);
    });

    it('should return false if kind has no insurance', () => {
      const kind: Kind = {
        id: 1,
        vorname: 'Max',
        nachname: 'Mustermann',
        geburtsdatum: '2010-01-01',
      };

      expect(isKindInsured(kind)).toBe(false);
    });

    it('should return false if kind has versicherung_id but no vertrag', () => {
      const kind: Kind = {
        id: 1,
        vorname: 'Max',
        nachname: 'Mustermann',
        geburtsdatum: '2010-01-01',
        versicherung_id: 2,
      };

      expect(isKindInsured(kind)).toBe(false);
    });
  });
});

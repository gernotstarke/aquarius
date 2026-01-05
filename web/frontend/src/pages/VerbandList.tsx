import React, { useState } from 'react';
import { useQuery } from '@tanstack/react-query';
import apiClient from '../api/client';
import { Verband } from '../types';
import Card from '../components/Card';
import Button from '../components/Button';

const VerbandList: React.FC = () => {
  const [sortBy, setSortBy] = useState<'name' | 'nomination_count'>('name');
  const [sortOrder, setSortOrder] = useState<'asc' | 'desc'>('asc');

  const { data: verbaende, isLoading } = useQuery<Verband[]>({
    queryKey: ['verbaende', sortBy, sortOrder],
    queryFn: async () => {
      const response = await apiClient.get('/verband', {
        params: {
          sort_by: sortBy,
          sort_order: sortOrder,
        },
      });
      return response.data;
    },
  });

  const toggleSortOrder = () => {
    setSortOrder(current => current === 'asc' ? 'desc' : 'asc');
  };

  if (isLoading) {
    return <div className="text-center py-12 text-body-lg">Lädt...</div>;
  }

  return (
    <div className="space-y-8">
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
        <h2 className="text-h1 font-bold text-neutral-900">Verbände</h2>
        <div className="flex gap-2">
          <select
            value={sortBy}
            onChange={(e) => setSortBy(e.target.value as 'name' | 'nomination_count')}
            className="px-4 py-3 bg-white border border-neutral-300 rounded-lg text-body focus-ring min-h-touch cursor-pointer"
          >
            <option value="name">Name</option>
            <option value="nomination_count">Nominierungen</option>
          </select>
          <Button variant="secondary" onClick={toggleSortOrder}>
            {sortOrder === 'asc' ? 'Aufsteigend' : 'Absteigend'}
          </Button>
        </div>
      </div>

      <div className="grid gap-6">
        {verbaende?.map((verband) => (
          <Card key={verband.id}>
            <div className="space-y-2">
              <h3 className="text-h3 font-semibold text-neutral-900">
                {verband.name} ({verband.abkuerzung})
              </h3>
              <p className="text-body text-neutral-600">{verband.ort}</p>
              <p className="text-body text-neutral-500">{verband.land}</p>
              <p className="text-body text-neutral-500">
                Nominierungen: {verband.nomination_count ?? 0}
              </p>
            </div>
          </Card>
        ))}

        {(!verbaende || verbaende.length === 0) && (
          <Card>
            <p className="text-center text-body-lg text-neutral-500 py-8">
              Keine Verbände vorhanden
            </p>
          </Card>
        )}
      </div>
    </div>
  );
};

export default VerbandList;

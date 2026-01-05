import React from 'react';
import { useQuery } from '@tanstack/react-query';
import apiClient from '../api/client';
import { Verband } from '../types';
import Card from '../components/Card';

const VerbandList: React.FC = () => {
  const { data: verbaende, isLoading } = useQuery<Verband[]>({
    queryKey: ['verbaende'],
    queryFn: async () => {
      const response = await apiClient.get('/verband');
      return response.data;
    },
  });

  if (isLoading) {
    return <div className="text-center py-12 text-body-lg">Lädt...</div>;
  }

  return (
    <div className="space-y-8">
      <div className="flex items-center justify-between">
        <h2 className="text-h1 font-bold text-neutral-900">Verbände</h2>
      </div>

      <div className="grid gap-6">
        {verbaende?.map((verband) => (
          <Card key={verband.id}>
            <div className="space-y-2">
              <h3 className="text-h3 font-semibold text-neutral-900">
                {verband.name}
              </h3>
              <p className="text-body text-neutral-600">{verband.ort}</p>
              <p className="text-body text-neutral-500">{verband.land}</p>
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

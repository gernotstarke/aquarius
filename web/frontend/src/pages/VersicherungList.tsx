import React from 'react';
import { useQuery } from '@tanstack/react-query';
import apiClient from '../api/client';
import { Versicherung } from '../types';
import Card from '../components/Card';

const VersicherungList: React.FC = () => {
  const { data: versicherungen, isLoading } = useQuery<Versicherung[]>({
    queryKey: ['versicherungen'],
    queryFn: async () => {
      const response = await apiClient.get('/versicherung');
      return response.data;
    },
  });

  if (isLoading) {
    return <div className="text-center py-12 text-body-lg">Lädt...</div>;
  }

  return (
    <div className="space-y-8">
      <div className="flex items-center justify-between">
        <h2 className="text-h1 font-bold text-neutral-900">Versicherungen</h2>
      </div>

      <div className="grid gap-6">
        {versicherungen?.map((versicherung) => (
          <Card key={versicherung.id}>
            <div className="space-y-2">
              <h3 className="text-h3 font-semibold text-neutral-900">
                {versicherung.name} ({versicherung.kurz})
              </h3>
              <p className="text-body text-neutral-600">{versicherung.hauptsitz}</p>
              <p className="text-body text-neutral-500">{versicherung.land}</p>
            </div>
          </Card>
        ))}

        {(!versicherungen || versicherungen.length === 0) && (
          <Card>
            <p className="text-center text-body-lg text-neutral-500 py-8">
              Keine Versicherungen vorhanden
            </p>
          </Card>
        )}
      </div>
    </div>
  );
};

export default VersicherungList;

import React from 'react';
import { Link } from 'react-router-dom';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import apiClient from '../api/client';
import { Verein } from '../types';
import Card from '../components/Card';
import Button from '../components/Button';

const VereinList: React.FC = () => {
  const queryClient = useQueryClient();

  const { data: vereine, isLoading } = useQuery<Verein[]>({
    queryKey: ['vereine'],
    queryFn: async () => {
      const response = await apiClient.get('/verein');
      return response.data;
    },
  });

  const deleteMutation = useMutation({
    mutationFn: (id: number) => apiClient.delete(`/verein/${id}`),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['vereine'] });
    },
  });

  if (isLoading) {
    return <div className="text-center py-12 text-body-lg">Lädt...</div>;
  }

  return (
    <div className="space-y-8">
      <div className="flex items-center justify-between">
        <h2 className="text-h1 font-bold text-neutral-900">Vereine</h2>
        <Link to="/grunddaten/vereine/new">
          <Button size="lg">Neuer Verein</Button>
        </Link>
      </div>

      <div className="grid gap-6">
        {vereine?.map((verein) => (
          <Card key={verein.id}>
            <div className="flex items-center justify-between">
              <Link to={`/grunddaten/vereine/${verein.id}`} className="block flex-1 group">
                <div className="space-y-2">
                  <h3 className="text-h3 font-semibold text-neutral-900 group-hover:text-primary-600 transition-colors">
                    {verein.name}
                  </h3>
                  <p className="text-body text-neutral-600">{verein.ort}</p>
                  <p className="text-body text-neutral-500">Register-ID: {verein.register_id}</p>
                  <p className="text-body text-neutral-500">Kontakt: {verein.contact}</p>
                </div>
              </Link>
              <div className="flex gap-4 ml-4">
                <Link to={`/grunddaten/vereine/${verein.id}`}>
                  <Button variant="secondary">Bearbeiten</Button>
                </Link>
                <Button
                  variant="danger"
                  onClick={() => {
                    if (confirm('Verein wirklich löschen?')) {
                      deleteMutation.mutate(verein.id);
                    }
                  }}
                >
                  Löschen
                </Button>
              </div>
            </div>
          </Card>
        ))}

        {(!vereine || vereine.length === 0) && (
          <Card>
            <p className="text-center text-body-lg text-neutral-500 py-8">
              Keine Vereine vorhanden
            </p>
          </Card>
        )}
      </div>
    </div>
  );
};

export default VereinList;

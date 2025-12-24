import React from 'react';
import { Link } from 'react-router-dom';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import apiClient from '../api/client';
import { Kind } from '../types';
import Card from '../components/Card';
import Button from '../components/Button';

const KindList: React.FC = () => {
  const queryClient = useQueryClient();

  const { data: kinder, isLoading } = useQuery<Kind[]>({
    queryKey: ['kinder'],
    queryFn: async () => {
      const response = await apiClient.get('/kind');
      return response.data;
    },
  });

  const deleteMutation = useMutation({
    mutationFn: (id: number) => apiClient.delete(`/kind/${id}`),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['kinder'] });
    },
  });

  if (isLoading) {
    return <div className="text-center py-12 text-body-lg">Lädt...</div>;
  }

  return (
    <div className="space-y-8">
      <div className="flex items-center justify-between">
        <h2 className="text-h1 font-bold text-neutral-900">Kinder</h2>
        <Link to="/kind/new">
          <Button size="lg">Neues Kind</Button>
        </Link>
      </div>

      <div className="grid gap-6">
        {kinder?.map((kind) => (
          <Card key={kind.id}>
            <div className="flex items-center justify-between">
              <Link to={`/kind/${kind.id}`} className="block flex-1 group">
                <div className="space-y-2">
                  <h3 className="text-h3 font-semibold text-neutral-900 group-hover:text-primary-600 transition-colors">
                    {kind.vorname} {kind.nachname}
                  </h3>
                  <p className="text-body text-neutral-600">
                    Geboren: {kind.geburtsdatum}
                  </p>
                  {kind.geschlecht && (
                    <p className="text-body text-neutral-500">Geschlecht: {kind.geschlecht}</p>
                  )}
                  {kind.verein && (
                    <p className="text-body text-neutral-500">Verein: {kind.verein}</p>
                  )}
                </div>
              </Link>
              <div className="flex gap-4 ml-4">
                <Link to={`/kind/${kind.id}`}>
                  <Button variant="secondary">Bearbeiten</Button>
                </Link>
                <Button
                  variant="danger"
                  onClick={() => {
                    if (confirm('Kind wirklich löschen?')) {
                      deleteMutation.mutate(kind.id);
                    }
                  }}
                >
                  Löschen
                </Button>
              </div>
            </div>
          </Card>
        ))}

        {(!kinder || kinder.length === 0) && (
          <Card>
            <p className="text-center text-body-lg text-neutral-500 py-8">
              Keine Kinder vorhanden
            </p>
          </Card>
        )}
      </div>
    </div>
  );
};

export default KindList;

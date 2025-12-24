import React from 'react';
import { Link } from 'react-router-dom';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import apiClient from '../api/client';
import { Schwimmbad } from '../types';
import Card from '../components/Card';
import Button from '../components/Button';

const SchwimmbadList: React.FC = () => {
  const queryClient = useQueryClient();

  const { data: schwimmbäder, isLoading } = useQuery<Schwimmbad[]>({
    queryKey: ['schwimmbäder'],
    queryFn: async () => {
      const response = await apiClient.get('/schwimmbad');
      return response.data;
    },
  });

  const deleteMutation = useMutation({
    mutationFn: (id: number) => apiClient.delete(`/schwimmbad/${id}`),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['schwimmbäder'] });
    },
  });

  if (isLoading) {
    return <div className="text-center py-12 text-body-lg">Lädt...</div>;
  }

  return (
    <div className="space-y-8">
      <div className="flex items-center justify-between">
        <h2 className="text-h1 font-bold text-neutral-900">Schwimmbäder</h2>
        <Link to="/schwimmbad/new">
          <Button size="lg">Neues Schwimmbad</Button>
        </Link>
      </div>

      <div className="grid gap-6">
        {schwimmbäder?.map((schwimmbad) => (
          <Card key={schwimmbad.id}>
            <div className="flex items-center justify-between">
              <div className="space-y-2">
                <h3 className="text-h3 font-semibold text-neutral-900">{schwimmbad.name}</h3>
                <p className="text-body text-neutral-600">{schwimmbad.adresse}</p>
                {schwimmbad.manager && (
                  <p className="text-body text-neutral-500">Leitung: {schwimmbad.manager}</p>
                )}
                {schwimmbad.phone_no && (
                  <p className="text-body text-neutral-500">Tel: {schwimmbad.phone_no}</p>
                )}
              </div>
              <div className="flex gap-4">
                <Link to={`/schwimmbad/${schwimmbad.id}`}>
                  <Button variant="secondary">Bearbeiten</Button>
                </Link>
                <Button
                  variant="danger"
                  onClick={() => {
                    if (confirm('Schwimmbad wirklich löschen?')) {
                      deleteMutation.mutate(schwimmbad.id);
                    }
                  }}
                >
                  Löschen
                </Button>
              </div>
            </div>
          </Card>
        ))}

        {(!schwimmbäder || schwimmbäder.length === 0) && (
          <Card>
            <p className="text-center text-body-lg text-neutral-500 py-8">
              Keine Schwimmbäder vorhanden
            </p>
          </Card>
        )}
      </div>
    </div>
  );
};

export default SchwimmbadList;

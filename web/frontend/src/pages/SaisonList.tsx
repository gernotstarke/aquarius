import React from 'react';
import { Link } from 'react-router-dom';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import apiClient from '../api/client';
import { Saison } from '../types';
import Card from '../components/Card';
import Button from '../components/Button';
import { useAuth } from '../context/AuthContext';

const SaisonList: React.FC = () => {
  const queryClient = useQueryClient();
  const { canWrite } = useAuth();

  const { data: saisons, isLoading } = useQuery<Saison[]>({
    queryKey: ['saisons'],
    queryFn: async () => {
      const response = await apiClient.get('/saison');
      return response.data;
    },
  });

  const deleteMutation = useMutation({
    mutationFn: (id: number) => apiClient.delete(`/saison/${id}`),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['saisons'] });
    },
  });

  if (isLoading) {
    return <div className="text-center py-12 text-body-lg">Lädt...</div>;
  }

  return (
    <div className="space-y-8">
      <div className="flex items-center justify-between">
        <h2 className="text-h1 font-bold text-neutral-900">Saisons</h2>
        {canWrite && (
          <Link to="/saison/new">
            <Button size="lg">Neue Saison</Button>
          </Link>
        )}
      </div>

      <div className="grid gap-6">
        {saisons?.map((saison) => (
          <Card key={saison.id}>
            <div className="flex items-center justify-between">
              <Link to={`/saison/${saison.id}`} className="block flex-1 group">
                <div className="space-y-2">
                  <h3 className="text-h3 font-semibold text-neutral-900 group-hover:text-primary-600 transition-colors">
                    {saison.name}
                  </h3>
                  <p className="text-body text-neutral-600">
                    {saison.from_date} bis {saison.to_date}
                  </p>
                </div>
              </Link>
              {canWrite && (
                <div className="flex gap-4 ml-4">
                  <Link to={`/saison/${saison.id}`}>
                    <Button variant="secondary">Bearbeiten</Button>
                  </Link>
                  <Button
                    variant="danger"
                    onClick={() => {
                      if (confirm('Saison wirklich löschen?')) {
                        deleteMutation.mutate(saison.id);
                      }
                    }}
                  >
                    Löschen
                  </Button>
                </div>
              )}
            </div>
          </Card>
        ))}

        {(!saisons || saisons.length === 0) && (
          <Card>
            <p className="text-center text-body-lg text-neutral-500 py-8">
              Keine Saisons vorhanden
            </p>
          </Card>
        )}
      </div>
    </div>
  );
};

export default SaisonList;

import React from 'react';
import { Link } from 'react-router-dom';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import apiClient from '../api/client';
import { Wettkampf } from '../types';
import Card from '../components/Card';
import Button from '../components/Button';

const WettkampfList: React.FC = () => {
  const queryClient = useQueryClient();

  const { data: wettkämpfe, isLoading } = useQuery<Wettkampf[]>({
    queryKey: ['wettkämpfe'],
    queryFn: async () => {
      const response = await apiClient.get('/wettkampf');
      return response.data;
    },
  });

  const deleteMutation = useMutation({
    mutationFn: (id: number) => apiClient.delete(`/wettkampf/${id}`),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['wettkämpfe'] });
    },
  });

  if (isLoading) {
    return <div className="text-center py-12 text-body-lg">Lädt...</div>;
  }

  return (
    <div className="space-y-8">
      <div className="flex items-center justify-between">
        <h2 className="text-h1 font-bold text-neutral-900">Wettkämpfe</h2>
        <Link to="/wettkaempfe/new">
          <Button size="lg">Neuer Wettkampf</Button>
        </Link>
      </div>

      <div className="grid gap-6">
        {wettkämpfe?.map((wettkampf) => (
          <Card key={wettkampf.id}>
            <div className="flex items-center justify-between">
              <div className="space-y-2 flex-1">
                <Link to={`/wettkaempfe/${wettkampf.id}/detail`}>
                  <h3 className="text-h3 font-semibold text-neutral-900 hover:text-primary-600 transition-colors">
                    {wettkampf.name}
                  </h3>
                </Link>
                <p className="text-body text-neutral-600">Datum: {wettkampf.datum}</p>
                {wettkampf.max_teilnehmer && (
                  <p className="text-body text-neutral-500">
                    Max. Teilnehmer: {wettkampf.max_teilnehmer}
                  </p>
                )}
              </div>
              <div className="flex gap-4">
                <Link to={`/wettkaempfe/${wettkampf.id}/detail`}>
                  <Button>Details</Button>
                </Link>
                <Link to={`/wettkaempfe/${wettkampf.id}`}>
                  <Button variant="secondary">Bearbeiten</Button>
                </Link>
                <Button
                  variant="danger"
                  onClick={() => {
                    if (confirm('Wettkampf wirklich löschen?')) {
                      deleteMutation.mutate(wettkampf.id);
                    }
                  }}
                >
                  Löschen
                </Button>
              </div>
            </div>
          </Card>
        ))}

        {(!wettkämpfe || wettkämpfe.length === 0) && (
          <Card>
            <p className="text-center text-body-lg text-neutral-500 py-8">
              Keine Wettkämpfe vorhanden
            </p>
          </Card>
        )}
      </div>
    </div>
  );
};

export default WettkampfList;

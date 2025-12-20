import React from 'react';
import { Link } from 'react-router-dom';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import apiClient from '../api/client';
import { Anmeldung, Kind, Wettkampf } from '../types';
import Card from '../components/Card';
import Button from '../components/Button';

const AnmeldungList: React.FC = () => {
  const queryClient = useQueryClient();

  const { data: anmeldungen, isLoading } = useQuery<Anmeldung[]>({
    queryKey: ['anmeldungen'],
    queryFn: async () => {
      const response = await apiClient.get('/anmeldung');
      return response.data;
    },
  });

  const { data: kinder } = useQuery<Kind[]>({
    queryKey: ['kinder'],
    queryFn: async () => {
      const response = await apiClient.get('/kind');
      return response.data;
    },
  });

  const { data: wettkaempfe } = useQuery<Wettkampf[]>({
    queryKey: ['wettkaempfe'],
    queryFn: async () => {
      const response = await apiClient.get('/wettkampf');
      return response.data;
    },
  });

  const deleteMutation = useMutation({
    mutationFn: (id: number) => apiClient.delete(`/anmeldung/${id}`),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['anmeldungen'] });
    },
  });

  if (isLoading) {
    return <div className="text-center py-12 text-body-lg">Lädt...</div>;
  }

  const getKindName = (kindId: number) => {
    const kind = kinder?.find(k => k.id === kindId);
    return kind ? `${kind.vorname} ${kind.nachname}` : `Kind #${kindId}`;
  };

  const getWettkampfName = (wettkampfId: number) => {
    const wettkampf = wettkaempfe?.find(w => w.id === wettkampfId);
    return wettkampf ? wettkampf.name : `Wettkampf #${wettkampfId}`;
  };

  return (
    <div className="space-y-8">
      <div className="flex items-center justify-between">
        <h2 className="text-h1 font-bold text-neutral-900">Anmeldungen</h2>
        <Link to="/anmeldung/new">
          <Button size="lg">Neue Anmeldung</Button>
        </Link>
      </div>

      <div className="grid gap-6">
        {anmeldungen?.map((anmeldung) => (
          <Card key={anmeldung.id}>
            <div className="flex items-start justify-between">
              <div className="space-y-3 flex-1">
                <div className="flex items-center gap-3">
                  <h3 className="text-h3 font-semibold text-neutral-900">
                    {getKindName(anmeldung.kind_id)}
                  </h3>
                  <span
                    className={`px-3 py-1 rounded-full text-sm ${
                      anmeldung.status === 'aktiv'
                        ? 'bg-green-100 text-green-700'
                        : 'bg-neutral-200 text-neutral-700'
                    }`}
                  >
                    {anmeldung.status}
                  </span>
                </div>
                <p className="text-body text-neutral-600">
                  {getWettkampfName(anmeldung.wettkampf_id)}
                </p>
                <p className="text-sm text-neutral-500">
                  Angemeldet am: {anmeldung.anmeldedatum}
                </p>
                {anmeldung.figuren.length > 0 && (
                  <div>
                    <p className="text-sm font-medium text-neutral-700 mb-2">
                      Figuren ({anmeldung.figuren.length}):
                    </p>
                    <div className="flex flex-wrap gap-2">
                      {anmeldung.figuren.map((figur) => (
                        <span
                          key={figur.id}
                          className="px-3 py-1 bg-primary-100 text-primary-700 rounded-full text-sm"
                        >
                          {figur.name}
                        </span>
                      ))}
                    </div>
                  </div>
                )}
              </div>
              <div className="flex gap-4">
                <Link to={`/anmeldung/${anmeldung.id}`}>
                  <Button variant="secondary">Bearbeiten</Button>
                </Link>
                <Button
                  variant="danger"
                  onClick={() => {
                    if (confirm('Anmeldung wirklich löschen?')) {
                      deleteMutation.mutate(anmeldung.id);
                    }
                  }}
                >
                  Löschen
                </Button>
              </div>
            </div>
          </Card>
        ))}

        {(!anmeldungen || anmeldungen.length === 0) && (
          <Card>
            <p className="text-center text-body-lg text-neutral-500 py-8">
              Keine Anmeldungen vorhanden
            </p>
          </Card>
        )}
      </div>
    </div>
  );
};

export default AnmeldungList;

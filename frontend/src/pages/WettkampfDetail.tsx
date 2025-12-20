import React, { useState } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import apiClient from '../api/client';
import { WettkampfWithDetails, Figur } from '../types';
import Card from '../components/Card';
import Tabs from '../components/Tabs';
import Button from '../components/Button';
import Input from '../components/Input';

const WettkampfDetail: React.FC = () => {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();
  const queryClient = useQueryClient();
  const [activeTab, setActiveTab] = useState('basis');

  const { data: wettkampf, isLoading } = useQuery<WettkampfWithDetails>({
    queryKey: ['wettkampf-details', id],
    queryFn: async () => {
      const response = await apiClient.get(`/wettkampf/${id}/details`);
      return response.data;
    },
  });

  const { data: allFiguren } = useQuery<Figur[]>({
    queryKey: ['figuren'],
    queryFn: async () => {
      const response = await apiClient.get('/figur');
      return response.data;
    },
  });

  const addFigurMutation = useMutation({
    mutationFn: (figurId: number) =>
      apiClient.post(`/wettkampf/${id}/figuren/${figurId}`),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['wettkampf-details', id] });
    },
  });

  const removeFigurMutation = useMutation({
    mutationFn: (figurId: number) =>
      apiClient.delete(`/wettkampf/${id}/figuren/${figurId}`),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['wettkampf-details', id] });
    },
  });

  if (isLoading) {
    return <div className="text-center py-12">Lädt...</div>;
  }

  if (!wettkampf) {
    return <div className="text-center py-12">Wettkampf nicht gefunden</div>;
  }

  const availableFiguren = allFiguren?.filter(
    f => !wettkampf.figuren.some(wf => wf.id === f.id)
  ) || [];

  const tabs = [
    {
      id: 'basis',
      label: 'Basis',
      content: (
        <Card>
          <div className="space-y-6">
            <h3 className="text-h2 font-bold">{wettkampf.name}</h3>
            <div className="grid grid-cols-2 gap-6">
              <div>
                <p className="text-sm text-neutral-500">Datum</p>
                <p className="text-body-lg font-medium">{wettkampf.datum}</p>
              </div>
              <div>
                <p className="text-sm text-neutral-500">Max. Teilnehmer</p>
                <p className="text-body-lg font-medium">
                  {wettkampf.max_teilnehmer || '—'}
                </p>
              </div>
              <div>
                <p className="text-sm text-neutral-500">Saison ID</p>
                <p className="text-body-lg font-medium">{wettkampf.saison_id}</p>
              </div>
              <div>
                <p className="text-sm text-neutral-500">Schwimmbad ID</p>
                <p className="text-body-lg font-medium">{wettkampf.schwimmbad_id}</p>
              </div>
            </div>
            <div className="pt-4">
              <Button
                variant="secondary"
                onClick={() => navigate(`/wettkampf/${id}`)}
              >
                Bearbeiten
              </Button>
            </div>
          </div>
        </Card>
      ),
    },
    {
      id: 'figuren',
      label: 'Figuren',
      content: (
        <div className="space-y-6">
          <Card>
            <h3 className="text-h3 font-bold mb-4">
              Erlaubte Figuren ({wettkampf.figuren.length})
            </h3>
            {wettkampf.figuren.length === 0 ? (
              <p className="text-neutral-500">Keine Figuren zugewiesen</p>
            ) : (
              <div className="space-y-3">
                {wettkampf.figuren.map((figur) => (
                  <div
                    key={figur.id}
                    className="flex items-center justify-between p-4 bg-neutral-50 rounded-lg"
                  >
                    <div>
                      <p className="font-medium">{figur.name}</p>
                      <p className="text-sm text-neutral-600">
                        {figur.kategorie} • Schwierigkeit: {(figur.schwierigkeitsgrad || 0) / 10}
                      </p>
                    </div>
                    <Button
                      variant="danger"
                      size="sm"
                      onClick={() => removeFigurMutation.mutate(figur.id)}
                    >
                      Entfernen
                    </Button>
                  </div>
                ))}
              </div>
            )}
          </Card>

          {availableFiguren.length > 0 && (
            <Card>
              <h3 className="text-h3 font-bold mb-4">
                Verfügbare Figuren ({availableFiguren.length})
              </h3>
              <div className="space-y-3 max-h-96 overflow-y-auto">
                {availableFiguren.map((figur) => (
                  <div
                    key={figur.id}
                    className="flex items-center justify-between p-4 bg-neutral-50 rounded-lg"
                  >
                    <div>
                      <p className="font-medium">{figur.name}</p>
                      <p className="text-sm text-neutral-600">
                        {figur.kategorie} • Schwierigkeit: {(figur.schwierigkeitsgrad || 0) / 10}
                      </p>
                    </div>
                    <Button
                      size="sm"
                      onClick={() => addFigurMutation.mutate(figur.id)}
                    >
                      Hinzufügen
                    </Button>
                  </div>
                ))}
              </div>
            </Card>
          )}
        </div>
      ),
    },
    {
      id: 'stationen',
      label: 'Stationen',
      content: (
        <Card>
          <div className="text-center py-12">
            <p className="text-neutral-500 mb-4">Stationsplanung kommt später</p>
            <p className="text-sm text-neutral-400">
              Hier können Sie Stationen definieren und Figuren zuweisen
            </p>
          </div>
        </Card>
      ),
    },
    {
      id: 'zeitplanung',
      label: 'Zeitplanung',
      content: (
        <Card>
          <div className="text-center py-12">
            <p className="text-neutral-500 mb-4">Zeitplanung kommt später</p>
            <p className="text-sm text-neutral-400">
              Hier können Sie Gruppen und Zeitslots planen
            </p>
          </div>
        </Card>
      ),
    },
    {
      id: 'anmeldungen',
      label: `Anmeldungen (${wettkampf.anmeldungen.length})`,
      content: (
        <Card>
          <h3 className="text-h3 font-bold mb-6">
            Anmeldungen ({wettkampf.anmeldungen.length})
          </h3>
          {wettkampf.anmeldungen.length === 0 ? (
            <p className="text-neutral-500 text-center py-8">
              Noch keine Anmeldungen vorhanden
            </p>
          ) : (
            <div className="space-y-4">
              {wettkampf.anmeldungen.map((anmeldung) => (
                <div
                  key={anmeldung.id}
                  className="p-6 bg-neutral-50 rounded-lg"
                >
                  <div className="flex items-start justify-between mb-4">
                    <div>
                      <p className="font-medium text-body-lg">
                        Anmeldung #{anmeldung.id}
                      </p>
                      <p className="text-sm text-neutral-600">
                        Kind-ID: {anmeldung.kind_id} • {anmeldung.anmeldedatum}
                      </p>
                    </div>
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
                  {anmeldung.figuren.length > 0 && (
                    <div>
                      <p className="text-sm font-medium text-neutral-700 mb-2">
                        Ausgewählte Figuren:
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
              ))}
            </div>
          )}
        </Card>
      ),
    },
  ];

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <h1 className="text-display font-bold">{wettkampf.name}</h1>
        <Button variant="secondary" onClick={() => navigate('/wettkaempfe')}>
          ← Zurück
        </Button>
      </div>

      <Tabs tabs={tabs} activeTab={activeTab} onChange={setActiveTab} />
    </div>
  );
};

export default WettkampfDetail;

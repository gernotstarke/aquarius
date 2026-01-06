import React from 'react';
import { Link } from 'react-router-dom';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import apiClient from '../api/client';
import { Anmeldung, Wettkampf } from '../types';
import Card from '../components/Card';
import Button from '../components/Button';

const AnmeldungList: React.FC = () => {
  const queryClient = useQueryClient();
  const [selectedWettkampfId, setSelectedWettkampfId] = React.useState<number>(0);

  const { data: anmeldungen, isLoading } = useQuery<Anmeldung[]>({
    queryKey: ['anmeldungen'],
    queryFn: async () => {
      const response = await apiClient.get('/anmeldung');
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

  const getKindName = (anmeldung: Anmeldung) => {
    if (anmeldung.kind) {
      return `${anmeldung.kind.vorname} ${anmeldung.kind.nachname}`;
    }
    return `Kind #${anmeldung.kind_id}`;
  };

  const getWettkampfName = (wettkampfId: number) => {
    const wettkampf = wettkaempfe?.find(w => w.id === wettkampfId);
    return wettkampf ? wettkampf.name : `Wettkampf #${wettkampfId}`;
  };

  // Filter anmeldungen by selected wettkampf
  const filteredAnmeldungen = selectedWettkampfId === 0
    ? anmeldungen
    : anmeldungen?.filter(a => a.wettkampf_id === selectedWettkampfId);

  return (
    <div className="space-y-8">
      <div className="flex items-center justify-between">
        <h2 className="text-h1 font-bold text-neutral-900">Anmeldungen</h2>
        <Link to="/anmeldung/new">
          <Button size="lg">Neue Anmeldung</Button>
        </Link>
      </div>

      {/* Wettkampf Filter */}
      <div className="bg-neutral-50 p-4 rounded-lg border border-neutral-200">
        <label className="block text-sm font-medium text-neutral-700 mb-2">
          Wettkampf filtern
        </label>
        <select
          value={selectedWettkampfId}
          onChange={(e) => setSelectedWettkampfId(Number(e.target.value))}
          className="w-full md:w-auto px-4 py-3 bg-white border border-neutral-300 rounded-lg text-body focus-ring min-h-touch cursor-pointer"
        >
          <option value={0}>Alle Wettkämpfe</option>
          {wettkaempfe?.map((wettkampf) => (
            <option key={wettkampf.id} value={wettkampf.id}>
              {wettkampf.name} - {wettkampf.datum}
            </option>
          ))}
        </select>
      </div>

      <div className="grid gap-6">
        {filteredAnmeldungen?.map((anmeldung) => (
          <Card key={anmeldung.id} className="transition-shadow hover:shadow-md">
            <div className="flex items-start justify-between">
              <Link to={`/anmeldung/${anmeldung.id}`} className="space-y-3 flex-1 group block">
                <div className="flex items-center gap-3">
                  <span className="px-3 py-1 bg-primary-600 text-white rounded-full text-sm font-semibold">
                    #{anmeldung.startnummer}
                  </span>
                  <h3 className="text-h3 font-semibold text-neutral-900 group-hover:text-primary-600 transition-colors">
                    {getKindName(anmeldung)}
                  </h3>
                  {anmeldung.vorlaeufig === 1 && (
                    <span className="px-3 py-1 rounded-full text-sm bg-yellow-100 text-yellow-700">
                      vorläufig
                    </span>
                  )}
                  {anmeldung.insurance_ok === false && (
                    <span className="px-3 py-1 rounded-full text-sm bg-orange-100 text-orange-700">
                      unversichert
                    </span>
                  )}
                  {anmeldung.vorlaeufig === 0 && anmeldung.status === 'aktiv' && (
                    <span className="px-3 py-1 rounded-full text-sm bg-green-100 text-green-700">
                      aktiv
                    </span>
                  )}
                  {anmeldung.status === 'storniert' && (
                    <span className="px-3 py-1 rounded-full text-sm bg-red-100 text-red-700">
                      storniert
                    </span>
                  )}
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
              </Link>
              <div className="flex gap-4 ml-4">
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

        {(!filteredAnmeldungen || filteredAnmeldungen.length === 0) && (
          <Card>
            <p className="text-center text-body-lg text-neutral-500 py-8">
              {selectedWettkampfId === 0
                ? 'Keine Anmeldungen vorhanden'
                : 'Keine Anmeldungen für den ausgewählten Wettkampf vorhanden'}
            </p>
          </Card>
        )}
      </div>
    </div>
  );
};

export default AnmeldungList;

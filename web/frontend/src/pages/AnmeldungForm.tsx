import React, { useState, useEffect } from 'react';
import { useNavigate, useParams, useSearchParams } from 'react-router-dom';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import apiClient from '../api/client';
import { AnmeldungCreate, Kind, Wettkampf, WettkampfWithDetails, Anmeldung } from '../types';
import Card from '../components/Card';
import Button from '../components/Button';

const AnmeldungForm: React.FC = () => {
  const { id } = useParams();
  const [searchParams] = useSearchParams();
  const navigate = useNavigate();
  const queryClient = useQueryClient();
  const isEdit = Boolean(id);

  const preselectedWettkampfId = searchParams.get('wettkampf');

  const [selectedKindId, setSelectedKindId] = useState<number>(0);
  const [selectedWettkampfId, setSelectedWettkampfId] = useState<number>(
    preselectedWettkampfId ? Number(preselectedWettkampfId) : 0
  );
  const [selectedFigurIds, setSelectedFigurIds] = useState<number[]>([]);

  const { data: anmeldung } = useQuery<Anmeldung>({
    queryKey: ['anmeldung', id],
    queryFn: async () => {
      const response = await apiClient.get(`/anmeldung/${id}`);
      return response.data;
    },
    enabled: isEdit,
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

  const { data: wettkampfDetails } = useQuery<WettkampfWithDetails>({
    queryKey: ['wettkampf-details', selectedWettkampfId],
    queryFn: async () => {
      const response = await apiClient.get(`/wettkampf/${selectedWettkampfId}/details`);
      return response.data;
    },
    enabled: selectedWettkampfId > 0,
  });

  useEffect(() => {
    if (anmeldung) {
      setSelectedKindId(anmeldung.kind_id);
      setSelectedWettkampfId(anmeldung.wettkampf_id);
      setSelectedFigurIds(anmeldung.figuren.map(f => f.id));
    }
  }, [anmeldung]);

  const createMutation = useMutation({
    mutationFn: (data: AnmeldungCreate) => apiClient.post('/anmeldung', data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['anmeldungen'] });
      navigate('/anmeldung/liste');
    },
  });

  const updateMutation = useMutation({
    mutationFn: (data: { figur_ids: number[] }) =>
      apiClient.put(`/anmeldung/${id}`, data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['anmeldungen'] });
      queryClient.invalidateQueries({ queryKey: ['anmeldung', id] });
      navigate('/anmeldung/liste');
    },
  });

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (isEdit) {
      updateMutation.mutate({ figur_ids: selectedFigurIds });
    } else {
      createMutation.mutate({
        kind_id: selectedKindId,
        wettkampf_id: selectedWettkampfId,
        figur_ids: selectedFigurIds,
      });
    }
  };

  const toggleFigur = (figurId: number) => {
    setSelectedFigurIds(prev =>
      prev.includes(figurId)
        ? prev.filter(id => id !== figurId)
        : [...prev, figurId]
    );
  };

  const availableFiguren = wettkampfDetails?.figuren || [];

  return (
    <div className="max-w-3xl space-y-8">
      <h2 className="text-h1 font-bold text-neutral-900">
        {isEdit ? 'Anmeldung bearbeiten' : 'Neue Anmeldung'}
      </h2>

      <Card>
        <form onSubmit={handleSubmit} className="space-y-6">
          {/* Kind auswählen */}
          <div className="space-y-2">
            <label className="block text-body font-medium text-neutral-700">
              Kind
            </label>
            <select
              className="w-full px-4 py-3 min-h-touch text-body bg-white border rounded-lg border-neutral-300 focus-ring"
              value={selectedKindId}
              onChange={(e) => setSelectedKindId(Number(e.target.value))}
              required
              disabled={isEdit}
            >
              <option value={0}>Bitte wählen...</option>
              {kinder?.map((kind) => (
                <option key={kind.id} value={kind.id}>
                  {kind.vorname} {kind.nachname} ({kind.verein?.name || 'Kein Verein'})
                </option>
              ))}
            </select>
          </div>

          {/* Wettkampf auswählen */}
          <div className="space-y-2">
            <label className="block text-body font-medium text-neutral-700">
              Wettkampf
            </label>
            <select
              className="w-full px-4 py-3 min-h-touch text-body bg-white border rounded-lg border-neutral-300 focus-ring"
              value={selectedWettkampfId}
              onChange={(e) => {
                setSelectedWettkampfId(Number(e.target.value));
                setSelectedFigurIds([]); // Reset selected figures when changing competition
              }}
              required
              disabled={isEdit}
            >
              <option value={0}>Bitte wählen...</option>
              {wettkaempfe?.map((wettkampf) => (
                <option key={wettkampf.id} value={wettkampf.id}>
                  {wettkampf.name} - {wettkampf.datum}
                </option>
              ))}
            </select>
          </div>

          {/* Figuren auswählen */}
          {selectedWettkampfId > 0 && (
            <div className="space-y-4">
              <label className="block text-body font-medium text-neutral-700">
                Figuren auswählen ({selectedFigurIds.length} ausgewählt)
              </label>

              {/* Info box for preliminary registration */}
              {selectedFigurIds.length === 0 && (
                <div className="bg-yellow-50 border border-yellow-200 rounded-lg p-4">
                  <p className="text-sm text-yellow-800">
                    <strong>Hinweis:</strong> Wenn keine Figuren ausgewählt werden, wird eine <strong>vorläufige Anmeldung</strong> erstellt.
                    Die Figuren können später noch ausgewählt werden.
                  </p>
                </div>
              )}

              {availableFiguren.length === 0 ? (
                <p className="text-neutral-500 py-4">
                  Für diesen Wettkampf sind noch keine Figuren zugelassen.
                </p>
              ) : (
                <div className="max-h-96 overflow-y-auto space-y-2 border border-neutral-200 rounded-lg p-4">
                  {availableFiguren.map((figur) => (
                    <label
                      key={figur.id}
                      className={`
                        flex items-center gap-3 p-4 rounded-lg cursor-pointer transition-colors
                        ${selectedFigurIds.includes(figur.id)
                          ? 'bg-primary-50 border-2 border-primary-500'
                          : 'bg-neutral-50 border-2 border-transparent hover:bg-neutral-100'}
                      `}
                    >
                      <input
                        type="checkbox"
                        className="w-5 h-5 text-primary-600 rounded focus:ring-primary-500"
                        checked={selectedFigurIds.includes(figur.id)}
                        onChange={() => toggleFigur(figur.id)}
                      />
                      <div className="flex-1">
                        <p className="font-medium">{figur.name}</p>
                        <p className="text-sm text-neutral-600">
                          {figur.kategorie} • Schwierigkeit: {(figur.schwierigkeitsgrad || 0) / 10}
                        </p>
                      </div>
                    </label>
                  ))}
                </div>
              )}
            </div>
          )}

          <div className="flex gap-4 pt-4">
            <Button type="submit" size="lg">
              {isEdit ? 'Speichern' : 'Anmelden'}
            </Button>
            <Button
              type="button"
              variant="secondary"
              size="lg"
              onClick={() => navigate('/anmeldung/liste')}
            >
              Abbrechen
            </Button>
          </div>
        </form>
      </Card>
    </div>
  );
};

export default AnmeldungForm;

import React, { useEffect, useState } from 'react';
import { useNavigate, useParams } from 'react-router-dom';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { getKind, createKind, updateKind } from '../api/kind';
import { listVereine, listVerbaende, listVersicherungen } from '../api/grunddaten';
import { Kind, KindCreate } from '../types/kind';
import { Verein, Verband, Versicherung } from '../types/grunddaten';
import Card from '../components/Card';
import Input from '../components/Input';
import Button from '../components/Button';
import { useAuth } from '../context/AuthContext';

const KindForm: React.FC = () => {
  const { id } = useParams();
  const navigate = useNavigate();
  const queryClient = useQueryClient();
  const { canWrite } = useAuth();
  const isEdit = Boolean(id);
  const [isInitialized, setIsInitialized] = useState(false);

  const [formData, setFormData] = useState<KindCreate>({
    vorname: '',
    nachname: '',
    geburtsdatum: '',
    geschlecht: '',
    verein_id: undefined,
    verband_id: undefined,
    versicherung_id: undefined,
    vertrag: '',
  });

  const { data: vereine } = useQuery<Verein[], Error, Verein[]>({
    queryKey: ['vereine'],
    queryFn: () => listVereine(),
  });

  const { data: verbaende } = useQuery<Verband[], Error, Verband[]>({
    queryKey: ['verbaende'],
    queryFn: () => listVerbaende(),
  });

  const { data: versicherungen } = useQuery<Versicherung[], Error, Versicherung[]>({
    queryKey: ['versicherungen'],
    queryFn: () => listVersicherungen(),
  });

  const { data: kind } = useQuery<Kind>({
    queryKey: ['kind', id],
    queryFn: () => getKind(Number(id)),
    enabled: isEdit,
  });

  // Reset initialization when ID changes (e.g. navigation between kinds)
  useEffect(() => {
    setIsInitialized(false);
  }, [id]);

  useEffect(() => {
    if (kind && !isInitialized) {
      setFormData({
        vorname: kind.vorname,
        nachname: kind.nachname,
        geburtsdatum: kind.geburtsdatum,
        geschlecht: kind.geschlecht || '',
        verein_id: kind.verein_id,
        verband_id: kind.verband_id,
        versicherung_id: kind.versicherung_id,
        vertrag: kind.vertrag || '',
      });
      setIsInitialized(true);
    }
  }, [kind, isInitialized]);

  const createMutation = useMutation({
    mutationFn: createKind,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['kinder'] });
      navigate('/kind');
    },
  });

  const updateMutation = useMutation({
    mutationFn: (data: KindCreate) => updateKind(Number(id), data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['kinder'] });
      queryClient.invalidateQueries({ queryKey: ['kind', id] });
      navigate('/kind');
    },
  });

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (!canWrite) return;

    if (isEdit) {
      updateMutation.mutate(formData);
    } else {
      createMutation.mutate(formData);
    }
  };

  if (isEdit && (!kind || !isInitialized)) {
    return <div className="text-center py-12">Lädt...</div>;
  }

  return (
    <div className="max-w-2xl space-y-8">
      <h2 className="text-h1 font-bold text-neutral-900">
        {isEdit ? 'Kind bearbeiten' : 'Neues Kind'}
      </h2>

      <Card>
        <form onSubmit={handleSubmit} className="space-y-6">
          {!canWrite && (
            <div className="px-4 py-3 rounded bg-orange-50 border border-orange-200 text-orange-700">
              Keine Schreibrechte.
            </div>
          )}
          <Input
            label="Vorname"
            name="vorname"
            type="text"
            value={formData.vorname}
            onChange={(e) => setFormData({ ...formData, vorname: e.target.value })}
            disabled={!canWrite}
            required
            placeholder="z.B. Max"
          />

          <Input
            label="Nachname"
            name="nachname"
            type="text"
            value={formData.nachname}
            onChange={(e) => setFormData({ ...formData, nachname: e.target.value })}
            disabled={!canWrite}
            required
            placeholder="z.B. Mustermann"
          />

          <Input
            label="Geburtsdatum"
            name="geburtsdatum"
            type="date"
            value={formData.geburtsdatum}
            onChange={(e) => setFormData({ ...formData, geburtsdatum: e.target.value })}
            disabled={!canWrite}
            required
          />

          <div className="space-y-2">
            <label className="block text-body font-medium text-neutral-700">
              Geschlecht (optional)
            </label>
            <select
              name="geschlecht"
              className="w-full px-4 py-3 min-h-touch text-body bg-white border rounded-lg border-neutral-300 focus-ring"
              value={formData.geschlecht ?? ''}
              onChange={(e) => setFormData({ ...formData, geschlecht: e.target.value })}
              disabled={!canWrite}
            >
              <option value="">Bitte wählen...</option>
              <option value="M">Männlich</option>
              <option value="W">Weiblich</option>
              <option value="D">Divers</option>
            </select>
          </div>

          <div className="space-y-2">
            <label className="block text-body font-medium text-neutral-700">
              Verein (optional)
            </label>
            <select
              name="verein_id"
              className="w-full px-4 py-3 min-h-touch text-body bg-white border rounded-lg border-neutral-300 focus-ring"
              value={formData.verein_id || ''}
              onChange={(e) => setFormData({ ...formData, verein_id: e.target.value ? Number(e.target.value) : null })}
              disabled={!canWrite}
            >
              <option value="">Kein Verein</option>
              {vereine?.map((verein) => (
                <option key={verein.id} value={verein.id}>
                  {verein.name} ({verein.ort})
                </option>
              ))}
            </select>
          </div>

          <div className="space-y-2">
            <label className="block text-body font-medium text-neutral-700">
              Verband (optional)
            </label>
            <select
              name="verband_id"
              className="w-full px-4 py-3 min-h-touch text-body bg-white border rounded-lg border-neutral-300 focus-ring"
              value={formData.verband_id || ''}
              onChange={(e) => setFormData({ ...formData, verband_id: e.target.value ? Number(e.target.value) : null })}
              disabled={!canWrite}
            >
              <option value="">Kein Verband</option>
              {verbaende?.map((verband) => (
                <option key={verband.id} value={verband.id}>
                  {verband.abkuerzung} — {verband.name}
                </option>
              ))}
            </select>
          </div>

          <div className="space-y-2">
            <label className="block text-body font-medium text-neutral-700">
              Versicherung (optional)
            </label>
            <select
              name="versicherung_id"
              className="w-full px-4 py-3 min-h-touch text-body bg-white border rounded-lg border-neutral-300 focus-ring"
              value={formData.versicherung_id || ''}
              onChange={(e) => setFormData({ ...formData, versicherung_id: e.target.value ? Number(e.target.value) : null })}
              disabled={!canWrite}
            >
              <option value="">Keine Versicherung</option>
              {versicherungen?.map((versicherung) => (
                <option key={versicherung.id} value={versicherung.id}>
                  {versicherung.kurz} — {versicherung.name}
                </option>
              ))}
            </select>
          </div>

          <Input
            label="Vertragsnummer (optional)"
            name="vertrag"
            type="text"
            value={formData.vertrag || ''}
            onChange={(e) => setFormData({ ...formData, vertrag: e.target.value })}
            disabled={!canWrite}
            placeholder="z.B. VK-2024-1234"
          />

          <div className="flex gap-4 pt-4">
            <Button type="submit" size="lg" disabled={!canWrite}>
              {isEdit ? 'Speichern' : 'Erstellen'}
            </Button>
            <Button
              type="button"
              variant="secondary"
              size="lg"
              onClick={() => navigate('/kind')}
            >
              Abbrechen
            </Button>
          </div>
        </form>
      </Card>
    </div>
  );
};

export default KindForm;

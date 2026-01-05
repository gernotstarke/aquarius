import React, { useEffect, useState } from 'react';
import { useNavigate, useParams } from 'react-router-dom';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import apiClient from '../api/client';
import { Kind, KindCreate, Verein, Verband } from '../types';
import Card from '../components/Card';
import Input from '../components/Input';
import Button from '../components/Button';

const KindForm: React.FC = () => {
  const { id } = useParams();
  const navigate = useNavigate();
  const queryClient = useQueryClient();
  const isEdit = Boolean(id);

  const [formData, setFormData] = useState<KindCreate>({
    vorname: '',
    nachname: '',
    geburtsdatum: '',
    geschlecht: '',
    verein_id: undefined,
    verband_id: undefined,
  });

  const { data: vereine } = useQuery<Verein[]>({
    queryKey: ['vereine'],
    queryFn: async () => {
      const response = await apiClient.get('/verein');
      return response.data;
    },
  });

  const { data: verbaende } = useQuery<Verband[]>({
    queryKey: ['verbaende'],
    queryFn: async () => {
      const response = await apiClient.get('/verband');
      return response.data;
    },
  });

  const { data: kind } = useQuery<Kind>({
    queryKey: ['kind', id],
    queryFn: async () => {
      const response = await apiClient.get(`/kind/${id}`);
      return response.data;
    },
    enabled: isEdit,
  });

  useEffect(() => {
    if (kind) {
      setFormData({
        vorname: kind.vorname,
        nachname: kind.nachname,
        geburtsdatum: kind.geburtsdatum,
        geschlecht: kind.geschlecht || '',
        verein_id: kind.verein_id,
        verband_id: kind.verband_id,
      });
    }
  }, [kind]);

  const createMutation = useMutation({
    mutationFn: (data: KindCreate) => apiClient.post('/kind', data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['kinder'] });
      navigate('/kind');
    },
  });

  const updateMutation = useMutation({
    mutationFn: (data: KindCreate) => apiClient.put(`/kind/${id}`, data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['kinder'] });
      queryClient.invalidateQueries({ queryKey: ['kind', id] });
      navigate('/kind');
    },
  });

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (isEdit) {
      updateMutation.mutate(formData);
    } else {
      createMutation.mutate(formData);
    }
  };

  return (
    <div className="max-w-2xl space-y-8">
      <h2 className="text-h1 font-bold text-neutral-900">
        {isEdit ? 'Kind bearbeiten' : 'Neues Kind'}
      </h2>

      <Card>
        <form onSubmit={handleSubmit} className="space-y-6">
          <Input
            label="Vorname"
            type="text"
            value={formData.vorname}
            onChange={(e) => setFormData({ ...formData, vorname: e.target.value })}
            required
            placeholder="z.B. Max"
          />

          <Input
            label="Nachname"
            type="text"
            value={formData.nachname}
            onChange={(e) => setFormData({ ...formData, nachname: e.target.value })}
            required
            placeholder="z.B. Mustermann"
          />

          <Input
            label="Geburtsdatum"
            type="date"
            value={formData.geburtsdatum}
            onChange={(e) => setFormData({ ...formData, geburtsdatum: e.target.value })}
            required
          />

          <div className="space-y-2">
            <label className="block text-body font-medium text-neutral-700">
              Geschlecht (optional)
            </label>
            <select
              className="w-full px-4 py-3 min-h-touch text-body bg-white border rounded-lg border-neutral-300 focus-ring"
              value={formData.geschlecht}
              onChange={(e) => setFormData({ ...formData, geschlecht: e.target.value })}
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
              className="w-full px-4 py-3 min-h-touch text-body bg-white border rounded-lg border-neutral-300 focus-ring"
              value={formData.verein_id || ''}
              onChange={(e) => setFormData({ ...formData, verein_id: e.target.value ? Number(e.target.value) : undefined })}
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
              className="w-full px-4 py-3 min-h-touch text-body bg-white border rounded-lg border-neutral-300 focus-ring"
              value={formData.verband_id || ''}
              onChange={(e) => setFormData({ ...formData, verband_id: e.target.value ? Number(e.target.value) : undefined })}
            >
              <option value="">Kein Verband</option>
              {verbaende?.map((verband) => (
                <option key={verband.id} value={verband.id}>
                  {verband.abkuerzung}
                </option>
              ))}
            </select>
          </div>

          <div className="flex gap-4 pt-4">
            <Button type="submit" size="lg">
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

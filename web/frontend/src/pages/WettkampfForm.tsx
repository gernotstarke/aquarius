import React, { useEffect, useState } from 'react';
import { useNavigate, useParams } from 'react-router-dom';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import apiClient from '../api/client';
import { Wettkampf, WettkampfCreate, Saison, Schwimmbad } from '../types';
import Card from '../components/Card';
import Input from '../components/Input';
import Button from '../components/Button';

const WettkampfForm: React.FC = () => {
  const { id } = useParams();
  const navigate = useNavigate();
  const queryClient = useQueryClient();
  const isEdit = Boolean(id);

  const [formData, setFormData] = useState<WettkampfCreate>({
    name: '',
    datum: '',
    max_teilnehmer: undefined,
    saison_id: 0,
    schwimmbad_id: 0,
  });

  const [maxTeilnehmerError, setMaxTeilnehmerError] = useState<string | null>(null);
  const [isWobbling, setIsWobbling] = useState(false);

  const { data: wettkampf } = useQuery<Wettkampf>({
    queryKey: ['wettkampf', id],
    queryFn: async () => {
      const response = await apiClient.get(`/wettkampf/${id}`);
      return response.data;
    },
    enabled: isEdit,
  });

  const { data: saisons } = useQuery<Saison[]>({
    queryKey: ['saisons'],
    queryFn: async () => {
      const response = await apiClient.get('/saison');
      return response.data;
    },
  });

  const { data: schwimmbäder } = useQuery<Schwimmbad[]>({
    queryKey: ['schwimmbäder'],
    queryFn: async () => {
      const response = await apiClient.get('/schwimmbad');
      return response.data;
    },
  });

  useEffect(() => {
    if (wettkampf) {
      setFormData({
        name: wettkampf.name,
        datum: wettkampf.datum,
        max_teilnehmer: wettkampf.max_teilnehmer,
        saison_id: wettkampf.saison_id,
        schwimmbad_id: wettkampf.schwimmbad_id,
      });
    }
  }, [wettkampf]);

  const createMutation = useMutation({
    mutationFn: (data: WettkampfCreate) => apiClient.post('/wettkampf', data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['wettkämpfe'] });
      navigate('/wettkampf');
    },
  });

  const updateMutation = useMutation({
    mutationFn: (data: WettkampfCreate) => apiClient.put(`/wettkampf/${id}`, data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['wettkämpfe'] });
      queryClient.invalidateQueries({ queryKey: ['wettkampf', id] });
      navigate('/wettkampf');
    },
  });

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();

    // Validation
    if (formData.max_teilnehmer !== undefined && formData.max_teilnehmer !== null && Number(formData.max_teilnehmer) <= 1) {
        setMaxTeilnehmerError('Max. Teilnehmer muss größer als 1 sein');
        setIsWobbling(true);
        setTimeout(() => setIsWobbling(false), 500);
        return;
    }
    setMaxTeilnehmerError(null);

    if (isEdit) {
      updateMutation.mutate(formData);
    } else {
      createMutation.mutate(formData);
    }
  };

  return (
    <div className="max-w-2xl space-y-8">
      <h2 className="text-h1 font-bold text-neutral-900">
        {isEdit ? 'Wettkampf bearbeiten' : 'Neuer Wettkampf'}
      </h2>

      <Card>
        <form onSubmit={handleSubmit} className="space-y-6">
          <Input
            label="Name"
            name="name"
            type="text"
            value={formData.name}
            onChange={(e) => setFormData({ ...formData, name: e.target.value })}
            required
            placeholder="z.B. Herbstcup 2024"
          />

          <Input
            label="Datum"
            name="datum"
            type="date"
            value={formData.datum}
            onChange={(e) => setFormData({ ...formData, datum: e.target.value })}
            required
          />

          <div className="space-y-2">
            <label className="block text-body font-medium text-neutral-700">
              Saison
            </label>
            <select
              name="saison_id"
              className="w-full px-4 py-3 min-h-touch text-body bg-white border rounded-lg border-neutral-300 focus-ring"
              value={formData.saison_id}
              onChange={(e) => setFormData({ ...formData, saison_id: Number(e.target.value) })}
              required
            >
              <option value={0}>Bitte wählen...</option>
              {saisons?.map((saison) => (
                <option key={saison.id} value={saison.id}>
                  {saison.name}
                </option>
              ))}
            </select>
          </div>

          <div className="space-y-2">
            <label className="block text-body font-medium text-neutral-700">
              Schwimmbad
            </label>
            <select
              name="schwimmbad_id"
              className="w-full px-4 py-3 min-h-touch text-body bg-white border rounded-lg border-neutral-300 focus-ring"
              value={formData.schwimmbad_id}
              onChange={(e) => setFormData({ ...formData, schwimmbad_id: Number(e.target.value) })}
              required
            >
              <option value={0}>Bitte wählen...</option>
              {schwimmbäder?.map((schwimmbad) => (
                <option key={schwimmbad.id} value={schwimmbad.id}>
                  {schwimmbad.name}
                </option>
              ))}
            </select>
          </div>

          <div className={isWobbling ? 'animate-wobble' : ''}>
            <Input
                id="max_teilnehmer"
                name="max_teilnehmer"
                label="Max. Teilnehmer (optional)"
                type="number"
                value={formData.max_teilnehmer || ''}
                onChange={(e) => {
                    setFormData({
                        ...formData,
                        max_teilnehmer: e.target.value ? Number(e.target.value) : undefined,
                    });
                    if (maxTeilnehmerError) setMaxTeilnehmerError(null);
                }}
                placeholder="z.B. 150"
                error={maxTeilnehmerError || undefined}
            />
          </div>

          <div className="flex gap-4 pt-4">
            <Button type="submit" size="lg">
              {isEdit ? 'Speichern' : 'Erstellen'}
            </Button>
            <Button
              type="button"
              variant="secondary"
              size="lg"
              onClick={() => navigate('/wettkampf')}
            >
              Abbrechen
            </Button>
          </div>
        </form>
      </Card>
    </div>
  );
};

export default WettkampfForm;

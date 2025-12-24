import React, { useEffect, useState } from 'react';
import { useNavigate, useParams } from 'react-router-dom';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import apiClient from '../api/client';
import { Figur, FigurCreate } from '../types';
import Card from '../components/Card';
import Input from '../components/Input';
import Button from '../components/Button';

const FigurenForm: React.FC = () => {
  const { id } = useParams();
  const navigate = useNavigate();
  const queryClient = useQueryClient();
  const isEdit = Boolean(id);

  const [formData, setFormData] = useState<FigurCreate>({
    name: '',
    beschreibung: '',
    schwierigkeitsgrad: 10,
    kategorie: '',
    min_alter: 8,
    bild: '',
  });

  const { data: figur } = useQuery<Figur>({
    queryKey: ['figur', id],
    queryFn: async () => {
      const response = await apiClient.get(`/figur/${id}`);
      return response.data;
    },
    enabled: isEdit,
  });

  useEffect(() => {
    if (figur) {
      setFormData({
        name: figur.name,
        beschreibung: figur.beschreibung || '',
        schwierigkeitsgrad: figur.schwierigkeitsgrad || 10,
        kategorie: figur.kategorie || '',
        min_alter: figur.min_alter || 8,
        bild: figur.bild || '',
      });
    }
  }, [figur]);

  const createMutation = useMutation({
    mutationFn: (data: FigurCreate) => apiClient.post('/figur', data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['figuren'] });
      navigate('/stammdaten/figuren');
    },
  });

  const updateMutation = useMutation({
    mutationFn: (data: FigurCreate) => apiClient.put(`/figur/${id}`, data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['figuren'] });
      queryClient.invalidateQueries({ queryKey: ['figur', id] });
      navigate('/stammdaten/figuren');
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

  const kategorien = [
    'Ballettbein',
    'Vertikale',
    'Flamingo',
    'Ritter',
    'Spagat',
    'Grundposition',
    'Kombination',
  ];

  return (
    <div className="max-w-2xl space-y-8">
      <h2 className="text-h1 font-bold text-neutral-900">
        {isEdit ? 'Figur bearbeiten' : 'Neue Figur'}
      </h2>

      <Card>
        <form onSubmit={handleSubmit} className="space-y-6">
          <Input
            label="Name"
            type="text"
            value={formData.name}
            onChange={(e) => setFormData({ ...formData, name: e.target.value })}
            required
            placeholder="z.B. Ballettbein"
          />

          <div className="space-y-2">
            <label className="block text-body font-medium text-neutral-700">
              Kategorie
            </label>
            <select
              className="w-full px-4 py-3 min-h-touch text-body bg-white border rounded-lg border-neutral-300 focus-ring"
              value={formData.kategorie}
              onChange={(e) => setFormData({ ...formData, kategorie: e.target.value })}
              required
            >
              <option value="">Bitte wählen...</option>
              {kategorien.map((kat) => (
                <option key={kat} value={kat}>
                  {kat}
                </option>
              ))}
            </select>
          </div>

          <div className="space-y-2">
            <label className="block text-body font-medium text-neutral-700">
              Beschreibung
            </label>
            <textarea
              className="w-full px-4 py-3 text-body bg-white border rounded-lg border-neutral-300 focus-ring"
              value={formData.beschreibung}
              onChange={(e) => setFormData({ ...formData, beschreibung: e.target.value })}
              rows={4}
              placeholder="Beschreibung der Figur..."
            />
          </div>

          <div className="grid grid-cols-2 gap-6">
            <div className="space-y-2">
              <label className="block text-body font-medium text-neutral-700">
                Schwierigkeitsgrad (1.0-2.0)
              </label>
              <input
                type="number"
                className="w-full px-4 py-3 min-h-touch text-body bg-white border rounded-lg border-neutral-300 focus-ring"
                value={(formData.schwierigkeitsgrad || 10) / 10}
                onChange={(e) =>
                  setFormData({
                    ...formData,
                    schwierigkeitsgrad: Math.round(parseFloat(e.target.value) * 10),
                  })
                }
                step="0.1"
                min="1.0"
                max="2.0"
                required
              />
            </div>

            <Input
              label="Mindestalter"
              type="number"
              value={formData.min_alter || ''}
              onChange={(e) =>
                setFormData({
                  ...formData,
                  min_alter: e.target.value ? parseInt(e.target.value) : undefined,
                })
              }
              placeholder="z.B. 8"
              min="6"
              max="18"
            />
          </div>

          <Input
            label="Bild-URL (optional)"
            type="text"
            value={formData.bild}
            onChange={(e) => setFormData({ ...formData, bild: e.target.value })}
            placeholder="z.B. /images/ballettbein.jpg"
          />

          <div className="flex gap-4 pt-4">
            <Button type="submit" size="lg">
              {isEdit ? 'Speichern' : 'Erstellen'}
            </Button>
            <Button
              type="button"
              variant="secondary"
              size="lg"
              onClick={() => navigate('/stammdaten/figuren')}
            >
              Abbrechen
            </Button>
          </div>
        </form>
      </Card>
    </div>
  );
};

export default FigurenForm;

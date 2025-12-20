import React, { useEffect, useState } from 'react';
import { useNavigate, useParams } from 'react-router-dom';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import apiClient from '../api/client';
import { Saison, SaisonCreate } from '../types';
import Card from '../components/Card';
import Input from '../components/Input';
import Button from '../components/Button';

const SaisonForm: React.FC = () => {
  const { id } = useParams();
  const navigate = useNavigate();
  const queryClient = useQueryClient();
  const isEdit = Boolean(id);

  const [formData, setFormData] = useState<SaisonCreate>({
    name: '',
    from_date: '',
    to_date: '',
  });

  const { data: saison } = useQuery<Saison>({
    queryKey: ['saison', id],
    queryFn: async () => {
      const response = await apiClient.get(`/saison/${id}`);
      return response.data;
    },
    enabled: isEdit,
  });

  useEffect(() => {
    if (saison) {
      setFormData({
        name: saison.name,
        from_date: saison.from_date,
        to_date: saison.to_date,
      });
    }
  }, [saison]);

  const createMutation = useMutation({
    mutationFn: (data: SaisonCreate) => apiClient.post('/saison', data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['saisons'] });
      navigate('/saison');
    },
  });

  const updateMutation = useMutation({
    mutationFn: (data: SaisonCreate) => apiClient.put(`/saison/${id}`, data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['saisons'] });
      queryClient.invalidateQueries({ queryKey: ['saison', id] });
      navigate('/saison');
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
        {isEdit ? 'Saison bearbeiten' : 'Neue Saison'}
      </h2>

      <Card>
        <form onSubmit={handleSubmit} className="space-y-6">
          <Input
            label="Name"
            type="text"
            value={formData.name}
            onChange={(e) => setFormData({ ...formData, name: e.target.value })}
            required
            placeholder="z.B. Saison 2024/2025"
          />

          <Input
            label="Startdatum"
            type="date"
            value={formData.from_date}
            onChange={(e) => setFormData({ ...formData, from_date: e.target.value })}
            required
          />

          <Input
            label="Enddatum"
            type="date"
            value={formData.to_date}
            onChange={(e) => setFormData({ ...formData, to_date: e.target.value })}
            required
          />

          <div className="flex gap-4 pt-4">
            <Button type="submit" size="lg">
              {isEdit ? 'Speichern' : 'Erstellen'}
            </Button>
            <Button
              type="button"
              variant="secondary"
              size="lg"
              onClick={() => navigate('/saison')}
            >
              Abbrechen
            </Button>
          </div>
        </form>
      </Card>
    </div>
  );
};

export default SaisonForm;

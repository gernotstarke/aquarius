import React, { useEffect, useState } from 'react';
import { useNavigate, useParams } from 'react-router-dom';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import apiClient from '../api/client';
import { Verein, VereinCreate } from '../types';
import Card from '../components/Card';
import Input from '../components/Input';
import Button from '../components/Button';
import { useAuth } from '../context/AuthContext';

const VereinForm: React.FC = () => {
  const { id } = useParams();
  const navigate = useNavigate();
  const queryClient = useQueryClient();
  const isEdit = Boolean(id);
  const { canWrite } = useAuth();

  const [formData, setFormData] = useState<VereinCreate>({
    name: '',
    ort: '',
    register_id: '',
    contact: '',
  });

  const { data: verein } = useQuery<Verein>({
    queryKey: ['verein', id],
    queryFn: async () => {
      const response = await apiClient.get(`/verein/${id}`);
      return response.data;
    },
    enabled: isEdit,
  });

  useEffect(() => {
    if (verein) {
      setFormData({
        name: verein.name,
        ort: verein.ort,
        register_id: verein.register_id,
        contact: verein.contact,
      });
    }
  }, [verein]);

  // Redirect read-only users who try to create new entries
  useEffect(() => {
    if (!isEdit && !canWrite) {
      navigate('/grunddaten/vereine');
    }
  }, [isEdit, canWrite, navigate]);

  const createMutation = useMutation({
    mutationFn: (data: VereinCreate) => apiClient.post('/verein', data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['vereine'] });
      navigate('/grunddaten/vereine');
    },
  });

  const updateMutation = useMutation({
    mutationFn: (data: VereinCreate) => apiClient.put(`/verein/${id}`, data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['vereine'] });
      queryClient.invalidateQueries({ queryKey: ['verein', id] });
      navigate('/grunddaten/vereine');
    },
  });

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();

    // Check permissions before submitting
    if (!canWrite) {
      return;
    }

    if (isEdit) {
      updateMutation.mutate(formData);
    } else {
      createMutation.mutate(formData);
    }
  };

  return (
    <div className="max-w-2xl space-y-8">
      <h2 className="text-h1 font-bold text-neutral-900">
        {isEdit ? 'Verein bearbeiten' : 'Neuer Verein'}
      </h2>

      <Card>
        <form onSubmit={handleSubmit} className="space-y-6">
          <Input
            label="Name"
            type="text"
            value={formData.name}
            onChange={(e) => setFormData({ ...formData, name: e.target.value })}
            required
            placeholder="z.B. Schwimmverein Berlin"
          />

          <Input
            label="Ort"
            type="text"
            value={formData.ort}
            onChange={(e) => setFormData({ ...formData, ort: e.target.value })}
            required
            placeholder="z.B. Berlin"
          />

          <Input
            label="Register-ID"
            type="text"
            value={formData.register_id}
            onChange={(e) => setFormData({ ...formData, register_id: e.target.value })}
            required
            placeholder="z.B. VR 12345"
          />

          <Input
            label="Kontakt"
            type="text"
            value={formData.contact}
            onChange={(e) => setFormData({ ...formData, contact: e.target.value })}
            required
            placeholder="z.B. info@verein.de oder +49 30 12345678"
          />

          <div className="flex gap-4 pt-4">
            {canWrite && (
              <Button type="submit" size="lg">
                {isEdit ? 'Speichern' : 'Erstellen'}
              </Button>
            )}
            <Button
              type="button"
              variant="secondary"
              size="lg"
              onClick={() => navigate('/grunddaten/vereine')}
            >
              Abbrechen
            </Button>
          </div>
        </form>
      </Card>
    </div>
  );
};

export default VereinForm;

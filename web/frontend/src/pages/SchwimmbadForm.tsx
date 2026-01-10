import React, { useEffect, useState } from 'react';
import { useNavigate, useParams } from 'react-router-dom';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import apiClient from '../api/client';
import { Schwimmbad, SchwimmbadCreate } from '../types';
import Card from '../components/Card';
import Input from '../components/Input';
import Button from '../components/Button';
import { useAuth } from '../context/AuthContext';

const SchwimmbadForm: React.FC = () => {
  const { id } = useParams();
  const navigate = useNavigate();
  const queryClient = useQueryClient();
  const isEdit = Boolean(id);
  const { canWrite } = useAuth();

  const [formData, setFormData] = useState<SchwimmbadCreate>({
    name: '',
    adresse: '',
    phone_no: '',
    manager: '',
  });

  const { data: schwimmbad } = useQuery<Schwimmbad>({
    queryKey: ['schwimmbad', id],
    queryFn: async () => {
      const response = await apiClient.get(`/schwimmbad/${id}`);
      return response.data;
    },
    enabled: isEdit,
  });

  useEffect(() => {
    if (schwimmbad) {
      setFormData({
        name: schwimmbad.name,
        adresse: schwimmbad.adresse,
        phone_no: schwimmbad.phone_no || '',
        manager: schwimmbad.manager || '',
      });
    }
  }, [schwimmbad]);

  // Redirect read-only users who try to create new entries
  useEffect(() => {
    if (!isEdit && !canWrite) {
      navigate('/schwimmbad');
    }
  }, [isEdit, canWrite, navigate]);

  const createMutation = useMutation({
    mutationFn: (data: SchwimmbadCreate) => apiClient.post('/schwimmbad', data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['schwimmbäder'] });
      navigate('/schwimmbad');
    },
  });

  const updateMutation = useMutation({
    mutationFn: (data: SchwimmbadCreate) => apiClient.put(`/schwimmbad/${id}`, data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['schwimmbäder'] });
      queryClient.invalidateQueries({ queryKey: ['schwimmbad', id] });
      navigate('/schwimmbad');
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
        {isEdit ? 'Schwimmbad bearbeiten' : 'Neues Schwimmbad'}
      </h2>

      <Card>
        <form onSubmit={handleSubmit} className="space-y-6">
          <Input
            label="Name"
            type="text"
            value={formData.name}
            onChange={(e) => setFormData({ ...formData, name: e.target.value })}
            required
            placeholder="z.B. Stadtbad Mitte"
          />

          <Input
            label="Adresse"
            type="text"
            value={formData.adresse}
            onChange={(e) => setFormData({ ...formData, adresse: e.target.value })}
            required
            placeholder="Straße, PLZ Ort"
          />

          <Input
            label="Telefon (optional)"
            type="tel"
            value={formData.phone_no}
            onChange={(e) => setFormData({ ...formData, phone_no: e.target.value })}
            placeholder="z.B. 030 12345678"
          />

          <Input
            label="Leitung (optional)"
            type="text"
            value={formData.manager}
            onChange={(e) => setFormData({ ...formData, manager: e.target.value })}
            placeholder="Name der Badleitung"
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
              onClick={() => navigate('/schwimmbad')}
            >
              Abbrechen
            </Button>
          </div>
        </form>
      </Card>
    </div>
  );
};

export default SchwimmbadForm;

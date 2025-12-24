import React from 'react';
import { useParams, Link, useNavigate } from 'react-router-dom';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import apiClient from '../api/client';
import { Figur } from '../types';
import Card from '../components/Card';
import Button from '../components/Button';

const FigurDetail: React.FC = () => {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();
  const queryClient = useQueryClient();

  const { data: figur, isLoading } = useQuery<Figur>({
    queryKey: ['figur', id],
    queryFn: async () => {
      const response = await apiClient.get(`/figur/${id}`);
      return response.data;
    },
  });

  const deleteMutation = useMutation({
    mutationFn: (id: number) => apiClient.delete(`/figur/${id}`),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['figuren'] });
      navigate('/stammdaten/figuren');
    },
  });

  if (isLoading) {
    return <div className="text-center py-12 text-body-lg">Lädt...</div>;
  }

  if (!figur) {
    return (
      <Card>
        <p className="text-center text-body-lg text-neutral-500 py-8">
          Figur nicht gefunden
        </p>
      </Card>
    );
  }

  const imageUrl = figur.bild
    ? `http://localhost:8000/static/${figur.bild}`
    : null;

  return (
    <div className="space-y-8 max-w-4xl">
      <div className="flex items-center justify-between">
        <h2 className="text-h1 font-bold text-neutral-900">{figur.name}</h2>
        <div className="flex gap-4">
          <Link to={`/stammdaten/figuren/${figur.id}`}>
            <Button variant="secondary">Bearbeiten</Button>
          </Link>
          <Button
            variant="danger"
            onClick={() => {
              if (confirm('Figur wirklich löschen?')) {
                deleteMutation.mutate(figur.id);
              }
            }}
          >
            Löschen
          </Button>
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
        {/* Left column: Image */}
        <Card>
          {imageUrl ? (
            <div className="space-y-4">
              <h3 className="text-h3 font-semibold text-neutral-900">Bild</h3>
              <img
                src={imageUrl}
                alt={figur.name}
                className="w-full h-auto rounded-lg border border-neutral-200"
                onError={(e) => {
                  e.currentTarget.style.display = 'none';
                  const parent = e.currentTarget.parentElement;
                  if (parent) {
                    const errorMsg = document.createElement('p');
                    errorMsg.className = 'text-body text-neutral-500 text-center py-8';
                    errorMsg.textContent = 'Bild nicht verfügbar';
                    parent.appendChild(errorMsg);
                  }
                }}
              />
            </div>
          ) : (
            <div className="text-center py-12">
              <p className="text-body text-neutral-500">Kein Bild vorhanden</p>
            </div>
          )}
        </Card>

        {/* Right column: Details */}
        <div className="space-y-6">
          <Card>
            <div className="space-y-4">
              <h3 className="text-h3 font-semibold text-neutral-900">Details</h3>

              <div className="space-y-3">
                {figur.kategorie && (
                  <div>
                    <span className="text-sm font-medium text-neutral-500">Kategorie</span>
                    <p className="text-body text-neutral-900">{figur.kategorie}</p>
                  </div>
                )}

                {figur.schwierigkeitsgrad && (
                  <div>
                    <span className="text-sm font-medium text-neutral-500">Schwierigkeitsgrad</span>
                    <p className="text-body text-neutral-900">
                      {(figur.schwierigkeitsgrad / 10).toFixed(1)}
                    </p>
                  </div>
                )}

                {figur.altersklasse && (
                  <div>
                    <span className="text-sm font-medium text-neutral-500">Altersklasse</span>
                    <p className="text-body text-neutral-900">{figur.altersklasse}</p>
                  </div>
                )}
              </div>
            </div>
          </Card>

          {figur.beschreibung && (
            <Card>
              <div className="space-y-4">
                <h3 className="text-h3 font-semibold text-neutral-900">Beschreibung</h3>
                <p className="text-body text-neutral-700 leading-relaxed">
                  {figur.beschreibung}
                </p>
              </div>
            </Card>
          )}
        </div>
      </div>

      <div>
        <Link to="/stammdaten/figuren">
          <Button variant="secondary">← Zurück zur Liste</Button>
        </Link>
      </div>
    </div>
  );
};

export default FigurDetail;

import React from 'react';
import { Link } from 'react-router-dom';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import apiClient from '../api/client';
import { Figur } from '../types';
import Card from '../components/Card';
import Button from '../components/Button';

const FigurenList: React.FC = () => {
  const queryClient = useQueryClient();

  const { data: figuren, isLoading } = useQuery<Figur[]>({
    queryKey: ['figuren'],
    queryFn: async () => {
      const response = await apiClient.get('/figur');
      return response.data;
    },
  });

  const deleteMutation = useMutation({
    mutationFn: (id: number) => apiClient.delete(`/figur/${id}`),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['figuren'] });
    },
  });

  if (isLoading) {
    return <div className="text-center py-12 text-body-lg">Lädt...</div>;
  }

  // Group figures by category
  const groupedFiguren = figuren?.reduce((acc, figur) => {
    const kategorie = figur.kategorie || 'Sonstige';
    if (!acc[kategorie]) acc[kategorie] = [];
    acc[kategorie].push(figur);
    return acc;
  }, {} as Record<string, Figur[]>);

  return (
    <div className="space-y-8">
      <div className="flex items-center justify-between">
        <h2 className="text-h1 font-bold text-neutral-900">Figuren</h2>
        <Link to="/stammdaten/figuren/new">
          <Button size="lg">Neue Figur</Button>
        </Link>
      </div>

      {groupedFiguren && Object.entries(groupedFiguren).map(([kategorie, figs]) => (
        <div key={kategorie}>
          <h3 className="text-h2 font-bold text-neutral-800 mb-4">{kategorie}</h3>
          <div className="grid gap-4">
            {figs.map((figur) => (
              <Card key={figur.id}>
                <div className="flex items-center justify-between">
                  <div className="space-y-2 flex-1">
                    <Link to={`/stammdaten/figuren/${figur.id}/detail`}>
                      <h4 className="text-h3 font-semibold text-neutral-900 hover:text-primary-600 cursor-pointer">
                        {figur.name}
                      </h4>
                    </Link>
                    <p className="text-body text-neutral-600">{figur.beschreibung}</p>
                    <div className="flex gap-4 text-sm text-neutral-500">
                      <span>Schwierigkeit: {(figur.schwierigkeitsgrad || 0) / 10}</span>
                      {figur.altersklasse && <span>{figur.altersklasse}</span>}
                    </div>
                  </div>
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
              </Card>
            ))}
          </div>
        </div>
      ))}

      {(!figuren || figuren.length === 0) && (
        <Card>
          <p className="text-center text-body-lg text-neutral-500 py-8">
            Keine Figuren vorhanden
          </p>
        </Card>
      )}
    </div>
  );
};

export default FigurenList;

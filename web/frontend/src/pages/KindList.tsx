import React, { useState } from 'react';
import { Link } from 'react-router-dom';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import apiClient from '../api/client';
import { Kind } from '../types';
import Card from '../components/Card';
import Button from '../components/Button';
import Input from '../components/Input';

const KindList: React.FC = () => {
  const queryClient = useQueryClient();

  // State for List controls
  const [page, setPage] = useState(1);
  const [pageSize] = useState(20);
  const [searchTerm, setSearchTerm] = useState('');
  const [sortBy, setSortBy] = useState('nachname');
  const [sortOrder, setSortOrder] = useState<'asc' | 'desc'>('asc');

  const { data, isLoading } = useQuery({
    queryKey: ['kinder', page, pageSize, searchTerm, sortBy, sortOrder],
    queryFn: async () => {
      const response = await apiClient.get<Kind[]>('/kind', {
        params: {
          skip: (page - 1) * pageSize,
          limit: pageSize,
          search: searchTerm || undefined,
          sort_by: sortBy,
          sort_order: sortOrder
        }
      });
      return {
        items: response.data,
        total: parseInt(response.headers['x-total-count'] || '0', 10)
      };
    },
    placeholderData: (previousData) => previousData,
  });

  const deleteMutation = useMutation({
    mutationFn: (id: number) => apiClient.delete(`/kind/${id}`),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['kinder'] });
    },
  });

  const handleSearchChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setSearchTerm(e.target.value);
    setPage(1); // Reset to page 1 on search
  };

  const handleSortChange = (e: React.ChangeEvent<HTMLSelectElement>) => {
    setSortBy(e.target.value);
    setPage(1);
  };

  const toggleSortOrder = () => {
    setSortOrder(current => current === 'asc' ? 'desc' : 'asc');
  };

  const totalItems = data?.total || 0;
  const totalPages = Math.ceil(totalItems / pageSize);
  const kinder = data?.items || [];

  const isKindInsured = (kind: Kind) => {
    const hasContractInsurance = Boolean(kind.versicherung_id && kind.vertrag);
    return Boolean(kind.verein_id || kind.verband_id || hasContractInsurance);
  };

  if (isLoading && !data) {
    return <div className="text-center py-12 text-body-lg">Lädt...</div>;
  }

  return (
    <div className="space-y-8">
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
        <h2 className="text-h1 font-bold text-neutral-900">Kinder</h2>
        <Link to="/kind/new">
          <Button size="lg">Neues Kind</Button>
        </Link>
      </div>

      {/* Controls: Search and Sort */}
      <div className="flex flex-col md:flex-row gap-4 bg-neutral-50 p-4 rounded-lg border border-neutral-200">
        <div className="flex-1">
          <Input
            placeholder="Suche nach Name oder Verein..."
            value={searchTerm}
            onChange={handleSearchChange}
            className="bg-white"
          />
        </div>
        <div className="flex gap-2 shrink-0">
          <select
            value={sortBy}
            onChange={handleSortChange}
            className="px-4 py-3 bg-white border border-neutral-300 rounded-lg text-body focus-ring min-h-touch cursor-pointer"
          >
            <option value="nachname">Nachname</option>
            <option value="vorname">Vorname</option>
            <option value="verein">Verein</option>
            <option value="unversichert">Unversichert</option>
          </select>
          <Button variant="secondary" onClick={toggleSortOrder}>
            {sortOrder === 'asc' ? 'Aufsteigend' : 'Absteigend'}
          </Button>
        </div>
      </div>

      <div className="grid gap-6">
        {kinder.map((kind) => (
          <Card key={kind.id}>
            <div className="relative flex items-center justify-between">
              <span
                className={`absolute top-4 right-4 h-3 w-3 rounded-full ${
                  isKindInsured(kind) ? 'bg-green-200' : 'bg-red-500'
                }`}
                title={isKindInsured(kind) ? 'Versichert' : 'Unversichert'}
              />
              <Link to={`/kind/${kind.id}`} className="block flex-1 group">
                <div className="space-y-2">
                  <h3 className="text-h3 font-semibold text-neutral-900 group-hover:text-primary-600 transition-colors">
                    {kind.vorname} {kind.nachname}
                  </h3>
                  <p className="text-body text-neutral-600">
                    Geboren: {kind.geburtsdatum}
                  </p>
                  {kind.verein && (
                    <p className="text-body text-neutral-500">Verein: {kind.verein.name} ({kind.verein.ort})</p>
                  )}
                  {kind.verband && (
                    <p className="text-body text-neutral-500">Verband: {kind.verband.abkuerzung}</p>
                  )}
                  {kind.versicherung && (
                    <p className="text-body text-neutral-500">
                      Versicherung: {kind.versicherung.kurz}
                      {kind.vertrag ? ` (Vertrag: ${kind.vertrag})` : ''}
                    </p>
                  )}
                </div>
              </Link>
              <div className="flex gap-4 ml-4">
                <Link to={`/kind/${kind.id}`}>
                  <Button variant="secondary">Bearbeiten</Button>
                </Link>
                <Button
                  variant="danger"
                  onClick={() => {
                    if (confirm('Kind wirklich löschen?')) {
                      deleteMutation.mutate(kind.id);
                    }
                  }}
                >
                  Löschen
                </Button>
              </div>
            </div>
          </Card>
        ))}

        {kinder.length === 0 && (
          <Card>
            <p className="text-center text-body-lg text-neutral-500 py-8">
              {searchTerm ? 'Keine Kinder gefunden, die der Suche entsprechen.' : 'Keine Kinder vorhanden.'}
            </p>
          </Card>
        )}
      </div>

      {/* Pagination */}
      {totalPages > 1 && (
        <div className="flex justify-center items-center gap-4 mt-8 pb-8">
          <Button
            variant="secondary"
            disabled={page === 1}
            onClick={() => setPage(p => Math.max(1, p - 1))}
          >
            Zurück
          </Button>
          <span className="text-body text-neutral-600">
            Seite {page} von {totalPages}
          </span>
          <Button
            variant="secondary"
            disabled={page >= totalPages}
            onClick={() => setPage(p => Math.min(totalPages, p + 1))}
          >
            Weiter
          </Button>
        </div>
      )}
    </div>
  );
};

export default KindList;

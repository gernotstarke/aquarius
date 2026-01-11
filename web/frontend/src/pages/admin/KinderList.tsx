import React, { useState } from 'react';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import adminApiClient from '../../api/adminClient';

interface Kind {
  id: number;
  vorname: string;
  nachname: string;
  email?: string;
  geburtsdatum: string;
  geschlecht?: string;
  verein_id?: number;
  verband_id?: number;
  versicherung_id?: number;
  vertrag?: string;
  verein?: {
    id: number;
    name: string;
  };
  verband?: {
    id: number;
    name: string;
  };
  versicherung?: {
    id: number;
    name: string;
  };
}

interface KinderResponse {
  items: Kind[];
  total: number;
}

const KinderList: React.FC = () => {
  const queryClient = useQueryClient();

  // State for list controls
  const [page, setPage] = useState(1);
  const [pageSize] = useState(20);
  const [searchTerm, setSearchTerm] = useState('');
  const [sortBy, setSortBy] = useState('nachname');
  const [sortOrder, setSortOrder] = useState<'asc' | 'desc'>('asc');

  // Modal states
  const [showCreateModal, setShowCreateModal] = useState(false);
  const [showEditModal, setShowEditModal] = useState(false);
  const [editingKind, setEditingKind] = useState<Kind | null>(null);

  // Form state
  const [formData, setFormData] = useState({
    vorname: '',
    nachname: '',
    email: '',
    password: '',
    geburtsdatum: '',
    geschlecht: '',
    verein_id: null as number | null,
    verband_id: null as number | null,
    versicherung_id: null as number | null,
    vertrag: ''
  });

  // Fetch Kinder
  const { data, isLoading } = useQuery<KinderResponse>({
    queryKey: ['admin-kinder', page, pageSize, searchTerm, sortBy, sortOrder],
    queryFn: async () => {
      const params = new URLSearchParams({
        skip: String((page - 1) * pageSize),
        limit: String(pageSize),
        sort_by: sortBy,
        sort_order: sortOrder
      });
      if (searchTerm) {
        params.append('search', searchTerm);
      }
      const response = await adminApiClient.get(`/kind?${params.toString()}`);
      return response.data;
    },
  });

  // Create Kind mutation
  const createMutation = useMutation({
    mutationFn: async (data: typeof formData) => {
      const response = await adminApiClient.post('/kind', data);
      return response.data;
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['admin-kinder'] });
      setShowCreateModal(false);
      setFormData({
        vorname: '',
        nachname: '',
        email: '',
        password: '',
        geburtsdatum: '',
        geschlecht: '',
        verein_id: null,
        verband_id: null,
        versicherung_id: null,
        vertrag: ''
      });
    },
  });

  // Update Kind mutation
  const updateMutation = useMutation({
    mutationFn: async ({ id, data }: { id: number; data: Partial<typeof formData> }) => {
      const response = await adminApiClient.put(`/kind/${id}`, data);
      return response.data;
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['admin-kinder'] });
      setShowEditModal(false);
      setEditingKind(null);
      setFormData({
        vorname: '',
        nachname: '',
        email: '',
        password: '',
        geburtsdatum: '',
        geschlecht: '',
        verein_id: null,
        verband_id: null,
        versicherung_id: null,
        vertrag: ''
      });
    },
  });

  // Delete Kind mutation
  const deleteMutation = useMutation({
    mutationFn: async (id: number) => {
      await adminApiClient.delete(`/kind/${id}`);
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['admin-kinder'] });
    },
  });

  const handleSearchChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setSearchTerm(e.target.value);
    setPage(1);
  };

  const handleSortChange = (e: React.ChangeEvent<HTMLSelectElement>) => {
    setSortBy(e.target.value);
    setPage(1);
  };

  const toggleSortOrder = () => {
    setSortOrder(current => current === 'asc' ? 'desc' : 'asc');
  };

  const handleCreate = () => {
    createMutation.mutate(formData);
  };

  const handleEdit = (kind: Kind) => {
    setEditingKind(kind);
    setFormData({
      vorname: kind.vorname,
      nachname: kind.nachname,
      email: kind.email || '',
      password: '',  // Don't pre-fill password
      geburtsdatum: kind.geburtsdatum,
      geschlecht: kind.geschlecht || '',
      verein_id: kind.verein_id || null,
      verband_id: kind.verband_id || null,
      versicherung_id: kind.versicherung_id || null,
      vertrag: kind.vertrag || ''
    });
    setShowEditModal(true);
  };

  const handleUpdate = () => {
    if (editingKind) {
      // Only send changed fields
      const updateData: Partial<typeof formData> = {};
      if (formData.vorname !== editingKind.vorname) updateData.vorname = formData.vorname;
      if (formData.nachname !== editingKind.nachname) updateData.nachname = formData.nachname;
      if (formData.email !== (editingKind.email || '')) updateData.email = formData.email;
      if (formData.password) updateData.password = formData.password;  // Only if password provided
      if (formData.geburtsdatum !== editingKind.geburtsdatum) updateData.geburtsdatum = formData.geburtsdatum;
      if (formData.geschlecht !== (editingKind.geschlecht || '')) updateData.geschlecht = formData.geschlecht;
      if (formData.verein_id !== editingKind.verein_id) updateData.verein_id = formData.verein_id;
      if (formData.verband_id !== editingKind.verband_id) updateData.verband_id = formData.verband_id;
      if (formData.versicherung_id !== editingKind.versicherung_id) updateData.versicherung_id = formData.versicherung_id;
      if (formData.vertrag !== (editingKind.vertrag || '')) updateData.vertrag = formData.vertrag;

      updateMutation.mutate({ id: editingKind.id, data: updateData });
    }
  };

  const handleDelete = (id: number, name: string) => {
    if (window.confirm(`Kind "${name}" wirklich löschen?`)) {
      deleteMutation.mutate(id);
    }
  };

  const totalItems = data?.total || 0;
  const totalPages = Math.ceil(totalItems / pageSize);
  const kinder = data?.items || [];

  if (isLoading && !data) {
    return <div className="text-center py-12">Lädt...</div>;
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex justify-between items-center">
        <div>
          <h1 className="text-2xl font-bold text-gray-900">Kinder Management</h1>
          <p className="text-gray-600 mt-1">Verwaltung aller Teilnehmenden (Kinder)</p>
        </div>
        <button
          onClick={() => setShowCreateModal(true)}
          className="bg-red-600 hover:bg-red-700 text-white px-4 py-2 rounded transition-colors"
        >
          Neues Kind
        </button>
      </div>

      {/* Search and Sort Controls */}
      <div className="flex gap-4 bg-white p-4 rounded-lg shadow">
        <div className="flex-1">
          <input
            type="text"
            placeholder="Suche nach Name oder Verein..."
            value={searchTerm}
            onChange={handleSearchChange}
            className="w-full px-4 py-2 border border-gray-300 rounded focus:outline-none focus:border-red-500"
          />
        </div>
        <select
          value={sortBy}
          onChange={handleSortChange}
          className="px-4 py-2 border border-gray-300 rounded focus:outline-none focus:border-red-500 bg-white"
        >
          <option value="nachname">Nachname</option>
          <option value="vorname">Vorname</option>
          <option value="verein">Verein</option>
        </select>
        <button
          onClick={toggleSortOrder}
          className="px-4 py-2 border border-gray-300 rounded hover:bg-gray-50"
        >
          {sortOrder === 'asc' ? '↑ Aufsteigend' : '↓ Absteigend'}
        </button>
      </div>

      {/* Kinder Table */}
      <div className="bg-white shadow rounded-lg overflow-hidden">
        <table className="min-w-full divide-y divide-gray-200">
          <thead className="bg-gray-50">
            <tr>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                Name
              </th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                Email
              </th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                Geburtsdatum
              </th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                Verein
              </th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                Aktionen
              </th>
            </tr>
          </thead>
          <tbody className="bg-white divide-y divide-gray-200">
            {kinder.map((kind) => (
              <tr key={kind.id} className="hover:bg-gray-50">
                <td className="px-6 py-4 whitespace-nowrap">
                  <div className="text-sm font-medium text-gray-900">
                    {kind.vorname} {kind.nachname}
                  </div>
                  {kind.geschlecht && (
                    <div className="text-sm text-gray-500">{kind.geschlecht}</div>
                  )}
                </td>
                <td className="px-6 py-4 whitespace-nowrap">
                  <div className="text-sm text-gray-900">{kind.email || '-'}</div>
                </td>
                <td className="px-6 py-4 whitespace-nowrap">
                  <div className="text-sm text-gray-900">{kind.geburtsdatum}</div>
                </td>
                <td className="px-6 py-4 whitespace-nowrap">
                  <div className="text-sm text-gray-900">{kind.verein?.name || '-'}</div>
                </td>
                <td className="px-6 py-4 whitespace-nowrap text-sm font-medium space-x-2">
                  <button
                    onClick={() => handleEdit(kind)}
                    className="text-blue-600 hover:text-blue-900"
                  >
                    Bearbeiten
                  </button>
                  <button
                    onClick={() => handleDelete(kind.id, `${kind.vorname} ${kind.nachname}`)}
                    className="text-red-600 hover:text-red-900"
                  >
                    Löschen
                  </button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      {/* Pagination */}
      {totalPages > 1 && (
        <div className="flex justify-center items-center space-x-2">
          <button
            onClick={() => setPage(p => Math.max(1, p - 1))}
            disabled={page === 1}
            className="px-4 py-2 border border-gray-300 rounded disabled:opacity-50 disabled:cursor-not-allowed hover:bg-gray-50"
          >
            Zurück
          </button>
          <span className="text-sm text-gray-700">
            Seite {page} von {totalPages} ({totalItems} Kinder)
          </span>
          <button
            onClick={() => setPage(p => Math.min(totalPages, p + 1))}
            disabled={page === totalPages}
            className="px-4 py-2 border border-gray-300 rounded disabled:opacity-50 disabled:cursor-not-allowed hover:bg-gray-50"
          >
            Weiter
          </button>
        </div>
      )}

      {/* Create Kind Modal */}
      {showCreateModal && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4 z-50">
          <div className="bg-white rounded-lg shadow-xl max-w-md w-full max-h-[90vh] overflow-y-auto">
            <div className="p-6">
              <h2 className="text-xl font-bold mb-4">Neues Kind erstellen</h2>

              <div className="space-y-4">
                <div>
                  <label className="block text-gray-700 text-sm font-bold mb-2">Vorname *</label>
                  <input
                    type="text"
                    className="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:border-red-500"
                    value={formData.vorname}
                    onChange={e => setFormData({...formData, vorname: e.target.value})}
                    required
                  />
                </div>

                <div>
                  <label className="block text-gray-700 text-sm font-bold mb-2">Nachname *</label>
                  <input
                    type="text"
                    className="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:border-red-500"
                    value={formData.nachname}
                    onChange={e => setFormData({...formData, nachname: e.target.value})}
                    required
                  />
                </div>

                <div>
                  <label className="block text-gray-700 text-sm font-bold mb-2">Email</label>
                  <input
                    type="email"
                    className="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:border-red-500"
                    value={formData.email}
                    onChange={e => setFormData({...formData, email: e.target.value})}
                  />
                </div>

                <div>
                  <label className="block text-gray-700 text-sm font-bold mb-2">Passwort</label>
                  <input
                    type="password"
                    className="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:border-red-500"
                    value={formData.password}
                    onChange={e => setFormData({...formData, password: e.target.value})}
                    placeholder="Optional für Self-Registration"
                  />
                </div>

                <div>
                  <label className="block text-gray-700 text-sm font-bold mb-2">Geburtsdatum *</label>
                  <input
                    type="date"
                    className="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:border-red-500"
                    value={formData.geburtsdatum}
                    onChange={e => setFormData({...formData, geburtsdatum: e.target.value})}
                    required
                  />
                </div>

                <div>
                  <label className="block text-gray-700 text-sm font-bold mb-2">Geschlecht</label>
                  <select
                    className="shadow border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:border-red-500 bg-white"
                    value={formData.geschlecht}
                    onChange={e => setFormData({...formData, geschlecht: e.target.value})}
                  >
                    <option value="">Bitte wählen</option>
                    <option value="m">Männlich</option>
                    <option value="w">Weiblich</option>
                    <option value="d">Divers</option>
                  </select>
                </div>
              </div>

              <div className="flex gap-3 mt-6">
                <button
                  onClick={handleCreate}
                  disabled={!formData.vorname || !formData.nachname || !formData.geburtsdatum || createMutation.isPending}
                  className="flex-1 bg-red-600 hover:bg-red-700 text-white px-4 py-2 rounded disabled:opacity-50 disabled:cursor-not-allowed"
                >
                  {createMutation.isPending ? 'Erstelle...' : 'Erstellen'}
                </button>
                <button
                  onClick={() => {
                    setShowCreateModal(false);
                    setFormData({
                      vorname: '',
                      nachname: '',
                      email: '',
                      password: '',
                      geburtsdatum: '',
                      geschlecht: '',
                      verein_id: null,
                      verband_id: null,
                      versicherung_id: null,
                      vertrag: ''
                    });
                  }}
                  className="flex-1 bg-gray-300 hover:bg-gray-400 text-gray-800 px-4 py-2 rounded"
                >
                  Abbrechen
                </button>
              </div>
            </div>
          </div>
        </div>
      )}

      {/* Edit Kind Modal */}
      {showEditModal && editingKind && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4 z-50">
          <div className="bg-white rounded-lg shadow-xl max-w-md w-full max-h-[90vh] overflow-y-auto">
            <div className="p-6">
              <h2 className="text-xl font-bold mb-4">Kind bearbeiten</h2>

              <div className="space-y-4">
                <div>
                  <label className="block text-gray-700 text-sm font-bold mb-2">Vorname *</label>
                  <input
                    type="text"
                    className="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:border-red-500"
                    value={formData.vorname}
                    onChange={e => setFormData({...formData, vorname: e.target.value})}
                    required
                  />
                </div>

                <div>
                  <label className="block text-gray-700 text-sm font-bold mb-2">Nachname *</label>
                  <input
                    type="text"
                    className="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:border-red-500"
                    value={formData.nachname}
                    onChange={e => setFormData({...formData, nachname: e.target.value})}
                    required
                  />
                </div>

                <div>
                  <label className="block text-gray-700 text-sm font-bold mb-2">Email</label>
                  <input
                    type="email"
                    className="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:border-red-500"
                    value={formData.email}
                    onChange={e => setFormData({...formData, email: e.target.value})}
                  />
                </div>

                <div>
                  <label className="block text-gray-700 text-sm font-bold mb-2">Neues Passwort</label>
                  <input
                    type="password"
                    className="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:border-red-500"
                    value={formData.password}
                    onChange={e => setFormData({...formData, password: e.target.value})}
                    placeholder="Leer lassen um Passwort nicht zu ändern"
                  />
                </div>

                <div>
                  <label className="block text-gray-700 text-sm font-bold mb-2">Geburtsdatum *</label>
                  <input
                    type="date"
                    className="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:border-red-500"
                    value={formData.geburtsdatum}
                    onChange={e => setFormData({...formData, geburtsdatum: e.target.value})}
                    required
                  />
                </div>

                <div>
                  <label className="block text-gray-700 text-sm font-bold mb-2">Geschlecht</label>
                  <select
                    className="shadow border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:border-red-500 bg-white"
                    value={formData.geschlecht}
                    onChange={e => setFormData({...formData, geschlecht: e.target.value})}
                  >
                    <option value="">Bitte wählen</option>
                    <option value="m">Männlich</option>
                    <option value="w">Weiblich</option>
                    <option value="d">Divers</option>
                  </select>
                </div>
              </div>

              <div className="flex gap-3 mt-6">
                <button
                  onClick={handleUpdate}
                  disabled={!formData.vorname || !formData.nachname || !formData.geburtsdatum || updateMutation.isPending}
                  className="flex-1 bg-red-600 hover:bg-red-700 text-white px-4 py-2 rounded disabled:opacity-50 disabled:cursor-not-allowed"
                >
                  {updateMutation.isPending ? 'Speichert...' : 'Speichern'}
                </button>
                <button
                  onClick={() => {
                    setShowEditModal(false);
                    setEditingKind(null);
                    setFormData({
                      vorname: '',
                      nachname: '',
                      email: '',
                      password: '',
                      geburtsdatum: '',
                      geschlecht: '',
                      verein_id: null,
                      verband_id: null,
                      versicherung_id: null,
                      vertrag: ''
                    });
                  }}
                  className="flex-1 bg-gray-300 hover:bg-gray-400 text-gray-800 px-4 py-2 rounded"
                >
                  Abbrechen
                </button>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default KinderList;

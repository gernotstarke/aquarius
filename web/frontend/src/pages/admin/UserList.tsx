import React, { useState } from 'react';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import adminApiClient from '../../api/adminClient';
import { UserPlus, Trash2, User as UserIcon, Edit2, Shield } from 'lucide-react';

interface User {
  id: number;
  username: string;
  email?: string;
  full_name: string;
  role: 'ADMIN' | 'CLEO' | 'VERWALTUNG' | 'OFFIZIELLE' | 'TEILNEHMENDE';
  is_active: boolean;
  is_app_user?: boolean;
  can_read_all?: boolean;
  can_write_all?: boolean;
  totp_enabled: boolean;
  created_at: string;
}

const ROLE_LABELS: Record<string, string> = {
  'ADMIN': 'Admin',
  'CLEO': 'Liga-Präsident',
  'VERWALTUNG': 'Verwaltung',
  'OFFIZIELLE': 'Offizielle',
  'TEILNEHMENDE': 'Teilnehmende'
};

const UserList: React.FC = () => {
  const queryClient = useQueryClient();
  const [isCreateModalOpen, setIsCreateModalOpen] = useState(false);
  const [isEditModalOpen, setIsEditModalOpen] = useState(false);
  const [editingUser, setEditingUser] = useState<User | null>(null);

  // Form State
  const [formData, setFormData] = useState({
    username: '',
    email: '',
    password: '',
    full_name: '',
    role: 'OFFIZIELLE',
    is_active: true,
    is_app_user: false,
    can_read_all: true,
    can_write_all: false
  });

  const { data: users, isLoading, error } = useQuery<User[]>({
    queryKey: ['users'],
    queryFn: async () => {
      const response = await adminApiClient.get('/users/');
      return response.data;
    }
  });

  const createMutation = useMutation({
    mutationFn: async (newUser: any) => {
      await adminApiClient.post('/users/', newUser);
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['users'] });
      setIsCreateModalOpen(false);
      setFormData({ username: '', email: '', password: '', full_name: '', role: 'OFFIZIELLE', is_active: true, is_app_user: false, can_read_all: true, can_write_all: false });
    }
  });

  const updateMutation = useMutation({
    mutationFn: async ({ id, data }: { id: number; data: any }) => {
      await adminApiClient.put(`/users/${id}`, data);
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['users'] });
      setIsEditModalOpen(false);
      setEditingUser(null);
      setFormData({ username: '', email: '', password: '', full_name: '', role: 'OFFIZIELLE', is_active: true, is_app_user: false, can_read_all: true, can_write_all: false });
    }
  });

  const deleteMutation = useMutation({
    mutationFn: async (userId: number) => {
      await adminApiClient.delete(`/users/${userId}`);
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['users'] });
    }
  });

  const handleCreateSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    createMutation.mutate(formData);
  };

  const handleEditSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (!editingUser) return;

    const updateData: any = {
      email: formData.email,
      full_name: formData.full_name,
      role: formData.role,
      is_active: formData.is_active,
      is_app_user: formData.is_app_user,
      can_read_all: formData.can_read_all,
      can_write_all: formData.can_write_all
    };

    // Only include password if it's been changed
    if (formData.password) {
      updateData.password = formData.password;
    }

    updateMutation.mutate({ id: editingUser.id, data: updateData });
  };

  const handleEdit = (user: User) => {
    setEditingUser(user);
    setFormData({
      username: user.username,
      email: user.email || '',
      password: '',
      full_name: user.full_name || '',
      role: user.role,
      is_active: user.is_active,
      is_app_user: user.is_app_user || false,
      can_read_all: user.can_read_all !== undefined ? user.can_read_all : true,
      can_write_all: user.can_write_all || false
    });
    setIsEditModalOpen(true);
  };

  if (isLoading) return <div className="text-center py-10">Loading users...</div>;
  if (error) return (
    <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded">
      Error loading users: {(error as any).message}
    </div>
  );

  return (
    <div>
      <div className="flex justify-between items-center mb-6">
        <h1 className="text-2xl font-bold text-gray-900">User Management</h1>
        <button 
          onClick={() => setIsCreateModalOpen(true)}
          className="bg-red-700 hover:bg-red-800 text-white px-4 py-2 rounded flex items-center space-x-2 transition-colors"
        >
          <UserPlus size={18} />
          <span>Create User</span>
        </button>
      </div>

      <div className="bg-white rounded-lg shadow overflow-hidden">
        <table className="min-w-full divide-y divide-gray-200">
          <thead className="bg-gray-50">
            <tr>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">User</th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Role</th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Status</th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">2FA</th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Created</th>
              <th className="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">Actions</th>
            </tr>
          </thead>
          <tbody className="bg-white divide-y divide-gray-200">
            {users?.map((user) => (
              <tr key={user.id} className="hover:bg-red-50 transition-colors">
                <td className="px-6 py-4 whitespace-nowrap">
                  <div className="flex items-center">
                    <div className="flex-shrink-0 h-10 w-10 bg-gray-200 rounded-full flex items-center justify-center text-gray-500">
                      <UserIcon size={20} />
                    </div>
                    <div className="ml-4">
                      <div className="text-sm font-medium text-gray-900">{user.username}</div>
                      <div className="text-sm text-gray-500">{user.full_name || '-'}</div>
                    </div>
                  </div>
                </td>
                <td className="px-6 py-4 whitespace-nowrap">
                  <span className={`px-2 inline-flex text-xs leading-5 font-semibold rounded-full
                    ${user.role === 'ADMIN' ? 'bg-red-100 text-red-800' :
                      user.role === 'CLEO' ? 'bg-purple-100 text-purple-800' :
                      user.role === 'VERWALTUNG' ? 'bg-blue-100 text-blue-800' :
                      user.role === 'OFFIZIELLE' ? 'bg-green-100 text-green-800' :
                      'bg-gray-100 text-gray-800'}`}>
                    {ROLE_LABELS[user.role]}
                  </span>
                </td>
                <td className="px-6 py-4 whitespace-nowrap">
                  <span className={`px-2 inline-flex text-xs leading-5 font-semibold rounded-full ${user.is_active ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800'}`}>
                    {user.is_active ? 'Active' : 'Inactive'}
                  </span>
                </td>
                <td className="px-6 py-4 whitespace-nowrap">
                  <div className="flex items-center space-x-2">
                    <div className={`h-2.5 w-2.5 rounded-full ${user.totp_enabled ? 'bg-green-500' : 'bg-red-500'}`}></div>
                    <span className={`flex items-center text-sm ${user.totp_enabled ? 'text-green-700' : 'text-red-700'}`}>
                      <Shield size={14} className="mr-1" />
                      {user.totp_enabled ? 'Enabled' : 'Disabled'}
                    </span>
                  </div>
                </td>
                <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                  {new Date(user.created_at).toLocaleDateString()}
                </td>
                <td className="px-6 py-4 whitespace-nowrap text-right text-sm font-medium">
                  <div className="flex justify-end space-x-3">
                    <button
                      onClick={() => handleEdit(user)}
                      className="text-blue-600 hover:text-blue-900"
                      title="Edit user"
                    >
                      <Edit2 size={18} />
                    </button>
                    {user.role !== 'ADMIN' && (
                      <button
                        onClick={() => {
                          if (confirm(`Are you sure you want to delete user ${user.username}?`)) {
                            deleteMutation.mutate(user.id);
                          }
                        }}
                        className="text-red-600 hover:text-red-900"
                        title="Delete user"
                      >
                        <Trash2 size={18} />
                      </button>
                    )}
                  </div>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      {/* Create User Modal */}
      {isCreateModalOpen && (
        <div className="fixed inset-0 bg-gray-600 bg-opacity-50 overflow-y-auto h-full w-full flex items-center justify-center p-4 z-50">
          <div className="bg-white rounded-lg shadow-xl p-8 w-full max-w-md border-t-4 border-red-600">
            <h2 className="text-xl font-bold mb-6">Create New User</h2>
            <form onSubmit={handleCreateSubmit}>
              <div className="mb-4">
                <label className="block text-gray-700 text-sm font-bold mb-2">Username</label>
                <input
                  type="text"
                  required
                  className="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:border-red-500"
                  value={formData.username}
                  onChange={e => setFormData({...formData, username: e.target.value})}
                />
              </div>
              <div className="mb-4">
                <label className="block text-gray-700 text-sm font-bold mb-2">Email</label>
                <input
                  type="email"
                  className="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:border-red-500"
                  value={formData.email}
                  onChange={e => setFormData({...formData, email: e.target.value})}
                />
              </div>
              <div className="mb-4">
                <label className="block text-gray-700 text-sm font-bold mb-2">Password</label>
                <input
                  type="password"
                  required
                  className="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:border-red-500"
                  value={formData.password}
                  onChange={e => setFormData({...formData, password: e.target.value})}
                />
              </div>
              <div className="mb-4">
                <label className="block text-gray-700 text-sm font-bold mb-2">Full Name</label>
                <input
                  type="text"
                  className="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:border-red-500"
                  value={formData.full_name}
                  onChange={e => setFormData({...formData, full_name: e.target.value})}
                />
              </div>
              <div className="mb-4">
                <label className="block text-gray-700 text-sm font-bold mb-2">Role</label>
                <select
                  className="shadow border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:border-red-500 bg-white"
                  value={formData.role}
                  onChange={e => setFormData({...formData, role: e.target.value})}
                >
                  <option value="OFFIZIELLE">Offizielle (Bewertung)</option>
                  <option value="VERWALTUNG">Verwaltung</option>
                  <option value="TEILNEHMENDE">Teilnehmende</option>
                  <option value="CLEO">CLEO (Liga-Präsident)</option>
                  <option value="ADMIN">Admin</option>
                </select>
              </div>
              <div className="mb-6">
                <label className="flex items-center">
                  <input
                    type="checkbox"
                    checked={formData.is_active}
                    onChange={e => setFormData({...formData, is_active: e.target.checked})}
                    className="mr-2"
                  />
                  <span className="text-sm text-gray-700">Active</span>
                </label>
              </div>

              {/* App Access Section */}
              <div className="mb-6 p-4 bg-blue-50 rounded border border-blue-200">
                <h3 className="font-bold text-sm text-blue-900 mb-3">App Access</h3>
                <label className="flex items-center mb-3">
                  <input
                    type="checkbox"
                    checked={formData.is_app_user}
                    onChange={e => setFormData({...formData, is_app_user: e.target.checked})}
                    className="mr-2"
                  />
                  <span className="text-sm text-gray-700">App User (can access Aquarius app)</span>
                </label>
                <label className="flex items-center mb-3">
                  <input
                    type="checkbox"
                    checked={formData.can_read_all}
                    onChange={e => setFormData({...formData, can_read_all: e.target.checked})}
                    disabled={!formData.is_app_user}
                    className="mr-2 disabled:opacity-50"
                  />
                  <span className="text-sm text-gray-700">Read Permission</span>
                </label>
                <label className="flex items-center">
                  <input
                    type="checkbox"
                    checked={formData.can_write_all}
                    onChange={e => setFormData({...formData, can_write_all: e.target.checked})}
                    disabled={!formData.is_app_user}
                    className="mr-2 disabled:opacity-50"
                  />
                  <span className="text-sm text-gray-700">Write Permission (edit/create/delete)</span>
                </label>
              </div>
              <div className="flex justify-end space-x-4">
                <button
                  type="button"
                  onClick={() => setIsCreateModalOpen(false)}
                  className="bg-gray-300 hover:bg-gray-400 text-gray-800 font-bold py-2 px-4 rounded transition-colors"
                >
                  Cancel
                </button>
                <button
                  type="submit"
                  className="bg-red-700 hover:bg-red-800 text-white font-bold py-2 px-4 rounded transition-colors"
                >
                  Create User
                </button>
              </div>
            </form>
          </div>
        </div>
      )}

      {/* Edit User Modal */}
      {isEditModalOpen && editingUser && (
        <div className="fixed inset-0 bg-gray-600 bg-opacity-50 overflow-y-auto h-full w-full flex items-center justify-center p-4 z-50">
          <div className="bg-white rounded-lg shadow-xl p-8 w-full max-w-md border-t-4 border-blue-600">
            <h2 className="text-xl font-bold mb-6">Edit User: {editingUser.username}</h2>
            <form onSubmit={handleEditSubmit}>
              <div className="mb-4">
                <label className="block text-gray-700 text-sm font-bold mb-2">Username</label>
                <input
                  type="text"
                  disabled
                  className="shadow appearance-none border rounded w-full py-2 px-3 text-gray-500 bg-gray-100 leading-tight"
                  value={formData.username}
                />
                <p className="text-xs text-gray-500 mt-1">Username cannot be changed</p>
              </div>
              <div className="mb-4">
                <label className="block text-gray-700 text-sm font-bold mb-2">Email</label>
                <input
                  type="email"
                  className="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:border-blue-500"
                  value={formData.email}
                  onChange={e => setFormData({...formData, email: e.target.value})}
                />
              </div>
              <div className="mb-4">
                <label className="block text-gray-700 text-sm font-bold mb-2">
                  Password
                  <span className="font-normal text-gray-500 ml-2">(leave empty to keep current)</span>
                </label>
                <input
                  type="password"
                  placeholder="Enter new password to change"
                  className="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:border-blue-500"
                  value={formData.password}
                  onChange={e => setFormData({...formData, password: e.target.value})}
                />
              </div>
              <div className="mb-4">
                <label className="block text-gray-700 text-sm font-bold mb-2">Full Name</label>
                <input
                  type="text"
                  className="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:border-blue-500"
                  value={formData.full_name}
                  onChange={e => setFormData({...formData, full_name: e.target.value})}
                />
              </div>
              <div className="mb-4">
                <label className="block text-gray-700 text-sm font-bold mb-2">Role</label>
                <select
                  className="shadow border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:border-blue-500 bg-white"
                  value={formData.role}
                  onChange={e => setFormData({...formData, role: e.target.value})}
                >
                  <option value="OFFIZIELLE">Offizielle (Bewertung)</option>
                  <option value="VERWALTUNG">Verwaltung</option>
                  <option value="TEILNEHMENDE">Teilnehmende</option>
                  <option value="CLEO">CLEO (Liga-Präsident)</option>
                  <option value="ADMIN">Admin</option>
                </select>
              </div>
              <div className="mb-6">
                <label className="flex items-center">
                  <input
                    type="checkbox"
                    checked={formData.is_active}
                    onChange={e => setFormData({...formData, is_active: e.target.checked})}
                    className="mr-2"
                  />
                  <span className="text-sm text-gray-700">Active</span>
                </label>
              </div>

              {/* App Access Section */}
              <div className="mb-6 p-4 bg-blue-50 rounded border border-blue-200">
                <h3 className="font-bold text-sm text-blue-900 mb-3">App Access</h3>
                <label className="flex items-center mb-3">
                  <input
                    type="checkbox"
                    checked={formData.is_app_user}
                    onChange={e => setFormData({...formData, is_app_user: e.target.checked})}
                    className="mr-2"
                  />
                  <span className="text-sm text-gray-700">App User (can access Aquarius app)</span>
                </label>
                <label className="flex items-center mb-3">
                  <input
                    type="checkbox"
                    checked={formData.can_read_all}
                    onChange={e => setFormData({...formData, can_read_all: e.target.checked})}
                    disabled={!formData.is_app_user}
                    className="mr-2 disabled:opacity-50"
                  />
                  <span className="text-sm text-gray-700">Read Permission</span>
                </label>
                <label className="flex items-center">
                  <input
                    type="checkbox"
                    checked={formData.can_write_all}
                    onChange={e => setFormData({...formData, can_write_all: e.target.checked})}
                    disabled={!formData.is_app_user}
                    className="mr-2 disabled:opacity-50"
                  />
                  <span className="text-sm text-gray-700">Write Permission (edit/create/delete)</span>
                </label>
              </div>
              <div className="flex justify-end space-x-4">
                <button
                  type="button"
                  onClick={() => {
                    setIsEditModalOpen(false);
                    setEditingUser(null);
                  }}
                  className="bg-gray-300 hover:bg-gray-400 text-gray-800 font-bold py-2 px-4 rounded transition-colors"
                >
                  Cancel
                </button>
                <button
                  type="submit"
                  className="bg-blue-700 hover:bg-blue-800 text-white font-bold py-2 px-4 rounded transition-colors"
                >
                  Update User
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
};

export default UserList;

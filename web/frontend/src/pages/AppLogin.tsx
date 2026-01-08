import React, { useState, useEffect } from 'react';
import { useNavigate, useLocation } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import Card from '../components/Card';
import Button from '../components/Button';
import Input from '../components/Input';

const AppLogin: React.FC = () => {
  const navigate = useNavigate();
  const location = useLocation();
  const { login, isAuthenticated, isLoading } = useAuth();

  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [isSubmitting, setIsSubmitting] = useState(false);

  // Redirect if already logged in
  useEffect(() => {
    if (isAuthenticated && !isLoading) {
      const from = (location.state as any)?.from?.pathname || '/';
      navigate(from);
    }
  }, [isAuthenticated, isLoading, navigate, location]);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');
    setIsSubmitting(true);

    try {
      await login(username, password);
      // Redirect after successful login
      const from = (location.state as any)?.from?.pathname || '/';
      navigate(from);
    } catch (err: any) {
      setError(err.message || 'Login fehlgeschlagen. Überprüfe Benutzernamen und Passwort.');
    } finally {
      setIsSubmitting(false);
    }
  };

  if (isLoading) {
    return (
      <div className="flex items-center justify-center h-screen">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto mb-4"></div>
          <p className="text-gray-600">Lädt...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 flex items-center justify-center py-12 px-4">
      <Card className="w-full max-w-md">
        <div className="text-center mb-8">
          <h1 className="text-3xl font-bold text-gray-800 mb-2">Aquarius</h1>
          <p className="text-gray-600">Wettkampf-Verwaltung</p>
        </div>

        <form onSubmit={handleSubmit} className="space-y-4">
          {error && (
            <div className="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded">
              {error}
            </div>
          )}

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Benutzername
            </label>
            <Input
              type="text"
              placeholder="Benutzername eingeben"
              value={username}
              onChange={(e) => setUsername(e.target.value)}
              disabled={isSubmitting}
              autoFocus
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Passwort
            </label>
            <Input
              type="password"
              placeholder="Passwort eingeben"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              disabled={isSubmitting}
            />
          </div>

          <Button
            type="submit"
            disabled={!username || !password || isSubmitting}
            className="w-full"
          >
            {isSubmitting ? 'Wird angemeldet...' : 'Anmelden'}
          </Button>
        </form>

        <div className="mt-8 pt-6 border-t border-gray-200">
          <p className="text-xs text-gray-500 text-center">
            Für Unterstützung wenden Sie sich an den Administrator.
          </p>
        </div>
      </Card>
    </div>
  );
};

export default AppLogin;

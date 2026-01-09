import React, { useState, useEffect } from 'react';
import { useNavigate, useLocation } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import Card from '../components/Card';
import Button from '../components/Button';
import Input from '../components/Input';

interface LoginAttempt {
  timestamp: number;
  count: number;
}

const AppLogin: React.FC = () => {
  const navigate = useNavigate();
  const location = useLocation();
  const { login, isAuthenticated, isLoading } = useAuth();

  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [lockoutTime, setLockoutTime] = useState(0);

  // Rate limiting constants
  const MAX_ATTEMPTS = 3;
  const LOCKOUT_DURATION_MS = 5 * 60 * 1000; // 5 minutes in milliseconds
  const STORAGE_KEY = 'app_login_attempts';

  // Redirect if already logged in
  useEffect(() => {
    if (isAuthenticated && !isLoading) {
      const from = (location.state as any)?.from?.pathname || '/';
      navigate(from);
    }
  }, [isAuthenticated, isLoading, navigate, location]);

  // Handle lockout timer
  useEffect(() => {
    if (lockoutTime <= 0) return;

    const interval = setInterval(() => {
      setLockoutTime(prev => {
        const newTime = prev - 1;
        if (newTime <= 0) {
          clearInterval(interval);
          // Clear attempts when lockout expires
          localStorage.removeItem(STORAGE_KEY);
          setError('');
        }
        return Math.max(0, newTime);
      });
    }, 1000);

    return () => clearInterval(interval);
  }, [lockoutTime]);

  // Check if user is locked out
  useEffect(() => {
    const stored = localStorage.getItem(STORAGE_KEY);
    if (stored) {
      const attempt: LoginAttempt = JSON.parse(stored);
      const now = Date.now();
      const elapsed = now - attempt.timestamp;

      if (elapsed < LOCKOUT_DURATION_MS && attempt.count >= MAX_ATTEMPTS) {
        const remainingMs = LOCKOUT_DURATION_MS - elapsed;
        setLockoutTime(Math.ceil(remainingMs / 1000));
      } else if (elapsed >= LOCKOUT_DURATION_MS) {
        // Lockout expired
        localStorage.removeItem(STORAGE_KEY);
      }
    }
  }, []);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');

    // Check if user is locked out
    if (lockoutTime > 0) {
      const minutes = Math.ceil(lockoutTime / 60);
      setError(
        `Zu viele fehlgeschlagene Anmeldeversuche. Bitte versuchen Sie es in ${minutes} Minute${
          minutes > 1 ? 'n' : ''
        } erneut.`
      );
      return;
    }

    setIsSubmitting(true);

    try {
      await login(username, password);
      // Clear attempts on successful login
      localStorage.removeItem(STORAGE_KEY);
      // Redirect after successful login
      const from = (location.state as any)?.from?.pathname || '/';
      navigate(from);
    } catch (err: any) {
      // Track failed attempt
      const stored = localStorage.getItem(STORAGE_KEY);
      let attempt: LoginAttempt = { timestamp: Date.now(), count: 1 };

      if (stored) {
        const parsed: LoginAttempt = JSON.parse(stored);
        const elapsed = Date.now() - parsed.timestamp;

        if (elapsed < LOCKOUT_DURATION_MS) {
          attempt.count = parsed.count + 1;
          attempt.timestamp = parsed.timestamp;
        }
      }

      localStorage.setItem(STORAGE_KEY, JSON.stringify(attempt));

      // Check if this was the final attempt before lockout
      if (attempt.count >= MAX_ATTEMPTS) {
        setLockoutTime(Math.ceil(LOCKOUT_DURATION_MS / 1000));
        setError(
          `Zu viele fehlgeschlagene Anmeldeversuche. Das Konto ist für 5 Minuten gesperrt.`
        );
      } else {
        const remainingAttempts = MAX_ATTEMPTS - attempt.count;
        setError(
          `Benutzername oder Kennwort falsch. ${remainingAttempts} Versuch${
            remainingAttempts > 1 ? 'e' : ''
          } verbleibend.`
        );
      }
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

  const isDisabled = lockoutTime > 0;

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 flex items-center justify-center py-12 px-4">
      <Card className="w-full max-w-md">
        <div className="text-center mb-8">
          <h1 className="text-3xl font-bold text-gray-800 mb-2">Aquarius</h1>
          <p className="text-gray-600">Wettkampf-Verwaltung</p>
        </div>

        <form onSubmit={handleSubmit} className="space-y-4">
          {error && (
            <div className={`px-4 py-3 rounded ${
              lockoutTime > 0
                ? 'bg-orange-50 border border-orange-200 text-orange-700'
                : 'bg-red-50 border border-red-200 text-red-700'
            }`}>
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
              disabled={isSubmitting || isDisabled}
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
              disabled={isSubmitting || isDisabled}
            />
          </div>

          <Button
            type="submit"
            disabled={!username || !password || isSubmitting || isDisabled}
            className="w-full"
          >
            {isSubmitting
              ? 'Wird angemeldet...'
              : isDisabled
              ? `Warten (${lockoutTime}s)`
              : 'Anmelden'}
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

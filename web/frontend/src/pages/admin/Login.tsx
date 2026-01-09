import React, { useState, useEffect } from 'react';
import { useNavigate, useLocation } from 'react-router-dom';
import adminApiClient from '../../api/adminClient';

const Login: React.FC = () => {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [totpCode, setTotpCode] = useState('');
  const [backupCode, setBackupCode] = useState('');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);
  const [step, setStep] = useState<'credentials' | 'totp' | 'backup'>('credentials');
  const navigate = useNavigate();
  const location = useLocation();

  useEffect(() => {
    const token = localStorage.getItem('admin_token');
    if (token) {
      // Verify token by calling /me
      adminApiClient.get('/auth/me')
        .then(() => {
          const from = (location.state as any)?.from?.pathname || "/admin";
          navigate(from, { replace: true });
        })
        .catch(() => {
          // Token is invalid/expired, clear it
          localStorage.removeItem('admin_token');
        });
    }
  }, [navigate, location]);

  const handleCredentialsSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError('');

    try {
      const params = new URLSearchParams();
      params.append('username', username);
      params.append('password', password);

      const response = await adminApiClient.post('/auth/token', params, {
        headers: { 'Content-Type': 'application/x-www-form-urlencoded' }
      });

      const { access_token, requires_2fa_setup } = response.data;
      localStorage.setItem('admin_token', access_token);

      // Check if 2FA setup is required
      if (requires_2fa_setup) {
        navigate('/admin/totp-setup', { replace: true });
        return;
      }

      // Navigate to where they came from, or dashboard
      const from = (location.state as any)?.from?.pathname || "/admin";
      navigate(from, { replace: true });
    } catch (err: any) {
      console.log('Login attempt error:', err.response?.status, err.response?.data);

      // Check if TOTP code is required (403 is our unique signal for ROOT + 2FA)
      if (err.response?.status === 403) {
        console.log('2FA required, switching to TOTP step');
        setStep('totp');
      } else {
        const detail = err.response?.data?.detail;
        setError(typeof detail === 'string' ? detail : 'Invalid username or password');
      }
    } finally {
      setLoading(false);
    }
  };

  const handleTotpSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError('');

    try {
      console.log('Submitting TOTP code...');
      const response = await adminApiClient.post('/auth/totp/verify', {
        username,
        password,
        code: totpCode
      });

      console.log('TOTP verification response:', response.data);

      const { access_token } = response.data;
      if (!access_token) {
        throw new Error('No access token received');
      }
      localStorage.setItem('admin_token', access_token);

      const from = (location.state as any)?.from?.pathname || "/admin";
      console.log('Navigating to:', from);
      navigate(from, { replace: true });
    } catch (err: any) {
      console.error('TOTP Error:', err);
      const detail = err.response?.data?.detail;
      setError(typeof detail === 'string' ? detail : (err.message || 'Invalid code'));
    } finally {
      setLoading(false);
    }
  };

  const handleBackupCodeSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError('');

    try {
      const response = await adminApiClient.post('/auth/totp/verify-backup', {
        username,
        password,
        backup_code: backupCode
      });

      const { access_token, warning } = response.data;
      localStorage.setItem('admin_token', access_token);

      if (warning) {
        alert(warning);
      }

      const from = (location.state as any)?.from?.pathname || "/admin";
      navigate(from, { replace: true });
    } catch (err: any) {
      console.error(err);
      const detail = err.response?.data?.detail;
      setError(typeof detail === 'string' ? detail : 'Invalid backup code');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-red-50 flex items-center justify-center p-4">
      <div className="bg-white p-8 rounded-lg shadow-xl border-t-4 border-red-600 w-full max-w-md">
        <div className="text-center mb-8">
          <h1 className="text-3xl font-bold text-gray-900 mb-2">System Admin</h1>
          <p className="text-red-600 font-medium bg-red-100 inline-block px-3 py-1 rounded-full text-sm">
            Restricted Access
          </p>
        </div>

        {error && (
          <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded relative mb-4" role="alert">
            <span className="block sm:inline">{error}</span>
          </div>
        )}

        {/* Step 1: Username & Password */}
        {step === 'credentials' && (
          <form onSubmit={handleCredentialsSubmit} className="space-y-6">
            <div>
              <label className="block text-gray-700 text-sm font-bold mb-2" htmlFor="username">
                Username
              </label>
              <input
                id="username"
                type="text"
                value={username}
                onChange={(e) => setUsername(e.target.value)}
                className="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline focus:border-red-500"
                required
              />
            </div>
            <div>
              <label className="block text-gray-700 text-sm font-bold mb-2" htmlFor="password">
                Password
              </label>
              <input
                id="password"
                type="password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                className="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline focus:border-red-500"
                required
              />
            </div>
            <div className="flex items-center justify-between">
              <button
                type="submit"
                disabled={loading}
                className={`w-full bg-red-700 hover:bg-red-800 text-white font-bold py-2 px-4 rounded focus:outline-none focus:shadow-outline transition duration-150 ${loading ? 'opacity-50 cursor-not-allowed' : ''}`}
              >
                {loading ? 'Authenticating...' : 'Login'}
              </button>
            </div>
          </form>
        )}

        {/* Step 2: TOTP Code */}
        {step === 'totp' && (
          <form onSubmit={handleTotpSubmit} className="space-y-6">
            <div className="text-center mb-4">
              <p className="text-gray-700">
                Enter the 6-digit code from your authenticator app
              </p>
            </div>
            <div>
              <label className="block text-gray-700 text-sm font-bold mb-2" htmlFor="totpCode">
                Authentication Code
              </label>
              <input
                id="totpCode"
                type="text"
                maxLength={6}
                pattern="[0-9]{6}"
                value={totpCode}
                onChange={(e) => setTotpCode(e.target.value.replace(/\D/g, ''))}
                className="text-center text-2xl tracking-widest font-mono shadow appearance-none border rounded w-full py-3 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline focus:border-red-500"
                placeholder="000000"
                autoFocus
                required
              />
            </div>
            <div className="flex items-center justify-between space-x-4">
              <button
                type="button"
                onClick={() => setStep('credentials')}
                className="flex-1 bg-gray-300 hover:bg-gray-400 text-gray-800 font-bold py-2 px-4 rounded focus:outline-none focus:shadow-outline transition duration-150"
              >
                Back
              </button>
              <button
                type="submit"
                disabled={loading || totpCode.length !== 6}
                className={`flex-1 bg-red-700 hover:bg-red-800 text-white font-bold py-2 px-4 rounded focus:outline-none focus:shadow-outline transition duration-150 ${loading || totpCode.length !== 6 ? 'opacity-50 cursor-not-allowed' : ''}`}
              >
                {loading ? 'Verifying...' : 'Verify'}
              </button>
            </div>
            <div className="text-center">
              <button
                type="button"
                onClick={() => setStep('backup')}
                className="text-sm text-red-600 hover:text-red-800 underline"
              >
                Use a backup code instead
              </button>
            </div>
          </form>
        )}

        {/* Step 3: Backup Code */}
        {step === 'backup' && (
          <form onSubmit={handleBackupCodeSubmit} className="space-y-6">
            <div className="text-center mb-4">
              <p className="text-gray-700">
                Enter one of your backup codes
              </p>
            </div>
            <div>
              <label className="block text-gray-700 text-sm font-bold mb-2" htmlFor="backupCode">
                Backup Code
              </label>
              <input
                id="backupCode"
                type="text"
                value={backupCode}
                onChange={(e) => setBackupCode(e.target.value.toUpperCase())}
                className="font-mono shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline focus:border-red-500"
                placeholder="XXXX-XXXX-XXXX"
                autoFocus
                required
              />
            </div>
            <div className="flex items-center justify-between space-x-4">
              <button
                type="button"
                onClick={() => setStep('totp')}
                className="flex-1 bg-gray-300 hover:bg-gray-400 text-gray-800 font-bold py-2 px-4 rounded focus:outline-none focus:shadow-outline transition duration-150"
              >
                Back
              </button>
              <button
                type="submit"
                disabled={loading}
                className={`flex-1 bg-red-700 hover:bg-red-800 text-white font-bold py-2 px-4 rounded focus:outline-none focus:shadow-outline transition duration-150 ${loading ? 'opacity-50 cursor-not-allowed' : ''}`}
              >
                {loading ? 'Verifying...' : 'Verify'}
              </button>
            </div>
          </form>
        )}

        <div className="mt-6 text-center text-xs text-gray-500">
          <p>Unauthorized access is prohibited and monitored.</p>
        </div>
      </div>
    </div>
  );
};

export default Login;

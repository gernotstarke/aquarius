import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import adminApiClient from '../../api/adminClient';
import { Shield, Download, Copy, Check } from 'lucide-react';

const TOTPSetup: React.FC = () => {
  const navigate = useNavigate();
  const [step, setStep] = useState<'loading' | 'scan' | 'verify' | 'complete'>('loading');
  const [qrCode, setQrCode] = useState('');
  const [secret, setSecret] = useState('');
  const [backupCodes, setBackupCodes] = useState<string[]>([]);
  const [verificationCode, setVerificationCode] = useState('');
  const [error, setError] = useState('');
  const [copied, setCopied] = useState(false);

  useEffect(() => {
    let ignore = false;

    // Fetch TOTP setup data
    adminApiClient.post('/auth/totp/setup')
      .then(response => {
        if (!ignore) {
          setQrCode(response.data.qr_code);
          setSecret(response.data.secret);
          setBackupCodes(response.data.backup_codes);
          setStep('scan');
        }
      })
      .catch(err => {
        if (!ignore) {
          console.error('Failed to setup TOTP:', err);
          setError('Failed to initialize 2FA setup');
        }
      });

    return () => {
      ignore = true;
    };
  }, []);

  const handleVerify = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');

    try {
      await adminApiClient.post('/auth/totp/enable', {
        code: verificationCode
      });
      setStep('complete');
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Invalid code. Please try again.');
    }
  };

  const downloadBackupCodes = () => {
    const text = backupCodes.join('\n');
    const blob = new Blob([text], { type: 'text/plain' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = 'aquarius-backup-codes.txt';
    a.click();
    URL.revokeObjectURL(url);
  };

  const copySecret = () => {
    navigator.clipboard.writeText(secret);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  if (step === 'loading') {
    return (
      <div className="min-h-screen bg-red-50 flex items-center justify-center">
        <div className="text-center">
          <p className="text-gray-600">Setting up 2FA...</p>
        </div>
      </div>
    );
  }

  if (step === 'complete') {
    return (
      <div className="min-h-screen bg-red-50 flex items-center justify-center p-4">
        <div className="bg-white rounded-lg shadow-xl p-8 w-full max-w-md border-t-4 border-green-600 text-center">
          <div className="mb-6">
            <div className="mx-auto w-16 h-16 bg-green-100 rounded-full flex items-center justify-center">
              <Check size={32} className="text-green-600" />
            </div>
          </div>
          <h1 className="text-2xl font-bold text-gray-900 mb-4">2FA Enabled!</h1>
          <p className="text-gray-600 mb-6">
            Two-factor authentication is now active for your account. You'll need your authenticator app for future logins.
          </p>
          <button
            onClick={() => navigate('/admin')}
            className="bg-green-600 hover:bg-green-700 text-white font-bold py-2 px-6 rounded transition-colors"
          >
            Continue to Dashboard
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-red-50 flex items-center justify-center p-4">
      <div className="bg-white rounded-lg shadow-xl p-8 w-full max-w-2xl border-t-4 border-red-600">
        <div className="flex items-center justify-center mb-6">
          <Shield size={40} className="text-red-600 mr-3" />
          <h1 className="text-2xl font-bold text-gray-900">Setup Two-Factor Authentication</h1>
        </div>

        {step === 'scan' && (
          <>
            <div className="mb-8">
              <h2 className="text-lg font-bold mb-4">Step 1: Scan QR Code</h2>
              <p className="text-gray-600 mb-4">
                Open Google Authenticator (or any compatible app) and scan this QR code:
              </p>
              <div className="flex justify-center mb-6">
                <img src={qrCode} alt="TOTP QR Code" className="border-4 border-gray-200 rounded" />
              </div>

              <div className="bg-gray-50 p-4 rounded">
                <p className="text-sm font-bold text-gray-700 mb-2">Can't scan? Enter this code manually:</p>
                <div className="flex items-center space-x-2">
                  <code className="flex-1 bg-white px-3 py-2 rounded border font-mono text-sm">
                    {secret}
                  </code>
                  <button
                    onClick={copySecret}
                    className="bg-gray-200 hover:bg-gray-300 p-2 rounded transition-colors"
                    title="Copy to clipboard"
                  >
                    {copied ? <Check size={20} className="text-green-600" /> : <Copy size={20} />}
                  </button>
                </div>
              </div>
            </div>

            <div className="mb-8">
              <h2 className="text-lg font-bold mb-4">Step 2: Save Backup Codes</h2>
              <div className="bg-yellow-50 border border-yellow-200 p-4 rounded mb-4">
                <p className="text-sm text-yellow-800 font-bold">⚠️  Important!</p>
                <p className="text-sm text-yellow-700">
                  Save these backup codes in a secure location. You can use them to access your account if you lose your device.
                </p>
              </div>

              <div className="bg-gray-50 p-4 rounded mb-4">
                <div className="grid grid-cols-2 gap-2 font-mono text-sm">
                  {backupCodes.map((code, idx) => (
                    <div key={idx} className="bg-white px-3 py-2 rounded border">
                      {code}
                    </div>
                  ))}
                </div>
              </div>

              <button
                onClick={downloadBackupCodes}
                className="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded flex items-center space-x-2 transition-colors"
              >
                <Download size={18} />
                <span>Download Backup Codes</span>
              </button>
            </div>

            <div className="border-t pt-6">
              <h2 className="text-lg font-bold mb-4">Step 3: Verify Setup</h2>
              <p className="text-gray-600 mb-4">
                Enter the 6-digit code from your authenticator app to complete setup:
              </p>

              <form onSubmit={handleVerify}>
                <div className="mb-4">
                  <input
                    type="text"
                    maxLength={6}
                    pattern="[0-9]{6}"
                    placeholder="000000"
                    value={verificationCode}
                    onChange={e => setVerificationCode(e.target.value.replace(/\D/g, ''))}
                    className="text-center text-2xl tracking-widest font-mono border-2 rounded w-full py-3 px-4 focus:outline-none focus:border-red-500"
                    required
                  />
                </div>

                {error && (
                  <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded mb-4">
                    {error}
                  </div>
                )}

                <div className="flex justify-end space-x-4">
                  <button
                    type="button"
                    onClick={() => navigate('/admin/login')}
                    className="bg-gray-300 hover:bg-gray-400 text-gray-800 font-bold py-2 px-6 rounded transition-colors"
                  >
                    Cancel
                  </button>
                  <button
                    type="submit"
                    disabled={verificationCode.length !== 6}
                    className="bg-red-700 hover:bg-red-800 text-white font-bold py-2 px-6 rounded transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
                  >
                    Enable 2FA
                  </button>
                </div>
              </form>
            </div>
          </>
        )}
      </div>
    </div>
  );
};

export default TOTPSetup;

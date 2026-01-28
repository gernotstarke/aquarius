import React, { useState, useRef, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { LogOut, Settings, Users } from 'lucide-react';
import apiClient from '../api/client';

const UserMenu: React.FC = () => {
  const navigate = useNavigate();
  const { user, logout, isAdmin } = useAuth();
  const [isOpen, setIsOpen] = useState(false);
  const [activeUserCount, setActiveUserCount] = useState<number | null>(null);
  const [isActiveUserCountLoading, setIsActiveUserCountLoading] = useState(false);
  const menuRef = useRef<HTMLDivElement>(null);

  // Close menu when clicking outside
  useEffect(() => {
    const handleClickOutside = (event: MouseEvent) => {
      if (menuRef.current && !menuRef.current.contains(event.target as Node)) {
        setIsOpen(false);
      }
    };

    if (isOpen) {
      document.addEventListener('mousedown', handleClickOutside);
      return () => document.removeEventListener('mousedown', handleClickOutside);
    }
  }, [isOpen]);

  useEffect(() => {
    if (!isOpen) return;

    let isCancelled = false;

    const fetchActiveUserCount = async () => {
      setIsActiveUserCountLoading(true);
      try {
        const response = await apiClient.get('/users/active-count', {
          params: { minutes: 5 },
        });
        if (!isCancelled) {
          setActiveUserCount(response.data?.active_users ?? null);
        }
      } catch {
        if (!isCancelled) {
          setActiveUserCount(null);
        }
      } finally {
        if (!isCancelled) {
          setIsActiveUserCountLoading(false);
        }
      }
    };

    fetchActiveUserCount();
    const interval = window.setInterval(fetchActiveUserCount, 30000);

    return () => {
      isCancelled = true;
      window.clearInterval(interval);
    };
  }, [isOpen]);

  if (!user) return null;

  const handleLogout = () => {
    logout();
    navigate('/app/login');
    setIsOpen(false);
  };

  const handleAdminClick = () => {
    navigate('/admin');
    setIsOpen(false);
  };

  const getAvatarImage = () => {
    if (user.role === 'CLEO') return '/cleo-glyph.png';
    if (user.role === 'ADMIN' || user.role === 'ROOT') return '/admin-glyph.png';
    return '/user-glyph.png';
  };

  return (
    <div className="relative" ref={menuRef}>
      {/* User Avatar Button with Glyph */}
      <button
        onClick={() => {
          const nextOpen = !isOpen;
          setIsOpen(nextOpen);
          if (nextOpen) {
            setIsActiveUserCountLoading(true);
          }
        }}
        className="flex items-center space-x-3 px-4 py-2 rounded-lg hover:bg-gray-100 transition"
        title={user.full_name || user.username}
      >
        <img
          src={getAvatarImage()}
          alt="User"
          className="w-16 h-16 object-contain"
        />
        <span className="text-sm text-gray-700">{user.username}</span>
      </button>

      {/* Dropdown Menu */}
      {isOpen && (
        <div className="absolute right-0 mt-2 w-56 bg-white rounded-lg shadow-lg border border-gray-200 py-2 z-50">
          {/* User Info */}
          <div className="px-4 py-2 border-b border-gray-200">
            <p className="text-sm font-medium text-gray-900">{user.full_name || user.username}</p>
            <p className="text-xs text-gray-500">{user.username}</p>
            <p className="text-xs text-gray-400 mt-1">
              {user.role === 'ROOT' ? 'Administrator' : 'App-Benutzer'}
            </p>
          </div>

          {/* Menu Items */}
          <div className="py-2">
            {/* Aktuelle User - Show concurrent users count */}
            <button
              onClick={() => setIsOpen(false)}
              className="w-full text-left px-4 py-2 text-sm text-gray-700 hover:bg-gray-100 flex items-center space-x-2 transition"
            >
              <Users size={16} />
              <div className="flex-1">
                <span>Aktuelle User</span>
              </div>
              <div className="ml-2">
                <span
                  className="inline-flex items-center justify-center min-w-[1.5rem] h-6 px-2 text-xs font-semibold rounded-full bg-gray-100 text-gray-700"
                  title="Aktiv in den letzten 5 Minuten"
                >
                  {isActiveUserCountLoading ? '…' : activeUserCount ?? '—'}
                </span>
              </div>
            </button>

            {/* Admin Link - only show if admin */}
            {isAdmin && (
              <button
                onClick={handleAdminClick}
                className="w-full text-left px-4 py-2 text-sm text-gray-700 hover:bg-gray-100 flex items-center space-x-2 transition"
              >
                <Settings size={16} />
                <span>Admin-Dashboard</span>
              </button>
            )}

            {/* Settings Link - future use */}
            <button
              onClick={() => setIsOpen(false)}
              className="w-full text-left px-4 py-2 text-sm text-gray-700 hover:bg-gray-100 flex items-center space-x-2 transition opacity-50 cursor-not-allowed"
              disabled
              title="Coming soon"
            >
              <Settings size={16} />
              <span>Einstellungen</span>
            </button>

            {/* Logout Button */}
            <button
              onClick={handleLogout}
              className="w-full text-left px-4 py-2 text-sm text-red-600 hover:bg-red-50 flex items-center space-x-2 transition border-t border-gray-200"
            >
              <LogOut size={16} />
              <span>Abmelden</span>
            </button>
          </div>
        </div>
      )}
    </div>
  );
};

export default UserMenu;

import React, { useState, useRef, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { LogOut, Settings, Users } from 'lucide-react';

const UserMenu: React.FC = () => {
  const navigate = useNavigate();
  const { user, logout, isAdmin } = useAuth();
  const [isOpen, setIsOpen] = useState(false);
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

  return (
    <div className="relative" ref={menuRef}>
      {/* User Avatar Button with Glyph */}
      <button
        onClick={() => setIsOpen(!isOpen)}
        className="flex items-center space-x-3 px-4 py-2 rounded-lg hover:bg-gray-100 transition"
        title={user.full_name || user.username}
      >
        <img
          src="/user-glyph.png"
          alt="User"
          className="w-12 h-12 object-contain"
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
                <span className="text-xs text-gray-400 ml-1">(coming soon)</span>
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

import React from 'react';
import { Link, useLocation } from 'react-router-dom';

interface LayoutProps {
  children: React.ReactNode;
}

const Layout: React.FC<LayoutProps> = ({ children }) => {
  const location = useLocation();

  const navItems = [
    { path: '/', label: 'Übersicht' },
    { path: '/saison', label: 'Saisons' },
    { path: '/schwimmbad', label: 'Schwimmbäder' },
    { path: '/wettkampf', label: 'Wettkämpfe' },
    { path: '/kind', label: 'Kinder' },
  ];

  return (
    <div className="min-h-screen bg-neutral-50">
      <nav className="bg-white border-b border-neutral-200 shadow-sm">
        <div className="max-w-7xl mx-auto px-8 py-6">
          <div className="flex items-center justify-between mb-6">
            <h1 className="text-h2 font-bold text-neutral-900">
              Arqua42 CRUD
            </h1>
          </div>
          <div className="flex gap-4 flex-wrap">
            {navItems.map((item) => (
              <Link
                key={item.path}
                to={item.path}
                className={`
                  px-6 py-3 min-h-touch rounded-lg font-medium text-body
                  transition-colors focus-ring
                  ${
                    location.pathname === item.path
                      ? 'bg-primary-600 text-white'
                      : 'bg-neutral-100 text-neutral-700 hover:bg-neutral-200'
                  }
                `}
              >
                {item.label}
              </Link>
            ))}
          </div>
        </div>
      </nav>
      <main className="max-w-7xl mx-auto px-8 py-12">
        {children}
      </main>
    </div>
  );
};

export default Layout;

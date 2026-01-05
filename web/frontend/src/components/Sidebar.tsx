import React, { useState } from 'react';
import { Link, useLocation } from 'react-router-dom';
import { useQuery } from '@tanstack/react-query';
import apiClient from '../api/client';
import { Verband } from '../types';

interface NavItem {
  to: string;
  label: string;
}

interface NavSection {
  title: string;
  icon: string;
  items: NavItem[];
  defaultOpen?: boolean;
}

const navSections: NavSection[] = [
  {
    title: 'Grunddaten',
    icon: '📅',
    defaultOpen: true,
    items: [
      { to: '/grunddaten/saisons', label: 'Saisons' },
      { to: '/grunddaten/schwimmbaeder', label: 'Schwimmbäder' },
      { to: '/grunddaten/figuren', label: 'Figuren' },
      { to: '/grunddaten/vereine', label: 'Vereine' },
      { to: '/grunddaten/verbaende', label: 'Verbände' },
    ],
  },
  {
    title: 'Kinder',
    icon: '👶',
    defaultOpen: false,
    items: [
      { to: '/kinder', label: 'Alle Kinder' },
    ],
  },
  {
    title: 'Wettkämpfe',
    icon: '🏆',
    defaultOpen: false,
    items: [
      { to: '/wettkaempfe', label: 'Übersicht' },
      { to: '/wettkaempfe/new', label: 'Neu anlegen' },
    ],
  },
  {
    title: 'Anmeldung',
    icon: '📝',
    defaultOpen: false,
    items: [
      { to: '/anmeldung', label: 'Neue Anmeldung' },
      { to: '/anmeldung/liste', label: 'Alle Anmeldungen' },
    ],
  },
];

const Sidebar: React.FC = () => {
  const location = useLocation();
  const { data: verbaende } = useQuery<Verband[]>({
    queryKey: ['verbaende'],
    queryFn: async () => {
      const response = await apiClient.get('/verband');
      return response.data;
    },
  });
  const [openSections, setOpenSections] = useState<Record<string, boolean>>(
    navSections.reduce((acc, section) => ({
      ...acc,
      [section.title]: section.defaultOpen ?? false,
    }), {})
  );

  const toggleSection = (title: string) => {
    setOpenSections(prev => ({
      ...prev,
      [title]: !prev[title],
    }));
  };

  const isActive = (path: string) => location.pathname === path;
  const isSectionActive = (items: NavItem[]) =>
    items.some(item => location.pathname.startsWith(item.to));

  return (
    <aside className="w-64 bg-white border-r border-neutral-200 min-h-screen flex-shrink-0">
      <div className="p-6 text-center">
        <Link to="/" className="block">
          <img src="/aquarius-logo.png" alt="Aquarius" className="h-20 mx-auto mb-2" />
          <p className="text-sm text-neutral-500 font-medium">Architektur in Aktion</p>
        </Link>
      </div>

      <nav className="px-3 pb-6">
        {navSections.map((section) => (
          <div key={section.title} className="mb-2">
            <button
              onClick={() => toggleSection(section.title)}
              className={`
                w-full flex items-center justify-between px-3 py-2 rounded-lg
                text-left font-medium transition-colors
                ${isSectionActive(section.items)
                  ? 'bg-primary-50 text-primary-700'
                  : 'text-neutral-700 hover:bg-neutral-100'}
              `}
            >
              <span className="flex items-center gap-2">
                <span className="text-lg">{section.icon}</span>
                <span>{section.title}</span>
              </span>
              <span className="text-xs">
                {openSections[section.title] ? '▼' : '▶'}
              </span>
            </button>

            {openSections[section.title] && (
              <div className="mt-1 ml-6 space-y-1">
                {section.items.map((item) => (
                  <Link
                    key={item.to}
                    to={item.to}
                    className={`
                      block px-3 py-2 rounded-lg text-sm transition-colors
                      ${isActive(item.to)
                        ? 'bg-primary-600 text-white font-medium'
                        : 'text-neutral-600 hover:bg-neutral-100'}
                    `}
                  >
                    {item.label}
                  </Link>
                ))}
                {section.title === 'Grunddaten' && verbaende && verbaende.length > 0 && (
                  <div className="pt-3">
                    <p className="text-xs font-semibold uppercase tracking-wide text-neutral-400">
                      Verbände
                    </p>
                    <div className="mt-2 space-y-1 text-xs text-neutral-500">
                      {verbaende.map((verband) => (
                        <div
                          key={verband.id}
                          className="truncate"
                          title={`${verband.name} (${verband.ort})`}
                        >
                          {verband.name}
                        </div>
                      ))}
                    </div>
                  </div>
                )}
              </div>
            )}
          </div>
        ))}
      </nav>
    </aside>
  );
};

export default Sidebar;

import React, { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import Card from '../components/Card';
import Button from '../components/Button';
import apiClient from '../api/client';

const Home: React.FC = () => {
  const [backendVersion, setBackendVersion] = useState<string>('0.0.0');
  useEffect(() => {
    // Fetch backend version from health endpoint
    apiClient.get('/health')
      .then(response => {
        if (response.data.version) {
          setBackendVersion(response.data.version);
        }
      })
      .catch(error => {
        console.error('Failed to fetch backend version:', error);
      });
  }, []);

  const mainSections = [
    {
      name: 'Anmeldung',
      description: 'Kinder für Wettkämpfe anmelden',
      path: '/anmeldung/liste',
      icon: '📝',
      color: 'bg-purple-50 hover:bg-purple-100',
    },
    {
      name: 'Wettkampf',
      description: 'Wettkämpfe organisieren und durchführen',
      path: '/wettkampf',
      icon: '🏆',
      color: 'bg-yellow-50 hover:bg-yellow-100',
    },
    {
      name: 'Grunddaten',
      description: 'Schwimmbäder, Figuren und Kinder verwalten',
      path: '/schwimmbad',
      icon: '🏊',
      color: 'bg-green-50 hover:bg-green-100',
    },
    {
      name: 'Saisonplanung',
      description: 'Saisons und Wettkämpfe planen',
      path: '/saison',
      icon: '📅',
      color: 'bg-blue-50 hover:bg-blue-100',
    },
  ];

  return (
    <div className="min-h-screen flex flex-col">
      {/* Main Content */}
      <div className="flex-1 space-y-12 pb-16">
        {/* Logo and Title */}
        <div className="text-center space-y-6">
          <h1 className="text-display font-bold text-neutral-900">
            Aquarius
          </h1>
          <p className="text-body-lg text-neutral-600 max-w-2xl mx-auto">
            Struktur, Konzepte, Wasser
          </p>
        </div>

        {/* Main Sections Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-8 max-w-4xl mx-auto">
          {mainSections.map((section: any) => (
            <Link key={section.path} to={section.path}>
              <Card className={`h-full transition-all duration-200 ${section.color}`}>
                <div className="flex flex-col h-full p-4">
                  <div className="flex-1 space-y-6">
                    <div className="text-6xl">{section.name === 'Grunddaten' ? '🏢 🤸 🧒' : section.icon}</div>
                    <div className="space-y-4">
                      {section.hideTitle ? (
                        <Button size="lg" className="w-full">
                          {section.buttonText}
                        </Button>
                      ) : (
                        <h2 className="text-h2 font-bold text-neutral-900">{section.name}</h2>
                      )}
                      <p className="text-body text-neutral-600">{section.description}</p>
                    </div>
                  </div>
                  <div className="mt-6">
                    {!section.hideTitle && (
                      <Button size="lg" className="w-full">
                        Öffnen
                      </Button>
                    )}
                  </div>
                </div>
              </Card>
            </Link>
          ))}
        </div>
      </div>

      {/* Footer */}
      <div className="border-t border-neutral-200 py-6">
        <div className="flex items-center justify-center gap-4 flex-wrap">
          <p className="text-sm text-neutral-500">
            made with passion in Cologne
          </p>
          <img
            src={`https://img.shields.io/badge/version-${backendVersion}-blue`}
            alt={`Version ${backendVersion}`}
            className="h-5"
          />
        </div>
      </div>
    </div>
  );
};

export default Home;

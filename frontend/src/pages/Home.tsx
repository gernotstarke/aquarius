import React from 'react';
import { Link } from 'react-router-dom';
import Card from '../components/Card';
import Button from '../components/Button';

const Home: React.FC = () => {
  const mainSections = [
    {
      name: 'Saisonplanung',
      description: 'Saisons und Wettkämpfe planen',
      path: '/saison',
      icon: '📅',
      color: 'bg-blue-50 hover:bg-blue-100',
    },
    {
      name: 'Wettkampf',
      description: 'Wettkämpfe organisieren und durchführen',
      path: '/wettkampf',
      icon: '🏆',
      color: 'bg-yellow-50 hover:bg-yellow-100',
    },
    {
      name: 'Stammdaten',
      description: 'Schwimmbäder, Figuren und Kinder verwalten',
      path: '/schwimmbad',
      icon: '🏊',
      color: 'bg-green-50 hover:bg-green-100',
    },
    {
      name: 'Anmeldung',
      description: 'Kinder für Wettkämpfe anmelden',
      path: '/anmeldung/liste',
      icon: '📝',
      color: 'bg-purple-50 hover:bg-purple-100',
    },
  ];

  return (
    <div className="min-h-screen flex flex-col">
      {/* Main Content */}
      <div className="flex-1 space-y-12 pb-16">
        {/* Logo and Title */}
        <div className="text-center space-y-6">
          <img
            src="/aquarius-logo.png"
            alt="Aquarius Logo"
            className="h-24 mx-auto"
          />
          <h1 className="text-display font-bold text-neutral-900">
            Aquarius
          </h1>
          <p className="text-body-lg text-neutral-600 max-w-2xl mx-auto">
            Kunstschwimmen-Wettkampf-Verwaltung
          </p>
        </div>

        {/* Main Sections Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-8 max-w-4xl mx-auto">
          {mainSections.map((section) => (
            <Link key={section.path} to={section.path}>
              <Card className={`h-full transition-all duration-200 ${section.color}`}>
                <div className="space-y-6 p-4">
                  <div className="text-6xl">{section.icon}</div>
                  <div className="space-y-2">
                    <h2 className="text-h2 font-bold text-neutral-900">{section.name}</h2>
                    <p className="text-body text-neutral-600">{section.description}</p>
                  </div>
                  <Button size="lg" className="w-full">
                    Öffnen
                  </Button>
                </div>
              </Card>
            </Link>
          ))}
        </div>
      </div>

      {/* Footer */}
      <div className="border-t border-neutral-200 py-6">
        <p className="text-center text-sm text-neutral-500">
          made with passion in Cologne
        </p>
      </div>
    </div>
  );
};

export default Home;

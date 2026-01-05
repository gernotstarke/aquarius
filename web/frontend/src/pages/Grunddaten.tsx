import React from 'react';
import { Link } from 'react-router-dom';
import Card from '../components/Card';
import Button from '../components/Button';
import { GRUNDDATEN_COLORS } from '../styles/colors';

const Grunddaten: React.FC = () => {
  const grunddatenSections = [
    {
      name: 'Saisons',
      description: 'Saisons verwalten und definieren',
      path: '/grunddaten/saisons',
      icon: '📅',
      color: GRUNDDATEN_COLORS.saisons.full,
    },
    {
      name: 'Schwimmbäder',
      description: 'Schwimmbäder und Austragungsorte verwalten',
      path: '/grunddaten/schwimmbaeder',
      icon: '🏊',
      color: GRUNDDATEN_COLORS.schwimmbaeder.full,
    },
    {
      name: 'Figuren',
      description: 'Figuren und Übungen definieren',
      path: '/grunddaten/figuren',
      icon: '🤸',
      color: GRUNDDATEN_COLORS.figuren.full,
    },
    {
      name: 'Vereine',
      description: 'Vereine und Organisationen verwalten',
      path: '/grunddaten/vereine',
      icon: '🏢',
      color: GRUNDDATEN_COLORS.vereine.full,
    },
  ];

  return (
    <div className="space-y-8">
      {/* Page Header */}
      <div>
        <h1 className="text-h1 font-bold text-neutral-900">Grunddaten</h1>
        <p className="text-body text-neutral-600 mt-2">
          Verwalten Sie alle grundlegenden Stammdaten für Aquarius
        </p>
      </div>

      {/* Tiles Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-2 gap-6">
        {grunddatenSections.map((section) => (
          <Link key={section.path} to={section.path}>
            <Card className={`h-full transition-all duration-200 ${section.color}`}>
              <div className="flex flex-col h-full p-4">
                <div className="flex-1 space-y-6">
                  <div className="text-6xl">{section.icon}</div>
                  <div className="space-y-4">
                    <h2 className="text-h2 font-bold text-neutral-900">
                      {section.name}
                    </h2>
                    <p className="text-body text-neutral-600">
                      {section.description}
                    </p>
                  </div>
                </div>
                <div className="mt-6">
                  <Button size="lg" className="w-full">
                    Öffnen
                  </Button>
                </div>
              </div>
            </Card>
          </Link>
        ))}
      </div>
    </div>
  );
};

export default Grunddaten;

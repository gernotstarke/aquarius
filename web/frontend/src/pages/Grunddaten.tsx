import React from 'react';
import { Link } from 'react-router-dom';
import Card from '../components/Card';
import Button from '../components/Button';

const Grunddaten: React.FC = () => {
  const tiles = [
    {
      name: 'Kinder',
      description: 'Teilnehmende Kinder verwalten',
      path: '/kinder',
      icon: '🧒',
      color: 'bg-orange-100 hover:bg-orange-200',
    },
    {
      name: 'Saisons',
      description: 'Saisons verwalten',
      path: '/grunddaten/saisons',
      icon: '📅',
      color: 'bg-blue-50 hover:bg-blue-100',
    },
    {
      name: 'Schwimmbäder',
      description: 'Bäder und Anlagen pflegen',
      path: '/grunddaten/schwimmbaeder',
      icon: '🏊',
      color: 'bg-cyan-50 hover:bg-cyan-100',
    },
    {
      name: 'Figuren',
      description: 'Figurenkatalog verwalten',
      path: '/grunddaten/figuren',
      icon: '🤸',
      color: 'bg-green-50 hover:bg-green-100',
    },
    {
      name: 'Vereine',
      description: 'Vereine verwalten',
      path: '/grunddaten/vereine',
      icon: '🏢',
      color: 'bg-amber-50 hover:bg-amber-100',
    },
    {
      name: 'Verbände',
      description: 'Nominierende Verbände anzeigen',
      path: '/grunddaten/verbaende',
      icon: '🏛️',
      color: 'bg-orange-50 hover:bg-orange-100',
    },
    {
      name: 'Versicherungen',
      description: 'Versicherungsgesellschaften anzeigen',
      path: '/grunddaten/versicherungen',
      icon: '🛡️',
      color: 'bg-amber-50 hover:bg-amber-100',
    },
  ];

  return (
    <div className="min-h-screen flex flex-col">
      <div className="flex-1 space-y-12 pb-16">
        <div className="text-center space-y-3">
          <h1 className="text-h1 font-bold text-neutral-900">Grunddaten</h1>
          <p className="text-body-lg text-neutral-600">
            Stammdaten für die Wettbewerbsorganisation
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-8 max-w-5xl mx-auto">
          {tiles.map((tile) => (
            <Link key={tile.path} to={tile.path}>
              <Card className={`h-full transition-all duration-200 ${tile.color}`}>
                <div className="flex flex-col h-full p-4">
                  <div className="flex-1 space-y-6">
                    <div className="text-6xl">{tile.icon}</div>
                    <div className="space-y-3">
                      <h2 className="text-h2 font-bold text-neutral-900">{tile.name}</h2>
                      <p className="text-body text-neutral-600">{tile.description}</p>
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
    </div>
  );
};

export default Grunddaten;

import React from 'react';
import { Link } from 'react-router-dom';
import Card from '../components/Card';
import Button from '../components/Button';

const Home: React.FC = () => {
  const entities = [
    {
      name: 'Saisons',
      description: 'Wettkampf-Saisons verwalten',
      path: '/saison',
      icon: '📅',
    },
    {
      name: 'Schwimmbäder',
      description: 'Schwimmbäder und Austragungsorte',
      path: '/schwimmbad',
      icon: '🏊',
    },
    {
      name: 'Wettkämpfe',
      description: 'Wettkämpfe planen und organisieren',
      path: '/wettkampf',
      icon: '🏆',
    },
    {
      name: 'Kinder',
      description: 'Teilnehmende Kinder verwalten',
      path: '/kind',
      icon: '👶',
    },
  ];

  return (
    <div className="space-y-12">
      <div className="text-center space-y-4">
        <h1 className="text-display font-bold text-neutral-900">
          Arqua42 CRUD Prototype
        </h1>
        <p className="text-body-lg text-neutral-600 max-w-2xl mx-auto">
          Einfache Verwaltung von Saisons, Schwimmbädern, Wettkämpfen und Kindern
        </p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-8 max-w-4xl mx-auto">
        {entities.map((entity) => (
          <Card key={entity.path} className="hover:shadow-md transition-shadow">
            <div className="space-y-6">
              <div className="text-6xl">{entity.icon}</div>
              <div className="space-y-2">
                <h2 className="text-h2 font-bold text-neutral-900">{entity.name}</h2>
                <p className="text-body text-neutral-600">{entity.description}</p>
              </div>
              <Link to={entity.path}>
                <Button size="lg" className="w-full">
                  Öffnen
                </Button>
              </Link>
            </div>
          </Card>
        ))}
      </div>
    </div>
  );
};

export default Home;

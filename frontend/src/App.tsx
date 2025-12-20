import React from 'react';
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import NewLayout from './components/NewLayout';
import Home from './pages/Home';
import SaisonList from './pages/SaisonList';
import SaisonForm from './pages/SaisonForm';
import SchwimmbadList from './pages/SchwimmbadList';
import SchwimmbadForm from './pages/SchwimmbadForm';
import WettkampfList from './pages/WettkampfList';
import WettkampfForm from './pages/WettkampfForm';
import WettkampfDetail from './pages/WettkampfDetail';
import KindList from './pages/KindList';
import KindForm from './pages/KindForm';
import FigurenList from './pages/FigurenList';
import FigurenForm from './pages/FigurenForm';
import AnmeldungList from './pages/AnmeldungList';
import AnmeldungForm from './pages/AnmeldungForm';

const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      refetchOnWindowFocus: false,
      retry: 1,
      staleTime: 30000,
    },
  },
});

const App: React.FC = () => {
  return (
    <QueryClientProvider client={queryClient}>
      <BrowserRouter>
        <NewLayout>
          <Routes>
            <Route path="/" element={<Home />} />

            {/* Stammdaten */}
            <Route path="/stammdaten/saisons" element={<SaisonList />} />
            <Route path="/stammdaten/saisons/new" element={<SaisonForm />} />
            <Route path="/stammdaten/saisons/:id" element={<SaisonForm />} />

            <Route path="/stammdaten/schwimmbaeder" element={<SchwimmbadList />} />
            <Route path="/stammdaten/schwimmbaeder/new" element={<SchwimmbadForm />} />
            <Route path="/stammdaten/schwimmbaeder/:id" element={<SchwimmbadForm />} />

            <Route path="/stammdaten/figuren" element={<FigurenList />} />
            <Route path="/stammdaten/figuren/new" element={<FigurenForm />} />
            <Route path="/stammdaten/figuren/:id" element={<FigurenForm />} />

            {/* Kinder */}
            <Route path="/kinder" element={<KindList />} />
            <Route path="/kinder/new" element={<KindForm />} />
            <Route path="/kinder/:id" element={<KindForm />} />

            {/* Wettkämpfe */}
            <Route path="/wettkaempfe" element={<WettkampfList />} />
            <Route path="/wettkaempfe/new" element={<WettkampfForm />} />
            <Route path="/wettkaempfe/:id/detail" element={<WettkampfDetail />} />
            <Route path="/wettkaempfe/:id" element={<WettkampfForm />} />

            {/* Anmeldung */}
            <Route path="/anmeldung" element={<AnmeldungForm />} />
            <Route path="/anmeldung/new" element={<AnmeldungForm />} />
            <Route path="/anmeldung/liste" element={<AnmeldungList />} />
            <Route path="/anmeldung/:id" element={<AnmeldungForm />} />

            {/* Legacy routes for backwards compatibility */}
            <Route path="/saison" element={<SaisonList />} />
            <Route path="/schwimmbad" element={<SchwimmbadList />} />
            <Route path="/wettkampf" element={<WettkampfList />} />
            <Route path="/kind" element={<KindList />} />
          </Routes>
        </NewLayout>
      </BrowserRouter>
    </QueryClientProvider>
  );
};

export default App;

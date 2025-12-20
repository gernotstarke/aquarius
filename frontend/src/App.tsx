import React from 'react';
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import Layout from './components/Layout';
import Home from './pages/Home';
import SaisonList from './pages/SaisonList';
import SaisonForm from './pages/SaisonForm';
import SchwimmbadList from './pages/SchwimmbadList';
import SchwimmbadForm from './pages/SchwimmbadForm';
import WettkampfList from './pages/WettkampfList';
import WettkampfForm from './pages/WettkampfForm';
import KindList from './pages/KindList';
import KindForm from './pages/KindForm';

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
        <Layout>
          <Routes>
            <Route path="/" element={<Home />} />

            <Route path="/saison" element={<SaisonList />} />
            <Route path="/saison/new" element={<SaisonForm />} />
            <Route path="/saison/:id" element={<SaisonForm />} />

            <Route path="/schwimmbad" element={<SchwimmbadList />} />
            <Route path="/schwimmbad/new" element={<SchwimmbadForm />} />
            <Route path="/schwimmbad/:id" element={<SchwimmbadForm />} />

            <Route path="/wettkampf" element={<WettkampfList />} />
            <Route path="/wettkampf/new" element={<WettkampfForm />} />
            <Route path="/wettkampf/:id" element={<WettkampfForm />} />

            <Route path="/kind" element={<KindList />} />
            <Route path="/kind/new" element={<KindForm />} />
            <Route path="/kind/:id" element={<KindForm />} />
          </Routes>
        </Layout>
      </BrowserRouter>
    </QueryClientProvider>
  );
};

export default App;

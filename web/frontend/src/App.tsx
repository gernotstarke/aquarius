import React from 'react';
import { BrowserRouter, Routes, Route, Navigate, Outlet } from 'react-router-dom';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { AuthProvider } from './context/AuthContext';
import NewLayout from './components/NewLayout';
import AppLoginGuard from './components/AppLoginGuard';
import AppLogin from './pages/AppLogin';
import Home from './pages/Home';
import Grunddaten from './pages/Grunddaten';
import SaisonList from './pages/SaisonList';
import SaisonForm from './pages/SaisonForm';
import SchwimmbadList from './pages/SchwimmbadList';
import SchwimmbadForm from './pages/SchwimmbadForm';
import VereinList from './pages/VereinList';
import VereinForm from './pages/VereinForm';
import VerbandList from './pages/VerbandList';
import VersicherungList from './pages/VersicherungList';
import WettkampfList from './pages/WettkampfList';
import WettkampfForm from './pages/WettkampfForm';
import WettkampfDetail from './pages/WettkampfDetail';
import KindList from './pages/KindList';
import KindForm from './pages/KindForm';
import FigurenList from './pages/FigurenList';
import FigurenForm from './pages/FigurenForm';
import FigurDetail from './pages/FigurDetail';
import AnmeldungList from './pages/AnmeldungList';
import AnmeldungForm from './pages/AnmeldungForm';

// Admin imports
import AdminLayout from './components/AdminLayout';
import AdminLogin from './pages/admin/Login';
import TOTPSetup from './pages/admin/TOTPSetup';
import AdminDashboard from './pages/admin/Dashboard';
import UserList from './pages/admin/UserList';
import KinderList from './pages/admin/KinderList';
import SystemHealth from './pages/admin/SystemHealth';
import DatabaseStats from './pages/admin/Database';

const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      refetchOnWindowFocus: false,
      retry: 1,
      staleTime: 30000,
    },
  },
});

// Simple Auth Guard for admin routes
const RequireAuth: React.FC = () => {
  const token = localStorage.getItem('admin_token');
  if (!token) {
    return <Navigate to="/admin/login" replace />;
  }
  return <Outlet />;
};

const App: React.FC = () => {
  return (
    <QueryClientProvider client={queryClient}>
      <AuthProvider>
        <BrowserRouter future={{ v7_startTransition: true, v7_relativeSplatPath: true }}>
          <Routes>
            {/* App Login */}
            <Route path="/app/login" element={<AppLogin />} />

            {/* Main App Routes - Protected */}
            <Route path="/" element={<AppLoginGuard />}>
              <Route element={<NewLayout><Outlet /></NewLayout>}>
                <Route index element={<Home />} />

                {/* Grunddaten */}
                <Route path="/grunddaten" element={<Grunddaten />} />
            <Route path="/grunddaten/saisons" element={<SaisonList />} />
            <Route path="/grunddaten/saisons/new" element={<SaisonForm />} />
            <Route path="/grunddaten/saisons/:id" element={<SaisonForm />} />

            <Route path="/grunddaten/schwimmbaeder" element={<SchwimmbadList />} />
            <Route path="/grunddaten/schwimmbaeder/new" element={<SchwimmbadForm />} />
            <Route path="/grunddaten/schwimmbaeder/:id" element={<SchwimmbadForm />} />

            <Route path="/grunddaten/figuren" element={<FigurenList />} />
            <Route path="/grunddaten/figuren/new" element={<FigurenForm />} />
            <Route path="/grunddaten/figuren/:id/detail" element={<FigurDetail />} />
            <Route path="/grunddaten/figuren/:id" element={<FigurenForm />} />

            <Route path="/grunddaten/vereine" element={<VereinList />} />
            <Route path="/grunddaten/vereine/new" element={<VereinForm />} />
            <Route path="/grunddaten/vereine/:id" element={<VereinForm />} />
            <Route path="/grunddaten/verbaende" element={<VerbandList />} />
            <Route path="/grunddaten/versicherungen" element={<VersicherungList />} />

            {/* Legacy stammdaten routes for backwards compatibility */}
            <Route path="/stammdaten/saisons" element={<SaisonList />} />
            <Route path="/stammdaten/saisons/new" element={<SaisonForm />} />
            <Route path="/stammdaten/saisons/:id" element={<SaisonForm />} />
            <Route path="/stammdaten/schwimmbaeder" element={<SchwimmbadList />} />
            <Route path="/stammdaten/schwimmbaeder/new" element={<SchwimmbadForm />} />
            <Route path="/stammdaten/schwimmbaeder/:id" element={<SchwimmbadForm />} />
            <Route path="/stammdaten/figuren" element={<FigurenList />} />
            <Route path="/stammdaten/figuren/new" element={<FigurenForm />} />
            <Route path="/stammdaten/figuren/:id/detail" element={<FigurDetail />} />
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
            <Route path="/saison/new" element={<SaisonForm />} />
            <Route path="/saison/:id" element={<SaisonForm />} />
            <Route path="/saison" element={<SaisonList />} />

            <Route path="/schwimmbad/new" element={<SchwimmbadForm />} />
            <Route path="/schwimmbad/:id" element={<SchwimmbadForm />} />
            <Route path="/schwimmbad" element={<SchwimmbadList />} />

            <Route path="/wettkampf/new" element={<WettkampfForm />} />
            <Route path="/wettkampf/:id" element={<WettkampfForm />} />
            <Route path="/wettkampf" element={<WettkampfList />} />
            
            <Route path="/kind/new" element={<KindForm />} />
            <Route path="/kind/:id" element={<KindForm />} />
            <Route path="/kind" element={<KindList />} />
              </Route>
            </Route>

            {/* Admin App */}
            <Route path="/admin/login" element={<AdminLogin />} />
            <Route path="/admin/totp-setup" element={<TOTPSetup />} />

            <Route path="/admin" element={<RequireAuth />}>
              <Route element={<AdminLayout />}>
                <Route index element={<AdminDashboard />} />
                <Route path="users" element={<UserList />} />
                <Route path="kinder" element={<KinderList />} />
                <Route path="health" element={<SystemHealth />} />
                <Route path="database" element={<DatabaseStats />} />
              </Route>
            </Route>

          </Routes>
        </BrowserRouter>
      </AuthProvider>
    </QueryClientProvider>
  );
};

export default App;

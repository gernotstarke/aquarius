import React from 'react';
import { Outlet, Link, useNavigate } from 'react-router-dom';

const AdminLayout: React.FC = () => {
  const navigate = useNavigate();

  const handleLogout = () => {
    localStorage.removeItem('token');
    navigate('/admin/login');
  };

  return (
    <div className="min-h-screen bg-red-50 text-gray-900">
      <header className="bg-red-900 text-white shadow-lg border-b-4 border-red-700">
        <div className="container mx-auto px-4 h-16 flex items-center justify-between">
          <div className="flex items-center space-x-4">
             <Link to="/admin" className="text-xl font-bold tracking-wider flex items-center">
               <img src="/logo.jpeg" alt="Aquarius Logo" className="h-10 w-auto mr-3 rounded-full border-2 border-red-200" />
               SYSTEM ADMIN
             </Link>
             <span className="bg-red-700 text-red-100 text-xs px-2 py-1 rounded uppercase font-bold tracking-wide">
               Restricted Area
             </span>
          </div>
          
          <div className="flex items-center space-x-6">
            <nav className="flex space-x-4 text-sm font-medium">
              <Link to="/admin/users" className="hover:text-red-200 transition-colors">Users</Link>
              <Link to="/" className="hover:text-red-200 transition-colors opacity-75">Exit to App</Link>
            </nav>
            <button 
              onClick={handleLogout}
              className="bg-red-800 hover:bg-red-700 text-white px-3 py-1 rounded text-sm transition-colors"
            >
              Logout
            </button>
          </div>
        </div>
      </header>

      <main className="container mx-auto px-4 py-8">
        <Outlet />
      </main>

      <footer className="bg-red-100 border-t border-red-200 mt-auto py-6 text-center text-red-800 text-sm">
        <p>
          ⚠️ Authorized Personnel Only. All actions are logged. |{' '}
          <a 
            href="https://github.com/gernotstarke/aquarius/blob/main/LICENSE" 
            target="_blank" 
            rel="noopener noreferrer"
            className="ml-1 text-red-900 hover:text-red-950 hover:underline font-medium"
          >
            MIT License
          </a>
        </p>
      </footer>
    </div>
  );
};

export default AdminLayout;

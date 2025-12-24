import React from 'react';
import { Link } from 'react-router-dom';

const AdminDashboard: React.FC = () => {
  return (
    <div>
      <h1 className="text-3xl font-bold text-gray-900 mb-8 border-b border-gray-200 pb-4">
        System Overview
      </h1>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        
        {/* User Management Card */}
        <div className="bg-white rounded-lg shadow border-t-4 border-red-600 p-6 hover:shadow-lg transition-shadow">
          <div className="flex items-center justify-between mb-4">
            <h2 className="text-xl font-bold text-gray-800">User Management</h2>
            <span className="text-3xl">👥</span>
          </div>
          <p className="text-gray-600 mb-6">
            Manage system administrators, planners, and officials (judges).
          </p>
          <Link 
            to="/admin/users" 
            className="block w-full text-center bg-red-100 hover:bg-red-200 text-red-800 font-semibold py-2 px-4 rounded transition-colors"
          >
            Manage Users
          </Link>
        </div>

        {/* System Health Card */}
        <div className="bg-white rounded-lg shadow border-t-4 border-gray-600 p-6 hover:shadow-lg transition-shadow">
          <div className="flex items-center justify-between mb-4">
            <h2 className="text-xl font-bold text-gray-800">System Health</h2>
            <span className="text-3xl">🩺</span>
          </div>
          <p className="text-gray-600 mb-6">
            Check database connectivity, storage usage, and system logs.
          </p>
          <Link 
            to="/admin/health" 
            className="block w-full text-center bg-gray-100 hover:bg-gray-200 text-gray-800 font-semibold py-2 px-4 rounded transition-colors"
          >
            Check Health
          </Link>
        </div>

        {/* Database Tools Card */}
        <div className="bg-white rounded-lg shadow border-t-4 border-gray-600 p-6 opacity-75">
          <div className="flex items-center justify-between mb-4">
            <h2 className="text-xl font-bold text-gray-800">Database Tools</h2>
            <span className="text-3xl">💾</span>
          </div>
          <p className="text-gray-600 mb-6">
            Backup, restore, or reset the database (Emergency Only).
          </p>
          <button disabled className="block w-full text-center bg-gray-100 text-gray-400 font-semibold py-2 px-4 rounded cursor-not-allowed">
            Coming Soon
          </button>
        </div>

      </div>

      <div className="mt-12 p-4 bg-yellow-50 border border-yellow-200 rounded-lg">
        <h3 className="text-lg font-bold text-yellow-800 mb-2">System Status</h3>
        <p className="text-sm text-yellow-700">
          Backend is running. Database connection established.
        </p>
      </div>
    </div>
  );
};

export default AdminDashboard;

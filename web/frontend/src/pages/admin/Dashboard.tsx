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
        <div className="bg-white rounded-lg shadow-md border-t-4 border-red-600 p-6 hover:shadow-xl transition-all hover:scale-105">
          <div className="flex items-center justify-between mb-4">
            <h2 className="text-xl font-bold text-gray-800">User Management</h2>
            <span className="text-4xl">👥</span>
          </div>
          <p className="text-gray-600 mb-6">
            Manage system administrators, planners, and officials (judges).
          </p>
          <Link
            to="/admin/users"
            className="block w-full text-center bg-red-500 hover:bg-red-600 text-white font-semibold py-2 px-4 rounded transition-colors"
          >
            Manage Users
          </Link>
        </div>

        {/* System Health Card */}
        <div className="bg-white rounded-lg shadow-md border-t-4 border-green-600 p-6 hover:shadow-xl transition-all hover:scale-105">
          <div className="flex items-center justify-between mb-4">
            <h2 className="text-xl font-bold text-gray-800">System Health</h2>
            <span className="text-4xl">🩺</span>
          </div>
          <p className="text-gray-600 mb-6">
            Check database connectivity, storage usage, and system logs.
          </p>
          <Link
            to="/admin/health"
            className="block w-full text-center bg-green-500 hover:bg-green-600 text-white font-semibold py-2 px-4 rounded transition-colors"
          >
            Check Health
          </Link>
        </div>

        {/* Database Tools Card */}
        <div className="bg-white rounded-lg shadow-md border-t-4 border-blue-600 p-6 hover:shadow-xl transition-all hover:scale-105">
          <div className="flex items-center justify-between mb-4">
            <h2 className="text-xl font-bold text-gray-800">Database Stats</h2>
            <span className="text-4xl">💾</span>
          </div>
          <p className="text-gray-600 mb-6">
            View database table statistics and row counts.
          </p>
          <Link
            to="/admin/database"
            className="block w-full text-center bg-blue-500 hover:bg-blue-600 text-white font-semibold py-2 px-4 rounded transition-colors"
          >
            View Stats
          </Link>
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

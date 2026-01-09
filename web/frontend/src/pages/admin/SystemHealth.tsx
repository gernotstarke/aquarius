import React from 'react';
import { useQuery } from '@tanstack/react-query';
import adminApiClient from '../../api/adminClient';
import { Activity, Database, Server, Clock, AlertTriangle, CheckCircle, Users } from 'lucide-react';

interface SystemHealthData {
  status: string;
  timestamp: string;
  uptime: string;
  system: {
    platform: string;
    python_version: string;
    cpu_percent: number;
    memory_usage_mb: number;
  };
  database: {
    status: string;
    latency_ms: number;
    type: string;
    size_bytes: number;
    table_count: number;
  };
}

interface ActiveUserCountResponse {
  active_users: number;
  window_minutes: number;
  timestamp: string;
}

const formatBytes = (bytes: number) => {
  if (bytes === 0) return '0 Bytes';
  const k = 1024;
  const sizes = ['Bytes', 'KB', 'MB', 'GB'];
  const i = Math.floor(Math.log(bytes) / Math.log(k));
  return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
};

const SystemHealth: React.FC = () => {
  const { data: health, isLoading, error } = useQuery<SystemHealthData>({
    queryKey: ['health'],
    queryFn: async () => {
      const response = await adminApiClient.get('/health/');
      return response.data;
    },
    refetchInterval: 5000 // Refresh every 5 seconds
  });

  const { data: activeUsers } = useQuery<ActiveUserCountResponse>({
    queryKey: ['activeUsers'],
    queryFn: async () => {
      const response = await adminApiClient.get('/admin/users/active-count?minutes=15');
      return response.data;
    },
    refetchInterval: 10000 // Refresh every 10 seconds
  });

  if (isLoading && !health) {
    return (
      <div className="flex justify-center items-center h-64">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-red-700"></div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded relative">
        <strong className="font-bold">Error loading system health: </strong>
        <span className="block sm:inline">{(error as any).message}</span>
      </div>
    );
  }

  const isHealthy = health?.status === 'healthy';

  return (
    <div>
      <div className="flex justify-between items-center mb-8">
        <h1 className="text-2xl font-bold text-gray-900 flex items-center">
          <Activity className="mr-3 text-red-700" size={32} />
          System Health Monitor
        </h1>
        <div className={`flex items-center px-4 py-2 rounded-full ${isHealthy ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800'}`}>
          {isHealthy ? <CheckCircle className="mr-2" size={20} /> : <AlertTriangle className="mr-2" size={20} />}
          <span className="font-bold uppercase">{health?.status}</span>
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        
        {/* System Info Card */}
        <div className="bg-white rounded-lg shadow border-t-4 border-blue-500 p-6">
          <div className="flex items-center justify-between mb-4 border-b pb-2">
            <h2 className="text-lg font-semibold text-gray-800 flex items-center">
              <Server className="mr-2 text-blue-500" /> Backend System
            </h2>
            <span className="text-sm text-gray-500">{health?.system.platform}</span>
          </div>
          <div className="space-y-4">
            <div className="flex justify-between items-center">
              <span className="text-gray-600">Uptime</span>
              <span className="font-mono font-medium">{health?.uptime}</span>
            </div>
            <div className="flex justify-between items-center">
              <span className="text-gray-600">Python Version</span>
              <span className="font-mono text-sm">{health?.system.python_version}</span>
            </div>
            <div className="flex justify-between items-center">
              <span className="text-gray-600">CPU Usage</span>
              <div className="flex items-center">
                <div className="w-24 bg-gray-200 rounded-full h-2.5 mr-2">
                  <div className="bg-blue-600 h-2.5 rounded-full" style={{ width: `${Math.min(health?.system.cpu_percent || 0, 100)}%` }}></div>
                </div>
                <span className="font-mono text-sm">{health?.system.cpu_percent}%</span>
              </div>
            </div>
            <div className="flex justify-between items-center">
              <span className="text-gray-600">Memory Usage</span>
              <span className="font-mono text-sm">{health?.system.memory_usage_mb} MB</span>
            </div>
          </div>
        </div>

        {/* Database Info Card */}
        <div className="bg-white rounded-lg shadow border-t-4 border-purple-500 p-6">
           <div className="flex items-center justify-between mb-4 border-b pb-2">
            <h2 className="text-lg font-semibold text-gray-800 flex items-center">
              <Database className="mr-2 text-purple-500" /> Database
            </h2>
            <span className="text-sm text-gray-500 uppercase">{health?.database.type}</span>
          </div>
          <div className="space-y-4">
             <div className="flex justify-between items-center">
              <span className="text-gray-600">Status</span>
              <span className={`px-2 py-1 rounded text-xs font-bold uppercase ${health?.database.status === 'ok' ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800'}`}>
                {health?.database.status}
              </span>
            </div>
            <div className="flex justify-between items-center">
              <span className="text-gray-600">Latency</span>
              <span className="font-mono text-sm">
                {health?.database.latency_ms} ms
              </span>
            </div>
            <div className="flex justify-between items-center">
              <span className="text-gray-600">Size</span>
              <span className="font-mono text-sm">
                {formatBytes(health?.database.size_bytes || 0)}
              </span>
            </div>
            <div className="flex justify-between items-center">
              <span className="text-gray-600">Tables</span>
              <span className="font-mono text-sm">
                {health?.database.table_count}
              </span>
            </div>
          </div>
        </div>

        {/* User Activity Card */}
        <div className="bg-white rounded-lg shadow border-t-4 border-green-500 p-6">
          <div className="flex items-center justify-between mb-4 border-b pb-2">
            <h2 className="text-lg font-semibold text-gray-800 flex items-center">
              <Users className="mr-2 text-green-500" /> User Activity
            </h2>
            <span className="text-sm text-gray-500">Live</span>
          </div>
          <div className="space-y-4">
            <div className="flex justify-between items-center">
              <span className="text-gray-600">Active Users</span>
              <span className="text-2xl font-bold text-green-600">
                {activeUsers?.active_users !== undefined ? activeUsers.active_users : '—'}
              </span>
            </div>
            <p className="text-sm text-gray-500">
              Users active in the last {activeUsers?.window_minutes || 15} minutes.
            </p>
          </div>
        </div>

        {/* Last Updated */}
        <div className="md:col-span-2 lg:col-span-3 text-center text-sm text-gray-500 flex justify-center items-center mt-4">
          <Clock size={16} className="mr-1" />
          Last updated: {new Date(health?.timestamp || '').toLocaleString()}
        </div>
      </div>
    </div>
  );
};

export default SystemHealth;

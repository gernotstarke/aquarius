import React, { useEffect, useState } from 'react';
import adminApiClient from '../../api/adminClient';

interface TableStat {
  table_name: string;
  count: number;
}

const DatabaseStats: React.FC = () => {
  const [stats, setStats] = useState<TableStat[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    fetchStats();
  }, []);

  const fetchStats = async () => {
    try {
      setLoading(true);
      setError(null);
      const response = await adminApiClient.get('/admin/database/stats');
      setStats(response.data.tables);
    } catch (err: any) {
      console.error('Failed to fetch database stats:', err);
      setError('Failed to load database statistics');
    } finally {
      setLoading(false);
    }
  };

  const totalRecords = stats.reduce((sum, stat) => sum + stat.count, 0);

  return (
    <div>
      <div className="flex items-center justify-between mb-8 border-b border-gray-200 pb-4">
        <h1 className="text-3xl font-bold text-gray-900">Database Statistics</h1>
        <button
          onClick={fetchStats}
          className="bg-blue-500 hover:bg-blue-600 text-white px-4 py-2 rounded transition-colors"
        >
          🔄 Refresh
        </button>
      </div>

      {loading && (
        <div className="text-center py-12">
          <p className="text-gray-600">Loading database statistics...</p>
        </div>
      )}

      {error && (
        <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded mb-6">
          {error}
        </div>
      )}

      {!loading && !error && (
        <>
          <div className="mb-6 p-4 bg-blue-50 border border-blue-200 rounded-lg">
            <div className="flex items-center justify-between">
              <h3 className="text-lg font-bold text-blue-800">Total Records</h3>
              <span className="text-3xl font-bold text-blue-900">{totalRecords.toLocaleString()}</span>
            </div>
          </div>

          <div className="bg-white rounded-lg shadow overflow-hidden">
            <table className="min-w-full divide-y divide-gray-200">
              <thead className="bg-gray-50">
                <tr>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Table Name
                  </th>
                  <th className="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Record Count
                  </th>
                  <th className="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Percentage
                  </th>
                </tr>
              </thead>
              <tbody className="bg-white divide-y divide-gray-200">
                {stats.map((stat) => {
                  const percentage = totalRecords > 0 ? (stat.count / totalRecords * 100) : 0;
                  return (
                    <tr key={stat.table_name} className="hover:bg-gray-50">
                      <td className="px-6 py-4 whitespace-nowrap">
                        <div className="flex items-center">
                          <span className="text-sm font-medium text-gray-900">
                            {stat.table_name}
                          </span>
                        </div>
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap text-right">
                        <span className="text-sm font-bold text-gray-900">
                          {stat.count.toLocaleString()}
                        </span>
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap text-right">
                        <div className="flex items-center justify-end space-x-2">
                          <div className="w-24 bg-gray-200 rounded-full h-2">
                            <div
                              className="bg-blue-600 h-2 rounded-full"
                              style={{ width: `${percentage}%` }}
                            ></div>
                          </div>
                          <span className="text-sm text-gray-500 w-12 text-right">
                            {percentage.toFixed(1)}%
                          </span>
                        </div>
                      </td>
                    </tr>
                  );
                })}
              </tbody>
            </table>
          </div>

          {stats.length === 0 && (
            <div className="text-center py-12 text-gray-500">
              No tables found in database.
            </div>
          )}
        </>
      )}
    </div>
  );
};

export default DatabaseStats;

import React, { useEffect, useState } from 'react';
import Link from 'next/link';
import { Database, Plus, RefreshCw, Search, ShieldCheck, Trash2 } from 'lucide-react';
import { apiClient } from '@/services/api';
import { Button } from '@/components/ui/Button';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/Card';
import { Badge } from '@/components/ui/Badge';
import { DataSource } from '@/types';

export default function SourcesIndexPage() {
  const [sources, setSources] = useState<DataSource[]>([]);
  const [loading, setLoading] = useState(true);
  const [search, setSearch] = useState('');
  const [testingId, setTestingId] = useState<string | null>(null);

  const fetchSources = async () => {
    setLoading(true);
    try {
      const res = await apiClient.get(`/sources?search=${search}`);
      setSources(res.data.items || []);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchSources();
  }, [search]);

  const testConnection = async (id: string) => {
    setTestingId(id);
    try {
      const res = await apiClient.post(`/sources/${id}/test`);
      alert(res.data.message || 'Connection test successful!');
      fetchSources();
    } catch (err: any) {
      alert(`Connection failed: ${err.response?.data?.detail || err.message}`);
    } finally {
      setTestingId(null);
    }
  };

  const deleteSource = async (id: string) => {
    if (confirm('Are you sure you want to delete this data source?')) {
      await apiClient.delete(`/sources/${id}`);
      fetchSources();
    }
  };

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-slate-100 tracking-tight">Data Sources & Connectors</h1>
          <p className="text-sm text-slate-400 mt-1">Manage external databases, object storage, event streams, and APIs</p>
        </div>
        <Link href="/sources/new">
          <Button variant="primary" size="sm">
            <Plus className="w-4 h-4 mr-1.5" />
            Connect Source
          </Button>
        </Link>
      </div>

      <Card>
        <CardHeader className="flex flex-row items-center justify-between gap-4">
          <div className="relative w-72">
            <Search className="w-4 h-4 absolute left-3 top-1/2 -translate-y-1/2 text-slate-400" />
            <input
              type="text"
              placeholder="Filter sources..."
              value={search}
              onChange={(e) => setSearch(e.target.value)}
              className="w-full pl-9 pr-4 py-2 bg-slate-900 border border-slate-800 rounded-lg text-xs text-slate-200 focus:outline-none focus:ring-1 focus:ring-blue-500"
            />
          </div>
          <Button variant="outline" size="sm" onClick={fetchSources}>
            <RefreshCw className="w-3.5 h-3.5 mr-1.5" /> Refresh
          </Button>
        </CardHeader>
        <CardContent className="p-0">
          <table className="w-full text-left text-xs">
            <thead className="bg-slate-900/60 text-slate-400 uppercase tracking-wider border-b border-slate-800">
              <tr>
                <th className="py-3.5 px-6">Name</th>
                <th className="py-3.5 px-6">Connector Type</th>
                <th className="py-3.5 px-6">Health Status</th>
                <th className="py-3.5 px-6">Credentials</th>
                <th className="py-3.5 px-6">Last Health Check</th>
                <th className="py-3.5 px-6 text-right">Actions</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-800 text-slate-300">
              {sources.length === 0 ? (
                <tr>
                  <td colSpan={6} className="text-center py-12 text-slate-500">
                    No data sources found. Connect PostgreSQL, MySQL, S3, or CSV to begin.
                  </td>
                </tr>
              ) : (
                sources.map((s) => (
                  <tr key={s.id} className="hover:bg-slate-800/40 transition-colors">
                    <td className="py-4 px-6 font-semibold text-slate-100">
                      <Link href={`/sources/${s.id}`} className="hover:text-blue-400">
                        {s.name}
                      </Link>
                    </td>
                    <td className="py-4 px-6 uppercase font-mono text-[11px] text-blue-400">
                      {s.connector_type}
                    </td>
                    <td className="py-4 px-6">
                      <Badge variant={s.health_status === 'healthy' ? 'success' : 'danger'}>
                        {s.health_status}
                      </Badge>
                    </td>
                    <td className="py-4 px-6">
                      {s.has_credentials ? (
                        <span className="text-emerald-400 font-medium">AES-256 Encrypted</span>
                      ) : (
                        <span className="text-slate-500">None</span>
                      )}
                    </td>
                    <td className="py-4 px-6 text-slate-400">
                      {s.last_health_check_at ? new Date(s.last_health_check_at).toLocaleString() : 'Never'}
                    </td>
                    <td className="py-4 px-6 text-right space-x-2">
                      <Button
                        variant="outline"
                        size="sm"
                        onClick={() => testConnection(s.id)}
                        isLoading={testingId === s.id}
                      >
                        Test
                      </Button>
                      <Button variant="danger" size="sm" onClick={() => deleteSource(s.id)}>
                        <Trash2 className="w-3.5 h-3.5" />
                      </Button>
                    </td>
                  </tr>
                ))
              )}
            </tbody>
          </table>
        </CardContent>
      </Card>
    </div>
  );
}

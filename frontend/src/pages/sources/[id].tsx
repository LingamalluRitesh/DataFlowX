import React, { useEffect, useState } from 'react';
import { useRouter } from 'next/router';
import Link from 'next/link';
import { ArrowLeft, Database, Play, RefreshCw, ShieldCheck } from 'lucide-react';
import { apiClient } from '@/services/api';
import { Button } from '@/components/ui/Button';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/Card';
import { Badge } from '@/components/ui/Badge';
import { DataSource } from '@/types';

export default function SourceDetailPage() {
  const router = useRouter();
  const { id } = router.query;
  const [source, setSource] = useState<DataSource | null>(null);
  const [schema, setSchema] = useState<any>(null);
  const [loading, setLoading] = useState(true);
  const [discovering, setDiscovering] = useState(false);

  const fetchSource = async () => {
    if (!id) return;
    try {
      const res = await apiClient.get(`/sources/${id}`);
      setSource(res.data);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchSource();
  }, [id]);

  const handleDiscoverSchema = async () => {
    if (!id) return;
    setDiscovering(true);
    try {
      const res = await apiClient.post(`/sources/${id}/discover-schema`);
      setSchema(res.data);
    } catch (err: any) {
      alert(`Schema discovery failed: ${err.response?.data?.detail || err.message}`);
    } finally {
      setDiscovering(false);
    }
  };

  if (loading) return <div>Loading source details...</div>;
  if (!source) return <div>Source not found</div>;

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-3">
          <Link href="/sources">
            <button className="p-2 rounded-lg bg-slate-900 border border-slate-800 text-slate-400 hover:text-slate-200">
              <ArrowLeft className="w-4 h-4" />
            </button>
          </Link>
          <div>
            <h1 className="text-xl font-bold text-slate-100">{source.name}</h1>
            <p className="text-xs text-slate-400 font-mono">{source.connector_type.toUpperCase()} • ID: {source.id}</p>
          </div>
        </div>

        <div className="flex items-center gap-3">
          <Button variant="outline" size="sm" onClick={handleDiscoverSchema} isLoading={discovering}>
            <RefreshCw className="w-3.5 h-3.5 mr-1.5" />
            Discover Schema & Tables
          </Button>
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <Card className="p-6 space-y-3">
          <h3 className="text-xs font-bold text-slate-400 uppercase tracking-wider">Connection Status</h3>
          <div className="flex items-center gap-2">
            <Badge variant={source.health_status === 'healthy' ? 'success' : 'danger'}>
              {source.health_status}
            </Badge>
          </div>
          <p className="text-xs text-slate-400">
            Last Checked: {source.last_health_check_at ? new Date(source.last_health_check_at).toLocaleString() : 'Never'}
          </p>
        </Card>

        <Card className="p-6 space-y-3">
          <h3 className="text-xs font-bold text-slate-400 uppercase tracking-wider">Credential Vault</h3>
          <div className="text-xs text-slate-200">
            {source.has_credentials ? 'AES-256 GCM Key rotation enabled' : 'No credentials configured'}
          </div>
        </Card>

        <Card className="p-6 space-y-3">
          <h3 className="text-xs font-bold text-slate-400 uppercase tracking-wider">Metadata Snapshot</h3>
          <p className="text-xs text-slate-300">Created: {new Date(source.created_at).toLocaleDateString()}</p>
        </Card>
      </div>

      {schema && (
        <Card>
          <CardHeader>
            <CardTitle>Discovered Tables & Columns</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="space-y-6">
              {schema.tables?.map((table: any) => (
                <div key={table.name} className="border border-slate-800 rounded-xl overflow-hidden">
                  <div className="bg-slate-900/80 px-4 py-2.5 flex items-center justify-between border-b border-slate-800">
                    <span className="font-mono text-xs font-bold text-blue-400">{table.name}</span>
                    <span className="text-[11px] text-slate-400">{table.columns?.length} columns</span>
                  </div>
                  <table className="w-full text-left text-xs">
                    <thead className="bg-slate-950 text-slate-400 border-b border-slate-800">
                      <tr>
                        <th className="py-2 px-4">Column Name</th>
                        <th className="py-2 px-4">Data Type</th>
                        <th className="py-2 px-4">Nullable</th>
                        <th className="py-2 px-4">Primary Key</th>
                      </tr>
                    </thead>
                    <tbody className="divide-y divide-slate-800 text-slate-300">
                      {table.columns?.map((col: any) => (
                        <tr key={col.name}>
                          <td className="py-2 px-4 font-mono">{col.name}</td>
                          <td className="py-2 px-4 font-mono text-purple-400">{col.data_type}</td>
                          <td className="py-2 px-4">{col.is_nullable ? 'Yes' : 'No'}</td>
                          <td className="py-2 px-4">{col.is_primary_key ? 'PK' : '-'}</td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>
              ))}
            </div>
          </CardContent>
        </Card>
      )}
    </div>
  );
}

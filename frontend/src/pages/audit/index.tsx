import React, { useEffect, useState } from 'react';
import { History, RefreshCw, Search, Shield } from 'lucide-react';
import { apiClient } from '@/services/api';
import { Button } from '@/components/ui/Button';
import { Card, CardContent, CardHeader } from '@/components/ui/Card';
import { AuditLog } from '@/types';

export default function AuditLogsPage() {
  const [logs, setLogs] = useState<AuditLog[]>([]);
  const [loading, setLoading] = useState(true);
  const [search, setSearch] = useState('');

  const fetchLogs = async () => {
    setLoading(true);
    try {
      const res = await apiClient.get(`/audit/logs?search=${search}`);
      setLogs(res.data.items || []);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchLogs();
  }, [search]);

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-slate-100 tracking-tight">Enterprise Audit Trail</h1>
          <p className="text-sm text-slate-400 mt-1">Immutable security, governance, and resource mutation history</p>
        </div>
        <Button variant="outline" size="sm" onClick={fetchLogs}>
          <RefreshCw className="w-3.5 h-3.5 mr-1.5" /> Refresh
        </Button>
      </div>

      <Card>
        <CardHeader className="flex flex-row items-center justify-between gap-4">
          <div className="relative w-72">
            <Search className="w-4 h-4 absolute left-3 top-1/2 -translate-y-1/2 text-slate-400" />
            <input
              type="text"
              placeholder="Search audit actions or actors..."
              value={search}
              onChange={(e) => setSearch(e.target.value)}
              className="w-full pl-9 pr-4 py-2 bg-slate-900 border border-slate-800 rounded-lg text-xs text-slate-200 focus:outline-none focus:ring-1 focus:ring-blue-500"
            />
          </div>
        </CardHeader>
        <CardContent className="p-0">
          <table className="w-full text-left text-xs">
            <thead className="bg-slate-900/60 text-slate-400 uppercase tracking-wider border-b border-slate-800">
              <tr>
                <th className="py-3.5 px-6">Timestamp</th>
                <th className="py-3.5 px-6">Actor Email</th>
                <th className="py-3.5 px-6">Action</th>
                <th className="py-3.5 px-6">Resource Type</th>
                <th className="py-3.5 px-6">Resource ID</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-800 text-slate-300 font-mono">
              {logs.length === 0 ? (
                <tr>
                  <td colSpan={5} className="text-center py-12 text-slate-500 font-sans">
                    No audit records match your query.
                  </td>
                </tr>
              ) : (
                logs.map((l) => (
                  <tr key={l.id} className="hover:bg-slate-800/40">
                    <td className="py-3.5 px-6 text-slate-400">{new Date(l.timestamp).toLocaleString()}</td>
                    <td className="py-3.5 px-6 text-blue-400">{l.actor_email || 'system'}</td>
                    <td className="py-3.5 px-6 font-bold text-slate-200">{l.action}</td>
                    <td className="py-3.5 px-6 uppercase text-purple-400">{l.resource_type}</td>
                    <td className="py-3.5 px-6 text-slate-400">{l.resource_id || '-'}</td>
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

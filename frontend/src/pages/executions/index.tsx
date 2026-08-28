import React, { useEffect, useState } from 'react';
import Link from 'next/link';
import { Activity, Play, RefreshCw, Search, ShieldCheck } from 'lucide-react';
import { apiClient } from '@/services/api';
import { Button } from '@/components/ui/Button';
import { Card, CardContent, CardHeader } from '@/components/ui/Card';
import { Badge } from '@/components/ui/Badge';
import { Execution } from '@/types';

export default function ExecutionsIndexPage() {
  const [executions, setExecutions] = useState<Execution[]>([]);
  const [loading, setLoading] = useState(true);
  const [search, setSearch] = useState('');

  const fetchExecutions = async () => {
    setLoading(true);
    try {
      const res = await apiClient.get(`/executions?search=${search}`);
      setExecutions(res.data.items || []);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchExecutions();
    const interval = setInterval(fetchExecutions, 10000);
    return () => clearInterval(interval);
  }, [search]);

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-slate-100 tracking-tight">Pipeline Executions</h1>
          <p className="text-sm text-slate-400 mt-1">Live execution status, throughput, durations, and logs</p>
        </div>
        <Button variant="outline" size="sm" onClick={fetchExecutions}>
          <RefreshCw className="w-3.5 h-3.5 mr-1.5" /> Refresh Live
        </Button>
      </div>

      <Card>
        <CardHeader className="flex flex-row items-center justify-between gap-4">
          <div className="relative w-72">
            <Search className="w-4 h-4 absolute left-3 top-1/2 -translate-y-1/2 text-slate-400" />
            <input
              type="text"
              placeholder="Search by status or trigger..."
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
                <th className="py-3.5 px-6">Execution ID</th>
                <th className="py-3.5 px-6">Status</th>
                <th className="py-3.5 px-6">Total Records</th>
                <th className="py-3.5 px-6">Failed Records</th>
                <th className="py-3.5 px-6">Quality Score</th>
                <th className="py-3.5 px-6">Duration</th>
                <th className="py-3.5 px-6">Trigger</th>
                <th className="py-3.5 px-6">Started</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-800 text-slate-300 font-medium">
              {executions.length === 0 ? (
                <tr>
                  <td colSpan={8} className="text-center py-12 text-slate-500">
                    No pipeline runs recorded. Trigger a pipeline to view execution telemetry.
                  </td>
                </tr>
              ) : (
                executions.map((e) => (
                  <tr key={e.id} className="hover:bg-slate-800/40 transition-colors">
                    <td className="py-4 px-6 font-mono text-blue-400 font-semibold">
                      <Link href={`/executions/${e.id}`}>{e.id}</Link>
                    </td>
                    <td className="py-4 px-6">
                      <Badge
                        variant={
                          e.status === 'SUCCESS'
                            ? 'success'
                            : e.status === 'RUNNING'
                            ? 'primary'
                            : e.status === 'FAILED'
                            ? 'danger'
                            : 'warning'
                        }
                      >
                        {e.status}
                      </Badge>
                    </td>
                    <td className="py-4 px-6">{e.total_records_processed.toLocaleString()}</td>
                    <td className="py-4 px-6 text-red-400">{e.records_failed.toLocaleString()}</td>
                    <td className="py-4 px-6 font-semibold text-emerald-400">
                      {e.quality_score !== undefined && e.quality_score !== null ? `${e.quality_score}%` : '-'}
                    </td>
                    <td className="py-4 px-6 font-mono text-slate-400">
                      {e.duration_seconds ? `${e.duration_seconds}s` : '< 1s'}
                    </td>
                    <td className="py-4 px-6 uppercase text-[10px] text-slate-400">{e.trigger_source || 'manual'}</td>
                    <td className="py-4 px-6 text-slate-400">{new Date(e.created_at).toLocaleString()}</td>
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

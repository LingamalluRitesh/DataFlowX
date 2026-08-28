import React, { useEffect, useState } from 'react';
import Link from 'next/link';
import { Play, Plus, RefreshCw, Search, Workflow } from 'lucide-react';
import { apiClient } from '@/services/api';
import { Button } from '@/components/ui/Button';
import { Card, CardContent, CardHeader } from '@/components/ui/Card';
import { Badge } from '@/components/ui/Badge';
import { Pipeline } from '@/types';

export default function PipelinesIndexPage() {
  const [pipelines, setPipelines] = useState<Pipeline[]>([]);
  const [loading, setLoading] = useState(true);
  const [search, setSearch] = useState('');
  const [triggeringId, setTriggeringId] = useState<string | null>(null);

  const fetchPipelines = async () => {
    setLoading(true);
    try {
      const res = await apiClient.get(`/pipelines?search=${search}`);
      setPipelines(res.data.items || []);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchPipelines();
  }, [search]);

  const handleTrigger = async (id: string) => {
    setTriggeringId(id);
    try {
      const res = await apiClient.post(`/pipelines/${id}/trigger`);
      alert(`Pipeline execution triggered! Execution ID: ${res.data.id}`);
      fetchPipelines();
    } catch (err: any) {
      alert(`Trigger failed: ${err.response?.data?.detail || err.message}`);
    } finally {
      setTriggeringId(null);
    }
  };

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-slate-100 tracking-tight">Pipelines & Workflows</h1>
          <p className="text-sm text-slate-400 mt-1">
            Visual Directed Acyclic Graph (DAG) pipelines, schedules, and retries
          </p>
        </div>
        <Link href="/pipelines/new">
          <Button variant="primary" size="sm">
            <Plus className="w-4 h-4 mr-1.5" />
            Create Pipeline
          </Button>
        </Link>
      </div>

      <Card>
        <CardHeader className="flex flex-row items-center justify-between gap-4">
          <div className="relative w-72">
            <Search className="w-4 h-4 absolute left-3 top-1/2 -translate-y-1/2 text-slate-400" />
            <input
              type="text"
              placeholder="Search pipelines..."
              value={search}
              onChange={(e) => setSearch(e.target.value)}
              className="w-full pl-9 pr-4 py-2 bg-slate-900 border border-slate-800 rounded-lg text-xs text-slate-200 focus:outline-none focus:ring-1 focus:ring-blue-500"
            />
          </div>
          <Button variant="outline" size="sm" onClick={fetchPipelines}>
            <RefreshCw className="w-3.5 h-3.5 mr-1.5" /> Refresh
          </Button>
        </CardHeader>
        <CardContent className="p-0">
          <table className="w-full text-left text-xs">
            <thead className="bg-slate-900/60 text-slate-400 uppercase tracking-wider border-b border-slate-800">
              <tr>
                <th className="py-3.5 px-6">Pipeline Name</th>
                <th className="py-3.5 px-6">Type</th>
                <th className="py-3.5 px-6">Environment</th>
                <th className="py-3.5 px-6">Status</th>
                <th className="py-3.5 px-6">Concurrency</th>
                <th className="py-3.5 px-6">Tags</th>
                <th className="py-3.5 px-6 text-right">Actions</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-800 text-slate-300">
              {pipelines.length === 0 ? (
                <tr>
                  <td colSpan={7} className="text-center py-12 text-slate-500">
                    No pipelines found. Click 'Create Pipeline' to design a visual DAG pipeline.
                  </td>
                </tr>
              ) : (
                pipelines.map((p) => (
                  <tr key={p.id} className="hover:bg-slate-800/40 transition-colors">
                    <td className="py-4 px-6 font-semibold text-slate-100">
                      <Link href={`/pipelines/${p.id}`} className="hover:text-blue-400">
                        {p.name}
                      </Link>
                    </td>
                    <td className="py-4 px-6 uppercase font-mono text-[11px] text-blue-400">
                      {p.pipeline_type}
                    </td>
                    <td className="py-4 px-6">
                      <Badge variant={p.environment === 'production' ? 'success' : 'neutral'}>
                        {p.environment}
                      </Badge>
                    </td>
                    <td className="py-4 px-6">
                      <Badge variant="primary">{p.status}</Badge>
                    </td>
                    <td className="py-4 px-6 text-slate-400">
                      {p.concurrency_limit} workers
                    </td>
                    <td className="py-4 px-6">
                      <div className="flex gap-1 flex-wrap">
                        {p.tags?.map((t) => (
                          <span key={t} className="px-2 py-0.5 rounded bg-slate-800 text-[10px] text-slate-400">
                            {t}
                          </span>
                        ))}
                      </div>
                    </td>
                    <td className="py-4 px-6 text-right">
                      <Button
                        variant="success"
                        size="sm"
                        onClick={() => handleTrigger(p.id)}
                        isLoading={triggeringId === p.id}
                      >
                        <Play className="w-3 h-3 mr-1 fill-current" /> Run
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

import React, { useEffect, useState } from 'react';
import { useRouter } from 'next/router';
import Link from 'next/link';
import { Activity, ArrowLeft, CheckCircle2, Clock, RefreshCw, Terminal, XCircle } from 'lucide-react';
import { apiClient } from '@/services/api';
import { Button } from '@/components/ui/Button';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/Card';
import { Badge } from '@/components/ui/Badge';
import { Execution, TaskExecution, TaskLog } from '@/types';

export default function ExecutionDetailPage() {
  const router = useRouter();
  const { id } = router.query;
  const [execution, setExecution] = useState<Execution | null>(null);
  const [logs, setLogs] = useState<TaskLog[]>([]);
  const [loading, setLoading] = useState(true);

  const fetchExecution = async () => {
    if (!id) return;
    try {
      const [execRes, logsRes] = await Promise.all([
        apiClient.get(`/executions/${id}`),
        apiClient.get(`/executions/${id}/logs`),
      ]);
      setExecution(execRes.data);
      setLogs(logsRes.data || []);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchExecution();
    const interval = setInterval(fetchExecution, 5000);
    return () => clearInterval(interval);
  }, [id]);

  if (loading) return <div>Loading execution run...</div>;
  if (!execution) return <div>Execution run not found</div>;

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-3">
          <Link href="/executions">
            <button className="p-2 rounded-lg bg-slate-900 border border-slate-800 text-slate-400 hover:text-slate-200">
              <ArrowLeft className="w-4 h-4" />
            </button>
          </Link>
          <div>
            <div className="flex items-center gap-3">
              <h1 className="text-xl font-mono font-bold text-slate-100">{execution.id}</h1>
              <Badge
                variant={
                  execution.status === 'SUCCESS'
                    ? 'success'
                    : execution.status === 'RUNNING'
                    ? 'primary'
                    : execution.status === 'FAILED'
                    ? 'danger'
                    : 'warning'
                }
              >
                {execution.status}
              </Badge>
            </div>
            <p className="text-xs text-slate-400 mt-1">Pipeline ID: {execution.pipeline_id}</p>
          </div>
        </div>

        <Button variant="outline" size="sm" onClick={fetchExecution}>
          <RefreshCw className="w-3.5 h-3.5 mr-1.5" /> Refresh
        </Button>
      </div>

      {/* Metrics Summary */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-5">
        <Card className="p-5">
          <span className="text-xs text-slate-400 font-medium">Duration</span>
          <p className="text-xl font-bold text-slate-100 mt-2 font-mono">
            {execution.duration_seconds ? `${execution.duration_seconds}s` : '< 1s'}
          </p>
        </Card>
        <Card className="p-5">
          <span className="text-xs text-slate-400 font-medium">Processed Records</span>
          <p className="text-xl font-bold text-blue-400 mt-2 font-mono">
            {execution.total_records_processed.toLocaleString()}
          </p>
        </Card>
        <Card className="p-5">
          <span className="text-xs text-slate-400 font-medium">Failed Records (Quarantine)</span>
          <p className="text-xl font-bold text-red-400 mt-2 font-mono">
            {execution.records_failed.toLocaleString()}
          </p>
        </Card>
        <Card className="p-5">
          <span className="text-xs text-slate-400 font-medium">Quality Score</span>
          <p className="text-xl font-bold text-emerald-400 mt-2 font-mono">
            {execution.quality_score !== undefined && execution.quality_score !== null
              ? `${execution.quality_score}%`
              : 'N/A'}
          </p>
        </Card>
      </div>

      {/* Task Executions Tree */}
      <Card>
        <CardHeader>
          <CardTitle>DAG Task Executions</CardTitle>
        </CardHeader>
        <CardContent className="p-0">
          <table className="w-full text-left text-xs">
            <thead className="bg-slate-900/60 text-slate-400 uppercase tracking-wider border-b border-slate-800">
              <tr>
                <th className="py-3 px-6">Task Node</th>
                <th className="py-3 px-6">Status</th>
                <th className="py-3 px-6">Duration</th>
                <th className="py-3 px-6">Records In</th>
                <th className="py-3 px-6">Records Out</th>
                <th className="py-3 px-6">Attempt</th>
                <th className="py-3 px-6">Error</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-800 text-slate-300">
              {execution.tasks?.map((t) => (
                <tr key={t.id} className="hover:bg-slate-800/40">
                  <td className="py-3.5 px-6 font-semibold text-slate-100 flex items-center gap-2">
                    {t.status === 'SUCCESS' ? (
                      <CheckCircle2 className="w-4 h-4 text-emerald-400" />
                    ) : t.status === 'FAILED' ? (
                      <XCircle className="w-4 h-4 text-red-400" />
                    ) : (
                      <Clock className="w-4 h-4 text-blue-400" />
                    )}
                    <span>{t.name}</span>
                  </td>
                  <td className="py-3.5 px-6">
                    <Badge variant={t.status === 'SUCCESS' ? 'success' : t.status === 'FAILED' ? 'danger' : 'primary'}>
                      {t.status}
                    </Badge>
                  </td>
                  <td className="py-3.5 px-6 font-mono text-slate-400">{t.duration_seconds}s</td>
                  <td className="py-3.5 px-6">{t.records_in.toLocaleString()}</td>
                  <td className="py-3.5 px-6">{t.records_out.toLocaleString()}</td>
                  <td className="py-3.5 px-6">#{t.attempt_number}</td>
                  <td className="py-3.5 px-6 text-red-400 font-mono max-w-xs truncate">{t.error_message || '-'}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </CardContent>
      </Card>

      {/* Live Terminal Log Stream */}
      <Card>
        <CardHeader className="flex flex-row items-center justify-between">
          <div className="flex items-center gap-2">
            <Terminal className="w-4 h-4 text-blue-400" />
            <CardTitle>Execution Log Stream</CardTitle>
          </div>
          <span className="text-xs text-slate-500 font-mono">{logs.length} entries</span>
        </CardHeader>
        <CardContent>
          <div className="h-80 bg-slate-950 rounded-xl p-4 font-mono text-xs overflow-y-auto space-y-1.5 border border-slate-800">
            {logs.length === 0 ? (
              <p className="text-slate-500 italic">No logs recorded for this execution.</p>
            ) : (
              logs.map((l) => (
                <div key={l.id} className="flex items-baseline gap-3">
                  <span className="text-slate-500 flex-shrink-0">{new Date(l.logged_at).toLocaleTimeString()}</span>
                  <span
                    className={`font-semibold flex-shrink-0 ${
                      l.log_level === 'ERROR'
                        ? 'text-red-400'
                        : l.log_level === 'WARNING'
                        ? 'text-amber-400'
                        : 'text-blue-400'
                    }`}
                  >
                    [{l.log_level}]
                  </span>
                  <span className="text-slate-300 break-all">{l.message}</span>
                </div>
              ))
            )}
          </div>
        </CardContent>
      </Card>
    </div>
  );
}

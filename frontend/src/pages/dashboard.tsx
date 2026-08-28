import React, { useEffect, useState } from 'react';
import Link from 'next/link';
import {
  Activity,
  AlertCircle,
  ArrowUpRight,
  CheckCircle2,
  Cpu,
  Database,
  Layers,
  Play,
  Plus,
  ShieldCheck,
  Workflow,
  XCircle,
} from 'lucide-react';
import {
  Area,
  AreaChart,
  CartesianGrid,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
} from 'recharts';
import { apiClient } from '@/services/api';
import { Button } from '@/components/ui/Button';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/Card';
import { StatCard } from '@/components/ui/StatCard';
import { Badge } from '@/components/ui/Badge';
import { Execution, SystemOverview } from '@/types';

const chartData = [
  { time: '00:00', records: 4500, quality: 98.5 },
  { time: '04:00', records: 8200, quality: 99.1 },
  { time: '08:00', records: 15400, quality: 97.8 },
  { time: '12:00', records: 28900, quality: 98.9 },
  { time: '16:00', records: 22100, quality: 99.4 },
  { time: '20:00', records: 18500, quality: 98.2 },
  { time: '24:00', records: 12000, quality: 99.0 },
];

export default function DashboardPage() {
  const [overview, setOverview] = useState<SystemOverview | null>(null);
  const [recentExecutions, setRecentExecutions] = useState<Execution[]>([]);
  const [loading, setLoading] = useState(true);
  const [runningDemo, setRunningDemo] = useState(false);

  const fetchDashboardData = async () => {
    try {
      const [ovRes, execRes] = await Promise.all([
        apiClient.get('/monitoring/overview'),
        apiClient.get('/executions?page=1&page_size=6'),
      ]);
      setOverview(ovRes.data);
      setRecentExecutions(execRes.data.items || []);
    } catch (err) {
      console.error('Failed to load dashboard metrics:', err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchDashboardData();
  }, []);

  const handleRunDemo = async () => {
    setRunningDemo(true);
    try {
      // Find customer 360 pipeline
      const pRes = await apiClient.get('/pipelines');
      const demoPipe = pRes.data.items?.find((p: any) => p.name.includes('Customer 360'));
      if (demoPipe) {
        await apiClient.post(`/pipelines/${demoPipe.id}/trigger`);
        await fetchDashboardData();
      }
    } catch (err) {
      console.error('Trigger demo failed:', err);
    } finally {
      setRunningDemo(false);
    }
  };

  return (
    <div className="space-y-8">
      {/* Top Banner & Quick Actions */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
        <div>
          <h1 className="text-2xl font-bold text-slate-900 dark:text-slate-100 tracking-tight">
            Enterprise Control Center
          </h1>
          <p className="text-sm text-slate-500 dark:text-slate-400 mt-1">
            Real-time pipeline orchestration, data quality telemetry & Medallion lakes.
          </p>
        </div>

        <div className="flex items-center gap-3">
          <Button variant="outline" size="sm" onClick={handleRunDemo} isLoading={runningDemo}>
            <Play className="w-4 h-4 mr-1.5 fill-current text-blue-500" />
            Run Customer 360 Pipeline
          </Button>
          <Link href="/pipelines/new">
            <Button variant="primary" size="sm">
              <Plus className="w-4 h-4 mr-1.5" />
              Build Pipeline
            </Button>
          </Link>
        </div>
      </div>

      {/* KPI Stat Cards Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-5">
        <StatCard
          title="Active Pipelines"
          value={overview?.active_pipelines ?? 0}
          icon={<Workflow className="w-5 h-5" />}
          description={`out of ${overview?.total_pipelines ?? 0} total pipelines`}
        />
        <StatCard
          title="24h Processed Records"
          value={(overview?.total_records_processed_24h ?? 0).toLocaleString()}
          icon={<Database className="w-5 h-5" />}
          trend={{ value: '18.4%', isPositive: true }}
          description="Across Bronze & Silver lakes"
        />
        <StatCard
          title="Avg Quality Score"
          value={`${overview?.average_data_quality_score ?? 98.5}%`}
          icon={<ShieldCheck className="w-5 h-5" />}
          trend={{ value: '1.2%', isPositive: true }}
          description="Passed data quality contracts"
        />
        <StatCard
          title="Worker Cluster Nodes"
          value={overview?.active_workers_count ?? 1}
          icon={<Cpu className="w-5 h-5" />}
          description="Auto-scaling priority queues"
        />
      </div>

      {/* Charts & Ingestion Throughput Section */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Main Records Ingestion Trend */}
        <Card className="lg:col-span-2">
          <CardHeader className="flex flex-row items-center justify-between">
            <div>
              <CardTitle>Ingestion & Processing Throughput</CardTitle>
              <p className="text-xs text-slate-400 mt-1">Processed records stream over the last 24 hours</p>
            </div>
            <Badge variant="primary">Live Stream</Badge>
          </CardHeader>
          <CardContent>
            <div className="h-[280px] w-full">
              <ResponsiveContainer width="100%" height="100%">
                <AreaChart data={chartData} margin={{ top: 10, right: 10, left: -20, bottom: 0 }}>
                  <defs>
                    <linearGradient id="colorRecords" x1="0" y1="0" x2="0" y2="1">
                      <stop offset="5%" stopColor="#3b82f6" stopOpacity={0.4} />
                      <stop offset="95%" stopColor="#3b82f6" stopOpacity={0.0} />
                    </linearGradient>
                  </defs>
                  <CartesianGrid strokeDasharray="3 3" stroke="#334155" opacity={0.3} />
                  <XAxis dataKey="time" stroke="#64748b" fontSize={12} tickLine={false} />
                  <YAxis stroke="#64748b" fontSize={12} tickLine={false} />
                  <Tooltip
                    contentStyle={{
                      backgroundColor: '#0f172a',
                      borderColor: '#1e293b',
                      borderRadius: '0.5rem',
                      color: '#f8fafc',
                    }}
                  />
                  <Area
                    type="monotone"
                    dataKey="records"
                    stroke="#3b82f6"
                    strokeWidth={2}
                    fillOpacity={1}
                    fill="url(#colorRecords)"
                  />
                </AreaChart>
              </ResponsiveContainer>
            </div>
          </CardContent>
        </Card>

        {/* Medallion Architecture Summary Card */}
        <Card>
          <CardHeader>
            <CardTitle>Medallion Lake Layers</CardTitle>
            <p className="text-xs text-slate-400 mt-1">Storage layout & data curation</p>
          </CardHeader>
          <CardContent className="space-y-4">
            <div className="p-4 rounded-xl bg-amber-950/20 border border-amber-800/40 flex items-center justify-between">
              <div className="flex items-center gap-3">
                <div className="p-2 rounded-lg bg-amber-500/20 text-amber-400">
                  <Database className="w-4 h-4" />
                </div>
                <div>
                  <h4 className="text-xs font-bold text-amber-200 uppercase tracking-wider">Bronze Lake</h4>
                  <p className="text-[11px] text-amber-400/80">Raw immutable append stream</p>
                </div>
              </div>
              <Badge variant="bronze">Raw Parquet</Badge>
            </div>

            <div className="p-4 rounded-xl bg-slate-800/40 border border-slate-700/60 flex items-center justify-between">
              <div className="flex items-center gap-3">
                <div className="p-2 rounded-lg bg-slate-400/20 text-slate-300">
                  <Layers className="w-4 h-4" />
                </div>
                <div>
                  <h4 className="text-xs font-bold text-slate-200 uppercase tracking-wider">Silver Lake</h4>
                  <p className="text-[11px] text-slate-400">Cleaned, validated & deduplicated</p>
                </div>
              </div>
              <Badge variant="silver">Curated</Badge>
            </div>

            <div className="p-4 rounded-xl bg-yellow-950/20 border border-yellow-800/40 flex items-center justify-between">
              <div className="flex items-center gap-3">
                <div className="p-2 rounded-lg bg-yellow-500/20 text-yellow-400">
                  <ShieldCheck className="w-4 h-4" />
                </div>
                <div>
                  <h4 className="text-xs font-bold text-yellow-200 uppercase tracking-wider">Gold Marts</h4>
                  <p className="text-[11px] text-yellow-400/80">Aggregated analytical tables</p>
                </div>
              </div>
              <Badge variant="gold">Business Ready</Badge>
            </div>
          </CardContent>
        </Card>
      </div>

      {/* Recent Executions Table */}
      <Card>
        <CardHeader className="flex flex-row items-center justify-between">
          <div>
            <CardTitle>Recent Pipeline Runs</CardTitle>
            <p className="text-xs text-slate-400 mt-1">Live telemetry for recent DAG executions</p>
          </div>
          <Link href="/executions" className="text-xs font-semibold text-blue-400 hover:text-blue-300 flex items-center gap-1">
            View all executions <ArrowUpRight className="w-3.5 h-3.5" />
          </Link>
        </CardHeader>
        <CardContent className="p-0">
          <div className="overflow-x-auto">
            <table className="w-full text-left text-xs">
              <thead className="bg-slate-900/60 text-slate-400 uppercase tracking-wider border-b border-slate-800">
                <tr>
                  <th className="py-3.5 px-6">Execution ID</th>
                  <th className="py-3.5 px-6">Status</th>
                  <th className="py-3.5 px-6">Records In/Out</th>
                  <th className="py-3.5 px-6">Quality Score</th>
                  <th className="py-3.5 px-6">Duration</th>
                  <th className="py-3.5 px-6">Trigger</th>
                  <th className="py-3.5 px-6">Started At</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-800 text-slate-300 font-medium">
                {recentExecutions.length === 0 ? (
                  <tr>
                    <td colSpan={7} className="text-center py-8 text-slate-500">
                      No executions recorded yet. Click 'Run Customer 360 Pipeline' to launch a demo run!
                    </td>
                  </tr>
                ) : (
                  recentExecutions.map((e) => (
                    <tr key={e.id} className="hover:bg-slate-800/40 transition-colors">
                      <td className="py-4 px-6 font-mono text-blue-400">
                        <Link href={`/executions/${e.id}`}>{e.id.substring(0, 18)}...</Link>
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
                      <td className="py-4 px-6">
                        {e.total_records_processed.toLocaleString()} rows
                      </td>
                      <td className="py-4 px-6 font-semibold text-emerald-400">
                        {e.quality_score !== undefined && e.quality_score !== null ? `${e.quality_score}%` : '-'}
                      </td>
                      <td className="py-4 px-6 font-mono text-slate-400">
                        {e.duration_seconds ? `${e.duration_seconds}s` : '< 1s'}
                      </td>
                      <td className="py-4 px-6 uppercase text-[10px] tracking-wider text-slate-400">
                        {e.trigger_source || 'manual'}
                      </td>
                      <td className="py-4 px-6 text-slate-400">
                        {new Date(e.created_at).toLocaleTimeString()}
                      </td>
                    </tr>
                  ))
                )}
              </tbody>
            </table>
          </div>
        </CardContent>
      </Card>
    </div>
  );
}

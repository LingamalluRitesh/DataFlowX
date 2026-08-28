import React, { useEffect, useState } from 'react';
import { Activity, Cpu, Database, RefreshCw, ShieldCheck, Zap } from 'lucide-react';
import { apiClient } from '@/services/api';
import { Button } from '@/components/ui/Button';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/Card';
import { StatCard } from '@/components/ui/StatCard';
import { SystemOverview } from '@/types';

export default function MonitoringPage() {
  const [metrics, setMetrics] = useState<SystemOverview | null>(null);
  const [loading, setLoading] = useState(true);

  const fetchMetrics = async () => {
    setLoading(true);
    try {
      const res = await apiClient.get('/monitoring/overview');
      setMetrics(res.data);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchMetrics();
  }, []);

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-slate-100 tracking-tight">Platform Observability & Metrics</h1>
          <p className="text-sm text-slate-400 mt-1">Prometheus counters, Redis locks, and execution KPIs</p>
        </div>
        <Button variant="outline" size="sm" onClick={fetchMetrics}>
          <RefreshCw className="w-3.5 h-3.5 mr-1.5" /> Refresh
        </Button>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <StatCard
          title="24h Success Rate"
          value={`${metrics?.success_rate_24h ?? 100}%`}
          icon={<ShieldCheck className="w-5 h-5" />}
          description="SLA target: 99.9%"
        />
        <StatCard
          title="Avg Task Duration"
          value={`${metrics?.avg_pipeline_duration_seconds ?? 0}s`}
          icon={<Zap className="w-5 h-5" />}
          description="Vectorized execution engine"
        />
        <StatCard
          title="Active Alerts"
          value={metrics?.active_alert_incidents_count ?? 0}
          icon={<Activity className="w-5 h-5" />}
          description="Open incident investigations"
        />
      </div>

      <Card>
        <CardHeader>
          <CardTitle>Prometheus Metric Endpoints</CardTitle>
        </CardHeader>
        <CardContent className="space-y-3 font-mono text-xs text-slate-300">
          <div className="p-3 rounded bg-slate-950 border border-slate-800 flex justify-between">
            <span className="text-blue-400">GET /metrics</span>
            <span className="text-slate-400">Prometheus exposition format</span>
          </div>
          <div className="p-3 rounded bg-slate-950 border border-slate-800 flex justify-between">
            <span className="text-emerald-400">GET /ready</span>
            <span className="text-slate-400">Kubernetes readiness probe</span>
          </div>
          <div className="p-3 rounded bg-slate-950 border border-slate-800 flex justify-between">
            <span className="text-purple-400">GET /live</span>
            <span className="text-slate-400">Kubernetes liveness probe</span>
          </div>
        </CardContent>
      </Card>
    </div>
  );
}

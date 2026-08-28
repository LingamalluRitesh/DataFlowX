import React, { useEffect, useState } from 'react';
import { useRouter } from 'next/router';
import Link from 'next/link';
import { ArrowLeft, Clock, History, Play, Plus, RefreshCw, Workflow } from 'lucide-react';
import { apiClient } from '@/services/api';
import { Button } from '@/components/ui/Button';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/Card';
import { Badge } from '@/components/ui/Badge';
import { Pipeline } from '@/types';

export default function PipelineDetailPage() {
  const router = useRouter();
  const { id } = router.query;
  const [pipeline, setPipeline] = useState<Pipeline | null>(null);
  const [loading, setLoading] = useState(true);
  const [triggering, setTriggering] = useState(false);
  const [cronExpr, setCronExpr] = useState('0 2 * * *');
  const [addingSchedule, setAddingSchedule] = useState(false);

  const fetchPipeline = async () => {
    if (!id) return;
    try {
      const res = await apiClient.get(`/pipelines/${id}`);
      setPipeline(res.data);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchPipeline();
  }, [id]);

  const handleTrigger = async () => {
    if (!id) return;
    setTriggering(true);
    try {
      const res = await apiClient.post(`/pipelines/${id}/trigger`);
      router.push(`/executions/${res.data.id}`);
    } catch (err: any) {
      alert(`Trigger failed: ${err.response?.data?.detail || err.message}`);
    } finally {
      setTriggering(false);
    }
  };

  const handleAddSchedule = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!id) return;
    setAddingSchedule(true);
    try {
      await apiClient.post(`/pipelines/${id}/schedules`, {
        cron_expression: cronExpr,
        timezone: 'UTC',
        is_enabled: true,
      });
      alert('Schedule added successfully!');
      fetchPipeline();
    } catch (err: any) {
      alert(`Failed to add schedule: ${err.response?.data?.detail || err.message}`);
    } finally {
      setAddingSchedule(false);
    }
  };

  if (loading) return <div>Loading pipeline...</div>;
  if (!pipeline) return <div>Pipeline not found</div>;

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-3">
          <Link href="/pipelines">
            <button className="p-2 rounded-lg bg-slate-900 border border-slate-800 text-slate-400 hover:text-slate-200">
              <ArrowLeft className="w-4 h-4" />
            </button>
          </Link>
          <div>
            <h1 className="text-xl font-bold text-slate-100">{pipeline.name}</h1>
            <div className="flex items-center gap-2 mt-1">
              <Badge variant={pipeline.environment === 'production' ? 'success' : 'neutral'}>
                {pipeline.environment.toUpperCase()}
              </Badge>
              <span className="text-xs text-slate-400 font-mono">Type: {pipeline.pipeline_type}</span>
            </div>
          </div>
        </div>

        <Button variant="success" size="sm" onClick={handleTrigger} isLoading={triggering}>
          <Play className="w-4 h-4 mr-1.5 fill-current" />
          Trigger Immediate Run
        </Button>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <Card className="p-6 space-y-3">
          <span className="text-xs font-bold text-slate-400 uppercase tracking-wider">Concurrency Limit</span>
          <p className="text-2xl font-bold text-slate-100">{pipeline.concurrency_limit} Tasks Parallel</p>
          <p className="text-xs text-slate-400">Timeout: {pipeline.timeout_seconds}s</p>
        </Card>

        <Card className="p-6 space-y-3">
          <span className="text-xs font-bold text-slate-400 uppercase tracking-wider">Retry Policy</span>
          <p className="text-2xl font-bold text-blue-400">{pipeline.retry_count} Max Retries</p>
          <p className="text-xs text-slate-400">Exponential backoff + jitter ({pipeline.retry_delay_seconds}s base)</p>
        </Card>

        <Card className="p-6 space-y-3">
          <span className="text-xs font-bold text-slate-400 uppercase tracking-wider">Active Version</span>
          <p className="text-2xl font-bold text-purple-400">v1.0</p>
          <p className="text-xs text-slate-400">Created: {new Date(pipeline.created_at).toLocaleDateString()}</p>
        </Card>
      </div>

      {/* Scheduler Section */}
      <Card>
        <CardHeader>
          <CardTitle>Automated Execution Schedules (Cron & Interval)</CardTitle>
        </CardHeader>
        <CardContent className="space-y-4">
          <form onSubmit={handleAddSchedule} className="flex gap-4 items-end">
            <div className="flex-1">
              <label className="block text-xs text-slate-400 mb-1 font-semibold">Cron Expression (UTC)</label>
              <input
                type="text"
                value={cronExpr}
                onChange={(e) => setCronExpr(e.target.value)}
                placeholder="0 2 * * *"
                className="w-full px-3.5 py-2 text-xs font-mono bg-slate-950 border border-slate-800 rounded-lg text-slate-100"
              />
            </div>
            <Button type="submit" variant="primary" size="sm" isLoading={addingSchedule}>
              <Clock className="w-4 h-4 mr-1.5" />
              Save Schedule
            </Button>
          </form>
        </CardContent>
      </Card>
    </div>
  );
}

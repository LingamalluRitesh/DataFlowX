import React, { useEffect, useState } from 'react';
import { Cpu, HardDrive, RefreshCw, Server } from 'lucide-react';
import { apiClient } from '@/services/api';
import { Button } from '@/components/ui/Button';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/Card';
import { Badge } from '@/components/ui/Badge';

export default function WorkersPage() {
  const [workers, setWorkers] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);

  const fetchWorkers = async () => {
    setLoading(true);
    try {
      const res = await apiClient.get('/monitoring/workers');
      setWorkers(res.data || []);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchWorkers();
  }, []);

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-slate-100 tracking-tight">Worker Node Cluster</h1>
          <p className="text-sm text-slate-400 mt-1">Distributed Celery worker instances & priority queues</p>
        </div>
        <Button variant="outline" size="sm" onClick={fetchWorkers}>
          <RefreshCw className="w-3.5 h-3.5 mr-1.5" /> Refresh Nodes
        </Button>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        {workers.map((w) => (
          <Card key={w.worker_id} className="p-6 space-y-4">
            <div className="flex items-center justify-between">
              <div className="flex items-center gap-3">
                <div className="p-2.5 rounded-xl bg-blue-500/20 text-blue-400">
                  <Server className="w-5 h-5" />
                </div>
                <div>
                  <h3 className="text-sm font-bold text-slate-100">{w.worker_id}</h3>
                  <p className="text-xs text-slate-400 font-mono">{w.hostname} ({w.ip_address})</p>
                </div>
              </div>
              <Badge variant="success">ACTIVE</Badge>
            </div>

            <div className="grid grid-cols-2 gap-4 pt-2">
              <div className="p-3 rounded-lg bg-slate-950 border border-slate-800">
                <span className="text-[11px] text-slate-400">CPU Usage</span>
                <p className="text-base font-bold text-slate-200 mt-1">{w.cpu_percent}%</p>
              </div>
              <div className="p-3 rounded-lg bg-slate-950 border border-slate-800">
                <span className="text-[11px] text-slate-400">RAM Allocated</span>
                <p className="text-base font-bold text-slate-200 mt-1">{w.memory_used_mb} MB</p>
              </div>
            </div>

            <div>
              <span className="text-[11px] text-slate-400 font-medium">Assigned Priority Queues:</span>
              <div className="flex gap-2 mt-2">
                {w.queues?.map((q: string) => (
                  <span key={q} className="px-2 py-0.5 rounded bg-blue-950/60 border border-blue-800 text-[10px] font-mono text-blue-300">
                    {q}
                  </span>
                ))}
              </div>
            </div>
          </Card>
        ))}
      </div>
    </div>
  );
}

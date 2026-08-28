import React, { useEffect, useState } from 'react';
import { AlertCircle, Bell, CheckCircle2, Plus, RefreshCw, ShieldAlert } from 'lucide-react';
import { apiClient } from '@/services/api';
import { Button } from '@/components/ui/Button';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/Card';
import { Badge } from '@/components/ui/Badge';
import { AlertIncident } from '@/types';

export default function AlertsPage() {
  const [incidents, setIncidents] = useState<AlertIncident[]>([]);
  const [loading, setLoading] = useState(true);

  const fetchAlerts = async () => {
    setLoading(true);
    try {
      const res = await apiClient.get('/monitoring/alerts/incidents');
      setIncidents(res.data || []);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchAlerts();
  }, []);

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-slate-100 tracking-tight">Alerts & Incidents</h1>
          <p className="text-sm text-slate-400 mt-1">Rule definitions, anomaly alerts, and incident response</p>
        </div>
        <Button variant="outline" size="sm" onClick={fetchAlerts}>
          <RefreshCw className="w-3.5 h-3.5 mr-1.5" /> Refresh
        </Button>
      </div>

      <Card>
        <CardHeader>
          <CardTitle>Active & Past Alert Incidents</CardTitle>
        </CardHeader>
        <CardContent className="p-0">
          <table className="w-full text-left text-xs">
            <thead className="bg-slate-900/60 text-slate-400 uppercase tracking-wider border-b border-slate-800">
              <tr>
                <th className="py-3 px-6">Incident Title</th>
                <th className="py-3 px-6">Severity</th>
                <th className="py-3 px-6">Status</th>
                <th className="py-3 px-6">Triggered At</th>
                <th className="py-3 px-6">Description</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-800 text-slate-300">
              {incidents.length === 0 ? (
                <tr>
                  <td colSpan={5} className="text-center py-12 text-slate-500">
                    No open alert incidents. All pipelines and SLAs operating within healthy parameters.
                  </td>
                </tr>
              ) : (
                incidents.map((i) => (
                  <tr key={i.id} className="hover:bg-slate-800/40">
                    <td className="py-3.5 px-6 font-semibold text-slate-100">{i.title}</td>
                    <td className="py-3.5 px-6">
                      <Badge variant={i.severity === 'CRITICAL' ? 'danger' : 'warning'}>{i.severity}</Badge>
                    </td>
                    <td className="py-3.5 px-6">
                      <Badge variant={i.status === 'TRIGGERED' ? 'danger' : 'success'}>{i.status}</Badge>
                    </td>
                    <td className="py-3.5 px-6 text-slate-400">{new Date(i.triggered_at).toLocaleString()}</td>
                    <td className="py-3.5 px-6 text-slate-400">{i.description}</td>
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

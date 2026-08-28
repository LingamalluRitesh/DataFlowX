import React from 'react';
import Head from 'next/head';
import { MainLayout } from '@/components/layout/MainLayout';
import { DataGrid, DataGridColumn } from '@/components/grid/DataGrid';
import { Eye, Activity, AlertTriangle, CheckCircle, Flame, Clock } from 'lucide-react';

interface DataIncidentItem {
  incident_id: string;
  dataset_name: string;
  incident_type: string;
  severity: 'CRITICAL' | 'HIGH' | 'MEDIUM';
  description: string;
  age: string;
  status: 'OPEN' | 'INVESTIGATING' | 'RESOLVED';
}

const mockIncidents: DataIncidentItem[] = [
  { incident_id: 'inc_orders_891', dataset_name: 'gold.fact_orders', incident_type: 'VOLUME_ANOMALY', severity: 'HIGH', description: 'Volume drop: 45,000 rows expected, 12,000 received (Z-score: -3.8σ)', age: '25 mins ago', status: 'INVESTIGATING' },
  { incident_id: 'inc_cust_892', dataset_name: 'silver.dim_customers', incident_type: 'FRESHNESS_BREACH', severity: 'MEDIUM', description: 'Freshness SLA exceeded by 18 minutes (SLA: 60m)', age: '1 hour ago', status: 'OPEN' },
  { incident_id: 'inc_telemetry_893', dataset_name: 'bronze.iot_telemetry', incident_type: 'DISTRIBUTION_DRIFT', severity: 'HIGH', description: 'Distribution drift detected in column "temperature" (Wasserstein distance: 0.18)', age: '3 hours ago', status: 'OPEN' },
];

export default function DataObservabilityPage() {
  const columns: DataGridColumn<DataIncidentItem>[] = [
    { key: 'incident_id', header: 'Incident ID', render: (i) => <strong className="text-cyan-400 font-mono text-xs">{i.incident_id}</strong> },
    { key: 'dataset_name', header: 'Impacted Dataset', render: (i) => <span className="font-mono text-white text-xs">{i.dataset_name}</span> },
    { key: 'incident_type', header: 'Anomaly Category', render: (i) => <span className="bg-slate-800 text-purple-300 font-mono text-[10px] px-2 py-0.5 rounded">{i.incident_type}</span> },
    {
      key: 'severity',
      header: 'Severity',
      render: (i) => (
        <span
          className={`px-2 py-0.5 rounded text-[10px] font-bold ${
            i.severity === 'CRITICAL'
              ? 'bg-red-950 text-red-400 border border-red-800'
              : i.severity === 'HIGH'
              ? 'bg-amber-950 text-amber-400 border border-amber-800'
              : 'bg-cyan-950 text-cyan-400 border border-cyan-800'
          }`}
        >
          {i.severity}
        </span>
      ),
    },
    { key: 'description', header: 'Anomaly Diagnosis', sortable: false },
    { key: 'age', header: 'Opened At' },
    {
      key: 'status',
      header: 'Status',
      render: (i) => (
        <span className="px-2 py-0.5 rounded bg-slate-800 text-slate-300 text-[10px] font-bold">
          {i.status}
        </span>
      ),
    },
  ];

  return (
    <MainLayout>
      <Head>
        <title>Data Observability & Anomaly Incidents — DataFlowX</title>
      </Head>

      <div className="space-y-6">
        <div>
          <h1 className="text-2xl font-bold text-white tracking-tight flex items-center gap-2.5">
            <Eye className="w-7 h-7 text-cyan-400" />
            Data Observability & Continuous Anomaly Detection Hub
          </h1>
          <p className="text-slate-400 text-sm mt-1">
            Automated volume anomaly detection, freshness SLA monitors, and distribution drift analysis across Lakehouse tables.
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <div className="bg-slate-900 border border-slate-800 rounded-xl p-4">
            <div className="text-xs text-slate-500 font-semibold uppercase">Open Data Incidents</div>
            <div className="text-2xl font-bold text-amber-400 mt-1">3 Incidents</div>
          </div>
          <div className="bg-slate-900 border border-slate-800 rounded-xl p-4">
            <div className="text-xs text-slate-500 font-semibold uppercase">Platform Data Uptime</div>
            <div className="text-2xl font-bold text-emerald-400 mt-1">99.94%</div>
          </div>
          <div className="bg-slate-900 border border-slate-800 rounded-xl p-4">
            <div className="text-xs text-slate-500 font-semibold uppercase">Mean Time to Detect (MTTD)</div>
            <div className="text-2xl font-bold text-cyan-400 mt-1">45 Seconds</div>
          </div>
        </div>

        <DataGrid data={mockIncidents} columns={columns} title="Active Data Health Incidents" />
      </div>
    </MainLayout>
  );
}

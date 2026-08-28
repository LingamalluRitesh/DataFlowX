import React from 'react';
import Head from 'next/head';
import { MainLayout } from '@/components/layout/MainLayout';
import { DataGrid, DataGridColumn } from '@/components/grid/DataGrid';
import { Activity, Server, CheckCircle, Database, Layers, ShieldCheck, Zap, Cpu } from 'lucide-react';

interface SubsystemStatusItem {
  subsystem_name: string;
  subsystem_type: 'STORAGE_ENGINE' | 'QUERY_OPTIMIZER' | 'STREAM_PROCESSOR' | 'SECURITY_GOVERNANCE' | 'MLOPS';
  active_instances: number;
  uptime_pct: number;
  p99_latency: string;
  health_state: 'OPTIMAL' | 'DEGRADED';
}

const mockSubsystems: SubsystemStatusItem[] = [
  { subsystem_name: 'Vectorized MPP Execution Engine', subsystem_type: 'QUERY_OPTIMIZER', active_instances: 16, uptime_pct: 100.0, p99_latency: '1.2 ms', health_state: 'OPTIMAL' },
  { subsystem_name: 'Iceberg & Delta Lake Transaction Committers', subsystem_type: 'STORAGE_ENGINE', active_instances: 8, uptime_pct: 100.0, p99_latency: '2.4 ms', health_state: 'OPTIMAL' },
  { subsystem_name: 'Two-Stacks (DABA) Sliding Window & CEP Engine', subsystem_type: 'STREAM_PROCESSOR', active_instances: 12, uptime_pct: 99.99, p99_latency: '0.8 ms', health_state: 'OPTIMAL' },
  { subsystem_name: 'HNSW & IVF-PQ Vector Graph Search Clusters', subsystem_type: 'MLOPS', active_instances: 6, uptime_pct: 100.0, p99_latency: '0.9 ms', health_state: 'OPTIMAL' },
  { subsystem_name: 'Row-Level Security & Differential Privacy Noise Generator', subsystem_type: 'SECURITY_GOVERNANCE', active_instances: 4, uptime_pct: 100.0, p99_latency: '0.1 ms', health_state: 'OPTIMAL' },
];

export default function SystemStatusPage() {
  const columns: DataGridColumn<SubsystemStatusItem>[] = [
    {
      key: 'subsystem_name',
      header: 'Subsystem Component',
      render: (s) => (
        <div className="flex items-center gap-2">
          <Server className="w-4 h-4 text-cyan-400" />
          <strong className="text-white font-mono text-xs">{s.subsystem_name}</strong>
        </div>
      ),
    },
    {
      key: 'subsystem_type',
      header: 'Domain Category',
      render: (s) => <span className="bg-slate-800 text-purple-300 font-mono text-[10px] px-2 py-0.5 rounded font-bold">{s.subsystem_type}</span>,
    },
    { key: 'active_instances', header: 'Active Workers', render: (s) => <span className="font-mono text-slate-300">{s.active_instances} nodes</span> },
    {
      key: 'uptime_pct',
      header: '30-Day SLA Uptime',
      render: (s) => <span className="font-mono text-emerald-400 font-bold">{s.uptime_pct.toFixed(2)}%</span>,
    },
    {
      key: 'p99_latency',
      header: 'P99 Latency',
      render: (s) => <span className="font-mono text-cyan-300 font-bold">{s.p99_latency}</span>,
    },
    {
      key: 'health_state',
      header: 'System State',
      render: (s) => (
        <span className="px-2 py-0.5 rounded bg-emerald-950 text-emerald-400 border border-emerald-800 text-[10px] font-bold">
          {s.health_state}
        </span>
      ),
    },
  ];

  return (
    <MainLayout>
      <Head>
        <title>Unified System Diagnostics & Subsystem Health — DataFlowX</title>
      </Head>

      <div className="space-y-6">
        <div>
          <h1 className="text-2xl font-bold text-white tracking-tight flex items-center gap-2.5">
            <Activity className="w-7 h-7 text-cyan-400" />
            Unified Engine Diagnostics & Subsystem Architecture Health
          </h1>
          <p className="text-slate-400 text-sm mt-1">
            Global monitoring dashboard tracking Lakehouse storage backends, vectorized query execution kernels, and stream processing workers.
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <div className="bg-slate-900 border border-slate-800 rounded-xl p-4">
            <div className="text-xs text-slate-500 font-semibold uppercase">Global System Status</div>
            <div className="text-2xl font-bold text-emerald-400 mt-1">All Systems Operational</div>
          </div>
          <div className="bg-slate-900 border border-slate-800 rounded-xl p-4">
            <div className="text-xs text-slate-500 font-semibold uppercase">Total Distributed Cores</div>
            <div className="text-2xl font-bold text-white mt-1">46 Cores Active</div>
          </div>
          <div className="bg-slate-900 border border-slate-800 rounded-xl p-4">
            <div className="text-xs text-slate-500 font-semibold uppercase">Cluster Consensus</div>
            <div className="text-2xl font-bold text-cyan-400 mt-1">Quorum Healthy</div>
          </div>
        </div>

        <DataGrid data={mockSubsystems} columns={columns} title="Core Platform Subsystem Status" />
      </div>
    </MainLayout>
  );
}

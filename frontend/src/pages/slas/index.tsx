import React from 'react';
import Head from 'next/head';
import { MainLayout } from '@/components/layout/MainLayout';
import { DataGrid, DataGridColumn } from '@/components/grid/DataGrid';
import { ThroughputSlaGauge } from '@/components/charts/ThroughputSlaGauge';
import { ComplianceScorecard } from '@/components/charts/ComplianceScorecard';
import { Clock, ShieldCheck, AlertTriangle, CheckCircle, Activity, Zap } from 'lucide-react';

interface SLAMonitorItem {
  id: string;
  pipeline_name: string;
  sla_target_duration_mins: number;
  last_run_duration_mins: number;
  availability_target_pct: number;
  actual_availability_pct: number;
  breach_risk: 'LOW' | 'MEDIUM' | 'HIGH';
}

const mockSlaMonitors: SLAMonitorItem[] = [
  { id: 'sla_01', pipeline_name: 'etl_daily_gold_aggregator', sla_target_duration_mins: 60, last_run_duration_mins: 42, availability_target_pct: 99.9, actual_availability_pct: 99.95, breach_risk: 'LOW' },
  { id: 'sla_02', pipeline_name: 'stream_clickstream_events', sla_target_duration_mins: 5, last_run_duration_mins: 4.8, availability_target_pct: 99.99, actual_availability_pct: 99.98, breach_risk: 'MEDIUM' },
  { id: 'sla_03', pipeline_name: 'cdc_wal_bronze_stream', sla_target_duration_mins: 2, last_run_duration_mins: 1.2, availability_target_pct: 99.9, actual_availability_pct: 100.0, breach_risk: 'LOW' },
];

export default function SLAMonitorPage() {
  const columns: DataGridColumn<SLAMonitorItem>[] = [
    {
      key: 'pipeline_name',
      header: 'Monitored Pipeline',
      render: (s) => (
        <div>
          <strong className="text-white font-mono">{s.pipeline_name}</strong>
          <div className="text-[10px] text-slate-500 font-mono">{s.id}</div>
        </div>
      ),
    },
    {
      key: 'last_run_duration_mins',
      header: 'Execution SLA (Target vs Actual)',
      render: (s) => (
        <span className="font-mono text-slate-300">
          <span className="text-cyan-300 font-bold">{s.last_run_duration_mins}m</span> / {s.sla_target_duration_mins}m target
        </span>
      ),
    },
    {
      key: 'actual_availability_pct',
      header: 'Availability Uptime',
      render: (s) => <span className="font-mono text-emerald-400 font-bold">{s.actual_availability_pct}%</span>,
    },
    {
      key: 'breach_risk',
      header: 'Breach Risk Level',
      render: (s) => (
        <span
          className={`px-2 py-0.5 rounded text-[10px] font-bold ${
            s.breach_risk === 'LOW'
              ? 'bg-emerald-950 text-emerald-400 border border-emerald-800'
              : 'bg-amber-950 text-amber-400 border border-amber-800'
          }`}
        >
          {s.breach_risk} RISK
        </span>
      ),
    },
  ];

  return (
    <MainLayout>
      <Head>
        <title>SLA & Reliability Monitoring — DataFlowX</title>
      </Head>

      <div className="space-y-6">
        <div>
          <h1 className="text-2xl font-bold text-white tracking-tight flex items-center gap-2.5">
            <Clock className="w-7 h-7 text-cyan-400" />
            SLA Adherence & Reliability Monitoring Hub
          </h1>
          <p className="text-slate-400 text-sm mt-1">
            Track execution deadline adherence, availability SLAs, breach risks, and automated escalation triggers.
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <ThroughputSlaGauge currentThroughputEps={48500} slaTargetEps={50000} />
          <div className="bg-slate-900 border border-slate-800 rounded-xl p-5 shadow-lg flex flex-col justify-between">
            <div className="text-xs text-slate-500 font-semibold uppercase">Platform-Wide SLA Adherence (Trailing 30d)</div>
            <div className="text-4xl font-extrabold text-emerald-400 mt-2">99.98%</div>
            <div className="text-xs text-slate-400 mt-2">242 of 243 pipeline DAG runs completed within deadline window.</div>
          </div>
        </div>

        <ComplianceScorecard />

        <DataGrid data={mockSlaMonitors} columns={columns} title="Pipeline SLA Tracking Matrix" />
      </div>
    </MainLayout>
  );
}

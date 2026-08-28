import React from 'react';
import Head from 'next/head';
import { MainLayout } from '@/components/layout/MainLayout';
import { DataGrid, DataGridColumn } from '@/components/grid/DataGrid';
import { PlayCircle, Activity, CheckCircle, Clock, AlertTriangle, RefreshCw, GitCommit } from 'lucide-react';

interface PipelineRunInstanceItem {
  run_id: string;
  pipeline_name: string;
  current_state: 'RUNNING' | 'SUCCESS' | 'FAILED' | 'QUEUED' | 'RETRYING';
  transition_count: number;
  duration_seconds: number;
  initiated_by: string;
}

const mockRuns: PipelineRunInstanceItem[] = [
  { run_id: 'run_gold_agg_172488', pipeline_name: 'etl_daily_gold_aggregator', current_state: 'SUCCESS', transition_count: 3, duration_seconds: 42.5, initiated_by: 'CRON_SCHEDULER' },
  { run_id: 'run_stream_click_172489', pipeline_name: 'stream_clickstream_events', current_state: 'RUNNING', transition_count: 2, duration_seconds: 180.0, initiated_by: 'KAFKA_TRIGGER' },
  { run_id: 'run_cdc_wal_172490', pipeline_name: 'cdc_wal_bronze_stream', current_state: 'RETRYING', transition_count: 4, duration_seconds: 15.2, initiated_by: 'WEBHOOK' },
];

export default function PipelineStateMachinePage() {
  const columns: DataGridColumn<PipelineRunInstanceItem>[] = [
    { key: 'run_id', header: 'Run Instance ID', render: (r) => <strong className="text-cyan-400 font-mono text-xs">{r.run_id}</strong> },
    { key: 'pipeline_name', header: 'Target Pipeline', render: (r) => <span className="font-mono text-white text-xs">{r.pipeline_name}</span> },
    {
      key: 'current_state',
      header: 'FSM Execution State',
      render: (r) => (
        <span
          className={`px-2 py-0.5 rounded text-[10px] font-bold ${
            r.current_state === 'SUCCESS'
              ? 'bg-emerald-950 text-emerald-400 border border-emerald-800'
              : r.current_state === 'RUNNING'
              ? 'bg-cyan-950 text-cyan-400 border border-cyan-800 animate-pulse'
              : 'bg-amber-950 text-amber-400 border border-amber-800'
          }`}
        >
          {r.current_state}
        </span>
      ),
    },
    { key: 'transition_count', header: 'Transitions', render: (r) => <span className="font-mono text-slate-300">{r.transition_count} transitions</span> },
    { key: 'duration_seconds', header: 'Elapsed Duration', render: (r) => <span className="font-mono text-purple-300">{r.duration_seconds}s</span> },
    { key: 'initiated_by', header: 'Trigger Source', render: (r) => <span className="bg-slate-800 text-slate-300 font-mono text-[10px] px-2 py-0.5 rounded">{r.initiated_by}</span> },
  ];

  return (
    <MainLayout>
      <Head>
        <title>Pipeline State Machine & FSM — DataFlowX</title>
      </Head>

      <div className="space-y-6">
        <div>
          <h1 className="text-2xl font-bold text-white tracking-tight flex items-center gap-2.5">
            <PlayCircle className="w-7 h-7 text-cyan-400" />
            Pipeline State Machine & Execution Coordinator
          </h1>
          <p className="text-slate-400 text-sm mt-1">
            Deterministic finite state machine governing pipeline execution lifecycles, dynamic task mapping, and retry policies.
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <div className="bg-slate-900 border border-slate-800 rounded-xl p-4">
            <div className="text-xs text-slate-500 font-semibold uppercase">Active Executing Runs</div>
            <div className="text-2xl font-bold text-cyan-400 mt-1">1 Running Run</div>
          </div>
          <div className="bg-slate-900 border border-slate-800 rounded-xl p-4">
            <div className="text-xs text-slate-500 font-semibold uppercase">Successful Completions (24h)</div>
            <div className="text-2xl font-bold text-emerald-400 mt-1">142 Runs</div>
          </div>
          <div className="bg-slate-900 border border-slate-800 rounded-xl p-4">
            <div className="text-xs text-slate-500 font-semibold uppercase">State Transition Accuracy</div>
            <div className="text-2xl font-bold text-white mt-1">100.0% Audited</div>
          </div>
        </div>

        <DataGrid data={mockRuns} columns={columns} title="Pipeline FSM Run Instances" />
      </div>
    </MainLayout>
  );
}

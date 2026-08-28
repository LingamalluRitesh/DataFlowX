import React from 'react';
import Head from 'next/head';
import { MainLayout } from '@/components/layout/MainLayout';
import { DataGrid, DataGridColumn } from '@/components/grid/DataGrid';
import { GitBranch, Activity, CheckCircle, Clock, Server, ArrowUpRight, Share2 } from 'lucide-react';

interface OpenLineageEventItem {
  event_id: string;
  event_type: 'START' | 'RUNNING' | 'COMPLETE' | 'FAIL';
  job_name: string;
  run_id: string;
  inputs_count: number;
  outputs_count: number;
  event_time: string;
}

const mockLineageEvents: OpenLineageEventItem[] = [
  { event_id: 'evt_ol_9841', event_type: 'COMPLETE', job_name: 'etl_daily_gold_aggregator', run_id: 'run_68d19a4e', inputs_count: 2, outputs_count: 1, event_time: '2 mins ago' },
  { event_id: 'evt_ol_9840', event_type: 'START', job_name: 'etl_daily_gold_aggregator', run_id: 'run_68d19a4e', inputs_count: 2, outputs_count: 1, event_time: '5 mins ago' },
  { event_id: 'evt_ol_9839', event_type: 'COMPLETE', job_name: 'cdc_wal_bronze_stream', run_id: 'run_12f9b8c0', inputs_count: 1, outputs_count: 1, event_time: '12 mins ago' },
];

export default function OpenLineageIndexPage() {
  const columns: DataGridColumn<OpenLineageEventItem>[] = [
    {
      key: 'job_name',
      header: 'OpenLineage Job',
      render: (e) => (
        <div>
          <strong className="text-white font-mono">{e.job_name}</strong>
          <div className="text-[10px] text-slate-500 font-mono">runId: {e.run_id}</div>
        </div>
      ),
    },
    {
      key: 'event_type',
      header: 'Event Type',
      render: (e) => (
        <span
          className={`px-2 py-0.5 rounded text-[10px] font-bold ${
            e.event_type === 'COMPLETE'
              ? 'bg-emerald-950 text-emerald-400 border border-emerald-800'
              : e.event_type === 'START'
              ? 'bg-cyan-950 text-cyan-400 border border-cyan-800'
              : 'bg-red-950 text-red-400 border border-red-800'
          }`}
        >
          {e.event_type}
        </span>
      ),
    },
    {
      key: 'inputs_count',
      header: 'Input Datasets',
      render: (e) => <span className="font-mono text-slate-300">{e.inputs_count} inputs</span>,
    },
    {
      key: 'outputs_count',
      header: 'Output Datasets',
      render: (e) => <span className="font-mono text-cyan-400">{e.outputs_count} outputs</span>,
    },
    { key: 'event_time', header: 'Timestamp' },
  ];

  return (
    <MainLayout>
      <Head>
        <title>OpenLineage Event Stream — DataFlowX</title>
      </Head>

      <div className="space-y-6">
        <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
          <div>
            <h1 className="text-2xl font-bold text-white tracking-tight flex items-center gap-2.5">
              <Share2 className="w-7 h-7 text-cyan-400" />
              OpenLineage & Marquez Standards Telemetry
            </h1>
            <p className="text-slate-400 text-sm mt-1">
              JSON-LD RunEvent stream emission for cross-platform data lineage interoperability across Marquez, Collibra, and DataHub.
            </p>
          </div>

          <span className="px-3 py-1 rounded-lg bg-slate-900 border border-slate-800 text-xs text-slate-300 font-mono self-start md:self-auto">
            OpenLineage Spec: v1.0.2
          </span>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <div className="bg-slate-900 border border-slate-800 rounded-xl p-4">
            <div className="text-xs text-slate-500 font-semibold uppercase">Total Lineage Events Emitted</div>
            <div className="text-2xl font-bold text-white mt-1">45,210 Events</div>
          </div>
          <div className="bg-slate-900 border border-slate-800 rounded-xl p-4">
            <div className="text-xs text-slate-500 font-semibold uppercase">Active Connected Lineage Backends</div>
            <div className="text-2xl font-bold text-emerald-400 mt-1">Marquez Server</div>
          </div>
          <div className="bg-slate-900 border border-slate-800 rounded-xl p-4">
            <div className="text-xs text-slate-500 font-semibold uppercase">Cross-Table Edges Tracked</div>
            <div className="text-2xl font-bold text-cyan-400 mt-1">128 Edges</div>
          </div>
        </div>

        <DataGrid data={mockLineageEvents} columns={columns} title="Live OpenLineage Telemetry Feed" />
      </div>
    </MainLayout>
  );
}

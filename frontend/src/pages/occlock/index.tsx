import React from 'react';
import Head from 'next/head';
import { MainLayout } from '@/components/layout/MainLayout';
import { DataGrid, DataGridColumn } from '@/components/grid/DataGrid';
import { Lock, ShieldCheck, CheckCircle, Database, Layers, ArrowRight } from 'lucide-react';

interface OCCCommitItem {
  table_name: string;
  expected_version: number;
  committed_version: number;
  committer_id: string;
  cas_retry_count: number;
  conflict_detected: boolean;
  status: 'COMMITTED' | 'CONFLICT_RETRY';
}

const mockOCC: OCCCommitItem[] = [
  { table_name: 'gold.fact_orders', expected_version: 141, committed_version: 142, committer_id: 'spark_batch_writer_01', cas_retry_count: 0, conflict_detected: false, status: 'COMMITTED' },
  { table_name: 'gold.fact_orders', expected_version: 141, committed_version: 143, committer_id: 'streaming_sink_worker_04', cas_retry_count: 1, conflict_detected: true, status: 'COMMITTED' },
  { table_name: 'silver.dim_customers', expected_version: 88, committed_version: 89, committer_id: 'cdc_ingest_pipeline_02', cas_retry_count: 0, conflict_detected: false, status: 'COMMITTED' },
];

export default function OCCLockStudioPage() {
  const columns: DataGridColumn<OCCCommitItem>[] = [
    { key: 'table_name', header: 'Target Table', render: (o) => <strong className="text-white font-mono text-xs">{o.table_name}</strong> },
    {
      key: 'committed_version',
      header: 'Committed Version (CAS)',
      render: (o) => <span className="font-mono text-cyan-300 font-bold">v{o.committed_version}</span>,
    },
    { key: 'committer_id', header: 'Distributed Committer', render: (o) => <span className="font-mono text-slate-300 text-xs">{o.committer_id}</span> },
    {
      key: 'cas_retry_count',
      header: 'CAS Retries',
      render: (o) => <span className="bg-slate-800 text-purple-300 font-mono text-[10px] px-2 py-0.5 rounded">{o.cas_retry_count} Retries</span>,
    },
    {
      key: 'conflict_detected',
      header: 'Conflict Auto-Resolution',
      render: (o) => (
        <span
          className={`px-2 py-0.5 rounded text-[10px] font-bold ${
            o.conflict_detected ? 'bg-amber-950 text-amber-400' : 'bg-emerald-950 text-emerald-400 border border-emerald-800'
          }`}
        >
          {o.conflict_detected ? 'CONFLICT RESOLVED' : 'CLEAN WRITE'}
        </span>
      ),
    },
    {
      key: 'status',
      header: 'Commit State',
      render: (o) => (
        <span className="px-2 py-0.5 rounded bg-emerald-950 text-emerald-400 border border-emerald-800 text-[10px] font-bold">
          {o.status}
        </span>
      ),
    },
  ];

  return (
    <MainLayout>
      <Head>
        <title>Optimistic Concurrency Control (OCC) — DataFlowX</title>
      </Head>

      <div className="space-y-6">
        <div>
          <h1 className="text-2xl font-bold text-white tracking-tight flex items-center gap-2.5">
            <Lock className="w-7 h-7 text-cyan-400" />
            Optimistic Concurrency Control (OCC) Multi-Writer Studio
          </h1>
          <p className="text-slate-400 text-sm mt-1">
            Compare-and-Swap (CAS) table metadata sequencer resolving concurrent distributed commits with automatic retries and conflict rebasing.
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <div className="bg-slate-900 border border-slate-800 rounded-xl p-4">
            <div className="text-xs text-slate-500 font-semibold uppercase">Total Committed Versions (24h)</div>
            <div className="text-2xl font-bold text-white mt-1">2,450 Commits</div>
          </div>
          <div className="bg-slate-900 border border-slate-800 rounded-xl p-4">
            <div className="text-xs text-slate-500 font-semibold uppercase">CAS Conflict Auto-Resolution Rate</div>
            <div className="text-2xl font-bold text-emerald-400 mt-1">100% Resolved</div>
          </div>
          <div className="bg-slate-900 border border-slate-800 rounded-xl p-4">
            <div className="text-xs text-slate-500 font-semibold uppercase">Average Commit Latency</div>
            <div className="text-2xl font-bold text-cyan-400 mt-1">1.8 ms / commit</div>
          </div>
        </div>

        <DataGrid data={mockOCC} columns={columns} title="Managed OCC Distributed Table Commits" />
      </div>
    </MainLayout>
  );
}

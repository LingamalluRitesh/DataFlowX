import React from 'react';
import Head from 'next/head';
import { MainLayout } from '@/components/layout/MainLayout';
import { DataGrid, DataGridColumn } from '@/components/grid/DataGrid';
import { FileCode, Database, CheckCircle, Clock, Layers, ArrowRight } from 'lucide-react';

interface DeltaCommitItem {
  version: number;
  timestamp: string;
  operation: string;
  files_added: number;
  files_removed: number;
  bytes_added_mb: number;
  committed_by: string;
}

const mockDeltaCommits: DeltaCommitItem[] = [
  { version: 142, timestamp: '2026-08-29 00:24:12 UTC', operation: 'MERGE (Upsert)', files_added: 4, files_removed: 2, bytes_added_mb: 48.5, committed_by: 'pipeline_gold_orders' },
  { version: 141, timestamp: '2026-08-29 00:20:00 UTC', operation: 'OPTIMIZE (Z-Order by customer_id)', files_added: 8, files_removed: 32, bytes_added_mb: 120.0, committed_by: 'compaction_scheduler_job' },
  { version: 140, timestamp: '2026-08-29 00:15:45 UTC', operation: 'WRITE (Append Batch)', files_added: 2, files_removed: 0, bytes_added_mb: 24.2, committed_by: 'streaming_ingestion_worker' },
];

export default function DeltaLogReplayerPage() {
  const columns: DataGridColumn<DeltaCommitItem>[] = [
    {
      key: 'version',
      header: 'Delta Version',
      render: (d) => <span className="font-mono text-cyan-300 font-bold">v{d.version}</span>,
    },
    { key: 'timestamp', header: 'Commit Timestamp', render: (d) => <span className="font-mono text-slate-300 text-xs">{d.timestamp}</span> },
    {
      key: 'operation',
      header: 'Delta Operation',
      render: (d) => <span className="bg-slate-800 text-purple-300 font-mono text-[10px] px-2 py-0.5 rounded">{d.operation}</span>,
    },
    {
      key: 'files_added',
      header: 'File Diffs (+ / -)',
      render: (d) => (
        <span className="font-mono text-xs">
          <span className="text-emerald-400 font-bold">+{d.files_added}</span> / <span className="text-red-400 font-bold">-{d.files_removed}</span>
        </span>
      ),
    },
    {
      key: 'bytes_added_mb',
      header: 'Data Change Volume',
      render: (d) => <span className="font-mono text-emerald-400 font-bold">{d.bytes_added_mb.toFixed(1)} MB</span>,
    },
    { key: 'committed_by', header: 'Engine / Committer', render: (d) => <span className="font-mono text-slate-300 text-xs">{d.committed_by}</span> },
  ];

  return (
    <MainLayout>
      <Head>
        <title>Delta Lake Transaction Log Replayer — DataFlowX</title>
      </Head>

      <div className="space-y-6">
        <div>
          <h1 className="text-2xl font-bold text-white tracking-tight flex items-center gap-2.5">
            <FileCode className="w-7 h-7 text-cyan-400" />
            Delta Lake Transaction Log (`_delta_log`) & Checkpoint Replayer
          </h1>
          <p className="text-slate-400 text-sm mt-1">
            ACID transaction log commit inspection, AddFile / RemoveFile action compaction, and time-travel state reconstruction.
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <div className="bg-slate-900 border border-slate-800 rounded-xl p-4">
            <div className="text-xs text-slate-500 font-semibold uppercase">Current Table Version</div>
            <div className="text-2xl font-bold text-white mt-1">v142 (Committed)</div>
          </div>
          <div className="bg-slate-900 border border-slate-800 rounded-xl p-4">
            <div className="text-xs text-slate-500 font-semibold uppercase">Active Parquet Data Files</div>
            <div className="text-2xl font-bold text-emerald-400 mt-1">128 Active Files</div>
          </div>
          <div className="bg-slate-900 border border-slate-800 rounded-xl p-4">
            <div className="text-xs text-slate-500 font-semibold uppercase">Last Checkpoint Version</div>
            <div className="text-2xl font-bold text-cyan-400 mt-1">v140.checkpoint.parquet</div>
          </div>
        </div>

        <DataGrid data={mockDeltaCommits} columns={columns} title="Delta Lake JSON Commit History" />
      </div>
    </MainLayout>
  );
}

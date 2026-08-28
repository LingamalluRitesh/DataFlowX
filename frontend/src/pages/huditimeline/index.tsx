import React from 'react';
import Head from 'next/head';
import { MainLayout } from '@/components/layout/MainLayout';
import { DataGrid, DataGridColumn } from '@/components/grid/DataGrid';
import { GitCommit, Clock, CheckCircle, Database, Layers, ArrowRight } from 'lucide-react';

interface HudiInstantItem {
  timestamp: string;
  action: 'COMMIT' | 'DELTACOMMIT' | 'COMPACTION' | 'CLEAN' | 'ROLLBACK';
  state: 'COMPLETED' | 'INFLIGHT' | 'REQUESTED';
  duration_seconds: number;
  files_written: number;
  records_written: number;
}

const mockHudi: HudiInstantItem[] = [
  { timestamp: '20260829002410', action: 'DELTACOMMIT', state: 'COMPLETED', duration_seconds: 4.2, files_written: 3, records_written: 15400 },
  { timestamp: '20260829002000', action: 'COMPACTION', state: 'COMPLETED', duration_seconds: 48.0, files_written: 12, records_written: 250000 },
  { timestamp: '20260829001500', action: 'CLEAN', state: 'COMPLETED', duration_seconds: 8.5, files_written: 0, records_written: 0 },
  { timestamp: '20260829001000', action: 'COMMIT', state: 'COMPLETED', duration_seconds: 12.0, files_written: 6, records_written: 84000 },
];

export default function HudiTimelinePage() {
  const columns: DataGridColumn<HudiInstantItem>[] = [
    {
      key: 'timestamp',
      header: 'Hudi Instant Timestamp',
      render: (h) => (
        <div className="flex items-center gap-2">
          <GitCommit className="w-4 h-4 text-cyan-400" />
          <strong className="text-white font-mono text-xs">{h.timestamp}</strong>
        </div>
      ),
    },
    {
      key: 'action',
      header: 'Timeline Action',
      render: (h) => <span className="bg-slate-800 text-purple-300 font-mono text-[10px] px-2 py-0.5 rounded">{h.action}</span>,
    },
    {
      key: 'state',
      header: 'Instant State',
      render: (h) => (
        <span
          className={`px-2 py-0.5 rounded text-[10px] font-bold ${
            h.state === 'COMPLETED'
              ? 'bg-emerald-950 text-emerald-400 border border-emerald-800'
              : 'bg-amber-950 text-amber-400'
          }`}
        >
          {h.state}
        </span>
      ),
    },
    { key: 'duration_seconds', header: 'Execution Duration', render: (h) => <span className="font-mono text-slate-300">{h.duration_seconds.toFixed(1)}s</span> },
    { key: 'files_written', header: 'Files Written', render: (h) => <span className="font-mono text-cyan-300">+{h.files_written} files</span> },
    {
      key: 'records_written',
      header: 'Records Ingested',
      render: (h) => <span className="font-mono text-emerald-400 font-bold">{h.records_written.toLocaleString()} rows</span>,
    },
  ];

  return (
    <MainLayout>
      <Head>
        <title>Apache Hudi Commit Timeline — DataFlowX</title>
      </Head>

      <div className="space-y-6">
        <div>
          <h1 className="text-2xl font-bold text-white tracking-tight flex items-center gap-2.5">
            <GitCommit className="w-7 h-7 text-cyan-400" />
            Apache Hudi Commit Timeline & Instant State Machine
          </h1>
          <p className="text-slate-400 text-sm mt-1">
            Tracking of `.hoodie` commit instants, deltacommit log appends, MOR compaction schedules, and clean operations.
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <div className="bg-slate-900 border border-slate-800 rounded-xl p-4">
            <div className="text-xs text-slate-500 font-semibold uppercase">Latest Active Instant</div>
            <div className="text-2xl font-bold text-white mt-1">20260829002410</div>
          </div>
          <div className="bg-slate-900 border border-slate-800 rounded-xl p-4">
            <div className="text-xs text-slate-500 font-semibold uppercase">Table Storage Type</div>
            <div className="text-2xl font-bold text-emerald-400 mt-1">Merge-On-Read (MOR)</div>
          </div>
          <div className="bg-slate-900 border border-slate-800 rounded-xl p-4">
            <div className="text-xs text-slate-500 font-semibold uppercase">Compaction Health</div>
            <div className="text-2xl font-bold text-cyan-400 mt-1">100% Up-To-Date</div>
          </div>
        </div>

        <DataGrid data={mockHudi} columns={columns} title="Hudi Active Timeline Instants" />
      </div>
    </MainLayout>
  );
}

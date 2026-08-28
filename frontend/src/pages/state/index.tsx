import React from 'react';
import Head from 'next/head';
import { MainLayout } from '@/components/layout/MainLayout';
import { DataGrid, DataGridColumn } from '@/components/grid/DataGrid';
import { Database, Save, CheckCircle, Activity, HardDrive, RefreshCw } from 'lucide-react';

interface StateCheckpointItem {
  checkpoint_id: number;
  operator_id: string;
  total_keys: number;
  size_kb: number;
  duration_ms: number;
  status: 'COMPLETED' | 'IN_PROGRESS';
}

const mockCheckpoints: StateCheckpointItem[] = [
  { checkpoint_id: 104, operator_id: 'session_window_aggregator', total_keys: 18450, size_kb: 1180, duration_ms: 24.2, status: 'COMPLETED' },
  { checkpoint_id: 103, operator_id: 'session_window_aggregator', total_keys: 18120, size_kb: 1160, duration_ms: 22.8, status: 'COMPLETED' },
  { checkpoint_id: 102, operator_id: 'session_window_aggregator', total_keys: 17800, size_kb: 1140, duration_ms: 25.1, status: 'COMPLETED' },
];

export default function StreamingStatePage() {
  const columns: DataGridColumn<StateCheckpointItem>[] = [
    { key: 'checkpoint_id', header: 'Checkpoint ID', render: (c) => <strong className="text-cyan-400 font-mono">chk_{c.checkpoint_id}</strong> },
    { key: 'operator_id', header: 'Streaming Operator', render: (c) => <span className="font-mono text-white">{c.operator_id}</span> },
    { key: 'total_keys', header: 'Keyed States', render: (c) => <span className="font-mono text-emerald-400 font-bold">{c.total_keys.toLocaleString()} keys</span> },
    { key: 'size_kb', header: 'Snapshot Size', render: (c) => <span className="font-mono text-purple-400">{c.size_kb} KB</span> },
    { key: 'duration_ms', header: 'Sync Duration', render: (c) => <span className="font-mono text-slate-300">{c.duration_ms} ms</span> },
    {
      key: 'status',
      header: 'Status',
      render: (c) => (
        <span className="px-2 py-0.5 rounded bg-emerald-950 text-emerald-400 border border-emerald-800 text-[10px] font-bold">
          {c.status}
        </span>
      ),
    },
  ];

  return (
    <MainLayout>
      <Head>
        <title>Streaming State Backend & Checkpoints — DataFlowX</title>
      </Head>

      <div className="space-y-6">
        <div>
          <h1 className="text-2xl font-bold text-white tracking-tight flex items-center gap-2.5">
            <Save className="w-7 h-7 text-cyan-400" />
            Streaming RocksDB State Backend & Checkpoint Inspector
          </h1>
          <p className="text-slate-400 text-sm mt-1">
            Incremental asynchronous state snapshotting and write-ahead log replay for exactly-once fault recovery.
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <div className="bg-slate-900 border border-slate-800 rounded-xl p-4">
            <div className="text-xs text-slate-500 font-semibold uppercase">Total Active Keyed States</div>
            <div className="text-2xl font-bold text-white mt-1">18,450 Keys</div>
          </div>
          <div className="bg-slate-900 border border-slate-800 rounded-xl p-4">
            <div className="text-xs text-slate-500 font-semibold uppercase">Avg Checkpoint Sync Latency</div>
            <div className="text-2xl font-bold text-emerald-400 mt-1">23.5 ms</div>
          </div>
          <div className="bg-slate-900 border border-slate-800 rounded-xl p-4">
            <div className="text-xs text-slate-500 font-semibold uppercase">Checkpoint Frequency</div>
            <div className="text-2xl font-bold text-cyan-400 mt-1">Every 10 Seconds</div>
          </div>
        </div>

        <DataGrid data={mockCheckpoints} columns={columns} title="Streaming Checkpoint Audit History" />
      </div>
    </MainLayout>
  );
}

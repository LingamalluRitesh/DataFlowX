import React from 'react';
import Head from 'next/head';
import { MainLayout } from '@/components/layout/MainLayout';
import { DataGrid, DataGridColumn } from '@/components/grid/DataGrid';
import { CheckCircle2, ShieldCheck, Clock, Layers, HardDrive, Zap } from 'lucide-react';

interface CheckpointSnapshotItem {
  checkpoint_id: number;
  trigger_type: 'PERIODIC_BARRIER' | 'SAVEPOINT_MANUAL';
  total_state_size_mb: number;
  alignment_duration_ms: number;
  completed_operators: string;
  storage_location: string;
  status: 'COMPLETED' | 'IN_PROGRESS';
}

const mockCheckpoints: CheckpointSnapshotItem[] = [
  { checkpoint_id: 1420, trigger_type: 'PERIODIC_BARRIER', total_state_size_mb: 272.7, alignment_duration_ms: 18, completed_operators: '12 / 12 (100%)', storage_location: 's3://lakehouse-checkpoints/chk-1420/', status: 'COMPLETED' },
  { checkpoint_id: 1419, trigger_type: 'PERIODIC_BARRIER', total_state_size_mb: 271.9, alignment_duration_ms: 22, completed_operators: '12 / 12 (100%)', storage_location: 's3://lakehouse-checkpoints/chk-1419/', status: 'COMPLETED' },
  { checkpoint_id: 1418, trigger_type: 'SAVEPOINT_MANUAL', total_state_size_mb: 271.5, alignment_duration_ms: 25, completed_operators: '12 / 12 (100%)', storage_location: 's3://lakehouse-checkpoints/savepoint-1418/', status: 'COMPLETED' },
];

export default function CheckpointsMonitorPage() {
  const columns: DataGridColumn<CheckpointSnapshotItem>[] = [
    {
      key: 'checkpoint_id',
      header: 'Checkpoint ID',
      render: (c) => (
        <span className="font-mono text-cyan-300 font-bold flex items-center gap-1.5">
          <CheckCircle2 className="w-3.5 h-3.5 text-emerald-400" /> #{c.checkpoint_id}
        </span>
      ),
    },
    {
      key: 'trigger_type',
      header: 'Snapshot Trigger',
      render: (c) => <span className="bg-slate-800 text-purple-300 font-mono text-[10px] px-2 py-0.5 rounded">{c.trigger_type}</span>,
    },
    {
      key: 'total_state_size_mb',
      header: 'State Snapshot Size',
      render: (c) => <span className="font-mono text-emerald-400 font-bold">{c.total_state_size_mb} MB</span>,
    },
    {
      key: 'alignment_duration_ms',
      header: 'Barrier Alignment',
      render: (c) => <span className="font-mono text-cyan-300 font-bold">{c.alignment_duration_ms} ms</span>,
    },
    { key: 'completed_operators', header: 'Operator Acks', render: (c) => <span className="font-mono text-slate-300">{c.completed_operators}</span> },
    { key: 'storage_location', header: 'Storage URI', render: (c) => <span className="font-mono text-slate-400 text-xs truncate max-w-xs">{c.storage_location}</span> },
    {
      key: 'status',
      header: 'Integrity State',
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
        <title>Chandy-Lamport Checkpoints & Savepoints — DataFlowX</title>
      </Head>

      <div className="space-y-6">
        <div>
          <h1 className="text-2xl font-bold text-white tracking-tight flex items-center gap-2.5">
            <ShieldCheck className="w-7 h-7 text-cyan-400" />
            Distributed Chandy-Lamport Checkpoint & Savepoint Coordinator
          </h1>
          <p className="text-slate-400 text-sm mt-1">
            Asynchronous barrier synchronization, incremental checkpoint snapshots, and exactly-once state recovery.
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <div className="bg-slate-900 border border-slate-800 rounded-xl p-4">
            <div className="text-xs text-slate-500 font-semibold uppercase">Latest Successful Checkpoint</div>
            <div className="text-2xl font-bold text-emerald-400 mt-1">#1420 (Consistent)</div>
          </div>
          <div className="bg-slate-900 border border-slate-800 rounded-xl p-4">
            <div className="text-xs text-slate-500 font-semibold uppercase">Average Alignment Duration</div>
            <div className="text-2xl font-bold text-cyan-400 mt-1">21.6 ms</div>
          </div>
          <div className="bg-slate-900 border border-slate-800 rounded-xl p-4">
            <div className="text-xs text-slate-500 font-semibold uppercase">Checkpoint Guarantee</div>
            <div className="text-2xl font-bold text-white mt-1">Exactly-Once (2PC)</div>
          </div>
        </div>

        <DataGrid data={mockCheckpoints} columns={columns} title="Managed Stream Checkpoints" />
      </div>
    </MainLayout>
  );
}

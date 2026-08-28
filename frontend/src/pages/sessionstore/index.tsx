import React from 'react';
import Head from 'next/head';
import { MainLayout } from '@/components/layout/MainLayout';
import { DataGrid, DataGridColumn } from '@/components/grid/DataGrid';
import { HardDrive, Activity, CheckCircle, Clock, Layers, Zap } from 'lucide-react';

interface ActiveSessionItem {
  session_id: string;
  user_id: string;
  event_count: number;
  total_value: number;
  idle_seconds: number;
  status: 'ACTIVE' | 'EXPIRED';
}

const mockSessions: ActiveSessionItem[] = [
  { session_id: 'sess_usr_9012_a8', user_id: 'usr_premium_1029', event_count: 48, total_value: 340.50, idle_seconds: 12, status: 'ACTIVE' },
  { session_id: 'sess_usr_9013_b9', user_id: 'usr_enterprise_8821', event_count: 120, total_value: 1250.00, idle_seconds: 45, status: 'ACTIVE' },
  { session_id: 'sess_usr_9014_c1', user_id: 'usr_anonymous_7741', event_count: 6, total_value: 14.20, idle_seconds: 140, status: 'ACTIVE' },
];

export default function SessionStorePage() {
  const columns: DataGridColumn<ActiveSessionItem>[] = [
    {
      key: 'session_id',
      header: 'Streaming Session ID',
      render: (s) => (
        <div className="flex items-center gap-2">
          <HardDrive className="w-4 h-4 text-cyan-400" />
          <strong className="text-white font-mono text-xs">{s.session_id}</strong>
        </div>
      ),
    },
    { key: 'user_id', header: 'User Identifier', render: (s) => <span className="font-mono text-slate-300 text-xs">{s.user_id}</span> },
    { key: 'event_count', header: 'Session Events', render: (s) => <span className="font-mono text-cyan-300 font-bold">{s.event_count} events</span> },
    {
      key: 'total_value',
      header: 'Accumulated Metric',
      render: (s) => <span className="font-mono text-emerald-400 font-bold">${s.total_value.toFixed(2)}</span>,
    },
    { key: 'idle_seconds', header: 'Inactivity Time', render: (s) => <span className="font-mono text-slate-400">{s.idle_seconds}s ago</span> },
    {
      key: 'status',
      header: 'State',
      render: (s) => (
        <span className="px-2 py-0.5 rounded bg-emerald-950 text-emerald-400 border border-emerald-800 text-[10px] font-bold">
          {s.status}
        </span>
      ),
    },
  ];

  return (
    <MainLayout>
      <Head>
        <title>Streaming State Store & Session Memory — DataFlowX</title>
      </Head>

      <div className="space-y-6">
        <div>
          <h1 className="text-2xl font-bold text-white tracking-tight flex items-center gap-2.5">
            <HardDrive className="w-7 h-7 text-cyan-400" />
            Streaming Session State Store & RocksDB State Management
          </h1>
          <p className="text-slate-400 text-sm mt-1">
            Stateful streaming session aggregators, inactivity timer evictions, and checkpointed RocksDB key-value stores.
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <div className="bg-slate-900 border border-slate-800 rounded-xl p-4">
            <div className="text-xs text-slate-500 font-semibold uppercase">Active In-Memory Sessions</div>
            <div className="text-2xl font-bold text-white mt-1">3 Sessions</div>
          </div>
          <div className="bg-slate-900 border border-slate-800 rounded-xl p-4">
            <div className="text-xs text-slate-500 font-semibold uppercase">State Store Checkpoint Health</div>
            <div className="text-2xl font-bold text-emerald-400 mt-1">100% Consistent</div>
          </div>
          <div className="bg-slate-900 border border-slate-800 rounded-xl p-4">
            <div className="text-xs text-slate-500 font-semibold uppercase">Average Session State Size</div>
            <div className="text-2xl font-bold text-cyan-400 mt-1">180 Bytes / session</div>
          </div>
        </div>

        <DataGrid data={mockSessions} columns={columns} title="Active Stateful Stream Sessions" />
      </div>
    </MainLayout>
  );
}

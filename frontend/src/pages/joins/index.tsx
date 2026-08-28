import React from 'react';
import Head from 'next/head';
import { MainLayout } from '@/components/layout/MainLayout';
import { DataGrid, DataGridColumn } from '@/components/grid/DataGrid';
import { GitMerge, Clock, Zap, CheckCircle, Radio } from 'lucide-react';

interface StreamJoinSessionItem {
  id: string;
  left_stream: string;
  right_stream: string;
  join_key: string;
  lower_bound_sec: number;
  upper_bound_sec: number;
  joined_events_total: number;
  status: 'ACTIVE' | 'PAUSED';
}

const mockJoins: StreamJoinSessionItem[] = [
  { id: 'join_01', left_stream: 'stream.user_clicks', right_stream: 'stream.ad_impressions', join_key: 'ad_id', lower_bound_sec: 30, upper_bound_sec: 60, joined_events_total: 84200, status: 'ACTIVE' },
  { id: 'join_02', left_stream: 'stream.payment_initiated', right_stream: 'stream.fraud_evaluations', join_key: 'transaction_id', lower_bound_sec: 5, upper_bound_sec: 5, joined_events_total: 125000, status: 'ACTIVE' },
];

export default function StreamingJoinsPage() {
  const columns: DataGridColumn<StreamJoinSessionItem>[] = [
    { key: 'id', header: 'Join Operator', render: (j) => <strong className="text-cyan-400 font-mono">{j.id}</strong> },
    {
      key: 'left_stream',
      header: 'Stream Pairing (Left ⋈ Right)',
      render: (j) => (
        <span className="font-mono text-xs">
          <span className="text-white font-bold">{j.left_stream}</span> ⋈ <span className="text-slate-300">{j.right_stream}</span>
        </span>
      ),
    },
    { key: 'join_key', header: 'Equi-Join Key', render: (j) => <span className="font-mono text-cyan-300 font-semibold">{j.join_key}</span> },
    {
      key: 'lower_bound_sec',
      header: 'Temporal Window Bounds',
      render: (j) => (
        <span className="font-mono text-slate-300 text-xs">
          [-{j.lower_bound_sec}s, +{j.upper_bound_sec}s]
        </span>
      ),
    },
    { key: 'joined_events_total', header: 'Joined Matches', render: (j) => <span className="font-mono text-emerald-400 font-bold">{j.joined_events_total.toLocaleString()}</span> },
    {
      key: 'status',
      header: 'Status',
      render: (j) => (
        <span className="px-2 py-0.5 rounded bg-emerald-950 text-emerald-400 border border-emerald-800 text-[10px] font-bold">
          {j.status}
        </span>
      ),
    },
  ];

  return (
    <MainLayout>
      <Head>
        <title>Streaming Temporal Interval Joins — DataFlowX</title>
      </Head>

      <div className="space-y-6">
        <div>
          <h1 className="text-2xl font-bold text-white tracking-tight flex items-center gap-2.5">
            <GitMerge className="w-7 h-7 text-cyan-400" />
            Streaming Temporal Interval Joins Studio
          </h1>
          <p className="text-slate-400 text-sm mt-1">
            Real-time stateful interval joins between unbounded Kafka streams within sliding temporal time windows.
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <div className="bg-slate-900 border border-slate-800 rounded-xl p-4">
            <div className="text-xs text-slate-500 font-semibold uppercase">Active Interval Join Pipelines</div>
            <div className="text-2xl font-bold text-white mt-1">2 Pipelines</div>
          </div>
          <div className="bg-slate-900 border border-slate-800 rounded-xl p-4">
            <div className="text-xs text-slate-500 font-semibold uppercase">Total Correlated Events</div>
            <div className="text-2xl font-bold text-emerald-400 mt-1">209,200 Matches</div>
          </div>
          <div className="bg-slate-900 border border-slate-800 rounded-xl p-4">
            <div className="text-xs text-slate-500 font-semibold uppercase">Temporal Lag</div>
            <div className="text-2xl font-bold text-cyan-400 mt-1">1.2 ms</div>
          </div>
        </div>

        <DataGrid data={mockJoins} columns={columns} title="Streaming Temporal Joins In Progress" />
      </div>
    </MainLayout>
  );
}

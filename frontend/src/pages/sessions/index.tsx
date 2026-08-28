import React from 'react';
import Head from 'next/head';
import { MainLayout } from '@/components/layout/MainLayout';
import { DataGrid, DataGridColumn } from '@/components/grid/DataGrid';
import { Radio, Activity, Clock, Zap, CheckCircle, Flame } from 'lucide-react';

interface StreamSessionItem {
  session_id: string;
  entity_id: string;
  duration_minutes: number;
  event_count: number;
  total_monetary_value: number;
  status: 'ACTIVE' | 'CLOSED';
}

const mockSessions: StreamSessionItem[] = [
  { session_id: 'sess_cust_101_1724881200', entity_id: 'cust_101', duration_minutes: 18.5, event_count: 34, total_monetary_value: 340.50, status: 'ACTIVE' },
  { session_id: 'sess_cust_102_1724880900', entity_id: 'cust_102', duration_minutes: 42.0, event_count: 82, total_monetary_value: 1250.00, status: 'CLOSED' },
  { session_id: 'sess_cust_103_1724881100', entity_id: 'cust_103', duration_minutes: 6.2, event_count: 12, total_monetary_value: 45.00, status: 'ACTIVE' },
];

export default function StreamingSessionsPage() {
  const columns: DataGridColumn<StreamSessionItem>[] = [
    {
      key: 'session_id',
      header: 'Stream Session Identifier',
      render: (s) => (
        <div className="flex items-center gap-2">
          <Radio className="w-4 h-4 text-amber-400" />
          <strong className="text-white font-mono">{s.session_id}</strong>
        </div>
      ),
    },
    { key: 'entity_id', header: 'Entity / Customer ID', render: (s) => <span className="font-mono text-cyan-300 font-semibold">{s.entity_id}</span> },
    { key: 'duration_minutes', header: 'Active Duration', render: (s) => <span className="font-mono text-slate-300">{s.duration_minutes} mins</span> },
    { key: 'event_count', header: 'Events in Session', render: (s) => <span className="font-mono text-emerald-400 font-bold">{s.event_count} events</span> },
    { key: 'total_monetary_value', header: 'Session Value', render: (s) => <span className="font-mono text-white font-semibold">${s.total_monetary_value.toFixed(2)}</span> },
    {
      key: 'status',
      header: 'Status',
      render: (s) => (
        <span
          className={`px-2 py-0.5 rounded text-[10px] font-bold ${
            s.status === 'ACTIVE'
              ? 'bg-emerald-950 text-emerald-400 border border-emerald-800 animate-pulse'
              : 'bg-slate-800 text-slate-400'
          }`}
        >
          {s.status}
        </span>
      ),
    },
  ];

  return (
    <MainLayout>
      <Head>
        <title>Streaming Session Windows — DataFlowX</title>
      </Head>

      <div className="space-y-6">
        <div>
          <h1 className="text-2xl font-bold text-white tracking-tight flex items-center gap-2.5">
            <Radio className="w-7 h-7 text-amber-400" />
            Streaming Activity Session Windows & Watermarks
          </h1>
          <p className="text-slate-400 text-sm mt-1">
            Dynamic inactivity-gap session aggregation windows with bounded out-of-orderness late event watermarks.
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <div className="bg-slate-900 border border-slate-800 rounded-xl p-4">
            <div className="text-xs text-slate-500 font-semibold uppercase">Active User Sessions</div>
            <div className="text-2xl font-bold text-white mt-1">2 Active Sessions</div>
          </div>
          <div className="bg-slate-900 border border-slate-800 rounded-xl p-4">
            <div className="text-xs text-slate-500 font-semibold uppercase">Watermark Lag</div>
            <div className="text-2xl font-bold text-emerald-400 mt-1">5.0s Bounded</div>
          </div>
          <div className="bg-slate-900 border border-slate-800 rounded-xl p-4">
            <div className="text-xs text-slate-500 font-semibold uppercase">Inactivity Timeout Gap</div>
            <div className="text-2xl font-bold text-cyan-400 mt-1">30 Minutes</div>
          </div>
        </div>

        <DataGrid data={mockSessions} columns={columns} title="Streaming Session Windows Feed" />
      </div>
    </MainLayout>
  );
}

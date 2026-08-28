import React from 'react';
import Head from 'next/head';
import { MainLayout } from '@/components/layout/MainLayout';
import { DataGrid, DataGridColumn } from '@/components/grid/DataGrid';
import { Users, Clock, CheckCircle, Database, Layers, ArrowRight } from 'lucide-react';

interface SessionItem {
  session_id: string;
  user_key: string;
  duration_minutes: number;
  events_in_session: number;
  inactivity_gap_limit: string;
  session_state: 'ACTIVE' | 'CLOSED';
}

const mockSessions: SessionItem[] = [
  { session_id: 'sess_usr_8910_178796', user_key: 'user:alex_smith_89', duration_minutes: 24.5, events_in_session: 142, inactivity_gap_limit: '30 mins gap', session_state: 'ACTIVE' },
  { session_id: 'sess_usr_4412_178795', user_key: 'user:sarah_connor_12', duration_minutes: 48.0, events_in_session: 310, inactivity_gap_limit: '30 mins gap', session_state: 'CLOSED' },
  { session_id: 'sess_usr_9901_178794', user_key: 'user:david_k_01', duration_minutes: 12.0, events_in_session: 65, inactivity_gap_limit: '30 mins gap', session_state: 'CLOSED' },
];

export default function SessionsStudioPage() {
  const columns: DataGridColumn<SessionItem>[] = [
    {
      key: 'session_id',
      header: 'Dynamic Session ID',
      render: (s) => (
        <div className="flex items-center gap-2">
          <Users className="w-4 h-4 text-cyan-400" />
          <strong className="text-white font-mono text-xs">{s.session_id}</strong>
        </div>
      ),
    },
    { key: 'user_key', header: 'Keyed Partition User', render: (s) => <span className="bg-slate-800 text-purple-300 font-mono text-[10px] px-2 py-0.5 rounded">{s.user_key}</span> },
    {
      key: 'duration_minutes',
      header: 'Active Session Duration',
      render: (s) => <span className="font-mono text-cyan-300 font-bold">{s.duration_minutes.toFixed(1)} mins</span>,
    },
    {
      key: 'events_in_session',
      header: 'Events in Window',
      render: (s) => <span className="font-mono text-emerald-400 font-bold">{s.events_in_session} events</span>,
    },
    { key: 'inactivity_gap_limit', header: 'Inactivity Gap Bound', render: (s) => <span className="text-slate-400 text-xs">{s.inactivity_gap_limit}</span> },
    {
      key: 'session_state',
      header: 'Session Status',
      render: (s) => (
        <span
          className={`px-2 py-0.5 rounded text-[10px] font-bold ${
            s.session_state === 'ACTIVE'
              ? 'bg-emerald-950 text-emerald-400 border border-emerald-800'
              : 'bg-slate-800 text-slate-400'
          }`}
        >
          {s.session_state}
        </span>
      ),
    },
  ];

  return (
    <MainLayout>
      <Head>
        <title>Streaming Dynamic Session Windows — DataFlowX</title>
      </Head>

      <div className="space-y-6">
        <div>
          <h1 className="text-2xl font-bold text-white tracking-tight flex items-center gap-2.5">
            <Users className="w-7 h-7 text-cyan-400" />
            Streaming Dynamic Inactivity Gap-Based Session Windows
          </h1>
          <p className="text-slate-400 text-sm mt-1">
            Dynamic session window mergers aggregating variable-length user activity bursts separated by configurable inactivity periods.
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <div className="bg-slate-900 border border-slate-800 rounded-xl p-4">
            <div className="text-xs text-slate-500 font-semibold uppercase">Active Session Windows</div>
            <div className="text-2xl font-bold text-white mt-1">14,250 Sessions</div>
          </div>
          <div className="bg-slate-900 border border-slate-800 rounded-xl p-4">
            <div className="text-xs text-slate-500 font-semibold uppercase">Average Session Length</div>
            <div className="text-2xl font-bold text-emerald-400 mt-1">28.2 Minutes</div>
          </div>
          <div className="bg-slate-900 border border-slate-800 rounded-xl p-4">
            <div className="text-xs text-slate-500 font-semibold uppercase">Inactivity Gap Timeout</div>
            <div className="text-2xl font-bold text-cyan-400 mt-1">30 Minutes Gap</div>
          </div>
        </div>

        <DataGrid data={mockSessions} columns={columns} title="Active Streaming Session Windows" />
      </div>
    </MainLayout>
  );
}

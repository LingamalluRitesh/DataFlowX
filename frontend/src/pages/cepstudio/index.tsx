import React from 'react';
import Head from 'next/head';
import { MainLayout } from '@/components/layout/MainLayout';
import { DataGrid, DataGridColumn } from '@/components/grid/DataGrid';
import { Zap, Activity, ShieldAlert, CheckCircle, Flame, Layers } from 'lucide-react';

interface CEPPatternItem {
  pattern_id: string;
  pattern_name: string;
  sequence_definition: string;
  window_seconds: number;
  detections_24h: number;
  severity: 'CRITICAL' | 'HIGH' | 'MEDIUM';
  status: 'ACTIVE' | 'PAUSED';
}

const mockCEP: CEPPatternItem[] = [
  { pattern_id: 'cep_01', pattern_name: 'Brute Force Login Attack', sequence_definition: 'LoginFailed x 3 -> PasswordReset (within 300s)', window_seconds: 300, detections_24h: 142, severity: 'HIGH', status: 'ACTIVE' },
  { pattern_id: 'cep_02', pattern_name: 'Immediate Card Withdrawal after Email Change', sequence_definition: 'EmailUpdated -> WithdrawalRequest > $5k (within 600s)', window_seconds: 600, detections_24h: 8, severity: 'CRITICAL', status: 'ACTIVE' },
  { pattern_id: 'cep_03', pattern_name: 'IoT High Temperature Cascading Failure', sequence_definition: 'TempSpike > 90C -> FanCurrentDrop (within 60s)', window_seconds: 60, detections_24h: 3, severity: 'CRITICAL', status: 'ACTIVE' },
];

export default function CEPStudioPage() {
  const columns: DataGridColumn<CEPPatternItem>[] = [
    {
      key: 'pattern_name',
      header: 'Complex Event Pattern',
      render: (c) => (
        <div>
          <strong className="text-white font-mono text-xs">{c.pattern_name}</strong>
          <div className="text-[10px] text-slate-500 font-mono">{c.pattern_id}</div>
        </div>
      ),
    },
    { key: 'sequence_definition', header: 'State Sequence (NFA Transition)', render: (c) => <span className="font-mono text-purple-300 text-xs">{c.sequence_definition}</span> },
    {
      key: 'window_seconds',
      header: 'Evaluation Window',
      render: (c) => <span className="font-mono text-cyan-300 font-bold">{c.window_seconds}s</span>,
    },
    {
      key: 'detections_24h',
      header: '24h Pattern Matches',
      render: (c) => <span className="font-mono text-emerald-400 font-bold">{c.detections_24h} matches</span>,
    },
    {
      key: 'severity',
      header: 'Alert Severity',
      render: (c) => (
        <span
          className={`px-2 py-0.5 rounded text-[10px] font-bold ${
            c.severity === 'CRITICAL'
              ? 'bg-red-950 text-red-400 border border-red-800'
              : 'bg-amber-950 text-amber-400 border border-amber-800'
          }`}
        >
          {c.severity}
        </span>
      ),
    },
    {
      key: 'status',
      header: 'Pattern State',
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
        <title>Complex Event Processing (CEP) Studio — DataFlowX</title>
      </Head>

      <div className="space-y-6">
        <div>
          <h1 className="text-2xl font-bold text-white tracking-tight flex items-center gap-2.5">
            <Zap className="w-7 h-7 text-cyan-400" />
            Complex Event Processing (CEP) & NFA Pattern Studio
          </h1>
          <p className="text-slate-400 text-sm mt-1">
            Declarative event sequence pattern matching, Non-deterministic Finite Automaton (NFA) state machines, and real-time fraud detection.
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <div className="bg-slate-900 border border-slate-800 rounded-xl p-4">
            <div className="text-xs text-slate-500 font-semibold uppercase">Active CEP Patterns</div>
            <div className="text-2xl font-bold text-white mt-1">3 Active Rules</div>
          </div>
          <div className="bg-slate-900 border border-slate-800 rounded-xl p-4">
            <div className="text-xs text-slate-500 font-semibold uppercase">Pattern Evaluation Throughput</div>
            <div className="text-2xl font-bold text-emerald-400 mt-1">6.1M events / sec</div>
          </div>
          <div className="bg-slate-900 border border-slate-800 rounded-xl p-4">
            <div className="text-xs text-slate-500 font-semibold uppercase">Pattern Latency</div>
            <div className="text-2xl font-bold text-cyan-400 mt-1">&lt;1 ms / match</div>
          </div>
        </div>

        <DataGrid data={mockCEP} columns={columns} title="Managed Complex Event Sequences" />
      </div>
    </MainLayout>
  );
}

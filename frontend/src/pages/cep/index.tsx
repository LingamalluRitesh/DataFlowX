import React from 'react';
import Head from 'next/head';
import { MainLayout } from '@/components/layout/MainLayout';
import { DataGrid, DataGridColumn } from '@/components/grid/DataGrid';
import { Zap, Activity, Clock, CheckCircle, Radio, Play, Sparkles } from 'lucide-react';

interface CEPPatternRuleItem {
  id: string;
  pattern_name: string;
  sequence_definition: string;
  time_window_seconds: number;
  matches_count_24h: number;
  status: 'EVALUATING' | 'PAUSED';
}

const mockCEPRules: CEPPatternRuleItem[] = [
  { id: 'cep_01', pattern_name: 'Suspicious Brute-Force Login Sequence', sequence_definition: 'FailedLogin -> FailedLogin -> AccountLocked', time_window_seconds: 300, matches_count_24h: 14, status: 'EVALUATING' },
  { id: 'cep_02', pattern_name: 'High-Value Shopping Cart Abandonment', sequence_definition: 'AddToCart(>$500) -> CheckoutStart -> Inactivity(15m)', time_window_seconds: 900, matches_count_24h: 82, status: 'EVALUATING' },
  { id: 'cep_03', pattern_name: 'IoT Sensor Overheat Cascade', sequence_definition: 'TempHigh(>80C) -> VibrationAlert -> EmergencyStop', time_window_seconds: 60, matches_count_24h: 3, status: 'EVALUATING' },
];

export default function CEPStudioPage() {
  const columns: DataGridColumn<CEPPatternRuleItem>[] = [
    {
      key: 'pattern_name',
      header: 'Pattern Name',
      render: (p) => (
        <div>
          <strong className="text-white">{p.pattern_name}</strong>
          <div className="text-[10px] text-slate-500 font-mono">{p.id}</div>
        </div>
      ),
    },
    { key: 'sequence_definition', header: 'Event Sequence Definition', render: (p) => <span className="font-mono text-cyan-300 text-xs">{p.sequence_definition}</span> },
    { key: 'time_window_seconds', header: 'Window Time', render: (p) => <span className="font-mono text-slate-400">{p.time_window_seconds}s</span> },
    { key: 'matches_count_24h', header: 'Matches (24h)', render: (p) => <span className="font-mono text-emerald-400 font-bold">{p.matches_count_24h} matches</span> },
    {
      key: 'status',
      header: 'Status',
      render: (p) => (
        <span className="px-2 py-0.5 rounded bg-emerald-950 text-emerald-400 border border-emerald-800 text-[10px] font-bold">
          {p.status}
        </span>
      ),
    },
  ];

  return (
    <MainLayout>
      <Head>
        <title>Complex Event Processing (CEP) — DataFlowX</title>
      </Head>

      <div className="space-y-6">
        <div>
          <h1 className="text-2xl font-bold text-white tracking-tight flex items-center gap-2.5">
            <Zap className="w-7 h-7 text-amber-400" />
            Complex Event Processing (CEP) State Machine Studio
          </h1>
          <p className="text-slate-400 text-sm mt-1">
            Detect complex temporal event sequences, multi-step fraud patterns, and industrial IoT state transitions in real time.
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <div className="bg-slate-900 border border-slate-800 rounded-xl p-4">
            <div className="text-xs text-slate-500 font-semibold uppercase">Active Pattern Automata</div>
            <div className="text-2xl font-bold text-white mt-1">3 Automata</div>
          </div>
          <div className="bg-slate-900 border border-slate-800 rounded-xl p-4">
            <div className="text-xs text-slate-500 font-semibold uppercase">Events Evaluated / Sec</div>
            <div className="text-2xl font-bold text-emerald-400 mt-1">42,500 evt/s</div>
          </div>
          <div className="bg-slate-900 border border-slate-800 rounded-xl p-4">
            <div className="text-xs text-slate-500 font-semibold uppercase">Pattern Match Latency</div>
            <div className="text-2xl font-bold text-cyan-400 mt-1">0.8 ms</div>
          </div>
        </div>

        <DataGrid data={mockCEPRules} columns={columns} title="Active Complex Event Patterns" />
      </div>
    </MainLayout>
  );
}

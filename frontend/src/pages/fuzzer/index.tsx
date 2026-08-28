import React from 'react';
import Head from 'next/head';
import { MainLayout } from '@/components/layout/MainLayout';
import { DataGrid, DataGridColumn } from '@/components/grid/DataGrid';
import { Flame, ShieldAlert, Zap, CheckCircle, Bug, Sliders, Play } from 'lucide-react';

interface FuzzTestItem {
  test_name: string;
  category: 'UNICODE_INJECTION' | 'NUMERICAL_OVERFLOW' | 'TRAFFIC_BURST';
  payload_sample: string;
  pipeline_resilience_rate: number;
  unhandled_crashes: number;
  status: 'PASSED' | 'VULNERABLE';
}

const mockFuzzTests: FuzzTestItem[] = [
  { test_name: 'Zero-Width Chars & RTL Marker Fuzz', category: 'UNICODE_INJECTION', payload_sample: 'مرحبا \\u200B\\u200C 🔥', pipeline_resilience_rate: 100.0, unhandled_crashes: 0, status: 'PASSED' },
  { test_name: 'Subnormal Floats & NaN Boundary Fuzz', category: 'NUMERICAL_OVERFLOW', payload_sample: '1e-300, NaN, ±Inf', pipeline_resilience_rate: 100.0, unhandled_crashes: 0, status: 'PASSED' },
  { test_name: '50,000 RPS Micro-Burst Spike Chaos', category: 'TRAFFIC_BURST', payload_sample: '50k msgs/s surge', pipeline_resilience_rate: 100.0, unhandled_crashes: 0, status: 'PASSED' },
];

export default function FuzzerChaosStudioPage() {
  const columns: DataGridColumn<FuzzTestItem>[] = [
    { key: 'test_name', header: 'Fuzzing Scenario', render: (f) => <strong className="text-white font-mono text-xs">{f.test_name}</strong> },
    {
      key: 'category',
      header: 'Attack Vector',
      render: (f) => <span className="bg-slate-800 text-purple-400 font-mono text-[10px] px-2 py-0.5 rounded">{f.category}</span>,
    },
    { key: 'payload_sample', header: 'Injected Payload', render: (f) => <span className="font-mono text-amber-300 text-xs">{f.payload_sample}</span> },
    {
      key: 'pipeline_resilience_rate',
      header: 'Resilience Score',
      render: (f) => <span className="font-mono text-emerald-400 font-bold">{f.pipeline_resilience_rate}% Handled</span>,
    },
    {
      key: 'status',
      header: 'Pipeline Health',
      render: (f) => (
        <span className="px-2 py-0.5 rounded bg-emerald-950 text-emerald-400 border border-emerald-800 text-[10px] font-bold">
          {f.status}
        </span>
      ),
    },
  ];

  return (
    <MainLayout>
      <Head>
        <title>Synthetic Data Fuzzer & Chaos Stress — DataFlowX</title>
      </Head>

      <div className="space-y-6">
        <div>
          <h1 className="text-2xl font-bold text-white tracking-tight flex items-center gap-2.5">
            <Flame className="w-7 h-7 text-amber-400" />
            Synthetic Data Fuzzer & Chaos Stress Testing Studio
          </h1>
          <p className="text-slate-400 text-sm mt-1">
            Automated pipeline fuzzing: Unicode zero-width injections, NaN / float overflow boundary attacks, and 50k RPS streaming traffic chaos.
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <div className="bg-slate-900 border border-slate-800 rounded-xl p-4">
            <div className="text-xs text-slate-500 font-semibold uppercase">Total Fuzz Test Vectors</div>
            <div className="text-2xl font-bold text-white mt-1">3 Suites</div>
          </div>
          <div className="bg-slate-900 border border-slate-800 rounded-xl p-4">
            <div className="text-xs text-slate-500 font-semibold uppercase">Platform Chaos Resilience</div>
            <div className="text-2xl font-bold text-emerald-400 mt-1">100.0% Crash Free</div>
          </div>
          <div className="bg-slate-900 border border-slate-800 rounded-xl p-4">
            <div className="text-xs text-slate-500 font-semibold uppercase">Peak Tested Throughput</div>
            <div className="text-2xl font-bold text-cyan-400 mt-1">50,000 RPS</div>
          </div>
        </div>

        <DataGrid data={mockFuzzTests} columns={columns} title="Active Fuzz Testing Vectors" />
      </div>
    </MainLayout>
  );
}

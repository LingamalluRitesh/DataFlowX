import React from 'react';
import Head from 'next/head';
import { MainLayout } from '@/components/layout/MainLayout';
import { DataGrid, DataGridColumn } from '@/components/grid/DataGrid';
import { Calendar, Clock, CheckCircle, Database, Layers, ArrowRight } from 'lucide-react';

interface DateTimeFuncItem {
  func_name: string;
  category: 'EXTRACTION' | 'ARITHMETIC' | 'TRUNCATION' | 'TIMEZONE';
  sample_input: string;
  sample_output: string;
  vectorized_throughput: string;
  ansi_compliant: boolean;
}

const mockDateFuncs: DateTimeFuncItem[] = [
  { func_name: 'DATE_TRUNC("month", ts)', category: 'TRUNCATION', sample_input: '2026-08-29 14:32:00 UTC', sample_output: '2026-08-01 00:00:00 UTC', vectorized_throughput: '18.5M ops/s', ansi_compliant: true },
  { func_name: 'DATE_ADD_DAYS(ts, 14)', category: 'ARITHMETIC', sample_input: '2026-08-29', sample_output: '2026-09-12', vectorized_throughput: '22.0M ops/s', ansi_compliant: true },
  { func_name: 'EXTRACT(EPOCH FROM ts)', category: 'EXTRACTION', sample_input: '2026-08-29 00:00:00 UTC', sample_output: '1787961600.0', vectorized_throughput: '24.1M ops/s', ansi_compliant: true },
];

export default function DateTimeOpsPage() {
  const columns: DataGridColumn<DateTimeFuncItem>[] = [
    {
      key: 'func_name',
      header: 'DateTime Function Expression',
      render: (d) => (
        <div className="flex items-center gap-2">
          <Calendar className="w-4 h-4 text-cyan-400" />
          <strong className="text-white font-mono text-xs">{d.func_name}</strong>
        </div>
      ),
    },
    {
      key: 'category',
      header: 'Function Category',
      render: (d) => <span className="bg-slate-800 text-purple-300 font-mono text-[10px] px-2 py-0.5 rounded">{d.category}</span>,
    },
    { key: 'sample_input', header: 'Input Timestamp', render: (d) => <span className="font-mono text-slate-400 text-xs">{d.sample_input}</span> },
    { key: 'sample_output', header: 'Computed Output', render: (d) => <span className="font-mono text-cyan-300 text-xs font-bold">{d.sample_output}</span> },
    {
      key: 'vectorized_throughput',
      header: 'Vectorized Speed',
      render: (d) => <span className="font-mono text-emerald-400 font-bold">{d.vectorized_throughput}</span>,
    },
    {
      key: 'ansi_compliant',
      header: 'ANSI SQL',
      render: (d) => (
        <span className="px-2 py-0.5 rounded bg-emerald-950 text-emerald-400 border border-emerald-800 text-[10px] font-bold">
          ANSI 2023
        </span>
      ),
    },
  ];

  return (
    <MainLayout>
      <Head>
        <title>Vectorized DateTime Functions — DataFlowX</title>
      </Head>

      <div className="space-y-6">
        <div>
          <h1 className="text-2xl font-bold text-white tracking-tight flex items-center gap-2.5">
            <Calendar className="w-7 h-7 text-cyan-400" />
            Vectorized DateTime Standard Library & Timestamp Studio
          </h1>
          <p className="text-slate-400 text-sm mt-1">
            40+ vectorized DateTime functions including date truncations, timezone shifts, epoch extractions, and business day additions.
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <div className="bg-slate-900 border border-slate-800 rounded-xl p-4">
            <div className="text-xs text-slate-500 font-semibold uppercase">Total Standard Library Functions</div>
            <div className="text-2xl font-bold text-white mt-1">42 Functions</div>
          </div>
          <div className="bg-slate-900 border border-slate-800 rounded-xl p-4">
            <div className="text-xs text-slate-500 font-semibold uppercase">Average SIMD Execution Speed</div>
            <div className="text-2xl font-bold text-emerald-400 mt-1">21.5M ops / sec</div>
          </div>
          <div className="bg-slate-900 border border-slate-800 rounded-xl p-4">
            <div className="text-xs text-slate-500 font-semibold uppercase">Timezone Conversion Engine</div>
            <div className="text-2xl font-bold text-cyan-400 mt-1">IANA Timezone DB</div>
          </div>
        </div>

        <DataGrid data={mockDateFuncs} columns={columns} title="Standard DateTime Library Functions" />
      </div>
    </MainLayout>
  );
}

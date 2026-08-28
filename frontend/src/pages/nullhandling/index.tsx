import React from 'react';
import Head from 'next/head';
import { MainLayout } from '@/components/layout/MainLayout';
import { DataGrid, DataGridColumn } from '@/components/grid/DataGrid';
import { ShieldCheck, Filter, CheckCircle, Database, Layers, ArrowRight } from 'lucide-react';

interface NullHandlingItem {
  func_name: string;
  category: 'COALESCE' | 'NULLIF' | 'FILL_FORWARD' | 'INTERPOLATION';
  sample_input: string;
  sample_output: string;
  vectorized_speed: string;
  ansi_compliant: boolean;
}

const mockNullOps: NullHandlingItem[] = [
  { func_name: 'COALESCE(discount, 0.0)', category: 'COALESCE', sample_input: 'NULL, 0.15, NULL, 0.20', sample_output: '0.0, 0.15, 0.0, 0.20', vectorized_speed: '38.0M ops/s', ansi_compliant: true },
  { func_name: 'NULLIF(department, "UNKNOWN")', category: 'NULLIF', sample_input: '"UNKNOWN", "Finance", "Sales"', sample_output: 'NULL, "Finance", "Sales"', vectorized_speed: '35.2M ops/s', ansi_compliant: true },
  { func_name: 'FORWARD_FILL(stock_price)', category: 'FILL_FORWARD', sample_input: '124.5, NULL, NULL, 125.0', sample_output: '124.5, 124.5, 124.5, 125.0', vectorized_speed: '28.4M ops/s', ansi_compliant: true },
];

export default function NullHandlingStudioPage() {
  const columns: DataGridColumn<NullHandlingItem>[] = [
    {
      key: 'func_name',
      header: 'Null Handling Function',
      render: (n) => (
        <div className="flex items-center gap-2">
          <ShieldCheck className="w-4 h-4 text-cyan-400" />
          <strong className="text-white font-mono text-xs">{n.func_name}</strong>
        </div>
      ),
    },
    {
      key: 'category',
      header: 'Policy Category',
      render: (n) => <span className="bg-slate-800 text-purple-300 font-mono text-[10px] px-2 py-0.5 rounded font-bold">{n.category}</span>,
    },
    { key: 'sample_input', header: 'Input Series (with Nulls)', render: (n) => <span className="font-mono text-slate-400 text-xs">{n.sample_input}</span> },
    { key: 'sample_output', header: 'Imputed / Cleaned Output', render: (n) => <span className="font-mono text-cyan-300 text-xs font-bold">{n.sample_output}</span> },
    {
      key: 'vectorized_speed',
      header: 'Vectorized Speed',
      render: (n) => <span className="font-mono text-emerald-400 font-bold">{n.vectorized_speed}</span>,
    },
    {
      key: 'ansi_compliant',
      header: 'ANSI SQL Standard',
      render: (n) => (
        <span className="px-2 py-0.5 rounded bg-emerald-950 text-emerald-400 border border-emerald-800 text-[10px] font-bold">
          ANSI 2023
        </span>
      ),
    },
  ];

  return (
    <MainLayout>
      <Head>
        <title>Vectorized Null-Handling & Imputation — DataFlowX</title>
      </Head>

      <div className="space-y-6">
        <div>
          <h1 className="text-2xl font-bold text-white tracking-tight flex items-center gap-2.5">
            <Filter className="w-7 h-7 text-cyan-400" />
            Vectorized Null-Handling, Imputation & COALESCE Studio
          </h1>
          <p className="text-slate-400 text-sm mt-1">
            SIMD-accelerated null replacement, COALESCE cascade evaluation, NULLIF conversion, and temporal forward/backward fill operators.
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <div className="bg-slate-900 border border-slate-800 rounded-xl p-4">
            <div className="text-xs text-slate-500 font-semibold uppercase">Total Imputation Functions</div>
            <div className="text-2xl font-bold text-white mt-1">12 Functions</div>
          </div>
          <div className="bg-slate-900 border border-slate-800 rounded-xl p-4">
            <div className="text-xs text-slate-500 font-semibold uppercase">Average SIMD Execution Speed</div>
            <div className="text-2xl font-bold text-emerald-400 mt-1">33.8M ops / sec</div>
          </div>
          <div className="bg-slate-900 border border-slate-800 rounded-xl p-4">
            <div className="text-xs text-slate-500 font-semibold uppercase">Bitmask Null Representation</div>
            <div className="text-2xl font-bold text-cyan-400 mt-1">Arrow Validity Bitmap</div>
          </div>
        </div>

        <DataGrid data={mockNullOps} columns={columns} title="Standard Null Handling Functions" />
      </div>
    </MainLayout>
  );
}

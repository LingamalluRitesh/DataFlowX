import React from 'react';
import Head from 'next/head';
import { MainLayout } from '@/components/layout/MainLayout';
import { DataGrid, DataGridColumn } from '@/components/grid/DataGrid';
import { Calculator, Sparkles, CheckCircle, Database, Layers, ArrowRight } from 'lucide-react';

interface MathFuncItem {
  func_name: string;
  category: 'ARITHMETIC' | 'TRIGONOMETRIC' | 'EXPONENTIAL' | 'ROUNDING';
  sample_input: string;
  sample_output: string;
  simd_acceleration: string;
  ansi_compliant: boolean;
}

const mockMathFuncs: MathFuncItem[] = [
  { func_name: 'LOG10(val)', category: 'EXPONENTIAL', sample_input: '1000.0', sample_output: '3.0', simd_acceleration: 'AVX2 256-bit Vectorized (28M ops/s)', ansi_compliant: true },
  { func_name: 'ROUND(val, 2)', category: 'ROUNDING', sample_input: '142.4568', sample_output: '142.46', simd_acceleration: 'SSE4.2 Vectorized (34M ops/s)', ansi_compliant: true },
  { func_name: 'SQRT(POW(x,2) + POW(y,2))', category: 'TRIGONOMETRIC', sample_input: 'x=3.0, y=4.0', sample_output: '5.0', simd_acceleration: 'AVX-512 FMA Vectorized (22M ops/s)', ansi_compliant: true },
];

export default function MathOpsPage() {
  const columns: DataGridColumn<MathFuncItem>[] = [
    {
      key: 'func_name',
      header: 'Mathematical Function Expression',
      render: (m) => (
        <div className="flex items-center gap-2">
          <Calculator className="w-4 h-4 text-cyan-400" />
          <strong className="text-white font-mono text-xs">{m.func_name}</strong>
        </div>
      ),
    },
    {
      key: 'category',
      header: 'Category',
      render: (m) => <span className="bg-slate-800 text-purple-300 font-mono text-[10px] px-2 py-0.5 rounded">{m.category}</span>,
    },
    { key: 'sample_input', header: 'Input Expression', render: (m) => <span className="font-mono text-slate-400 text-xs">{m.sample_input}</span> },
    { key: 'sample_output', header: 'Computed Result', render: (m) => <span className="font-mono text-cyan-300 text-xs font-bold">{m.sample_output}</span> },
    {
      key: 'simd_acceleration',
      header: 'Hardware SIMD Acceleration',
      render: (m) => <span className="font-mono text-emerald-400 font-bold text-xs">{m.simd_acceleration}</span>,
    },
    {
      key: 'ansi_compliant',
      header: 'ANSI SQL',
      render: (m) => (
        <span className="px-2 py-0.5 rounded bg-emerald-950 text-emerald-400 border border-emerald-800 text-[10px] font-bold">
          ANSI 2023
        </span>
      ),
    },
  ];

  return (
    <MainLayout>
      <Head>
        <title>Vectorized Math & Trig Functions — DataFlowX</title>
      </Head>

      <div className="space-y-6">
        <div>
          <h1 className="text-2xl font-bold text-white tracking-tight flex items-center gap-2.5">
            <Calculator className="w-7 h-7 text-cyan-400" />
            Vectorized Math, Trigonometry & Precision Rounding Standard Library
          </h1>
          <p className="text-slate-400 text-sm mt-1">
            30+ vectorized arithmetic, logarithmic, trigonometric, and IEEE 754 precision rounding operations accelerated with AVX2/AVX-512.
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <div className="bg-slate-900 border border-slate-800 rounded-xl p-4">
            <div className="text-xs text-slate-500 font-semibold uppercase">Total Standard Library Functions</div>
            <div className="text-2xl font-bold text-white mt-1">32 Functions</div>
          </div>
          <div className="bg-slate-900 border border-slate-800 rounded-xl p-4">
            <div className="text-xs text-slate-500 font-semibold uppercase">Average SIMD Execution Speed</div>
            <div className="text-2xl font-bold text-emerald-400 mt-1">28.0M ops / sec</div>
          </div>
          <div className="bg-slate-900 border border-slate-800 rounded-xl p-4">
            <div className="text-xs text-slate-500 font-semibold uppercase">Floating Point Precision</div>
            <div className="text-2xl font-bold text-cyan-400 mt-1">IEEE 754 Float64 Exact</div>
          </div>
        </div>

        <DataGrid data={mockMathFuncs} columns={columns} title="Standard Mathematical Library Functions" />
      </div>
    </MainLayout>
  );
}

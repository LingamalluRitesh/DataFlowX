import React from 'react';
import Head from 'next/head';
import { MainLayout } from '@/components/layout/MainLayout';
import { DataGrid, DataGridColumn } from '@/components/grid/DataGrid';
import { Layers, Sparkles, CheckCircle, Database, ArrowRight } from 'lucide-react';

interface ArrayOpItem {
  operation_name: string;
  operation_type: 'DISTINCT' | 'UNION' | 'INTERSECT' | 'EXCEPT' | 'COMPACT';
  sample_input: string;
  sample_output: string;
  simd_throughput: string;
  ansi_compliant: boolean;
}

const mockArrayOps: ArrayOpItem[] = [
  { operation_name: 'ARRAY_DISTINCT(tags)', operation_type: 'DISTINCT', sample_input: "['vip', 'retail', 'vip', 'premium']", sample_output: "['vip', 'retail', 'premium']", simd_throughput: '16.5M arrays/s', ansi_compliant: true },
  { operation_name: 'ARRAY_INTERSECT(arr_a, arr_b)', operation_type: 'INTERSECT', sample_input: "A: [1,2,3], B: [2,3,4]", sample_output: "[2, 3]", simd_throughput: '14.2M arrays/s', ansi_compliant: true },
  { operation_name: 'ARRAY_COMPACT(arr)', operation_type: 'COMPACT', sample_input: "['apple', NULL, 'banana', NULL]", sample_output: "['apple', 'banana']", simd_throughput: '22.0M arrays/s', ansi_compliant: true },
];

export default function ArraySetAlgebraPage() {
  const columns: DataGridColumn<ArrayOpItem>[] = [
    {
      key: 'operation_name',
      header: 'Array Operation Expression',
      render: (a) => (
        <div className="flex items-center gap-2">
          <Layers className="w-4 h-4 text-cyan-400" />
          <strong className="text-white font-mono text-xs">{a.operation_name}</strong>
        </div>
      ),
    },
    {
      key: 'operation_type',
      header: 'Set Algebra Type',
      render: (a) => <span className="bg-slate-800 text-purple-300 font-mono text-[10px] px-2 py-0.5 rounded font-bold">{a.operation_type}</span>,
    },
    { key: 'sample_input', header: 'Input Array Payload', render: (a) => <span className="font-mono text-slate-400 text-xs">{a.sample_input}</span> },
    { key: 'sample_output', header: 'Set Algebra Output', render: (a) => <span className="font-mono text-cyan-300 text-xs font-bold">{a.sample_output}</span> },
    {
      key: 'simd_throughput',
      header: 'Vectorized Speed',
      render: (a) => <span className="font-mono text-emerald-400 font-bold">{a.simd_throughput}</span>,
    },
    {
      key: 'ansi_compliant',
      header: 'ANSI SQL Standard',
      render: (a) => (
        <span className="px-2 py-0.5 rounded bg-emerald-950 text-emerald-400 border border-emerald-800 text-[10px] font-bold">
          ANSI 2023
        </span>
      ),
    },
  ];

  return (
    <MainLayout>
      <Head>
        <title>Vectorized Array Set Algebra — DataFlowX</title>
      </Head>

      <div className="space-y-6">
        <div>
          <h1 className="text-2xl font-bold text-white tracking-tight flex items-center gap-2.5">
            <Layers className="w-7 h-7 text-cyan-400" />
            Vectorized Array Set Algebra & Collection Operators
          </h1>
          <p className="text-slate-400 text-sm mt-1">
            High-speed vectorized array transformations including deduplication, union, intersection, set differences, and null compaction.
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <div className="bg-slate-900 border border-slate-800 rounded-xl p-4">
            <div className="text-xs text-slate-500 font-semibold uppercase">Total Array Operators</div>
            <div className="text-2xl font-bold text-white mt-1">16 Vectorized Ops</div>
          </div>
          <div className="bg-slate-900 border border-slate-800 rounded-xl p-4">
            <div className="text-xs text-slate-500 font-semibold uppercase">Average Set Algebra Speed</div>
            <div className="text-2xl font-bold text-emerald-400 mt-1">17.5M arrays / sec</div>
          </div>
          <div className="bg-slate-900 border border-slate-800 rounded-xl p-4">
            <div className="text-xs text-slate-500 font-semibold uppercase">Memory Allocation Mode</div>
            <div className="text-2xl font-bold text-cyan-400 mt-1">Zero-Copy Slices</div>
          </div>
        </div>

        <DataGrid data={mockArrayOps} columns={columns} title="Managed Array Algebra Operations" />
      </div>
    </MainLayout>
  );
}

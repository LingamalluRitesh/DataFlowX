import React from 'react';
import Head from 'next/head';
import { MainLayout } from '@/components/layout/MainLayout';
import { DataGrid, DataGridColumn } from '@/components/grid/DataGrid';
import { Type, Sparkles, CheckCircle, Database, Layers, ArrowRight } from 'lucide-react';

interface StringFuncItem {
  func_name: string;
  category: 'CLEANING' | 'REGEX' | 'HASHING' | 'FUZZY';
  sample_input: string;
  sample_output: string;
  vectorized_throughput: string;
  ansi_compliant: boolean;
}

const mockStringFuncs: StringFuncItem[] = [
  { func_name: 'SHA256_SALT(val, salt)', category: 'HASHING', sample_input: 'user@example.com', sample_output: 'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855', vectorized_throughput: '14.2M ops/s', ansi_compliant: true },
  { func_name: 'LEVENSHTEIN_DISTANCE(a, b)', category: 'FUZZY', sample_input: 'DataFlowX vs DataFlow', sample_output: '1 distance', vectorized_throughput: '9.8M ops/s', ansi_compliant: true },
  { func_name: 'REGEXP_REPLACE(val, pat, rep)', category: 'REGEX', sample_input: 'Order #98124', sample_output: '98124', vectorized_throughput: '12.0M ops/s', ansi_compliant: true },
];

export default function StringOpsPage() {
  const columns: DataGridColumn<StringFuncItem>[] = [
    {
      key: 'func_name',
      header: 'String Function Expression',
      render: (s) => (
        <div className="flex items-center gap-2">
          <Type className="w-4 h-4 text-cyan-400" />
          <strong className="text-white font-mono text-xs">{s.func_name}</strong>
        </div>
      ),
    },
    {
      key: 'category',
      header: 'Operation Category',
      render: (s) => <span className="bg-slate-800 text-purple-300 font-mono text-[10px] px-2 py-0.5 rounded">{s.category}</span>,
    },
    { key: 'sample_input', header: 'Input String', render: (s) => <span className="font-mono text-slate-400 text-xs">{s.sample_input}</span> },
    { key: 'sample_output', header: 'Computed Output', render: (s) => <span className="font-mono text-cyan-300 text-xs font-bold truncate max-w-xs">{s.sample_output}</span> },
    {
      key: 'vectorized_throughput',
      header: 'Vectorized Speed',
      render: (s) => <span className="font-mono text-emerald-400 font-bold">{s.vectorized_throughput}</span>,
    },
    {
      key: 'ansi_compliant',
      header: 'ANSI SQL',
      render: (s) => (
        <span className="px-2 py-0.5 rounded bg-emerald-950 text-emerald-400 border border-emerald-800 text-[10px] font-bold">
          ANSI 2023
        </span>
      ),
    },
  ];

  return (
    <MainLayout>
      <Head>
        <title>Vectorized String & Crypto Functions — DataFlowX</title>
      </Head>

      <div className="space-y-6">
        <div>
          <h1 className="text-2xl font-bold text-white tracking-tight flex items-center gap-2.5">
            <Type className="w-7 h-7 text-cyan-400" />
            Vectorized String, Regex & Cryptographic Standard Library
          </h1>
          <p className="text-slate-400 text-sm mt-1">
            35+ vectorized string manipulation, Levenshtein distance, regex extractions, and SHA-256 salted cryptographic hash functions.
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <div className="bg-slate-900 border border-slate-800 rounded-xl p-4">
            <div className="text-xs text-slate-500 font-semibold uppercase">Total Standard Library Functions</div>
            <div className="text-2xl font-bold text-white mt-1">36 Functions</div>
          </div>
          <div className="bg-slate-900 border border-slate-800 rounded-xl p-4">
            <div className="text-xs text-slate-500 font-semibold uppercase">Average SIMD Execution Speed</div>
            <div className="text-2xl font-bold text-emerald-400 mt-1">12.0M ops / sec</div>
          </div>
          <div className="bg-slate-900 border border-slate-800 rounded-xl p-4">
            <div className="text-xs text-slate-500 font-semibold uppercase">Regular Expression Engine</div>
            <div className="text-2xl font-bold text-cyan-400 mt-1">Vectorized PCRE2</div>
          </div>
        </div>

        <DataGrid data={mockStringFuncs} columns={columns} title="Standard String Library Functions" />
      </div>
    </MainLayout>
  );
}

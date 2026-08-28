import React from 'react';
import Head from 'next/head';
import { MainLayout } from '@/components/layout/MainLayout';
import { DataGrid, DataGridColumn } from '@/components/grid/DataGrid';
import { Cpu, Zap, Activity, Layers, Play, CheckCircle, Flame } from 'lucide-react';

interface MPPFragmentItem {
  stage_id: number;
  operator_name: string;
  partition_count: number;
  rows_processed: number;
  cpu_time_ms: number;
  memory_peak_mb: number;
  status: 'COMPLETED' | 'EXECUTING';
}

const mockFragments: MPPFragmentItem[] = [
  { stage_id: 1, operator_name: 'ParquetVectorScanExec', partition_count: 64, rows_processed: 5000000, cpu_time_ms: 18.4, memory_peak_mb: 128.0, status: 'COMPLETED' },
  { stage_id: 2, operator_name: 'VectorizedFilterExec', partition_count: 64, rows_processed: 1250000, cpu_time_ms: 8.2, memory_peak_mb: 64.5, status: 'COMPLETED' },
  { stage_id: 3, operator_name: 'HashAggregateExec', partition_count: 16, rows_processed: 45000, cpu_time_ms: 12.1, memory_peak_mb: 32.0, status: 'COMPLETED' },
  { stage_id: 4, operator_name: 'ExchangeMergeSortExec', partition_count: 1, rows_processed: 100, cpu_time_ms: 2.3, memory_peak_mb: 8.0, status: 'COMPLETED' },
];

export default function MPPQueryStudioPage() {
  const columns: DataGridColumn<MPPFragmentItem>[] = [
    { key: 'stage_id', header: 'Stage', render: (f) => <span className="font-mono text-cyan-400 font-bold">Stage {f.stage_id}</span> },
    { key: 'operator_name', header: 'Vectorized Physical Operator', render: (f) => <strong className="text-white font-mono">{f.operator_name}</strong> },
    { key: 'partition_count', header: 'Parallel Partitions', render: (f) => <span className="font-mono text-slate-300">{f.partition_count} partitions</span> },
    { key: 'rows_processed', header: 'Rows Processed', render: (f) => <span className="font-mono text-emerald-400 font-semibold">{f.rows_processed.toLocaleString()}</span> },
    { key: 'cpu_time_ms', header: 'CPU Time', render: (f) => <span className="font-mono text-slate-300">{f.cpu_time_ms} ms</span> },
    { key: 'memory_peak_mb', header: 'Peak Memory', render: (f) => <span className="font-mono text-purple-400">{f.memory_peak_mb} MB</span> },
    {
      key: 'status',
      header: 'Status',
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
        <title>Vectorized MPP Engine Execution Profile — DataFlowX</title>
      </Head>

      <div className="space-y-6">
        <div>
          <h1 className="text-2xl font-bold text-white tracking-tight flex items-center gap-2.5">
            <Cpu className="w-7 h-7 text-cyan-400" />
            Vectorized MPP Query Engine & Fragment Profiler
          </h1>
          <p className="text-slate-400 text-sm mt-1">
            Volcano iterator physical execution fragments with SIMD column vector batches and partition exchange operators.
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
          <div className="bg-slate-900 border border-slate-800 rounded-xl p-4">
            <div className="text-xs text-slate-500 font-semibold uppercase">Total Scanned Rows</div>
            <div className="text-2xl font-bold text-white mt-1">5,000,000</div>
          </div>
          <div className="bg-slate-900 border border-slate-800 rounded-xl p-4">
            <div className="text-xs text-slate-500 font-semibold uppercase">End-to-End Latency</div>
            <div className="text-2xl font-bold text-emerald-400 mt-1">41.0 ms</div>
          </div>
          <div className="bg-slate-900 border border-slate-800 rounded-xl p-4">
            <div className="text-xs text-slate-500 font-semibold uppercase">Throughput Rate</div>
            <div className="text-2xl font-bold text-cyan-400 mt-1">121.9M rows/s</div>
          </div>
          <div className="bg-slate-900 border border-slate-800 rounded-xl p-4">
            <div className="text-xs text-slate-500 font-semibold uppercase">Peak Allocation</div>
            <div className="text-2xl font-bold text-purple-400 mt-1">232.5 MB</div>
          </div>
        </div>

        <DataGrid data={mockFragments} columns={columns} title="Active Query Execution Stage Profile" />
      </div>
    </MainLayout>
  );
}

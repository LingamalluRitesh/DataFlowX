import React from 'react';
import Head from 'next/head';
import { MainLayout } from '@/components/layout/MainLayout';
import { DataGrid, DataGridColumn } from '@/components/grid/DataGrid';
import { Boxes, Layers, RefreshCw, CheckCircle, Activity, Sparkles } from 'lucide-react';

interface CompactionJobItem {
  id: string;
  table_name: string;
  partition: string;
  strategy: 'BIN_PACKING' | 'Z_ORDER' | 'HIERARCHICAL_SORT';
  input_files_count: number;
  output_files_count: number;
  bytes_compacted_mb: number;
  status: 'COMPLETED' | 'RUNNING';
}

const mockCompactionJobs: CompactionJobItem[] = [
  { id: 'comp_01', table_name: 'gold.fact_orders', partition: 'order_date=2026-08-28', strategy: 'Z_ORDER', input_files_count: 64, output_files_count: 2, bytes_compacted_mb: 256.0, status: 'COMPLETED' },
  { id: 'comp_02', table_name: 'silver.dim_customers', partition: 'country=US', strategy: 'HIERARCHICAL_SORT', input_files_count: 28, output_files_count: 1, bytes_compacted_mb: 128.0, status: 'COMPLETED' },
  { id: 'comp_03', table_name: 'bronze.iot_telemetry', partition: 'dt=2026-08-28', strategy: 'BIN_PACKING', input_files_count: 140, output_files_count: 4, bytes_compacted_mb: 512.0, status: 'COMPLETED' },
];

export default function CompactionEnginePage() {
  const columns: DataGridColumn<CompactionJobItem>[] = [
    {
      key: 'table_name',
      header: 'Lakehouse Table Target',
      render: (c) => (
        <div>
          <strong className="text-white font-mono">{c.table_name}</strong>
          <div className="text-[10px] text-slate-500 font-mono">{c.partition}</div>
        </div>
      ),
    },
    {
      key: 'strategy',
      header: 'Compaction Strategy',
      render: (c) => <span className="bg-slate-800 text-purple-400 font-mono text-[10px] px-2 py-0.5 rounded">{c.strategy}</span>,
    },
    {
      key: 'input_files_count',
      header: 'File Consolidation (In → Out)',
      render: (c) => (
        <span className="font-mono text-xs">
          <span className="text-red-400 font-bold">{c.input_files_count}</span> →{' '}
          <span className="text-emerald-400 font-bold">{c.output_files_count} files</span>
        </span>
      ),
    },
    { key: 'bytes_compacted_mb', header: 'Compacted Size', render: (c) => <span className="font-mono text-cyan-300 font-bold">{c.bytes_compacted_mb} MB</span> },
    {
      key: 'status',
      header: 'Status',
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
        <title>Lakehouse Compaction & Z-Order Clustering — DataFlowX</title>
      </Head>

      <div className="space-y-6">
        <div>
          <h1 className="text-2xl font-bold text-white tracking-tight flex items-center gap-2.5">
            <Boxes className="w-7 h-7 text-cyan-400" />
            Lakehouse Compaction & Z-Order Clustering Engine
          </h1>
          <p className="text-slate-400 text-sm mt-1">
            First-Fit Decreasing bin-packing small file consolidator and multi-dimensional Morton Z-curve space-filling indexer.
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <div className="bg-slate-900 border border-slate-800 rounded-xl p-4">
            <div className="text-xs text-slate-500 font-semibold uppercase">Total Small Files Consolidated</div>
            <div className="text-2xl font-bold text-emerald-400 mt-1">232 Small Files Merged</div>
          </div>
          <div className="bg-slate-900 border border-slate-800 rounded-xl p-4">
            <div className="text-xs text-slate-500 font-semibold uppercase">Target File Chunk Size</div>
            <div className="text-2xl font-bold text-white mt-1">128 MB Target</div>
          </div>
          <div className="bg-slate-900 border border-slate-800 rounded-xl p-4">
            <div className="text-xs text-slate-500 font-semibold uppercase">Scan Latency Speedup</div>
            <div className="text-2xl font-bold text-cyan-400 mt-1">4.8x Faster Queries</div>
          </div>
        </div>

        <DataGrid data={mockCompactionJobs} columns={columns} title="Lakehouse Compaction History" />
      </div>
    </MainLayout>
  );
}

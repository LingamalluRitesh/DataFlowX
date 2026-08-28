import React from 'react';
import Head from 'next/head';
import { MainLayout } from '@/components/layout/MainLayout';
import { DataGrid, DataGridColumn } from '@/components/grid/DataGrid';
import { Layers, HardDrive, CheckCircle, Flame, ArrowRight, Package } from 'lucide-react';

interface BinPackItem {
  bin_id: number;
  table_name: string;
  source_files_packed: number;
  target_file_size_mb: number;
  reduction_factor: string;
  compaction_duration_s: number;
  status: 'COMPACTED' | 'SCHEDULED';
}

const mockBins: BinPackItem[] = [
  { bin_id: 1, table_name: 'gold.fact_orders', source_files_packed: 48, target_file_size_mb: 128.0, reduction_factor: '48 files -> 1 file (98% reduction)', compaction_duration_s: 4.2, status: 'COMPACTED' },
  { bin_id: 2, table_name: 'silver.dim_customers', source_files_packed: 32, target_file_size_mb: 128.0, reduction_factor: '32 files -> 1 file (97% reduction)', compaction_duration_s: 2.8, status: 'COMPACTED' },
  { bin_id: 3, table_name: 'bronze.iot_telemetry', source_files_packed: 120, target_file_size_mb: 512.0, reduction_factor: '120 files -> 1 file (99% reduction)', compaction_duration_s: 14.5, status: 'COMPACTED' },
];

export default function BinPackingPartitionerPage() {
  const columns: DataGridColumn<BinPackItem>[] = [
    {
      key: 'bin_id',
      header: 'Compaction Bin ID',
      render: (b) => (
        <div className="flex items-center gap-2">
          <Package className="w-4 h-4 text-cyan-400" />
          <strong className="text-white font-mono text-xs">Bin #{b.bin_id}</strong>
        </div>
      ),
    },
    { key: 'table_name', header: 'Target Table', render: (b) => <span className="font-mono text-slate-300 text-xs">{b.table_name}</span> },
    {
      key: 'source_files_packed',
      header: 'Small Files Aggregated',
      render: (b) => <span className="font-mono text-amber-400 font-bold">{b.source_files_packed} small files</span>,
    },
    {
      key: 'target_file_size_mb',
      header: 'Target Parquet File Size',
      render: (b) => <span className="font-mono text-emerald-400 font-bold">{b.target_file_size_mb} MB</span>,
    },
    { key: 'reduction_factor', header: 'Metadata Reduction', render: (b) => <span className="font-mono text-cyan-300 text-xs">{b.reduction_factor}</span> },
    { key: 'compaction_duration_s', header: 'Execution Duration', render: (b) => <span className="font-mono text-slate-400">{b.compaction_duration_s}s</span> },
    {
      key: 'status',
      header: 'State',
      render: (b) => (
        <span className="px-2 py-0.5 rounded bg-emerald-950 text-emerald-400 border border-emerald-800 text-[10px] font-bold">
          {b.status}
        </span>
      ),
    },
  ];

  return (
    <MainLayout>
      <Head>
        <title>First-Fit-Decreasing Bin Packing Partitioner — DataFlowX</title>
      </Head>

      <div className="space-y-6">
        <div>
          <h1 className="text-2xl font-bold text-white tracking-tight flex items-center gap-2.5">
            <Package className="w-7 h-7 text-cyan-400" />
            First-Fit-Decreasing (FFD) Parquet File Bin Packing Studio
          </h1>
          <p className="text-slate-400 text-sm mt-1">
            Optimizes Lakehouse object stores by grouping thousands of small ingestion micro-batches into ideal 128MB/512MB columnar files.
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <div className="bg-slate-900 border border-slate-800 rounded-xl p-4">
            <div className="text-xs text-slate-500 font-semibold uppercase">Total Small Files Compacted</div>
            <div className="text-2xl font-bold text-white mt-1">200 Small Files</div>
          </div>
          <div className="bg-slate-900 border border-slate-800 rounded-xl p-4">
            <div className="text-xs text-slate-500 font-semibold uppercase">Metadata Overhead Reduction</div>
            <div className="text-2xl font-bold text-emerald-400 mt-1">98.5% Metadata Shrunk</div>
          </div>
          <div className="bg-slate-900 border border-slate-800 rounded-xl p-4">
            <div className="text-xs text-slate-500 font-semibold uppercase">Compaction Heuristic</div>
            <div className="text-2xl font-bold text-cyan-400 mt-1">FFD (Optimal Bin)</div>
          </div>
        </div>

        <DataGrid data={mockBins} columns={columns} title="Compaction Bin Packing Operations" />
      </div>
    </MainLayout>
  );
}

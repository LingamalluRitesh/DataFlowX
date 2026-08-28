import React from 'react';
import Head from 'next/head';
import { MainLayout } from '@/components/layout/MainLayout';
import { DataGrid, DataGridColumn } from '@/components/grid/DataGrid';
import { Layers, Minimize2, CheckCircle, Sparkles, Database, FileText } from 'lucide-react';

interface CompactionJobItem {
  id: string;
  table_name: string;
  files_before: number;
  files_after: number;
  reduction_ratio: string;
  z_order_columns: string[];
  duration_seconds: number;
  status: 'SUCCESS' | 'OPTIMIZING';
}

const mockCompactions: CompactionJobItem[] = [
  { id: 'compact_01', table_name: 'gold.fact_orders', files_before: 1240, files_after: 8, reduction_ratio: '99.3% reduction', z_order_columns: ['customer_id', 'created_at'], duration_seconds: 42, status: 'SUCCESS' },
  { id: 'compact_02', table_name: 'silver.dim_customers_scd2', files_before: 450, files_after: 4, reduction_ratio: '99.1% reduction', z_order_columns: ['email_hash'], duration_seconds: 18, status: 'SUCCESS' },
  { id: 'compact_03', table_name: 'bronze.iot_telemetry', files_before: 8400, files_after: 32, reduction_ratio: '99.6% reduction', z_order_columns: ['device_id', 'recorded_at'], duration_seconds: 110, status: 'SUCCESS' },
];

export default function CompactionIndexPage() {
  const columns: DataGridColumn<CompactionJobItem>[] = [
    {
      key: 'table_name',
      header: 'Lakehouse Table',
      render: (c) => (
        <div>
          <strong className="text-white font-mono">{c.table_name}</strong>
          <div className="text-[10px] text-slate-500">{c.id}</div>
        </div>
      ),
    },
    {
      key: 'files_before',
      header: 'Small Files Merged',
      render: (c) => (
        <div className="flex items-center gap-2 font-mono">
          <span className="text-red-400 line-through">{c.files_before} files</span>
          <span>&rarr;</span>
          <span className="text-emerald-400 font-bold">{c.files_after} bins</span>
        </div>
      ),
    },
    {
      key: 'reduction_ratio',
      header: 'Metadata Reduction',
      render: (c) => <span className="text-cyan-400 font-bold font-mono">{c.reduction_ratio}</span>,
    },
    {
      key: 'z_order_columns',
      header: 'Z-Order Spatial Index',
      render: (c) => (
        <div className="flex flex-wrap gap-1">
          {c.z_order_columns.map((col) => (
            <span key={col} className="bg-purple-950 text-purple-400 border border-purple-800 px-1.5 py-0.5 rounded font-mono text-[10px]">
              Z({col})
            </span>
          ))}
        </div>
      ),
    },
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
        <title>Parquet Compaction & Z-Order Indexing — DataFlowX</title>
      </Head>

      <div className="space-y-6">
        <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
          <div>
            <h1 className="text-2xl font-bold text-white tracking-tight flex items-center gap-2.5">
              <Minimize2 className="w-7 h-7 text-purple-400" />
              Parquet Compaction & Z-Order Indexing Console
            </h1>
            <p className="text-slate-400 text-sm mt-1">
              Bin-packs sub-optimal micro-files into 128MB-512MB compressed row groups with multi-dimensional Morton Z-curves.
            </p>
          </div>

          <button className="flex items-center gap-1.5 px-4 py-2 rounded-lg bg-cyan-600 hover:bg-cyan-500 text-white text-xs font-semibold shadow-lg shadow-cyan-600/20 transition self-start md:self-auto">
            <Sparkles className="w-4 h-4" /> Trigger Auto-Compaction
          </button>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <div className="bg-slate-900 border border-slate-800 rounded-xl p-4">
            <div className="text-xs text-slate-500 font-semibold uppercase">Total Files Compacted (30d)</div>
            <div className="text-2xl font-bold text-white mt-1">10,090 Files</div>
          </div>
          <div className="bg-slate-900 border border-slate-800 rounded-xl p-4">
            <div className="text-xs text-slate-500 font-semibold uppercase">Average Scan Speedup</div>
            <div className="text-2xl font-bold text-emerald-400 mt-1">12.5x Faster</div>
          </div>
          <div className="bg-slate-900 border border-slate-800 rounded-xl p-4">
            <div className="text-xs text-slate-500 font-semibold uppercase">Object Storage S3 LIST Calls Saved</div>
            <div className="text-2xl font-bold text-cyan-400 mt-1">2.4M Ops</div>
          </div>
        </div>

        <DataGrid data={mockCompactions} columns={columns} title="Compacted Lakehouse Tables" />
      </div>
    </MainLayout>
  );
}

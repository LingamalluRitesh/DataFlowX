import React from 'react';
import Head from 'next/head';
import { MainLayout } from '@/components/layout/MainLayout';
import { DataGrid, DataGridColumn } from '@/components/grid/DataGrid';
import { Search, Database, Layers, CheckCircle, Sparkles, Filter, ShieldCheck } from 'lucide-react';

interface IndexHealthItem {
  id: string;
  table_name: string;
  column_name: string;
  index_type: 'BLOOM_FILTER' | 'ROARING_BITMAP' | 'INVERTED_POSTING' | 'MINMAX_ZONEMAP';
  pruning_efficiency_pct: number;
  index_size_kb: number;
  status: 'ACTIVE' | 'BUILDING';
}

const mockIndexes: IndexHealthItem[] = [
  { id: 'idx_01', table_name: 'gold.fact_orders', column_name: 'customer_id', index_type: 'BLOOM_FILTER', pruning_efficiency_pct: 94.2, index_size_kb: 512, status: 'ACTIVE' },
  { id: 'idx_02', table_name: 'silver.dim_customers', column_name: 'country_code', index_type: 'ROARING_BITMAP', pruning_efficiency_pct: 99.1, index_size_kb: 64, status: 'ACTIVE' },
  { id: 'idx_03', table_name: 'bronze.iot_telemetry', column_name: 'recorded_at', index_type: 'MINMAX_ZONEMAP', pruning_efficiency_pct: 88.5, index_size_kb: 12, status: 'ACTIVE' },
  { id: 'idx_04', table_name: 'gold.fact_orders', column_name: 'order_status', index_type: 'INVERTED_POSTING', pruning_efficiency_pct: 96.0, index_size_kb: 32, status: 'ACTIVE' },
];

export default function IndexingHealthPage() {
  const columns: DataGridColumn<IndexHealthItem>[] = [
    {
      key: 'column_name',
      header: 'Indexed Column Target',
      render: (i) => (
        <div>
          <strong className="text-white font-mono">{i.column_name}</strong>
          <div className="text-[10px] text-slate-500 font-mono">{i.table_name}</div>
        </div>
      ),
    },
    {
      key: 'index_type',
      header: 'Index Architecture',
      render: (i) => (
        <span className="bg-slate-800 text-purple-400 font-mono text-[10px] px-2 py-0.5 rounded">
          {i.index_type}
        </span>
      ),
    },
    {
      key: 'pruning_efficiency_pct',
      header: 'Row-Group Pruning Rate',
      render: (i) => <span className="font-mono text-emerald-400 font-bold">{i.pruning_efficiency_pct}% pruned</span>,
    },
    { key: 'index_size_kb', header: 'Index Footprint', render: (i) => <span className="font-mono text-slate-300">{i.index_size_kb} KB</span> },
    {
      key: 'status',
      header: 'Status',
      render: (i) => (
        <span className="px-2 py-0.5 rounded bg-emerald-950 text-emerald-400 border border-emerald-800 text-[10px] font-bold">
          {i.status}
        </span>
      ),
    },
  ];

  return (
    <MainLayout>
      <Head>
        <title>Bloom Filters & Inverted Indexing — DataFlowX</title>
      </Head>

      <div className="space-y-6">
        <div>
          <h1 className="text-2xl font-bold text-white tracking-tight flex items-center gap-2.5">
            <Search className="w-7 h-7 text-cyan-400" />
            Lakehouse Secondary Indexing & Pruning Hub
          </h1>
          <p className="text-slate-400 text-sm mt-1">
            Probabilistic split-block Bloom filters, compressed Roaring Bitmaps, inverted posting lists, and Min/Max zone-maps.
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <div className="bg-slate-900 border border-slate-800 rounded-xl p-4">
            <div className="text-xs text-slate-500 font-semibold uppercase">Active Secondary Indexes</div>
            <div className="text-2xl font-bold text-white mt-1">4 Indexes</div>
          </div>
          <div className="bg-slate-900 border border-slate-800 rounded-xl p-4">
            <div className="text-xs text-slate-500 font-semibold uppercase">Average Disk I/O Reduction</div>
            <div className="text-2xl font-bold text-emerald-400 mt-1">94.4% Skipped</div>
          </div>
          <div className="bg-slate-900 border border-slate-800 rounded-xl p-4">
            <div className="text-xs text-slate-500 font-semibold uppercase">Total Index Overhead</div>
            <div className="text-2xl font-bold text-cyan-400 mt-1">620 KB (0.01%)</div>
          </div>
        </div>

        <DataGrid data={mockIndexes} columns={columns} title="Active Secondary Indexes & Pruning Efficiency" />
      </div>
    </MainLayout>
  );
}

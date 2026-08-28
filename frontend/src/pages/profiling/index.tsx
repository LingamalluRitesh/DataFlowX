import React from 'react';
import Head from 'next/head';
import { MainLayout } from '@/components/layout/MainLayout';
import { DataGrid, DataGridColumn } from '@/components/grid/DataGrid';
import { BarChart3, Database, Layers, CheckCircle, ShieldAlert, Sparkles } from 'lucide-react';

interface ColumnProfileData {
  column: string;
  type: string;
  null_pct: number;
  distinct_count: number;
  min_val: string;
  max_val: string;
  mean_val?: string;
  p50_median?: string;
  p95?: string;
}

const mockProfile: ColumnProfileData[] = [
  { column: 'order_id', type: 'BIGINT', null_pct: 0.0, distinct_count: 1000000, min_val: '1', max_val: '1000000', mean_val: '500000.5', p50_median: '500000', p95: '950000' },
  { column: 'customer_id', type: 'VARCHAR(64)', null_pct: 0.0, distinct_count: 85200, min_val: 'cust_0001', max_val: 'cust_9999' },
  { column: 'order_total', type: 'DECIMAL(12,2)', null_pct: 0.1, distinct_count: 34500, min_val: '$4.99', max_val: '$14,500.00', mean_val: '$142.50', p50_median: '$89.99', p95: '$499.00' },
  { column: 'tax_amount', type: 'DECIMAL(10,2)', null_pct: 0.1, distinct_count: 12000, min_val: '$0.00', max_val: '$1,250.00', mean_val: '$11.40', p50_median: '$7.20', p95: '$39.90' },
  { column: 'order_status', type: 'VARCHAR(32)', null_pct: 0.0, distinct_count: 4, min_val: 'CANCELLED', max_val: 'SHIPPED' },
  { column: 'created_at', type: 'TIMESTAMP', null_pct: 0.0, distinct_count: 985000, min_val: '2026-01-01 00:00:00', max_val: '2026-08-28 23:59:59' },
];

export default function ProfilingIndexPage() {
  const columns: DataGridColumn<ColumnProfileData>[] = [
    { key: 'column', header: 'Column Name', render: (c) => <strong className="text-white font-mono">{c.column}</strong> },
    { key: 'type', header: 'Data Type', render: (c) => <span className="bg-slate-800 px-2 py-0.5 rounded text-cyan-400 font-mono text-xs">{c.type}</span> },
    {
      key: 'null_pct',
      header: 'Missing %',
      render: (c) => (
        <span className={`font-mono ${c.null_pct > 0 ? 'text-amber-400' : 'text-emerald-400'}`}>
          {c.null_pct}%
        </span>
      ),
    },
    { key: 'distinct_count', header: 'Cardinality (Distinct)', render: (c) => <span className="font-mono">{c.distinct_count.toLocaleString()}</span> },
    { key: 'min_val', header: 'Min Value' },
    { key: 'max_val', header: 'Max Value' },
    { key: 'mean_val', header: 'Mean' },
    { key: 'p50_median', header: 'Median (P50)' },
    { key: 'p95', header: 'P95' },
  ];

  return (
    <MainLayout>
      <Head>
        <title>Deep Data Profiling & Statistical Summaries — DataFlowX</title>
      </Head>

      <div className="space-y-6">
        <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
          <div>
            <h1 className="text-2xl font-bold text-white tracking-tight flex items-center gap-2.5">
              <BarChart3 className="w-7 h-7 text-cyan-400" />
              Deep Statistical Data Profiler
            </h1>
            <p className="text-slate-400 text-sm mt-1">
              Automated quantile calculations (P1 to P99), skewness, zero-inflation, cardinality metrics, and histogram distributions.
            </p>
          </div>

          <button className="flex items-center gap-1.5 px-4 py-2 rounded-lg bg-cyan-600 hover:bg-cyan-500 text-white text-xs font-semibold shadow-lg shadow-cyan-600/20 transition self-start md:self-auto">
            <Sparkles className="w-4 h-4" /> Run Deep Profile
          </button>
        </div>

        {/* Dataset Summary Cards */}
        <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
          <div className="bg-slate-900 border border-slate-800 rounded-xl p-4">
            <div className="text-xs text-slate-500 font-semibold uppercase">Profiled Dataset</div>
            <div className="text-lg font-bold text-white mt-1 truncate">gold.fact_orders</div>
          </div>
          <div className="bg-slate-900 border border-slate-800 rounded-xl p-4">
            <div className="text-xs text-slate-500 font-semibold uppercase">Total Rows</div>
            <div className="text-2xl font-bold text-cyan-400 mt-1">1,000,000</div>
          </div>
          <div className="bg-slate-900 border border-slate-800 rounded-xl p-4">
            <div className="text-xs text-slate-500 font-semibold uppercase">In-Memory Footprint</div>
            <div className="text-2xl font-bold text-purple-400 mt-1">68.5 MB</div>
          </div>
          <div className="bg-slate-900 border border-slate-800 rounded-xl p-4">
            <div className="text-xs text-slate-500 font-semibold uppercase">Duplicate Rows</div>
            <div className="text-2xl font-bold text-emerald-400 mt-1">0 (0.00%)</div>
          </div>
        </div>

        <DataGrid data={mockProfile} columns={columns} title="Column Statistical Distribution Matrix" />
      </div>
    </MainLayout>
  );
}

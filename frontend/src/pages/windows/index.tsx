import React from 'react';
import Head from 'next/head';
import { MainLayout } from '@/components/layout/MainLayout';
import { DataGrid, DataGridColumn } from '@/components/grid/DataGrid';
import { Sliders, Activity, CheckCircle, Flame, Layers } from 'lucide-react';

interface WindowFunctionSpecItem {
  id: string;
  function_name: string;
  partition_by: string;
  order_by: string;
  frame_clause: string;
  vectorized_speed_m_rows_s: number;
}

const mockWindowSpecs: WindowFunctionSpecItem[] = [
  { id: 'win_01', function_name: 'DENSE_RANK()', partition_by: 'region, product_category', order_by: 'revenue DESC', frame_clause: 'ENTIRE PARTITION', vectorized_speed_m_rows_s: 48.5 },
  { id: 'win_02', function_name: 'LEAD(price, 1)', partition_by: 'asset_symbol', order_by: 'timestamp ASC', frame_clause: 'N/A', vectorized_speed_m_rows_s: 62.0 },
  { id: 'win_03', function_name: 'AVG(amount) (Moving Average)', partition_by: 'customer_id', order_by: 'order_date ASC', frame_clause: 'ROWS BETWEEN 3 PRECEDING AND CURRENT ROW', vectorized_speed_m_rows_s: 34.1 },
];

export default function WindowFunctionsStudioPage() {
  const columns: DataGridColumn<WindowFunctionSpecItem>[] = [
    { key: 'function_name', header: 'Window Analytical Function', render: (w) => <strong className="text-white font-mono">{w.function_name}</strong> },
    { key: 'partition_by', header: 'PARTITION BY Columns', render: (w) => <span className="font-mono text-cyan-300 text-xs">{w.partition_by}</span> },
    { key: 'order_by', header: 'ORDER BY Sequence', render: (w) => <span className="font-mono text-purple-300 text-xs">{w.order_by}</span> },
    { key: 'frame_clause', header: 'Window Frame Specification', render: (w) => <span className="bg-slate-800 text-slate-300 font-mono text-[10px] px-2 py-0.5 rounded">{w.frame_clause}</span> },
    {
      key: 'vectorized_speed_m_rows_s',
      header: 'Vectorized Processing Throughput',
      render: (w) => <span className="font-mono text-emerald-400 font-bold">{w.vectorized_speed_m_rows_s}M rows/s</span>,
    },
  ];

  return (
    <MainLayout>
      <Head>
        <title>Vectorized Window Functions — DataFlowX</title>
      </Head>

      <div className="space-y-6">
        <div>
          <h1 className="text-2xl font-bold text-white tracking-tight flex items-center gap-2.5">
            <Sliders className="w-7 h-7 text-cyan-400" />
            Vectorized Analytical Window Functions Studio
          </h1>
          <p className="text-slate-400 text-sm mt-1">
            SIMD-accelerated ROW_NUMBER(), DENSE_RANK(), LEAD/LAG offsets, and moving average sliding frames.
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <div className="bg-slate-900 border border-slate-800 rounded-xl p-4">
            <div className="text-xs text-slate-500 font-semibold uppercase">Configured Window Operators</div>
            <div className="text-2xl font-bold text-white mt-1">3 Operators</div>
          </div>
          <div className="bg-slate-900 border border-slate-800 rounded-xl p-4">
            <div className="text-xs text-slate-500 font-semibold uppercase">Peak Execution Speed</div>
            <div className="text-2xl font-bold text-emerald-400 mt-1">62.0M rows/s</div>
          </div>
          <div className="bg-slate-900 border border-slate-800 rounded-xl p-4">
            <div className="text-xs text-slate-500 font-semibold uppercase">Memory Model</div>
            <div className="text-2xl font-bold text-cyan-400 mt-1">Zero-Copy Bitmaps</div>
          </div>
        </div>

        <DataGrid data={mockWindowSpecs} columns={columns} title="Active Vectorized Window Expressions" />
      </div>
    </MainLayout>
  );
}

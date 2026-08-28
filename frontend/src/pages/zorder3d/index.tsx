import React from 'react';
import Head from 'next/head';
import { MainLayout } from '@/components/layout/MainLayout';
import { DataGrid, DataGridColumn } from '@/components/grid/DataGrid';
import { Box, Layers, CheckCircle, Flame, Sparkles, ArrowRight } from 'lucide-react';

interface ZOrderItem {
  table_name: string;
  z_columns: string[];
  total_records: string;
  clustering_efficiency_pct: number;
  data_skipping_ratio_pct: number;
  compaction_state: 'OPTIMAL' | 'NEEDS_COMPACTION';
}

const mockZOrders: ZOrderItem[] = [
  { table_name: 'gold.fact_orders', z_columns: ['customer_id', 'order_timestamp', 'region_id'], total_records: '10,000,000 Rows', clustering_efficiency_pct: 96.4, data_skipping_ratio_pct: 92.5, compaction_state: 'OPTIMAL' },
  { table_name: 'silver.iot_telemetry', z_columns: ['device_id', 'sensor_timestamp', 'firmware_ver'], total_records: '45,000,000 Rows', clustering_efficiency_pct: 94.1, data_skipping_ratio_pct: 89.0, compaction_state: 'OPTIMAL' },
  { table_name: 'silver.clickstream_events', z_columns: ['session_id', 'event_timestamp', 'url_path'], total_records: '80,000,000 Rows', clustering_efficiency_pct: 91.8, data_skipping_ratio_pct: 85.4, compaction_state: 'OPTIMAL' },
];

export default function ZOrder3DStudioPage() {
  const columns: DataGridColumn<ZOrderItem>[] = [
    { key: 'table_name', header: 'Clustered Lakehouse Table', render: (z) => <strong className="text-white font-mono text-xs">{z.table_name}</strong> },
    {
      key: 'z_columns',
      header: 'Morton 3D Dimensions (X / Y / Z)',
      render: (z) => (
        <div className="flex flex-wrap gap-1">
          {z.z_columns.map((c) => (
            <span key={c} className="bg-slate-800 text-purple-300 font-mono text-[9px] px-1.5 py-0.2 rounded">
              {c}
            </span>
          ))}
        </div>
      ),
    },
    { key: 'total_records', header: 'Total Clustered Rows', render: (z) => <span className="font-mono text-slate-300">{z.total_records}</span> },
    {
      key: 'clustering_efficiency_pct',
      header: 'Morton Locality Score',
      render: (z) => <span className="font-mono text-emerald-400 font-bold">{z.clustering_efficiency_pct}% Locality</span>,
    },
    {
      key: 'data_skipping_ratio_pct',
      header: 'File Pruning Efficiency',
      render: (z) => <span className="font-mono text-cyan-300 font-bold">{z.data_skipping_ratio_pct}% Pruned</span>,
    },
    {
      key: 'compaction_state',
      header: 'Compaction State',
      render: (z) => (
        <span className="px-2 py-0.5 rounded bg-emerald-950 text-emerald-400 border border-emerald-800 text-[10px] font-bold">
          {z.compaction_state}
        </span>
      ),
    },
  ];

  return (
    <MainLayout>
      <Head>
        <title>3D Morton Z-Order Compaction — DataFlowX</title>
      </Head>

      <div className="space-y-6">
        <div>
          <h1 className="text-2xl font-bold text-white tracking-tight flex items-center gap-2.5">
            <Box className="w-7 h-7 text-cyan-400" />
            3D Morton Space-Filling Curve (Z-Order) Clustering Studio
          </h1>
          <p className="text-slate-400 text-sm mt-1">
            Multidimensional binary bit-interleaved Z-order curve clustering providing symmetric min/max data skipping across 3 dimensions.
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <div className="bg-slate-900 border border-slate-800 rounded-xl p-4">
            <div className="text-xs text-slate-500 font-semibold uppercase">Average Data Skipping</div>
            <div className="text-2xl font-bold text-emerald-400 mt-1">89.0% Files Skipped</div>
          </div>
          <div className="bg-slate-900 border border-slate-800 rounded-xl p-4">
            <div className="text-xs text-slate-500 font-semibold uppercase">Z-Order Bit Resolution</div>
            <div className="text-2xl font-bold text-cyan-400 mt-1">64-Bit Morton Integer</div>
          </div>
          <div className="bg-slate-900 border border-slate-800 rounded-xl p-4">
            <div className="text-xs text-slate-500 font-semibold uppercase">Query Speedup Multiplier</div>
            <div className="text-2xl font-bold text-white mt-1">9.2x Query Acceleration</div>
          </div>
        </div>

        <DataGrid data={mockZOrders} columns={columns} title="Z-Order Clustered Tables" />
      </div>
    </MainLayout>
  );
}

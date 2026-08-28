import React from 'react';
import Head from 'next/head';
import { MainLayout } from '@/components/layout/MainLayout';
import { DataGrid, DataGridColumn } from '@/components/grid/DataGrid';
import { FolderTree, Layers, CheckCircle, Database, GitCommit, ArrowRight } from 'lucide-react';

interface PartitionSpecItem {
  table_name: string;
  spec_id: number;
  partition_transform: string;
  source_column: string;
  partition_count: number;
  status: 'ACTIVE' | 'EVOLVED';
}

const mockSpecs: PartitionSpecItem[] = [
  { table_name: 'gold.fact_orders', spec_id: 1, partition_transform: 'day(order_timestamp)', source_column: 'order_timestamp', partition_count: 365, status: 'ACTIVE' },
  { table_name: 'silver.dim_customers', spec_id: 1, partition_transform: 'bucket[16](customer_id)', source_column: 'customer_id', partition_count: 16, status: 'ACTIVE' },
  { table_name: 'bronze.iot_telemetry', spec_id: 2, partition_transform: 'hour(recorded_at)', source_column: 'recorded_at', partition_count: 720, status: 'ACTIVE' },
];

export default function PartitionsStudioPage() {
  const columns: DataGridColumn<PartitionSpecItem>[] = [
    { key: 'table_name', header: 'Lakehouse Table', render: (p) => <strong className="text-white font-mono">{p.table_name}</strong> },
    { key: 'spec_id', header: 'Spec Version', render: (p) => <span className="font-mono text-cyan-300 font-bold">spec_v{p.spec_id}</span> },
    {
      key: 'partition_transform',
      header: 'Iceberg Partition Transform',
      render: (p) => <span className="bg-slate-800 text-purple-400 font-mono text-[10px] px-2 py-0.5 rounded">{p.partition_transform}</span>,
    },
    { key: 'source_column', header: 'Source Field', render: (p) => <span className="font-mono text-slate-300 text-xs">{p.source_column}</span> },
    { key: 'partition_count', header: 'Active Partitions', render: (p) => <span className="font-mono text-emerald-400 font-bold">{p.partition_count} dirs</span> },
    {
      key: 'status',
      header: 'Status',
      render: (p) => (
        <span className="px-2 py-0.5 rounded bg-emerald-950 text-emerald-400 border border-emerald-800 text-[10px] font-bold">
          {p.status}
        </span>
      ),
    },
  ];

  return (
    <MainLayout>
      <Head>
        <title>Iceberg Hidden Partitioning & Spec Evolution — DataFlowX</title>
      </Head>

      <div className="space-y-6">
        <div>
          <h1 className="text-2xl font-bold text-white tracking-tight flex items-center gap-2.5">
            <FolderTree className="w-7 h-7 text-cyan-400" />
            Iceberg Hidden Partitioning & Spec Evolution Studio
          </h1>
          <p className="text-slate-400 text-sm mt-1">
            Zero-rewrite partition evolution, bucket/truncate/day transforms, and partition pruning optimizations.
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <div className="bg-slate-900 border border-slate-800 rounded-xl p-4">
            <div className="text-xs text-slate-500 font-semibold uppercase">Total Managed Partition Specs</div>
            <div className="text-2xl font-bold text-white mt-1">3 Specs</div>
          </div>
          <div className="bg-slate-900 border border-slate-800 rounded-xl p-4">
            <div className="text-xs text-slate-500 font-semibold uppercase">Average Partition Pruning</div>
            <div className="text-2xl font-bold text-emerald-400 mt-1">96.2% Pruned</div>
          </div>
          <div className="bg-slate-900 border border-slate-800 rounded-xl p-4">
            <div className="text-xs text-slate-500 font-semibold uppercase">Evolution Overhead</div>
            <div className="text-2xl font-bold text-cyan-400 mt-1">0ms (Zero Data Movement)</div>
          </div>
        </div>

        <DataGrid data={mockSpecs} columns={columns} title="Lakehouse Partition Specs & Transforms" />
      </div>
    </MainLayout>
  );
}

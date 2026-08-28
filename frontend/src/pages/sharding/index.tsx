import React from 'react';
import Head from 'next/head';
import { MainLayout } from '@/components/layout/MainLayout';
import { DataGrid, DataGridColumn } from '@/components/grid/DataGrid';
import { PieChart, Server, Layers, CheckCircle, RefreshCw, Cpu } from 'lucide-react';

interface StorageShardItem {
  shard_id: string;
  assigned_node: string;
  key_range: string;
  total_records: number;
  storage_size_mb: number;
  rebalance_status: 'SYNCED' | 'MIGRATING';
}

const mockShards: StorageShardItem[] = [
  { shard_id: 'shard_001', assigned_node: 'worker-node-1', key_range: '[00000000 - 3FFFFFFF]', total_records: 4500000, storage_size_mb: 480.0, rebalance_status: 'SYNCED' },
  { shard_id: 'shard_002', assigned_node: 'worker-node-2', key_range: '[40000000 - 7FFFFFFF]', total_records: 4800000, storage_size_mb: 512.0, rebalance_status: 'SYNCED' },
  { shard_id: 'shard_003', assigned_node: 'worker-node-3', key_range: '[80000000 - BFFFFFFF]', total_records: 4200000, storage_size_mb: 450.0, rebalance_status: 'SYNCED' },
  { shard_id: 'shard_004', assigned_node: 'worker-node-4', key_range: '[C0000000 - FFFFFFFF]', total_records: 5100000, storage_size_mb: 540.0, rebalance_status: 'SYNCED' },
];

export default function StorageShardingPage() {
  const columns: DataGridColumn<StorageShardItem>[] = [
    {
      key: 'shard_id',
      header: 'Shard ID',
      render: (s) => (
        <div className="flex items-center gap-2">
          <Server className="w-4 h-4 text-cyan-400" />
          <strong className="text-white font-mono text-xs">{s.shard_id}</strong>
        </div>
      ),
    },
    { key: 'assigned_node', header: 'Assigned Physical Worker', render: (s) => <span className="font-mono text-slate-300 text-xs">{s.assigned_node}</span> },
    { key: 'key_range', header: 'Consistent Hash Range', render: (s) => <span className="bg-slate-800 text-purple-300 font-mono text-[10px] px-2 py-0.5 rounded">{s.key_range}</span> },
    { key: 'total_records', header: 'Total Shard Rows', render: (s) => <span className="font-mono text-emerald-400 font-bold">{s.total_records.toLocaleString()}</span> },
    { key: 'storage_size_mb', header: 'Storage Footprint', render: (s) => <span className="font-mono text-cyan-300">{s.storage_size_mb} MB</span> },
    {
      key: 'rebalance_status',
      header: 'Cluster State',
      render: (s) => (
        <span className="px-2 py-0.5 rounded bg-emerald-950 text-emerald-400 border border-emerald-800 text-[10px] font-bold">
          {s.rebalance_status}
        </span>
      ),
    },
  ];

  return (
    <MainLayout>
      <Head>
        <title>Storage Sharding & Consistent Hashing — DataFlowX</title>
      </Head>

      <div className="space-y-6">
        <div>
          <h1 className="text-2xl font-bold text-white tracking-tight flex items-center gap-2.5">
            <PieChart className="w-7 h-7 text-cyan-400" />
            Storage Sharding & Consistent Hash Ring Architecture
          </h1>
          <p className="text-slate-400 text-sm mt-1">
            256-vnode consistent hashing ring, range partition routing, and zero-downtime shard migration rebalancing.
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <div className="bg-slate-900 border border-slate-800 rounded-xl p-4">
            <div className="text-xs text-slate-500 font-semibold uppercase">Total Storage Shards</div>
            <div className="text-2xl font-bold text-white mt-1">4 Shards</div>
          </div>
          <div className="bg-slate-900 border border-slate-800 rounded-xl p-4">
            <div className="text-xs text-slate-500 font-semibold uppercase">Key Distribution Variance</div>
            <div className="text-2xl font-bold text-emerald-400 mt-1">±1.8% (Uniform)</div>
          </div>
          <div className="bg-slate-900 border border-slate-800 rounded-xl p-4">
            <div className="text-xs text-slate-500 font-semibold uppercase">Rebalance Migration State</div>
            <div className="text-2xl font-bold text-cyan-400 mt-1">100% Balanced</div>
          </div>
        </div>

        <DataGrid data={mockShards} columns={columns} title="Active Storage Shard Distribution" />
      </div>
    </MainLayout>
  );
}

import React from 'react';
import Head from 'next/head';
import { MainLayout } from '@/components/layout/MainLayout';
import { DataGrid, DataGridColumn } from '@/components/grid/DataGrid';
import { Database, Activity, CheckCircle, Clock, Layers, Flame } from 'lucide-react';

interface KeyedStateItem {
  state_name: string;
  state_type: 'VALUE_STATE' | 'LIST_STATE' | 'MAP_STATE' | 'REDUCING_STATE';
  operator_id: string;
  total_keys: number;
  memory_size_mb: number;
  ttl_policy: string;
  status: 'ACTIVE' | 'CLEANING';
}

const mockKeyedState: KeyedStateItem[] = [
  { state_name: 'user_session_activity_state', state_type: 'VALUE_STATE', operator_id: 'op_session_counter_01', total_keys: 145000, memory_size_mb: 28.5, ttl_policy: 'TTL 30 minutes on last update', status: 'ACTIVE' },
  { state_name: 'order_history_accumulator', state_type: 'LIST_STATE', operator_id: 'op_order_aggregator_02', total_keys: 82000, memory_size_mb: 64.0, ttl_policy: 'TTL 7 days', status: 'ACTIVE' },
  { state_name: 'feature_vector_lookup_map', state_type: 'MAP_STATE', operator_id: 'op_ml_feature_store_03', total_keys: 310000, memory_size_mb: 180.2, ttl_policy: 'No Expiry (Persistent)', status: 'ACTIVE' },
];

export default function KeyedStateStudioPage() {
  const columns: DataGridColumn<KeyedStateItem>[] = [
    {
      key: 'state_name',
      header: 'Keyed State Descriptor',
      render: (k) => (
        <div className="flex items-center gap-2">
          <Database className="w-4 h-4 text-cyan-400" />
          <strong className="text-white font-mono text-xs">{k.state_name}</strong>
        </div>
      ),
    },
    {
      key: 'state_type',
      header: 'State Backend Model',
      render: (k) => <span className="bg-slate-800 text-purple-300 font-mono text-[10px] px-2 py-0.5 rounded">{k.state_type}</span>,
    },
    { key: 'operator_id', header: 'Streaming Operator', render: (k) => <span className="font-mono text-slate-300 text-xs">{k.operator_id}</span> },
    {
      key: 'total_keys',
      header: 'Managed Key Partitions',
      render: (k) => <span className="font-mono text-cyan-300 font-bold">{k.total_keys.toLocaleString()} keys</span>,
    },
    {
      key: 'memory_size_mb',
      header: 'State Memory (RocksDB)',
      render: (k) => <span className="font-mono text-emerald-400 font-bold">{k.memory_size_mb.toFixed(1)} MB</span>,
    },
    { key: 'ttl_policy', header: 'State TTL & Eviction', render: (k) => <span className="text-slate-300 text-xs">{k.ttl_policy}</span> },
  ];

  return (
    <MainLayout>
      <Head>
        <title>Keyed State Store Management — DataFlowX</title>
      </Head>

      <div className="space-y-6">
        <div>
          <h1 className="text-2xl font-bold text-white tracking-tight flex items-center gap-2.5">
            <Database className="w-7 h-7 text-cyan-400" />
            Keyed State Store & RocksDB State Backend Management
          </h1>
          <p className="text-slate-400 text-sm mt-1">
            ValueState, ListState, MapState, and ReducingState partitions with state TTL compaction and distributed RocksDB persistence.
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <div className="bg-slate-900 border border-slate-800 rounded-xl p-4">
            <div className="text-xs text-slate-500 font-semibold uppercase">Total Managed Key Partitions</div>
            <div className="text-2xl font-bold text-white mt-1">537,000 Keys</div>
          </div>
          <div className="bg-slate-900 border border-slate-800 rounded-xl p-4">
            <div className="text-xs text-slate-500 font-semibold uppercase">Total RocksDB State Size</div>
            <div className="text-2xl font-bold text-emerald-400 mt-1">272.7 MB</div>
          </div>
          <div className="bg-slate-900 border border-slate-800 rounded-xl p-4">
            <div className="text-xs text-slate-500 font-semibold uppercase">State TTL Engine</div>
            <div className="text-2xl font-bold text-cyan-400 mt-1">Active Cleanup</div>
          </div>
        </div>

        <DataGrid data={mockKeyedState} columns={columns} title="Active Keyed State Operators" />
      </div>
    </MainLayout>
  );
}

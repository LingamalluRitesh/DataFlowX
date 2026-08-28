import React from 'react';
import Head from 'next/head';
import { MainLayout } from '@/components/layout/MainLayout';
import { DataGrid, DataGridColumn } from '@/components/grid/DataGrid';
import { Database, Zap, CheckCircle, Clock, Layers, Sparkles } from 'lucide-react';

interface FeatureViewItem {
  view_name: string;
  entity_key: string;
  feature_count: number;
  online_latency_ms: number;
  offline_table: string;
  ttl_hours: number;
  sync_status: 'SYNCED' | 'INGESTING';
}

const mockFeatureViews: FeatureViewItem[] = [
  { view_name: 'user_fraud_risk_features', entity_key: 'user_id', feature_count: 32, online_latency_ms: 0.85, offline_table: 'gold.user_features_v2', ttl_hours: 24, sync_status: 'SYNCED' },
  { view_name: 'item_collaborative_embedding_view', entity_key: 'item_id', feature_count: 128, online_latency_ms: 1.10, offline_table: 'gold.item_features_v1', ttl_hours: 72, sync_status: 'SYNCED' },
  { view_name: 'merchant_daily_chargeback_rate', entity_key: 'merchant_id', feature_count: 16, online_latency_ms: 0.65, offline_table: 'silver.merchant_metrics', ttl_hours: 12, sync_status: 'SYNCED' },
];

export default function FeatureStoreV2Page() {
  const columns: DataGridColumn<FeatureViewItem>[] = [
    {
      key: 'view_name',
      header: 'Feature View',
      render: (f) => (
        <div className="flex items-center gap-2">
          <Database className="w-4 h-4 text-cyan-400" />
          <strong className="text-white font-mono text-xs">{f.view_name}</strong>
        </div>
      ),
    },
    { key: 'entity_key', header: 'Entity Primary Key', render: (f) => <span className="bg-slate-800 text-purple-300 font-mono text-[10px] px-2 py-0.5 rounded">{f.entity_key}</span> },
    { key: 'feature_count', header: 'Registered Features', render: (f) => <span className="font-mono text-slate-300">{f.feature_count} features</span> },
    {
      key: 'online_latency_ms',
      header: 'Redis Point Lookup',
      render: (f) => <span className="font-mono text-emerald-400 font-bold">{f.online_latency_ms} ms</span>,
    },
    { key: 'offline_table', header: 'Offline Lakehouse Table', render: (f) => <span className="font-mono text-cyan-300 text-xs">{f.offline_table}</span> },
    { key: 'ttl_hours', header: 'Online TTL', render: (f) => <span className="font-mono text-slate-300">{f.ttl_hours}h</span> },
    {
      key: 'sync_status',
      header: 'Sync State',
      render: (f) => (
        <span className="px-2 py-0.5 rounded bg-emerald-950 text-emerald-400 border border-emerald-800 text-[10px] font-bold">
          {f.sync_status}
        </span>
      ),
    },
  ];

  return (
    <MainLayout>
      <Head>
        <title>Dual Online-Offline Feature Store — DataFlowX</title>
      </Head>

      <div className="space-y-6">
        <div>
          <h1 className="text-2xl font-bold text-white tracking-tight flex items-center gap-2.5">
            <Zap className="w-7 h-7 text-cyan-400" />
            Dual Online-Offline Machine Learning Feature Store Registry
          </h1>
          <p className="text-slate-400 text-sm mt-1">
            Low-latency sub-millisecond online key-value feature retrieval and point-in-time correct Lakehouse time-travel training joins.
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <div className="bg-slate-900 border border-slate-800 rounded-xl p-4">
            <div className="text-xs text-slate-500 font-semibold uppercase">Total Feature Views</div>
            <div className="text-2xl font-bold text-white mt-1">3 Active Views</div>
          </div>
          <div className="bg-slate-900 border border-slate-800 rounded-xl p-4">
            <div className="text-xs text-slate-500 font-semibold uppercase">P99 Online Read Latency</div>
            <div className="text-2xl font-bold text-emerald-400 mt-1">0.85 ms (Redis Backend)</div>
          </div>
          <div className="bg-slate-900 border border-slate-800 rounded-xl p-4">
            <div className="text-xs text-slate-500 font-semibold uppercase">Point-in-Time Correctness</div>
            <div className="text-2xl font-bold text-cyan-400 mt-1">100% Guaranteed</div>
          </div>
        </div>

        <DataGrid data={mockFeatureViews} columns={columns} title="Managed ML Feature Views" />
      </div>
    </MainLayout>
  );
}

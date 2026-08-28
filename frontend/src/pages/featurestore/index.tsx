import React from 'react';
import Head from 'next/head';
import { MainLayout } from '@/components/layout/MainLayout';
import { DataGrid, DataGridColumn } from '@/components/grid/DataGrid';
import { Cpu, Plus, Sparkles, Database, CheckCircle, Activity, Zap } from 'lucide-react';

interface FeatureViewItem {
  id: string;
  name: string;
  entity_id_column: string;
  feature_count: number;
  online_enabled: boolean;
  psi_drift_score: number;
  status: 'SERVING' | 'STALE';
}

const mockFeatureViews: FeatureViewItem[] = [
  { id: 'fv_user_rfm', name: 'user_rfm_features', entity_id_column: 'customer_id', feature_count: 8, online_enabled: true, psi_drift_score: 0.042, status: 'SERVING' },
  { id: 'fv_merchant_risk', name: 'merchant_fraud_risk_signals', entity_id_column: 'merchant_id', feature_count: 14, online_enabled: true, psi_drift_score: 0.089, status: 'SERVING' },
  { id: 'fv_item_affinity', name: 'product_cooccurrence_embeddings', entity_id_column: 'sku_id', feature_count: 64, online_enabled: false, psi_drift_score: 0.021, status: 'SERVING' },
];

export default function FeatureStoreIndexPage() {
  const columns: DataGridColumn<FeatureViewItem>[] = [
    {
      key: 'name',
      header: 'Feature View Identifier',
      render: (f) => (
        <div className="flex items-center gap-2">
          <Cpu className="w-4 h-4 text-cyan-400" />
          <strong className="text-white font-mono">{f.name}</strong>
        </div>
      ),
    },
    { key: 'entity_id_column', header: 'Entity Primary Key', render: (f) => <span className="font-mono text-cyan-300 font-semibold">{f.entity_id_column}</span> },
    { key: 'feature_count', header: 'Features', render: (f) => <span className="font-mono text-slate-300">{f.feature_count} features</span> },
    {
      key: 'online_enabled',
      header: 'Low-Latency Online Serving',
      render: (f) => (
        <span
          className={`px-2 py-0.5 rounded text-[10px] font-bold ${
            f.online_enabled
              ? 'bg-emerald-950 text-emerald-400 border border-emerald-800'
              : 'bg-slate-800 text-slate-400'
          }`}
        >
          {f.online_enabled ? 'ONLINE (REDIS)' : 'OFFLINE ONLY'}
        </span>
      ),
    },
    {
      key: 'psi_drift_score',
      header: 'Population Stability Index (PSI)',
      render: (f) => (
        <span className={`font-mono font-bold ${f.psi_drift_score < 0.1 ? 'text-emerald-400' : 'text-amber-400'}`}>
          PSI: {f.psi_drift_score} {f.psi_drift_score < 0.1 ? '(No Drift)' : '(Moderate)'}
        </span>
      ),
    },
    {
      key: 'status',
      header: 'Status',
      render: (f) => (
        <span className="px-2 py-0.5 rounded bg-emerald-950 text-emerald-400 border border-emerald-800 text-[10px] font-bold">
          {f.status}
        </span>
      ),
    },
  ];

  return (
    <MainLayout>
      <Head>
        <title>ML Feature Store & Drift Monitoring — DataFlowX</title>
      </Head>

      <div className="space-y-6">
        <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
          <div>
            <h1 className="text-2xl font-bold text-white tracking-tight flex items-center gap-2.5">
              <Cpu className="w-7 h-7 text-cyan-400" />
              Machine Learning Feature Store & Drift Monitor
            </h1>
            <p className="text-slate-400 text-sm mt-1">
              Point-in-time correct historical training dataset generation, low-latency online serving, and continuous PSI feature drift detection.
            </p>
          </div>

          <button className="flex items-center gap-1.5 px-4 py-2 rounded-lg bg-cyan-600 hover:bg-cyan-500 text-white text-xs font-semibold shadow-lg shadow-cyan-600/20 transition self-start md:self-auto">
            <Plus className="w-4 h-4" /> Register Feature View
          </button>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <div className="bg-slate-900 border border-slate-800 rounded-xl p-4">
            <div className="text-xs text-slate-500 font-semibold uppercase">Registered Features</div>
            <div className="text-2xl font-bold text-white mt-1">86 Features</div>
          </div>
          <div className="bg-slate-900 border border-slate-800 rounded-xl p-4">
            <div className="text-xs text-slate-500 font-semibold uppercase">Online P99 Lookup Latency</div>
            <div className="text-2xl font-bold text-emerald-400 mt-1">3.8 ms</div>
          </div>
          <div className="bg-slate-900 border border-slate-800 rounded-xl p-4">
            <div className="text-xs text-slate-500 font-semibold uppercase">Feature Drift Health</div>
            <div className="text-2xl font-bold text-cyan-400 mt-1">100% Stable</div>
          </div>
        </div>

        <DataGrid data={mockFeatureViews} columns={columns} title="Active Machine Learning Feature Views" />
      </div>
    </MainLayout>
  );
}

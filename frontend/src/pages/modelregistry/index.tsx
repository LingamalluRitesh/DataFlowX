import React from 'react';
import Head from 'next/head';
import { MainLayout } from '@/components/layout/MainLayout';
import { DataGrid, DataGridColumn } from '@/components/grid/DataGrid';
import { Award, Layers, CheckCircle, Clock, Sparkles, ArrowRight } from 'lucide-react';

interface ModelRegistryItem {
  model_name: string;
  version: string;
  training_snapshot: string;
  roc_auc: number;
  f1_score: number;
  stage: 'PRODUCTION' | 'STAGING' | 'EXPERIMENT';
  registered_time: string;
}

const mockModels: ModelRegistryItem[] = [
  { model_name: 'fraud_detection_xgboost_v4', version: 'v4.2.0', training_snapshot: 'gold.fact_orders@v140', roc_auc: 0.984, f1_score: 0.942, stage: 'PRODUCTION', registered_time: '2026-08-29 00:10 UTC' },
  { model_name: 'churn_prediction_lightgbm', version: 'v2.1.0', training_snapshot: 'gold.user_features_v2@v88', roc_auc: 0.912, f1_score: 0.885, stage: 'PRODUCTION', registered_time: '2026-08-28 18:30 UTC' },
  { model_name: 'revenue_forecasting_transformer', version: 'v1.0.0', training_snapshot: 'gold.daily_financials@v45', roc_auc: 0.945, f1_score: 0.910, stage: 'STAGING', registered_time: '2026-08-29 00:20 UTC' },
];

export default function ModelRegistryPage() {
  const columns: DataGridColumn<ModelRegistryItem>[] = [
    {
      key: 'model_name',
      header: 'Model Artifact Name',
      render: (m) => (
        <div>
          <strong className="text-white font-mono text-xs">{m.model_name}</strong>
          <div className="text-[10px] text-cyan-400 font-mono">{m.version}</div>
        </div>
      ),
    },
    { key: 'training_snapshot', header: 'Training Dataset Version', render: (m) => <span className="bg-slate-800 text-purple-300 font-mono text-[10px] px-2 py-0.5 rounded">{m.training_snapshot}</span> },
    {
      key: 'roc_auc',
      header: 'ROC-AUC Metric',
      render: (m) => <span className="font-mono text-emerald-400 font-bold">{m.roc_auc.toFixed(3)}</span>,
    },
    {
      key: 'f1_score',
      header: 'F1 Score',
      render: (m) => <span className="font-mono text-cyan-300 font-bold">{m.f1_score.toFixed(3)}</span>,
    },
    {
      key: 'stage',
      header: 'Deployment Stage',
      render: (m) => (
        <span
          className={`px-2 py-0.5 rounded text-[10px] font-bold ${
            m.stage === 'PRODUCTION'
              ? 'bg-emerald-950 text-emerald-400 border border-emerald-800'
              : 'bg-purple-950 text-purple-400 border border-purple-800'
          }`}
        >
          {m.stage}
        </span>
      ),
    },
    { key: 'registered_time', header: 'Registration Time', render: (m) => <span className="font-mono text-slate-400 text-xs">{m.registered_time}</span> },
  ];

  return (
    <MainLayout>
      <Head>
        <title>ML Model Registry & Dataset Lineage — DataFlowX</title>
      </Head>

      <div className="space-y-6">
        <div>
          <h1 className="text-2xl font-bold text-white tracking-tight flex items-center gap-2.5">
            <Award className="w-7 h-7 text-cyan-400" />
            Machine Learning Model Artifact Registry & Dataset Lineage
          </h1>
          <p className="text-slate-400 text-sm mt-1">
            Tracking model weights, hyperparameters, ROC-AUC evaluation metrics, and point-in-time training dataset snapshot versions.
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <div className="bg-slate-900 border border-slate-800 rounded-xl p-4">
            <div className="text-xs text-slate-500 font-semibold uppercase">Models in Production</div>
            <div className="text-2xl font-bold text-white mt-1">2 Production Models</div>
          </div>
          <div className="bg-slate-900 border border-slate-800 rounded-xl p-4">
            <div className="text-xs text-slate-500 font-semibold uppercase">Average Model ROC-AUC</div>
            <div className="text-2xl font-bold text-emerald-400 mt-1">0.947 (High Accuracy)</div>
          </div>
          <div className="bg-slate-900 border border-slate-800 rounded-xl p-4">
            <div className="text-xs text-slate-500 font-semibold uppercase">Dataset Snapshot Lineage</div>
            <div className="text-2xl font-bold text-cyan-400 mt-1">100% Tracked</div>
          </div>
        </div>

        <DataGrid data={mockModels} columns={columns} title="Registered Machine Learning Models" />
      </div>
    </MainLayout>
  );
}

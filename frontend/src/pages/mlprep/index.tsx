import React from 'react';
import Head from 'next/head';
import { MainLayout } from '@/components/layout/MainLayout';
import { DataGrid, DataGridColumn } from '@/components/grid/DataGrid';
import { Sparkles, Cpu, CheckCircle, Sliders, Layers, ArrowRight } from 'lucide-react';

interface MLPrepPipelineItem {
  id: string;
  pipeline_name: string;
  encoder_steps: string[];
  scaler_steps: string[];
  train_split_pct: number;
  total_output_features: number;
  status: 'READY' | 'FITTING';
}

const mockMLPipelines: MLPrepPipelineItem[] = [
  { id: 'ml_pipe_01', pipeline_name: 'customer_churn_feature_prep', encoder_steps: ['OneHotEncoder(country, tier)'], scaler_steps: ['StandardScaler(age, tenure, balance)'], train_split_pct: 80, total_output_features: 24, status: 'READY' },
  { id: 'ml_pipe_02', pipeline_name: 'credit_risk_scoring_prep', encoder_steps: ['OneHotEncoder(employment_type)'], scaler_steps: ['RobustScaler(income, debt_ratio)'], train_split_pct: 80, total_output_features: 38, status: 'READY' },
];

export default function MLPrepStudioPage() {
  const columns: DataGridColumn<MLPrepPipelineItem>[] = [
    {
      key: 'pipeline_name',
      header: 'ML Feature Pipeline',
      render: (p) => (
        <div>
          <strong className="text-white font-mono text-xs">{p.pipeline_name}</strong>
          <div className="text-[10px] text-slate-500 font-mono">{p.id}</div>
        </div>
      ),
    },
    {
      key: 'encoder_steps',
      header: 'Categorical Encoders',
      render: (p) => (
        <div className="flex flex-wrap gap-1">
          {p.encoder_steps.map((s) => (
            <span key={s} className="bg-slate-800 text-purple-300 font-mono text-[9px] px-1.5 py-0.2 rounded">
              {s}
            </span>
          ))}
        </div>
      ),
    },
    {
      key: 'scaler_steps',
      header: 'Numerical Scalers',
      render: (p) => (
        <div className="flex flex-wrap gap-1">
          {p.scaler_steps.map((s) => (
            <span key={s} className="bg-slate-800 text-cyan-300 font-mono text-[9px] px-1.5 py-0.2 rounded">
              {s}
            </span>
          ))}
        </div>
      ),
    },
    { key: 'total_output_features', header: 'Output Features', render: (p) => <span className="font-mono text-emerald-400 font-bold">{p.total_output_features} features</span> },
    { key: 'train_split_pct', header: 'Train/Test Split', render: (p) => <span className="font-mono text-slate-300">{p.train_split_pct}% / {100 - p.train_split_pct}%</span> },
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
        <title>ML Feature Engineering & Prep Studio — DataFlowX</title>
      </Head>

      <div className="space-y-6">
        <div>
          <h1 className="text-2xl font-bold text-white tracking-tight flex items-center gap-2.5">
            <Sparkles className="w-7 h-7 text-cyan-400" />
            Machine Learning Feature Engineering & Prep Studio
          </h1>
          <p className="text-slate-400 text-sm mt-1">
            Composable feature pipelines with Vectorized One-Hot Encoders, Standard/Robust scalers, and chronological train/test splitters.
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <div className="bg-slate-900 border border-slate-800 rounded-xl p-4">
            <div className="text-xs text-slate-500 font-semibold uppercase">Configured Feature Pipelines</div>
            <div className="text-2xl font-bold text-white mt-1">2 Pipelines</div>
          </div>
          <div className="bg-slate-900 border border-slate-800 rounded-xl p-4">
            <div className="text-xs text-slate-500 font-semibold uppercase">Transformation Speed</div>
            <div className="text-2xl font-bold text-emerald-400 mt-1">1.4M rows / sec</div>
          </div>
          <div className="bg-slate-900 border border-slate-800 rounded-xl p-4">
            <div className="text-xs text-slate-500 font-semibold uppercase">Export Formats</div>
            <div className="text-2xl font-bold text-cyan-400 mt-1">Parquet, NumPy, Arrow</div>
          </div>
        </div>

        <DataGrid data={mockMLPipelines} columns={columns} title="Active ML Feature Preprocessing Pipelines" />
      </div>
    </MainLayout>
  );
}

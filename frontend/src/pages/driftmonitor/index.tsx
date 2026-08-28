import React from 'react';
import Head from 'next/head';
import { MainLayout } from '@/components/layout/MainLayout';
import { DataGrid, DataGridColumn } from '@/components/grid/DataGrid';
import { AlertTriangle, TrendingUp, CheckCircle, Activity, Layers, Sparkles } from 'lucide-react';

interface FeatureDriftItem {
  feature_name: string;
  test_type: 'PSI' | 'KS_TEST' | 'CHI_SQUARE';
  drift_score: number;
  threshold: number;
  baseline_mean: number;
  current_mean: number;
  drift_status: 'STABLE' | 'DRIFTED';
}

const mockDrifts: FeatureDriftItem[] = [
  { feature_name: 'transaction_amount_usd', test_type: 'PSI', drift_score: 0.042, threshold: 0.20, baseline_mean: 142.50, current_mean: 145.10, drift_status: 'STABLE' },
  { feature_name: 'user_days_since_signup', test_type: 'KS_TEST', drift_score: 0.015, threshold: 0.05, baseline_mean: 85.0, current_mean: 87.2, drift_status: 'STABLE' },
  { feature_name: 'payment_method_category', test_type: 'CHI_SQUARE', drift_score: 0.082, threshold: 0.20, baseline_mean: 2.1, current_mean: 2.2, drift_status: 'STABLE' },
];

export default function FeatureDriftMonitorPage() {
  const columns: DataGridColumn<FeatureDriftItem>[] = [
    { key: 'feature_name', header: 'Target ML Feature', render: (d) => <strong className="text-white font-mono text-xs">{d.feature_name}</strong> },
    {
      key: 'test_type',
      header: 'Statistical Test',
      render: (d) => <span className="bg-slate-800 text-purple-300 font-mono text-[10px] px-2 py-0.5 rounded">{d.test_type}</span>,
    },
    {
      key: 'drift_score',
      header: 'Drift Score (PSI)',
      render: (d) => (
        <span className={`font-mono font-bold ${d.drift_score >= d.threshold ? 'text-amber-400' : 'text-emerald-400'}`}>
          {d.drift_score.toFixed(4)}
        </span>
      ),
    },
    { key: 'threshold', header: 'Warning Threshold', render: (d) => <span className="font-mono text-slate-400">≥ {d.threshold}</span> },
    {
      key: 'baseline_mean',
      header: 'Distribution Shift (Base / Current)',
      render: (d) => (
        <span className="font-mono text-xs text-slate-300">
          {d.baseline_mean.toFixed(2)} → <span className="text-cyan-300 font-bold">{d.current_mean.toFixed(2)}</span>
        </span>
      ),
    },
    {
      key: 'drift_status',
      header: 'Drift State',
      render: (d) => (
        <span className="px-2 py-0.5 rounded bg-emerald-950 text-emerald-400 border border-emerald-800 text-[10px] font-bold">
          {d.drift_status}
        </span>
      ),
    },
  ];

  return (
    <MainLayout>
      <Head>
        <title>ML Feature Drift & Statistical Profiling — DataFlowX</title>
      </Head>

      <div className="space-y-6">
        <div>
          <h1 className="text-2xl font-bold text-white tracking-tight flex items-center gap-2.5">
            <Activity className="w-7 h-7 text-cyan-400" />
            Machine Learning Feature & Concept Drift Monitoring Hub
          </h1>
          <p className="text-slate-400 text-sm mt-1">
            Population Stability Index (PSI), 2-Sample Kolmogorov-Smirnov statistical tests, and automated concept drift alerting.
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <div className="bg-slate-900 border border-slate-800 rounded-xl p-4">
            <div className="text-xs text-slate-500 font-semibold uppercase">Monitored ML Features</div>
            <div className="text-2xl font-bold text-white mt-1">3 Features</div>
          </div>
          <div className="bg-slate-900 border border-slate-800 rounded-xl p-4">
            <div className="text-xs text-slate-500 font-semibold uppercase">Drift Alert Incidents</div>
            <div className="text-2xl font-bold text-emerald-400 mt-1">0 Alerts (Stable)</div>
          </div>
          <div className="bg-slate-900 border border-slate-800 rounded-xl p-4">
            <div className="text-xs text-slate-500 font-semibold uppercase">Drift Test Standard</div>
            <div className="text-2xl font-bold text-cyan-400 mt-1">Evidently / PSI 0.2</div>
          </div>
        </div>

        <DataGrid data={mockDrifts} columns={columns} title="Feature Distribution Drift Metrics" />
      </div>
    </MainLayout>
  );
}

import React from 'react';
import Head from 'next/head';
import { MainLayout } from '@/components/layout/MainLayout';
import { DataGrid, DataGridColumn } from '@/components/grid/DataGrid';
import { ShieldCheck, Award, CheckCircle, TrendingUp, Sparkles, Layers } from 'lucide-react';

interface DatasetTrustItem {
  table_name: string;
  trust_score: number;
  badge_tier: 'GOLD_CERTIFIED' | 'SILVER_VALIDATED' | 'BRONZE_INGESTED';
  quality_subscore: number;
  freshness_subscore: number;
  volume_stability_subscore: number;
  sla_status: 'SLA_MET' | 'AT_RISK';
}

const mockTrustScores: DatasetTrustItem[] = [
  { table_name: 'gold.fact_orders', trust_score: 98.5, badge_tier: 'GOLD_CERTIFIED', quality_subscore: 40.0, freshness_subscore: 25.0, volume_stability_subscore: 19.5, sla_status: 'SLA_MET' },
  { table_name: 'silver.dim_customers', trust_score: 94.0, badge_tier: 'GOLD_CERTIFIED', quality_subscore: 38.0, freshness_subscore: 25.0, volume_stability_subscore: 18.0, sla_status: 'SLA_MET' },
  { table_name: 'bronze.iot_telemetry', trust_score: 82.5, badge_tier: 'SILVER_VALIDATED', quality_subscore: 32.0, freshness_subscore: 20.0, volume_stability_subscore: 16.5, sla_status: 'SLA_MET' },
];

export default function TrustIndexStudioPage() {
  const columns: DataGridColumn<DatasetTrustItem>[] = [
    { key: 'table_name', header: 'Lakehouse Dataset', render: (t) => <strong className="text-white font-mono text-xs">{t.table_name}</strong> },
    {
      key: 'badge_tier',
      header: 'Certification Badge',
      render: (t) => (
        <span
          className={`px-2.5 py-1 rounded text-xs font-bold flex items-center gap-1.5 w-fit ${
            t.badge_tier === 'GOLD_CERTIFIED'
              ? 'bg-emerald-950 text-emerald-400 border border-emerald-800'
              : 'bg-cyan-950 text-cyan-400 border border-cyan-800'
          }`}
        >
          <Award className="w-3.5 h-3.5" /> {t.badge_tier}
        </span>
      ),
    },
    {
      key: 'trust_score',
      header: 'Composite Trust Score',
      render: (t) => <span className="font-mono text-emerald-400 font-bold text-sm">{t.trust_score} / 100</span>,
    },
    {
      key: 'quality_subscore',
      header: 'Component Breakdown (Q / F / V)',
      render: (t) => (
        <span className="font-mono text-xs text-slate-300">
          Q: {t.quality_subscore} | F: {t.freshness_subscore} | V: {t.volume_stability_subscore}
        </span>
      ),
    },
    {
      key: 'sla_status',
      header: 'Trust SLA Compliance',
      render: (t) => (
        <span className="px-2 py-0.5 rounded bg-emerald-950 text-emerald-400 border border-emerald-800 text-[10px] font-bold">
          {t.sla_status}
        </span>
      ),
    },
  ];

  return (
    <MainLayout>
      <Head>
        <title>Lakehouse Trust Index & Quality Certification — DataFlowX</title>
      </Head>

      <div className="space-y-6">
        <div>
          <h1 className="text-2xl font-bold text-white tracking-tight flex items-center gap-2.5">
            <ShieldCheck className="w-7 h-7 text-emerald-400" />
            Lakehouse Trust Index & Data Quality Certification
          </h1>
          <p className="text-slate-400 text-sm mt-1">
            Automated composite data trust scoring combining assertion pass rates, freshness SLAs, and schema health into consumer certification badges.
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <div className="bg-slate-900 border border-slate-800 rounded-xl p-4">
            <div className="text-xs text-slate-500 font-semibold uppercase">Average Platform Trust Score</div>
            <div className="text-2xl font-bold text-emerald-400 mt-1">91.7 / 100 (AAA Grade)</div>
          </div>
          <div className="bg-slate-900 border border-slate-800 rounded-xl p-4">
            <div className="text-xs text-slate-500 font-semibold uppercase">Gold Certified Datasets</div>
            <div className="text-2xl font-bold text-cyan-400 mt-1">2 Datasets</div>
          </div>
          <div className="bg-slate-900 border border-slate-800 rounded-xl p-4">
            <div className="text-xs text-slate-500 font-semibold uppercase">Trust SLA Breaches (30d)</div>
            <div className="text-2xl font-bold text-white mt-1">0 Breaches</div>
          </div>
        </div>

        <DataGrid data={mockTrustScores} columns={columns} title="Dataset Certification & Trust Index Scores" />
      </div>
    </MainLayout>
  );
}

import React from 'react';
import Head from 'next/head';
import { MainLayout } from '@/components/layout/MainLayout';
import { DataGrid, DataGridColumn } from '@/components/grid/DataGrid';
import { Sparkles, ShieldCheck, AlertOctagon, CheckCircle, RefreshCw, Layers } from 'lucide-react';

interface AutoHealingJobItem {
  id: string;
  target_dataset: string;
  healed_records: number;
  dlq_quarantined: number;
  imputation_strategy: string;
  outlier_clipping: string;
  status: 'COMPLETED' | 'HEALING';
}

const mockHealingJobs: AutoHealingJobItem[] = [
  { id: 'heal_01', target_dataset: 'gold.fact_orders', healed_records: 1420, dlq_quarantined: 3, imputation_strategy: 'MEDIAN (order_total)', outlier_clipping: 'Z-Score 3.0σ', status: 'COMPLETED' },
  { id: 'heal_02', target_dataset: 'silver.dim_customers', healed_records: 890, dlq_quarantined: 0, imputation_strategy: 'MODE (country_code)', outlier_clipping: 'IQR 1.5x', status: 'COMPLETED' },
  { id: 'heal_03', target_dataset: 'bronze.iot_telemetry', healed_records: 12400, dlq_quarantined: 45, imputation_strategy: 'FORWARD_FILL', outlier_clipping: 'Z-Score 3.5σ', status: 'COMPLETED' },
];

export default function AutoHealingPage() {
  const columns: DataGridColumn<AutoHealingJobItem>[] = [
    {
      key: 'target_dataset',
      header: 'Target Dataset',
      render: (h) => (
        <div>
          <strong className="text-white font-mono">{h.target_dataset}</strong>
          <div className="text-[10px] text-slate-500 font-mono">{h.id}</div>
        </div>
      ),
    },
    { key: 'healed_records', header: 'Repaired Records', render: (h) => <span className="font-mono text-emerald-400 font-bold">+{h.healed_records.toLocaleString()} rows</span> },
    {
      key: 'dlq_quarantined',
      header: 'Quarantined DLQ Records',
      render: (h) => (
        <span className={`font-mono font-semibold ${h.dlq_quarantined > 0 ? 'text-amber-400' : 'text-slate-400'}`}>
          {h.dlq_quarantined} rows
        </span>
      ),
    },
    { key: 'imputation_strategy', header: 'Imputation Strategy', render: (h) => <span className="bg-slate-800 text-cyan-300 font-mono text-[10px] px-2 py-0.5 rounded">{h.imputation_strategy}</span> },
    { key: 'outlier_clipping', header: 'Outlier Bounds', render: (h) => <span className="bg-slate-800 text-purple-300 font-mono text-[10px] px-2 py-0.5 rounded">{h.outlier_clipping}</span> },
    {
      key: 'status',
      header: 'Status',
      render: (h) => (
        <span className="px-2 py-0.5 rounded bg-emerald-950 text-emerald-400 border border-emerald-800 text-[10px] font-bold">
          {h.status}
        </span>
      ),
    },
  ];

  return (
    <MainLayout>
      <Head>
        <title>Automated Data Quality Healing & DLQ — DataFlowX</title>
      </Head>

      <div className="space-y-6">
        <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
          <div>
            <h1 className="text-2xl font-bold text-white tracking-tight flex items-center gap-2.5">
              <Sparkles className="w-7 h-7 text-emerald-400" />
              Automated Data Quality Healing & DLQ Quarantine
            </h1>
            <p className="text-slate-400 text-sm mt-1">
              Statistical missing value imputation, outlier winsorization, and automatic Dead-Letter-Queue (DLQ) partition isolation.
            </p>
          </div>

          <button className="flex items-center gap-1.5 px-4 py-2 rounded-lg bg-cyan-600 hover:bg-cyan-500 text-white text-xs font-semibold shadow-lg shadow-cyan-600/20 transition self-start md:self-auto">
            <RefreshCw className="w-4 h-4" /> Trigger Auto-Heal Job
          </button>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <div className="bg-slate-900 border border-slate-800 rounded-xl p-4">
            <div className="text-xs text-slate-500 font-semibold uppercase">Total Repaired Records (30d)</div>
            <div className="text-2xl font-bold text-emerald-400 mt-1">14,710 Records</div>
          </div>
          <div className="bg-slate-900 border border-slate-800 rounded-xl p-4">
            <div className="text-xs text-slate-500 font-semibold uppercase">Quarantined to Dead-Letter Queue</div>
            <div className="text-2xl font-bold text-amber-400 mt-1">48 Records</div>
          </div>
          <div className="bg-slate-900 border border-slate-800 rounded-xl p-4">
            <div className="text-xs text-slate-500 font-semibold uppercase">Data Recovery Rate</div>
            <div className="text-2xl font-bold text-cyan-400 mt-1">99.67%</div>
          </div>
        </div>

        <DataGrid data={mockHealingJobs} columns={columns} title="Automated Healing Execution History" />
      </div>
    </MainLayout>
  );
}

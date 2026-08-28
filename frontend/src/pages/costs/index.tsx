import React from 'react';
import Head from 'next/head';
import { MainLayout } from '@/components/layout/MainLayout';
import { DataGrid, DataGridColumn } from '@/components/grid/DataGrid';
import { DollarSign, TrendingDown, Server, HardDrive, ArrowUpRight, Zap, CheckCircle } from 'lucide-react';

interface CostRecItem {
  id: string;
  category: 'STORAGE' | 'COMPUTE' | 'NETWORK';
  dataset: string;
  title: string;
  monthly_savings_usd: number;
  impact: 'HIGH' | 'MEDIUM' | 'LOW';
  action_status: 'RECOMMENDED' | 'APPLIED';
}

const mockCostRecs: CostRecItem[] = [
  { id: 'cost_01', category: 'STORAGE', dataset: 'bronze.raw_telemetry_csv', title: 'Convert 4.8 TB CSV files to Parquet with Snappy compression', monthly_savings_usd: 82.50, impact: 'HIGH', action_status: 'RECOMMENDED' },
  { id: 'cost_02', category: 'COMPUTE', dataset: 'gold.fact_orders', title: 'Add partition pruning by created_date to reduce BigQuery scan slots', monthly_savings_usd: 145.00, impact: 'HIGH', action_status: 'RECOMMENDED' },
  { id: 'cost_03', category: 'STORAGE', dataset: 'silver.api_payload_archive', title: 'Set S3 Glacier Instant Retrieval lifecycle policy on 90d+ partitions', monthly_savings_usd: 64.20, impact: 'MEDIUM', action_status: 'RECOMMENDED' },
];

export default function CostsIndexPage() {
  const columns: DataGridColumn<CostRecItem>[] = [
    {
      key: 'title',
      header: 'Optimization Recommendation',
      render: (c) => (
        <div>
          <strong className="text-white">{c.title}</strong>
          <div className="text-xs text-cyan-400 font-mono mt-0.5">{c.dataset}</div>
        </div>
      ),
    },
    {
      key: 'category',
      header: 'Category',
      render: (c) => <span className="bg-slate-800 text-slate-300 font-mono text-[10px] px-2 py-0.5 rounded">{c.category}</span>,
    },
    {
      key: 'monthly_savings_usd',
      header: 'Est. Monthly Savings',
      render: (c) => <span className="font-mono text-emerald-400 font-extrabold text-sm">+${c.monthly_savings_usd.toFixed(2)}/mo</span>,
    },
    {
      key: 'impact',
      header: 'Impact',
      render: (c) => (
        <span
          className={`px-2 py-0.5 rounded text-[10px] font-bold ${
            c.impact === 'HIGH'
              ? 'bg-emerald-950 text-emerald-400 border border-emerald-800'
              : 'bg-amber-950 text-amber-400 border border-amber-800'
          }`}
        >
          {c.impact} IMPACT
        </span>
      ),
    },
    {
      key: 'action_status',
      header: 'Action',
      render: (c) => (
        <button className="px-3 py-1 rounded bg-cyan-600 hover:bg-cyan-500 text-white text-xs font-semibold shadow transition">
          Apply Optimization
        </button>
      ),
    },
  ];

  return (
    <MainLayout>
      <Head>
        <title>Cost Optimization Advisor — DataFlowX</title>
      </Head>

      <div className="space-y-6">
        <div>
          <h1 className="text-2xl font-bold text-white tracking-tight flex items-center gap-2.5">
            <DollarSign className="w-7 h-7 text-emerald-400" />
            Storage & Compute Cost Optimization Advisor
          </h1>
          <p className="text-slate-400 text-sm mt-1">
            Automated recommendations to reduce cloud warehouse compute charges, optimize Parquet compression, and prune unneeded storage tiers.
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <div className="bg-slate-900 border border-slate-800 rounded-xl p-5 shadow-lg">
            <div className="text-xs text-slate-500 font-semibold uppercase">Total Monthly Savings Identified</div>
            <div className="text-3xl font-extrabold text-emerald-400 mt-2">$291.70 / mo</div>
            <div className="text-xs text-slate-400 mt-1">~$3,500.40 projected annual savings</div>
          </div>
          <div className="bg-slate-900 border border-slate-800 rounded-xl p-5 shadow-lg">
            <div className="text-xs text-slate-500 font-semibold uppercase">Total Data Scanned (30d)</div>
            <div className="text-3xl font-extrabold text-cyan-400 mt-2">18.4 TB</div>
            <div className="text-xs text-slate-400 mt-1">Down 24% after partition pruning</div>
          </div>
          <div className="bg-slate-900 border border-slate-800 rounded-xl p-5 shadow-lg">
            <div className="text-xs text-slate-500 font-semibold uppercase">Optimized Lakehouse Tables</div>
            <div className="text-3xl font-extrabold text-purple-400 mt-2">8 of 12 Tables</div>
            <div className="text-xs text-slate-400 mt-1">Snappy columnar format applied</div>
          </div>
        </div>

        <DataGrid data={mockCostRecs} columns={columns} title="Cost Reduction Recommendations" />
      </div>
    </MainLayout>
  );
}

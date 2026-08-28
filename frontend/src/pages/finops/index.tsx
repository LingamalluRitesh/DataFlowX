import React from 'react';
import Head from 'next/head';
import { MainLayout } from '@/components/layout/MainLayout';
import { DataGrid, DataGridColumn } from '@/components/grid/DataGrid';
import { DollarSign, TrendingDown, Server, HardDrive, CheckCircle, ArrowRight } from 'lucide-react';

interface FinOpsRecommendationItem {
  id: string;
  category: 'STORAGE_TIERING' | 'IDLE_CLUSTER' | 'QUERY_OPTIMIZATION';
  resource_target: string;
  monthly_savings_usd: number;
  implementation_effort: 'AUTOMATED' | 'LOW' | 'MEDIUM';
}

const mockFinOps: FinOpsRecommendationItem[] = [
  { id: 'fin_01', category: 'STORAGE_TIERING', resource_target: 's3://lakehouse/bronze/iot_telemetry (older than 90d)', monthly_savings_usd: 153.00, implementation_effort: 'AUTOMATED' },
  { id: 'fin_02', category: 'IDLE_CLUSTER', resource_target: 'Ad-hoc Spark cluster "spark-adhoc-01" (idle 45m)', monthly_savings_usd: 320.00, implementation_effort: 'AUTOMATED' },
  { id: 'fin_03', category: 'QUERY_OPTIMIZATION', resource_target: 'BigQuery unpartitioned full-scan query "etl_orders"', monthly_savings_usd: 84.50, implementation_effort: 'LOW' },
];

export default function FinOpsStudioPage() {
  const columns: DataGridColumn<FinOpsRecommendationItem>[] = [
    {
      key: 'resource_target',
      header: 'Cloud Resource Target',
      render: (f) => (
        <div>
          <strong className="text-white text-xs">{f.resource_target}</strong>
          <div className="text-[10px] text-slate-500 font-mono">{f.id}</div>
        </div>
      ),
    },
    {
      key: 'category',
      header: 'Optimization Category',
      render: (f) => <span className="bg-slate-800 text-purple-400 font-mono text-[10px] px-2 py-0.5 rounded">{f.category}</span>,
    },
    {
      key: 'monthly_savings_usd',
      header: 'Projected Monthly Savings',
      render: (f) => <span className="font-mono text-emerald-400 font-bold">${f.monthly_savings_usd.toFixed(2)} / mo</span>,
    },
    {
      key: 'implementation_effort',
      header: 'Effort Level',
      render: (f) => (
        <span className="px-2 py-0.5 rounded bg-cyan-950 text-cyan-400 border border-cyan-800 text-[10px] font-bold">
          {f.implementation_effort}
        </span>
      ),
    },
    {
      key: 'id',
      header: 'Action',
      render: (f) => (
        <button className="flex items-center gap-1 px-3 py-1 rounded bg-cyan-600 hover:bg-cyan-500 text-white text-xs font-semibold shadow transition">
          Apply Savings
        </button>
      ),
    },
  ];

  return (
    <MainLayout>
      <Head>
        <title>FinOps & Cloud Cost Optimization — DataFlowX</title>
      </Head>

      <div className="space-y-6">
        <div>
          <h1 className="text-2xl font-bold text-white tracking-tight flex items-center gap-2.5">
            <DollarSign className="w-7 h-7 text-emerald-400" />
            FinOps & Cloud Data Cost Optimization Hub
          </h1>
          <p className="text-slate-400 text-sm mt-1">
            Compute waste detection, BigQuery/Snowflake query cost estimations, and automated S3/GCS storage lifecycle tiering.
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <div className="bg-slate-900 border border-slate-800 rounded-xl p-4">
            <div className="text-xs text-slate-500 font-semibold uppercase">Total Identified Monthly Savings</div>
            <div className="text-2xl font-bold text-emerald-400 mt-1">$557.50 / mo</div>
          </div>
          <div className="bg-slate-900 border border-slate-800 rounded-xl p-4">
            <div className="text-xs text-slate-500 font-semibold uppercase">Realized Cost Reduction (YTD)</div>
            <div className="text-2xl font-bold text-cyan-400 mt-1">32.4% Saved</div>
          </div>
          <div className="bg-slate-900 border border-slate-800 rounded-xl p-4">
            <div className="text-xs text-slate-500 font-semibold uppercase">Automated Actions Ready</div>
            <div className="text-2xl font-bold text-white mt-1">2 Actions</div>
          </div>
        </div>

        <DataGrid data={mockFinOps} columns={columns} title="Cost Optimization Recommendations" />
      </div>
    </MainLayout>
  );
}

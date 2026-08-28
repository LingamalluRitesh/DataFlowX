import React from 'react';
import Head from 'next/head';
import { MainLayout } from '@/components/layout/MainLayout';
import { DataGrid, DataGridColumn } from '@/components/grid/DataGrid';
import { DollarSign, PieChart, TrendingDown, CheckCircle, ArrowRight, Layers } from 'lucide-react';

interface CostAttributionItem {
  team_name: string;
  domain: string;
  monthly_spend_usd: number;
  compute_hours: number;
  storage_tb: number;
  cost_trend_pct: number;
  budget_status: 'WITHIN_BUDGET' | 'WARNING';
}

const mockCosts: CostAttributionItem[] = [
  { team_name: 'Risk & Fraud Analytics', domain: 'Security', monthly_spend_usd: 12450.00, compute_hours: 4200, storage_tb: 45.2, cost_trend_pct: -8.4, budget_status: 'WITHIN_BUDGET' },
  { team_name: 'Core Growth Intelligence', domain: 'Marketing', monthly_spend_usd: 8900.00, compute_hours: 2800, storage_tb: 28.6, cost_trend_pct: -3.2, budget_status: 'WITHIN_BUDGET' },
  { team_name: 'Supply Chain Optimization', domain: 'Logistics', monthly_spend_usd: 6420.00, compute_hours: 1950, storage_tb: 18.0, cost_trend_pct: +1.5, budget_status: 'WITHIN_BUDGET' },
  { team_name: 'Executive & Financial Reporting', domain: 'Finance', monthly_spend_usd: 4800.00, compute_hours: 1400, storage_tb: 12.4, cost_trend_pct: -12.0, budget_status: 'WITHIN_BUDGET' },
];

export default function CostAttributionPage() {
  const columns: DataGridColumn<CostAttributionItem>[] = [
    { key: 'team_name', header: 'Team / Business Unit', render: (c) => <strong className="text-white font-mono text-xs">{c.team_name}</strong> },
    { key: 'domain', header: 'Mesh Domain', render: (c) => <span className="bg-slate-800 text-purple-300 font-mono text-[10px] px-2 py-0.5 rounded">{c.domain}</span> },
    {
      key: 'monthly_spend_usd',
      header: 'Current Month Spend',
      render: (c) => <span className="font-mono text-emerald-400 font-bold text-sm">${c.monthly_spend_usd.toLocaleString(undefined, { minimumFractionDigits: 2 })}</span>,
    },
    { key: 'compute_hours', header: 'Compute Allocated', render: (c) => <span className="font-mono text-slate-300">{c.compute_hours.toLocaleString()} core-hrs</span> },
    { key: 'storage_tb', header: 'Lakehouse Storage', render: (c) => <span className="font-mono text-cyan-300">{c.storage_tb} TB</span> },
    {
      key: 'cost_trend_pct',
      header: 'Month-over-Month Trend',
      render: (c) => (
        <span className={`font-mono font-bold ${c.cost_trend_pct < 0 ? 'text-emerald-400' : 'text-amber-400'}`}>
          {c.cost_trend_pct > 0 ? `+${c.cost_trend_pct}%` : `${c.cost_trend_pct}%`}
        </span>
      ),
    },
    {
      key: 'budget_status',
      header: 'FinOps Budget State',
      render: (c) => (
        <span className="px-2 py-0.5 rounded bg-emerald-950 text-emerald-400 border border-emerald-800 text-[10px] font-bold">
          {c.budget_status}
        </span>
      ),
    },
  ];

  return (
    <MainLayout>
      <Head>
        <title>FinOps Cost Attribution & Showback — DataFlowX</title>
      </Head>

      <div className="space-y-6">
        <div>
          <h1 className="text-2xl font-bold text-white tracking-tight flex items-center gap-2.5">
            <DollarSign className="w-7 h-7 text-emerald-400" />
            FinOps Team Cost Attribution & Showback Center
          </h1>
          <p className="text-slate-400 text-sm mt-1">
            Fine-grained multi-tenant cost allocation, query compute showback, and automated idle resource waste prevention.
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <div className="bg-slate-900 border border-slate-800 rounded-xl p-4">
            <div className="text-xs text-slate-500 font-semibold uppercase">Total Platform Monthly Spend</div>
            <div className="text-2xl font-bold text-white mt-1">$32,570.00</div>
          </div>
          <div className="bg-slate-900 border border-slate-800 rounded-xl p-4">
            <div className="text-xs text-slate-500 font-semibold uppercase">FinOps Optimization Savings</div>
            <div className="text-2xl font-bold text-emerald-400 mt-1">$4,180.00 / mo</div>
          </div>
          <div className="bg-slate-900 border border-slate-800 rounded-xl p-4">
            <div className="text-xs text-slate-500 font-semibold uppercase">Tracked Business Units</div>
            <div className="text-2xl font-bold text-cyan-400 mt-1">4 Units</div>
          </div>
        </div>

        <DataGrid data={mockCosts} columns={columns} title="Team Showback & Spend Allocation" />
      </div>
    </MainLayout>
  );
}
